"""
Authentication and Authorization Schemas

Pydantic schemas for authentication and RBAC system.
Implements FEAT-014 Authentication System (P0 priority).
"""

from pydantic import BaseModel, EmailStr, Field, validator, SecretStr
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID
import re


# Validators
def validate_password(v: str) -> str:
    """Validate password strength."""
    if len(v) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", v):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", v):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", v):
        raise ValueError("Password must contain at least one digit")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
        raise ValueError("Password must contain at least one special character")
    return v


# User schemas
class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool = True
    preferences: Optional[Dict[str, Any]] = Field(default_factory=dict)


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        return validate_password(v)


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    preferences: Optional[Dict[str, Any]] = None
    
    @validator('password')
    def validate_password(cls, v):
        if v is not None:
            return validate_password(v)
        return v


class UserPasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str
    
    @validator('new_password')
    def validate_password(cls, v):
        return validate_password(v)


class UserResponse(UserBase):
    """Schema for user responses."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    email_verified: bool = False
    roles: List[str] = Field(default_factory=list)
    
    class Config:
        orm_mode = True


# Auth schemas
class LoginRequest(BaseModel):
    """Schema for login requests."""
    username: str = Field(..., description="Email or username")
    password: str
    remember_me: bool = False


class TokenResponse(BaseModel):
    """Schema for token responses."""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class TokenRefreshRequest(BaseModel):
    """Schema for token refresh requests."""
    refresh_token: str


class TokenVerifyRequest(BaseModel):
    """Schema for token verification requests."""
    token: str


class TokenPayload(BaseModel):
    """Schema for JWT token payload."""
    sub: str  # User ID
    exp: int  # Expiration timestamp
    iat: int  # Issued at timestamp
    type: str  # Token type: access or refresh
    roles: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)


# Role schemas
class RoleBase(BaseModel):
    """Base role schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class RoleCreate(RoleBase):
    """Schema for creating a role."""
    permission_ids: List[UUID] = Field(default_factory=list)


class RoleUpdate(BaseModel):
    """Schema for updating a role."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    permission_ids: Optional[List[UUID]] = None


class RoleResponse(RoleBase):
    """Schema for role responses."""
    id: UUID
    is_system: bool
    permissions: List['PermissionResponse']
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Permission schemas
class PermissionBase(BaseModel):
    """Base permission schema."""
    name: str = Field(..., min_length=1, max_length=100)
    resource: str = Field(..., min_length=1, max_length=100)
    action: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None


class PermissionCreate(PermissionBase):
    """Schema for creating a permission."""
    pass


class PermissionResponse(PermissionBase):
    """Schema for permission responses."""
    id: UUID
    created_at: datetime
    
    class Config:
        orm_mode = True


# User-Role management schemas
class UserRoleAssignment(BaseModel):
    """Schema for assigning roles to users."""
    user_id: UUID
    role_ids: List[UUID]


class UserRoleResponse(BaseModel):
    """Schema for user-role responses."""
    user_id: UUID
    roles: List[RoleResponse]


# API Key schemas
class APIKeyCreate(BaseModel):
    """Schema for creating an API key."""
    name: str = Field(..., min_length=1, max_length=200)
    scopes: Optional[List[str]] = None
    expires_at: Optional[datetime] = None
    service_name: Optional[str] = Field(None, max_length=100)


class APIKeyResponse(BaseModel):
    """Schema for API key responses (without sensitive data)."""
    id: UUID
    name: str
    prefix: str
    scopes: Optional[List[str]]
    is_active: bool
    expires_at: Optional[datetime]
    last_used_at: Optional[datetime]
    created_at: datetime
    service_name: Optional[str]
    
    class Config:
        orm_mode = True


class APIKeyCreateResponse(APIKeyResponse):
    """Schema for API key creation response (includes the key once)."""
    api_key: str  # Only returned on creation


# Permission check schemas
class PermissionCheckRequest(BaseModel):
    """Schema for permission check requests."""
    user_id: UUID
    resource: str
    action: str


class PermissionCheckResponse(BaseModel):
    """Schema for permission check responses."""
    allowed: bool
    user_id: UUID
    resource: str
    action: str
    roles: List[str] = Field(default_factory=list)


# Session schemas
class SessionResponse(BaseModel):
    """Schema for session responses."""
    user: UserResponse
    permissions: List[str]
    expires_at: datetime


# OAuth schemas
class OAuthAuthorizeRequest(BaseModel):
    """Schema for OAuth authorization requests."""
    client_id: str
    redirect_uri: str
    response_type: str = "code"
    scope: Optional[str] = None
    state: Optional[str] = None


class OAuthTokenRequest(BaseModel):
    """Schema for OAuth token requests."""
    grant_type: str = Field(..., regex="^(authorization_code|refresh_token|client_credentials)$")
    code: Optional[str] = None
    refresh_token: Optional[str] = None
    client_id: str
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    scope: Optional[str] = None


# Forward references
RoleResponse.update_forward_refs()
UserResponse.update_forward_refs()