from sqlalchemy import Column, String, DateTime, Text, ARRAY, Float, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database import Base

class UserVote(Base):
    __tablename__ = "user_votes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)
    bill_id = Column(String, nullable=False, index=True)
    vote_choice = Column(String, nullable=False)  # 'yes', 'no', 'abstain'
    reason = Column(Text, nullable=False)
    confidence_level = Column(String, default='medium')  # 'low', 'medium', 'high'
    constituency = Column(String, nullable=True)
    party_preference = Column(String, nullable=True)
    influence_factors = Column(ARRAY(String), default=[])
    related_issues = Column(ARRAY(String), default=[])
    public_visibility = Column(String, default='public')  # 'public', 'private'
    vote_weight = Column(Float, default=1.0)
    device = Column(String, nullable=True)
    location = Column(String, nullable=True)
    session_id = Column(String, nullable=True)
    vote_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Composite indexes for efficient queries
    __table_args__ = (
        Index('idx_user_bill', 'user_id', 'bill_id'),
        Index('idx_bill_vote_choice', 'bill_id', 'vote_choice'),
        Index('idx_vote_date', 'vote_date'),
        Index('idx_public_visibility', 'public_visibility'),
        Index('idx_constituency', 'constituency'),
        Index('idx_party_preference', 'party_preference'),
    )
    
    def __repr__(self):
        return f"<UserVote(id={self.id}, user_id={self.user_id}, bill_id={self.bill_id}, vote_choice={self.vote_choice})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "bill_id": self.bill_id,
            "vote_choice": self.vote_choice,
            "reason": self.reason,
            "confidence_level": self.confidence_level,
            "constituency": self.constituency,
            "party_preference": self.party_preference,
            "influence_factors": self.influence_factors or [],
            "related_issues": self.related_issues or [],
            "public_visibility": self.public_visibility,
            "vote_weight": self.vote_weight,
            "device": self.device,
            "location": self.location,
            "session_id": self.session_id,
            "vote_date": self.vote_date.isoformat() if self.vote_date else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
