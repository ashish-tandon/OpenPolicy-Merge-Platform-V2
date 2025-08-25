"""
Debate Transcript Schemas

Pydantic schemas for debate transcript functionality.
Implements FEAT-018 Debate Transcripts (P1 priority).
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time
from uuid import UUID
from enum import Enum


# Enums
class StatementType(str, Enum):
    """Types of debate statements."""
    SPEECH = "speech"
    QUESTION = "question"
    ANSWER = "answer"
    INTERVENTION = "intervention"
    PROCEDURAL = "procedural"
    POINT_OF_ORDER = "point_of_order"
    SPEAKER_RULING = "speaker_ruling"


class AnnotationType(str, Enum):
    """Types of annotations."""
    CORRECTION = "correction"
    CLARIFICATION = "clarification"
    CONTEXT = "context"
    REFERENCE = "reference"


class HouseStatus(str, Enum):
    """House sitting status."""
    SITTING = "sitting"
    COMMITTEE_OF_WHOLE = "committee_of_whole"
    ADJOURNMENT = "adjournment"
    SUSPENSION = "suspension"


# Session schemas
class SessionBase(BaseModel):
    """Base debate session schema."""
    parliament_number: int = Field(..., ge=1, le=99)
    session_number: int = Field(..., ge=1, le=10)
    sitting_number: int = Field(..., ge=1, le=999)
    sitting_date: date
    language: str = Field("en", regex="^(en|fr)$")
    is_bilingual: bool = True
    
    @validator('sitting_date')
    def validate_date(cls, v):
        if v > date.today():
            raise ValueError('Sitting date cannot be in the future')
        return v


class SessionCreate(SessionBase):
    """Schema for creating debate session."""
    source_url: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    house_status: Optional[HouseStatus] = None


class SessionUpdate(BaseModel):
    """Schema for updating debate session."""
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    house_status: Optional[HouseStatus] = None
    topics: Optional[List[str]] = None
    bills_discussed: Optional[List[str]] = None
    committees_mentioned: Optional[List[str]] = None


class SessionResponse(SessionBase):
    """Schema for debate session responses."""
    id: UUID
    document_number: str
    source_url: Optional[str]
    start_time: Optional[time]
    end_time: Optional[time]
    house_status: Optional[str]
    total_statements: int
    total_words: int
    total_speakers: int
    topics: Optional[List[str]]
    bills_discussed: Optional[List[str]]
    committees_mentioned: Optional[List[str]]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class SessionListResponse(BaseModel):
    """Schema for session list responses."""
    results: List[SessionResponse]
    pagination: Dict[str, Any]
    
    class Config:
        orm_mode = True


# Statement schemas
class StatementBase(BaseModel):
    """Base debate statement schema."""
    statement_type: StatementType
    content: str = Field(..., min_length=1)
    language: str = Field("en", regex="^(en|fr)$")
    
    @validator('content')
    def validate_content(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Statement content cannot be empty')
        return v.strip()


class StatementCreate(StatementBase):
    """Schema for creating statement."""
    session_id: UUID
    speaker_id: Optional[UUID] = None
    speaker_role: Optional[str] = None
    timestamp: Optional[time] = None
    topic: Optional[str] = None
    bill_reference: Optional[str] = None
    content_fr: Optional[str] = None
    references: Optional[Dict[str, List[str]]] = None
    interjections: Optional[List[str]] = None


class StatementUpdate(BaseModel):
    """Schema for updating statement."""
    content: Optional[str] = Field(None, min_length=1)
    content_fr: Optional[str] = None
    topic: Optional[str] = None
    bill_reference: Optional[str] = None
    references: Optional[Dict[str, List[str]]] = None


class StatementResponse(StatementBase):
    """Schema for statement responses."""
    id: UUID
    session_id: UUID
    sequence_number: int
    timestamp: Optional[time]
    speaker_id: Optional[UUID]
    speaker_name: Optional[str]  # Populated from speaker relationship
    speaker_party: Optional[str]  # Populated from speaker relationship
    speaker_riding: Optional[str]  # Populated from speaker relationship
    speaker_role: Optional[str]
    content_fr: Optional[str]
    word_count: int
    topic: Optional[str]
    bill_reference: Optional[str]
    references: Optional[Dict[str, List[str]]]
    interjections: Optional[List[str]]
    created_at: datetime
    annotation_count: int = 0
    
    class Config:
        orm_mode = True


# Speaker schemas
class SpeakerBase(BaseModel):
    """Base speaker schema."""
    name: str = Field(..., min_length=1, max_length=200)
    party: Optional[str] = Field(None, max_length=100)
    riding: Optional[str] = Field(None, max_length=200)
    province: Optional[str] = Field(None, max_length=50)
    role: Optional[str] = Field(None, max_length=100)


class SpeakerCreate(SpeakerBase):
    """Schema for creating speaker."""
    member_id: Optional[UUID] = None
    alternate_names: Optional[List[str]] = None


class SpeakerUpdate(BaseModel):
    """Schema for updating speaker."""
    party: Optional[str] = Field(None, max_length=100)
    riding: Optional[str] = Field(None, max_length=200)
    province: Optional[str] = Field(None, max_length=50)
    role: Optional[str] = Field(None, max_length=100)
    member_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class SpeakerResponse(SpeakerBase):
    """Schema for speaker responses."""
    id: UUID
    normalized_name: str
    member_id: Optional[UUID]
    total_statements: int
    total_words: int
    first_seen: Optional[date]
    last_seen: Optional[date]
    alternate_names: Optional[List[str]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Annotation schemas
class AnnotationBase(BaseModel):
    """Base annotation schema."""
    annotation_type: AnnotationType
    content: str = Field(..., min_length=1)


class AnnotationCreate(AnnotationBase):
    """Schema for creating annotation."""
    statement_id: UUID
    is_official: bool = False


class AnnotationUpdate(BaseModel):
    """Schema for updating annotation."""
    content: str = Field(..., min_length=1)


class AnnotationResponse(AnnotationBase):
    """Schema for annotation responses."""
    id: UUID
    statement_id: UUID
    created_by: UUID
    creator_name: Optional[str]  # Populated from user relationship
    is_official: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Search schemas
class SearchBase(BaseModel):
    """Base search schema."""
    name: str = Field(..., min_length=1, max_length=200)
    query: str = Field(..., min_length=1)
    filters: Dict[str, Any]


class SearchCreate(SearchBase):
    """Schema for creating saved search."""
    is_public: bool = False
    email_alerts: bool = False


class SearchUpdate(BaseModel):
    """Schema for updating saved search."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    query: Optional[str] = Field(None, min_length=1)
    filters: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None
    email_alerts: Optional[bool] = None


class SearchResponse(SearchBase):
    """Schema for search responses."""
    id: UUID
    user_id: UUID
    is_public: bool
    email_alerts: bool
    run_count: int
    last_run: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Topic schemas
class TopicBase(BaseModel):
    """Base topic schema."""
    name: str = Field(..., min_length=1, max_length=200)
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None


class TopicCreate(TopicBase):
    """Schema for creating topic."""
    keywords: Optional[List[str]] = None


class TopicUpdate(BaseModel):
    """Schema for updating topic."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    is_active: Optional[bool] = None


class TopicResponse(TopicBase):
    """Schema for topic responses."""
    id: UUID
    slug: str
    keywords: Optional[List[str]]
    mention_count: int
    first_mentioned: Optional[date]
    last_mentioned: Optional[date]
    is_active: bool
    auto_detected: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Analytics schemas
class AnalyticsResponse(BaseModel):
    """Schema for analytics responses."""
    id: UUID
    session_id: UUID
    top_words: Optional[List[Dict[str, Any]]]
    word_cloud_data: Optional[Dict[str, Any]]
    topic_distribution: Optional[Dict[str, float]]
    sentiment_scores: Optional[Dict[str, float]]
    speaker_time_distribution: Optional[Dict[str, float]]
    party_participation: Optional[Dict[str, float]]
    interruption_count: int
    question_count: int
    auto_summary: Optional[str]
    key_points: Optional[List[str]]
    computed_at: datetime
    computation_time_ms: Optional[int]
    
    class Config:
        orm_mode = True


# Filter and search request schemas
class TranscriptSearchRequest(BaseModel):
    """Schema for transcript search requests."""
    query: Optional[str] = Field(None, description="Full-text search query")
    parliament_number: Optional[int] = Field(None, ge=1, le=99)
    session_number: Optional[int] = Field(None, ge=1, le=10)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    speaker_ids: Optional[List[UUID]] = None
    speaker_names: Optional[List[str]] = None
    parties: Optional[List[str]] = None
    statement_types: Optional[List[StatementType]] = None
    topics: Optional[List[str]] = None
    bills: Optional[List[str]] = None
    
    # Pagination
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    
    # Sorting
    sort_by: str = Field("date", regex="^(date|relevance|speaker)$")
    sort_order: str = Field("desc", regex="^(asc|desc)$")
    
    @validator('end_date')
    def validate_date_range(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v


class StatementSearchResponse(BaseModel):
    """Schema for statement search responses."""
    results: List[StatementResponse]
    pagination: Dict[str, Any]
    facets: Dict[str, Dict[str, int]]  # Faceted search results
    
    class Config:
        orm_mode = True


# Import/export schemas
class TranscriptImportRequest(BaseModel):
    """Schema for importing transcripts."""
    source: str = Field(..., regex="^(parlxml|json|legacy)$")
    document_url: Optional[str] = None
    document_content: Optional[str] = None
    parliament_number: int = Field(..., ge=1, le=99)
    session_number: int = Field(..., ge=1, le=10)
    sitting_number: int = Field(..., ge=1, le=999)
    sitting_date: date
    language: str = Field("en", regex="^(en|fr)$")
    overwrite: bool = False


class TranscriptExportRequest(BaseModel):
    """Schema for exporting transcripts."""
    session_id: UUID
    format: str = Field("json", regex="^(json|xml|pdf|txt)$")
    include_annotations: bool = False
    include_analytics: bool = False