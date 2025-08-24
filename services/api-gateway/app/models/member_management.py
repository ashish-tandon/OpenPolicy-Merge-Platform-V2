"""
Member Management Models

Enhanced models for member management functionality.
Implements FEAT-015 Member Management (P0 priority).
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Index, Date, Integer, Float, Table
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime


class MemberAudit(Base):
    """Audit trail for member changes."""
    
    __tablename__ = "member_audits"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_id = Column(UUID(as_uuid=True), ForeignKey("openpolicy.members.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action = Column(String(50), nullable=False)  # create, update, delete, import, merge
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    changes = Column(JSONB, nullable=True)  # Before/after values
    reason = Column(Text, nullable=True)
    metadata = Column(JSONB, nullable=True)  # Additional context
    
    # Relationships
    member = relationship("Member", backref="audit_logs")
    user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_member_audit_member_id', 'member_id'),
        Index('idx_member_audit_user_id', 'user_id'),
        Index('idx_member_audit_timestamp', 'timestamp'),
        Index('idx_member_audit_action', 'action'),
    )


class MemberImport(Base):
    """Track bulk member imports."""
    
    __tablename__ = "member_imports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    import_source = Column(String(100), nullable=False)  # openparliament, manual, csv, api
    import_type = Column(String(50), nullable=False)  # full, incremental, update
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), nullable=False)  # pending, processing, completed, failed
    total_records = Column(Integer, nullable=True)
    processed_records = Column(Integer, default=0, nullable=False)
    created_count = Column(Integer, default=0, nullable=False)
    updated_count = Column(Integer, default=0, nullable=False)
    error_count = Column(Integer, default=0, nullable=False)
    errors = Column(JSONB, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "import_source": self.import_source,
            "import_type": self.import_type,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "status": self.status,
            "total_records": self.total_records,
            "processed_records": self.processed_records,
            "created_count": self.created_count,
            "updated_count": self.updated_count,
            "error_count": self.error_count,
            "errors": self.errors
        }


class MemberContact(Base):
    """Extended contact information for members."""
    
    __tablename__ = "member_contacts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_id = Column(UUID(as_uuid=True), ForeignKey("openpolicy.members.id"), nullable=False)
    contact_type = Column(String(50), nullable=False)  # office, constituency, personal
    address_line1 = Column(String(200), nullable=True)
    address_line2 = Column(String(200), nullable=True)
    city = Column(String(100), nullable=True)
    province = Column(String(50), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(100), default="Canada", nullable=False)
    phone = Column(String(50), nullable=True)
    fax = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    hours = Column(JSONB, nullable=True)  # Office hours
    is_primary = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    member = relationship("Member", backref="contacts")
    
    # Indexes
    __table_args__ = (
        Index('idx_member_contact_member_id', 'member_id'),
        Index('idx_member_contact_type', 'contact_type'),
    )


class MemberSocialMedia(Base):
    """Social media accounts for members."""
    
    __tablename__ = "member_social_media"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_id = Column(UUID(as_uuid=True), ForeignKey("openpolicy.members.id"), nullable=False)
    platform = Column(String(50), nullable=False)  # twitter, facebook, instagram, linkedin, youtube
    handle = Column(String(100), nullable=False)
    url = Column(String(500), nullable=True)
    verified = Column(Boolean, default=False, nullable=False)
    follower_count = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    last_verified = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    member = relationship("Member", backref="social_media")
    
    # Indexes
    __table_args__ = (
        Index('idx_member_social_member_id', 'member_id'),
        Index('idx_member_social_platform', 'platform'),
    )


class MemberEducation(Base):
    """Educational background for members."""
    
    __tablename__ = "member_education"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_id = Column(UUID(as_uuid=True), ForeignKey("openpolicy.members.id"), nullable=False)
    institution = Column(String(200), nullable=False)
    degree = Column(String(200), nullable=True)
    field_of_study = Column(String(200), nullable=True)
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    graduated = Column(Boolean, nullable=True)
    notes = Column(Text, nullable=True)
    display_order = Column(Integer, default=0, nullable=False)
    
    # Relationships
    member = relationship("Member", backref="education")
    
    # Indexes
    __table_args__ = (
        Index('idx_member_education_member_id', 'member_id'),
    )


class MemberProfession(Base):
    """Professional background for members."""
    
    __tablename__ = "member_professions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_id = Column(UUID(as_uuid=True), ForeignKey("openpolicy.members.id"), nullable=False)
    title = Column(String(200), nullable=False)
    organization = Column(String(200), nullable=True)
    industry = Column(String(100), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_current = Column(Boolean, default=False, nullable=False)
    description = Column(Text, nullable=True)
    display_order = Column(Integer, default=0, nullable=False)
    
    # Relationships
    member = relationship("Member", backref="professions")
    
    # Indexes
    __table_args__ = (
        Index('idx_member_profession_member_id', 'member_id'),
    )


class MemberTag(Base):
    """Tags for categorizing and searching members."""
    
    __tablename__ = "member_tags"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50), nullable=True)  # topic, role, committee, etc.
    description = Column(Text, nullable=True)
    color = Column(String(7), nullable=True)  # Hex color
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_member_tag_name', 'name'),
        Index('idx_member_tag_category', 'category'),
    )


# Association table for member tags
member_tag_associations = Table(
    'member_tag_associations',
    Base.metadata,
    Column('member_id', UUID(as_uuid=True), ForeignKey('openpolicy.members.id')),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('member_tags.id')),
    Column('tagged_at', DateTime(timezone=True), server_default=func.now()),
    Column('tagged_by', UUID(as_uuid=True), ForeignKey('users.id'))
)


class MemberMetrics(Base):
    """Computed metrics and statistics for members."""
    
    __tablename__ = "member_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_id = Column(UUID(as_uuid=True), ForeignKey("openpolicy.members.id"), unique=True, nullable=False)
    
    # Activity metrics
    bills_sponsored = Column(Integer, default=0, nullable=False)
    bills_cosponsored = Column(Integer, default=0, nullable=False)
    votes_total = Column(Integer, default=0, nullable=False)
    votes_yea = Column(Integer, default=0, nullable=False)
    votes_nay = Column(Integer, default=0, nullable=False)
    votes_abstain = Column(Integer, default=0, nullable=False)
    attendance_rate = Column(Float, nullable=True)  # Percentage
    
    # Engagement metrics
    speeches_count = Column(Integer, default=0, nullable=False)
    questions_asked = Column(Integer, default=0, nullable=False)
    committee_memberships = Column(Integer, default=0, nullable=False)
    
    # Social media metrics
    twitter_followers = Column(Integer, nullable=True)
    facebook_likes = Column(Integer, nullable=True)
    social_engagement_score = Column(Float, nullable=True)
    
    # Computed scores
    activity_score = Column(Float, nullable=True)  # 0-100
    influence_score = Column(Float, nullable=True)  # 0-100
    transparency_score = Column(Float, nullable=True)  # 0-100
    
    # Last updated
    last_calculated = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    member = relationship("Member", backref="metrics", uselist=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_member_metrics_member_id', 'member_id'),
        Index('idx_member_metrics_activity_score', 'activity_score'),
        Index('idx_member_metrics_influence_score', 'influence_score'),
    )


# Extend the existing Member model with new relationships
def setup_member_relationships():
    """Set up additional relationships on the Member model."""
    from app.models.openparliament import Member
    
    # Add the tags relationship
    Member.tags = relationship(
        "MemberTag",
        secondary=member_tag_associations,
        backref="members"
    )