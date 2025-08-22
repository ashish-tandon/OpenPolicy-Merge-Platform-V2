from sqlalchemy import Column, String, DateTime, Boolean, Text, Index, ForeignKey, Date, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class User(Base):
    """Model for storing user accounts."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Enhanced profile fields
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    phone = Column(String(20), nullable=True)
    website = Column(String(500), nullable=True)
    location = Column(String(200), nullable=True)
    postal_code = Column(String(10), nullable=True)
    timezone = Column(String(50), nullable=True)
    language_preference = Column(String(10), default="en", nullable=False)
    
    # Social media
    twitter_handle = Column(String(100), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    facebook_url = Column(String(500), nullable=True)
    
    # Preferences and settings
    notification_email = Column(Boolean, default=True, nullable=False)
    notification_push = Column(Boolean, default=False, nullable=False)
    notification_sms = Column(Boolean, default=False, nullable=False)
    theme_preference = Column(String(20), default="light", nullable=False)
    privacy_level = Column(String(20), default="public", nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    last_activity = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user", cascade="all, delete-orphan")
    oauth_accounts = relationship("OAuthAccount", back_populates="user", cascade="all, delete-orphan")
    preferences = relationship("UserPreferences", back_populates="user", cascade="all, delete-orphan", uselist=False)
    activities = relationship("UserActivity", back_populates="user", cascade="all, delete-orphan")

    # Create indexes for efficient queries
    __table_args__ = (
        Index('idx_user_username', 'username'),
        Index('idx_user_email', 'email'),
        Index('idx_user_active', 'is_active'),
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

    def to_dict(self):
        """Convert model to dictionary (excluding sensitive data)."""
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "bio": self.bio,
            "avatar_url": self.avatar_url,
            "phone": self.phone,
            "website": self.website,
            "location": self.location,
            "postal_code": self.postal_code,
            "timezone": self.timezone,
            "language_preference": self.language_preference,
            "twitter_handle": self.twitter_handle,
            "linkedin_url": self.linkedin_url,
            "facebook_url": self.facebook_url,
            "notification_email": self.notification_email,
            "notification_push": self.notification_push,
            "notification_sms": self.notification_sms,
            "theme_preference": self.theme_preference,
            "privacy_level": self.privacy_level,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None
        }

class UserSession(Base):
    """Model for storing user sessions."""

    __tablename__ = "user_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="sessions")

    # Create indexes for efficient queries
    __table_args__ = (
        Index('idx_session_user_id', 'user_id'),
        Index('idx_session_token', 'session_token'),
        Index('idx_session_expires', 'expires_at'),
    )

    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id})>"

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class PasswordResetToken(Base):
    """Model for storing password reset tokens."""

    __tablename__ = "password_reset_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used_at = Column(DateTime(timezone=True), nullable=True)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="password_reset_tokens")

    # Create indexes for efficient queries
    __table_args__ = (
        Index('idx_reset_user_id', 'user_id'),
        Index('idx_reset_token', 'token'),
        Index('idx_reset_expires', 'expires_at'),
        Index('idx_reset_used', 'used_at'),
    )

    def __repr__(self):
        return f"<PasswordResetToken(id={self.id}, user_id={self.user_id})>"

    def is_valid(self):
        """Check if token is still valid (not expired and not used)."""
        from datetime import datetime, timezone
        return (
            self.used_at is None and
            self.expires_at > datetime.now(timezone.utc)
        )

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "used_at": self.used_at.isoformat() if self.used_at else None,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class OAuthAccount(Base):
    """Model for storing OAuth account information."""

    __tablename__ = "oauth_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    provider = Column(String(20), nullable=False)  # google, github, etc.
    provider_account_id = Column(String(255), nullable=False)  # OAuth provider's user ID
    access_token = Column(Text, nullable=True)  # Encrypted access token
    refresh_token = Column(Text, nullable=True)  # Encrypted refresh token
    expires_at = Column(DateTime(timezone=True), nullable=True)
    scope = Column(String(255), nullable=True)  # OAuth scopes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="oauth_accounts")

    # Create indexes for efficient queries
    __table_args__ = (
        Index('idx_oauth_user_id', 'user_id'),
        Index('idx_oauth_provider', 'provider'),
        Index('idx_oauth_provider_account_id', 'provider_account_id'),
        Index('idx_oauth_provider_user', 'provider', 'user_id'),
    )

    def __repr__(self):
        return f"<OAuthAccount(id={self.id}, user_id={self.user_id}, provider='{self.provider}')>"

    def to_dict(self):
        """Convert model to dictionary (excluding sensitive tokens)."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "provider": self.provider,
            "provider_account_id": self.provider_account_id,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "scope": self.scope,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# ============================================================================
# USER PREFERENCES AND SETTINGS
# ============================================================================

class UserPreferences(Base):
    """Model for storing user preferences and settings."""
    
    __tablename__ = "user_preferences"
    __table_args__ = {"schema": "public"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Content preferences
    favorite_topics = Column(Text, nullable=True)  # JSON array of favorite topics
    favorite_mps = Column(Text, nullable=True)    # JSON array of favorite MP IDs
    favorite_parties = Column(Text, nullable=True) # JSON array of favorite party IDs
    excluded_topics = Column(Text, nullable=True)  # JSON array of excluded topics
    content_difficulty = Column(String(20), default="intermediate", nullable=False)
    
    # Display preferences
    show_advanced_features = Column(Boolean, default=True, nullable=False)
    show_analytics = Column(Boolean, default=True, nullable=False)
    show_social_features = Column(Boolean, default=False, nullable=False)
    font_size = Column(String(20), default="medium", nullable=False)
    
    # Privacy settings
    profile_visibility = Column(String(20), default="public", nullable=False)
    activity_sharing = Column(String(20), default="friends_only", nullable=False)
    data_collection = Column(Boolean, default=True, nullable=False)
    third_party_sharing = Column(Boolean, default=False, nullable=False)
    
    # Accessibility
    high_contrast = Column(Boolean, default=False, nullable=False)
    screen_reader = Column(Boolean, default=False, nullable=False)
    keyboard_navigation = Column(Boolean, default=True, nullable=False)
    reduced_motion = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self):
        return f"<UserPreferences(user_id={self.user_id})>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "favorite_topics": self.favorite_topics,
            "favorite_mps": self.favorite_mps,
            "favorite_parties": self.favorite_parties,
            "excluded_topics": self.excluded_topics,
            "content_difficulty": self.content_difficulty,
            "show_advanced_features": self.show_advanced_features,
            "show_analytics": self.show_analytics,
            "show_social_features": self.show_social_features,
            "font_size": self.font_size,
            "profile_visibility": self.profile_visibility,
            "activity_sharing": self.activity_sharing,
            "data_collection": self.data_collection,
            "third_party_sharing": self.third_party_sharing,
            "high_contrast": self.high_contrast,
            "screen_reader": self.screen_reader,
            "keyboard_navigation": self.keyboard_navigation,
            "reduced_motion": self.reduced_motion,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class UserActivity(Base):
    """Model for tracking user activity and engagement."""
    
    __tablename__ = "user_activities"
    __table_args__ = {"schema": "public"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Activity details
    activity_type = Column(String(50), nullable=False)  # bill_view, mp_research, vote_analysis, etc.
    content_id = Column(String(100), nullable=True)     # ID of the content being interacted with
    content_type = Column(String(50), nullable=True)    # bill, mp, vote, debate, committee
    content_title = Column(String(500), nullable=True)  # Title/name of the content
    content_summary = Column(Text, nullable=True)       # Description of the activity
    
    # Interaction details
    time_spent = Column(Integer, nullable=True)         # Time spent in seconds
    pages_viewed = Column(Integer, nullable=True)      # Number of pages viewed
    actions_taken = Column(Text, nullable=True)        # JSON array of actions (read, bookmark, share, etc.)
    
    # Related content
    related_bills = Column(Text, nullable=True)        # JSON array of related bill IDs
    related_mps = Column(Text, nullable=True)          # JSON array of related MP IDs
    related_committees = Column(Text, nullable=True)   # JSON array of related committee IDs
    
    # Metadata
    device = Column(String(50), nullable=True)         # Desktop, Mobile, Tablet
    browser = Column(String(50), nullable=True)        # Chrome, Firefox, Safari, etc.
    location = Column(String(200), nullable=True)      # User's location
    ip_address = Column(String(45), nullable=True)     # IP address for analytics
    
    # Timestamps
    activity_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self):
        return f"<UserActivity(user_id={self.user_id}, activity_type='{self.activity_type}')>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "activity_type": self.activity_type,
            "content_id": self.content_id,
            "content_type": self.content_type,
            "content_title": self.content_title,
            "content_summary": self.content_summary,
            "time_spent": self.time_spent,
            "pages_viewed": self.pages_viewed,
            "actions_taken": self.actions_taken,
            "related_bills": self.related_bills,
            "related_mps": self.related_mps,
            "related_committees": self.related_committees,
            "device": self.device,
            "browser": self.browser,
            "location": self.location,
            "ip_address": self.ip_address,
            "activity_date": self.activity_date.isoformat() if self.activity_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
