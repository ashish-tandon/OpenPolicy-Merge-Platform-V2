"""
Pydantic schemas for bills API.

Defines the data models for API requests and responses.
"""

from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Pagination(BaseModel):
    """Pagination information for list responses."""
    
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total: int = Field(..., description="Total number of items")
    pages: int = Field(..., description="Total number of pages")


class BillSummary(BaseModel):
    """Summary information about a bill."""
    
    id: str = Field(..., description="Unique bill identifier")
    bill_number: str = Field(..., description="Bill number (e.g., C-123)")
    title: str = Field(..., description="Bill title")
    short_title: Optional[str] = Field(None, description="Short title if available")
    summary: Optional[str] = Field(None, description="Bill summary")
    status: str = Field(..., description="Current bill status")
    introduced_date: Optional[date] = Field(None, description="Date bill was introduced")
    sponsor_name: Optional[str] = Field(None, description="Name of the sponsor")
    party_name: Optional[str] = Field(None, description="Party of the sponsor")
    session_name: Optional[str] = Field(None, description="Parliament session name")
    keywords: List[str] = Field(default_factory=list, description="Keywords for the bill")
    tags: List[str] = Field(default_factory=list, description="Tags for the bill")
    
    model_config = {"from_attributes": True}


class VoteInfo(BaseModel):
    """Information about a parliamentary vote."""
    
    vote_id: str = Field(..., description="Vote identifier")
    vote_date: date = Field(..., description="Date of the vote")
    description: str = Field(..., description="Description of the vote")
    result: str = Field(..., description="Vote result (Passed, Defeated, Tied)")
    
    model_config = {"from_attributes": True}


class BillDetail(BaseModel):
    """Detailed information about a bill."""
    
    id: str = Field(..., description="Unique bill identifier")
    bill_number: str = Field(..., description="Bill number (e.g., C-123)")
    title: str = Field(..., description="Bill title")
    short_title: Optional[str] = Field(None, description="Short title if available")
    summary: Optional[str] = Field(None, description="Bill summary")
    status: str = Field(..., description="Current bill status")
    introduced_date: Optional[date] = Field(None, description="Date bill was introduced")
    sponsor_name: Optional[str] = Field(None, description="Name of the sponsor")
    party_name: Optional[str] = Field(None, description="Party of the sponsor")
    riding_name: Optional[str] = Field(None, description="Electoral district of the sponsor")
    session_id: str = Field(None, description="Session identifier")
    institution: str = Field(..., description="Institution (H for House, S for Senate)")
    votes: List[VoteInfo] = Field(default_factory=list, description="Voting records")
    
    # Enhanced status tracking
    current_stage: Optional[str] = Field(None, description="Current legislative stage")
    stage_progress: Optional[float] = Field(None, description="Progress through stages (0.0-1.0)")
    next_stage: Optional[str] = Field(None, description="Next expected stage")
    estimated_completion: Optional[date] = Field(None, description="Estimated completion date")
    
    # LEGISinfo integration
    legisinfo_id: Optional[int] = Field(None, description="LEGISinfo identifier")
    library_summary: Optional[str] = Field(None, description="Library of Parliament summary")
    
    # Bill lifecycle
    last_activity_date: Optional[date] = Field(None, description="Date of last legislative activity")
    days_in_current_stage: Optional[int] = Field(None, description="Days spent in current stage")
    total_legislative_days: Optional[int] = Field(None, description="Total days since introduction")
    
    model_config = {"from_attributes": True}


class BillSuggestionsResponse(BaseModel):
    """Response model for bill suggestions."""
    
    suggestions: List[dict] = Field(..., description="List of bill suggestions")


class BillListResponse(BaseModel):
    """Response model for bill list endpoint."""
    
    bills: List[BillSummary] = Field(..., description="List of bills")
    pagination: Pagination = Field(..., description="Pagination information")


class BillDetailResponse(BaseModel):
    """Response model for bill detail endpoint."""
    
    bill: BillDetail = Field(..., description="Detailed bill information")


class BillSummaryResponse(BaseModel):
    """Response model for bill summary statistics."""
    
    total_bills: int = Field(..., description="Total number of bills")
    status_breakdown: dict = Field(..., description="Count of bills by status")
    session_breakdown: dict = Field(..., description="Count of bills by session")


class BillStage(BaseModel):
    """Information about a legislative stage."""
    
    stage: str = Field(..., description="Stage identifier")
    title: str = Field(..., description="Stage title")
    description: str = Field(..., description="Stage description")
    status: str = Field(..., description="Stage status (completed, in_progress, pending)")
    start_date: Optional[date] = Field(None, description="Stage start date")
    end_date: Optional[date] = Field(None, description="Stage end date")
    duration_days: Optional[int] = Field(None, description="Duration in days")
    order: int = Field(..., description="Stage order in legislative process")
    
    model_config = {"from_attributes": True}


class BillStatus(BaseModel):
    """Comprehensive bill status information."""
    
    bill_id: str = Field(..., description="Bill identifier")
    current_stage: str = Field(..., description="Current legislative stage")
    stage_progress: float = Field(..., description="Progress through stages (0.0-1.0)")
    next_stage: Optional[str] = Field(None, description="Next expected stage")
    estimated_completion: Optional[date] = Field(None, description="Estimated completion date")
    last_activity_date: Optional[date] = Field(None, description="Date of last legislative activity")
    days_in_current_stage: int = Field(..., description="Days spent in current stage")
    total_legislative_days: int = Field(..., description="Total days since introduction")
    stages: List[BillStage] = Field(default_factory=list, description="All legislative stages")
    
    model_config = {"from_attributes": True}


class BillStatusResponse(BaseModel):
    """Response model for comprehensive bill status."""
    
    status: BillStatus = Field(..., description="Bill status information")


class BillTimeline(BaseModel):
    """Detailed bill timeline with stages and events."""
    
    bill_id: str = Field(..., description="Bill identifier")
    bill_number: str = Field(..., description="Bill number")
    bill_title: str = Field(..., description="Bill title")
    current_stage: str = Field(..., description="Current legislative stage")
    timeline: List[BillStage] = Field(default_factory=list, description="Timeline events")
    summary: dict = Field(..., description="Timeline summary statistics")
    last_updated: str = Field(..., description="Last update timestamp")
    
    model_config = {"from_attributes": True}


class BillTimelineResponse(BaseModel):
    """Response model for bill timeline."""
    
    timeline: BillTimeline = Field(..., description="Bill timeline information")
