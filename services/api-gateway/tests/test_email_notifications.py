"""
Tests for email notification system.

Tests FEAT-007 Email Notifications (P2 priority).
"""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy.orm import Session
from app.core.email_notifications import EmailNotificationService
from app.models.email_notifications import (
    EmailTemplate, NotificationPreference, EmailNotification,
    EmailBatch, EmailDomain, NotificationType, EmailStatus, EmailProvider
)
from app.models.users import User
from app.schemas.email_notifications import (
    EmailTemplateCreate, NotificationPreferenceUpdate,
    SendEmailRequest, SendBulkEmailRequest,
    PreviewEmailRequest, TypePreference, DigestFrequency
)


class TestEmailNotificationService:
    """Test email notification service functionality."""
    
    @pytest.fixture
    def service(self, db_session):
        """Create service instance."""
        return EmailNotificationService(db_session)
    
    @pytest.fixture
    def test_user(self, db_session):
        """Create test user."""
        user = User(
            email="emailtest@example.com",
            username="emailuser",
            full_name="Email Test User",
            hashed_password="hashed"
        )
        db_session.add(user)
        db_session.commit()
        return user
    
    @pytest.fixture
    def test_domain(self, db_session):
        """Create test email domain."""
        domain = EmailDomain(
            domain="test.com",
            from_name="Test System",
            from_email="noreply@test.com",
            provider=EmailProvider.SMTP,
            provider_config={
                "host": "smtp.test.com",
                "port": 587,
                "username": "test",
                "password": "test"
            },
            is_default=True,
            daily_limit=100
        )
        db_session.add(domain)
        db_session.commit()
        return domain
    
    @pytest.fixture
    def test_template(self, db_session):
        """Create test email template."""
        template = EmailTemplate(
            name="Test Notification",
            slug="test-notification",
            notification_type=NotificationType.CUSTOM_ALERT,
            subject_template="Test: {{ title }}",
            html_template="<p>Hello {{ user_name }}, {{ message }}</p>",
            text_template="Hello {{ user_name }}, {{ message }}",
            is_active=True,
            is_system=True
        )
        db_session.add(template)
        db_session.commit()
        return template
    
    def test_create_template(self, service):
        """Test creating email template."""
        template_data = EmailTemplateCreate(
            name="Bill Update Alert",
            notification_type=NotificationType.BILL_UPDATE,
            subject_template="Bill {{ bill_number }} Updated",
            html_template="<p>Bill {{ bill_number }} has been updated.</p>",
            text_template="Bill {{ bill_number }} has been updated.",
            description="Alert for bill updates",
            variables={"bill_number": "string", "bill_title": "string"}
        )
        
        template = service.create_template(template_data)
        
        assert template.name == "Bill Update Alert"
        assert template.slug == "bill-update-alert"
        assert template.notification_type == NotificationType.BILL_UPDATE
    
    def test_get_or_create_preferences(self, service, test_user):
        """Test getting or creating notification preferences."""
        # First call creates
        prefs1 = service.get_or_create_preferences(test_user.id)
        assert prefs1.user_id == test_user.id
        assert prefs1.email_enabled is True
        assert prefs1.unsubscribe_token is not None
        
        # Second call gets existing
        prefs2 = service.get_or_create_preferences(test_user.id)
        assert prefs2.id == prefs1.id
    
    def test_update_preferences(self, service, test_user):
        """Test updating notification preferences."""
        prefs = service.get_or_create_preferences(test_user.id)
        
        # Update preferences
        update_data = NotificationPreferenceUpdate(
            digest_frequency=DigestFrequency.DAILY,
            type_preferences={
                NotificationType.BILL_UPDATE: TypePreference(
                    enabled=False,
                    frequency=DigestFrequency.NEVER
                ),
                NotificationType.VOTE_RESULT: TypePreference(
                    enabled=True,
                    frequency=DigestFrequency.IMMEDIATE
                )
            },
            quiet_hours_start=22,
            quiet_hours_end=8
        )
        
        updated_prefs = service.update_preferences(test_user.id, update_data)
        
        assert updated_prefs.digest_frequency == "daily"
        assert updated_prefs.type_preferences["bill_update"]["enabled"] is False
        assert updated_prefs.type_preferences["vote_result"]["enabled"] is True
        assert updated_prefs.quiet_hours_start == 22
        assert updated_prefs.quiet_hours_end == 8
    
    @pytest.mark.asyncio
    async def test_send_email(self, service, test_user, test_template, test_domain):
        """Test sending single email."""
        request = SendEmailRequest(
            user_id=test_user.id,
            notification_type=NotificationType.CUSTOM_ALERT,
            template_id=test_template.id,
            template_variables={
                "title": "Test Alert",
                "message": "This is a test message"
            },
            send_immediately=False  # Don't actually send in test
        )
        
        notification = await service.send_email(request)
        
        assert notification.user_id == test_user.id
        assert notification.subject == "Test: Test Alert"
        assert "Hello Email Test User, This is a test message" in notification.text_content
        assert notification.status == EmailStatus.PENDING
    
    @pytest.mark.asyncio
    async def test_send_bulk_email(self, service, test_user, test_template, test_domain):
        """Test sending bulk emails."""
        # Create additional users
        users = []
        for i in range(3):
            user = User(
                email=f"bulktest{i}@example.com",
                username=f"bulkuser{i}",
                full_name=f"Bulk User {i}",
                hashed_password="hashed"
            )
            service.db.add(user)
            users.append(user)
        service.db.commit()
        
        request = SendBulkEmailRequest(
            notification_type=NotificationType.WEEKLY_DIGEST,
            template_id=test_template.id,
            recipient_filters={"user_ids": [u.id for u in users]},
            template_variables={
                "week_of": "December 18-24, 2024"
            },
            batch_name="Test Weekly Digest"
        )
        
        batch = await service.send_bulk_email(request, test_user)
        
        assert batch.name == "Test Weekly Digest"
        assert batch.total_count == 3
        assert batch.notification_type == NotificationType.WEEKLY_DIGEST
        
        # Check notifications created
        notifications = service.db.query(EmailNotification).filter(
            EmailNotification.batch_id == batch.id
        ).all()
        
        assert len(notifications) == 3
    
    def test_preview_email(self, service, test_template):
        """Test email preview."""
        request = PreviewEmailRequest(
            template_id=test_template.id,
            template_variables={
                "title": "Preview Test",
                "message": "This is a preview"
            }
        )
        
        preview = service.preview_email(request)
        
        assert preview["subject"] == "Test: Preview Test"
        assert "Hello John Doe, This is a preview" in preview["html_content"]
        assert preview["from_email"] == "noreply@test.com"
        assert preview["from_name"] == "Test System"
    
    def test_render_template(self, service, test_template, test_user):
        """Test template rendering."""
        prefs = service.get_or_create_preferences(test_user.id)
        
        variables = {
            "title": "Render Test",
            "message": "Testing template rendering"
        }
        
        subject, html, text = service._render_template(
            test_template,
            variables,
            test_user,
            prefs
        )
        
        assert subject == "Test: Render Test"
        assert "Hello Email Test User, Testing template rendering" in html
        assert f"/unsubscribe?token={prefs.unsubscribe_token}" in html
        assert "Unsubscribe" in text
    
    def test_check_rate_limit(self, service, test_domain):
        """Test rate limit checking."""
        # Initially should allow
        assert service._check_rate_limit(test_domain) is True
        
        # Simulate reaching daily limit
        test_domain.emails_sent_today = 100
        assert service._check_rate_limit(test_domain) is False
        
        # Reset for new day
        test_domain.last_reset_date = None
        assert service._check_rate_limit(test_domain) is True
        assert test_domain.emails_sent_today == 0


class TestEmailNotificationEndpoints:
    """Test email notification API endpoints."""
    
    def test_create_template(self, client, admin_headers):
        """Test creating email template."""
        response = client.post(
            "/api/v1/email-notifications/templates",
            json={
                "name": "New Bill Alert",
                "notification_type": "bill_update",
                "subject_template": "New Bill: {{ bill_title }}",
                "html_template": "<p>A new bill has been introduced.</p>",
                "text_template": "A new bill has been introduced.",
                "language": "en"
            },
            headers=admin_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "New Bill Alert"
        assert data["slug"] == "new-bill-alert"
    
    def test_get_preferences(self, client, auth_headers):
        """Test getting notification preferences."""
        response = client.get(
            "/api/v1/email-notifications/preferences",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email_enabled"] is True
        assert "unsubscribe_token" in data
    
    def test_update_preferences(self, client, auth_headers):
        """Test updating notification preferences."""
        response = client.put(
            "/api/v1/email-notifications/preferences",
            json={
                "email_enabled": True,
                "digest_frequency": "daily",
                "type_preferences": {
                    "bill_update": {
                        "enabled": True,
                        "frequency": "immediate"
                    }
                },
                "timezone": "America/Toronto"
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["digest_frequency"] == "daily"
        assert data["timezone"] == "America/Toronto"
    
    def test_send_email(self, client, auth_headers, db_session):
        """Test sending email notification."""
        # Create template
        template = EmailTemplate(
            id=uuid4(),
            name="Test Template",
            slug="test-template",
            notification_type=NotificationType.CUSTOM_ALERT,
            subject_template="Test Subject",
            html_template="<p>Test HTML</p>",
            text_template="Test Text",
            is_active=True
        )
        db_session.add(template)
        
        # Create domain
        domain = EmailDomain(
            domain="test.com",
            from_name="Test",
            from_email="test@test.com",
            provider=EmailProvider.SMTP,
            provider_config={},
            is_default=True
        )
        db_session.add(domain)
        db_session.commit()
        
        # Get user
        user = db_session.query(User).filter(User.email == "test@example.com").first()
        
        response = client.post(
            "/api/v1/email-notifications/send",
            json={
                "user_id": str(user.id),
                "notification_type": "custom_alert",
                "template_id": str(template.id),
                "template_variables": {
                    "message": "Test message"
                },
                "send_immediately": False
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "pending"
        assert data["subject"] == "Test Subject"
    
    def test_preview_email(self, client, auth_headers, db_session):
        """Test email preview."""
        # Create template
        template = EmailTemplate(
            id=uuid4(),
            name="Preview Template",
            slug="preview-template",
            notification_type=NotificationType.CUSTOM_ALERT,
            subject_template="Preview: {{ title }}",
            html_template="<p>Hello {{ user_name }}, preview message</p>",
            text_template="Hello {{ user_name }}, preview message",
            is_active=True
        )
        db_session.add(template)
        
        # Create domain
        domain = EmailDomain(
            domain="test.com",
            from_name="Test",
            from_email="test@test.com",
            provider=EmailProvider.SMTP,
            provider_config={},
            is_default=True
        )
        db_session.add(domain)
        db_session.commit()
        
        response = client.post(
            "/api/v1/email-notifications/preview",
            json={
                "template_id": str(template.id),
                "template_variables": {
                    "title": "Test Preview"
                }
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["subject"] == "Preview: Test Preview"
        assert "Hello John Doe, preview message" in data["html_content"]
    
    def test_list_notifications(self, client, auth_headers):
        """Test listing notifications."""
        response = client.get(
            "/api/v1/email-notifications/notifications",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "pagination" in data
    
    def test_email_statistics(self, client, admin_headers):
        """Test getting email statistics."""
        response = client.get(
            "/api/v1/email-notifications/statistics",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "total_sent" in data
        assert "delivery_rate" in data
        assert "open_rate" in data
    
    def test_unsubscribe(self, client, db_session):
        """Test unsubscribe functionality."""
        # Create user with preferences
        user = User(
            email="unsub@example.com",
            username="unsubuser",
            full_name="Unsub User",
            hashed_password="hashed"
        )
        db_session.add(user)
        db_session.flush()
        
        prefs = NotificationPreference(
            user_id=user.id,
            unsubscribe_token="test-unsub-token",
            email_enabled=True,
            type_preferences={}
        )
        db_session.add(prefs)
        db_session.commit()
        
        # Test unsubscribe
        response = client.post(
            "/api/v1/email-notifications/unsubscribe",
            json={
                "token": "test-unsub-token",
                "notification_types": ["bill_update", "vote_result"]
            }
        )
        
        assert response.status_code == 204
        
        # Check preferences updated
        db_session.refresh(prefs)
        assert prefs.type_preferences["bill_update"]["enabled"] is False
        assert prefs.type_preferences["vote_result"]["enabled"] is False