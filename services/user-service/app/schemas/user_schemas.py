"""
User schemas compatible with FastAPI Users.

These schemas extend the base FastAPI Users schemas with our custom fields.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from fastapi_users import schemas
from app.models.user import UserRole, AccountType, UserStatus


class UserRead(schemas.BaseUser[str]):
    """User read schema with all fields."""
    
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    postal_code: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    date_of_birth: Optional[str] = None
    role: UserRole
    account_type: AccountType
    status: UserStatus
    avatar_url: Optional[str] = None
    profile_picture: Optional[str] = None
    preferences: Optional[str] = None
    created_at: str
    updated_at: str
    last_login_at: Optional[str] = None
    
    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    """User creation schema."""
    
    first_name: str = Field(..., min_length=1, max_length=255)
    last_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    postal_code: Optional[str] = Field(None, max_length=10)
    gender: Optional[str] = Field(None, max_length=10)
    age: Optional[int] = Field(None, ge=0, le=150)
    date_of_birth: Optional[str] = None
    role: UserRole = UserRole.NORMAL
    account_type: AccountType = AccountType.CONSUMER
    password: str = Field(..., min_length=8)


class UserUpdate(schemas.BaseUserUpdate):
    """User update schema."""
    
    first_name: Optional[str] = Field(None, min_length=1, max_length=255)
    last_name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    postal_code: Optional[str] = Field(None, max_length=10)
    gender: Optional[str] = Field(None, max_length=10)
    age: Optional[int] = Field(None, ge=0, le=150)
    date_of_birth: Optional[str] = None
    avatar_url: Optional[str] = None
    profile_picture: Optional[str] = None
    preferences: Optional[str] = None


class UserProfileUpdate(BaseModel):
    """User profile update schema."""
    
    first_name: Optional[str] = Field(None, min_length=1, max_length=255)
    last_name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    postal_code: Optional[str] = Field(None, max_length=10)
    gender: Optional[str] = Field(None, max_length=10)
    age: Optional[int] = Field(None, ge=0, le=150)
    date_of_birth: Optional[str] = None
    preferences: Optional[str] = None


class UserRoleUpdate(BaseModel):
    """User role update schema."""
    
    role: UserRole


class UserStatusUpdate(BaseModel):
    """User status update schema."""
    
    status: UserStatus
    reason: Optional[str] = None


class UserAnalytics(BaseModel):
    """User analytics data."""
    
    votes_cast: int = 0
    saved_bills: int = 0
    issues_raised: int = 0
    total_engagement: int = 0
    
    def __init__(self, **data):
        super().__init__(**data)
        self.total_engagement = self.votes_cast + self.saved_bills + self.issues_raised


class AccountDeletionRequest(BaseModel):
    """Account deletion request schema."""
    
    email: EmailStr
    reason: str = Field(..., min_length=1, max_length=500)
    feedback: Optional[str] = Field(None, max_length=1000)


class PasswordChangeRequest(BaseModel):
    """Password change request schema."""
    
    current_password: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str
    
    def validate_passwords(self):
        """Validate that new password and confirmation match."""
        if self.new_password != self.confirm_password:
            raise ValueError("New password and confirmation do not match")
        return True
