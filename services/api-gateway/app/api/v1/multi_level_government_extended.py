"""
Extended Multi-Level Government API endpoints

Additional endpoints for bills, votes, offices, and data sources.
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
    OfficeResponse, BillResponse, VoteResponse, DataSourceResponse,
    OfficeListResponse, BillListResponse, VoteListResponse, DataSourceListResponse,
    BillSearchParams, VoteSearchParams
)

router = APIRouter()


# ============================================================================
# Offices Endpoints
# ============================================================================

@router.get("/offices", response_model=OfficeListResponse)
async def list_offices(
    jurisdiction_id: Optional[str] = Query(None, description="Filter by jurisdiction ID"),
    government_level: Optional[str] = Query(None, description="Filter by government level ID"),
    office_type: Optional[str] = Query(None, description="Filter by office type"),
    province: Optional[str] = Query(None, description="Filter by province/territory"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    List all offices across all government levels.
    
    Supports filtering by jurisdiction, government level, office type, and province.
    """
    # Build base query
    query = db.query(Office).join(Jurisdiction).join(GovernmentLevel)
    
    # Apply filters
    if jurisdiction_id:
        query = query.filter(Office.jurisdiction_id == jurisdiction_id)
    
    if government_level:
        query = query.filter(Jurisdiction.government_level_id == government_level)
    
    if office_type:
        query = query.filter(Office.office_type == office_type)
    
    if province:
        query = query.filter(Jurisdiction.province == province)
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get offices
    offices = query.offset(offset).limit(page_size).all()
    
    # Convert to response format
    office_responses = []
    for office in offices:
        # Get jurisdiction details
        jurisdiction = db.query(Jurisdiction).filter(
            Jurisdiction.id == office.jurisdiction_id
        ).first()
        
        gov_level = db.query(GovernmentLevel).filter(
            GovernmentLevel.id == jurisdiction.government_level_id
        ).first()
        
        from app.schemas.multi_level_government import GovernmentLevelResponse, JurisdictionResponse
        
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
        
        office_responses.append(OfficeResponse(
            id=str(office.id),
            name=office.name,
            jurisdiction_id=str(office.jurisdiction_id),
            office_type=office.office_type,
            location=office.location,
            phone=office.phone,
            email=office.email,
            extras=office.extras,
            jurisdiction=jurisdiction_response,
            created_at=office.created_at,
            updated_at=office.updated_at
        ))
    
    # Create pagination info
    from app.schemas.multi_level_government import PaginationInfo
    pagination = PaginationInfo(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )
    
    return OfficeListResponse(items=office_responses, pagination=pagination)


@router.get("/offices/{office_id}", response_model=OfficeResponse)
async def get_office(
    office_id: str = Path(..., description="Office ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get a specific office by ID.
    
    Returns detailed information about an office including jurisdiction and government level.
    """
    office = db.query(Office).filter(Office.id == office_id).first()
    
    if not office:
        raise HTTPException(status_code=404, detail="Office not found")
    
    # Get jurisdiction details
    jurisdiction = db.query(Jurisdiction).filter(
        Jurisdiction.id == office.jurisdiction_id
    ).first()
    
    gov_level = db.query(GovernmentLevel).filter(
        GovernmentLevel.id == jurisdiction.government_level_id
    ).first()
    
    from app.schemas.multi_level_government import GovernmentLevelResponse, JurisdictionResponse
    
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
    
    return OfficeResponse(
        id=str(office.id),
        name=office.name,
        jurisdiction_id=str(office.jurisdiction_id),
        office_type=office.office_type,
        location=office.location,
        phone=office.phone,
        email=office.email,
        extras=office.extras,
        jurisdiction=jurisdiction_response,
        created_at=office.created_at,
        updated_at=office.updated_at
    )


# ============================================================================
# Bills Endpoints
# ============================================================================

@router.get("/bills", response_model=BillListResponse)
async def list_bills(
    q: Optional[str] = Query(None, description="Search query for bill title"),
    jurisdiction_id: Optional[str] = Query(None, description="Filter by jurisdiction ID"),
    government_level: Optional[str] = Query(None, description="Filter by government level ID"),
    status: Optional[str] = Query(None, description="Filter by bill status"),
    sponsor_id: Optional[str] = Query(None, description="Filter by sponsor representative ID"),
    introduced_after: Optional[datetime] = Query(None, description="Filter by introduction date (after)"),
    introduced_before: Optional[datetime] = Query(None, description="Filter by introduction date (before)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    List all bills across all government levels.
    
    Supports search, filtering, and pagination.
    """
    # Build base query
    query = db.query(Bill).join(Jurisdiction).join(GovernmentLevel)
    
    # Apply filters
    if jurisdiction_id:
        query = query.filter(Bill.jurisdiction_id == jurisdiction_id)
    
    if government_level:
        query = query.filter(Jurisdiction.government_level_id == government_level)
    
    if status:
        query = query.filter(Bill.status == status)
    
    if sponsor_id:
        query = query.filter(Bill.sponsor_id == sponsor_id)
    
    if introduced_after:
        query = query.filter(Bill.introduced_date >= introduced_after)
    
    if introduced_before:
        query = query.filter(Bill.introduced_date <= introduced_before)
    
    # Apply search if query provided
    if q:
        search_query = text("""
            to_tsvector('english', bills.title) @@ plainto_tsquery('english', :search_term)
        """)
        query = query.filter(search_query.bindparams(search_term=q))
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get bills
    bills = query.offset(offset).limit(page_size).all()
    
    # Convert to response format
    bill_responses = []
    for bill in bills:
        # Get jurisdiction details
        jurisdiction = db.query(Jurisdiction).filter(
            Jurisdiction.id == bill.jurisdiction_id
        ).first()
        
        gov_level = db.query(GovernmentLevel).filter(
            GovernmentLevel.id == jurisdiction.government_level_id
        ).first()
        
        from app.schemas.multi_level_government import GovernmentLevelResponse, JurisdictionResponse, RepresentativeResponse
        
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
        
        # Get sponsor details if available
        sponsor_response = None
        if bill.sponsor_id:
            sponsor = db.query(Representative).filter(
                Representative.id == bill.sponsor_id
            ).first()
            
            if sponsor:
                sponsor_response = RepresentativeResponse(
                    id=str(sponsor.id),
                    name=sponsor.name,
                    jurisdiction_id=str(sponsor.jurisdiction_id),
                    party=sponsor.party,
                    position=sponsor.position,
                    riding=sponsor.riding,
                    email=sponsor.email,
                    phone=sponsor.phone,
                    website=sponsor.website,
                    extras=sponsor.extras,
                    metadata_json=sponsor.metadata_json,
                    jurisdiction=jurisdiction_response,
                    created_at=sponsor.created_at,
                    updated_at=sponsor.updated_at
                )
        
        bill_responses.append(BillResponse(
            id=str(bill.id),
            title=bill.title,
            jurisdiction_id=str(bill.jurisdiction_id),
            bill_number=bill.bill_number,
            summary=bill.summary,
            status=bill.status,
            introduced_date=bill.introduced_date,
            sponsor_id=str(bill.sponsor_id) if bill.sponsor_id else None,
            extras=bill.extras,
            jurisdiction=jurisdiction_response,
            sponsor=sponsor_response,
            created_at=bill.created_at,
            updated_at=bill.updated_at
        ))
    
    # Create pagination info
    from app.schemas.multi_level_government import PaginationInfo
    pagination = PaginationInfo(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )
    
    return BillListResponse(items=bill_responses, pagination=pagination)


@router.get("/bills/{bill_id}", response_model=BillResponse)
async def get_bill(
    bill_id: str = Path(..., description="Bill ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get a specific bill by ID.
    
    Returns detailed information about a bill including jurisdiction, government level, and sponsor.
    """
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # Get jurisdiction details
    jurisdiction = db.query(Jurisdiction).filter(
        Jurisdiction.id == bill.jurisdiction_id
    ).first()
    
    gov_level = db.query(GovernmentLevel).filter(
        GovernmentLevel.id == jurisdiction.government_level_id
    ).first()
    
    from app.schemas.multi_level_government import GovernmentLevelResponse, JurisdictionResponse, RepresentativeResponse
    
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
    
    # Get sponsor details if available
    sponsor_response = None
    if bill.sponsor_id:
        sponsor = db.query(Representative).filter(
            Representative.id == bill.sponsor_id
        ).first()
        
        if sponsor:
            sponsor_response = RepresentativeResponse(
                id=str(sponsor.id),
                name=sponsor.name,
                jurisdiction_id=str(sponsor.jurisdiction_id),
                party=sponsor.party,
                position=sponsor.position,
                riding=sponsor.riding,
                email=sponsor.email,
                phone=sponsor.phone,
                website=sponsor.website,
                extras=sponsor.extras,
                metadata_json=sponsor.metadata_json,
                jurisdiction=jurisdiction_response,
                created_at=sponsor.created_at,
                updated_at=sponsor.updated_at
            )
    
    return BillResponse(
        id=str(bill.id),
        title=bill.title,
        jurisdiction_id=str(bill.jurisdiction_id),
        bill_number=bill.bill_number,
        summary=bill.summary,
        status=bill.status,
        introduced_date=bill.introduced_date,
        sponsor_id=str(bill.sponsor_id) if bill.sponsor_id else None,
        extras=bill.extras,
        jurisdiction=jurisdiction_response,
        sponsor=sponsor_response,
        created_at=bill.created_at,
        updated_at=bill.updated_at
    )


# ============================================================================
# Votes Endpoints
# ============================================================================

@router.get("/votes", response_model=VoteListResponse)
async def list_votes(
    bill_id: Optional[str] = Query(None, description="Filter by bill ID"),
    representative_id: Optional[str] = Query(None, description="Filter by representative ID"),
    vote_position: Optional[str] = Query(None, description="Filter by vote position"),
    vote_after: Optional[datetime] = Query(None, description="Filter by vote date (after)"),
    vote_before: Optional[datetime] = Query(None, description="Filter by vote date (before)"),
    session: Optional[str] = Query(None, description="Filter by session"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    List all votes across all government levels.
    
    Supports filtering and pagination.
    """
    # Build base query
    query = db.query(Vote).join(Bill).join(Jurisdiction).join(GovernmentLevel)
    
    # Apply filters
    if bill_id:
        query = query.filter(Vote.bill_id == bill_id)
    
    if representative_id:
        query = query.filter(Vote.representative_id == representative_id)
    
    if vote_position:
        query = query.filter(Vote.vote_position == vote_position)
    
    if vote_after:
        query = query.filter(Vote.vote_date >= vote_after)
    
    if vote_before:
        query = query.filter(Vote.vote_date <= vote_before)
    
    if session:
        query = query.filter(Vote.session == session)
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get votes
    votes = query.offset(offset).limit(page_size).all()
    
    # Convert to response format
    vote_responses = []
    for vote in votes:
        # Get bill details
        bill = db.query(Bill).filter(Bill.id == vote.bill_id).first()
        
        # Get representative details
        representative = db.query(Representative).filter(
            Representative.id == vote.representative_id
        ).first()
        
        # Get jurisdiction details
        jurisdiction = db.query(Jurisdiction).filter(
            Jurisdiction.id == bill.jurisdiction_id
        ).first()
        
        gov_level = db.query(GovernmentLevel).filter(
            GovernmentLevel.id == jurisdiction.government_level_id
        ).first()
        
        from app.schemas.multi_level_government import (
            GovernmentLevelResponse, JurisdictionResponse, RepresentativeResponse, BillResponse
        )
        
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
        
        bill_response = BillResponse(
            id=str(bill.id),
            title=bill.title,
            jurisdiction_id=str(bill.jurisdiction_id),
            bill_number=bill.bill_number,
            summary=bill.summary,
            status=bill.status,
            introduced_date=bill.introduced_date,
            sponsor_id=str(bill.sponsor_id) if bill.sponsor_id else None,
            extras=bill.extras,
            jurisdiction=jurisdiction_response,
            sponsor=None,  # Skip sponsor to avoid circular reference
            created_at=bill.created_at,
            updated_at=bill.updated_at
        )
        
        representative_response = RepresentativeResponse(
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
        
        vote_responses.append(VoteResponse(
            id=str(vote.id),
            bill_id=str(vote.bill_id),
            representative_id=str(vote.representative_id),
            vote_position=vote.vote_position,
            vote_date=vote.vote_date,
            session=vote.session,
            extras=vote.extras,
            bill=bill_response,
            representative=representative_response,
            created_at=vote.created_at,
            updated_at=vote.updated_at
        ))
    
    # Create pagination info
    from app.schemas.multi_level_government import PaginationInfo
    pagination = PaginationInfo(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )
    
    return VoteListResponse(items=vote_responses, pagination=pagination)


# ============================================================================
# Data Sources Endpoints
# ============================================================================

@router.get("/data-sources", response_model=DataSourceListResponse)
async def list_data_sources(
    jurisdiction_id: Optional[str] = Query(None, description="Filter by jurisdiction ID"),
    government_level: Optional[str] = Query(None, description="Filter by government level ID"),
    source_type: Optional[str] = Query(None, description="Filter by source type"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    List all data sources across all government levels.
    
    Supports filtering by jurisdiction, government level, and source type.
    """
    # Build base query
    query = db.query(DataSource).join(Jurisdiction).join(GovernmentLevel)
    
    # Apply filters
    if jurisdiction_id:
        query = query.filter(DataSource.jurisdiction_id == jurisdiction_id)
    
    if government_level:
        query = query.filter(Jurisdiction.government_level_id == government_level)
    
    if source_type:
        query = query.filter(DataSource.source_type == source_type)
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get data sources
    data_sources = query.offset(offset).limit(page_size).all()
    
    # Convert to response format
    data_source_responses = []
    for source in data_sources:
        # Get jurisdiction details
        jurisdiction = db.query(Jurisdiction).filter(
            Jurisdiction.id == source.jurisdiction_id
        ).first()
        
        gov_level = db.query(GovernmentLevel).filter(
            GovernmentLevel.id == jurisdiction.government_level_id
        ).first()
        
        from app.schemas.multi_level_government import GovernmentLevelResponse, JurisdictionResponse
        
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
        
        data_source_responses.append(DataSourceResponse(
            id=str(source.id),
            name=source.name,
            jurisdiction_id=str(source.jurisdiction_id),
            source_type=source.source_type,
            url=source.url,
            legacy_module=source.legacy_module,
            legacy_class=source.legacy_class,
            last_updated=source.last_updated,
            extras=source.extras,
            jurisdiction=jurisdiction_response,
            created_at=source.created_at,
            updated_at=source.updated_at
        ))
    
    # Create pagination info
    from app.schemas.multi_level_government import PaginationInfo
    pagination = PaginationInfo(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )
    
    return DataSourceListResponse(items=data_source_responses, pagination=pagination)
