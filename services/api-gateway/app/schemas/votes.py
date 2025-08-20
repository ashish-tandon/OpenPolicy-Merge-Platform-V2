"""
Pydantic schemas for votes API.

Defines the data models for API requests and responses.
"""

from datetime import date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Pagination(BaseModel):
    """Pagination information for list responses."""
    
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total: int = Field(..., description="Total number of items")
    pages: int = Field(..., description="Total number of pages")


class VoteSummary(BaseModel):
    """Summary information about a parliamentary vote."""
    
    id: str = Field(..., description="Unique vote identifier")
    session: str = Field(..., description="Session ID (e.g., '45-1')")
    number: int = Field(..., description="Vote number in session")
    date: date = Field(..., description="Date of the vote")
    description: str = Field(..., description="Vote description")
    result: str = Field(..., description="Vote result (Passed, Failed, etc.)")
    yea_total: int = Field(..., description="Number of votes in favor")
    nay_total: int = Field(..., description="Number of votes against")
    bill_number: str = Field(..., description="Associated bill number")
    bill_title: str = Field(..., description="Associated bill title")
    
    model_config = {"from_attributes": True}


class VoteDetail(BaseModel):
    """Detailed information about a parliamentary vote."""
    
    id: str = Field(..., description="Unique vote identifier")
    session: str = Field(..., description="Session ID (e.g., '45-1')")
    number: int = Field(..., description="Vote number in session")
    date: date = Field(..., description="Date of the vote")
    description: str = Field(..., description="Vote description")
    result: str = Field(..., description="Vote result (Passed, Failed, etc.)")
    yea_total: int = Field(..., description="Number of votes in favor")
    nay_total: int = Field(..., description="Number of votes against")
    bill_number: str = Field(..., description="Associated bill number")
    bill_title: str = Field(..., description="Associated bill title")
    parties_yea: List[str] = Field(default_factory=list, description="Parties that voted in favor")
    parties_nay: List[str] = Field(default_factory=list, description="Parties that voted against")
    
    model_config = {"from_attributes": True}


class VoteBallot(BaseModel):
    """Individual MP voting record."""
    
    id: str = Field(..., description="Unique ballot identifier")
    vote_id: str = Field(..., description="Vote question identifier")
    member_name: str = Field(..., description="MP's full name")
    party_name: str = Field(..., description="MP's party name")
    constituency: str = Field(..., description="MP's electoral district")
    vote_choice: str = Field(..., description="How the MP voted (Yea, Nay, etc.)")
    
    model_config = {"from_attributes": True}


class VoteListResponse(BaseModel):
    """Response model for vote list endpoint."""
    
    votes: List[VoteSummary] = Field(..., description="List of votes")
    pagination: Pagination = Field(..., description="Pagination information")


class VoteDetailResponse(BaseModel):
    """Response model for vote detail endpoint."""
    
    vote: VoteDetail = Field(..., description="Detailed vote information")


class VoteBallotsResponse(BaseModel):
    """Response model for vote ballots endpoint."""
    
    ballots: List[VoteBallot] = Field(..., description="List of vote ballots")
    pagination: Pagination = Field(..., description="Pagination information")


class VoteSummaryResponse(BaseModel):
    """Response model for vote summary statistics."""
    
    total_votes: int = Field(..., description="Total number of votes")
    result_breakdown: Dict[str, int] = Field(..., description="Count of votes by result")
    session_breakdown: Dict[str, int] = Field(..., description="Count of votes by session")
    latest_vote_date: Optional[date] = Field(None, description="Date of most recent vote")
