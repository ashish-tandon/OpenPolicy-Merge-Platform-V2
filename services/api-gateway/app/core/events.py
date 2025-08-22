"""
Event definitions and schemas for real-time parliamentary data.

This module defines all event types, schemas, and message formats
used throughout the real-time system.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
from enum import Enum
from pydantic import BaseModel, Field, validator


class EventType(str, Enum):
    """Types of real-time events that can be broadcast."""
    # Parliamentary events
    VOTE_UPDATE = "vote_update"
    BILL_STATUS_CHANGE = "bill_status_change"
    BILL_AMENDMENT = "bill_amendment"
    BILL_INTRODUCTION = "bill_introduction"
    
    # Debate events
    DEBATE_STATEMENT = "debate_statement"
    DEBATE_START = "debate_start"
    DEBATE_END = "debate_end"
    
    # Committee events
    COMMITTEE_MEETING_UPDATE = "committee_meeting_update"
    COMMITTEE_MEETING_START = "committee_meeting_start"
    COMMITTEE_MEETING_END = "committee_meeting_end"
    COMMITTEE_STUDY_UPDATE = "committee_study_update"
    
    # Member events
    MEMBER_PRESENCE = "member_presence"
    MEMBER_SPEAKING = "member_speaking"
    
    # System events
    NOTIFICATION = "notification"
    PRESENCE_UPDATE = "presence_update"
    HEARTBEAT = "heartbeat"
    SYSTEM_ALERT = "system_alert"
    
    # User events
    USER_JOIN = "user_join"
    USER_LEAVE = "user_leave"
    USER_TYPING = "user_typing"


class EventPriority(str, Enum):
    """Priority levels for events."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class EventCategory(str, Enum):
    """Categories for organizing events."""
    PARLIAMENTARY = "parliamentary"
    DEBATE = "debate"
    COMMITTEE = "committee"
    MEMBER = "member"
    SYSTEM = "system"
    USER = "user"


class BaseEvent(BaseModel):
    """Base model for all events."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: EventType
    category: EventCategory
    priority: EventPriority = EventPriority.NORMAL
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: Optional[str] = None
    target_rooms: Optional[List[str]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        use_enum_values = True


# Parliamentary Event Schemas

class VoteData(BaseModel):
    """Data structure for vote events."""
    vote_id: str
    bill_number: Optional[str] = None
    bill_title: Optional[str] = None
    session: str
    vote_number: int
    result: str
    yea_total: int
    nay_total: int
    paired_count: int = 0
    absent_count: int = 0
    vote_date: datetime
    description: str


class VoteUpdateEvent(BaseEvent):
    """Event for vote updates."""
    type: EventType = EventType.VOTE_UPDATE
    category: EventCategory = EventCategory.PARLIAMENTARY
    priority: EventPriority = EventPriority.HIGH
    data: VoteData


class BillStatusData(BaseModel):
    """Data structure for bill status changes."""
    bill_id: str
    bill_number: str
    bill_title: str
    old_status: Optional[str] = None
    new_status: str
    session_id: str
    institution: str
    change_reason: Optional[str] = None
    effective_date: datetime


class BillStatusChangeEvent(BaseEvent):
    """Event for bill status changes."""
    type: EventType = EventType.BILL_STATUS_CHANGE
    category: EventCategory = EventCategory.PARLIAMENTARY
    priority: EventPriority = EventPriority.NORMAL
    data: BillStatusData


class BillAmendmentData(BaseModel):
    """Data structure for bill amendments."""
    amendment_id: str
    bill_id: str
    bill_number: str
    amendment_number: str
    amendment_type: str
    status: str
    proposed_by: str
    proposed_date: datetime
    description: str


class BillAmendmentEvent(BaseEvent):
    """Event for bill amendments."""
    type: EventType = EventType.BILL_AMENDMENT
    category: EventCategory = EventCategory.PARLIAMENTARY
    priority: EventPriority = EventPriority.NORMAL
    data: BillAmendmentData


# Debate Event Schemas

class DebateStatementData(BaseModel):
    """Data structure for debate statements."""
    statement_id: str
    debate_date: datetime
    debate_number: int
    politician_name: str
    politician_party: Optional[str] = None
    politician_riding: Optional[str] = None
    bill_mentioned: Optional[str] = None
    statement_text: str
    statement_time: datetime
    sequence: int


class DebateStatementEvent(BaseEvent):
    """Event for debate statements."""
    type: EventType = EventType.DEBATE_STATEMENT
    category: EventCategory = EventCategory.DEBATE
    priority: EventPriority = EventPriority.LOW
    data: DebateStatementData


class DebateSessionData(BaseModel):
    """Data structure for debate session events."""
    debate_date: datetime
    debate_number: int
    session_id: str
    institution: str
    topic: Optional[str] = None
    expected_duration: Optional[int] = None


class DebateStartEvent(BaseEvent):
    """Event for debate start."""
    type: EventType = EventType.DEBATE_START
    category: EventCategory = EventCategory.DEBATE
    priority: EventPriority = EventPriority.NORMAL
    data: DebateSessionData


class DebateEndEvent(BaseEvent):
    """Event for debate end."""
    type: EventType = EventType.DEBATE_END
    category: EventCategory = EventCategory.DEBATE
    priority: EventPriority = EventPriority.NORMAL
    data: DebateSessionData


# Committee Event Schemas

class CommitteeMeetingData(BaseModel):
    """Data structure for committee meeting events."""
    meeting_id: str
    committee_id: str
    committee_name: str
    meeting_number: int
    session_id: str
    meeting_date: datetime
    meeting_type: str
    status: str
    agenda: Optional[str] = None
    attendees_count: Optional[int] = None


class CommitteeMeetingUpdateEvent(BaseEvent):
    """Event for committee meeting updates."""
    type: EventType = EventType.COMMITTEE_MEETING_UPDATE
    category: EventCategory = EventCategory.COMMITTEE
    priority: EventPriority = EventPriority.NORMAL
    data: CommitteeMeetingData


class CommitteeStudyData(BaseModel):
    """Data structure for committee study events."""
    study_id: str
    committee_id: str
    committee_name: str
    study_title: str
    study_type: str
    status: str
    start_date: datetime
    end_date: Optional[datetime] = None
    witnesses_count: Optional[int] = None


class CommitteeStudyUpdateEvent(BaseEvent):
    """Event for committee study updates."""
    type: EventType = EventType.COMMITTEE_STUDY_UPDATE
    category: EventCategory = EventCategory.COMMITTEE
    priority: EventPriority = EventPriority.NORMAL
    data: CommitteeStudyData


# Member Event Schemas

class MemberPresenceData(BaseModel):
    """Data structure for member presence events."""
    member_id: str
    member_name: str
    party: str
    riding: str
    status: str  # present, absent, paired, etc.
    location: Optional[str] = None
    timestamp: datetime


class MemberPresenceEvent(BaseEvent):
    """Event for member presence updates."""
    type: EventType = EventType.MEMBER_PRESENCE
    category: EventCategory = EventCategory.MEMBER
    priority: EventPriority = EventPriority.LOW
    data: MemberPresenceData


class MemberSpeakingData(BaseModel):
    """Data structure for member speaking events."""
    member_id: str
    member_name: str
    party: str
    riding: str
    debate_id: Optional[str] = None
    bill_id: Optional[str] = None
    speaking_time: datetime
    duration: Optional[int] = None


class MemberSpeakingEvent(BaseEvent):
    """Event for member speaking updates."""
    type: EventType = EventType.MEMBER_SPEAKING
    category: EventCategory = EventCategory.MEMBER
    priority: EventPriority = EventPriority.LOW
    data: MemberSpeakingData


# System Event Schemas

class NotificationData(BaseModel):
    """Data structure for notification events."""
    message: str
    title: Optional[str] = None
    notification_type: str = "info"  # info, success, warning, error
    action_url: Optional[str] = None
    expires_at: Optional[datetime] = None


class NotificationEvent(BaseEvent):
    """Event for notifications."""
    type: EventType = EventType.NOTIFICATION
    category: EventCategory = EventCategory.SYSTEM
    priority: EventPriority = EventPriority.NORMAL
    data: NotificationData


class SystemAlertData(BaseModel):
    """Data structure for system alerts."""
    alert_type: str  # maintenance, error, update, etc.
    severity: str  # low, medium, high, critical
    message: str
    affected_services: Optional[List[str]] = None
    estimated_duration: Optional[str] = None


class SystemAlertEvent(BaseEvent):
    """Event for system alerts."""
    type: EventType = EventType.SYSTEM_ALERT
    category: EventCategory = EventCategory.SYSTEM
    priority: EventPriority = EventPriority.HIGH
    data: SystemAlertData


# User Event Schemas

class UserPresenceData(BaseModel):
    """Data structure for user presence events."""
    user_id: str
    username: str
    status: str  # online, away, busy, offline
    last_seen: datetime
    current_page: Optional[str] = None


class UserPresenceEvent(BaseEvent):
    """Event for user presence updates."""
    type: EventType = EventType.PRESENCE_UPDATE
    category: EventCategory = EventCategory.USER
    priority: EventPriority = EventPriority.LOW
    data: UserPresenceData


class UserTypingData(BaseModel):
    """Data structure for user typing events."""
    user_id: str
    username: str
    room: str
    is_typing: bool


class UserTypingEvent(BaseEvent):
    """Event for user typing indicators."""
    type: EventType = EventType.USER_TYPING
    category: EventCategory = EventCategory.USER
    priority: EventPriority = EventPriority.LOW
    data: UserTypingData


# Utility Event Schemas

class HeartbeatEvent(BaseEvent):
    """Event for connection heartbeat."""
    type: EventType = EventType.HEARTBEAT
    category: EventCategory = EventCategory.SYSTEM
    priority: EventPriority = EventPriority.LOW
    data: Dict[str, Any] = Field(default_factory=dict)


# Event Factory Functions

def create_vote_update_event(vote_data: Dict[str, Any], **kwargs) -> VoteUpdateEvent:
    """Create a vote update event."""
    return VoteUpdateEvent(
        data=VoteData(**vote_data),
        **kwargs
    )


def create_bill_status_change_event(bill_data: Dict[str, Any], **kwargs) -> BillStatusChangeEvent:
    """Create a bill status change event."""
    return BillStatusChangeEvent(
        data=BillStatusData(**bill_data),
        **kwargs
    )


def create_debate_statement_event(statement_data: Dict[str, Any], **kwargs) -> DebateStatementEvent:
    """Create a debate statement event."""
    return DebateStatementEvent(
        data=DebateStatementData(**statement_data),
        **kwargs
    )


def create_committee_meeting_event(meeting_data: Dict[str, Any], **kwargs) -> CommitteeMeetingUpdateEvent:
    """Create a committee meeting event."""
    return CommitteeMeetingUpdateEvent(
        data=CommitteeMeetingData(**meeting_data),
        **kwargs
    )


def create_notification_event(message: str, **kwargs) -> NotificationEvent:
    """Create a notification event."""
    return NotificationEvent(
        data=NotificationData(message=message),
        **kwargs
    )


def create_heartbeat_event(**kwargs) -> HeartbeatEvent:
    """Create a heartbeat event."""
    return HeartbeatEvent(**kwargs)


# Event Type Registry

EVENT_REGISTRY = {
    EventType.VOTE_UPDATE: VoteUpdateEvent,
    EventType.BILL_STATUS_CHANGE: BillStatusChangeEvent,
    EventType.BILL_AMENDMENT: BillAmendmentEvent,
    EventType.DEBATE_STATEMENT: DebateStatementEvent,
    EventType.DEBATE_START: DebateStartEvent,
    EventType.DEBATE_END: DebateEndEvent,
    EventType.COMMITTEE_MEETING_UPDATE: CommitteeMeetingUpdateEvent,
    EventType.COMMITTEE_STUDY_UPDATE: CommitteeStudyUpdateEvent,
    EventType.MEMBER_PRESENCE: MemberPresenceEvent,
    EventType.MEMBER_SPEAKING: MemberSpeakingEvent,
    EventType.NOTIFICATION: NotificationEvent,
    EventType.SYSTEM_ALERT: SystemAlertEvent,
    EventType.PRESENCE_UPDATE: UserPresenceEvent,
    EventType.USER_TYPING: UserTypingEvent,
    EventType.HEARTBEAT: HeartbeatEvent,
}


def get_event_class(event_type: EventType) -> type:
    """Get the event class for a given event type."""
    return EVENT_REGISTRY.get(event_type, BaseEvent)


def create_event_from_data(event_type: EventType, event_data: Dict[str, Any], **kwargs) -> BaseEvent:
    """Create an event instance from event type and data."""
    event_class = get_event_class(event_type)
    if event_class == BaseEvent:
        # Fallback to base event with custom data
        return BaseEvent(type=event_type, data=event_data, **kwargs)
    
    # Create specific event type
    return event_class(data=event_data, **kwargs)
