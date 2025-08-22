"""
Comprehensive tests for the Email Alert System API

Tests all endpoints and functionality for the email notification system.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json
from unittest.mock import patch, MagicMock

from app.main import app
from app.database import get_db
from app.models.email_alerts import EmailAlert, EmailTemplate, EmailCampaign, EmailLog, UnsubscribeToken
from app.models.users import User
from app.core.auth import create_access_token

client = TestClient(app)


@pytest.fixture
def test_db():
    """Get test database session."""
    return next(get_db())


@pytest.fixture
def test_user(test_db):
    """Create a test user."""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def test_user_token(test_user):
    """Create access token for test user."""
    return create_access_token(data={"sub": test_user.email})


@pytest.fixture
def test_email_template(test_db):
    """Create a test email template."""
    template = EmailTemplate(
        template_name="test_template",
        template_type="bill_update",
        subject_template="Test: {{title}}",
        html_template="<h1>{{title}}</h1><p>{{content}}</p>",
        text_template="{{title}}\n\n{{content}}",
        description="Test template",
        variables={"title": "string", "content": "string"},
        is_active=True
    )
    test_db.add(template)
    test_db.commit()
    test_db.refresh(template)
    return template


@pytest.fixture
def test_email_campaign(test_db):
    """Create a test email campaign."""
    campaign = EmailCampaign(
        campaign_name="Test Campaign",
        campaign_type="newsletter",
        subject="Test Subject",
        html_content="<h1>Test</h1>",
        text_content="Test content",
        target_audience={"user_type": "all"},
        is_active=True
    )
    test_db.add(campaign)
    test_db.commit()
    test_db.refresh(campaign)
    return campaign


class TestEmailAlerts:
    """Test email alert endpoints."""
    
    def test_create_email_alert_success(self, test_db, test_user, test_user_token):
        """Test successful email alert creation."""
        alert_data = {
            "alert_type": "bill_update",
            "frequency": "daily",
            "is_active": True,
            "include_summary": True,
            "include_links": True,
            "include_analytics": False,
            "filters": {"bill_type": "government"}
        }
        
        response = client.post(
            "/api/v1/email/alerts",
            json=alert_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["alert_type"] == "bill_update"
        assert data["frequency"] == "daily"
        assert data["is_active"] == True
        
        # Verify database record
        alert = test_db.query(EmailAlert).filter(
            EmailAlert.user_id == test_user.id
        ).first()
        assert alert is not None
        assert alert.alert_type == "bill_update"
    
    def test_create_email_alert_duplicate(self, test_db, test_user, test_user_token):
        """Test creating duplicate alert type."""
        # Create first alert
        alert1 = EmailAlert(
            user_id=test_user.id,
            alert_type="bill_update",
            frequency="daily",
            is_active=True
        )
        test_db.add(alert1)
        test_db.commit()
        
        # Try to create duplicate
        alert_data = {
            "alert_type": "bill_update",
            "frequency": "weekly",
            "is_active": True
        }
        
        response = client.post(
            "/api/v1/email/alerts",
            json=alert_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 400
        assert "already has an active" in response.json()["detail"]
    
    def test_list_user_alerts(self, test_db, test_user, test_user_token):
        """Test listing user alerts."""
        # Create test alerts
        alert1 = EmailAlert(
            user_id=test_user.id,
            alert_type="bill_update",
            frequency="daily",
            is_active=True
        )
        alert2 = EmailAlert(
            user_id=test_user.id,
            alert_type="vote_reminder",
            frequency="weekly",
            is_active=True
        )
        test_db.add_all([alert1, alert2])
        test_db.commit()
        
        response = client.get(
            "/api/v1/email/alerts",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["alerts"]) == 2
        assert data["alerts"][0]["alert_type"] in ["bill_update", "vote_reminder"]
    
    def test_list_user_alerts_with_filters(self, test_db, test_user, test_user_token):
        """Test listing alerts with filters."""
        # Create test alerts
        alert1 = EmailAlert(
            user_id=test_user.id,
            alert_type="bill_update",
            frequency="daily",
            is_active=True
        )
        alert2 = EmailAlert(
            user_id=test_user.id,
            alert_type="vote_reminder",
            frequency="weekly",
            is_active=False
        )
        test_db.add_all([alert1, alert2])
        test_db.commit()
        
        # Filter by alert type
        response = client.get(
            "/api/v1/email/alerts?alert_type=bill_update",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["alerts"][0]["alert_type"] == "bill_update"
        
        # Filter by active status
        response = client.get(
            "/api/v1/email/alerts?is_active=false",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["alerts"][0]["is_active"] == False
    
    def test_get_email_alert(self, test_db, test_user, test_user_token):
        """Test getting specific email alert."""
        alert = EmailAlert(
            user_id=test_user.id,
            alert_type="bill_update",
            frequency="daily",
            is_active=True
        )
        test_db.add(alert)
        test_db.commit()
        
        response = client.get(
            f"/api/v1/email/alerts/{alert.id}",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(alert.id)
        assert data["alert_type"] == "bill_update"
    
    def test_get_email_alert_not_found(self, test_db, test_user, test_user_token):
        """Test getting non-existent alert."""
        response = client.get(
            "/api/v1/email/alerts/nonexistent-id",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_update_email_alert(self, test_db, test_user, test_user_token):
        """Test updating email alert."""
        alert = EmailAlert(
            user_id=test_user.id,
            alert_type="bill_update",
            frequency="daily",
            is_active=True
        )
        test_db.add(alert)
        test_db.commit()
        
        update_data = {
            "frequency": "weekly",
            "include_analytics": True
        }
        
        response = client.put(
            f"/api/v1/email/alerts/{alert.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["frequency"] == "weekly"
        assert data["include_analytics"] == True
        
        # Verify database update
        test_db.refresh(alert)
        assert alert.frequency == "weekly"
        assert alert.include_analytics == True
    
    def test_delete_email_alert(self, test_db, test_user, test_user_token):
        """Test deleting email alert."""
        alert = EmailAlert(
            user_id=test_user.id,
            alert_type="bill_update",
            frequency="daily",
            is_active=True
        )
        test_db.add(alert)
        test_db.commit()
        
        response = client.delete(
            f"/api/v1/email/alerts/{alert.id}",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
        
        # Verify database deletion
        deleted_alert = test_db.query(EmailAlert).filter(
            EmailAlert.id == alert.id
        ).first()
        assert deleted_alert is None


class TestEmailTemplates:
    """Test email template endpoints."""
    
    def test_list_email_templates(self, test_db, test_user_token, test_email_template):
        """Test listing email templates."""
        response = client.get(
            "/api/v1/email/templates",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert len(data["templates"]) >= 1
        
        # Check if our test template is in the list
        template_names = [t["template_name"] for t in data["templates"]]
        assert "test_template" in template_names
    
    def test_list_email_templates_with_filters(self, test_db, test_user_token, test_email_template):
        """Test listing templates with filters."""
        # Filter by template type
        response = client.get(
            "/api/v1/email/templates?template_type=bill_update",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        
        # All returned templates should be of the specified type
        for template in data["templates"]:
            assert template["template_type"] == "bill_update"
    
    def test_get_email_template(self, test_db, test_user_token, test_email_template):
        """Test getting specific email template."""
        response = client.get(
            f"/api/v1/email/templates/{test_email_template.id}",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_email_template.id)
        assert data["template_name"] == "test_template"
        assert data["template_type"] == "bill_update"
    
    def test_get_email_template_not_found(self, test_db, test_user_token):
        """Test getting non-existent template."""
        response = client.get(
            "/api/v1/email/templates/nonexistent-id",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestEmailCampaigns:
    """Test email campaign endpoints."""
    
    def test_create_email_campaign(self, test_db, test_user, test_user_token):
        """Test creating email campaign."""
        campaign_data = {
            "campaign_name": "Test Newsletter",
            "campaign_type": "newsletter",
            "subject": "Monthly Update",
            "html_content": "<h1>Newsletter</h1>",
            "text_content": "Newsletter content",
            "target_audience": {"user_type": "subscribers"},
            "is_active": True
        }
        
        response = client.post(
            "/api/v1/email/campaigns",
            json=campaign_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["campaign_name"] == "Test Newsletter"
        assert data["campaign_type"] == "newsletter"
        assert data["is_active"] == True
        
        # Verify database record
        campaign = test_db.query(EmailCampaign).filter(
            EmailCampaign.campaign_name == "Test Newsletter"
        ).first()
        assert campaign is not None
    
    def test_list_email_campaigns(self, test_db, test_user_token, test_email_campaign):
        """Test listing email campaigns."""
        response = client.get(
            "/api/v1/email/campaigns",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert len(data["campaigns"]) >= 1
        
        # Check if our test campaign is in the list
        campaign_names = [c["campaign_name"] for c in data["campaigns"]]
        assert "Test Campaign" in campaign_names


class TestEmailAnalytics:
    """Test email analytics endpoints."""
    
    def test_get_email_analytics(self, test_db, test_user, test_user_token):
        """Test getting email analytics."""
        # Create test email logs
        log1 = EmailLog(
            user_id=test_user.id,
            email_type="alert",
            recipient_email=test_user.email,
            subject="Test Email 1",
            status="sent",
            sent_at=datetime.utcnow()
        )
        log2 = EmailLog(
            user_id=test_user.id,
            email_type="alert",
            recipient_email=test_user.email,
            subject="Test Email 2",
            status="opened",
            sent_at=datetime.utcnow(),
            opened_at=datetime.utcnow()
        )
        test_db.add_all([log1, log2])
        test_db.commit()
        
        response = client.get(
            "/api/v1/email/analytics",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_emails_sent"] >= 2
        assert data["total_emails_opened"] >= 1
        assert "delivery_rate" in data
        assert "open_rate" in data
    
    def test_get_email_analytics_with_date_range(self, test_db, test_user, test_user_token):
        """Test getting analytics with date range."""
        response = client.get(
            "/api/v1/email/analytics?date_from=2024-01-01&date_to=2024-12-31",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "total_emails_sent" in data
    
    def test_get_email_analytics_invalid_date_format(self, test_db, test_user, test_user_token):
        """Test analytics with invalid date format."""
        response = client.get(
            "/api/v1/email/analytics?date_from=invalid-date",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 400
        assert "Invalid date format" in response.json()["detail"]
    
    def test_get_user_alert_stats(self, test_db, test_user, test_user_token):
        """Test getting user alert statistics."""
        # Create test alerts and logs
        alert = EmailAlert(
            user_id=test_user.id,
            alert_type="bill_update",
            frequency="daily",
            is_active=True
        )
        test_db.add(alert)
        
        log = EmailLog(
            user_id=test_user.id,
            email_type="alert",
            recipient_email=test_user.email,
            subject="Test Email",
            status="opened",
            sent_at=datetime.utcnow(),
            opened_at=datetime.utcnow()
        )
        test_db.add(log)
        test_db.commit()
        
        response = client.get(
            "/api/v1/email/alerts/stats",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == str(test_user.id)
        assert data["total_alerts"] >= 1
        assert data["total_emails_received"] >= 1
        assert "engagement_rate" in data


class TestEmailNotifications:
    """Test email notification endpoints."""
    
    def test_send_email_notification_success(self, test_db, test_user, test_user_token, test_email_template):
        """Test sending email notification successfully."""
        # Create user alert
        alert = EmailAlert(
            user_id=test_user.id,
            alert_type="bill_update",
            frequency="daily",
            is_active=True
        )
        test_db.add(alert)
        test_db.commit()
        
        notification_data = {
            "user_id": str(test_user.id),
            "alert_type": "bill_update",
            "content": {
                "title": "Test Bill Update",
                "description": "A test bill has been updated",
                "link": "https://example.com/bill/123"
            }
        }
        
        with patch('app.api.v1.email_alerts.send_email') as mock_send:
            mock_send.return_value = True
            
            response = client.post(
                "/api/v1/email/notifications/send",
                json=notification_data,
                headers={"Authorization": f"Bearer {test_user_token}"}
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "message_id" in data
        
        # Verify email log was created
        email_log = test_db.query(EmailLog).filter(
            EmailLog.user_id == test_user.id
        ).first()
        assert email_log is not None
        assert email_log.status == "sent"
    
    def test_send_email_notification_user_not_found(self, test_db, test_user_token):
        """Test sending notification to non-existent user."""
        notification_data = {
            "user_id": "nonexistent-id",
            "alert_type": "bill_update",
            "content": {
                "title": "Test",
                "description": "Test content",
                "link": "https://example.com"
            }
        }
        
        response = client.post(
            "/api/v1/email/notifications/send",
            json=notification_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_send_email_notification_no_active_alert(self, test_db, test_user, test_user_token):
        """Test sending notification when user has no active alerts."""
        notification_data = {
            "user_id": str(test_user.id),
            "alert_type": "bill_update",
            "content": {
                "title": "Test",
                "description": "Test content",
                "link": "https://example.com"
            }
        }
        
        response = client.post(
            "/api/v1/email/notifications/send",
            json=notification_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 400
        assert "does not have active alerts" in response.json()["detail"]


class TestUnsubscribeManagement:
    """Test unsubscribe management endpoints."""
    
    def test_generate_unsubscribe_token(self, test_db, test_user, test_user_token):
        """Test generating unsubscribe token."""
        response = client.post(
            "/api/v1/email/unsubscribe/generate",
            json={"alert_type": "bill_update"},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "unsubscribe_url" in data
        assert "expires_at" in data
        
        # Verify token was created in database
        token = test_db.query(UnsubscribeToken).filter(
            UnsubscribeToken.user_id == test_user.id
        ).first()
        assert token is not None
        assert token.alert_type == "bill_update"
    
    def test_generate_unsubscribe_token_all_alerts(self, test_db, test_user, test_user_token):
        """Test generating token for all alerts."""
        response = client.post(
            "/api/v1/email/unsubscribe/generate",
            json={},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "unsubscribe_url" in data
        
        # Verify token was created
        token = test_db.query(UnsubscribeToken).filter(
            UnsubscribeToken.user_id == test_user.id,
            UnsubscribeToken.alert_type.is_(None)
        ).first()
        assert token is not None
    
    def test_unsubscribe_user_success(self, test_db, test_user):
        """Test successful user unsubscribe."""
        # Create unsubscribe token
        token = UnsubscribeToken(
            user_id=test_user.id,
            email=test_user.email,
            token="test-token-123",
            alert_type="bill_update",
            expires_at=datetime.utcnow() + timedelta(days=30),
            is_active=True
        )
        test_db.add(token)
        
        # Create user alert
        alert = EmailAlert(
            user_id=test_user.id,
            alert_type="bill_update",
            frequency="daily",
            is_active=True
        )
        test_db.add(alert)
        test_db.commit()
        
        response = client.post(f"/api/v1/email/unsubscribe/test-token-123")
        
        assert response.status_code == 200
        data = response.json()
        assert "Successfully unsubscribed" in data["message"]
        assert data["unsubscribed_from"] == "bill_update"
        
        # Verify alert was deactivated
        test_db.refresh(alert)
        assert alert.is_active == False
        
        # Verify token was marked as used
        test_db.refresh(token)
        assert token.used_at is not None
        assert token.is_active == False
    
    def test_unsubscribe_user_invalid_token(self, test_db):
        """Test unsubscribe with invalid token."""
        response = client.post("/api/v1/email/unsubscribe/invalid-token")
        
        assert response.status_code == 400
        assert "Invalid or expired" in response.json()["detail"]
    
    def test_unsubscribe_user_expired_token(self, test_db, test_user):
        """Test unsubscribe with expired token."""
        # Create expired token
        token = UnsubscribeToken(
            user_id=test_user.id,
            email=test_user.email,
            token="expired-token",
            alert_type="bill_update",
            expires_at=datetime.utcnow() - timedelta(days=1),
            is_active=True
        )
        test_db.add(token)
        test_db.commit()
        
        response = client.post("/api/v1/email/unsubscribe/expired-token")
        
        assert response.status_code == 400
        assert "expired" in response.json()["detail"]


class TestEmailAlertSystemIntegration:
    """Integration tests for the complete email alert system."""
    
    def test_complete_email_alert_workflow(self, test_db, test_user, test_user_token):
        """Test complete workflow: create alert, send notification, check analytics."""
        # 1. Create email alert
        alert_data = {
            "alert_type": "bill_update",
            "frequency": "daily",
            "is_active": True
        }
        
        response = client.post(
            "/api/v1/email/alerts",
            json=alert_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        
        # 2. Send notification
        notification_data = {
            "user_id": str(test_user.id),
            "alert_type": "bill_update",
            "content": {
                "title": "Integration Test",
                "description": "Testing complete workflow",
                "link": "https://example.com"
            }
        }
        
        with patch('app.api.v1.email_alerts.send_email') as mock_send:
            mock_send.return_value = True
            
            response = client.post(
                "/api/v1/email/notifications/send",
                json=notification_data,
                headers={"Authorization": f"Bearer {test_user_token}"}
            )
        assert response.status_code == 200
        
        # 3. Check analytics
        response = client.get(
            "/api/v1/email/analytics",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_emails_sent"] >= 1
        
        # 4. Check user stats
        response = client.get(
            "/api/v1/email/alerts/stats",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_alerts"] >= 1
        assert data["total_emails_received"] >= 1
    
    def test_email_alert_pagination(self, test_db, test_user, test_user_token):
        """Test pagination in email alert listing."""
        # Create multiple alerts
        for i in range(25):
            alert = EmailAlert(
                user_id=test_user.id,
                alert_type=f"alert_type_{i}",
                frequency="daily",
                is_active=True
            )
            test_db.add(alert)
        test_db.commit()
        
        # Test first page
        response = client.get(
            "/api/v1/email/alerts?page=1&page_size=10",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["alerts"]) == 10
        assert data["has_next"] == True
        assert data["has_prev"] == False
        
        # Test second page
        response = client.get(
            "/api/v1/email/alerts?page=2&page_size=10",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["alerts"]) == 10
        assert data["has_next"] == True
        assert data["has_prev"] == True
        
        # Test last page
        response = client.get(
            "/api/v1/email/alerts?page=3&page_size=10",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["alerts"]) == 5  # Remaining alerts
        assert data["has_next"] == False
        assert data["has_prev"] == True


if __name__ == "__main__":
    pytest.main([__file__])
