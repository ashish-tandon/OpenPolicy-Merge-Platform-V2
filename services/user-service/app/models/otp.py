"""
OTP model for Multi-Factor Authentication.

Based on legacy Open Policy Infra patterns.
"""

from sqlalchemy import Column, String, DateTime, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OTP(Base):
    """One-Time Password model for MFA."""
    
    __tablename__ = "otps"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    
    # OTP details
    phone = Column(String(20), nullable=False, index=True)  # Phone number or email
    otp = Column(String(10), nullable=False)  # The OTP code
    otp_type = Column(String(20), default="sms", nullable=False)  # sms, email, totp
    
    # Expiration and usage
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False, nullable=False)
    attempts = Column(Integer, default=0, nullable=False)  # Number of attempts to use OTP
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    used_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<OTP(id={self.id}, phone='{self.phone}', type='{self.otp_type}')>"
    
    @property
    def is_expired(self) -> bool:
        """Check if OTP has expired."""
        from datetime import datetime
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_valid(self) -> bool:
        """Check if OTP is valid and can be used."""
        return not self.used and not self.is_expired and self.attempts < 3
