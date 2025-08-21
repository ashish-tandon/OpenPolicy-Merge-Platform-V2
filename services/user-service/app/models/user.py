"""
User model for the User Service.

Separate from legislative data models to maintain clean architecture.
Based on legacy Open Policy Infra patterns.
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class UserRole(str, enum.Enum):
    """User roles for access control."""
    NORMAL = "normal"
    ENTERPRISE = "enterprise"
    REPRESENTATIVE = "representative"
    MODERATOR = "moderator"
    ADMIN = "admin"


class AccountType(str, enum.Enum):
    """Account types for user classification."""
    CONSUMER = "consumer"
    INTERNAL = "internal"
    TEST = "test"


class UserStatus(str, enum.Enum):
    """User account status."""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    PENDING = "pending"
    DEACTIVATED = "deactivated"


class User(Base):
    """User model for authentication and user management."""
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    
    # Basic information
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), unique=True, nullable=True, index=True)
    postal_code = Column(String(10), nullable=True)
    
    # Additional fields from Open Policy Infra
    gender = Column(String(10), nullable=True)  # male, female, other
    age = Column(Integer, nullable=True)  # Age in years
    date_of_birth = Column(DateTime(timezone=True), nullable=True)  # Date of birth
    
    # Authentication
    password_hash = Column(String(255), nullable=True)  # Nullable for OAuth users
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    phone_verified_at = Column(DateTime(timezone=True), nullable=True)
    
    # Security features
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(255), nullable=True)
    
    # User classification
    role = Column(Enum(UserRole), default=UserRole.NORMAL, nullable=False)
    account_type = Column(Enum(AccountType), default=AccountType.CONSUMER, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE, nullable=False)
    
    # Metadata
    avatar_url = Column(String(500), nullable=True)  # Profile picture URL
    profile_picture = Column(Text, nullable=True)  # Base64 encoded image
    preferences = Column(Text, nullable=True)  # JSON string for user preferences
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    # Soft delete
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    account_deletion_reason = Column(Text, nullable=True)
    
    # Relationships for user engagement
    bill_votes = relationship("BillVoteCast", back_populates="user", cascade="all, delete-orphan")
    saved_bills = relationship("SavedBill", back_populates="user", cascade="all, delete-orphan")
    representative_issues = relationship("RepresentativeIssue", back_populates="user", cascade="all, delete-orphan")
    postal_code_history = relationship("UserPostalCodeHistory", back_populates="user", cascade="all, delete-orphan")
    profile_pictures = relationship("UserProfilePicture", back_populates="user", cascade="all, delete-orphan")
    account_deletions = relationship("UserAccountDeletion", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_verified(self) -> bool:
        """Check if user's email is verified."""
        return self.email_verified_at is not None
    
    @property
    def is_active(self) -> bool:
        """Check if user account is active."""
        return self.status == UserStatus.ACTIVE and self.deleted_at is None
