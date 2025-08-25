"""
Feedback Models

Models for user feedback collection system.
Implements FEAT-003 Feedback Collection (P1 priority).
"""

from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey, Index, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime


class FeedbackType(str, Enum):
    """Types of feedback."""
    BUG_REPORT = "bug_report"
    FEATURE_REQUEST = "feature_request"
    GENERAL_FEEDBACK = "general_feedback"
    COMPLAINT = "complaint"
    SUGGESTION = "suggestion"
    QUESTION = "question"


class FeedbackStatus(str, Enum):
    """Feedback processing status."""
    PENDING = "pending"
    IN_REVIEW = "in_review"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REJECTED = "rejected"
    DUPLICATE = "duplicate"


class FeedbackPriority(str, Enum):
    """Feedback priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FeedbackCategory(str, Enum):
    """Feedback categories."""
    UI_UX = "ui_ux"
    PERFORMANCE = "performance"
    DATA_QUALITY = "data_quality"
    FUNCTIONALITY = "functionality"
    DOCUMENTATION = "documentation"
    SECURITY = "security"
    ACCESSIBILITY = "accessibility"
    OTHER = "other"


class Feedback(Base):
    """User feedback model."""
    
    __tablename__ = "feedback"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # User information
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    user_email = Column(String(255), nullable=True)  # For anonymous feedback
    user_name = Column(String(200), nullable=True)  # For anonymous feedback
    
    # Feedback details
    type = Column(SQLEnum(FeedbackType), nullable=False, default=FeedbackType.GENERAL_FEEDBACK)
    category = Column(SQLEnum(FeedbackCategory), nullable=False, default=FeedbackCategory.OTHER)
    subject = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    
    # Context information
    page_url = Column(String(1000), nullable=True)  # Where feedback was submitted from
    browser_info = Column(JSONB, nullable=True)  # User agent, browser, OS
    session_data = Column(JSONB, nullable=True)  # Session context
    
    # Status tracking
    status = Column(SQLEnum(FeedbackStatus), nullable=False, default=FeedbackStatus.PENDING)
    priority = Column(SQLEnum(FeedbackPriority), nullable=False, default=FeedbackPriority.MEDIUM)
    
    # Processing information
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    resolution_notes = Column(Text, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    metadata = Column(JSONB, nullable=True)  # Additional structured data
    tags = Column(JSONB, nullable=True)  # Array of tags
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], backref="submitted_feedback")
    assignee = relationship("User", foreign_keys=[assigned_to], backref="assigned_feedback")
    attachments = relationship("FeedbackAttachment", back_populates="feedback", cascade="all, delete-orphan")
    responses = relationship("FeedbackResponse", back_populates="feedback", cascade="all, delete-orphan")
    votes = relationship("FeedbackVote", back_populates="feedback", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_feedback_user_id', 'user_id'),
        Index('idx_feedback_status', 'status'),
        Index('idx_feedback_priority', 'priority'),
        Index('idx_feedback_type', 'type'),
        Index('idx_feedback_category', 'category'),
        Index('idx_feedback_created_at', 'created_at'),
        Index('idx_feedback_assigned_to', 'assigned_to'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id) if self.user_id else None,
            "user_email": self.user_email,
            "user_name": self.user_name,
            "type": self.type,
            "category": self.category,
            "subject": self.subject,
            "description": self.description,
            "page_url": self.page_url,
            "status": self.status,
            "priority": self.priority,
            "assigned_to": str(self.assigned_to) if self.assigned_to else None,
            "resolution_notes": self.resolution_notes,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "metadata": self.metadata,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class FeedbackAttachment(Base):
    """Attachments for feedback."""
    
    __tablename__ = "feedback_attachments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feedback_id = Column(UUID(as_uuid=True), ForeignKey("feedback.id"), nullable=False)
    
    # File information
    filename = Column(String(255), nullable=False)
    file_type = Column(String(100), nullable=False)
    file_size = Column(Integer, nullable=False)  # In bytes
    file_url = Column(String(1000), nullable=False)
    
    # Metadata
    description = Column(Text, nullable=True)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    feedback = relationship("Feedback", back_populates="attachments")
    uploader = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_attachment_feedback_id', 'feedback_id'),
    )


class FeedbackResponse(Base):
    """Responses to feedback."""
    
    __tablename__ = "feedback_responses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feedback_id = Column(UUID(as_uuid=True), ForeignKey("feedback.id"), nullable=False)
    
    # Response details
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=False, nullable=False)  # Internal notes vs public response
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    feedback = relationship("Feedback", back_populates="responses")
    user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_response_feedback_id', 'feedback_id'),
        Index('idx_response_user_id', 'user_id'),
        Index('idx_response_created_at', 'created_at'),
    )


class FeedbackVote(Base):
    """Votes on feedback items."""
    
    __tablename__ = "feedback_votes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feedback_id = Column(UUID(as_uuid=True), ForeignKey("feedback.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Vote type (1 = upvote, -1 = downvote)
    vote_type = Column(Integer, nullable=False)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    feedback = relationship("Feedback", back_populates="votes")
    user = relationship("User")
    
    # Indexes and constraints
    __table_args__ = (
        Index('idx_vote_feedback_id', 'feedback_id'),
        Index('idx_vote_user_id', 'user_id'),
        Index('idx_vote_feedback_user', 'feedback_id', 'user_id', unique=True),  # One vote per user per feedback
    )


class FeedbackTemplate(Base):
    """Templates for feedback forms."""
    
    __tablename__ = "feedback_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Template details
    name = Column(String(200), nullable=False, unique=True)
    type = Column(SQLEnum(FeedbackType), nullable=False)
    category = Column(SQLEnum(FeedbackCategory), nullable=False)
    
    # Form fields configuration
    fields = Column(JSONB, nullable=False)  # JSON schema for form fields
    
    # Settings
    is_active = Column(Boolean, default=True, nullable=False)
    requires_auth = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_template_name', 'name'),
        Index('idx_template_type', 'type'),
        Index('idx_template_active', 'is_active'),
    )