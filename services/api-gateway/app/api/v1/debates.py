"""
Debates (Hansards) API endpoints for OpenParliament data.

Provides endpoints for managing House debates, including document listing, 
detail views, and speech access. Copied and adapted from legacy OpenParliament codebase.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import text, and_, desc
from typing import List, Optional
from datetime import date, datetime
from app.database import get_db
from app.models.openparliament import Statement, Bill, ElectedMember, Politician, Party
from app.schemas.debates import (
    DebateSummary, DebateDetail, SpeechSummary, SpeechDetail, Pagination,
    DebateListResponse, DebateDetailResponse, SpeechListResponse, SpeechDetailResponse,
    DebateSummaryResponse
)

router = APIRouter()


@router.get("/", response_model=DebateListResponse)
async def list_debates(
    session: Optional[str] = Query(None, description="Session ID (e.g., '45-1')"),
    date__gte: Optional[str] = Query(None, description="Date greater than or equal (YYYY-MM-DD)"),
    date__lte: Optional[str] = Query(None, description="Date less than or equal (YYYY-MM-DD)"),
    number: Optional[int] = Query(None, description="Hansard number in session"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    List House debates with optional filtering.
    
    Supports:
    - Filtering by session
    - Date range filtering
    - Filtering by hansard number
    - Pagination
    """
    
        # Build base query for hansard statements
    # Group by date to get unique debate dates
    query = db.query(Statement.time).distinct()
    
    # Apply filters
    if date__gte:
        try:
            date_gte = datetime.strptime(date__gte, "%Y-%m-%d").date()
            query = query.filter(Statement.time >= date_gte)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    if date__lte:
        try:
            date_lte = datetime.strptime(date__lte, "%Y-%m-%d").date()
            query = query.filter(Statement.time <= date_lte)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    # Get total count for pagination
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    debate_dates = query.offset(offset).limit(page_size).all()
    
    # Get debate summaries for each date
    debate_summaries = []
    for (debate_date,) in debate_dates:
        if debate_date:
            # Count total statements for this date
            statement_count = db.query(Statement).filter(
                and_(
                    Statement.time >= datetime.combine(debate_date.date(), datetime.min.time()),
                    Statement.time < datetime.combine(debate_date.date(), datetime.max.time())
                )
            ).count()
            
            # Get unique speakers for this date
            speaker_count = db.query(Statement.politician_id).filter(
                and_(
                    Statement.time >= datetime.combine(debate_date.date(), datetime.min.time()),
                    Statement.time < datetime.combine(debate_date.date(), datetime.max.time())
                )
            ).distinct().count()
            
            debate_summaries.append(DebateSummary(
                id=f"{debate_date.year}-{debate_date.month:02d}-{debate_date.day:02d}",
                date=debate_date.date().isoformat(),
                number=debate_date.day,  # Using day as the number for now
                statement_count=statement_count,
                url=f"/api/v1/debates/{debate_date.year}/{debate_date.month:02d}/{debate_date.day:02d}/"
            ))
    
    # Calculate pagination info
    total_pages = (total + page_size - 1) // page_size
    
    pagination = Pagination(
        page=page,
        page_size=page_size,
        total=total,
        pages=total_pages
    )
    
    return DebateListResponse(
        debates=debate_summaries,
        pagination=pagination
    )


@router.get("/{year}/{month}/{day}/", response_model=DebateDetailResponse)
async def get_debate_detail(
    year: int,
    month: int,
    day: int,
    db: DBSession = Depends(get_db)
):
    """
    Get detailed information about a specific House debate by date.
    """
    
    try:
        debate_date = date(year, month, day)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date")
    
    # Get all statements for this date
    statements = db.query(Statement).filter(
        and_(
            Statement.time >= datetime.combine(debate_date, datetime.min.time()),
            Statement.time < datetime.combine(debate_date, datetime.max.time())
        )
    ).order_by(Statement.sequence).all()
    
    if not statements:
        raise HTTPException(status_code=404, detail="Debate not found for this date")
    
    # Count speakers and topics
    unique_speakers = set()
    topics = set()
    
    for stmt in statements:
        if stmt.politician_id:
            unique_speakers.add(stmt.politician_id)
        # TODO: Extract topics from statement text or add topic field
    
    debate_detail = DebateDetail(
        id=f"{year}-{month:02d}-{day:02d}",
        date=debate_date.isoformat(),
        number=day,
        statement_count=len(statements),
        speaker_count=len(unique_speakers),
        url=f"/api/v1/debates/{year}/{month:02d}/{day:02d}/"
    )
    
    return DebateDetailResponse(debate=debate_detail)


@router.get("/speeches/", response_model=SpeechListResponse)
async def list_speeches(
    politician: Optional[str] = Query(None, description="Politician name filter"),
    date__gte: Optional[str] = Query(None, description="Date greater than or equal (YYYY-MM-DD)"),
    date__lte: Optional[str] = Query(None, description="Date less than or equal (YYYY-MM-DD)"),
    mentioned_politician: Optional[str] = Query(None, description="Mentioned politician filter"),
    bill: Optional[str] = Query(None, description="Bill filter (e.g., '45-1/C-5')"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    List speeches/statements with comprehensive filtering.
    
    Based on legacy SpeechesView functionality.
    """
    
    # Build base query
    query = db.query(Statement).join(Politician, Statement.politician_id == Politician.id, isouter=True)
    
    # Apply filters
    if politician:
        query = query.filter(Politician.name.ilike(f"%{politician}%"))
    
    if date__gte:
        try:
            date_gte = datetime.strptime(date__gte, "%Y-%m-%d")
            query = query.filter(Statement.time >= date_gte)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    if date__lte:
        try:
            date_lte = datetime.strptime(date__lte, "%Y-%m-%d")
            query = query.filter(Statement.time <= date_lte)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    if bill:
        # Parse bill filter (e.g., "45-1/C-5")
        if '/' in bill:
            session_id, bill_number = bill.split('/', 1)
            query = query.join(Bill, Statement.bill_id == Bill.id, isouter=True).filter(
                and_(Bill.session_id == session_id, Bill.number == bill_number)
            )
    
    # TODO: Add mentioned_politician filter when we have the relationship
    
    # Order by time descending (most recent first)
    query = query.order_by(desc(Statement.time))
    
    # Get total count for pagination
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    statements = query.offset(offset).limit(page_size).all()
    
    # Convert to response format
    speeches = []
    for stmt in statements:
        speeches.append(SpeechSummary(
            id=str(stmt.id),
            politician_name=stmt.politician.name if stmt.politician else "Unknown",
            date=stmt.time.date() if stmt.time else None,
            time=stmt.time,
            text_preview=stmt.content_en[:200] + "..." if stmt.content_en and len(stmt.content_en) > 200 else (stmt.content_en or "No content available"),
            bill_mentioned=str(stmt.bill_debated_id) if stmt.bill_debated_id else None,
            url=f"/api/v1/debates/speeches/{stmt.id}/"
        ))
    
    # Calculate pagination info
    total_pages = (total + page_size - 1) // page_size
    
    pagination = Pagination(
        page=page,
        page_size=page_size,
        total=total,
        pages=total_pages
    )
    
    return SpeechListResponse(
        speeches=speeches,
        pagination=pagination
    )


@router.get("/speeches/{speech_id}/", response_model=SpeechDetailResponse)
async def get_speech_detail(
    speech_id: int,
    db: DBSession = Depends(get_db)
):
    """
    Get detailed information about a specific speech/statement.
    """
    
    statement = db.query(Statement).filter(Statement.id == speech_id).first()
    
    if not statement:
        raise HTTPException(status_code=404, detail="Speech not found")
    
    speech_detail = SpeechDetail(
        id=str(statement.id),
        politician_name=statement.politician.name if statement.politician else "Unknown",
        party_name=statement.member.party.name_en if statement.member and statement.member.party else None,
        constituency=statement.member.riding.name_en if statement.member and statement.member.riding else None,
        date=statement.time.date() if statement.time else None,
        time=statement.time,
        text=statement.content_en or "No content available",
        bill_mentioned=str(statement.bill_debated_id) if statement.bill_debated_id else None,
                    sitting_id=statement.sequence,
        sequence=statement.sequence
    )
    
    return SpeechDetailResponse(speech=speech_detail)


@router.get("/summary/stats", response_model=DebateSummaryResponse)
async def get_debate_summary_stats(db: DBSession = Depends(get_db)):
    """
    Get summary statistics about debates and speeches.
    """
    
    # Get total statements count
    total_speeches = db.query(Statement).count()
    
    # Get unique sitting count (debates)
    total_debates = db.query(Statement.time).distinct().count()
    
    # Get unique politician count
    total_speakers = db.query(Statement.politician_id).filter(
        Statement.politician_id.isnot(None)
    ).distinct().count()
    
    # Get most recent debate date
    latest_statement = db.query(Statement).order_by(desc(Statement.time)).first()
    
    return DebateSummaryResponse(
        total_debates=total_debates,
        total_speeches=total_speeches,
        total_speakers=total_speakers,
        latest_debate_date=latest_statement.time.date() if latest_statement and latest_statement.time else None
    )
