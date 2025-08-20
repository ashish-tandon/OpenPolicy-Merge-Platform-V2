"""
Votes API endpoints for OpenParliament data.

Provides endpoints for managing parliamentary votes, including search, filtering, and detailed information.
This is adapted from the working legacy OpenParliament codebase.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import text
from typing import List, Optional
from app.database import get_db
from app.models.openparliament import VoteQuestion, Bill, MemberVote, PartyVote, ElectedMember, Politician, Party
from app.schemas.votes import (
    VoteSummary, VoteDetail, VoteBallot, Pagination, 
    VoteListResponse, VoteDetailResponse, VoteBallotsResponse,
    VoteSummaryResponse
)

router = APIRouter()


@router.get("/", response_model=VoteListResponse)
async def list_votes(
    session: Optional[str] = Query(None, description="Session ID (e.g., '45-1')"),
    bill: Optional[str] = Query(None, description="Bill filter (e.g., '45-1/C-5')"),
    result: Optional[str] = Query(None, description="Vote result filter"),
    date__gte: Optional[str] = Query(None, description="Date greater than or equal (YYYY-MM-DD)"),
    date__lte: Optional[str] = Query(None, description="Date less than or equal (YYYY-MM-DD)"),
    number: Optional[int] = Query(None, description="Vote number in session"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    List parliamentary votes with optional filtering.
    
    Supports:
    - Filtering by session
    - Filtering by bill
    - Filtering by result
    - Date range filtering
    - Filtering by vote number
    - Pagination
    """
    
    # Build base query
    query = db.query(VoteQuestion).join(Bill)
    
    # Apply filters
    if session:
        query = query.filter(Bill.session_id == session)
    
    if bill:
        # Parse bill filter (e.g., "45-1/C-5")
        if '/' in bill:
            session_id, bill_number = bill.split('/', 1)
            query = query.filter(Bill.session_id == session_id, Bill.number == bill_number)
    
    if result:
        query = query.filter(VoteQuestion.result == result)
    
    if date__gte:
        query = query.filter(VoteQuestion.date >= date__gte)
    
    if date__lte:
        query = query.filter(VoteQuestion.date <= date__lte)
    
    if number:
        query = query.filter(VoteQuestion.number == number)
    
    # Get total count for pagination
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    votes = query.offset(offset).limit(page_size).all()
    
    # Convert to response format
    vote_summaries = []
    for vote in votes:
        # Get vote totals
        yea_total = db.query(MemberVote).filter(
            MemberVote.votequestion_id == vote.id,
            MemberVote.vote == 'Yea'
        ).count()
        
        nay_total = db.query(MemberVote).filter(
            MemberVote.votequestion_id == vote.id,
            MemberVote.vote == 'Nay'
        ).count()
        
        vote_summaries.append(VoteSummary(
            id=str(vote.id),
            session=vote.bill.session_id,
            number=vote.number,
            date=vote.date,
            description=vote.description,
            result=vote.result,
            yea_total=yea_total,
            nay_total=nay_total,
            bill_number=vote.bill.number,
            bill_title=vote.bill.name_en
        ))
    
    # Calculate pagination info
    total_pages = (total + page_size - 1) // page_size
    
    pagination = Pagination(
        page=page,
        page_size=page_size,
        total=total,
        pages=total_pages
    )
    
    return VoteListResponse(
        votes=vote_summaries,
        pagination=pagination
    )


@router.get("/{session_id}/{vote_number}", response_model=VoteDetailResponse)
async def get_vote_detail(
    session_id: str,
    vote_number: int,
    db: DBSession = Depends(get_db)
):
    """
    Get detailed information about a specific vote.
    """
    
    vote = db.query(VoteQuestion).join(Bill).filter(
        Bill.session_id == session_id,
        VoteQuestion.number == vote_number
    ).first()
    
    if not vote:
        raise HTTPException(status_code=404, detail="Vote not found")
    
    # Get bill info
    bill_info = {
        "bill_number": vote.bill.number,
        "bill_title": vote.bill.name_en,
        "session": vote.bill.session_id
    }
    
    # Get vote totals
    yea_total = db.query(MemberVote).filter(
        MemberVote.votequestion_id == vote.id,
        MemberVote.vote == 'Yea'
    ).count()
    
    nay_total = db.query(MemberVote).filter(
        MemberVote.votequestion_id == vote.id,
        MemberVote.vote == 'Nay'
    ).count()
    
    # Get party votes
    party_votes = db.query(PartyVote).filter(
        PartyVote.votequestion_id == vote.id
    ).all()
    
    parties_y = [pv.party.name_en for pv in party_votes if pv.vote == 'Y']
    parties_n = [pv.party.name_en for pv in party_votes if pv.vote == 'N']
    
    vote_detail = VoteDetail(
        id=str(vote.id),
        session=vote.bill.session_id,
        number=vote.number,
        date=vote.date,
        description=vote.description,
        result=vote.result,
        yea_total=yea_total,
        nay_total=nay_total,
        bill_number=vote.bill.number,
        bill_title=vote.bill.name_en,
        parties_yea=parties_y,
        parties_nay=parties_n
    )
    
    return VoteDetailResponse(vote=vote_detail)


@router.get("/ballots/", response_model=VoteBallotsResponse)
async def get_vote_ballots(
    vote: Optional[str] = Query(None, description="Vote filter (e.g., '45-1/34')"),
    politician: Optional[str] = Query(None, description="Politician filter"),
    ballot: Optional[str] = Query(None, description="Vote choice filter (Yea, Nay, etc.)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    Get individual vote ballots (how each MP voted).
    """
    
    # Build base query
    query = db.query(MemberVote).join(VoteQuestion).join(Bill)
    
    # Apply filters
    if vote:
        # Parse vote filter (e.g., "45-1/34")
        if '/' in vote:
            session_id, vote_number = vote.split('/', 1)
            query = query.filter(
                Bill.session_id == session_id,
                VoteQuestion.number == int(vote_number)
            )
    
    if politician:
        query = query.join(Politician).filter(
            Politician.name.contains(politician)
        )
    
    if ballot:
        query = query.filter(MemberVote.vote == ballot)
    
    # Get total count for pagination
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    ballots = query.offset(offset).limit(page_size).all()
    
    # Convert to response format
    ballot_list = []
    for ballot in ballots:
        ballot_list.append(VoteBallot(
            id=str(ballot.id),
            vote_id=str(ballot.votequestion_id),
            member_name=f"{ballot.politician.name_given} {ballot.politician.name_family}",
            party_name=ballot.member.party.name_en,
            constituency=ballot.member.riding.name_en,
            vote_choice=ballot.vote
        ))
    
    # Calculate pagination info
    total_pages = (total + page_size - 1) // page_size
    
    pagination = Pagination(
        page=page,
        page_size=page_size,
        total=total,
        pages=total_pages
    )
    
    return VoteBallotsResponse(
        ballots=ballot_list,
        pagination=pagination
    )


@router.get("/summary/stats", response_model=VoteSummaryResponse)
async def get_vote_summary_stats(db: DBSession = Depends(get_db)):
    """
    Get summary statistics about votes.
    """
    
    # Get total votes count
    total_votes = db.query(VoteQuestion).count()
    
    # Get votes by result
    result_counts = db.query(
        VoteQuestion.result,
        db.func.count(VoteQuestion.id)
    ).group_by(VoteQuestion.result).all()
    
    # Get votes by session
    session_counts = db.query(
        Bill.session_id,
        db.func.count(VoteQuestion.id)
    ).join(VoteQuestion).group_by(Bill.session_id).all()
    
    # Get most recent vote
    latest_vote = db.query(VoteQuestion).order_by(VoteQuestion.date.desc()).first()
    
    return VoteSummaryResponse(
        total_votes=total_votes,
        result_breakdown={result: count for result, count in result_counts},
        session_breakdown={session: count for session, count in session_counts},
        latest_vote_date=latest_vote.date if latest_vote else None
    )
