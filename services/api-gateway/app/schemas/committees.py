"""
Pydantic schemas for committees API.

Defines the data models for API requests and responses.
Adapted from legacy OpenParliament committees functionality.
"""

from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class Pagination(BaseModel):
    """Pagination information for list responses."""
    
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total: int = Field(..., description="Total number of items")
    pages: int = Field(..., description="Total number of pages")


class CommitteeSummary(BaseModel):
    """Summary information about a parliamentary committee."""
    
    id: str = Field(..., description="Unique committee identifier")
    name: str = Field(..., description="Full committee name")
    short_name: str = Field(..., description="Committee abbreviation")
    active: bool = Field(..., description="Whether the committee is active")
    meeting_count: int = Field(..., description="Number of meetings held")
    url: str = Field(..., description="URL to committee detail")
    
    model_config = {"from_attributes": True}


class MeetingSummary(BaseModel):
    """Summary information about a committee meeting."""
    
    id: str = Field(..., description="Unique meeting identifier")
    committee_name: str = Field(..., description="Committee name")
    committee_slug: str = Field(..., description="Committee slug")
    date: Optional[str] = Field(None, description="Meeting date (YYYY-MM-DD)")
    number: int = Field(..., description="Meeting number in session")
    session_id: str = Field(..., description="Session identifier")
    has_evidence: bool = Field(..., description="Whether meeting has transcripts")
    url: str = Field(..., description="URL to meeting detail")
    
    model_config = {"from_attributes": True}
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        if v is not None:
            try:
                return date.fromisoformat(v)
            except ValueError:
                raise ValueError('Invalid date format. Use YYYY-MM-DD')
        return v


class CommitteeDetail(BaseModel):
    """Detailed information about a parliamentary committee."""
    
    id: str = Field(..., description="Unique committee identifier")
    name: str = Field(..., description="Full committee name")
    short_name: str = Field(..., description="Committee abbreviation")
    active: bool = Field(..., description="Whether the committee is active")
    meeting_count: int = Field(..., description="Number of meetings held")
    member_count: int = Field(..., description="Number of committee members")
    recent_meetings: List[MeetingSummary] = Field(default_factory=list, description="Recent meetings")
    url: str = Field(..., description="URL to committee detail")
    
    model_config = {"from_attributes": True}


class MeetingDetail(BaseModel):
    """Detailed information about a committee meeting."""
    
    id: str = Field(..., description="Unique meeting identifier")
    committee_name: str = Field(..., description="Committee name")
    committee_slug: str = Field(..., description="Committee slug")
    date: Optional[str] = Field(None, description="Meeting date (YYYY-MM-DD)")
    number: int = Field(..., description="Meeting number in session")
    session_id: str = Field(..., description="Session identifier")
    has_evidence: bool = Field(..., description="Whether meeting has transcripts")
    evidence_url: Optional[str] = Field(None, description="URL to meeting transcripts")
    witness_count: int = Field(default=0, description="Number of witnesses")
    statement_count: int = Field(default=0, description="Number of statements")
    url: str = Field(..., description="URL to meeting detail")
    
    model_config = {"from_attributes": True}
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        if v is not None:
            try:
                return date.fromisoformat(v)
            except ValueError:
                raise ValueError('Invalid date format. Use YYYY-MM-DD')
        return v


class CommitteeListResponse(BaseModel):
    """Response model for committee list endpoint."""
    
    committees: List[CommitteeSummary] = Field(..., description="List of committees")
    pagination: Pagination = Field(..., description="Pagination information")


class CommitteeDetailResponse(BaseModel):
    """Response model for committee detail endpoint."""
    
    committee: CommitteeDetail = Field(..., description="Detailed committee information")


class MeetingListResponse(BaseModel):
    """Response model for committee meeting list endpoint."""
    
    meetings: List[MeetingSummary] = Field(..., description="List of meetings")
    pagination: Pagination = Field(..., description="Pagination information")


class MeetingDetailResponse(BaseModel):
    """Response model for committee meeting detail endpoint."""
    
    meeting: MeetingDetail = Field(..., description="Detailed meeting information")


class CommitteeSummaryResponse(BaseModel):
    """Response model for committee summary statistics."""
    
    total_committees: int = Field(..., description="Total number of committees")
    active_committees: int = Field(..., description="Number of active committees")
    total_meetings: int = Field(..., description="Total number of meetings")
    recent_meetings: int = Field(..., description="Number of recent meetings")
    latest_meeting_date: Optional[str] = Field(None, description="Date of most recent meeting (YYYY-MM-DD)")
