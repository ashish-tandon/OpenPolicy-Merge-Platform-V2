"""
Core Member Management Service

Business logic for member management functionality.
Implements FEAT-015 Member Management (P0 priority).
"""

from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, date
from uuid import UUID
import csv
import json
import io
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func
from fastapi import HTTPException, status
from app.models.openparliament import Member, Party, Jurisdiction
from app.models.member_management import (
    MemberAudit, MemberImport, MemberContact, MemberSocialMedia,
    MemberEducation, MemberProfession, MemberTag, MemberMetrics,
    member_tag_associations
)
from app.models.users import User
from app.schemas.member_management import (
    MemberCreate, MemberUpdate, MemberSearchRequest,
    ContactCreate, ContactUpdate, SocialMediaCreate, SocialMediaUpdate,
    EducationCreate, ProfessionCreate, TagCreate,
    BulkMemberImport, BulkOperationRequest, MemberDuplicateCheck,
    MemberMergeRequest, MemberExportRequest, MemberMetricsUpdate
)
import logging

logger = logging.getLogger(__name__)


class MemberManagementService:
    """Service for managing members."""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Member CRUD operations
    def create_member(self, member_data: MemberCreate, user: User) -> Member:
        """Create a new member."""
        # Check for duplicates
        duplicates = self.check_duplicates(MemberDuplicateCheck(
            first_name=member_data.first_name,
            last_name=member_data.last_name,
            email=member_data.email,
            district=member_data.district,
            jurisdiction_id=member_data.jurisdiction_id
        ))
        
        if duplicates:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Potential duplicate member found: {duplicates[0]['full_name']}"
            )
        
        # Create member
        member = Member(
            **member_data.dict(exclude={'bio', 'photo_url'}),
            full_name=f"{member_data.first_name} {member_data.last_name}"
        )
        
        self.db.add(member)
        self.db.flush()
        
        # Create audit log
        self._create_audit_log(
            member_id=member.id,
            user_id=user.id,
            action="create",
            changes={"new": member_data.dict()},
            reason="Manual creation"
        )
        
        self.db.commit()
        logger.info(f"Created member: {member.full_name} (ID: {member.id})")
        
        return member
    
    def update_member(
        self, 
        member_id: UUID, 
        member_data: MemberUpdate, 
        user: User,
        reason: Optional[str] = None
    ) -> Member:
        """Update a member."""
        member = self.db.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found"
            )
        
        # Track changes
        old_data = {
            k: getattr(member, k) 
            for k in member_data.dict(exclude_unset=True).keys()
        }
        
        # Update fields
        update_data = member_data.dict(exclude_unset=True)
        if 'first_name' in update_data or 'last_name' in update_data:
            first_name = update_data.get('first_name', member.first_name)
            last_name = update_data.get('last_name', member.last_name)
            update_data['full_name'] = f"{first_name} {last_name}"
        
        for field, value in update_data.items():
            setattr(member, field, value)
        
        # Create audit log
        self._create_audit_log(
            member_id=member.id,
            user_id=user.id,
            action="update",
            changes={"old": old_data, "new": update_data},
            reason=reason
        )
        
        self.db.commit()
        logger.info(f"Updated member: {member.full_name} (ID: {member.id})")
        
        return member
    
    def delete_member(
        self, 
        member_id: UUID, 
        user: User,
        reason: str
    ) -> None:
        """Delete a member (soft delete by setting end_date)."""
        member = self.db.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found"
            )
        
        # Soft delete by setting end date
        if not member.end_date:
            member.end_date = date.today()
        
        # Create audit log
        self._create_audit_log(
            member_id=member.id,
            user_id=user.id,
            action="delete",
            reason=reason
        )
        
        self.db.commit()
        logger.info(f"Deleted member: {member.full_name} (ID: {member.id})")
    
    # Search and filtering
    def search_members(self, search_request: MemberSearchRequest) -> Tuple[List[Member], int]:
        """Search members with advanced filtering."""
        query = self.db.query(Member).options(
            joinedload(Member.party),
            joinedload(Member.jurisdiction)
        )
        
        # Text search
        if search_request.query:
            search_term = f"%{search_request.query}%"
            query = query.filter(
                or_(
                    Member.full_name.ilike(search_term),
                    Member.district.ilike(search_term),
                    Member.email.ilike(search_term)
                )
            )
        
        # Filters
        if search_request.jurisdiction_ids:
            query = query.filter(Member.jurisdiction_id.in_(search_request.jurisdiction_ids))
        
        if search_request.party_ids:
            query = query.filter(Member.party_id.in_(search_request.party_ids))
        
        if search_request.districts:
            query = query.filter(Member.district.in_(search_request.districts))
        
        if search_request.roles:
            query = query.filter(Member.role.in_(search_request.roles))
        
        if search_request.is_current is not None:
            if search_request.is_current:
                query = query.filter(Member.end_date.is_(None))
            else:
                query = query.filter(Member.end_date.isnot(None))
        
        # Tag filter
        if search_request.tag_ids:
            query = query.join(member_tag_associations).filter(
                member_tag_associations.c.tag_id.in_(search_request.tag_ids)
            )
        
        # Activity score filter
        if search_request.min_activity_score is not None or search_request.max_activity_score is not None:
            query = query.join(MemberMetrics)
            if search_request.min_activity_score:
                query = query.filter(MemberMetrics.activity_score >= search_request.min_activity_score)
            if search_request.max_activity_score:
                query = query.filter(MemberMetrics.activity_score <= search_request.max_activity_score)
        
        # Social media filter
        if search_request.has_social_media is not None:
            if search_request.has_social_media:
                query = query.join(MemberSocialMedia).distinct()
            else:
                query = query.outerjoin(MemberSocialMedia).filter(
                    MemberSocialMedia.id.is_(None)
                )
        
        # Get total count
        total_count = query.count()
        
        # Sorting
        sort_column = getattr(Member, search_request.sort_by)
        if search_request.sort_by in ['activity_score', 'influence_score']:
            query = query.join(MemberMetrics)
            sort_column = getattr(MemberMetrics, search_request.sort_by)
        
        if search_request.sort_order == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column)
        
        # Pagination
        offset = (search_request.page - 1) * search_request.page_size
        members = query.offset(offset).limit(search_request.page_size).all()
        
        return members, total_count
    
    # Bulk operations
    def bulk_import_members(
        self, 
        import_data: BulkMemberImport,
        user: User
    ) -> MemberImport:
        """Bulk import members from various sources."""
        import_record = MemberImport(
            import_source=import_data.import_source,
            import_type=import_data.import_type,
            status="processing",
            user_id=user.id
        )
        self.db.add(import_record)
        self.db.flush()
        
        try:
            members_data = []
            
            # Parse data based on source
            if import_data.import_source == "csv" and import_data.csv_data:
                members_data = self._parse_csv_import(import_data.csv_data)
            elif import_data.member_data:
                members_data = import_data.member_data
            else:
                raise ValueError("No import data provided")
            
            import_record.total_records = len(members_data)
            errors = []
            
            for idx, member_data in enumerate(members_data):
                try:
                    if import_data.dry_run:
                        # Just validate
                        self._validate_member_data(member_data)
                    else:
                        # Check for existing member
                        existing = self._find_existing_member(member_data)
                        
                        if existing and import_data.update_existing:
                            # Update existing
                            self.update_member(
                                existing.id,
                                MemberUpdate(**member_data.dict()),
                                user,
                                reason=f"Bulk import update from {import_data.import_source}"
                            )
                            import_record.updated_count += 1
                        elif not existing:
                            # Create new
                            self.create_member(member_data, user)
                            import_record.created_count += 1
                    
                    import_record.processed_records += 1
                    
                except Exception as e:
                    import_record.error_count += 1
                    errors.append({
                        "index": idx,
                        "member": member_data.dict() if hasattr(member_data, 'dict') else member_data,
                        "error": str(e)
                    })
            
            import_record.status = "completed"
            import_record.completed_at = datetime.utcnow()
            if errors:
                import_record.errors = errors
            
        except Exception as e:
            import_record.status = "failed"
            import_record.errors = [{"error": str(e)}]
            import_record.completed_at = datetime.utcnow()
            logger.error(f"Bulk import failed: {str(e)}")
        
        self.db.commit()
        return import_record
    
    def bulk_operation(
        self,
        operation_request: BulkOperationRequest,
        user: User
    ) -> Dict[str, Any]:
        """Perform bulk operations on members."""
        start_time = datetime.utcnow()
        success_count = 0
        errors = []
        
        for member_id in operation_request.member_ids:
            try:
                if operation_request.operation == "delete":
                    self.delete_member(
                        member_id, 
                        user,
                        operation_request.reason or "Bulk delete"
                    )
                elif operation_request.operation == "archive":
                    member = self.db.query(Member).filter(Member.id == member_id).first()
                    if member and not member.end_date:
                        member.end_date = date.today()
                        self._create_audit_log(
                            member_id=member_id,
                            user_id=user.id,
                            action="archive",
                            reason=operation_request.reason
                        )
                elif operation_request.operation == "tag":
                    tag_ids = operation_request.parameters.get('tag_ids', [])
                    self._add_tags_to_member(member_id, tag_ids, user.id)
                elif operation_request.operation == "untag":
                    tag_ids = operation_request.parameters.get('tag_ids', [])
                    self._remove_tags_from_member(member_id, tag_ids)
                
                success_count += 1
                
            except Exception as e:
                errors.append({
                    "member_id": str(member_id),
                    "error": str(e)
                })
        
        self.db.commit()
        
        duration = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "operation": operation_request.operation,
            "total_count": len(operation_request.member_ids),
            "success_count": success_count,
            "error_count": len(errors),
            "errors": errors if errors else None,
            "duration_seconds": duration
        }
    
    # Duplicate detection and merging
    def check_duplicates(self, check_data: MemberDuplicateCheck) -> List[Dict[str, Any]]:
        """Check for potential duplicate members."""
        query = self.db.query(Member)
        
        # Name matching
        query = query.filter(
            and_(
                func.lower(Member.first_name) == check_data.first_name.lower(),
                func.lower(Member.last_name) == check_data.last_name.lower()
            )
        )
        
        # Additional criteria
        if check_data.email:
            query = query.filter(Member.email == check_data.email)
        if check_data.district:
            query = query.filter(Member.district == check_data.district)
        if check_data.jurisdiction_id:
            query = query.filter(Member.jurisdiction_id == check_data.jurisdiction_id)
        
        duplicates = query.all()
        
        return [
            {
                "id": str(m.id),
                "full_name": m.full_name,
                "district": m.district,
                "party": m.party.name if m.party else None,
                "is_current": m.end_date is None
            }
            for m in duplicates
        ]
    
    def merge_members(
        self,
        merge_request: MemberMergeRequest,
        user: User
    ) -> Member:
        """Merge duplicate members into one."""
        # Get primary member
        primary = self.db.query(Member).filter(
            Member.id == merge_request.primary_member_id
        ).first()
        
        if not primary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Primary member not found"
            )
        
        # Process each duplicate
        for dup_id in merge_request.duplicate_member_ids:
            duplicate = self.db.query(Member).filter(Member.id == dup_id).first()
            if not duplicate:
                continue
            
            # Merge relationships
            if merge_request.merge_contacts:
                for contact in duplicate.contacts:
                    contact.member_id = primary.id
            
            if merge_request.merge_social_media:
                for social in duplicate.social_media:
                    social.member_id = primary.id
            
            if merge_request.merge_education:
                for edu in duplicate.education:
                    edu.member_id = primary.id
            
            if merge_request.merge_professions:
                for prof in duplicate.professions:
                    prof.member_id = primary.id
            
            if merge_request.merge_tags:
                # Get duplicate's tags and add to primary
                dup_tags = self.db.query(member_tag_associations).filter(
                    member_tag_associations.c.member_id == dup_id
                ).all()
                
                for tag_assoc in dup_tags:
                    # Check if primary already has this tag
                    existing = self.db.query(member_tag_associations).filter(
                        and_(
                            member_tag_associations.c.member_id == primary.id,
                            member_tag_associations.c.tag_id == tag_assoc.tag_id
                        )
                    ).first()
                    
                    if not existing:
                        self.db.execute(
                            member_tag_associations.insert().values(
                                member_id=primary.id,
                                tag_id=tag_assoc.tag_id,
                                tagged_by=user.id
                            )
                        )
            
            # Create audit log for merge
            self._create_audit_log(
                member_id=primary.id,
                user_id=user.id,
                action="merge",
                changes={
                    "merged_from": str(dup_id),
                    "merge_options": merge_request.dict(exclude={'primary_member_id', 'duplicate_member_ids'})
                },
                reason=merge_request.reason
            )
            
            # Delete the duplicate
            self.db.delete(duplicate)
        
        self.db.commit()
        return primary
    
    # Export functionality
    def export_members(
        self,
        export_request: MemberExportRequest,
        member_ids: Optional[List[UUID]] = None
    ) -> bytes:
        """Export members in various formats."""
        # Get members
        query = self.db.query(Member).options(
            joinedload(Member.party),
            joinedload(Member.jurisdiction)
        )
        
        if member_ids:
            query = query.filter(Member.id.in_(member_ids))
        
        members = query.all()
        
        if export_request.format == "json":
            return self._export_json(members, export_request)
        elif export_request.format == "csv":
            return self._export_csv(members, export_request)
        else:
            raise ValueError(f"Unsupported export format: {export_request.format}")
    
    # Tag management
    def create_tag(self, tag_data: TagCreate) -> MemberTag:
        """Create a new tag."""
        # Check for duplicates
        existing = self.db.query(MemberTag).filter(
            func.lower(MemberTag.name) == tag_data.name.lower()
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Tag with this name already exists"
            )
        
        tag = MemberTag(**tag_data.dict())
        self.db.add(tag)
        self.db.commit()
        
        return tag
    
    def update_member_metrics(
        self,
        member_id: UUID,
        metrics_data: MemberMetricsUpdate
    ) -> MemberMetrics:
        """Update or create member metrics."""
        metrics = self.db.query(MemberMetrics).filter(
            MemberMetrics.member_id == member_id
        ).first()
        
        if not metrics:
            metrics = MemberMetrics(member_id=member_id)
            self.db.add(metrics)
        
        # Update fields
        for field, value in metrics_data.dict(exclude_unset=True).items():
            setattr(metrics, field, value)
        
        # Recalculate scores
        metrics = self._calculate_member_scores(metrics)
        metrics.last_calculated = datetime.utcnow()
        
        self.db.commit()
        return metrics
    
    # Helper methods
    def _create_audit_log(
        self,
        member_id: UUID,
        user_id: UUID,
        action: str,
        changes: Optional[Dict[str, Any]] = None,
        reason: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Create an audit log entry."""
        audit = MemberAudit(
            member_id=member_id,
            user_id=user_id,
            action=action,
            changes=changes,
            reason=reason,
            metadata=metadata
        )
        self.db.add(audit)
    
    def _parse_csv_import(self, csv_data: str) -> List[MemberCreate]:
        """Parse CSV data for import."""
        members = []
        reader = csv.DictReader(io.StringIO(csv_data))
        
        for row in reader:
            # Map CSV fields to MemberCreate schema
            member_data = MemberCreate(
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row.get('email'),
                phone=row.get('phone'),
                website=row.get('website'),
                district=row.get('district'),
                role=row.get('role'),
                party_id=row.get('party_id'),
                jurisdiction_id=row['jurisdiction_id'],
                start_date=row['start_date'],
                end_date=row.get('end_date')
            )
            members.append(member_data)
        
        return members
    
    def _validate_member_data(self, member_data: MemberCreate) -> None:
        """Validate member data."""
        # Check jurisdiction exists
        jurisdiction = self.db.query(Jurisdiction).filter(
            Jurisdiction.id == member_data.jurisdiction_id
        ).first()
        
        if not jurisdiction:
            raise ValueError(f"Invalid jurisdiction_id: {member_data.jurisdiction_id}")
        
        # Check party exists if provided
        if member_data.party_id:
            party = self.db.query(Party).filter(
                Party.id == member_data.party_id
            ).first()
            
            if not party:
                raise ValueError(f"Invalid party_id: {member_data.party_id}")
    
    def _find_existing_member(self, member_data: MemberCreate) -> Optional[Member]:
        """Find existing member based on name and jurisdiction."""
        return self.db.query(Member).filter(
            and_(
                func.lower(Member.first_name) == member_data.first_name.lower(),
                func.lower(Member.last_name) == member_data.last_name.lower(),
                Member.jurisdiction_id == member_data.jurisdiction_id
            )
        ).first()
    
    def _add_tags_to_member(
        self,
        member_id: UUID,
        tag_ids: List[UUID],
        user_id: UUID
    ) -> None:
        """Add tags to a member."""
        for tag_id in tag_ids:
            # Check if already tagged
            existing = self.db.query(member_tag_associations).filter(
                and_(
                    member_tag_associations.c.member_id == member_id,
                    member_tag_associations.c.tag_id == tag_id
                )
            ).first()
            
            if not existing:
                self.db.execute(
                    member_tag_associations.insert().values(
                        member_id=member_id,
                        tag_id=tag_id,
                        tagged_by=user_id
                    )
                )
    
    def _remove_tags_from_member(
        self,
        member_id: UUID,
        tag_ids: List[UUID]
    ) -> None:
        """Remove tags from a member."""
        self.db.execute(
            member_tag_associations.delete().where(
                and_(
                    member_tag_associations.c.member_id == member_id,
                    member_tag_associations.c.tag_id.in_(tag_ids)
                )
            )
        )
    
    def _calculate_member_scores(self, metrics: MemberMetrics) -> MemberMetrics:
        """Calculate activity, influence, and transparency scores."""
        # Activity score (0-100)
        activity_components = [
            min(metrics.bills_sponsored / 10, 1) * 25,  # Max 25 points
            min(metrics.votes_total / 100, 1) * 25,     # Max 25 points
            min(metrics.speeches_count / 20, 1) * 25,   # Max 25 points
            min(metrics.questions_asked / 10, 1) * 25   # Max 25 points
        ]
        metrics.activity_score = sum(activity_components)
        
        # Influence score (0-100)
        influence_components = [
            min(metrics.bills_sponsored / 5, 1) * 30,    # Max 30 points
            min(metrics.committee_memberships / 3, 1) * 30,  # Max 30 points
            min((metrics.twitter_followers or 0) / 10000, 1) * 20,  # Max 20 points
            min((metrics.facebook_likes or 0) / 5000, 1) * 20   # Max 20 points
        ]
        metrics.influence_score = sum(influence_components)
        
        # Transparency score (0-100) - based on data completeness
        # This would need more sophisticated calculation in production
        metrics.transparency_score = min(metrics.attendance_rate or 0, 100)
        
        return metrics
    
    def _export_json(
        self,
        members: List[Member],
        export_request: MemberExportRequest
    ) -> bytes:
        """Export members as JSON."""
        data = []
        
        for member in members:
            member_dict = {
                "id": str(member.id),
                "first_name": member.first_name,
                "last_name": member.last_name,
                "full_name": member.full_name,
                "email": member.email,
                "phone": member.phone,
                "website": member.website,
                "district": member.district,
                "role": member.role,
                "party": member.party.name if member.party else None,
                "jurisdiction": member.jurisdiction.name if member.jurisdiction else None,
                "start_date": member.start_date.isoformat() if member.start_date else None,
                "end_date": member.end_date.isoformat() if member.end_date else None
            }
            
            if export_request.include_contacts:
                member_dict["contacts"] = [
                    {
                        "type": c.contact_type,
                        "address": f"{c.address_line1} {c.address_line2}".strip(),
                        "city": c.city,
                        "province": c.province,
                        "postal_code": c.postal_code,
                        "phone": c.phone,
                        "email": c.email
                    }
                    for c in member.contacts
                ]
            
            if export_request.include_social_media:
                member_dict["social_media"] = [
                    {
                        "platform": s.platform,
                        "handle": s.handle,
                        "url": s.url,
                        "verified": s.verified
                    }
                    for s in member.social_media
                ]
            
            data.append(member_dict)
        
        return json.dumps(data, indent=2).encode('utf-8')
    
    def _export_csv(
        self,
        members: List[Member],
        export_request: MemberExportRequest
    ) -> bytes:
        """Export members as CSV."""
        output = io.StringIO()
        
        # Define fields
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
            'website', 'district', 'role', 'party', 'jurisdiction',
            'start_date', 'end_date'
        ]
        
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        
        for member in members:
            row = {
                'id': str(member.id),
                'first_name': member.first_name,
                'last_name': member.last_name,
                'full_name': member.full_name,
                'email': member.email or '',
                'phone': member.phone or '',
                'website': member.website or '',
                'district': member.district or '',
                'role': member.role or '',
                'party': member.party.name if member.party else '',
                'jurisdiction': member.jurisdiction.name if member.jurisdiction else '',
                'start_date': member.start_date.isoformat() if member.start_date else '',
                'end_date': member.end_date.isoformat() if member.end_date else ''
            }
            writer.writerow(row)
        
        return output.getvalue().encode('utf-8')


# Dependency injection helper
def get_member_management_service(db: Session) -> MemberManagementService:
    """Get member management service instance."""
    return MemberManagementService(db)