"""
Feedback Schemas

Pydantic schemas for feedback collection functionality.
Implements FEAT-003 Feedback Collection (P1 priority).
"""

from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum


# Enums (matching model enums)
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


# Request/Response schemas
class FeedbackBase(BaseModel):
    """Base feedback schema."""
    type: FeedbackType = Field(..., description="Type of feedback")
    category: FeedbackCategory = Field(..., description="Category of feedback")
    subject: str = Field(..., min_length=5, max_length=500, description="Brief subject/title")
    description: str = Field(..., min_length=10, description="Detailed description")
    
    @validator('subject')
    def validate_subject(cls, v):
        if not v or len(v.strip()) < 5:
            raise ValueError('Subject must be at least 5 characters long')
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        if not v or len(v.strip()) < 10:
            raise ValueError('Description must be at least 10 characters long')
        return v.strip()


class FeedbackCreate(FeedbackBase):
    """Schema for creating feedback."""
    user_email: Optional[EmailStr] = Field(None, description="Email for anonymous feedback")
    user_name: Optional[str] = Field(None, max_length=200, description="Name for anonymous feedback")
    page_url: Optional[str] = Field(None, max_length=1000, description="Page where feedback was submitted")
    browser_info: Optional[Dict[str, Any]] = Field(None, description="Browser information")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    tags: Optional[List[str]] = Field(None, description="Tags for categorization")


class FeedbackUpdate(BaseModel):
    """Schema for updating feedback."""
    type: Optional[FeedbackType] = None
    category: Optional[FeedbackCategory] = None
    subject: Optional[str] = Field(None, min_length=5, max_length=500)
    description: Optional[str] = Field(None, min_length=10)
    status: Optional[FeedbackStatus] = None
    priority: Optional[FeedbackPriority] = None
    resolution_notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None


class FeedbackAssign(BaseModel):
    """Schema for assigning feedback."""
    assignee_id: UUID = Field(..., description="User ID to assign feedback to")
    priority: Optional[FeedbackPriority] = Field(None, description="Update priority")
    notes: Optional[str] = Field(None, description="Assignment notes")


class FeedbackResponse(FeedbackBase):
    """Schema for feedback responses."""
    id: UUID
    user_id: Optional[UUID]
    user_email: Optional[str]
    user_name: Optional[str]
    page_url: Optional[str]
    browser_info: Optional[Dict[str, Any]]
    status: FeedbackStatus
    priority: FeedbackPriority
    assigned_to: Optional[UUID]
    resolution_notes: Optional[str]
    resolved_at: Optional[datetime]
    metadata: Optional[Dict[str, Any]]
    tags: Optional[List[str]]
    created_at: datetime
    updated_at: datetime
    
    # Related counts
    attachment_count: int = 0
    response_count: int = 0
    vote_score: int = 0  # Sum of votes (upvotes - downvotes)
    
    class Config:
        orm_mode = True


class FeedbackListResponse(BaseModel):
    """Schema for feedback list responses."""
    results: List[FeedbackResponse]
    pagination: Dict[str, Any]
    filters: Dict[str, Any]
    
    class Config:
        orm_mode = True


# Attachment schemas
class AttachmentCreate(BaseModel):
    """Schema for creating attachment."""
    filename: str = Field(..., min_length=1, max_length=255)
    file_type: str = Field(..., min_length=1, max_length=100)
    file_size: int = Field(..., gt=0, description="File size in bytes")
    file_url: str = Field(..., min_length=1, max_length=1000)
    description: Optional[str] = None


class AttachmentResponse(BaseModel):
    """Schema for attachment responses."""
    id: UUID
    feedback_id: UUID
    filename: str
    file_type: str
    file_size: int
    file_url: str
    description: Optional[str]
    uploaded_by: UUID
    uploaded_at: datetime
    
    class Config:
        orm_mode = True


# Response schemas
class ResponseCreate(BaseModel):
    """Schema for creating feedback response."""
    message: str = Field(..., min_length=1, description="Response message")
    is_internal: bool = Field(False, description="Internal note vs public response")


class ResponseUpdate(BaseModel):
    """Schema for updating feedback response."""
    message: str = Field(..., min_length=1)


class ResponseItem(BaseModel):
    """Schema for response items."""
    id: UUID
    feedback_id: UUID
    user_id: UUID
    user_name: Optional[str]  # Populated from user relationship
    message: str
    is_internal: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Vote schemas
class VoteCreate(BaseModel):
    """Schema for creating vote."""
    vote_type: int = Field(..., ge=-1, le=1, ne=0, description="1 for upvote, -1 for downvote")


class VoteResponse(BaseModel):
    """Schema for vote response."""
    feedback_id: UUID
    user_vote: Optional[int] = Field(None, description="Current user's vote")
    total_score: int = Field(..., description="Total vote score")
    upvotes: int = Field(..., description="Number of upvotes")
    downvotes: int = Field(..., description="Number of downvotes")


# Template schemas
class TemplateBase(BaseModel):
    """Base template schema."""
    name: str = Field(..., min_length=1, max_length=200)
    type: FeedbackType
    category: FeedbackCategory
    fields: Dict[str, Any] = Field(..., description="JSON schema for form fields")
    is_active: bool = True
    requires_auth: bool = False


class TemplateCreate(TemplateBase):
    """Schema for creating template."""
    pass


class TemplateUpdate(BaseModel):
    """Schema for updating template."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    type: Optional[FeedbackType] = None
    category: Optional[FeedbackCategory] = None
    fields: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    requires_auth: Optional[bool] = None


class TemplateResponse(TemplateBase):
    """Schema for template responses."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Analytics schemas
class FeedbackStats(BaseModel):
    """Schema for feedback statistics."""
    total_count: int
    by_status: Dict[str, int]
    by_type: Dict[str, int]
    by_category: Dict[str, int]
    by_priority: Dict[str, int]
    avg_resolution_time: Optional[float]  # In hours
    pending_count: int
    resolved_count: int
    response_rate: float  # Percentage of feedback with responses


class FeedbackTrends(BaseModel):
    """Schema for feedback trends."""
    period: str  # daily, weekly, monthly
    data: List[Dict[str, Any]]  # Time series data
    
    
class FeedbackFilter(BaseModel):
    """Schema for filtering feedback."""
    type: Optional[FeedbackType] = None
    category: Optional[FeedbackCategory] = None
    status: Optional[FeedbackStatus] = None
    priority: Optional[FeedbackPriority] = None
    user_id: Optional[UUID] = None
    assigned_to: Optional[UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    search: Optional[str] = Field(None, description="Search in subject and description")
    tags: Optional[List[str]] = None
    has_attachments: Optional[bool] = None
    has_responses: Optional[bool] = None
    
    # Pagination
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    
    # Sorting
    sort_by: str = Field("created_at", regex="^(created_at|updated_at|priority|vote_score)$")
    sort_order: str = Field("desc", regex="^(asc|desc)$")