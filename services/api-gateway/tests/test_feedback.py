"""
Tests for feedback collection system.

Tests FEAT-003 Feedback Collection (P1 priority).
"""

import pytest
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import Session
from app.core.feedback import FeedbackService
from app.models.feedback import (
    Feedback, FeedbackAttachment, FeedbackResponse,
    FeedbackVote, FeedbackTemplate,
    FeedbackType, FeedbackStatus, FeedbackPriority, FeedbackCategory
)
from app.models.users import User
from app.schemas.feedback import (
    FeedbackCreate, FeedbackUpdate, FeedbackAssign,
    FeedbackFilter, AttachmentCreate, ResponseCreate,
    VoteCreate, TemplateCreate
)


class TestFeedbackService:
    """Test feedback service functionality."""
    
    @pytest.fixture
    def service(self, db_session):
        """Create service instance."""
        return FeedbackService(db_session)
    
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
    def admin_user(self, db_session):
        """Create admin user."""
        user = User(
            email="admin@example.com",
            username="admin",
            full_name="Admin User",
            hashed_password="hashed",
            is_admin=True
        )
        db_session.add(user)
        db_session.commit()
        return user
    
    @pytest.fixture
    def test_feedback(self, db_session, test_user):
        """Create test feedback."""
        feedback = Feedback(
            user_id=test_user.id,
            type=FeedbackType.BUG_REPORT,
            category=FeedbackCategory.FUNCTIONALITY,
            subject="Test bug report",
            description="This is a test bug report with detailed description",
            priority=FeedbackPriority.MEDIUM,
            status=FeedbackStatus.PENDING
        )
        db_session.add(feedback)
        db_session.commit()
        return feedback
    
    def test_create_feedback_authenticated(self, service, test_user):
        """Test creating feedback as authenticated user."""
        feedback_data = FeedbackCreate(
            type=FeedbackType.FEATURE_REQUEST,
            category=FeedbackCategory.UI_UX,
            subject="Add dark mode",
            description="Please add a dark mode option to the interface",
            page_url="/settings",
            tags=["ui", "accessibility"]
        )
        
        feedback = service.create_feedback(feedback_data, test_user)
        
        assert feedback.user_id == test_user.id
        assert feedback.user_email == test_user.email
        assert feedback.type == FeedbackType.FEATURE_REQUEST
        assert feedback.subject == "Add dark mode"
        assert feedback.tags == ["ui", "accessibility"]
    
    def test_create_feedback_anonymous(self, service):
        """Test creating feedback as anonymous user."""
        feedback_data = FeedbackCreate(
            type=FeedbackType.GENERAL_FEEDBACK,
            category=FeedbackCategory.OTHER,
            subject="Great platform!",
            description="I really enjoy using this platform for tracking bills",
            user_email="anonymous@example.com",
            user_name="Anonymous User"
        )
        
        feedback = service.create_feedback(feedback_data, None)
        
        assert feedback.user_id is None
        assert feedback.user_email == "anonymous@example.com"
        assert feedback.user_name == "Anonymous User"
    
    def test_update_feedback(self, service, test_feedback, test_user):
        """Test updating feedback."""
        update_data = FeedbackUpdate(
            priority=FeedbackPriority.HIGH,
            status=FeedbackStatus.IN_REVIEW,
            tags=["urgent", "bug"]
        )
        
        updated = service.update_feedback(
            test_feedback.id,
            update_data,
            test_user
        )
        
        assert updated.priority == FeedbackPriority.HIGH
        assert updated.status == FeedbackStatus.IN_REVIEW
        assert updated.tags == ["urgent", "bug"]
    
    def test_feedback_status_transition(self, service, test_feedback, test_user):
        """Test feedback status transitions."""
        # Resolve feedback
        update_data = FeedbackUpdate(
            status=FeedbackStatus.RESOLVED,
            resolution_notes="Fixed in version 2.1.0"
        )
        
        updated = service.update_feedback(
            test_feedback.id,
            update_data,
            test_user
        )
        
        assert updated.status == FeedbackStatus.RESOLVED
        assert updated.resolved_at is not None
        assert updated.resolution_notes == "Fixed in version 2.1.0"
    
    def test_search_feedback(self, service, test_feedback):
        """Test searching feedback."""
        # Create additional feedback
        feedback2 = Feedback(
            type=FeedbackType.FEATURE_REQUEST,
            category=FeedbackCategory.UI_UX,
            subject="Another feedback",
            description="Another test feedback",
            priority=FeedbackPriority.LOW,
            status=FeedbackStatus.PENDING
        )
        service.db.add(feedback2)
        service.db.commit()
        
        # Search by type
        filter_params = FeedbackFilter(
            type=FeedbackType.BUG_REPORT,
            page=1,
            page_size=10
        )
        
        results, total = service.search_feedback(filter_params)
        
        assert total == 1
        assert len(results) == 1
        assert results[0].id == test_feedback.id
        
        # Search with text
        filter_params = FeedbackFilter(
            search="bug",
            page=1,
            page_size=10
        )
        
        results, total = service.search_feedback(filter_params)
        assert total == 1
    
    def test_assign_feedback(self, service, test_feedback, admin_user):
        """Test assigning feedback."""
        assign_data = FeedbackAssign(
            assignee_id=admin_user.id,
            priority=FeedbackPriority.HIGH,
            notes="Assigning to admin for review"
        )
        
        assigned = service.assign_feedback(
            test_feedback.id,
            assign_data,
            admin_user
        )
        
        assert assigned.assigned_to == admin_user.id
        assert assigned.priority == FeedbackPriority.HIGH
        assert assigned.status == FeedbackStatus.IN_REVIEW
    
    def test_add_response(self, service, test_feedback, admin_user):
        """Test adding response to feedback."""
        response_data = ResponseCreate(
            message="Thank you for your feedback. We are looking into this issue.",
            is_internal=False
        )
        
        response = service.add_response(
            test_feedback.id,
            response_data,
            admin_user
        )
        
        assert response.feedback_id == test_feedback.id
        assert response.user_id == admin_user.id
        assert response.message == "Thank you for your feedback. We are looking into this issue."
        assert response.is_internal is False
        
        # Check feedback status updated
        service.db.refresh(test_feedback)
        assert test_feedback.status == FeedbackStatus.IN_REVIEW
    
    def test_vote_feedback(self, service, test_feedback, test_user, admin_user):
        """Test voting on feedback."""
        # User upvotes
        vote_data = VoteCreate(vote_type=1)
        vote_stats = service.vote_feedback(
            test_feedback.id,
            vote_data,
            test_user
        )
        
        assert vote_stats['total_score'] == 1
        assert vote_stats['upvotes'] == 1
        assert vote_stats['downvotes'] == 0
        assert vote_stats['user_vote'] == 1
        
        # Admin downvotes
        vote_data = VoteCreate(vote_type=-1)
        vote_stats = service.vote_feedback(
            test_feedback.id,
            vote_data,
            admin_user
        )
        
        assert vote_stats['total_score'] == 0  # 1 upvote - 1 downvote
        assert vote_stats['upvotes'] == 1
        assert vote_stats['downvotes'] == 1
        
        # User toggles vote (removes it)
        vote_data = VoteCreate(vote_type=1)
        vote_stats = service.vote_feedback(
            test_feedback.id,
            vote_data,
            test_user
        )
        
        assert vote_stats['total_score'] == -1  # Only admin's downvote remains
        assert vote_stats['user_vote'] is None
    
    def test_add_attachment(self, service, test_feedback, test_user):
        """Test adding attachment to feedback."""
        attachment_data = AttachmentCreate(
            filename="screenshot.png",
            file_type="image/png",
            file_size=102400,  # 100KB
            file_url="https://example.com/uploads/screenshot.png",
            description="Screenshot of the bug"
        )
        
        attachment = service.add_attachment(
            test_feedback.id,
            attachment_data,
            test_user
        )
        
        assert attachment.feedback_id == test_feedback.id
        assert attachment.filename == "screenshot.png"
        assert attachment.uploaded_by == test_user.id
    
    def test_create_template(self, service):
        """Test creating feedback template."""
        template_data = TemplateCreate(
            name="Performance Issue Form",
            type=FeedbackType.BUG_REPORT,
            category=FeedbackCategory.PERFORMANCE,
            fields={
                "page_affected": {
                    "type": "text",
                    "label": "Which page is slow?",
                    "required": True
                },
                "load_time": {
                    "type": "number",
                    "label": "Approximate load time (seconds)",
                    "required": True
                }
            },
            requires_auth=False
        )
        
        template = service.create_template(template_data)
        
        assert template.name == "Performance Issue Form"
        assert template.type == FeedbackType.BUG_REPORT
        assert "page_affected" in template.fields
    
    def test_feedback_stats(self, service, test_feedback):
        """Test feedback statistics."""
        # Create more feedback
        for i in range(3):
            feedback = Feedback(
                type=FeedbackType.FEATURE_REQUEST,
                category=FeedbackCategory.UI_UX,
                subject=f"Feature request {i}",
                description="Test description",
                priority=FeedbackPriority.LOW,
                status=FeedbackStatus.PENDING
            )
            service.db.add(feedback)
        
        # Resolve one
        resolved = Feedback(
            type=FeedbackType.BUG_REPORT,
            category=FeedbackCategory.FUNCTIONALITY,
            subject="Resolved bug",
            description="This bug was resolved",
            priority=FeedbackPriority.HIGH,
            status=FeedbackStatus.RESOLVED,
            resolved_at=datetime.utcnow()
        )
        service.db.add(resolved)
        service.db.commit()
        
        stats = service.get_feedback_stats()
        
        assert stats.total_count == 5  # 1 test + 3 new + 1 resolved
        assert stats.by_type[FeedbackType.FEATURE_REQUEST] == 3
        assert stats.by_type[FeedbackType.BUG_REPORT] == 2
        assert stats.pending_count == 4
        assert stats.resolved_count == 1
    
    def test_feedback_trends(self, service):
        """Test feedback trends."""
        # Create feedback over time
        from datetime import timedelta
        
        base_date = datetime.utcnow()
        
        for i in range(5):
            feedback = Feedback(
                type=FeedbackType.GENERAL_FEEDBACK,
                category=FeedbackCategory.OTHER,
                subject=f"Feedback {i}",
                description="Test feedback",
                created_at=base_date - timedelta(days=i)
            )
            service.db.add(feedback)
        
        service.db.commit()
        
        trends = service.get_feedback_trends(period="daily", days=7)
        
        assert trends.period == "daily"
        assert len(trends.data) > 0
        
        # Check that data contains expected fields
        if trends.data:
            first_entry = trends.data[0]
            assert 'period' in first_entry
            assert 'total' in first_entry
            assert 'by_type' in first_entry
            assert 'by_status' in first_entry


class TestFeedbackEndpoints:
    """Test feedback API endpoints."""
    
    def test_submit_feedback_anonymous(self, client):
        """Test submitting feedback anonymously."""
        response = client.post(
            "/api/v1/feedback/",
            json={
                "type": "general_feedback",
                "category": "other",
                "subject": "Great work!",
                "description": "I love this platform, keep up the good work!",
                "user_email": "fan@example.com"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["subject"] == "Great work!"
        assert data["user_email"] == "fan@example.com"
    
    def test_submit_feedback_authenticated(self, client, auth_headers):
        """Test submitting feedback as authenticated user."""
        response = client.post(
            "/api/v1/feedback/",
            json={
                "type": "bug_report",
                "category": "functionality",
                "subject": "Login button not working",
                "description": "The login button on the homepage is not responding to clicks",
                "page_url": "/",
                "tags": ["bug", "login", "urgent"]
            },
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["subject"] == "Login button not working"
        assert data["user_id"] is not None
    
    def test_get_my_feedback(self, client, auth_headers, db_session):
        """Test getting user's own feedback."""
        # Create some feedback first
        response = client.post(
            "/api/v1/feedback/",
            json={
                "type": "feature_request",
                "category": "ui_ux",
                "subject": "Dark mode",
                "description": "Please add dark mode support"
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        
        # Get my feedback
        response = client.get(
            "/api/v1/feedback/my-feedback",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) > 0
        assert data["results"][0]["subject"] == "Dark mode"
    
    def test_vote_on_feedback(self, client, auth_headers):
        """Test voting on feedback."""
        # Create feedback
        response = client.post(
            "/api/v1/feedback/",
            json={
                "type": "suggestion",
                "category": "other",
                "subject": "Add more filters",
                "description": "It would be nice to have more filter options"
            }
        )
        assert response.status_code == 201
        feedback_id = response.json()["id"]
        
        # Vote on it
        response = client.post(
            f"/api/v1/feedback/{feedback_id}/vote",
            json={"vote_type": 1},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_score"] == 1
        assert data["user_vote"] == 1
    
    def test_get_feedback_templates(self, client):
        """Test getting feedback templates."""
        response = client.get("/api/v1/feedback/templates")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Should have default templates from migration
        assert len(data) > 0