"""
Pydantic schemas for members API.

Defines the data models for API requests and responses.
"""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class Pagination(BaseModel):
    """Pagination information for list responses."""
    
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total: int = Field(..., description="Total number of items")
    pages: int = Field(..., description="Total number of pages")


class MemberSummary(BaseModel):
    """Summary information about a Member of Parliament."""
    
    id: str = Field(..., description="Unique member identifier")
    full_name: str = Field(..., description="Full name of the MP")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    party_name: str = Field(..., description="Political party name")
    party_slug: str = Field(..., description="Party slug")
    constituency: Optional[str] = Field(None, description="Electoral district/riding")
    province: Optional[str] = Field(None, description="Province")
    is_current: bool = Field(..., description="Whether the MP is currently serving")
    start_date: date = Field(..., description="Start date of service")
    end_date: Optional[date] = Field(None, description="End date of service")
    
    model_config = {"from_attributes": True}


class MemberDetail(BaseModel):
    """Detailed information about a Member of Parliament."""
    
    id: str = Field(..., description="Unique member identifier")
    full_name: str = Field(..., description="Full name of the MP")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    party_name: str = Field(..., description="Political party name")
    party_slug: str = Field(..., description="Party slug")
    constituency: Optional[str] = Field(None, description="Electoral district/riding")
    province: Optional[str] = Field(None, description="Electoral district/riding")
    is_current: bool = Field(..., description="Whether the MP is currently serving")
    start_date: date = Field(..., description="Start date of service")
    end_date: Optional[date] = Field(None, description="End date of service")
    sponsored_bills_count: int = Field(..., description="Number of bills sponsored")
    recent_votes_count: int = Field(..., description="Number of recent votes")
    
    model_config = {"from_attributes": True}


class MemberSuggestionsResponse(BaseModel):
    """Response model for member suggestions."""
    
    suggestions: List[dict] = Field(..., description="List of member suggestions")


class MemberListResponse(BaseModel):
    """Response model for member list endpoint."""
    
    members: List[MemberSummary] = Field(..., description="List of members")
    pagination: Pagination = Field(..., description="Pagination information")


class MemberDetailResponse(BaseModel):
    """Response model for member detail endpoint."""
    
    member: MemberDetail = Field(..., description="Detailed member information")


class MemberSummaryResponse(BaseModel):
    """Response model for member summary statistics."""
    
    total_members: int = Field(..., description="Total number of members")
    current_members: int = Field(..., description="Number of current members")
    party_breakdown: dict = Field(..., description="Count of members by party")
    province_breakdown: dict = Field(..., description="Count of members by province")
    top_sponsors: List[dict] = Field(..., description="Top bill sponsors")
