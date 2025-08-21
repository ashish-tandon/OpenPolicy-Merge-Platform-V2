"""
User engagement models for tracking user interactions.

These models track how users interact with the legislative system.
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class BillVoteCast(Base):
    """Model for tracking user votes on bills."""
    
    __tablename__ = "bill_votes_cast"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    bill_id = Column(String(255), nullable=False, index=True)  # External bill ID
    vote_type = Column(String(50), nullable=False)  # support, oppose, abstain
    vote_reason = Column(Text, nullable=True)  # Optional reason for vote
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="bill_votes")


class SavedBill(Base):
    """Model for tracking bills saved by users."""
    
    __tablename__ = "saved_bills"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    bill_id = Column(String(255), nullable=False, index=True)  # External bill ID
    bill_title = Column(String(500), nullable=True)  # Bill title for display
    bill_summary = Column(Text, nullable=True)  # Bill summary
    is_saved = Column(Boolean, default=True, nullable=False)
    saved_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    notes = Column(Text, nullable=True)  # User notes about the bill
    
    # Relationship
    user = relationship("User", back_populates="saved_bills")


class RepresentativeIssue(Base):
    """Model for tracking issues raised by users to representatives."""
    
    __tablename__ = "representative_issues"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    representative_id = Column(String(255), nullable=False, index=True)  # External rep ID
    issue_title = Column(String(255), nullable=False)
    issue_description = Column(Text, nullable=False)
    issue_category = Column(String(100), nullable=True)  # e.g., healthcare, education
    priority = Column(String(20), default="medium", nullable=False)  # low, medium, high
    status = Column(String(20), default="pending", nullable=False)  # pending, approved, rejected, resolved
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    representative_response = Column(Text, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="representative_issues")


class UserPostalCodeHistory(Base):
    """Model for tracking user postal code changes."""
    
    __tablename__ = "user_postal_code_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    old_postal_code = Column(String(10), nullable=True)
    new_postal_code = Column(String(10), nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    reason = Column(String(255), nullable=True)  # Reason for change
    representative_id = Column(String(255), nullable=True)  # Linked representative
    
    # Relationship
    user = relationship("User", back_populates="postal_code_history")


class UserProfilePicture(Base):
    """Model for tracking user profile picture changes."""
    
    __tablename__ = "user_profile_pictures"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    image_data = Column(Text, nullable=False)  # Base64 encoded image
    image_type = Column(String(10), nullable=False)  # jpg, png, gif
    file_size = Column(Integer, nullable=False)  # Size in bytes
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="profile_pictures")


class UserAccountDeletion(Base):
    """Model for tracking account deletion requests."""
    
    __tablename__ = "user_account_deletions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    deletion_reason = Column(Text, nullable=False)
    feedback = Column(Text, nullable=True)
    requested_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(20), default="pending", nullable=False)  # pending, approved, rejected
    
    # Relationship
    user = relationship("User", back_populates="account_deletions")
