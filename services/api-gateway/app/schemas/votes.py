"""
Pydantic schemas for votes API.

Defines the data models for API requests and responses.
"""

from datetime import date
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict


class Pagination(BaseModel):
    """Pagination information for list responses."""
    
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total: int = Field(..., description="Total number of items")
    pages: int = Field(..., description="Total number of pages")


class VoteSummary(BaseModel):
    """Summary information about a parliamentary vote."""
    
    vote_id: str = Field(..., description="Unique vote identifier")
    session: str = Field(..., description="Session ID (e.g., '45-1')")
    number: int = Field(..., description="Vote number in session")
    vote_date: date = Field(..., description="Date of the vote")
    description: str = Field(..., description="Vote description")
    description_en: str = Field(..., description="Vote description in English")
    description_fr: str = Field(..., description="Vote description in French")
    result: str = Field(..., description="Vote result (Passed, Failed, etc.)")
    yea_total: int = Field(..., description="Number of votes in favor")
    nay_total: int = Field(..., description="Number of votes against")
    paired_count: int = Field(0, description="Number of paired votes")
    absent_count: int = Field(0, description="Number of absent votes")
    bill_number: str = Field(..., description="Associated bill number")
    bill_title: str = Field(..., description="Associated bill title")
    
    model_config = ConfigDict(from_attributes=True)


class VoteDetail(BaseModel):
    """Detailed information about a parliamentary vote."""
    
    vote_id: str = Field(..., description="Unique vote identifier")
    session: str = Field(..., description="Session ID (e.g., '45-1')")
    number: int = Field(..., description="Vote number in session")
    vote_date: date = Field(..., description="Date of the vote")
    description: str = Field(..., description="Vote description")
    description_en: str = Field(..., description="Vote description in English")
    description_fr: str = Field(..., description="Vote description in French")
    result: str = Field(..., description="Vote result (Passed, Failed, etc.)")
    yea_total: int = Field(..., description="Number of votes in favor")
    nay_total: int = Field(..., description="Number of votes against")
    paired_count: int = Field(0, description="Number of paired votes")
    absent_count: int = Field(0, description="Number of absent votes")
    bill_number: str = Field(..., description="Associated bill number")
    bill_title: str = Field(..., description="Associated bill title")
    parties_yea: List[str] = Field(default_factory=list, description="Parties that voted in favor")
    parties_nay: List[str] = Field(default_factory=list, description="Parties that voted against")
    
    model_config = ConfigDict(from_attributes=True)


class VoteBallot(BaseModel):
    """Individual MP voting record."""
    
    ballot_id: str = Field(..., description="Unique ballot identifier")
    vote_id: str = Field(..., description="Vote question identifier")
    member_name: str = Field(..., description="MP's full name")
    party_name: str = Field(..., description="MP's party name")
    constituency: str = Field(..., description="MP's electoral district")
    vote_choice: str = Field(..., description="How the MP voted (Yea, Nay, etc.)")
    
    # Enhanced MP position analysis
    party_position: Optional[str] = Field(None, description="Official party position on this vote")
    voted_with_party: bool = Field(..., description="Whether MP voted with their party")
    government_position: Optional[str] = Field(None, description="Government's official position")
    voted_with_government: bool = Field(..., description="Whether MP voted with government")
    whip_status: Optional[str] = Field(None, description="Whether this was a whipped vote")
    dissent_reason: Optional[str] = Field(None, description="Reason for dissenting from party line")
    constituency_impact: Optional[str] = Field(None, description="How this vote affects the MP's constituency")
    
    model_config = ConfigDict(from_attributes=True)


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


class MPVotePosition(BaseModel):
    """MP's voting position and analysis."""
    
    member_id: str = Field(..., description="MP identifier")
    member_name: str = Field(..., description="MP's full name")
    party_name: str = Field(..., description="MP's party")
    constituency: str = Field(..., description="MP's constituency")
    vote_choice: str = Field(..., description="How the MP voted")
    party_position: str = Field(..., description="Official party position")
    voted_with_party: bool = Field(..., description="Whether MP voted with party")
    government_position: str = Field(..., description="Government position")
    voted_with_government: bool = Field(..., description="Whether MP voted with government")
    whip_status: str = Field(..., description="Whip status for this vote")
    dissent_impact: Optional[str] = Field(None, description="Impact of dissenting vote")
    
    model_config = ConfigDict(from_attributes=True)


class VoteAnalysis(BaseModel):
    """Comprehensive vote analysis."""
    
    vote_id: str = Field(..., description="Vote identifier")
    total_members: int = Field(..., description="Total MPs eligible to vote")
    votes_cast: int = Field(..., description="Number of votes actually cast")
    yea_votes: int = Field(..., description="Votes in favor")
    nay_votes: int = Field(..., description="Votes against")
    absent_votes: int = Field(..., description="Absent members")
    paired_votes: int = Field(..., description="Paired votes")
    
    # Party analysis
    party_breakdown: Dict[str, Dict[str, int]] = Field(..., description="Votes by party")
    party_unity_scores: Dict[str, float] = Field(..., description="Party unity percentages")
    
    # Government vs Opposition
    government_support: float = Field(..., description="Government support percentage")
    opposition_support: float = Field(..., description="Opposition support percentage")
    
    # Dissent analysis
    party_dissents: List[MPVotePosition] = Field(default_factory=list, description="MPs who broke party line")
    cross_party_supporters: List[MPVotePosition] = Field(default_factory=list, description="Cross-party supporters")
    
    # Regional analysis
    regional_breakdown: Dict[str, Dict[str, int]] = Field(default_factory=dict, description="Votes by region")
    
    model_config = ConfigDict(from_attributes=True)


class VoteAnalysisResponse(BaseModel):
    """Response model for comprehensive vote analysis."""
    
    analysis: VoteAnalysis = Field(..., description="Vote analysis information")


class RealTimeVoteUpdate(BaseModel):
    """Real-time vote update for WebSocket."""
    
    vote_id: str = Field(..., description="Vote identifier")
    update_type: str = Field(..., description="Type of update (cast, change, final)")
    member_id: Optional[str] = Field(None, description="Member who cast/changed vote")
    vote_choice: Optional[str] = Field(None, description="New vote choice")
    current_totals: Dict[str, int] = Field(..., description="Current vote totals")
    timestamp: str = Field(..., description="Update timestamp")
    
    model_config = ConfigDict(from_attributes=True)


class UserVoteCast(BaseModel):
    """User vote casting request."""
    
    vote_choice: str = Field(..., description="User's vote choice (Yea, Nay, Abstain)")
    reasoning: Optional[str] = Field(None, description="User's reasoning for their vote")
    
    model_config = ConfigDict(from_attributes=True)


class UserVoteResponse(BaseModel):
    """Response for user vote casting."""
    
    success: bool = Field(..., description="Whether vote was successfully cast")
    vote_id: str = Field(..., description="Vote identifier")
    user_choice: str = Field(..., description="User's vote choice")
    message: str = Field(..., description="Success/error message")
    
    model_config = ConfigDict(from_attributes=True)
