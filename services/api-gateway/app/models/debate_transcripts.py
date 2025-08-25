"""
Debate Transcript Models

Models for parliamentary debate transcripts (Hansard).
Implements FEAT-018 Debate Transcripts (P1 priority).
"""

from sqlalchemy import Column, String, Text, DateTime, Integer, Float, Boolean, ForeignKey, Index, Date, Time
from sqlalchemy.dialects.postgresql import UUID, JSONB, TSVECTOR
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from typing import Optional, Dict, Any, List
from datetime import datetime, date, time


class DebateSession(Base):
    """Parliamentary debate session (Hansard document)."""
    
    __tablename__ = "debate_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Session identification
    parliament_number = Column(Integer, nullable=False)  # e.g., 44
    session_number = Column(Integer, nullable=False)     # e.g., 1
    sitting_number = Column(Integer, nullable=False)     # e.g., 123
    sitting_date = Column(Date, nullable=False)
    
    # Document metadata
    document_number = Column(String(50), unique=True, nullable=False)  # e.g., "44-1-123"
    source_url = Column(String(500), nullable=True)
    language = Column(String(10), nullable=False, default="en")  # en, fr
    is_bilingual = Column(Boolean, default=True, nullable=False)
    
    # Session details
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    house_status = Column(String(50), nullable=True)  # sitting, committee_of_whole, etc.
    
    # Content summary
    total_statements = Column(Integer, default=0, nullable=False)
    total_words = Column(Integer, default=0, nullable=False)
    total_speakers = Column(Integer, default=0, nullable=False)
    
    # Topics and metadata
    topics = Column(JSONB, nullable=True)  # Array of detected topics
    bills_discussed = Column(JSONB, nullable=True)  # Array of bill IDs
    committees_mentioned = Column(JSONB, nullable=True)  # Array of committee names
    
    # Full-text search
    search_vector = Column(TSVECTOR, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    statements = relationship("DebateStatement", back_populates="session", cascade="all, delete-orphan")
    speakers = relationship("DebateSpeaker", secondary="debate_session_speakers", back_populates="sessions")
    
    # Indexes
    __table_args__ = (
        Index('idx_debate_session_date', 'sitting_date'),
        Index('idx_debate_session_parliament', 'parliament_number', 'session_number'),
        Index('idx_debate_session_number', 'document_number'),
        Index('idx_debate_session_search', 'search_vector', postgresql_using='gin'),
    )


class DebateStatement(Base):
    """Individual statement within a debate."""
    
    __tablename__ = "debate_statements"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("debate_sessions.id"), nullable=False)
    
    # Statement metadata
    sequence_number = Column(Integer, nullable=False)  # Order within session
    timestamp = Column(Time, nullable=True)
    statement_type = Column(String(50), nullable=False)  # speech, question, answer, intervention, procedural
    
    # Speaker information
    speaker_id = Column(UUID(as_uuid=True), ForeignKey("debate_speakers.id"), nullable=True)
    speaker_role = Column(String(100), nullable=True)  # member, speaker, clerk, etc.
    
    # Content
    content = Column(Text, nullable=False)
    content_fr = Column(Text, nullable=True)  # French version if available
    language = Column(String(10), nullable=False, default="en")
    
    # Metadata
    word_count = Column(Integer, nullable=False)
    topic = Column(String(200), nullable=True)  # Current topic being discussed
    bill_reference = Column(String(50), nullable=True)  # Bill being discussed
    
    # References
    references = Column(JSONB, nullable=True)  # Bills, documents, members mentioned
    interjections = Column(JSONB, nullable=True)  # Interruptions, applause, etc.
    
    # Full-text search
    search_vector = Column(TSVECTOR, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("DebateSession", back_populates="statements")
    speaker = relationship("DebateSpeaker", back_populates="statements")
    annotations = relationship("DebateAnnotation", back_populates="statement", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_statement_session', 'session_id'),
        Index('idx_statement_speaker', 'speaker_id'),
        Index('idx_statement_sequence', 'session_id', 'sequence_number'),
        Index('idx_statement_type', 'statement_type'),
        Index('idx_statement_search', 'search_vector', postgresql_using='gin'),
    )


class DebateSpeaker(Base):
    """Speaker in debates (may or may not be a current member)."""
    
    __tablename__ = "debate_speakers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Speaker identification
    name = Column(String(200), nullable=False)
    normalized_name = Column(String(200), nullable=False)  # For matching
    member_id = Column(UUID(as_uuid=True), ForeignKey("openpolicy.members.id"), nullable=True)
    
    # Speaker details
    party = Column(String(100), nullable=True)
    riding = Column(String(200), nullable=True)
    province = Column(String(50), nullable=True)
    role = Column(String(100), nullable=True)  # minister, parliamentary_secretary, etc.
    
    # Statistics
    total_statements = Column(Integer, default=0, nullable=False)
    total_words = Column(Integer, default=0, nullable=False)
    first_seen = Column(Date, nullable=True)
    last_seen = Column(Date, nullable=True)
    
    # Metadata
    alternate_names = Column(JSONB, nullable=True)  # Other forms of the name
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    member = relationship("Member", backref="debate_speaker")
    statements = relationship("DebateStatement", back_populates="speaker")
    sessions = relationship("DebateSession", secondary="debate_session_speakers", back_populates="speakers")
    
    # Indexes
    __table_args__ = (
        Index('idx_speaker_name', 'normalized_name'),
        Index('idx_speaker_member', 'member_id'),
        Index('idx_speaker_party', 'party'),
    )


# Association table for session speakers
debate_session_speakers = Table(
    'debate_session_speakers',
    Base.metadata,
    Column('session_id', UUID(as_uuid=True), ForeignKey('debate_sessions.id')),
    Column('speaker_id', UUID(as_uuid=True), ForeignKey('debate_speakers.id')),
    Column('statement_count', Integer, default=0),
    Column('word_count', Integer, default=0)
)


class DebateAnnotation(Base):
    """Annotations and notes on debate statements."""
    
    __tablename__ = "debate_annotations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    statement_id = Column(UUID(as_uuid=True), ForeignKey("debate_statements.id"), nullable=False)
    
    # Annotation details
    annotation_type = Column(String(50), nullable=False)  # correction, clarification, context, reference
    content = Column(Text, nullable=False)
    
    # Source
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_official = Column(Boolean, default=False, nullable=False)  # Official correction vs user note
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    statement = relationship("DebateStatement", back_populates="annotations")
    creator = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_annotation_statement', 'statement_id'),
        Index('idx_annotation_type', 'annotation_type'),
    )


class DebateSearch(Base):
    """Saved debate searches."""
    
    __tablename__ = "debate_searches"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Search parameters
    name = Column(String(200), nullable=False)
    query = Column(Text, nullable=False)
    filters = Column(JSONB, nullable=False)  # Date range, speakers, topics, etc.
    
    # Settings
    is_public = Column(Boolean, default=False, nullable=False)
    email_alerts = Column(Boolean, default=False, nullable=False)
    
    # Statistics
    run_count = Column(Integer, default=0, nullable=False)
    last_run = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_search_user', 'user_id'),
        Index('idx_search_public', 'is_public'),
    )


class DebateTopic(Base):
    """Topics and themes in debates."""
    
    __tablename__ = "debate_topics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Topic information
    name = Column(String(200), unique=True, nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    category = Column(String(100), nullable=True)  # economy, health, environment, etc.
    
    # Description
    description = Column(Text, nullable=True)
    keywords = Column(JSONB, nullable=True)  # Keywords for auto-detection
    
    # Statistics
    mention_count = Column(Integer, default=0, nullable=False)
    first_mentioned = Column(Date, nullable=True)
    last_mentioned = Column(Date, nullable=True)
    
    # Metadata
    is_active = Column(Boolean, default=True, nullable=False)
    auto_detected = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_topic_slug', 'slug'),
        Index('idx_topic_category', 'category'),
    )


class DebateAnalytics(Base):
    """Analytics and statistics for debate sessions."""
    
    __tablename__ = "debate_analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("debate_sessions.id"), unique=True, nullable=False)
    
    # Word frequency analysis
    top_words = Column(JSONB, nullable=True)  # [{word, count, tfidf_score}]
    word_cloud_data = Column(JSONB, nullable=True)
    
    # Topic analysis
    topic_distribution = Column(JSONB, nullable=True)  # {topic: percentage}
    sentiment_scores = Column(JSONB, nullable=True)  # {positive, negative, neutral}
    
    # Speaker analysis
    speaker_time_distribution = Column(JSONB, nullable=True)  # {speaker_id: minutes}
    party_participation = Column(JSONB, nullable=True)  # {party: percentage}
    
    # Engagement metrics
    interruption_count = Column(Integer, default=0, nullable=False)
    question_count = Column(Integer, default=0, nullable=False)
    
    # Generated summaries
    auto_summary = Column(Text, nullable=True)
    key_points = Column(JSONB, nullable=True)  # Array of key discussion points
    
    # Computation metadata
    computed_at = Column(DateTime(timezone=True), server_default=func.now())
    computation_time_ms = Column(Integer, nullable=True)
    
    # Relationships
    session = relationship("DebateSession", backref="analytics", uselist=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_analytics_session', 'session_id'),
    )