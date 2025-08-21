"""
Pydantic schemas for User Service API.

Separate from legislative data schemas to maintain clean architecture.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from app.models.user import UserRole, AccountType, UserStatus


# Base schemas
class UserBase(BaseModel):
    """Base user schema."""
    first_name: str = Field(..., min_length=1, max_length=255)
    last_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    postal_code: Optional[str] = Field(None, max_length=10)
    role: UserRole = UserRole.NORMAL
    account_type: AccountType = AccountType.CONSUMER


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, max_length=128)
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=255)
    last_name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    postal_code: Optional[str] = Field(None, max_length=10)
    avatar_url: Optional[str] = Field(None, max_length=500)
    preferences: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: str
    email_verified_at: Optional[datetime]
    phone_verified_at: Optional[datetime]
    two_factor_enabled: bool
    status: UserStatus
    avatar_url: Optional[str]
    preferences: Optional[str]
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Authentication schemas
class LoginRequest(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class OAuthLoginRequest(BaseModel):
    """Schema for OAuth login."""
    provider: str = Field(..., pattern="^(google|github)$")
    token: str


class OTPRequest(BaseModel):
    """Schema for requesting OTP."""
    phone: str = Field(..., max_length=20)
    otp_type: str = Field(default="sms", pattern="^(sms|email)$")


class OTPVerifyRequest(BaseModel):
    """Schema for verifying OTP."""
    phone: str = Field(..., max_length=20)
    otp: str = Field(..., min_length=4, max_length=10)
    otp_type: str = Field(default="sms", pattern="^(sms|email)$")


class ForgotPasswordRequest(BaseModel):
    """Schema for forgot password request."""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Schema for resetting password."""
    email: EmailStr
    otp: str = Field(..., min_length=4, max_length=10)
    new_password: str = Field(..., min_length=8, max_length=128)
    
    @validator('new_password')
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v


# Response schemas
class AuthResponse(BaseModel):
    """Schema for authentication response."""
    success: bool
    message: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class OTPResponse(BaseModel):
    """Schema for OTP response."""
    success: bool
    message: str
    otp_sent: bool
    expires_in_minutes: int = 15


class PasswordResetResponse(BaseModel):
    """Schema for password reset response."""
    success: bool
    message: str


class LogoutResponse(BaseModel):
    """Schema for logout response."""
    success: bool
    message: str


# User management schemas
class UserListResponse(BaseModel):
    """Schema for user list response."""
    users: List[UserResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class UserRoleUpdate(BaseModel):
    """Schema for updating user role."""
    role: UserRole


class UserStatusUpdate(BaseModel):
    """Schema for updating user status."""
    status: UserStatus
    reason: Optional[str] = None


# Health check schema
class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str
    service: str
    version: str
    timestamp: datetime
    database: str
    redis: str
