"""
Tests for member management system.

Tests FEAT-015 Member Management (P0 priority).
"""

import pytest
from datetime import datetime, date
from uuid import uuid4
from sqlalchemy.orm import Session
from app.core.member_management import MemberManagementService
from app.models.openparliament import Member, Party, Jurisdiction
from app.models.member_management import (
    MemberAudit, MemberImport, MemberContact, MemberSocialMedia,
    MemberEducation, MemberProfession, MemberTag, MemberMetrics
)
from app.models.users import User
from app.schemas.member_management import (
    MemberCreate, MemberUpdate, MemberSearchRequest,
    ContactCreate, SocialMediaCreate, BulkMemberImport,
    BulkOperationRequest, MemberDuplicateCheck, MemberMergeRequest,
    MemberExportRequest, MemberMetricsUpdate
)


class TestMemberManagementService:
    """Test member management service functionality."""
    
    @pytest.fixture
    def service(self, db_session):
        """Create service instance."""
        return MemberManagementService(db_session)
    
    @pytest.fixture
    def test_user(self, db_session):
        """Create test user."""
        user = User(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            hashed_password="hashed"
        )
        db_session.add(user)
        db_session.commit()
        return user
    
    @pytest.fixture
    def test_jurisdiction(self, db_session):
        """Create test jurisdiction."""
        jurisdiction = Jurisdiction(
            id=uuid4(),
            name="Federal",
            level="federal",
            country="Canada"
        )
        db_session.add(jurisdiction)
        db_session.commit()
        return jurisdiction
    
    @pytest.fixture
    def test_party(self, db_session):
        """Create test party."""
        party = Party(
            id=uuid4(),
            name="Test Party",
            short_name="TP",
            color="#FF0000"
        )
        db_session.add(party)
        db_session.commit()
        return party
    
    @pytest.fixture
    def test_member(self, db_session, test_jurisdiction, test_party):
        """Create test member."""
        member = Member(
            id=uuid4(),
            first_name="John",
            last_name="Doe",
            full_name="John Doe",
            email="john.doe@parliament.ca",
            phone="613-555-0100",
            district="Test District",
            jurisdiction_id=test_jurisdiction.id,
            party_id=test_party.id,
            start_date=date(2020, 1, 1)
        )
        db_session.add(member)
        db_session.commit()
        return member
    
    def test_create_member_success(self, service, test_user, test_jurisdiction):
        """Test successful member creation."""
        member_data = MemberCreate(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@parliament.ca",
            district="New District",
            jurisdiction_id=test_jurisdiction.id,
            start_date=date.today()
        )
        
        member = service.create_member(member_data, test_user)
        
        assert member.first_name == "Jane"
        assert member.last_name == "Smith"
        assert member.full_name == "Jane Smith"
        assert member.email == "jane.smith@parliament.ca"
        
        # Check audit log created
        audit = service.db.query(MemberAudit).filter(
            MemberAudit.member_id == member.id
        ).first()
        assert audit is not None
        assert audit.action == "create"
        assert audit.user_id == test_user.id
    
    def test_create_member_duplicate(self, service, test_user, test_member):
        """Test duplicate member detection."""
        member_data = MemberCreate(
            first_name=test_member.first_name,
            last_name=test_member.last_name,
            email=test_member.email,
            district=test_member.district,
            jurisdiction_id=test_member.jurisdiction_id,
            start_date=date.today()
        )
        
        with pytest.raises(Exception) as exc_info:
            service.create_member(member_data, test_user)
        
        assert "duplicate" in str(exc_info.value).lower()
    
    def test_update_member_success(self, service, test_user, test_member):
        """Test successful member update."""
        update_data = MemberUpdate(
            email="new.email@parliament.ca",
            phone="613-555-0200"
        )
        
        updated = service.update_member(
            test_member.id,
            update_data,
            test_user,
            reason="Contact info update"
        )
        
        assert updated.email == "new.email@parliament.ca"
        assert updated.phone == "613-555-0200"
        
        # Check audit log
        audit = service.db.query(MemberAudit).filter(
            MemberAudit.member_id == test_member.id,
            MemberAudit.action == "update"
        ).first()
        assert audit is not None
        assert audit.reason == "Contact info update"
    
    def test_delete_member(self, service, test_user, test_member):
        """Test member deletion (soft delete)."""
        service.delete_member(test_member.id, test_user, "No longer serving")
        
        # Should set end date
        assert test_member.end_date is not None
        assert test_member.end_date == date.today()
        
        # Check audit log
        audit = service.db.query(MemberAudit).filter(
            MemberAudit.member_id == test_member.id,
            MemberAudit.action == "delete"
        ).first()
        assert audit is not None
        assert audit.reason == "No longer serving"
    
    def test_search_members(self, service, test_member):
        """Test member search functionality."""
        # Add another member
        member2 = Member(
            id=uuid4(),
            first_name="Jane",
            last_name="Smith",
            full_name="Jane Smith",
            district="Another District",
            jurisdiction_id=test_member.jurisdiction_id,
            start_date=date(2021, 1, 1)
        )
        service.db.add(member2)
        service.db.commit()
        
        # Search by name
        search_request = MemberSearchRequest(
            query="John",
            page=1,
            page_size=10
        )
        
        members, total = service.search_members(search_request)
        
        assert total == 1
        assert len(members) == 1
        assert members[0].id == test_member.id
        
        # Search current members only
        search_request = MemberSearchRequest(
            is_current=True,
            page=1,
            page_size=10
        )
        
        members, total = service.search_members(search_request)
        assert total == 2  # Both have no end date
    
    def test_bulk_import_csv(self, service, test_user, test_jurisdiction):
        """Test CSV bulk import."""
        csv_data = """first_name,last_name,email,district,jurisdiction_id,start_date
Alice,Johnson,alice@parliament.ca,District A,{},2022-01-01
Bob,Wilson,bob@parliament.ca,District B,{},2022-01-01""".format(
            test_jurisdiction.id,
            test_jurisdiction.id
        )
        
        import_data = BulkMemberImport(
            import_source="csv",
            import_type="incremental",
            csv_data=csv_data,
            update_existing=True,
            dry_run=False
        )
        
        import_record = service.bulk_import_members(import_data, test_user)
        
        assert import_record.status == "completed"
        assert import_record.total_records == 2
        assert import_record.created_count == 2
        assert import_record.error_count == 0
        
        # Verify members created
        alice = service.db.query(Member).filter(
            Member.last_name == "Johnson"
        ).first()
        assert alice is not None
        assert alice.first_name == "Alice"
    
    def test_bulk_operation_tag(self, service, test_user, test_member, db_session):
        """Test bulk tagging operation."""
        # Create tags
        tag1 = MemberTag(name="Environment", category="topic")
        tag2 = MemberTag(name="Healthcare", category="topic")
        db_session.add_all([tag1, tag2])
        db_session.commit()
        
        operation_request = BulkOperationRequest(
            member_ids=[test_member.id],
            operation="tag",
            parameters={"tag_ids": [tag1.id, tag2.id]}
        )
        
        result = service.bulk_operation(operation_request, test_user)
        
        assert result["success_count"] == 1
        assert result["error_count"] == 0
        
        # Verify tags added
        service.db.refresh(test_member)
        assert len(test_member.tags) == 2
    
    def test_check_duplicates(self, service, test_member):
        """Test duplicate checking."""
        check_data = MemberDuplicateCheck(
            first_name=test_member.first_name,
            last_name=test_member.last_name,
            jurisdiction_id=test_member.jurisdiction_id
        )
        
        duplicates = service.check_duplicates(check_data)
        
        assert len(duplicates) == 1
        assert duplicates[0]["id"] == str(test_member.id)
        assert duplicates[0]["full_name"] == test_member.full_name
    
    def test_merge_members(self, service, test_user, test_member, test_jurisdiction):
        """Test member merging."""
        # Create duplicate member
        duplicate = Member(
            id=uuid4(),
            first_name=test_member.first_name,
            last_name=test_member.last_name,
            full_name=test_member.full_name,
            district="Duplicate District",
            jurisdiction_id=test_jurisdiction.id,
            start_date=date(2021, 1, 1)
        )
        service.db.add(duplicate)
        
        # Add contact to duplicate
        contact = MemberContact(
            member_id=duplicate.id,
            contact_type="office",
            phone="613-555-9999"
        )
        service.db.add(contact)
        service.db.commit()
        
        merge_request = MemberMergeRequest(
            primary_member_id=test_member.id,
            duplicate_member_ids=[duplicate.id],
            merge_contacts=True,
            reason="Duplicate entry"
        )
        
        result = service.merge_members(merge_request, test_user)
        
        assert result.id == test_member.id
        
        # Verify duplicate deleted
        dup_check = service.db.query(Member).filter(
            Member.id == duplicate.id
        ).first()
        assert dup_check is None
        
        # Verify contact transferred
        service.db.refresh(test_member)
        assert len(test_member.contacts) == 1
        assert test_member.contacts[0].phone == "613-555-9999"
    
    def test_export_members_json(self, service, test_member):
        """Test JSON export."""
        export_request = MemberExportRequest(
            format="json",
            include_contacts=True,
            include_social_media=True
        )
        
        export_data = service.export_members(export_request, [test_member.id])
        
        import json
        data = json.loads(export_data.decode('utf-8'))
        
        assert len(data) == 1
        assert data[0]["id"] == str(test_member.id)
        assert data[0]["full_name"] == test_member.full_name
    
    def test_export_members_csv(self, service, test_member):
        """Test CSV export."""
        export_request = MemberExportRequest(format="csv")
        
        export_data = service.export_members(export_request, [test_member.id])
        
        import csv
        import io
        reader = csv.DictReader(io.StringIO(export_data.decode('utf-8')))
        rows = list(reader)
        
        assert len(rows) == 1
        assert rows[0]["id"] == str(test_member.id)
        assert rows[0]["full_name"] == test_member.full_name
    
    def test_update_member_metrics(self, service, test_member):
        """Test member metrics update."""
        metrics_data = MemberMetricsUpdate(
            bills_sponsored=5,
            votes_total=100,
            votes_yea=60,
            votes_nay=30,
            votes_abstain=10,
            attendance_rate=85.5,
            speeches_count=15,
            questions_asked=8
        )
        
        metrics = service.update_member_metrics(test_member.id, metrics_data)
        
        assert metrics.bills_sponsored == 5
        assert metrics.votes_total == 100
        assert metrics.attendance_rate == 85.5
        assert metrics.activity_score > 0  # Should be calculated
        assert metrics.influence_score >= 0  # Should be calculated
    
    def test_member_contacts(self, service, test_member, db_session):
        """Test member contact management."""
        # Add contacts
        contact1 = MemberContact(
            member_id=test_member.id,
            contact_type="office",
            address_line1="123 Parliament St",
            city="Ottawa",
            province="ON",
            postal_code="K1A 0A1",
            phone="613-555-0001",
            is_primary=True
        )
        contact2 = MemberContact(
            member_id=test_member.id,
            contact_type="constituency",
            address_line1="456 Main St",
            city="Toronto",
            province="ON",
            postal_code="M1A 1A1",
            phone="416-555-0001"
        )
        db_session.add_all([contact1, contact2])
        db_session.commit()
        
        # Verify contacts
        db_session.refresh(test_member)
        assert len(test_member.contacts) == 2
        
        primary = [c for c in test_member.contacts if c.is_primary][0]
        assert primary.contact_type == "office"
        assert primary.city == "Ottawa"
    
    def test_member_social_media(self, service, test_member, db_session):
        """Test member social media management."""
        # Add social media
        twitter = MemberSocialMedia(
            member_id=test_member.id,
            platform="twitter",
            handle="johndoe_mp",
            url="https://twitter.com/johndoe_mp",
            verified=True,
            follower_count=5000
        )
        facebook = MemberSocialMedia(
            member_id=test_member.id,
            platform="facebook",
            handle="johndoemp",
            url="https://facebook.com/johndoemp"
        )
        db_session.add_all([twitter, facebook])
        db_session.commit()
        
        # Verify social media
        db_session.refresh(test_member)
        assert len(test_member.social_media) == 2
        
        twitter_account = [s for s in test_member.social_media if s.platform == "twitter"][0]
        assert twitter_account.verified is True
        assert twitter_account.follower_count == 5000


class TestMemberManagementEndpoints:
    """Test member management API endpoints."""
    
    def test_create_member_endpoint(self, client, auth_headers, db_session):
        """Test member creation endpoint."""
        # Create jurisdiction first
        jurisdiction = Jurisdiction(
            id=uuid4(),
            name="Federal",
            level="federal",
            country="Canada"
        )
        db_session.add(jurisdiction)
        db_session.commit()
        
        response = client.post(
            "/api/v1/member-management/",
            json={
                "first_name": "Test",
                "last_name": "Member",
                "email": "test.member@parliament.ca",
                "district": "Test District",
                "jurisdiction_id": str(jurisdiction.id),
                "start_date": "2023-01-01"
            },
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["full_name"] == "Test Member"
        assert data["email"] == "test.member@parliament.ca"
    
    def test_search_members_endpoint(self, client, auth_headers):
        """Test member search endpoint."""
        response = client.post(
            "/api/v1/member-management/search",
            json={
                "query": "test",
                "page": 1,
                "page_size": 20
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "pagination" in data
    
    def test_export_members_endpoint(self, client, auth_headers):
        """Test member export endpoint."""
        response = client.post(
            "/api/v1/member-management/export",
            json={
                "format": "json",
                "include_contacts": True
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"