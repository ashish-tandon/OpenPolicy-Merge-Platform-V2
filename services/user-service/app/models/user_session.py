"""
User session model for tracking active user sessions.

Separate from legislative data to maintain clean architecture.
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserSession(Base):
    """User session model for authentication tracking."""
    
    __tablename__ = "user_sessions"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    
    # User relationship
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Session details
    session_token = Column(String(500), nullable=False, unique=True, index=True)
    refresh_token = Column(String(500), nullable=True, unique=True, index=True)
    token_type = Column(String(20), default="jwt", nullable=False)  # jwt, oauth, api_key
    
    # Device information
    user_agent = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    device_type = Column(String(50), nullable=True)  # mobile, desktop, tablet
    
    # Session status
    is_active = Column(Boolean, default=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_used_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id}, token_type='{self.token_type}')>"
    
    @property
    def is_expired(self) -> bool:
        """Check if session has expired."""
        from datetime import datetime
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_valid(self) -> bool:
        """Check if session is valid and active."""
        return self.is_active and not self.is_expired and self.revoked_at is None
