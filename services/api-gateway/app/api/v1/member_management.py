"""
Member Management API endpoints.

Implements FEAT-015 Member Management (P0 priority).
Provides administrative endpoints for managing members.
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body, File, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import (
    get_current_user,
    require_permission,
    require_admin
)
from app.core.member_management import (
    MemberManagementService,
    get_member_management_service
)
from app.models.users import User
from app.models.member_management import MemberTag, MemberImport
from app.schemas.member_management import (
    MemberCreate, MemberUpdate, MemberManagementResponse,
    MemberSearchRequest, MemberExportRequest, MemberDuplicateCheck,
    MemberMergeRequest, BulkMemberImport, BulkOperationRequest,
    BulkOperationResponse, ImportStatusResponse,
    ContactCreate, ContactUpdate, ContactResponse,
    SocialMediaCreate, SocialMediaUpdate, SocialMediaResponse,
    EducationCreate, EducationResponse,
    ProfessionCreate, ProfessionResponse,
    TagCreate, TagResponse,
    AuditLogResponse, MemberMetricsUpdate, MemberMetricsResponse
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# Member CRUD endpoints
@router.post("/", response_model=MemberManagementResponse, status_code=status.HTTP_201_CREATED)
async def create_member(
    member_data: MemberCreate,
    current_user: User = Depends(require_permission("members", "write")),
    db: Session = Depends(get_db)
):
    """Create a new member."""
    service = get_member_management_service(db)
    member = service.create_member(member_data, current_user)
    
    # Get full response with counts
    response = MemberManagementResponse.from_orm(member)
    response.contact_count = len(member.contacts)
    response.social_media_count = len(member.social_media)
    response.education_count = len(member.education)
    response.profession_count = len(member.professions)
    response.tag_count = len(member.tags) if hasattr(member, 'tags') else 0
    
    if hasattr(member, 'metrics') and member.metrics:
        response.activity_score = member.metrics.activity_score
        response.influence_score = member.metrics.influence_score
    
    return response


@router.put("/{member_id}", response_model=MemberManagementResponse)
async def update_member(
    member_id: UUID,
    member_data: MemberUpdate,
    reason: Optional[str] = Query(None, description="Reason for update"),
    current_user: User = Depends(require_permission("members", "write")),
    db: Session = Depends(get_db)
):
    """Update a member."""
    service = get_member_management_service(db)
    member = service.update_member(member_id, member_data, current_user, reason)
    
    # Get full response with counts
    response = MemberManagementResponse.from_orm(member)
    response.contact_count = len(member.contacts)
    response.social_media_count = len(member.social_media)
    response.education_count = len(member.education)
    response.profession_count = len(member.professions)
    response.tag_count = len(member.tags) if hasattr(member, 'tags') else 0
    
    if hasattr(member, 'metrics') and member.metrics:
        response.activity_score = member.metrics.activity_score
        response.influence_score = member.metrics.influence_score
    
    return response


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_member(
    member_id: UUID,
    reason: str = Query(..., description="Reason for deletion"),
    current_user: User = Depends(require_permission("members", "delete")),
    db: Session = Depends(get_db)
):
    """Delete a member (soft delete)."""
    service = get_member_management_service(db)
    service.delete_member(member_id, current_user, reason)


# Search and filtering
@router.post("/search", response_model=dict)
async def search_members(
    search_request: MemberSearchRequest,
    current_user: User = Depends(require_permission("members", "read")),
    db: Session = Depends(get_db)
):
    """Search members with advanced filtering."""
    service = get_member_management_service(db)
    members, total_count = service.search_members(search_request)
    
    # Build response
    results = []
    for member in members:
        response = MemberManagementResponse.from_orm(member)
        response.contact_count = len(member.contacts)
        response.social_media_count = len(member.social_media)
        response.education_count = len(member.education)
        response.profession_count = len(member.professions)
        response.tag_count = len(member.tags) if hasattr(member, 'tags') else 0
        
        if hasattr(member, 'metrics') and member.metrics:
            response.activity_score = member.metrics.activity_score
            response.influence_score = member.metrics.influence_score
        
        results.append(response)
    
    return {
        "results": results,
        "pagination": {
            "page": search_request.page,
            "page_size": search_request.page_size,
            "total": total_count,
            "total_pages": (total_count + search_request.page_size - 1) // search_request.page_size
        }
    }


# Bulk operations
@router.post("/bulk/import", response_model=ImportStatusResponse)
async def bulk_import_members(
    import_data: BulkMemberImport,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Bulk import members from various sources."""
    service = get_member_management_service(db)
    import_record = service.bulk_import_members(import_data, current_user)
    return ImportStatusResponse.from_orm(import_record)


@router.post("/bulk/import/csv", response_model=ImportStatusResponse)
async def import_members_csv(
    file: UploadFile = File(...),
    import_type: str = Query("incremental", regex="^(full|incremental|update)$"),
    update_existing: bool = Query(True),
    dry_run: bool = Query(False),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Import members from CSV file."""
    # Read CSV content
    content = await file.read()
    csv_data = content.decode('utf-8')
    
    import_data = BulkMemberImport(
        import_source="csv",
        import_type=import_type,
        csv_data=csv_data,
        update_existing=update_existing,
        dry_run=dry_run
    )
    
    service = get_member_management_service(db)
    import_record = service.bulk_import_members(import_data, current_user)
    return ImportStatusResponse.from_orm(import_record)


@router.post("/bulk/operation", response_model=BulkOperationResponse)
async def bulk_member_operation(
    operation_request: BulkOperationRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Perform bulk operations on members."""
    service = get_member_management_service(db)
    result = service.bulk_operation(operation_request, current_user)
    return BulkOperationResponse(**result)


# Export endpoints
@router.post("/export")
async def export_members(
    export_request: MemberExportRequest,
    member_ids: Optional[List[UUID]] = Query(None),
    current_user: User = Depends(require_permission("members", "read")),
    db: Session = Depends(get_db)
):
    """Export members in various formats."""
    service = get_member_management_service(db)
    export_data = service.export_members(export_request, member_ids)
    
    # Set appropriate content type
    if export_request.format == "json":
        media_type = "application/json"
        filename = "members_export.json"
    elif export_request.format == "csv":
        media_type = "text/csv"
        filename = "members_export.csv"
    else:
        media_type = "application/octet-stream"
        filename = "members_export"
    
    return Response(
        content=export_data,
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


# Duplicate detection and merging
@router.post("/check-duplicates", response_model=List[dict])
async def check_duplicate_members(
    check_data: MemberDuplicateCheck,
    current_user: User = Depends(require_permission("members", "read")),
    db: Session = Depends(get_db)
):
    """Check for potential duplicate members."""
    service = get_member_management_service(db)
    duplicates = service.check_duplicates(check_data)
    return duplicates


@router.post("/merge", response_model=MemberManagementResponse)
async def merge_members(
    merge_request: MemberMergeRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Merge duplicate members."""
    service = get_member_management_service(db)
    member = service.merge_members(merge_request, current_user)
    
    # Get full response
    response = MemberManagementResponse.from_orm(member)
    response.contact_count = len(member.contacts)
    response.social_media_count = len(member.social_media)
    response.education_count = len(member.education)
    response.profession_count = len(member.professions)
    response.tag_count = len(member.tags) if hasattr(member, 'tags') else 0
    
    return response


# Contact management
@router.post("/{member_id}/contacts", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def add_member_contact(
    member_id: UUID,
    contact_data: ContactCreate,
    current_user: User = Depends(require_permission("members", "write")),
    db: Session = Depends(get_db)
):
    """Add contact information to a member."""
    # Verify member exists
    from app.models.openparliament import Member
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    # Create contact
    from app.models.member_management import MemberContact
    contact = MemberContact(
        member_id=member_id,
        **contact_data.dict(exclude={'member_id'})
    )
    db.add(contact)
    
    # Create audit log
    service = get_member_management_service(db)
    service._create_audit_log(
        member_id=member_id,
        user_id=current_user.id,
        action="add_contact",
        changes={"new": contact_data.dict()},
        reason="Added contact information"
    )
    
    db.commit()
    return ContactResponse.from_orm(contact)


@router.put("/{member_id}/contacts/{contact_id}", response_model=ContactResponse)
async def update_member_contact(
    member_id: UUID,
    contact_id: UUID,
    contact_data: ContactUpdate,
    current_user: User = Depends(require_permission("members", "write")),
    db: Session = Depends(get_db)
):
    """Update member contact information."""
    from app.models.member_management import MemberContact
    
    contact = db.query(MemberContact).filter(
        MemberContact.id == contact_id,
        MemberContact.member_id == member_id
    ).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    # Update fields
    for field, value in contact_data.dict(exclude_unset=True).items():
        setattr(contact, field, value)
    
    db.commit()
    return ContactResponse.from_orm(contact)


@router.delete("/{member_id}/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_member_contact(
    member_id: UUID,
    contact_id: UUID,
    current_user: User = Depends(require_permission("members", "write")),
    db: Session = Depends(get_db)
):
    """Delete member contact information."""
    from app.models.member_management import MemberContact
    
    contact = db.query(MemberContact).filter(
        MemberContact.id == contact_id,
        MemberContact.member_id == member_id
    ).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    db.delete(contact)
    db.commit()


# Social media management
@router.post("/{member_id}/social-media", response_model=SocialMediaResponse, status_code=status.HTTP_201_CREATED)
async def add_member_social_media(
    member_id: UUID,
    social_data: SocialMediaCreate,
    current_user: User = Depends(require_permission("members", "write")),
    db: Session = Depends(get_db)
):
    """Add social media account to a member."""
    # Verify member exists
    from app.models.openparliament import Member
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    # Create social media
    from app.models.member_management import MemberSocialMedia
    social = MemberSocialMedia(
        member_id=member_id,
        **social_data.dict(exclude={'member_id'})
    )
    db.add(social)
    
    # Create audit log
    service = get_member_management_service(db)
    service._create_audit_log(
        member_id=member_id,
        user_id=current_user.id,
        action="add_social_media",
        changes={"new": social_data.dict()},
        reason="Added social media account"
    )
    
    db.commit()
    return SocialMediaResponse.from_orm(social)


# Tag management
@router.get("/tags", response_model=List[TagResponse])
async def list_tags(
    category: Optional[str] = Query(None),
    is_active: bool = Query(True),
    current_user: User = Depends(require_permission("members", "read")),
    db: Session = Depends(get_db)
):
    """List all available tags."""
    query = db.query(MemberTag)
    
    if category:
        query = query.filter(MemberTag.category == category)
    if is_active is not None:
        query = query.filter(MemberTag.is_active == is_active)
    
    tags = query.order_by(MemberTag.name).all()
    
    # Add member count
    responses = []
    for tag in tags:
        response = TagResponse.from_orm(tag)
        response.member_count = len(tag.members) if hasattr(tag, 'members') else 0
        responses.append(response)
    
    return responses


@router.post("/tags", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new tag."""
    service = get_member_management_service(db)
    tag = service.create_tag(tag_data)
    
    response = TagResponse.from_orm(tag)
    response.member_count = 0
    return response


@router.post("/{member_id}/tags")
async def add_tags_to_member(
    member_id: UUID,
    tag_ids: List[UUID] = Body(...),
    current_user: User = Depends(require_permission("members", "write")),
    db: Session = Depends(get_db)
):
    """Add tags to a member."""
    service = get_member_management_service(db)
    service._add_tags_to_member(member_id, tag_ids, current_user.id)
    db.commit()
    
    return {"message": "Tags added successfully"}


@router.delete("/{member_id}/tags")
async def remove_tags_from_member(
    member_id: UUID,
    tag_ids: List[UUID] = Body(...),
    current_user: User = Depends(require_permission("members", "write")),
    db: Session = Depends(get_db)
):
    """Remove tags from a member."""
    service = get_member_management_service(db)
    service._remove_tags_from_member(member_id, tag_ids)
    db.commit()
    
    return {"message": "Tags removed successfully"}


# Member metrics
@router.put("/{member_id}/metrics", response_model=MemberMetricsResponse)
async def update_member_metrics(
    member_id: UUID,
    metrics_data: MemberMetricsUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update member metrics."""
    service = get_member_management_service(db)
    metrics = service.update_member_metrics(member_id, metrics_data)
    return MemberMetricsResponse.from_orm(metrics)


@router.get("/{member_id}/metrics", response_model=MemberMetricsResponse)
async def get_member_metrics(
    member_id: UUID,
    current_user: User = Depends(require_permission("members", "read")),
    db: Session = Depends(get_db)
):
    """Get member metrics."""
    from app.models.member_management import MemberMetrics
    
    metrics = db.query(MemberMetrics).filter(
        MemberMetrics.member_id == member_id
    ).first()
    
    if not metrics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member metrics not found"
        )
    
    return MemberMetricsResponse.from_orm(metrics)


# Audit logs
@router.get("/{member_id}/audit-logs", response_model=List[AuditLogResponse])
async def get_member_audit_logs(
    member_id: UUID,
    action: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get audit logs for a member."""
    from app.models.member_management import MemberAudit
    
    query = db.query(MemberAudit).filter(MemberAudit.member_id == member_id)
    
    if action:
        query = query.filter(MemberAudit.action == action)
    
    audits = query.order_by(MemberAudit.timestamp.desc()).limit(limit).all()
    
    # Build responses with user info
    responses = []
    for audit in audits:
        response = AuditLogResponse.from_orm(audit)
        response.user_email = audit.user.email if audit.user else "Unknown"
        responses.append(response)
    
    return responses


# Import status
@router.get("/imports", response_model=List[ImportStatusResponse])
async def list_imports(
    status: Optional[str] = Query(None, regex="^(pending|processing|completed|failed)$"),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """List import operations."""
    query = db.query(MemberImport)
    
    if status:
        query = query.filter(MemberImport.status == status)
    
    imports = query.order_by(MemberImport.started_at.desc()).limit(limit).all()
    
    return [ImportStatusResponse.from_orm(imp) for imp in imports]


@router.get("/imports/{import_id}", response_model=ImportStatusResponse)
async def get_import_status(
    import_id: UUID,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get status of a specific import operation."""
    import_record = db.query(MemberImport).filter(
        MemberImport.id == import_id
    ).first()
    
    if not import_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Import not found"
        )
    
    return ImportStatusResponse.from_orm(import_record)