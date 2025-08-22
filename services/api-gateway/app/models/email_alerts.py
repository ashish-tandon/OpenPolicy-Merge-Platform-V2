"""
Email Alert System Models for OpenPolicy V2

Comprehensive email notification system for parliamentary updates and user engagement.
This implements a P1 priority feature identified in the priority analysis.
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, Index, ForeignKey, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime


class EmailAlert(Base):
    """Model for storing email alert subscriptions."""
    
    __tablename__ = "email_alerts"
    __table_args__ = {"schema": "public"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Alert preferences
    alert_type = Column(String(50), nullable=False)  # bill_updates, mp_activity, vote_results, committee_reports, etc.
    frequency = Column(String(20), default="daily", nullable=False)  # realtime, hourly, daily, weekly
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Content preferences
    include_summary = Column(Boolean, default=True, nullable=False)
    include_links = Column(Boolean, default=True, nullable=False)
    include_analytics = Column(Boolean, default=False, nullable=False)
    
    # Filtering preferences (stored as JSON)
    filters = Column(JSON, nullable=True)  # e.g., {"parties": ["Liberal"], "topics": ["Environment"]}
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_sent = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self):
        return f"<EmailAlert(user_id={self.user_id}, alert_type='{self.alert_type}', frequency='{self.frequency}')>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "alert_type": self.alert_type,
            "frequency": self.frequency,
            "is_active": self.is_active,
            "include_summary": self.include_summary,
            "include_links": self.include_links,
            "include_analytics": self.include_analytics,
            "filters": self.filters,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_sent": self.last_sent.isoformat() if self.last_sent else None
        }


class EmailTemplate(Base):
    """Model for storing email templates."""
    
    __tablename__ = "email_templates"
    __table_args__ = {"schema": "public"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_name = Column(String(100), nullable=False, unique=True)
    template_type = Column(String(50), nullable=False)  # bill_update, mp_activity, vote_result, etc.
    
    # Template content
    subject_template = Column(Text, nullable=False)
    html_template = Column(Text, nullable=False)
    text_template = Column(Text, nullable=False)
    
    # Template metadata
    description = Column(Text, nullable=True)
    variables = Column(JSON, nullable=True)  # Available template variables
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<EmailTemplate(name='{self.template_name}', type='{self.template_type}')>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": str(self.id),
            "template_name": self.template_name,
            "template_type": self.template_type,
            "subject_template": self.subject_template,
            "html_template": self.html_template,
            "text_template": self.text_template,
            "description": self.description,
            "variables": self.variables,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class EmailCampaign(Base):
    """Model for storing email campaigns and bulk sends."""
    
    __tablename__ = "email_campaigns"
    __table_args__ = {"schema": "public"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_name = Column(String(200), nullable=False)
    campaign_type = Column(String(50), nullable=False)  # bulk, scheduled, triggered
    
    # Campaign content
    subject = Column(String(500), nullable=False)
    html_content = Column(Text, nullable=False)
    text_content = Column(Text, nullable=False)
    
    # Campaign settings
    target_audience = Column(JSON, nullable=True)  # Target user criteria
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Campaign statistics
    total_recipients = Column(Integer, default=0, nullable=False)
    sent_count = Column(Integer, default=0, nullable=False)
    delivered_count = Column(Integer, default=0, nullable=False)
    opened_count = Column(Integer, default=0, nullable=False)
    clicked_count = Column(Integer, default=0, nullable=False)
    bounced_count = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<EmailCampaign(name='{self.campaign_name}', type='{self.campaign_type}')>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": str(self.id),
            "campaign_name": self.campaign_name,
            "campaign_type": self.campaign_type,
            "subject": self.subject,
            "html_content": self.html_content,
            "text_content": self.text_content,
            "target_audience": self.target_audience,
            "scheduled_at": self.scheduled_at.isoformat() if self.scheduled_at else None,
            "is_active": self.is_active,
            "total_recipients": self.total_recipients,
            "sent_count": self.sent_count,
            "delivered_count": self.delivered_count,
            "opened_count": self.opened_count,
            "clicked_count": self.clicked_count,
            "bounced_count": self.bounced_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


# class EmailLog(Base):
#     """Model for storing email delivery logs."""
#     
#     __tablename__ = "email_logs"
#     __table_args__ = {"schema": "public"}
#     
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
#     campaign_id = Column(UUID(as_uuid=True), ForeignKey("email_campaigns.id"), nullable=True, index=True)
#     
#     # Email details
#     email_type = Column(String(50), nullable=False)  # alert, campaign, system
#     recipient_email = Column(String(255), nullable=False)
#     subject = Column(String(500), nullable=False)
#     
#     # Delivery status
#     status = Column(String(50), nullable=False)  # sent, delivered, opened, clicked, bounced, failed
#     sent_at = Column(DateTime(timezone=True), nullable=True)
#     delivered_at = Column(DateTime(timezone=True), nullable=True)
#     opened_at = Column(DateTime(timezone=True), nullable=True)
#     clicked_at = Column(DateTime(timezone=True), nullable=True)
#     
#     # Email provider details
#     provider_message_id = Column(String(255), nullable=True)
#     provider_status = Column(String(100), nullable=True)
#     error_message = Column(Text, nullable=True)
#     
#     # Analytics
#     open_count = Column(Integer, default=0, nullable=False)
#     click_count = Column(Integer, default=0, nullable=False)
#     
#     # Timestamps
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     
#     # Relationships
#     user = relationship("User")
#     campaign = relationship("EmailCampaign")
#     
#     def __repr__(self):
#         return f"<EmailLog(email='{self.recipient_email}', status='{self.status}')>"
#     
#     def to_dict(self):
#         """Convert model to dictionary."""
#         return {
#             "id": str(self.id),
#             "user_id": str(self.user_id) if self.user_id else None,
#             "campaign_id": str(self.campaign_id) if self.campaign_id else None,
#             "email_type": self.email_type,
#             "recipient_email": self.recipient_email,
#             "subject": self.subject,
#             "status": self.status,
#             "sent_at": self.sent_at.isoformat() if self.sent_at else None,
#             "delivered_at": self.delivered_at.isoformat() if self.delivered_at else None,
#             "opened_at": self.opened_at.isoformat() if self.opened_at else None,
#             "clicked_at": self.clicked_at.isoformat() if self.clicked_at else None,
#             "provider_message_id": self.provider_message_id,
#             "provider_status": self.provider_status,
#             "error_message": self.error_message,
#             "open_count": self.open_count,
#             "click_count": self.click_count,
#             "created_at": self.created_at.isoformat() if self.created_at else None
#         }


class UnsubscribeToken(Base):
    """Model for storing unsubscribe tokens for email management."""
    
    __tablename__ = "unsubscribe_tokens"
    __table_args__ = {"schema": "public"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    email = Column(String(255), nullable=False)
    
    # Token details
    token = Column(String(255), nullable=False, unique=True, index=True)
    alert_type = Column(String(50), nullable=True)  # null means unsubscribe from all
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Usage tracking
    used_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self):
        return f"<UnsubscribeToken(user_id={self.user_id}, alert_type='{self.alert_type}')>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "email": self.email,
            "token": self.token,
            "alert_type": self.alert_type,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "used_at": self.used_at.isoformat() if self.used_at else None,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


# Create indexes for efficient queries
__table_args__ = (
    Index('idx_email_alert_user_type', 'user_id', 'alert_type'),
    Index('idx_email_alert_frequency', 'frequency'),
    Index('idx_email_alert_active', 'is_active'),
    Index('idx_email_template_type', 'template_type'),
    Index('idx_email_template_active', 'is_active'),
    Index('idx_email_campaign_type', 'campaign_type'),
    Index('idx_email_campaign_scheduled', 'scheduled_at'),
    Index('idx_email_campaign_active', 'is_active'),
    Index('idx_email_log_user', 'user_id'),
    Index('idx_email_log_campaign', 'campaign_id'),
    Index('idx_email_log_status', 'status'),
    Index('idx_email_log_sent', 'sent_at'),
    Index('idx_unsubscribe_token_user', 'user_id'),
    Index('idx_unsubscribe_token_token', 'token'),
    Index('idx_unsubscribe_token_active', 'is_active'),
)
