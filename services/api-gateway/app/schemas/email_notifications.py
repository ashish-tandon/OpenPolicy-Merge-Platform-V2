"""
Email Notification Schemas

Pydantic schemas for enhanced email notification functionality.
Implements FEAT-007 Email Notifications (P2 priority).
"""

from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum


# Enums (matching model enums)
class EmailProvider(str, Enum):
    """Supported email service providers."""
    SMTP = "smtp"
    SENDGRID = "sendgrid"
    MAILGUN = "mailgun"
    POSTMARK = "postmark"
    RESEND = "resend"
    AWS_SES = "aws_ses"


class EmailStatus(str, Enum):
    """Email delivery status."""
    PENDING = "pending"
    SENDING = "sending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    BOUNCED = "bounced"
    COMPLAINED = "complained"


class NotificationType(str, Enum):
    """Types of notifications."""
    ALERT = "alert"
    DIGEST = "digest"
    WELCOME = "welcome"
    VERIFICATION = "verification"
    PASSWORD_RESET = "password_reset"
    REPORT = "report"
    INVITATION = "invitation"
    REMINDER = "reminder"
    ANNOUNCEMENT = "announcement"
    CUSTOM = "custom"


class NotificationPriority(str, Enum):
    """Notification priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class NotificationFrequency(str, Enum):
    """Notification frequency options."""
    REALTIME = "realtime"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    NEVER = "never"


# Template schemas
class TemplateVariable(BaseModel):
    """Template variable definition."""
    name: str
    type: str = Field(..., regex="^(string|number|boolean|array|object)$")
    required: bool = True
    default: Optional[Any] = None
    description: Optional[str] = None


class EmailTemplateBase(BaseModel):
    """Base email template schema."""
    template_key: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    subject_template: str = Field(..., min_length=1)
    html_template: str = Field(..., min_length=1)
    text_template: Optional[str] = None
    notification_type: NotificationType
    variables: Optional[List[TemplateVariable]] = None
    language: str = Field("en", regex="^[a-z]{2}$")


class EmailTemplateCreate(EmailTemplateBase):
    """Schema for creating email template."""
    pass


class EmailTemplateUpdate(BaseModel):
    """Schema for updating email template."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    subject_template: Optional[str] = Field(None, min_length=1)
    html_template: Optional[str] = Field(None, min_length=1)
    text_template: Optional[str] = None
    variables: Optional[List[TemplateVariable]] = None
    is_active: Optional[bool] = None


class EmailTemplateResponse(EmailTemplateBase):
    """Schema for email template responses."""
    id: UUID
    version: int
    is_active: bool
    is_default: bool
    created_at: datetime
    updated_at: datetime
    usage_count: int = 0
    
    class Config:
        orm_mode = True


# Preference schemas
class NotificationTypePreference(BaseModel):
    """Preference for a specific notification type."""
    enabled: bool = True
    frequency: NotificationFrequency = NotificationFrequency.REALTIME
    channels: List[str] = Field(default_factory=lambda: ["email"])
    filters: Optional[Dict[str, Any]] = None


class PreferenceUpdate(BaseModel):
    """Schema for updating notification preferences."""
    email_enabled: Optional[bool] = None
    preferences: Optional[Dict[NotificationType, NotificationTypePreference]] = None
    quiet_hours_enabled: Optional[bool] = None
    quiet_hours_start: Optional[str] = Field(None, regex="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    quiet_hours_end: Optional[str] = Field(None, regex="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    quiet_hours_timezone: Optional[str] = None
    digest_enabled: Optional[bool] = None
    digest_frequency: Optional[str] = Field(None, regex="^(daily|weekly|monthly)$")
    digest_day: Optional[int] = Field(None, ge=0, le=6)
    digest_time: Optional[str] = Field(None, regex="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")


class PreferenceResponse(BaseModel):
    """Schema for preference responses."""
    id: UUID
    user_id: UUID
    email_enabled: bool
    unsubscribe_token: Optional[str]
    preferences: Dict[str, Any]
    quiet_hours_enabled: bool
    quiet_hours_start: Optional[str]
    quiet_hours_end: Optional[str]
    quiet_hours_timezone: str
    digest_enabled: bool
    digest_frequency: str
    digest_day: Optional[int]
    digest_time: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Notification schemas
class EmailNotificationBase(BaseModel):
    """Base email notification schema."""
    recipient_email: EmailStr
    recipient_name: Optional[str] = None
    notification_type: NotificationType
    subject: str = Field(..., min_length=1)
    priority: NotificationPriority = NotificationPriority.MEDIUM


class EmailNotificationCreate(EmailNotificationBase):
    """Schema for creating email notification."""
    user_id: Optional[UUID] = None
    template_id: Optional[UUID] = None
    template_variables: Optional[Dict[str, Any]] = None
    reference_id: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = None
    scheduled_for: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    
    @validator('expires_at')
    def validate_expiry(cls, v, values):
        if v and 'scheduled_for' in values and values['scheduled_for']:
            if v <= values['scheduled_for']:
                raise ValueError('Expiry time must be after scheduled time')
        return v


class EmailNotificationResponse(EmailNotificationBase):
    """Schema for email notification responses."""
    id: UUID
    user_id: Optional[UUID]
    template_id: Optional[UUID]
    template_variables: Optional[Dict[str, Any]]
    reference_id: Optional[str]
    tags: Optional[List[str]]
    scheduled_for: Optional[datetime]
    expires_at: Optional[datetime]
    status: EmailStatus
    attempts: int
    last_attempt_at: Optional[datetime]
    provider: Optional[EmailProvider]
    provider_message_id: Optional[str]
    sent_at: Optional[datetime]
    delivered_at: Optional[datetime]
    opened_at: Optional[datetime]
    clicked_at: Optional[datetime]
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class EmailNotificationListResponse(BaseModel):
    """Schema for notification list responses."""
    results: List[EmailNotificationResponse]
    pagination: Dict[str, Any]
    
    class Config:
        orm_mode = True


# Event schemas
class EmailEventResponse(BaseModel):
    """Schema for email event responses."""
    id: UUID
    notification_id: UUID
    event_type: str
    event_data: Optional[Dict[str, Any]]
    ip_address: Optional[str]
    user_agent: Optional[str]
    occurred_at: datetime
    
    class Config:
        orm_mode = True


# Attachment schemas
class AttachmentCreate(BaseModel):
    """Schema for creating attachment."""
    filename: str = Field(..., min_length=1, max_length=255)
    content_type: str = Field(..., min_length=1, max_length=100)
    content_base64: str = Field(..., min_length=1)
    
    @validator('content_base64')
    def validate_base64(cls, v):
        import base64
        try:
            base64.b64decode(v)
        except Exception:
            raise ValueError('Invalid base64 content')
        return v


class AttachmentResponse(BaseModel):
    """Schema for attachment responses."""
    id: UUID
    filename: str
    content_type: str
    size_bytes: int
    checksum: Optional[str]
    created_at: datetime
    
    class Config:
        orm_mode = True


# Batch schemas
class BatchRecipientCriteria(BaseModel):
    """Criteria for selecting batch recipients."""
    user_groups: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    preferences: Optional[Dict[str, Any]] = None
    custom_query: Optional[str] = None


class EmailBatchBase(BaseModel):
    """Base email batch schema."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    batch_type: str = Field(..., regex="^(digest|campaign|announcement)$")
    template_id: UUID
    recipient_criteria: BatchRecipientCriteria


class EmailBatchCreate(EmailBatchBase):
    """Schema for creating email batch."""
    scheduled_for: Optional[datetime] = None


class EmailBatchUpdate(BaseModel):
    """Schema for updating email batch."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    scheduled_for: Optional[datetime] = None
    status: Optional[str] = Field(None, regex="^(draft|scheduled|cancelled)$")


class EmailBatchResponse(EmailBatchBase):
    """Schema for email batch responses."""
    id: UUID
    recipient_count: int
    status: str
    scheduled_for: Optional[datetime]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    sent_count: int
    failed_count: int
    opened_count: int
    clicked_count: int
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Send request schemas
class SendEmailRequest(BaseModel):
    """Request to send an email."""
    to: List[EmailStr] = Field(..., min_items=1)
    subject: str = Field(..., min_length=1)
    html_content: Optional[str] = None
    text_content: Optional[str] = None
    template_id: Optional[UUID] = None
    template_variables: Optional[Dict[str, Any]] = None
    attachments: Optional[List[AttachmentCreate]] = None
    priority: NotificationPriority = NotificationPriority.MEDIUM
    tags: Optional[List[str]] = None
    reference_id: Optional[str] = Field(None, max_length=100)
    
    @validator('html_content')
    def validate_content(cls, v, values):
        if not v and not values.get('template_id'):
            raise ValueError('Either html_content or template_id must be provided')
        return v


class SendBulkEmailRequest(BaseModel):
    """Request to send bulk emails."""
    template_id: UUID
    recipients: List[Dict[str, Any]]  # [{email, name, variables}, ...]
    default_variables: Optional[Dict[str, Any]] = None
    batch_name: str = Field(..., min_length=1, max_length=200)
    scheduled_for: Optional[datetime] = None
    priority: NotificationPriority = NotificationPriority.LOW


# Analytics schemas
class EmailAnalytics(BaseModel):
    """Email analytics data."""
    period: str  # day, week, month
    total_sent: int
    total_delivered: int
    total_opened: int
    total_clicked: int
    total_bounced: int
    total_complained: int
    delivery_rate: float
    open_rate: float
    click_rate: float
    bounce_rate: float
    complaint_rate: float
    by_type: Dict[str, Dict[str, int]]
    by_provider: Dict[str, Dict[str, int]]


class ProviderStats(BaseModel):
    """Provider statistics."""
    provider: EmailProvider
    is_active: bool
    total_sent: int
    total_failed: int
    success_rate: float
    avg_delivery_time: Optional[float]
    last_used_at: Optional[datetime]


# Webhook schemas
class WebhookEvent(BaseModel):
    """Webhook event from email provider."""
    provider: EmailProvider
    event_type: str
    message_id: str
    timestamp: datetime
    data: Dict[str, Any]


# Unsubscribe schemas
class UnsubscribeRequest(BaseModel):
    """Request to unsubscribe."""
    token: str = Field(..., min_length=1)
    notification_types: Optional[List[NotificationType]] = None
    reason: Optional[str] = None
    feedback: Optional[str] = None


class UnsubscribeResponse(BaseModel):
    """Response for unsubscribe request."""
    success: bool
    message: str
    unsubscribed_types: List[str]