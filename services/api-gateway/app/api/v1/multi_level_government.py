"""
Multi-Level Government API endpoints

Provides unified access to federal, provincial, and municipal government data
across all levels of Canadian government.
"""

from fastapi import APIRouter, HTTPException, Query, Depends, Path
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import text, func, and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import math

from app.database import get_db
from app.models.government_levels_simple import (
    GovernmentLevel, Jurisdiction, Representative, Office, 
    Bill, Vote, DataSource, IngestionLog
)
from app.schemas.multi_level_government import (
    GovernmentLevelResponse, JurisdictionResponse, RepresentativeResponse,
    OfficeResponse, BillResponse, VoteResponse, DataSourceResponse,
    GovernmentLevelListResponse, JurisdictionListResponse, RepresentativeListResponse,
    OfficeListResponse, BillListResponse, VoteListResponse, DataSourceListResponse,
    RepresentativeSearchParams, BillSearchParams, VoteSearchParams,
    JurisdictionStats, GovernmentLevelStats, SystemStats,
    PaginationInfo
)

router = APIRouter()


# ============================================================================
# Government Levels Endpoints
# ============================================================================

@router.get("/government-levels", response_model=GovernmentLevelListResponse)
async def list_government_levels(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    List all government levels (Federal, Provincial, Municipal).
    
    Returns government levels ordered by their level_order.
    """
    # Get total count
    total = db.query(GovernmentLevel).count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get government levels
    levels = db.query(GovernmentLevel).order_by(GovernmentLevel.level_order).offset(offset).limit(page_size).all()
    
    # Convert to response format
    level_responses = []
    for level in levels:
        level_responses.append(GovernmentLevelResponse(
            id=str(level.id),
            name=level.name,
            description=level.description,
            level_order=level.level_order,
            created_at=level.created_at,
            updated_at=level.updated_at
        ))
    
    # Create pagination info
    pagination = PaginationInfo(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )
    
    return GovernmentLevelListResponse(items=level_responses, pagination=pagination)


@router.get("/government-levels/{level_id}", response_model=GovernmentLevelResponse)
async def get_government_level(
    level_id: str = Path(..., description="Government level ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get a specific government level by ID.
    
    Returns detailed information about a government level.
    """
    level = db.query(GovernmentLevel).filter(GovernmentLevel.id == level_id).first()
    
    if not level:
        raise HTTPException(status_code=404, detail="Government level not found")
    
    return GovernmentLevelResponse(
        id=str(level.id),
        name=level.name,
        description=level.description,
        level_order=level.level_order,
        created_at=level.created_at,
        updated_at=level.updated_at
    )


# ============================================================================
# Jurisdictions Endpoints
# ============================================================================

@router.get("/jurisdictions", response_model=JurisdictionListResponse)
async def list_jurisdictions(
    government_level: Optional[str] = Query(None, description="Filter by government level ID"),
    province: Optional[str] = Query(None, description="Filter by province/territory"),
    jurisdiction_type: Optional[str] = Query(None, description="Filter by jurisdiction type"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    List all jurisdictions across all government levels.
    
    Supports filtering by government level, province, and jurisdiction type.
    """
    # Build base query
    query = db.query(Jurisdiction).join(GovernmentLevel)
    
    # Apply filters
    if government_level:
        query = query.filter(Jurisdiction.government_level_id == government_level)
    
    if province:
        query = query.filter(Jurisdiction.province == province)
    
    if jurisdiction_type:
        query = query.filter(Jurisdiction.jurisdiction_type == jurisdiction_type)
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get jurisdictions
    jurisdictions = query.offset(offset).limit(page_size).all()
    
    # Convert to response format
    jurisdiction_responses = []
    for jurisdiction in jurisdictions:
        # Get government level details
        gov_level = db.query(GovernmentLevel).filter(
            GovernmentLevel.id == jurisdiction.government_level_id
        ).first()
        
        gov_level_response = GovernmentLevelResponse(
            id=str(gov_level.id),
            name=gov_level.name,
            description=gov_level.description,
            level_order=gov_level.level_order,
            created_at=gov_level.created_at,
            updated_at=gov_level.updated_at
        )
        
        jurisdiction_responses.append(JurisdictionResponse(
            id=str(jurisdiction.id),
            name=jurisdiction.name,
            code=jurisdiction.code,
            government_level_id=str(jurisdiction.government_level_id),
            province=jurisdiction.province,
            jurisdiction_type=jurisdiction.jurisdiction_type,
            website=jurisdiction.website,
            extras=jurisdiction.extras,
            government_level=gov_level_response,
            created_at=jurisdiction.created_at,
            updated_at=jurisdiction.updated_at
        ))
    
    # Create pagination info
    pagination = PaginationInfo(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )
    
    return JurisdictionListResponse(items=jurisdiction_responses, pagination=pagination)


@router.get("/jurisdictions/{jurisdiction_id}", response_model=JurisdictionResponse)
async def get_jurisdiction(
    jurisdiction_id: str = Path(..., description="Jurisdiction ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get a specific jurisdiction by ID.
    
    Returns detailed information about a jurisdiction including its government level.
    """
    jurisdiction = db.query(Jurisdiction).filter(Jurisdiction.id == jurisdiction_id).first()
    
    if not jurisdiction:
        raise HTTPException(status_code=404, detail="Jurisdiction not found")
    
    # Get government level details
    gov_level = db.query(GovernmentLevel).filter(
        GovernmentLevel.id == jurisdiction.government_level_id
    ).first()
    
    gov_level_response = GovernmentLevelResponse(
        id=str(gov_level.id),
        name=gov_level.name,
        description=gov_level.description,
        level_order=gov_level.level_order,
        created_at=gov_level.created_at,
        updated_at=gov_level.updated_at
    )
    
    return JurisdictionResponse(
        id=str(jurisdiction.id),
        name=jurisdiction.name,
        code=jurisdiction.code,
        government_level_id=str(jurisdiction.government_level_id),
        province=jurisdiction.province,
        jurisdiction_type=jurisdiction.jurisdiction_type,
        website=jurisdiction.website,
        extras=jurisdiction.extras,
        government_level=gov_level_response,
        created_at=jurisdiction.created_at,
        updated_at=jurisdiction.updated_at
    )


# ============================================================================
# Representatives Endpoints
# ============================================================================

@router.get("/representatives", response_model=RepresentativeListResponse)
async def list_representatives(
    q: Optional[str] = Query(None, description="Search query for representative name"),
    jurisdiction_id: Optional[str] = Query(None, description="Filter by jurisdiction ID"),
    government_level: Optional[str] = Query(None, description="Filter by government level ID"),
    province: Optional[str] = Query(None, description="Filter by province/territory"),
    party: Optional[str] = Query(None, description="Filter by political party"),
    position: Optional[str] = Query(None, description="Filter by position"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    List all representatives across all government levels.
    
    Supports search, filtering, and pagination.
    """
    # Build base query
    query = db.query(Representative).join(Jurisdiction).join(GovernmentLevel)
    
    # Apply filters
    if jurisdiction_id:
        query = query.filter(Representative.jurisdiction_id == jurisdiction_id)
    
    if government_level:
        query = query.filter(Jurisdiction.government_level_id == government_level)
    
    if province:
        query = query.filter(Jurisdiction.province == province)
    
    if party:
        query = query.filter(Representative.party.ilike(f"%{party}%"))
    
    if position:
        query = query.filter(Representative.position == position)
    
    # Apply search if query provided
    if q:
        search_query = text("""
            to_tsvector('english', representatives.name) @@ plainto_tsquery('english', :search_term)
        """)
        query = query.filter(search_query.bindparams(search_term=q))
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get representatives
    representatives = query.offset(offset).limit(page_size).all()
    
    # Convert to response format
    representative_responses = []
    for rep in representatives:
        # Get jurisdiction details
        jurisdiction = db.query(Jurisdiction).filter(
            Jurisdiction.id == rep.jurisdiction_id
        ).first()
        
        gov_level = db.query(GovernmentLevel).filter(
            GovernmentLevel.id == jurisdiction.government_level_id
        ).first()
        
        gov_level_response = GovernmentLevelResponse(
            id=str(gov_level.id),
            name=gov_level.name,
            description=gov_level.description,
            level_order=gov_level.level_order,
            created_at=gov_level.created_at,
            updated_at=gov_level.updated_at
        )
        
        jurisdiction_response = JurisdictionResponse(
            id=str(jurisdiction.id),
            name=jurisdiction.name,
            code=jurisdiction.code,
            government_level_id=str(jurisdiction.government_level_id),
            province=jurisdiction.province,
            jurisdiction_type=jurisdiction.jurisdiction_type,
            website=jurisdiction.website,
            extras=jurisdiction.extras,
            government_level=gov_level_response,
            created_at=jurisdiction.created_at,
            updated_at=jurisdiction.updated_at
        )
        
        representative_responses.append(RepresentativeResponse(
            id=str(rep.id),
            name=rep.name,
            jurisdiction_id=str(rep.jurisdiction_id),
            party=rep.party,
            position=rep.position,
            riding=rep.riding,
            email=rep.email,
            phone=rep.phone,
            website=rep.website,
            extras=rep.extras,
            metadata_json=rep.metadata_json,
            jurisdiction=jurisdiction_response,
            created_at=rep.created_at,
            updated_at=rep.updated_at
        ))
    
    # Create pagination info
    pagination = PaginationInfo(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )
    
    return RepresentativeListResponse(items=representative_responses, pagination=pagination)


@router.get("/representatives/{representative_id}", response_model=RepresentativeResponse)
async def get_representative(
    representative_id: str = Path(..., description="Representative ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get a specific representative by ID.
    
    Returns detailed information about a representative including jurisdiction and government level.
    """
    representative = db.query(Representative).filter(Representative.id == representative_id).first()
    
    if not representative:
        raise HTTPException(status_code=404, detail="Representative not found")
    
    # Get jurisdiction details
    jurisdiction = db.query(Jurisdiction).filter(
        Jurisdiction.id == representative.jurisdiction_id
    ).first()
    
    gov_level = db.query(GovernmentLevel).filter(
        GovernmentLevel.id == jurisdiction.government_level_id
    ).first()
    
    gov_level_response = GovernmentLevelResponse(
        id=str(gov_level.id),
        name=gov_level.name,
        description=gov_level.description,
        level_order=gov_level.level_order,
        created_at=gov_level.created_at,
        updated_at=gov_level.updated_at
    )
    
    jurisdiction_response = JurisdictionResponse(
        id=str(jurisdiction.id),
        name=jurisdiction.name,
        code=jurisdiction.code,
        government_level_id=str(jurisdiction.government_level_id),
        province=jurisdiction.province,
        jurisdiction_type=jurisdiction.jurisdiction_type,
        website=jurisdiction.website,
        extras=jurisdiction.extras,
        government_level=gov_level_response,
        created_at=jurisdiction.created_at,
        updated_at=jurisdiction.updated_at
    )
    
    return RepresentativeResponse(
        id=str(representative.id),
        name=representative.name,
        jurisdiction_id=str(representative.jurisdiction_id),
        party=representative.party,
        position=representative.position,
        riding=representative.riding,
        email=representative.email,
        phone=representative.phone,
        website=representative.website,
        extras=representative.extras,
        metadata_json=representative.metadata_json,
        jurisdiction=jurisdiction_response,
        created_at=representative.created_at,
        updated_at=representative.updated_at
    )


# ============================================================================
# Statistics Endpoints
# ============================================================================

@router.get("/stats/system", response_model=SystemStats)
async def get_system_stats(db: DBSession = Depends(get_db)):
    """
    Get system-wide statistics.
    
    Returns counts of all major data types across the system.
    """
    # Get counts
    total_government_levels = db.query(GovernmentLevel).count()
    total_jurisdictions = db.query(Jurisdiction).count()
    total_representatives = db.query(Representative).count()
    total_bills = db.query(Bill).count()
    total_votes = db.query(Vote).count()
    total_offices = db.query(Office).count()
    total_data_sources = db.query(DataSource).count()
    
    return SystemStats(
        total_government_levels=total_government_levels,
        total_jurisdictions=total_jurisdictions,
        total_representatives=total_representatives,
        total_bills=total_bills,
        total_votes=total_votes,
        total_offices=total_offices,
        total_data_sources=total_data_sources,
        last_updated=datetime.utcnow()
    )


@router.get("/stats/government-levels/{level_id}", response_model=GovernmentLevelStats)
async def get_government_level_stats(
    level_id: str = Path(..., description="Government level ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get statistics for a specific government level.
    
    Returns counts of jurisdictions, representatives, bills, votes, and offices for the level.
    """
    # Verify government level exists
    gov_level = db.query(GovernmentLevel).filter(GovernmentLevel.id == level_id).first()
    if not gov_level:
        raise HTTPException(status_code=404, detail="Government level not found")
    
    # Get counts for this level
    total_jurisdictions = db.query(Jurisdiction).filter(
        Jurisdiction.government_level_id == level_id
    ).count()
    
    total_representatives = db.query(Representative).join(Jurisdiction).filter(
        Jurisdiction.government_level_id == level_id
    ).count()
    
    total_bills = db.query(Bill).join(Jurisdiction).filter(
        Jurisdiction.government_level_id == level_id
    ).count()
    
    total_votes = db.query(Vote).join(Bill).join(Jurisdiction).filter(
        Jurisdiction.government_level_id == level_id
    ).count()
    
    total_offices = db.query(Office).join(Jurisdiction).filter(
        Jurisdiction.government_level_id == level_id
    ).count()
    
    return GovernmentLevelStats(
        level_id=level_id,
        level_name=gov_level.name,
        total_jurisdictions=total_jurisdictions,
        total_representatives=total_representatives,
        total_bills=total_bills,
        total_votes=total_votes,
        total_offices=total_offices,
        last_updated=datetime.utcnow()
    )


@router.get("/stats/jurisdictions/{jurisdiction_id}", response_model=JurisdictionStats)
async def get_jurisdiction_stats(
    jurisdiction_id: str = Path(..., description="Jurisdiction ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get statistics for a specific jurisdiction.
    
    Returns counts of representatives, bills, votes, and offices for the jurisdiction.
    """
    # Verify jurisdiction exists
    jurisdiction = db.query(Jurisdiction).filter(Jurisdiction.id == jurisdiction_id).first()
    if not jurisdiction:
        raise HTTPException(status_code=404, detail="Jurisdiction not found")
    
    # Get counts for this jurisdiction
    total_representatives = db.query(Representative).filter(
        Representative.jurisdiction_id == jurisdiction_id
    ).count()
    
    total_bills = db.query(Bill).filter(
        Bill.jurisdiction_id == jurisdiction_id
    ).count()
    
    total_votes = db.query(Vote).join(Bill).filter(
        Bill.jurisdiction_id == jurisdiction_id
    ).count()
    
    total_offices = db.query(Office).filter(
        Office.jurisdiction_id == jurisdiction_id
    ).count()
    
    return JurisdictionStats(
        jurisdiction_id=jurisdiction_id,
        jurisdiction_name=jurisdiction.name,
        total_representatives=total_representatives,
        total_bills=total_bills,
        total_votes=total_votes,
        total_offices=total_offices,
        last_updated=datetime.utcnow()
    )
