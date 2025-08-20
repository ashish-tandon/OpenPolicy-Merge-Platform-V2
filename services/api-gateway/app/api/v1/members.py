"""
Members API endpoints for OpenParliament data.

Provides endpoints for managing Members of Parliament, including search, filtering, and detailed information.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import text
from typing import List, Optional
from app.database import get_db
from app.models.openparliament import ElectedMember, Party, Bill, VoteQuestion, MemberVote, Politician, Riding
from app.schemas.members import (
    MemberSummary, MemberDetail, Pagination, 
    MemberListResponse, MemberDetailResponse, MemberSuggestionsResponse,
    MemberSummaryResponse
)

router = APIRouter()


@router.get("/", response_model=MemberListResponse)
async def list_members(
    q: Optional[str] = Query(None, description="Search query for member name"),
    province: Optional[str] = Query(None, description="Province filter"),
    party: Optional[str] = Query(None, description="Party slug filter"),
    current_only: bool = Query(True, description="Show only current MPs"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    List Members of Parliament with optional filtering and search.
    
    Supports:
    - Full-text search on member names
    - Filtering by province
    - Filtering by party
    - Filtering by current status
    - Pagination
    """
    
    # Build base query - join with politician and party info
    query = db.query(ElectedMember).join(Politician).join(Party)
    
    # Apply filters
    if province:
        query = query.join(Riding).filter(Riding.province == province)
    
    if party:
        query = query.filter(Party.slug == party)
    
    if current_only:
        query = query.filter(ElectedMember.end_date.is_(None))
    
    # Apply search if query provided
    if q:
        # Use PostgreSQL full-text search on politician names
        search_query = text("""
            to_tsvector('english', 
                core_politician.name_given || ' ' || core_politician.name_family
            ) @@ plainto_tsquery('english', :search_term)
        """)
        query = query.filter(search_query.bindparams(search_term=q))
    
    # Get total count for pagination
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    members = query.offset(offset).limit(page_size).all()
    
    # Convert to response format
    member_summaries = []
    for member in members:
        # Get riding info
        riding = db.query(Riding).filter(Riding.id == member.riding_id).first()
        riding_name = riding.name_en if riding else None
        
        member_summaries.append(MemberSummary(
            id=str(member.id),
            full_name=f"{member.politician.name_given} {member.politician.name_family}",
            first_name=member.politician.name_given,
            last_name=member.politician.name_family,
            party_name=member.party.name_en,
            party_slug=member.party.slug,
            constituency=riding_name,
            province=riding.province if riding else None,
            is_current=member.end_date is None,
            start_date=member.start_date,
            end_date=member.end_date
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
        "members": member_summaries,
        "pagination": pagination
    }


@router.get("/{member_id}", response_model=MemberDetailResponse)
async def get_member_detail(
    member_id: int,
    db: DBSession = Depends(get_db)
):
    """
    Get detailed information about a specific Member of Parliament.
    """
    member = db.query(ElectedMember).filter(ElectedMember.id == member_id).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Get riding info
    riding = db.query(Riding).filter(Riding.id == member.riding_id).first()
    
    # Get sponsored bills
    sponsored_bills = db.query(Bill).filter(Bill.sponsor_member_id == member_id).all()
    
    # Get recent votes
    recent_votes = db.query(
        MemberVote, VoteQuestion, Bill
    ).join(
        VoteQuestion, MemberVote.votequestion_id == VoteQuestion.id
    ).join(
        Bill, VoteQuestion.bill_id == Bill.id
    ).filter(
        MemberVote.member_id == member_id
    ).order_by(
        VoteQuestion.date.desc()
    ).limit(10).all()
    
    member_detail = MemberDetail(
        id=str(member.id),
        full_name=f"{member.politician.name_given} {member.politician.name_family}",
        first_name=member.politician.name_given,
        last_name=member.politician.name_family,
        party_name=member.party.name_en,
        party_slug=member.party.slug,
        constituency=riding.name_en if riding else None,
        province=riding.province if riding else None,
        is_current=member.end_date is None,
        start_date=member.start_date,
        end_date=member.end_date,
        sponsored_bills_count=len(sponsored_bills),
        recent_votes_count=len(recent_votes)
    )
    
    return MemberDetailResponse(member=member_detail)


@router.get("/suggestions", response_model=MemberSuggestionsResponse)
async def get_member_suggestions(
    q: str = Query(..., min_length=1, description="Search query for member suggestions"),
    limit: int = Query(10, ge=1, le=50, description="Number of suggestions to return"),
    db: DBSession = Depends(get_db)
):
    """
    Get member name suggestions using trigram similarity.
    """
    if not q or len(q.strip()) < 1:
        return MemberSuggestionsResponse(suggestions=[])
    
    # Use trigram similarity for fuzzy matching on politician names
    suggestions_query = text("""
        SELECT em.id, cp.name_given, cp.name_family,
               similarity(cp.name_given || ' ' || cp.name_family, :query) as sim
        FROM core_electedmember em
        JOIN core_politician cp ON em.politician_id = cp.id
        WHERE cp.name_given || ' ' || cp.name_family % :query
        ORDER BY sim DESC, cp.name_family, cp.name_given
        LIMIT :limit
    """)
    
    results = db.execute(suggestions_query, {"query": q, "limit": limit})
    
    suggestions = []
    for row in results:
        suggestions.append({
            "id": str(row.id),
            "full_name": f"{row.name_given} {row.name_family}",
            "similarity": float(row.sim)
        })
    
    return MemberSuggestionsResponse(suggestions=suggestions)


@router.get("/summary/stats", response_model=MemberSummaryResponse)
async def get_member_summary_stats(db: DBSession = Depends(get_db)):
    """
    Get summary statistics about Members of Parliament.
    """
    # Get total MPs
    total_members = db.query(ElectedMember).count()
    
    # Current MPs
    current_members = db.query(ElectedMember).filter(
        ElectedMember.end_date.is_(None)
    ).count()
    
    # MPs by party
    party_counts = db.query(
        Party.name_en,
        db.func.count(ElectedMember.id)
    ).join(ElectedMember).group_by(Party.name_en).all()
    
    # MPs by province
    province_counts = db.query(
        Riding.province,
        db.func.count(ElectedMember.id)
    ).join(ElectedMember).filter(
        ElectedMember.end_date.is_(None)
    ).group_by(Riding.province).all()
    
    # Top bill sponsors
    top_sponsors = db.query(
        db.func.concat(Politician.name_given, ' ', Politician.name_family).label('full_name'),
        db.func.count(Bill.id).label('bill_count')
    ).join(ElectedMember, Politician.id == ElectedMember.politician_id).join(
        Bill, ElectedMember.id == Bill.sponsor_member_id
    ).group_by(
        Politician.id, Politician.name_given, Politician.name_family
    ).order_by(db.func.count(Bill.id).desc()).limit(10).all()
    
    return MemberSummaryResponse(
        total_members=total_members,
        current_members=current_members,
        party_breakdown={party: count for party, count in party_counts},
        province_breakdown={province: count for province, count in province_counts},
        top_sponsors=[{"name": sponsor.full_name, "count": sponsor.bill_count} for sponsor in top_sponsors]
    )
