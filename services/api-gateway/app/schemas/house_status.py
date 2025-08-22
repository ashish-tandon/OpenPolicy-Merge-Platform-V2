"""
House Status Schemas for OpenPolicy V2

Comprehensive Pydantic schemas for real-time parliamentary house status,
session information, voting status, and live updates.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class HouseStatusEnum(str, Enum):
    """House status enumeration."""
    SITTING = "sitting"
    ADJOURNED = "adjourned"
    PROROGUED = "prorogued"
    DISSOLVED = "dissolved"


class SittingStatusEnum(str, Enum):
    """Sitting status enumeration."""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    SUSPENDED = "suspended"
    ADJOURNED = "adjourned"


class VotingStatusEnum(str, Enum):
    """Voting status enumeration."""
    NONE = "none"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class DebateStatusEnum(str, Enum):
    """Debate status enumeration."""
    NONE = "none"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ADJOURNED = "adjourned"


class VoteTypeEnum(str, Enum):
    """Vote type enumeration."""
    DIVISION = "division"
    VOICE_VOTE = "voice_vote"
    UNANIMOUS_CONSENT = "unanimous_consent"


class VoteResultEnum(str, Enum):
    """Vote result enumeration."""
    PASSED = "passed"
    DEFEATED = "defeated"
    TIED = "tied"


class IndividualVoteEnum(str, Enum):
    """Individual vote enumeration."""
    YEA = "yea"
    NAY = "nay"
    ABSTAIN = "abstain"
    ABSENT = "absent"


class DebateTypeEnum(str, Enum):
    """Debate type enumeration."""
    GOVERNMENT_BUSINESS = "government_business"
    OPPOSITION_DAY = "opposition_day"
    PRIVATE_MEMBERS = "private_members"
    EMERGENCY_DEBATE = "emergency_debate"


class EventPriorityEnum(str, Enum):
    """Event priority enumeration."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class QuestionPeriodStatusEnum(str, Enum):
    """Question period status enumeration."""
    NONE = "none"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


# ============================================================================
# BASE MODELS
# ============================================================================

class HouseSessionBase(BaseModel):
    """Base model for house sessions."""
    model_config = ConfigDict(from_attributes=True)
    
    session_number: int = Field(..., description="Session number")
    session_name: str = Field(..., description="Session name")
    parliament_number: int = Field(..., description="Parliament number")
    start_date: datetime = Field(..., description="Session start date")
    end_date: Optional[datetime] = Field(None, description="Session end date")
    is_active: bool = Field(True, description="Whether session is active")
    status: HouseStatusEnum = Field(HouseStatusEnum.SITTING, description="Session status")
    government_party: Optional[str] = Field(None, description="Government party")
    opposition_leader: Optional[str] = Field(None, description="Opposition leader")
    speaker: Optional[str] = Field(None, description="House speaker")


class HouseSittingBase(BaseModel):
    """Base model for house sittings."""
    model_config = ConfigDict(from_attributes=True)
    
    session_id: str = Field(..., description="Session ID")
    sitting_number: int = Field(..., description="Sitting number")
    sitting_date: datetime = Field(..., description="Sitting date")
    start_time: Optional[datetime] = Field(None, description="Sitting start time")
    end_time: Optional[datetime] = Field(None, description="Sitting end time")
    is_active: bool = Field(True, description="Whether sitting is active")
    status: SittingStatusEnum = Field(SittingStatusEnum.SCHEDULED, description="Sitting status")
    quorum_present: bool = Field(True, description="Whether quorum is present")
    members_present: int = Field(0, description="Number of members present")
    total_members: int = Field(338, description="Total number of members")
    agenda_items: Optional[Dict[str, Any]] = Field(None, description="Agenda items")
    notes: Optional[str] = Field(None, description="Sitting notes")


class HouseVoteBase(BaseModel):
    """Base model for house votes."""
    model_config = ConfigDict(from_attributes=True)
    
    session_id: str = Field(..., description="Session ID")
    sitting_id: Optional[str] = Field(None, description="Sitting ID")
    vote_number: int = Field(..., description="Vote number")
    bill_id: Optional[str] = Field(None, description="Related bill ID")
    motion_text: str = Field(..., description="Motion text")
    vote_type: VoteTypeEnum = Field(..., description="Vote type")
    status: VotingStatusEnum = Field(VotingStatusEnum.SCHEDULED, description="Vote status")
    start_time: Optional[datetime] = Field(None, description="Vote start time")
    end_time: Optional[datetime] = Field(None, description="Vote end time")
    duration_minutes: Optional[int] = Field(None, description="Vote duration in minutes")
    total_votes_cast: int = Field(0, description="Total votes cast")
    yeas: int = Field(0, description="Number of yea votes")
    nays: int = Field(0, description="Number of nay votes")
    abstentions: int = Field(0, description="Number of abstentions")
    result: Optional[VoteResultEnum] = Field(None, description="Vote result")
    requires_royal_assent: bool = Field(False, description="Whether royal assent is required")
    royal_assent_date: Optional[datetime] = Field(None, description="Royal assent date")
    vote_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class IndividualVoteBase(BaseModel):
    """Base model for individual votes."""
    model_config = ConfigDict(from_attributes=True)
    
    house_vote_id: str = Field(..., description="House vote ID")
    member_id: str = Field(..., description="Member ID")
    member_name: str = Field(..., description="Member name")
    party: str = Field(..., description="Member party")
    riding: str = Field(..., description="Member riding")
    vote_cast: IndividualVoteEnum = Field(..., description="Vote cast")
    vote_time: Optional[datetime] = Field(None, description="When vote was cast")
    is_paired: bool = Field(False, description="Whether vote is paired")
    paired_with: Optional[str] = Field(None, description="Paired with member")
    whip_status: Optional[str] = Field(None, description="Whip status")


class HouseDebateBase(BaseModel):
    """Base model for house debates."""
    model_config = ConfigDict(from_attributes=True)
    
    session_id: str = Field(..., description="Session ID")
    sitting_id: Optional[str] = Field(None, description="Sitting ID")
    debate_type: DebateTypeEnum = Field(..., description="Debate type")
    subject: str = Field(..., description="Debate subject")
    bill_id: Optional[str] = Field(None, description="Related bill ID")
    status: DebateStatusEnum = Field(DebateStatusEnum.SCHEDULED, description="Debate status")
    start_time: Optional[datetime] = Field(None, description="Debate start time")
    end_time: Optional[datetime] = Field(None, description="Debate end time")
    current_speaker: Optional[str] = Field(None, description="Current speaker")
    time_allocation_minutes: Optional[int] = Field(None, description="Time allocation in minutes")
    time_used_minutes: Optional[int] = Field(None, description="Time used in minutes")
    speakers_list: Optional[List[Dict[str, Any]]] = Field(None, description="List of scheduled speakers")
    current_amendment: Optional[str] = Field(None, description="Current amendment")
    closure_motion: bool = Field(False, description="Whether closure motion is active")


class HouseStatusBase(BaseModel):
    """Base model for house status."""
    model_config = ConfigDict(from_attributes=True)
    
    current_session_id: Optional[str] = Field(None, description="Current session ID")
    current_sitting_id: Optional[str] = Field(None, description="Current sitting ID")
    current_vote_id: Optional[str] = Field(None, description="Current vote ID")
    current_debate_id: Optional[str] = Field(None, description="Current debate ID")
    house_status: HouseStatusEnum = Field(HouseStatusEnum.SITTING, description="House status")
    sitting_status: SittingStatusEnum = Field(SittingStatusEnum.IN_PROGRESS, description="Sitting status")
    voting_status: VotingStatusEnum = Field(VotingStatusEnum.NONE, description="Voting status")
    debate_status: DebateStatusEnum = Field(DebateStatusEnum.NONE, description="Debate status")
    members_present: int = Field(0, description="Number of members present")
    quorum_met: bool = Field(True, description="Whether quorum is met")
    current_time: datetime = Field(..., description="Current time")
    next_scheduled_event: Optional[str] = Field(None, description="Next scheduled event")
    next_event_time: Optional[datetime] = Field(None, description="Next event time")
    question_period_status: QuestionPeriodStatusEnum = Field(QuestionPeriodStatusEnum.NONE, description="Question period status")
    emergency_debate_requested: bool = Field(False, description="Whether emergency debate is requested")
    closure_motion_active: bool = Field(False, description="Whether closure motion is active")
    update_source: str = Field("system", description="Update source")
    notes: Optional[str] = Field(None, description="Additional notes")


class HouseEventBase(BaseModel):
    """Base model for house events."""
    model_config = ConfigDict(from_attributes=True)
    
    event_type: str = Field(..., description="Event type")
    event_title: str = Field(..., description="Event title")
    event_description: Optional[str] = Field(None, description="Event description")
    event_time: datetime = Field(..., description="Event time")
    session_id: Optional[str] = Field(None, description="Related session ID")
    sitting_id: Optional[str] = Field(None, description="Related sitting ID")
    related_bill_id: Optional[str] = Field(None, description="Related bill ID")
    related_vote_id: Optional[str] = Field(None, description="Related vote ID")
    related_debate_id: Optional[str] = Field(None, description="Related debate ID")
    priority: EventPriorityEnum = Field(EventPriorityEnum.NORMAL, description="Event priority")
    requires_notification: bool = Field(True, description="Whether notification is required")
    notification_sent: bool = Field(False, description="Whether notification was sent")
    event_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


# ============================================================================
# REQUEST MODELS
# ============================================================================

class HouseSessionCreateRequest(HouseSessionBase):
    """Request model for creating house sessions."""
    pass


class HouseSessionUpdateRequest(BaseModel):
    """Request model for updating house sessions."""
    session_name: Optional[str] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    status: Optional[HouseStatusEnum] = None
    government_party: Optional[str] = None
    opposition_leader: Optional[str] = None
    speaker: Optional[str] = None


class HouseSittingCreateRequest(HouseSittingBase):
    """Request model for creating house sittings."""
    pass


class HouseSittingUpdateRequest(BaseModel):
    """Request model for updating house sittings."""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_active: Optional[bool] = None
    status: Optional[SittingStatusEnum] = None
    quorum_present: Optional[bool] = None
    members_present: Optional[int] = None
    agenda_items: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


class HouseVoteCreateRequest(HouseVoteBase):
    """Request model for creating house votes."""
    pass


class HouseVoteUpdateRequest(BaseModel):
    """Request model for updating house votes."""
    sitting_id: Optional[str] = None
    bill_id: Optional[str] = None
    motion_text: Optional[str] = None
    vote_type: Optional[VoteTypeEnum] = None
    status: Optional[VotingStatusEnum] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    total_votes_cast: Optional[int] = None
    yeas: Optional[int] = None
    nays: Optional[int] = None
    abstentions: Optional[int] = None
    result: Optional[VoteResultEnum] = None
    requires_royal_assent: Optional[bool] = None
    royal_assent_date: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class IndividualVoteCreateRequest(IndividualVoteBase):
    """Request model for creating individual votes."""
    pass


class IndividualVoteUpdateRequest(BaseModel):
    """Request model for updating individual votes."""
    vote_cast: Optional[IndividualVoteEnum] = None
    vote_time: Optional[datetime] = None
    is_paired: Optional[bool] = None
    paired_with: Optional[str] = None
    whip_status: Optional[str] = None


class HouseDebateCreateRequest(HouseDebateBase):
    """Request model for creating house debates."""
    pass


class HouseDebateUpdateRequest(BaseModel):
    """Request model for updating house debates."""
    sitting_id: Optional[str] = None
    bill_id: Optional[str] = None
    subject: Optional[str] = None
    status: Optional[DebateStatusEnum] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    current_speaker: Optional[str] = None
    time_allocation_minutes: Optional[int] = None
    time_used_minutes: Optional[int] = None
    speakers_list: Optional[List[Dict[str, Any]]] = None
    current_amendment: Optional[str] = None
    closure_motion: Optional[bool] = None


class HouseStatusUpdateRequest(BaseModel):
    """Request model for updating house status."""
    current_session_id: Optional[str] = None
    current_sitting_id: Optional[str] = None
    current_vote_id: Optional[str] = None
    current_debate_id: Optional[str] = None
    house_status: Optional[HouseStatusEnum] = None
    sitting_status: Optional[SittingStatusEnum] = None
    voting_status: Optional[VotingStatusEnum] = None
    debate_status: Optional[DebateStatusEnum] = None
    members_present: Optional[int] = None
    quorum_met: Optional[bool] = None
    next_scheduled_event: Optional[str] = None
    next_event_time: Optional[datetime] = None
    question_period_status: Optional[QuestionPeriodStatusEnum] = None
    emergency_debate_requested: Optional[bool] = None
    closure_motion_active: Optional[bool] = None
    notes: Optional[str] = None


class HouseEventCreateRequest(HouseEventBase):
    """Request model for creating house events."""
    pass


class HouseEventUpdateRequest(BaseModel):
    """Request model for updating house events."""
    event_title: Optional[str] = None
    event_description: Optional[str] = None
    event_time: Optional[datetime] = None
    priority: Optional[EventPriorityEnum] = None
    requires_notification: Optional[bool] = None
    notification_sent: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class HouseSessionResponse(HouseSessionBase):
    """Response model for house sessions."""
    id: str
    created_at: datetime
    updated_at: datetime


class HouseSittingResponse(HouseSittingBase):
    """Response model for house sittings."""
    id: str
    created_at: datetime
    updated_at: datetime


class HouseVoteResponse(HouseVoteBase):
    """Response model for house votes."""
    id: str
    created_at: datetime
    updated_at: datetime


class IndividualVoteResponse(IndividualVoteBase):
    """Response model for individual votes."""
    id: str
    created_at: datetime


class HouseDebateResponse(HouseDebateBase):
    """Response model for house debates."""
    id: str
    created_at: datetime
    updated_at: datetime


class HouseStatusResponse(HouseStatusBase):
    """Response model for house status."""
    id: str
    last_updated: datetime


class HouseEventResponse(HouseEventBase):
    """Response model for house events."""
    id: str
    created_at: datetime
    updated_at: datetime


# ============================================================================
# LIST RESPONSE MODELS
# ============================================================================

class HouseSessionListResponse(BaseModel):
    """List response model for house sessions."""
    sessions: List[HouseSessionResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class HouseSittingListResponse(BaseModel):
    """List response model for house sittings."""
    sittings: List[HouseSittingResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class HouseVoteListResponse(BaseModel):
    """List response model for house votes."""
    votes: List[HouseVoteResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class IndividualVoteListResponse(BaseModel):
    """List response model for individual votes."""
    votes: List[IndividualVoteResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class HouseDebateListResponse(BaseModel):
    """List response model for house debates."""
    debates: List[HouseDebateResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class HouseEventListResponse(BaseModel):
    """List response model for house events."""
    events: List[HouseEventResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


# ============================================================================
# WEBSOCKET AND REAL-TIME MODELS
# ============================================================================

class HouseStatusUpdate(BaseModel):
    """Model for real-time house status updates."""
    event_type: str = Field(..., description="Type of update")
    timestamp: datetime = Field(..., description="Update timestamp")
    house_status: HouseStatusResponse = Field(..., description="Updated house status")
    changes: Dict[str, Any] = Field(..., description="What changed")
    source: str = Field(..., description="Update source")


class VoteProgressUpdate(BaseModel):
    """Model for real-time vote progress updates."""
    event_type: str = Field(..., description="Type of update")
    timestamp: datetime = Field(..., description="Update timestamp")
    vote_id: str = Field(..., description="Vote ID")
    vote_status: VotingStatusEnum = Field(..., description="Current vote status")
    progress: Dict[str, Any] = Field(..., description="Vote progress details")
    estimated_completion: Optional[datetime] = Field(None, description="Estimated completion time")


class DebateProgressUpdate(BaseModel):
    """Model for real-time debate progress updates."""
    event_type: str = Field(..., description="Type of update")
    timestamp: datetime = Field(..., description="Update timestamp")
    debate_id: str = Field(..., description="Debate ID")
    debate_status: DebateStatusEnum = Field(..., description="Current debate status")
    current_speaker: Optional[str] = Field(None, description="Current speaker")
    time_remaining: Optional[int] = Field(None, description="Time remaining in minutes")
    next_speaker: Optional[str] = Field(None, description="Next scheduled speaker")


class HouseEventNotification(BaseModel):
    """Model for house event notifications."""
    event_id: str = Field(..., description="Event ID")
    event_type: str = Field(..., description="Event type")
    event_title: str = Field(..., description="Event title")
    event_description: Optional[str] = Field(None, description="Event description")
    event_time: datetime = Field(..., description="Event time")
    priority: EventPriorityEnum = Field(..., description="Event priority")
    requires_action: bool = Field(False, description="Whether action is required")
    action_url: Optional[str] = Field(None, description="URL for action if required")


class WebSocketMessage(BaseModel):
    """Base model for WebSocket messages."""
    message_type: str = Field(..., description="Type of message")
    timestamp: datetime = Field(..., description="Message timestamp")
    data: Dict[str, Any] = Field(..., description="Message data")


class HouseStatusWebSocketMessage(WebSocketMessage):
    """WebSocket message for house status updates."""
    message_type: str = Field("house_status_update", description="Message type")
    data: HouseStatusUpdate = Field(..., description="House status update data")


class VoteProgressWebSocketMessage(WebSocketMessage):
    """WebSocket message for vote progress updates."""
    message_type: str = Field("vote_progress_update", description="Message type")
    data: VoteProgressUpdate = Field(..., description="Vote progress update data")


class DebateProgressWebSocketMessage(WebSocketMessage):
    """WebSocket message for debate progress updates."""
    message_type: str = Field("debate_progress_update", description="Message type")
    data: DebateProgressUpdate = Field(..., description="Debate progress update data")


class HouseEventWebSocketMessage(WebSocketMessage):
    """WebSocket message for house event notifications."""
    message_type: str = Field("house_event_notification", description="Message type")
    data: HouseEventNotification = Field(..., description="House event notification data")


# ============================================================================
# ANALYTICS AND STATISTICS MODELS
# ============================================================================

class HouseStatusStatistics(BaseModel):
    """Model for house status statistics."""
    total_sessions: int = Field(..., description="Total number of sessions")
    active_sessions: int = Field(..., description="Number of active sessions")
    total_sittings: int = Field(..., description="Total number of sittings")
    active_sittings: int = Field(..., description="Number of active sittings")
    total_votes: int = Field(..., description="Total number of votes")
    active_votes: int = Field(..., description="Number of active votes")
    total_debates: int = Field(..., description="Total number of debates")
    active_debates: int = Field(..., description="Number of active debates")
    average_sitting_duration: Optional[float] = Field(None, description="Average sitting duration in hours")
    average_vote_duration: Optional[float] = Field(None, description="Average vote duration in minutes")
    quorum_met_percentage: float = Field(..., description="Percentage of time quorum was met")
    generated_at: datetime = Field(..., description="When statistics were generated")


class SessionAnalytics(BaseModel):
    """Model for session analytics."""
    session_id: str = Field(..., description="Session ID")
    session_number: int = Field(..., description="Session number")
    total_sittings: int = Field(..., description="Total sittings in session")
    total_votes: int = Field(..., description="Total votes in session")
    total_debates: int = Field(..., description="Total debates in session")
    total_hours: float = Field(..., description="Total sitting hours")
    bills_passed: int = Field(..., description="Number of bills passed")
    bills_defeated: int = Field(..., description="Number of bills defeated")
    attendance_average: float = Field(..., description="Average attendance percentage")
    generated_at: datetime = Field(..., description="When analytics were generated")
