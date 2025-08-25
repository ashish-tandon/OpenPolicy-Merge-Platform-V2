"""
Email Notification Models

Enhanced email notification system models.
Implements FEAT-007 Email Notifications (P2 priority).
"""

from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey, Index, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime


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


class EmailTemplate(Base):
    """Email templates with versioning."""
    
    __tablename__ = "email_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Template identification
    template_key = Column(String(100), nullable=False)
    version = Column(Integer, default=1, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Template content
    subject_template = Column(Text, nullable=False)
    html_template = Column(Text, nullable=False)
    text_template = Column(Text, nullable=True)
    
    # Template metadata
    notification_type = Column(SQLEnum(NotificationType), nullable=False)
    variables = Column(JSONB, nullable=True)  # List of expected variables
    
    # Settings
    is_active = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    
    # Localization
    language = Column(String(10), default="en", nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    notifications = relationship("EmailNotification", back_populates="template")
    
    # Indexes
    __table_args__ = (
        Index('idx_template_key_version', 'template_key', 'version', unique=True),
        Index('idx_template_type', 'notification_type'),
        Index('idx_template_active', 'is_active'),
        Index('idx_template_language', 'language'),
    )


class NotificationPreference(Base):
    """User notification preferences."""
    
    __tablename__ = "notification_preferences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Global preferences
    email_enabled = Column(Boolean, default=True, nullable=False)
    unsubscribe_token = Column(String(100), unique=True, nullable=True)
    
    # Type-specific preferences
    preferences = Column(JSONB, nullable=False, default={})
    # Structure: {
    #   "alert": {"enabled": true, "frequency": "realtime", "channels": ["email"]},
    #   "digest": {"enabled": true, "frequency": "daily", "time": "09:00"},
    #   "announcement": {"enabled": true, "frequency": "immediate"}
    # }
    
    # Quiet hours
    quiet_hours_enabled = Column(Boolean, default=False, nullable=False)
    quiet_hours_start = Column(String(5), nullable=True)  # HH:MM format
    quiet_hours_end = Column(String(5), nullable=True)
    quiet_hours_timezone = Column(String(50), default="UTC", nullable=False)
    
    # Digest settings
    digest_enabled = Column(Boolean, default=True, nullable=False)
    digest_frequency = Column(String(20), default="daily", nullable=False)
    digest_day = Column(Integer, nullable=True)  # For weekly digests (0-6)
    digest_time = Column(String(5), default="09:00", nullable=False)  # HH:MM
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="notification_preferences")
    
    # Indexes
    __table_args__ = (
        Index('idx_pref_user', 'user_id', unique=True),
        Index('idx_pref_token', 'unsubscribe_token'),
    )


class EmailNotification(Base):
    """Individual email notifications."""
    
    __tablename__ = "email_notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Recipient
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    recipient_email = Column(String(255), nullable=False)
    recipient_name = Column(String(200), nullable=True)
    
    # Template and content
    template_id = Column(UUID(as_uuid=True), ForeignKey("email_templates.id"), nullable=True)
    notification_type = Column(SQLEnum(NotificationType), nullable=False)
    subject = Column(Text, nullable=False)
    
    # Variables for template rendering
    template_variables = Column(JSONB, nullable=True)
    
    # Metadata
    priority = Column(SQLEnum(NotificationPriority), default=NotificationPriority.MEDIUM, nullable=False)
    reference_id = Column(String(100), nullable=True)  # External reference
    tags = Column(JSONB, nullable=True)  # Array of tags
    
    # Scheduling
    scheduled_for = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Status tracking
    status = Column(SQLEnum(EmailStatus), default=EmailStatus.PENDING, nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    last_attempt_at = Column(DateTime(timezone=True), nullable=True)
    
    # Provider information
    provider = Column(SQLEnum(EmailProvider), nullable=True)
    provider_message_id = Column(String(255), nullable=True)
    provider_response = Column(JSONB, nullable=True)
    
    # Delivery tracking
    sent_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    opened_at = Column(DateTime(timezone=True), nullable=True)
    clicked_at = Column(DateTime(timezone=True), nullable=True)
    
    # Error handling
    error_message = Column(Text, nullable=True)
    error_details = Column(JSONB, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="email_notifications")
    template = relationship("EmailTemplate", back_populates="notifications")
    events = relationship("EmailEvent", back_populates="notification", cascade="all, delete-orphan")
    attachments = relationship("EmailAttachment", back_populates="notification", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_notification_user', 'user_id'),
        Index('idx_notification_status', 'status'),
        Index('idx_notification_scheduled', 'scheduled_for'),
        Index('idx_notification_created', 'created_at'),
        Index('idx_notification_reference', 'reference_id'),
        Index('idx_notification_provider_id', 'provider_message_id'),
    )


class EmailEvent(Base):
    """Email delivery events and tracking."""
    
    __tablename__ = "email_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    notification_id = Column(UUID(as_uuid=True), ForeignKey("email_notifications.id"), nullable=False)
    
    # Event details
    event_type = Column(String(50), nullable=False)  # sent, delivered, opened, clicked, bounced, complained
    event_data = Column(JSONB, nullable=True)
    
    # Source information
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Timestamp
    occurred_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    notification = relationship("EmailNotification", back_populates="events")
    
    # Indexes
    __table_args__ = (
        Index('idx_event_notification', 'notification_id'),
        Index('idx_event_type', 'event_type'),
        Index('idx_event_occurred', 'occurred_at'),
    )


class EmailAttachment(Base):
    """Email attachments."""
    
    __tablename__ = "email_attachments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    notification_id = Column(UUID(as_uuid=True), ForeignKey("email_notifications.id"), nullable=False)
    
    # Attachment details
    filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    size_bytes = Column(Integer, nullable=False)
    
    # Storage
    storage_path = Column(String(500), nullable=True)  # For file storage
    content_base64 = Column(Text, nullable=True)  # For small attachments
    
    # Metadata
    checksum = Column(String(64), nullable=True)  # SHA256
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    notification = relationship("EmailNotification", back_populates="attachments")
    
    # Indexes
    __table_args__ = (
        Index('idx_attachment_notification', 'notification_id'),
    )


class EmailBatch(Base):
    """Batch email operations."""
    
    __tablename__ = "email_batches"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Batch details
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    batch_type = Column(String(50), nullable=False)  # digest, campaign, announcement
    
    # Template
    template_id = Column(UUID(as_uuid=True), ForeignKey("email_templates.id"), nullable=True)
    
    # Recipients
    recipient_count = Column(Integer, default=0, nullable=False)
    recipient_criteria = Column(JSONB, nullable=True)  # Query criteria
    
    # Status
    status = Column(String(50), default="draft", nullable=False)  # draft, scheduled, sending, completed, cancelled
    
    # Scheduling
    scheduled_for = Column(DateTime(timezone=True), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Statistics
    sent_count = Column(Integer, default=0, nullable=False)
    failed_count = Column(Integer, default=0, nullable=False)
    opened_count = Column(Integer, default=0, nullable=False)
    clicked_count = Column(Integer, default=0, nullable=False)
    
    # Creator
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    template = relationship("EmailTemplate")
    creator = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_batch_status', 'status'),
        Index('idx_batch_scheduled', 'scheduled_for'),
        Index('idx_batch_created_by', 'created_by'),
    )


class NotificationQueue(Base):
    """Queue for processing notifications."""
    
    __tablename__ = "notification_queue"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Queue item
    notification_id = Column(UUID(as_uuid=True), ForeignKey("email_notifications.id"), nullable=False)
    priority = Column(Integer, default=0, nullable=False)  # Higher number = higher priority
    
    # Processing
    status = Column(String(50), default="pending", nullable=False)  # pending, processing, completed, failed
    processor_id = Column(String(100), nullable=True)  # Worker ID
    
    # Retry logic
    retry_count = Column(Integer, default=0, nullable=False)
    retry_after = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    notification = relationship("EmailNotification")
    
    # Indexes
    __table_args__ = (
        Index('idx_queue_status', 'status'),
        Index('idx_queue_priority', 'priority', 'created_at'),
        Index('idx_queue_retry', 'retry_after'),
    )


class EmailProvider(Base):
    """Email service provider configuration."""
    
    __tablename__ = "email_providers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Provider details
    provider_type = Column(SQLEnum(EmailProvider), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    
    # Configuration (encrypted in production)
    config = Column(JSONB, nullable=False)  # API keys, SMTP settings, etc.
    
    # Rate limiting
    rate_limit_per_second = Column(Integer, nullable=True)
    rate_limit_per_day = Column(Integer, nullable=True)
    
    # Statistics
    total_sent = Column(Integer, default=0, nullable=False)
    total_failed = Column(Integer, default=0, nullable=False)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_provider_active', 'is_active'),
        Index('idx_provider_default', 'is_default'),
    )