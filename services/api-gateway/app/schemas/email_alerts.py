"""
Email Alert System Schemas for OpenPolicy V2

Comprehensive schemas for email notifications, templates, campaigns, and analytics.
This implements a P1 priority feature identified in the priority analysis.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr, validator
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class AlertTypeEnum(str, Enum):
    """Email alert types enumeration"""
    BILL_UPDATES = "bill_updates"
    MP_ACTIVITY = "mp_activity"
    VOTE_RESULTS = "vote_results"
    COMMITTEE_REPORTS = "committee_reports"
    DEBATE_HIGHLIGHTS = "debate_highlights"
    PARLIAMENTARY_SCHEDULE = "parliamentary_schedule"
    CONSTITUENCY_UPDATES = "constituency_updates"
    SYSTEM_NOTIFICATIONS = "system_notifications"


class FrequencyEnum(str, Enum):
    """Email frequency enumeration"""
    REALTIME = "realtime"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class CampaignTypeEnum(str, Enum):
    """Email campaign types enumeration"""
    BULK = "bulk"
    SCHEDULED = "scheduled"
    TRIGGERED = "triggered"
    WELCOME = "welcome"
    ONBOARDING = "onboarding"


class EmailStatusEnum(str, Enum):
    """Email delivery status enumeration"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    CLICKED = "clicked"
    BOUNCED = "bounced"
    FAILED = "failed"


# ============================================================================
# BASE MODELS
# ============================================================================

class EmailAlertBase(BaseModel):
    """Base email alert model"""
    alert_type: AlertTypeEnum = Field(..., description="Type of alert")
    frequency: FrequencyEnum = Field(FrequencyEnum.DAILY, description="Alert frequency")
    is_active: bool = Field(True, description="Whether the alert is active")
    include_summary: bool = Field(True, description="Include content summary")
    include_links: bool = Field(True, description="Include relevant links")
    include_analytics: bool = Field(False, description="Include analytics data")
    filters: Optional[Dict[str, Any]] = Field(None, description="Content filtering preferences")


class EmailTemplateBase(BaseModel):
    """Base email template model"""
    template_name: str = Field(..., description="Template name")
    template_type: AlertTypeEnum = Field(..., description="Template type")
    subject_template: str = Field(..., description="Email subject template")
    html_template: str = Field(..., description="HTML email template")
    text_template: str = Field(..., description="Plain text email template")
    description: Optional[str] = Field(None, description="Template description")
    variables: Optional[Dict[str, Any]] = Field(None, description="Available template variables")
    is_active: bool = Field(True, description="Whether template is active")


class EmailCampaignBase(BaseModel):
    """Base email campaign model"""
    campaign_name: str = Field(..., description="Campaign name")
    campaign_type: CampaignTypeEnum = Field(..., description="Campaign type")
    subject: str = Field(..., description="Email subject")
    html_content: str = Field(..., description="HTML email content")
    text_content: str = Field(..., description="Plain text email content")
    target_audience: Optional[Dict[str, Any]] = Field(None, description="Target user criteria")
    scheduled_at: Optional[datetime] = Field(None, description="Scheduled send time")
    is_active: bool = Field(True, description="Whether campaign is active")


# ============================================================================
# REQUEST MODELS
# ============================================================================

class EmailAlertCreateRequest(EmailAlertBase):
    """Request model for creating email alerts"""
    pass


class EmailAlertUpdateRequest(BaseModel):
    """Request model for updating email alerts"""
    frequency: Optional[FrequencyEnum] = Field(None, description="Alert frequency")
    is_active: Optional[bool] = Field(None, description="Whether the alert is active")
    include_summary: Optional[bool] = Field(None, description="Include content summary")
    include_links: Optional[bool] = Field(None, description="Include relevant links")
    include_analytics: Optional[bool] = Field(None, description="Include analytics data")
    filters: Optional[Dict[str, Any]] = Field(None, description="Content filtering preferences")


class EmailTemplateCreateRequest(EmailTemplateBase):
    """Request model for creating email templates"""
    pass


class EmailTemplateUpdateRequest(BaseModel):
    """Request model for updating email templates"""
    subject_template: Optional[str] = Field(None, description="Email subject template")
    html_template: Optional[str] = Field(None, description="HTML email template")
    text_template: Optional[str] = Field(None, description="Plain text email template")
    description: Optional[str] = Field(None, description="Template description")
    variables: Optional[Dict[str, Any]] = Field(None, description="Available template variables")
    is_active: Optional[bool] = Field(None, description="Whether template is active")


class EmailCampaignCreateRequest(EmailCampaignBase):
    """Request model for creating email campaigns"""
    pass


class EmailCampaignUpdateRequest(BaseModel):
    """Request model for updating email campaigns"""
    campaign_name: Optional[str] = Field(None, description="Campaign name")
    subject: Optional[str] = Field(None, description="Email subject")
    html_content: Optional[str] = Field(None, description="HTML email content")
    text_content: Optional[str] = Field(None, description="Plain text email content")
    target_audience: Optional[Dict[str, Any]] = Field(None, description="Target user criteria")
    scheduled_at: Optional[datetime] = Field(None, description="Scheduled send time")
    is_active: Optional[bool] = Field(None, description="Whether campaign is active")


class SendTestEmailRequest(BaseModel):
    """Request model for sending test emails"""
    recipient_email: EmailStr = Field(..., description="Test recipient email")
    template_id: str = Field(..., description="Template ID to use")
    variables: Optional[Dict[str, Any]] = Field(None, description="Template variables")


class BulkEmailRequest(BaseModel):
    """Request model for bulk email sending"""
    campaign_id: str = Field(..., description="Campaign ID")
    recipient_emails: List[EmailStr] = Field(..., description="List of recipient emails")
    send_immediately: bool = Field(False, description="Send immediately or queue")


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class EmailAlertResponse(EmailAlertBase):
    """Response model for email alerts"""
    id: str = Field(..., description="Alert ID")
    user_id: str = Field(..., description="User ID")
    created_at: datetime = Field(..., description="Creation date")
    updated_at: datetime = Field(..., description="Last update date")
    last_sent: Optional[datetime] = Field(None, description="Last sent date")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "user-123",
                "alert_type": "bill_updates",
                "frequency": "daily",
                "is_active": True,
                "include_summary": True,
                "include_links": True,
                "include_analytics": False,
                "filters": {"parties": ["Liberal"], "topics": ["Environment"]},
                "created_at": "2025-01-15T10:00:00Z",
                "updated_at": "2025-01-15T10:00:00Z"
            }
        }


class EmailTemplateResponse(EmailTemplateBase):
    """Response model for email templates"""
    id: str = Field(..., description="Template ID")
    created_at: datetime = Field(..., description="Creation date")
    updated_at: datetime = Field(..., description="Last update date")


class EmailCampaignResponse(EmailCampaignBase):
    """Response model for email campaigns"""
    id: str = Field(..., description="Campaign ID")
    total_recipients: int = Field(..., description="Total recipients")
    sent_count: int = Field(..., description="Sent count")
    delivered_count: int = Field(..., description="Delivered count")
    opened_count: int = Field(..., description="Opened count")
    clicked_count: int = Field(..., description="Clicked count")
    bounced_count: int = Field(..., description="Bounced count")
    created_at: datetime = Field(..., description="Creation date")
    updated_at: datetime = Field(..., description="Last update date")
    started_at: Optional[datetime] = Field(None, description="Start date")
    completed_at: Optional[datetime] = Field(None, description="Completion date")


class EmailLogResponse(BaseModel):
    """Response model for email logs"""
    id: str = Field(..., description="Log ID")
    user_id: Optional[str] = Field(None, description="User ID")
    campaign_id: Optional[str] = Field(None, description="Campaign ID")
    email_type: str = Field(..., description="Email type")
    recipient_email: str = Field(..., description="Recipient email")
    subject: str = Field(..., description="Email subject")
    status: EmailStatusEnum = Field(..., description="Delivery status")
    sent_at: Optional[datetime] = Field(None, description="Sent date")
    delivered_at: Optional[datetime] = Field(None, description="Delivered date")
    opened_at: Optional[datetime] = Field(None, description="Opened date")
    clicked_at: Optional[datetime] = Field(None, description="Clicked date")
    provider_message_id: Optional[str] = Field(None, description="Provider message ID")
    provider_status: Optional[str] = Field(None, description="Provider status")
    error_message: Optional[str] = Field(None, description="Error message")
    open_count: int = Field(..., description="Open count")
    click_count: int = Field(..., description="Click count")
    created_at: datetime = Field(..., description="Creation date")


class UnsubscribeTokenResponse(BaseModel):
    """Response model for unsubscribe tokens"""
    id: str = Field(..., description="Token ID")
    user_id: str = Field(..., description="User ID")
    email: str = Field(..., description="Email address")
    token: str = Field(..., description="Unsubscribe token")
    alert_type: Optional[str] = Field(None, description="Alert type")
    expires_at: Optional[datetime] = Field(None, description="Expiration date")
    used_at: Optional[datetime] = Field(None, description="Usage date")
    is_active: bool = Field(..., description="Whether token is active")
    created_at: datetime = Field(..., description="Creation date")


# ============================================================================
# LIST RESPONSE MODELS
# ============================================================================

class EmailAlertListResponse(BaseModel):
    """Response model for email alert list"""
    alerts: List[EmailAlertResponse] = Field(..., description="List of email alerts")
    total: int = Field(..., description="Total number of alerts")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Has next page")
    has_prev: bool = Field(..., description="Has previous page")


class EmailTemplateListResponse(BaseModel):
    """Response model for email template list"""
    templates: List[EmailTemplateResponse] = Field(..., description="List of email templates")
    total: int = Field(..., description="Total number of templates")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Has next page")
    has_prev: bool = Field(..., description="Has previous page")


class EmailCampaignListResponse(BaseModel):
    """Response model for email campaign list"""
    campaigns: List[EmailCampaignResponse] = Field(..., description="List of email campaigns")
    total: int = Field(..., description="Total number of campaigns")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Has next page")
    has_prev: bool = Field(..., description="Has previous page")


class EmailLogListResponse(BaseModel):
    """Response model for email log list"""
    logs: List[EmailLogResponse] = Field(..., description="List of email logs")
    total: int = Field(..., description="Total number of logs")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Has next page")
    has_prev: bool = Field(..., description="Has previous page")


# ============================================================================
# ANALYTICS MODELS
# ============================================================================

class EmailAnalyticsResponse(BaseModel):
    """Response model for email analytics"""
    total_emails_sent: int = Field(..., description="Total emails sent")
    total_emails_delivered: int = Field(..., description="Total emails delivered")
    total_emails_opened: int = Field(..., description="Total emails opened")
    total_emails_clicked: int = Field(..., description="Total emails clicked")
    total_emails_bounced: int = Field(..., description="Total emails bounced")
    total_emails_failed: int = Field(..., description="Total emails failed")
    
    # Rates
    delivery_rate: float = Field(..., description="Delivery rate percentage")
    open_rate: float = Field(..., description="Open rate percentage")
    click_rate: float = Field(..., description="Click rate percentage")
    bounce_rate: float = Field(..., description="Bounce rate percentage")
    
    # Time-based analytics
    emails_by_day: Dict[str, int] = Field(..., description="Emails sent by day")
    opens_by_day: Dict[str, int] = Field(..., description="Opens by day")
    clicks_by_day: Dict[str, int] = Field(..., description="Clicks by day")
    
    # Campaign performance
    campaign_performance: List[Dict[str, Any]] = Field(..., description="Campaign performance data")
    
    # Generated timestamp
    generated_at: datetime = Field(..., description="Analytics generation timestamp")


class EmailAlertStatsResponse(BaseModel):
    """Response model for email alert statistics"""
    user_id: str = Field(..., description="User ID")
    total_alerts: int = Field(..., description="Total active alerts")
    alerts_by_type: Dict[str, int] = Field(..., description="Alerts by type")
    alerts_by_frequency: Dict[str, int] = Field(..., description="Alerts by frequency")
    last_alert_sent: Optional[datetime] = Field(None, description="Last alert sent")
    total_emails_received: int = Field(..., description="Total emails received")
    emails_opened: int = Field(..., description="Emails opened")
    emails_clicked: int = Field(..., description="Emails clicked")
    engagement_rate: float = Field(..., description="Overall engagement rate")
    generated_at: datetime = Field(..., description="Statistics generation timestamp")


# ============================================================================
# NOTIFICATION MODELS
# ============================================================================

class NotificationContent(BaseModel):
    """Model for notification content"""
    title: str = Field(..., description="Notification title")
    summary: str = Field(..., description="Content summary")
    content_type: str = Field(..., description="Content type (bill, mp, vote, etc.)")
    content_id: str = Field(..., description="Content ID")
    url: str = Field(..., description="Content URL")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class EmailNotificationRequest(BaseModel):
    """Request model for sending email notifications"""
    user_id: str = Field(..., description="User ID")
    alert_type: AlertTypeEnum = Field(..., description="Alert type")
    content: NotificationContent = Field(..., description="Notification content")
    template_variables: Optional[Dict[str, Any]] = Field(None, description="Template variables")
    priority: str = Field("normal", description="Email priority")


class EmailNotificationResponse(BaseModel):
    """Response model for email notification results"""
    success: bool = Field(..., description="Whether notification was sent successfully")
    message_id: Optional[str] = Field(None, description="Email message ID")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    sent_at: datetime = Field(..., description="Send timestamp")
