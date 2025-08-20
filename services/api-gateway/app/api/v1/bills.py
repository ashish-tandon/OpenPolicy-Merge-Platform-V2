"""
Bills API endpoints for OpenParliament data.

Provides endpoints for managing bills, including search, filtering, and detailed information.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import text
from typing import List, Optional
from app.database import get_db
from app.models.openparliament import Bill, ElectedMember, Party, VoteQuestion, Riding
from app.schemas.bills import (
    BillSummary, BillDetail, VoteInfo, Pagination, 
    BillListResponse, BillDetailResponse, BillSuggestionsResponse,
    BillSummaryResponse
)

router = APIRouter()


@router.get("/", response_model=BillListResponse)
async def list_bills(
    q: Optional[str] = Query(None, description="Search query for bill title"),
    session: Optional[str] = Query(None, description="Session ID (e.g., '44-1')"),
    status: Optional[str] = Query(None, description="Bill status filter"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    List bills with optional filtering and search.
    
    Supports:
    - Full-text search on title
    - Filtering by session
    - Filtering by status
    - Pagination
    """
    
    # Build base query
    query = db.query(Bill)
    
    # Apply filters
    if session:
        query = query.filter(Bill.session_id == session)
    
    if status:
        query = query.filter(Bill.status_code == status)
    
    # Apply search if query provided
    if q:
        # Use PostgreSQL full-text search on name_en
        search_query = text("""
            to_tsvector('english', bills_bill.name_en) @@ plainto_tsquery('english', :search_term)
        """)
        query = query.filter(search_query.bindparams(search_term=q))
    
    # Get total count for pagination
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    bills = query.offset(offset).limit(page_size).all()
    
    # Convert to response format
    bill_summaries = []
    for bill in bills:
        # Get sponsor info
        sponsor_name = None
        party_name = None
        
        if bill.sponsor_member_id:
            # Get sponsor member info
            sponsor_member = db.query(ElectedMember).filter(
                ElectedMember.id == bill.sponsor_member_id
            ).first()
            
            if sponsor_member:
                sponsor_name = f"{sponsor_member.politician.name_given} {sponsor_member.politician.name_family}"
                
                # Get party info
                party = db.query(Party).filter(Party.id == sponsor_member.party_id).first()
                if party:
                    party_name = party.name_en
        
        bill_summaries.append(BillSummary(
            id=str(bill.id),
            bill_number=bill.number,
            title=bill.name_en,
            short_title=bill.short_title_en,
            summary=None,  # Not available in this schema
            status=bill.status_code,
            introduced_date=bill.introduced,
            sponsor_name=sponsor_name,
            party_name=party_name,
            session_name=f"Session {bill.session_id}",
            keywords=[],  # Not available in this schema
            tags=[]  # Not available in this schema
        ))
    
    # Calculate pagination info
    total_pages = (total + page_size - 1) // page_size
    
    pagination = Pagination(
        page=page,
        page_size=page_size,
        total=total,
        pages=total_pages
    )
    
    return {
        "bills": bill_summaries,
        "pagination": pagination
    }


@router.get("/{bill_id}", response_model=BillDetailResponse)
async def get_bill_detail(
    bill_id: int,
    db: DBSession = Depends(get_db)
):
    """
    Get detailed information about a specific bill.
    """
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # Get sponsor info
    sponsor_name = None
    party_name = None
    riding_name = None
    
    if bill.sponsor_member_id:
        sponsor_member = db.query(ElectedMember).filter(
            ElectedMember.id == bill.sponsor_member_id
        ).first()
        
        if sponsor_member:
            sponsor_name = f"{sponsor_member.politician.name_given} {sponsor_member.politician.name_family}"
            
            # Get party info
            party = db.query(Party).filter(Party.id == sponsor_member.party_id).first()
            if party:
                party_name = party.name_en
            
            # Get riding info
            riding = db.query(Riding).filter(Riding.id == sponsor_member.riding_id).first()
            if riding:
                riding_name = riding.name_en
    
    # Get vote information
    votes = db.query(VoteQuestion).filter(VoteQuestion.bill_id == bill_id).all()
    vote_info = []
    
    for vote in votes:
        vote_info.append(VoteInfo(
            vote_id=str(vote.id),
            vote_date=vote.date,
            description=vote.description,
            result=vote.result
        ))
    
    bill_detail = BillDetail(
        id=str(bill.id),
        bill_number=bill.number,
        title=bill.name_en,
        short_title=bill.short_title_en,
        summary=None,  # Not available in this schema
        status=bill.status_code,
        introduced_date=bill.introduced,
        sponsor_name=sponsor_name,
        party_name=party_name,
        riding_name=riding_name,
        session_id=bill.session_id,
        institution=bill.institution,
        votes=vote_info
    )
    
    return BillDetailResponse(bill=bill_detail)


@router.get("/suggestions", response_model=BillSuggestionsResponse)
async def get_bill_suggestions(
    q: str = Query(..., min_length=1, description="Search query for bill suggestions"),
    limit: int = Query(10, ge=1, le=50, description="Number of suggestions to return"),
    db: DBSession = Depends(get_db)
):
    """
    Get bill title suggestions using trigram similarity.
    """
    if not q or len(q.strip()) < 1:
        return BillSuggestionsResponse(suggestions=[])
    
    # Use trigram similarity for fuzzy matching
    suggestions_query = text("""
        SELECT id, name_en, number, 
               similarity(name_en, :query) as sim
        FROM bills_bill 
        WHERE name_en % :query
        ORDER BY sim DESC, name_en
        LIMIT :limit
    """)
    
    results = db.execute(suggestions_query, {"query": q, "limit": limit})
    
    suggestions = []
    for row in results:
        suggestions.append({
            "id": str(row.id),
            "title": row.name_en,
            "bill_number": row.number,
            "similarity": float(row.sim)
        })
    
    return BillSuggestionsResponse(suggestions=suggestions)


@router.get("/summary/stats", response_model=BillSummaryResponse)
async def get_bill_summary_stats(db: DBSession = Depends(get_db)):
    """
    Get summary statistics about bills.
    """
    # Get total bills count
    total_bills = db.query(Bill).count()
    
    # Get bills by status
    status_counts = db.query(
        Bill.status_code,
        db.func.count(Bill.id)
    ).group_by(Bill.status_code).all()
    
    # Get bills by session
    session_counts = db.query(
        Bill.session_id,
        db.func.count(Bill.id)
    ).group_by(Bill.session_id).all()
    
    return BillSummaryResponse(
        total_bills=total_bills,
        status_breakdown={status: count for status, count in status_counts},
        session_breakdown={session: count for session, count in session_counts}
    )
