"""
House Status Models for OpenPolicy V2

Comprehensive models for tracking real-time parliamentary house status,
session information, voting status, and live updates.
"""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base


class HouseSession(Base):
    """Model for tracking parliamentary house sessions."""
    
    __tablename__ = "house_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_number = Column(Integer, nullable=False, unique=True)
    session_name = Column(String(200), nullable=False)
    parliament_number = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    status = Column(String(50), default="active", nullable=False)  # active, prorogued, dissolved
    government_party = Column(String(100), nullable=True)
    opposition_leader = Column(String(100), nullable=True)
    speaker = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    sittings = relationship("HouseSitting", back_populates="session", cascade="all, delete-orphan")
    votes = relationship("HouseVote", back_populates="session", cascade="all, delete-orphan")
    debates = relationship("HouseDebate", back_populates="session", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_house_sessions_parliament_number', 'parliament_number'),
        Index('ix_house_sessions_is_active', 'is_active'),
        Index('ix_house_sessions_status', 'status'),
        Index('ix_house_sessions_start_date', 'start_date'),
    )


class HouseSitting(Base):
    """Model for tracking individual house sittings within a session."""
    
    __tablename__ = "house_sittings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("house_sessions.id"), nullable=False)
    sitting_number = Column(Integer, nullable=False)
    sitting_date = Column(DateTime, nullable=False)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    status = Column(String(50), default="scheduled", nullable=False)  # scheduled, in_progress, adjourned, suspended
    quorum_present = Column(Boolean, default=True, nullable=False)
    members_present = Column(Integer, default=0, nullable=False)
    total_members = Column(Integer, default=338, nullable=False)  # Canadian House of Commons
    agenda_items = Column(JSONB, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    session = relationship("HouseSession", back_populates="sittings")
    votes = relationship("HouseVote", back_populates="sitting", cascade="all, delete-orphan")
    debates = relationship("HouseDebate", back_populates="sitting", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_house_sittings_session_id', 'session_id'),
        Index('ix_house_sittings_sitting_date', 'sitting_date'),
        Index('ix_house_sittings_is_active', 'is_active'),
        Index('ix_house_sittings_status', 'status'),
    )


class HouseVote(Base):
    """Model for tracking real-time voting status and results."""
    
    __tablename__ = "house_votes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("house_sessions.id"), nullable=False)
    sitting_id = Column(UUID(as_uuid=True), ForeignKey("house_sittings.id"), nullable=True)
    vote_number = Column(Integer, nullable=False)
    bill_id = Column(String(100), nullable=True)
    motion_text = Column(Text, nullable=False)
    vote_type = Column(String(50), nullable=False)  # division, voice_vote, unanimous_consent
    status = Column(String(50), default="scheduled", nullable=False)  # scheduled, in_progress, completed, cancelled
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    total_votes_cast = Column(Integer, default=0, nullable=False)
    yeas = Column(Integer, default=0, nullable=False)
    nays = Column(Integer, default=0, nullable=False)
    abstentions = Column(Integer, default=0, nullable=False)
    result = Column(String(50), nullable=True)  # passed, defeated, tied
    requires_royal_assent = Column(Boolean, default=False, nullable=False)
    royal_assent_date = Column(DateTime, nullable=True)
    vote_metadata = Column(JSONB, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    session = relationship("HouseSession", back_populates="votes")
    sitting = relationship("HouseSitting", back_populates="votes")
    individual_votes = relationship("IndividualVote", back_populates="house_vote", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_house_votes_session_id', 'session_id'),
        Index('ix_house_votes_sitting_id', 'sitting_id'),
        Index('ix_house_votes_vote_number', 'vote_number'),
        Index('ix_house_votes_status', 'status'),
        Index('ix_house_votes_bill_id', 'bill_id'),
        Index('ix_house_votes_start_time', 'start_time'),
    )


class IndividualVote(Base):
    """Model for tracking individual MP votes within a house vote."""
    
    __tablename__ = "individual_votes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    house_vote_id = Column(UUID(as_uuid=True), ForeignKey("house_votes.id"), nullable=False)
    member_id = Column(String(100), nullable=False)
    member_name = Column(String(200), nullable=False)
    party = Column(String(100), nullable=False)
    riding = Column(String(200), nullable=False)
    vote_cast = Column(String(20), nullable=False)  # yea, nay, abstain, absent
    vote_time = Column(DateTime, nullable=True)
    is_paired = Column(Boolean, default=False, nullable=False)
    paired_with = Column(String(100), nullable=True)
    whip_status = Column(String(50), nullable=True)  # whipped, free_vote, cabinet
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    house_vote = relationship("HouseVote", back_populates="individual_votes")
    
    # Indexes
    __table_args__ = (
        Index('ix_individual_votes_house_vote_id', 'house_vote_id'),
        Index('ix_individual_votes_member_id', 'member_id'),
        Index('ix_individual_votes_party', 'party'),
        Index('ix_individual_votes_vote_cast', 'vote_cast'),
    )


class HouseDebate(Base):
    """Model for tracking live debate status and progress."""
    
    __tablename__ = "house_debates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("house_sessions.id"), nullable=False)
    sitting_id = Column(UUID(as_uuid=True), ForeignKey("house_sittings.id"), nullable=True)
    debate_type = Column(String(100), nullable=False)  # government_business, opposition_day, private_members
    subject = Column(String(500), nullable=False)
    bill_id = Column(String(100), nullable=True)
    status = Column(String(50), default="scheduled", nullable=False)  # scheduled, in_progress, completed, adjourned
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    current_speaker = Column(String(200), nullable=True)
    time_allocation_minutes = Column(Integer, nullable=True)
    time_used_minutes = Column(Integer, nullable=True)
    speakers_list = Column(JSONB, nullable=True)  # List of scheduled speakers
    current_amendment = Column(String(500), nullable=True)
    closure_motion = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    session = relationship("HouseSession", back_populates="debates")
    sitting = relationship("HouseSitting", back_populates="debates")
    
    # Indexes
    __table_args__ = (
        Index('ix_house_debates_session_id', 'session_id'),
        Index('ix_house_debates_sitting_id', 'sitting_id'),
        Index('ix_house_debates_status', 'status'),
        Index('ix_house_debates_debate_type', 'debate_type'),
        Index('ix_house_debates_start_time', 'start_time'),
    )


class HouseStatus(Base):
    """Model for tracking current real-time house status."""
    
    __tablename__ = "house_status"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    current_session_id = Column(UUID(as_uuid=True), ForeignKey("house_sessions.id"), nullable=True)
    current_sitting_id = Column(UUID(as_uuid=True), ForeignKey("house_sittings.id"), nullable=True)
    current_vote_id = Column(UUID(as_uuid=True), ForeignKey("house_votes.id"), nullable=True)
    current_debate_id = Column(UUID(as_uuid=True), ForeignKey("house_debates.id"), nullable=True)
    
    # Current status
    house_status = Column(String(50), default="sitting", nullable=False)  # sitting, adjourned, prorogued, dissolved
    sitting_status = Column(String(50), default="in_progress", nullable=False)  # in_progress, suspended, adjourned
    voting_status = Column(String(50), default="none", nullable=False)  # none, in_progress, completed
    debate_status = Column(String(50), default="none", nullable=False)  # none, in_progress, completed
    
    # Real-time information
    members_present = Column(Integer, default=0, nullable=False)
    quorum_met = Column(Boolean, default=True, nullable=False)
    current_time = Column(DateTime, server_default=func.now(), nullable=False)
    next_scheduled_event = Column(String(500), nullable=True)
    next_event_time = Column(DateTime, nullable=True)
    
    # House rules and procedures
    question_period_status = Column(String(50), default="none", nullable=False)  # none, scheduled, in_progress, completed
    emergency_debate_requested = Column(Boolean, default=False, nullable=False)
    closure_motion_active = Column(Boolean, default=False, nullable=False)
    
    # Metadata
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    update_source = Column(String(100), default="system", nullable=False)
    notes = Column(Text, nullable=True)
    
    # Relationships
    current_session = relationship("HouseSession", foreign_keys=[current_session_id])
    current_sitting = relationship("HouseSitting", foreign_keys=[current_sitting_id])
    current_vote = relationship("HouseVote", foreign_keys=[current_vote_id])
    current_debate = relationship("HouseDebate", foreign_keys=[current_debate_id])
    
    # Indexes
    __table_args__ = (
        Index('ix_house_status_house_status', 'house_status'),
        Index('ix_house_status_sitting_status', 'sitting_status'),
        Index('ix_house_status_voting_status', 'voting_status'),
        Index('ix_house_status_debate_status', 'debate_status'),
        Index('ix_house_status_last_updated', 'last_updated'),
    )


class HouseEvent(Base):
    """Model for tracking house events and notifications."""
    
    __tablename__ = "house_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String(100), nullable=False)  # vote_start, vote_end, debate_start, adjournment, etc.
    event_title = Column(String(200), nullable=False)
    event_description = Column(Text, nullable=True)
    event_time = Column(DateTime, nullable=False)
    session_id = Column(UUID(as_uuid=True), ForeignKey("house_sessions.id"), nullable=True)
    sitting_id = Column(UUID(as_uuid=True), ForeignKey("house_sittings.id"), nullable=True)
    related_bill_id = Column(String(100), nullable=True)
    related_vote_id = Column(UUID(as_uuid=True), ForeignKey("house_votes.id"), nullable=True)
    related_debate_id = Column(UUID(as_uuid=True), ForeignKey("house_debates.id"), nullable=True)
    
    # Event details
    priority = Column(String(20), default="normal", nullable=False)  # low, normal, high, critical
    requires_notification = Column(Boolean, default=True, nullable=False)
    notification_sent = Column(Boolean, default=False, nullable=False)
    event_metadata = Column(JSONB, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    session = relationship("HouseSession", foreign_keys=[session_id])
    sitting = relationship("HouseSitting", foreign_keys=[sitting_id])
    related_vote = relationship("HouseVote", foreign_keys=[related_vote_id])
    related_debate = relationship("HouseDebate", foreign_keys=[related_debate_id])
    
    # Indexes
    __table_args__ = (
        Index('ix_house_events_event_type', 'event_type'),
        Index('ix_house_events_event_time', 'event_time'),
        Index('ix_house_events_priority', 'priority'),
        Index('ix_house_events_requires_notification', 'requires_notification'),
        Index('ix_house_events_session_id', 'session_id'),
    )
