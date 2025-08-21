from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class UserVoteBase(BaseModel):
    user_id: str = Field(..., description="User ID casting the vote")
    vote_choice: str = Field(..., description="Vote choice: yes, no, or abstain")
    reason: str = Field(..., description="Reason for the vote")
    confidence_level: str = Field('medium', description="Confidence level: low, medium, or high")
    constituency: Optional[str] = Field(None, description="User's constituency")
    party_preference: Optional[str] = Field(None, description="User's party preference")
    influence_factors: Optional[List[str]] = Field([], description="Factors that influenced the vote")
    related_issues: Optional[List[str]] = Field([], description="Related issues this bill addresses")
    public_visibility: str = Field('public', description="Vote visibility: public or private")
    vote_weight: float = Field(1.0, description="Weight of the vote")
    device: Optional[str] = Field(None, description="Device used for voting")
    location: Optional[str] = Field(None, description="Location where vote was cast")
    session_id: Optional[str] = Field(None, description="Session identifier")

class UserVoteCreate(UserVoteBase):
    """Schema for creating a new user vote"""
    pass

class UserVoteUpdate(BaseModel):
    """Schema for updating a user vote"""
    vote_choice: Optional[str] = Field(None, description="Updated vote choice")
    reason: Optional[str] = Field(None, description="Updated reason")
    confidence_level: Optional[str] = Field(None, description="Updated confidence level")
    constituency: Optional[str] = Field(None, description="Updated constituency")
    party_preference: Optional[str] = Field(None, description="Updated party preference")
    influence_factors: Optional[List[str]] = Field(None, description="Updated influence factors")
    related_issues: Optional[List[str]] = Field(None, description="Updated related issues")
    public_visibility: Optional[str] = Field(None, description="Updated visibility")
    vote_weight: Optional[float] = Field(None, description="Updated vote weight")

class UserVoteResponse(UserVoteBase):
    """Schema for user vote response"""
    id: UUID = Field(..., description="Unique identifier for the vote")
    bill_id: str = Field(..., description="Bill ID the vote was cast on")
    vote_date: datetime = Field(..., description="When the vote was cast")
    updated_at: Optional[datetime] = Field(None, description="When the vote was last updated")
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }

class UserVoteListResponse(BaseModel):
    """Schema for paginated list of user votes"""
    results: List[UserVoteResponse] = Field(..., description="List of user votes")
    total_count: int = Field(..., description="Total number of votes")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of votes per page")
    total_pages: int = Field(..., description="Total number of pages")

class BillVoteSummaryResponse(BaseModel):
    """Schema for bill voting summary"""
    bill_id: str = Field(..., description="Bill ID for the summary")
    overall_statistics: dict = Field(..., description="Overall voting statistics")
    constituency_breakdown: dict = Field(..., description="Constituency-based voting breakdown")
    demographic_breakdown: dict = Field(..., description="Demographic voting breakdown")
    voting_trends: dict = Field(..., description="Voting trends and patterns")

class VotingRecommendation(BaseModel):
    """Schema for voting recommendations"""
    type: str = Field(..., description="Type of recommendation")
    message: str = Field(..., description="Recommendation message")
    confidence: str = Field(..., description="Confidence level of recommendation")

class VotingRecommendationsResponse(BaseModel):
    """Schema for voting recommendations response"""
    user_id: str = Field(..., description="User ID for recommendations")
    total_votes: int = Field(..., description="Total number of votes cast")
    voting_pattern: dict = Field(..., description="User's voting pattern analysis")
    recommendations: List[VotingRecommendation] = Field(..., description="List of recommendations")

class VoteAnalytics(BaseModel):
    """Schema for vote analytics data"""
    bill_id: str = Field(..., description="Bill ID for analytics")
    total_votes: int = Field(..., description="Total votes cast")
    yes_percentage: float = Field(..., description="Percentage of yes votes")
    no_percentage: float = Field(..., description="Percentage of no votes")
    abstain_percentage: float = Field(..., description="Percentage of abstentions")
    constituency_coverage: float = Field(..., description="Percentage of constituencies with votes")
    peak_voting_time: str = Field(..., description="Peak voting time")
    voting_momentum: str = Field(..., description="Voting momentum description")
