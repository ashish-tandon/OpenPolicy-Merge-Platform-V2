"""
House Status API for OpenPolicy V2

Comprehensive real-time parliamentary house status system with WebSocket integration.
This implements a P2 priority feature for enhanced user engagement and transparency.
"""

from fastapi import APIRouter, HTTPException, Query, Depends, Path, Body, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_, desc
from typing import Optional
from datetime import datetime
import math
import json
import asyncio

from app.database import get_db
from app.models.house_status import (
    HouseSession, HouseSitting, HouseVote, IndividualVote, HouseDebate, 
    HouseStatus, HouseEvent
)
from app.schemas.house_status import (
    HouseSessionResponse, HouseSittingResponse, HouseVoteResponse, IndividualVoteResponse,
    HouseDebateResponse, HouseStatusResponse, HouseEventResponse,
    HouseSessionListResponse, HouseSittingListResponse, HouseVoteListResponse,
    HouseDebateListResponse, HouseEventListResponse,
    HouseSessionCreateRequest, HouseSessionUpdateRequest, HouseSittingCreateRequest,
    HouseVoteCreateRequest, IndividualVoteCreateRequest, HouseDebateCreateRequest,
    HouseStatusUpdateRequest, HouseEventCreateRequest,
    HouseEventUpdateRequest, HouseStatusStatistics
)
from app.api.v1.auth import get_current_user
from app.models.users import User
import structlog

logger = structlog.get_logger(__name__)
router = APIRouter()


# ============================================================================
# HOUSE SESSIONS
# ============================================================================

@router.post("/sessions", response_model=HouseSessionResponse)
async def create_house_session(
    session_data: HouseSessionCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new house session.
    
    This is typically used by administrators to set up new parliamentary sessions.
    """
    # Check if session number already exists
    existing_session = db.query(HouseSession).filter(
        HouseSession.session_number == session_data.session_number
    ).first()
    
    if existing_session:
        raise HTTPException(
            status_code=400,
            detail=f"Session number {session_data.session_number} already exists"
        )
    
    # Create new session
    session = HouseSession(**session_data.dict())
    db.add(session)
    db.commit()
    db.refresh(session)
    
    logger.info(f"House session created: {current_user.username} - {session_data.session_name}")
    
    return HouseSessionResponse(
        id=str(session.id),
        session_number=session.session_number,
        session_name=session.session_name,
        parliament_number=session.parliament_number,
        start_date=session.start_date,
        end_date=session.end_date,
        is_active=session.is_active,
        status=session.status,
        government_party=session.government_party,
        opposition_leader=session.opposition_leader,
        speaker=session.speaker,
        created_at=session.created_at,
        updated_at=session.updated_at
    )


@router.get("/sessions", response_model=HouseSessionListResponse)
async def list_house_sessions(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    parliament_number: Optional[int] = Query(None, description="Filter by parliament number"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    status: Optional[str] = Query(None, description="Filter by session status"),
    db: DBSession = Depends(get_db)
):
    """
    List house sessions with filtering and pagination.
    """
    # Build base query
    query = db.query(HouseSession)
    
    # Apply filters
    if parliament_number:
        query = query.filter(HouseSession.parliament_number == parliament_number)
    
    if is_active is not None:
        query = query.filter(HouseSession.is_active == is_active)
    
    if status:
        query = query.filter(HouseSession.status == status)
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get sessions
    sessions = query.order_by(desc(HouseSession.start_date)).offset(offset).limit(page_size).all()
    
    # Convert to response format
    session_responses = []
    for session in sessions:
        session_responses.append(HouseSessionResponse(
            id=str(session.id),
            session_number=session.session_number,
            session_name=session.session_name,
            parliament_number=session.parliament_number,
            start_date=session.start_date,
            end_date=session.end_date,
            is_active=session.is_active,
            status=session.status,
            government_party=session.government_party,
            opposition_leader=session.opposition_leader,
            speaker=session.speaker,
            created_at=session.created_at,
            updated_at=session.updated_at
        ))
    
    return HouseSessionListResponse(
        sessions=session_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


@router.get("/sessions/{session_id}", response_model=HouseSessionResponse)
async def get_house_session(
    session_id: str = Path(..., description="Session ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get a specific house session by ID.
    """
    session = db.query(HouseSession).filter(HouseSession.id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="House session not found")
    
    return HouseSessionResponse(
        id=str(session.id),
        session_number=session.session_number,
        session_name=session.session_name,
        parliament_number=session.parliament_number,
        start_date=session.start_date,
        end_date=session.end_date,
        is_active=session.is_active,
        status=session.status,
        government_party=session.government_party,
        opposition_leader=session.opposition_leader,
        speaker=session.speaker,
        created_at=session.created_at,
        updated_at=session.updated_at
    )


@router.put("/sessions/{session_id}", response_model=HouseSessionResponse)
async def update_house_session(
    session_id: str = Path(..., description="Session ID"),
    session_data: HouseSessionUpdateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a house session.
    """
    session = db.query(HouseSession).filter(HouseSession.id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="House session not found")
    
    # Update session fields
    update_data = session_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(session, field):
            setattr(session, field, value)
    
    session.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(session)
    
    logger.info(f"House session updated: {current_user.username} - {session.session_name}")
    
    return HouseSessionResponse(
        id=str(session.id),
        session_number=session.session_number,
        session_name=session.session_name,
        parliament_number=session.parliament_number,
        start_date=session.start_date,
        end_date=session.end_date,
        is_active=session.is_active,
        status=session.status,
        government_party=session.government_party,
        opposition_leader=session.opposition_leader,
        speaker=session.speaker,
        created_at=session.created_at,
        updated_at=session.updated_at
    )


# ============================================================================
# HOUSE SITTINGS
# ============================================================================

@router.post("/sessions/{session_id}/sittings", response_model=HouseSittingResponse)
async def create_house_sitting(
    session_id: str = Path(..., description="Session ID"),
    sitting_data: HouseSittingCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new house sitting within a session.
    """
    # Verify session exists
    session = db.query(HouseSession).filter(HouseSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="House session not found")
    
    # Create new sitting
    sitting = HouseSitting(**sitting_data.dict())
    sitting.session_id = session_id
    db.add(sitting)
    db.commit()
    db.refresh(sitting)
    
    logger.info(f"House sitting created: {current_user.username} - Session {session.session_number}")
    
    return HouseSittingResponse(
        id=str(sitting.id),
        session_id=str(sitting.session_id),
        sitting_number=sitting.sitting_number,
        sitting_date=sitting.sitting_date,
        start_time=sitting.start_time,
        end_time=sitting.end_time,
        is_active=sitting.is_active,
        status=sitting.status,
        quorum_present=sitting.quorum_present,
        members_present=sitting.members_present,
        total_members=sitting.total_members,
        agenda_items=sitting.agenda_items,
        notes=sitting.notes,
        created_at=sitting.created_at,
        updated_at=sitting.updated_at
    )


@router.get("/sessions/{session_id}/sittings", response_model=HouseSittingListResponse)
async def list_house_sittings(
    session_id: str = Path(..., description="Session ID"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    status: Optional[str] = Query(None, description="Filter by sitting status"),
    db: DBSession = Depends(get_db)
):
    """
    List house sittings for a specific session.
    """
    # Verify session exists
    session = db.query(HouseSession).filter(HouseSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="House session not found")
    
    # Build base query
    query = db.query(HouseSitting).filter(HouseSitting.session_id == session_id)
    
    # Apply filters
    if is_active is not None:
        query = query.filter(HouseSitting.is_active == is_active)
    
    if status:
        query = query.filter(HouseSitting.status == status)
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get sittings
    sittings = query.order_by(desc(HouseSitting.sitting_date)).offset(offset).limit(page_size).all()
    
    # Convert to response format
    sitting_responses = []
    for sitting in sittings:
        sitting_responses.append(HouseSittingResponse(
            id=str(sitting.id),
            session_id=str(sitting.session_id),
            sitting_number=sitting.sitting_number,
            sitting_date=sitting.sitting_date,
            start_time=sitting.start_time,
            end_time=sitting.end_time,
            is_active=sitting.is_active,
            status=sitting.status,
            quorum_present=sitting.quorum_present,
            members_present=sitting.members_present,
            total_members=sitting.total_members,
            agenda_items=sitting.agenda_items,
            notes=sitting.notes,
            created_at=sitting.created_at,
            updated_at=sitting.updated_at
        ))
    
    return HouseSittingListResponse(
        sittings=sitting_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


# ============================================================================
# HOUSE VOTES
# ============================================================================

@router.post("/sessions/{session_id}/votes", response_model=HouseVoteResponse)
async def create_house_vote(
    session_id: str = Path(..., description="Session ID"),
    vote_data: HouseVoteCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new house vote within a session.
    """
    # Verify session exists
    session = db.query(HouseSession).filter(HouseSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="House session not found")
    
    # Create new vote
    vote = HouseVote(**vote_data.dict())
    vote.session_id = session_id
    db.add(vote)
    db.commit()
    db.refresh(vote)
    
    logger.info(f"House vote created: {current_user.username} - Vote {vote.vote_number}")
    
    return HouseVoteResponse(
        id=str(vote.id),
        session_id=str(vote.session_id),
        sitting_id=str(vote.sitting_id) if vote.sitting_id else None,
        vote_number=vote.vote_number,
        bill_id=vote.bill_id,
        motion_text=vote.motion_text,
        vote_type=vote.vote_type,
        status=vote.status,
        start_time=vote.start_time,
        end_time=vote.end_time,
        duration_minutes=vote.duration_minutes,
        total_votes_cast=vote.total_votes_cast,
        yeas=vote.yeas,
        nays=vote.nays,
        abstentions=vote.abstentions,
        result=vote.result,
        requires_royal_assent=vote.requires_royal_assent,
        royal_assent_date=vote.royal_assent_date,
        vote_metadata=vote.vote_metadata,
        created_at=vote.created_at,
        updated_at=vote.updated_at
    )


@router.get("/sessions/{session_id}/votes", response_model=HouseVoteListResponse)
async def list_house_votes(
    session_id: str = Path(..., description="Session ID"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by vote status"),
    vote_type: Optional[str] = Query(None, description="Filter by vote type"),
    db: DBSession = Depends(get_db)
):
    """
    List house votes for a specific session.
    """
    # Verify session exists
    session = db.query(HouseSession).filter(HouseSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="House session not found")
    
    # Build base query
    query = db.query(HouseVote).filter(HouseVote.session_id == session_id)
    
    # Apply filters
    if status:
        query = query.filter(HouseVote.status == status)
    
    if vote_type:
        query = query.filter(HouseVote.vote_type == vote_type)
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get votes
    votes = query.order_by(desc(HouseVote.vote_number)).offset(offset).limit(page_size).all()
    
    # Convert to response format
    vote_responses = []
    for vote in votes:
        vote_responses.append(HouseVoteResponse(
            id=str(vote.id),
            session_id=str(vote.session_id),
            sitting_id=str(vote.sitting_id) if vote.sitting_id else None,
            vote_number=vote.vote_number,
            bill_id=vote.bill_id,
            motion_text=vote.motion_text,
            vote_type=vote.vote_type,
            status=vote.status,
            start_time=vote.start_time,
            end_time=vote.end_time,
            duration_minutes=vote.duration_minutes,
            total_votes_cast=vote.total_votes_cast,
            yeas=vote.yeas,
            nays=vote.nays,
            abstentions=vote.abstentions,
            result=vote.result,
            requires_royal_assent=vote.requires_royal_assent,
            royal_assent_date=vote.royal_assent_date,
            metadata=vote.metadata,
            created_at=vote.created_at,
            updated_at=vote.updated_at
        ))
    
    return HouseVoteListResponse(
        votes=vote_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


# ============================================================================
# INDIVIDUAL VOTES
# ============================================================================

@router.post("/votes/{vote_id}/individual-votes", response_model=IndividualVoteResponse)
async def create_individual_vote(
    vote_id: str = Path(..., description="House vote ID"),
    vote_data: IndividualVoteCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create an individual vote for a house vote.
    """
    # Verify house vote exists
    house_vote = db.query(HouseVote).filter(HouseVote.id == vote_id).first()
    if not house_vote:
        raise HTTPException(status_code=404, detail="House vote not found")
    
    # Check if member already voted
    existing_vote = db.query(IndividualVote).filter(
        and_(
            IndividualVote.house_vote_id == vote_id,
            IndividualVote.member_id == vote_data.member_id
        )
    ).first()
    
    if existing_vote:
        raise HTTPException(
            status_code=400,
            detail=f"Member {vote_data.member_id} has already voted on this motion"
        )
    
    # Create new individual vote
    vote = IndividualVote(**vote_data.dict())
    vote.house_vote_id = vote_id
    db.add(vote)
    db.commit()
    db.refresh(vote)
    
    logger.info(f"Individual vote created: {current_user.username} - Member {vote.member_id}")
    
    return IndividualVoteResponse(
        id=str(vote.id),
        house_vote_id=str(vote.house_vote_id),
        member_id=vote.member_id,
        member_name=vote.member_name,
        party=vote.party,
        riding=vote.riding,
        vote_cast=vote.vote_cast,
        vote_time=vote.vote_time,
        is_paired=vote.is_paired,
        paired_with=vote.paired_with,
        whip_status=vote.whip_status,
        created_at=vote.created_at
    )


# ============================================================================
# HOUSE DEBATES
# ============================================================================

@router.post("/sessions/{session_id}/debates", response_model=HouseDebateResponse)
async def create_house_debate(
    session_id: str = Path(..., description="Session ID"),
    debate_data: HouseDebateCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new house debate within a session.
    """
    # Verify session exists
    session = db.query(HouseSession).filter(HouseSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="House session not found")
    
    # Create new debate
    debate = HouseDebate(**debate_data.dict())
    debate.session_id = session_id
    db.add(debate)
    db.commit()
    db.refresh(debate)
    
    logger.info(f"House debate created: {current_user.username} - {debate.subject}")
    
    return HouseDebateResponse(
        id=str(debate.id),
        session_id=str(debate.session_id),
        sitting_id=str(debate.sitting_id) if debate.sitting_id else None,
        debate_type=debate.debate_type,
        subject=debate.subject,
        bill_id=debate.bill_id,
        status=debate.status,
        start_time=debate.start_time,
        end_time=debate.end_time,
        current_speaker=debate.current_speaker,
        time_allocation_minutes=debate.time_allocation_minutes,
        time_used_minutes=debate.time_used_minutes,
        speakers_list=debate.speakers_list,
        current_amendment=debate.current_amendment,
        closure_motion=debate.closure_motion,
        created_at=debate.created_at,
        updated_at=debate.updated_at
    )


# ============================================================================
# HOUSE STATUS
# ============================================================================

@router.get("/status/current", response_model=HouseStatusResponse)
async def get_current_house_status(
    db: DBSession = Depends(get_db)
):
    """
    Get the current real-time house status.
    """
    # Get the most recent house status
    status = db.query(HouseStatus).order_by(desc(HouseStatus.last_updated)).first()
    
    if not status:
        # Create default status if none exists
        status = HouseStatus(
            house_status="sitting",
            sitting_status="in_progress",
            voting_status="none",
            debate_status="none",
            members_present=0,
            quorum_met=True,
            current_time=datetime.utcnow(),
            update_source="system"
        )
        db.add(status)
        db.commit()
        db.refresh(status)
    
    return HouseStatusResponse(
        id=str(status.id),
        current_session_id=str(status.current_session_id) if status.current_session_id else None,
        current_sitting_id=str(status.current_sitting_id) if status.current_sitting_id else None,
        current_vote_id=str(status.current_vote_id) if status.current_vote_id else None,
        current_debate_id=str(status.current_debate_id) if status.current_debate_id else None,
        house_status=status.house_status,
        sitting_status=status.sitting_status,
        voting_status=status.voting_status,
        debate_status=status.debate_status,
        members_present=status.members_present,
        quorum_met=status.quorum_met,
        current_time=status.current_time,
        next_scheduled_event=status.next_scheduled_event,
        next_event_time=status.next_event_time,
        question_period_status=status.question_period_status,
        emergency_debate_requested=status.emergency_debate_requested,
        closure_motion_active=status.closure_motion_active,
        update_source=status.update_source,
        notes=status.notes,
        last_updated=status.last_updated
    )


@router.put("/status/current", response_model=HouseStatusResponse)
async def update_current_house_status(
    status_data: HouseStatusUpdateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update the current house status.
    """
    # Get the most recent house status
    status = db.query(HouseStatus).order_by(desc(HouseStatus.last_updated)).first()
    
    if not status:
        # Create new status if none exists
        status = HouseStatus(
            house_status="sitting",
            sitting_status="in_progress",
            voting_status="none",
            debate_status="none",
            members_present=0,
            quorum_met=True,
            current_time=datetime.utcnow(),
            update_source="user"
        )
        db.add(status)
    else:
        # Update existing status
        status.current_time = datetime.utcnow()
        status.update_source = "user"
    
    # Update status fields
    update_data = status_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(status, field):
            setattr(status, field, value)
    
    db.commit()
    db.refresh(status)
    
    logger.info(f"House status updated: {current_user.username}")
    
    return HouseStatusResponse(
        id=str(status.id),
        current_session_id=str(status.current_session_id) if status.current_session_id else None,
        current_sitting_id=str(status.current_sitting_id) if status.current_sitting_id else None,
        current_vote_id=str(status.current_vote_id) if status.current_vote_id else None,
        current_debate_id=str(status.current_debate_id) if status.current_debate_id else None,
        house_status=status.house_status,
        sitting_status=status.sitting_status,
        voting_status=status.voting_status,
        debate_status=status.debate_status,
        members_present=status.members_present,
        quorum_met=status.quorum_met,
        current_time=status.current_time,
        next_scheduled_event=status.next_scheduled_event,
        next_event_time=status.next_event_time,
        question_period_status=status.question_period_status,
        emergency_debate_requested=status.emergency_debate_requested,
        closure_motion_active=status.closure_motion_active,
        update_source=status.update_source,
        notes=status.notes,
        last_updated=status.last_updated
    )


# ============================================================================
# HOUSE EVENTS
# ============================================================================

@router.post("/events", response_model=HouseEventResponse)
async def create_house_event(
    event_data: HouseEventCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new house event.
    """
    # Create new event
    event = HouseEvent(**event_data.dict())
    db.add(event)
    db.commit()
    db.refresh(event)
    
    logger.info(f"House event created: {current_user.username} - {event.event_title}")
    
    return HouseEventResponse(
        id=str(event.id),
        event_type=event.event_type,
        event_title=event.event_title,
        event_description=event.event_description,
        event_time=event.event_time,
        session_id=str(event.session_id) if event.session_id else None,
        sitting_id=str(event.sitting_id) if event.sitting_id else None,
        related_bill_id=event.related_bill_id,
        related_vote_id=str(event.related_vote_id) if event.related_vote_id else None,
        related_debate_id=str(event.related_debate_id) if event.related_debate_id else None,
        priority=event.priority,
        requires_notification=event.requires_notification,
        notification_sent=event.notification_sent,
        event_metadata=event.event_metadata,
        created_at=event.created_at,
        updated_at=event.updated_at
    )


@router.get("/events", response_model=HouseEventListResponse)
async def list_house_events(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    requires_notification: Optional[bool] = Query(None, description="Filter by notification requirement"),
    db: DBSession = Depends(get_db)
):
    """
    List house events with filtering and pagination.
    """
    # Build base query
    query = db.query(HouseEvent)
    
    # Apply filters
    if event_type:
        query = query.filter(HouseEvent.event_type == event_type)
    
    if priority:
        query = query.filter(HouseEvent.priority == priority)
    
    if requires_notification is not None:
        query = query.filter(HouseEvent.requires_notification == requires_notification)
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get events
    events = query.order_by(desc(HouseEvent.event_time)).offset(offset).limit(page_size).all()
    
    # Convert to response format
    event_responses = []
    for event in events:
        event_responses.append(HouseEventResponse(
            id=str(event.id),
            event_type=event.event_type,
            event_title=event.event_title,
            event_description=event.event_description,
            event_time=event.event_time,
            session_id=str(event.session_id) if event.session_id else None,
            sitting_id=str(event.sitting_id) if event.sitting_id else None,
            related_bill_id=event.related_bill_id,
            related_vote_id=str(event.related_vote_id) if event.related_vote_id else None,
            related_debate_id=str(event.related_debate_id) if event.related_debate_id else None,
            priority=event.priority,
            requires_notification=event.requires_notification,
            notification_sent=event.notification_sent,
            metadata=event.metadata,
            created_at=event.created_at,
            updated_at=event.updated_at
        ))
    
    return HouseEventListResponse(
        events=event_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


# ============================================================================
# ANALYTICS AND STATISTICS
# ============================================================================

@router.get("/statistics", response_model=HouseStatusStatistics)
async def get_house_statistics(
    db: DBSession = Depends(get_db)
):
    """
    Get comprehensive house status statistics.
    """
    # Count sessions
    total_sessions = db.query(HouseSession).count()
    active_sessions = db.query(HouseSession).filter(HouseSession.is_active == True).count()
    
    # Count sittings
    total_sittings = db.query(HouseSitting).count()
    active_sittings = db.query(HouseSitting).filter(HouseSitting.is_active == True).count()
    
    # Count votes
    total_votes = db.query(HouseVote).count()
    active_votes = db.query(HouseVote).filter(HouseVote.status.in_(["scheduled", "in_progress"])).count()
    
    # Count debates
    total_debates = db.query(HouseDebate).count()
    active_debates = db.query(HouseDebate).filter(HouseDebate.status.in_(["scheduled", "in_progress"])).count()
    
    # Calculate averages
    sittings_with_duration = db.query(HouseSitting).filter(
        and_(
            HouseSitting.start_time.isnot(None),
            HouseSitting.end_time.isnot(None)
        )
    ).all()
    
    average_sitting_duration = None
    if sittings_with_duration:
        total_duration = sum([
            (sitting.end_time - sitting.start_time).total_seconds() / 3600
            for sitting in sittings_with_duration
        ])
        average_sitting_duration = total_duration / len(sittings_with_duration)
    
    votes_with_duration = db.query(HouseVote).filter(
        and_(
            HouseVote.start_time.isnot(None),
            HouseVote.end_time.isnot(None),
            HouseVote.duration_minutes.isnot(None)
        )
    ).all()
    
    average_vote_duration = None
    if votes_with_duration:
        total_duration = sum([vote.duration_minutes for vote in votes_with_duration])
        average_vote_duration = total_duration / len(votes_with_duration)
    
    # Calculate quorum percentage
    total_sittings_with_quorum = db.query(HouseSitting).filter(
        HouseSitting.quorum_present.isnot(None)
    ).count()
    
    quorum_met_count = db.query(HouseSitting).filter(
        HouseSitting.quorum_present == True
    ).count()
    
    quorum_met_percentage = (quorum_met_count / total_sittings_with_quorum * 100) if total_sittings_with_quorum > 0 else 0
    
    return HouseStatusStatistics(
        total_sessions=total_sessions,
        active_sessions=active_sessions,
        total_sittings=total_sittings,
        active_sittings=active_sittings,
        total_votes=total_votes,
        active_votes=active_votes,
        total_debates=total_debates,
        active_debates=active_debates,
        average_sitting_duration=average_sitting_duration,
        average_vote_duration=average_vote_duration,
        quorum_met_percentage=round(quorum_met_percentage, 2),
        generated_at=datetime.utcnow()
    )


# ============================================================================
# WEBSOCKET ENDPOINTS
# ============================================================================

@router.websocket("/ws/house-status")
async def house_status_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for real-time house status updates.
    """
    await websocket.accept()
    
    try:
        # Send initial status
        db = next(get_db())
        status = db.query(HouseStatus).order_by(desc(HouseStatus.last_updated)).first()
        
        if status:
            initial_message = {
                "message_type": "house_status_update",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "house_status": status.house_status,
                    "sitting_status": status.sitting_status,
                    "voting_status": status.voting_status,
                    "debate_status": status.debate_status,
                    "members_present": status.members_present,
                    "quorum_met": status.quorum_met,
                    "last_updated": status.last_updated.isoformat()
                }
            }
            await websocket.send_text(json.dumps(initial_message))
        
        # Keep connection alive and send periodic updates
        while True:
            await asyncio.sleep(30)  # Update every 30 seconds
            
            # Get latest status
            db = next(get_db())
            status = db.query(HouseStatus).order_by(desc(HouseStatus.last_updated)).first()
            
            if status:
                update_message = {
                    "message_type": "house_status_update",
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": {
                        "house_status": status.house_status,
                        "sitting_status": status.sitting_status,
                        "voting_status": status.voting_status,
                        "debate_status": status.debate_status,
                        "members_present": status.members_present,
                        "quorum_met": status.quorum_met,
                        "last_updated": status.last_updated.isoformat()
                    }
                }
                await websocket.send_text(json.dumps(update_message))
                
    except WebSocketDisconnect:
        logger.info("House status WebSocket disconnected")
    except Exception as e:
        logger.error(f"House status WebSocket error: {e}")
        try:
            await websocket.close()
        except:
            pass


@router.websocket("/ws/vote-progress")
async def vote_progress_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for real-time vote progress updates.
    """
    await websocket.accept()
    
    try:
        # Send initial active votes
        db = next(get_db())
        active_votes = db.query(HouseVote).filter(
            HouseVote.status.in_(["scheduled", "in_progress"])
        ).all()
        
        for vote in active_votes:
            initial_message = {
                "message_type": "vote_progress_update",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "vote_id": str(vote.id),
                    "vote_status": vote.status,
                    "progress": {
                        "total_votes_cast": vote.total_votes_cast,
                        "yeas": vote.yeas,
                        "nays": vote.nays,
                        "abstentions": vote.abstentions
                    }
                }
            }
            await websocket.send_text(json.dumps(initial_message))
        
        # Keep connection alive and send periodic updates
        while True:
            await asyncio.sleep(15)  # Update every 15 seconds
            
            # Get latest active votes
            db = next(get_db())
            active_votes = db.query(HouseVote).filter(
                HouseVote.status.in_(["scheduled", "in_progress"])
            ).all()
            
            for vote in active_votes:
                update_message = {
                    "message_type": "vote_progress_update",
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": {
                        "vote_id": str(vote.id),
                        "vote_status": vote.status,
                        "progress": {
                            "total_votes_cast": vote.total_votes_cast,
                            "yeas": vote.yeas,
                            "nays": vote.nays,
                            "abstentions": vote.abstentions
                        }
                    }
                }
                await websocket.send_text(json.dumps(update_message))
                
    except WebSocketDisconnect:
        logger.info("Vote progress WebSocket disconnected")
    except Exception as e:
        logger.error(f"Vote progress WebSocket error: {e}")
        try:
            await websocket.close()
        except:
            pass
