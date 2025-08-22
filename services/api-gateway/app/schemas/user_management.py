"""
Enhanced User Management Schemas for OpenPolicy V2

Comprehensive schemas for user profiles, preferences, and activity tracking.
This implements Feature F008: User Management (Authentication and Profile Management)
"""

from datetime import datetime, date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr, validator
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class ThemeEnum(str, Enum):
    """Theme preference enumeration"""
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"


class PrivacyLevelEnum(str, Enum):
    """Privacy level enumeration"""
    PUBLIC = "public"
    FRIENDS_ONLY = "friends_only"
    PRIVATE = "private"


class ContentDifficultyEnum(str, Enum):
    """Content difficulty level enumeration"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class NotificationFrequencyEnum(str, Enum):
    """Notification frequency enumeration"""
    REALTIME = "realtime"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    NEVER = "never"


# ============================================================================
# BASE MODELS
# ============================================================================

class UserProfileBase(BaseModel):
    """Base user profile model"""
    username: str = Field(..., description="Unique username")
    email: EmailStr = Field(..., description="User email address")
    full_name: str = Field(..., description="User's full name")
    bio: Optional[str] = Field(None, description="User biography")
    avatar_url: Optional[str] = Field(None, description="Avatar image URL")
    phone: Optional[str] = Field(None, description="Phone number")
    website: Optional[str] = Field(None, description="Personal website")
    location: Optional[str] = Field(None, description="User location")
    postal_code: Optional[str] = Field(None, description="Postal code")
    timezone: Optional[str] = Field(None, description="User timezone")
    language_preference: str = Field("en", description="Language preference")


class UserPreferencesBase(BaseModel):
    """Base user preferences model"""
    # Content preferences
    favorite_topics: Optional[List[str]] = Field(None, description="Favorite topics")
    favorite_mps: Optional[List[str]] = Field(None, description="Favorite MP IDs")
    favorite_parties: Optional[List[str]] = Field(None, description="Favorite party IDs")
    excluded_topics: Optional[List[str]] = Field(None, description="Excluded topics")
    content_difficulty: ContentDifficultyEnum = Field(ContentDifficultyEnum.INTERMEDIATE, description="Content difficulty preference")
    
    # Display preferences
    show_advanced_features: bool = Field(True, description="Show advanced features")
    show_analytics: bool = Field(True, description="Show analytics")
    show_social_features: bool = Field(False, description="Show social features")
    font_size: str = Field("medium", description="Font size preference")
    theme_preference: ThemeEnum = Field(ThemeEnum.LIGHT, description="Theme preference")
    
    # Privacy settings
    profile_visibility: PrivacyLevelEnum = Field(PrivacyLevelEnum.PUBLIC, description="Profile visibility")
    activity_sharing: PrivacyLevelEnum = Field(PrivacyLevelEnum.FRIENDS_ONLY, description="Activity sharing level")
    data_collection: bool = Field(True, description="Allow data collection")
    third_party_sharing: bool = Field(False, description="Allow third-party sharing")
    
    # Accessibility
    high_contrast: bool = Field(False, description="High contrast mode")
    screen_reader: bool = Field(False, description="Screen reader support")
    keyboard_navigation: bool = Field(True, description="Keyboard navigation support")
    reduced_motion: bool = Field(False, description="Reduced motion")


class UserActivityBase(BaseModel):
    """Base user activity model"""
    activity_type: str = Field(..., description="Type of activity")
    content_id: Optional[str] = Field(None, description="Content ID")
    content_type: Optional[str] = Field(None, description="Content type")
    content_title: Optional[str] = Field(None, description="Content title")
    content_summary: Optional[str] = Field(None, description="Activity summary")
    time_spent: Optional[int] = Field(None, description="Time spent in seconds")
    pages_viewed: Optional[int] = Field(None, description="Pages viewed")
    actions_taken: Optional[List[str]] = Field(None, description="Actions taken")
    device: Optional[str] = Field(None, description="Device type")
    browser: Optional[str] = Field(None, description="Browser type")
    location: Optional[str] = Field(None, description="User location")


# ============================================================================
# REQUEST MODELS
# ============================================================================

class UserCreateRequest(UserProfileBase):
    """Request model for creating a new user"""
    password: str = Field(..., description="User password", min_length=8)
    confirm_password: str = Field(..., description="Password confirmation")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v


class UserUpdateRequest(BaseModel):
    """Request model for updating user profile"""
    full_name: Optional[str] = Field(None, description="Full name")
    bio: Optional[str] = Field(None, description="Biography")
    avatar_url: Optional[str] = Field(None, description="Avatar URL")
    phone: Optional[str] = Field(None, description="Phone number")
    website: Optional[str] = Field(None, description="Website")
    location: Optional[str] = Field(None, description="Location")
    postal_code: Optional[str] = Field(None, description="Postal code")
    timezone: Optional[str] = Field(None, description="Timezone")
    language_preference: Optional[str] = Field(None, description="Language preference")
    twitter_handle: Optional[str] = Field(None, description="Twitter handle")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn URL")
    facebook_url: Optional[str] = Field(None, description="Facebook URL")


class UserPreferencesUpdateRequest(UserPreferencesBase):
    """Request model for updating user preferences"""
    pass


class PasswordChangeRequest(BaseModel):
    """Request model for changing password"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., description="New password", min_length=8)
    confirm_password: str = Field(..., description="Password confirmation")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class UserActivityCreateRequest(UserActivityBase):
    """Request model for creating user activity"""
    pass


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class UserProfileResponse(UserProfileBase):
    """Response model for user profile"""
    id: str = Field(..., description="User ID")
    is_active: bool = Field(..., description="Account active status")
    is_verified: bool = Field(..., description="Email verification status")
    created_at: datetime = Field(..., description="Account creation date")
    updated_at: datetime = Field(..., description="Last update date")
    last_login: Optional[datetime] = Field(None, description="Last login date")
    last_activity: Optional[datetime] = Field(None, description="Last activity date")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "username": "john_doe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "bio": "Political science enthusiast",
                "avatar_url": "https://example.com/avatar.jpg",
                "phone": "+1-555-123-4567",
                "website": "https://johndoe.com",
                "location": "Toronto, ON",
                "postal_code": "M5V 3A8",
                "timezone": "America/Toronto",
                "language_preference": "en",
                "is_active": True,
                "is_verified": True,
                "created_at": "2025-01-15T10:00:00Z",
                "updated_at": "2025-01-15T10:00:00Z"
            }
        }


class UserPreferencesResponse(UserPreferencesBase):
    """Response model for user preferences"""
    id: str = Field(..., description="Preferences ID")
    user_id: str = Field(..., description="User ID")
    created_at: datetime = Field(..., description="Creation date")
    updated_at: datetime = Field(..., description="Last update date")


class UserActivityResponse(UserActivityBase):
    """Response model for user activity"""
    id: str = Field(..., description="Activity ID")
    user_id: str = Field(..., description="User ID")
    related_bills: Optional[List[str]] = Field(None, description="Related bill IDs")
    related_mps: Optional[List[str]] = Field(None, description="Related MP IDs")
    related_committees: Optional[List[str]] = Field(None, description="Related committee IDs")
    ip_address: Optional[str] = Field(None, description="IP address")
    activity_date: datetime = Field(..., description="Activity date")
    created_at: datetime = Field(..., description="Creation date")


class UserListResponse(BaseModel):
    """Response model for user list"""
    users: List[UserProfileResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Has next page")
    has_prev: bool = Field(..., description="Has previous page")


class UserActivityListResponse(BaseModel):
    """Response model for user activity list"""
    activities: List[UserActivityResponse] = Field(..., description="List of activities")
    total: int = Field(..., description="Total number of activities")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Has next page")
    has_prev: bool = Field(..., description="Has previous page")


class UserStatsResponse(BaseModel):
    """Response model for user statistics"""
    user_id: str = Field(..., description="User ID")
    total_activities: int = Field(..., description="Total activities")
    total_bills_viewed: int = Field(..., description="Total bills viewed")
    total_mps_researched: int = Field(..., description="Total MPs researched")
    total_votes_analyzed: int = Field(..., description="Total votes analyzed")
    favorite_topics: List[str] = Field(..., description="Favorite topics")
    favorite_mps: List[str] = Field(..., description="Favorite MPs")
    favorite_parties: List[str] = Field(..., description="Favorite parties")
    engagement_score: float = Field(..., description="User engagement score")
    last_activity: Optional[datetime] = Field(None, description="Last activity date")
    generated_at: datetime = Field(..., description="Statistics generation date")


class UserSearchResponse(BaseModel):
    """Response model for user search"""
    query: str = Field(..., description="Search query")
    results: List[UserProfileResponse] = Field(..., description="Search results")
    total_results: int = Field(..., description="Total results")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")
    total_pages: int = Field(..., description="Total pages")


# ============================================================================
# NOTIFICATION MODELS
# ============================================================================

class NotificationSettings(BaseModel):
    """Model for notification settings"""
    email: bool = Field(True, description="Email notifications enabled")
    push: bool = Field(False, description="Push notifications enabled")
    sms: bool = Field(False, description="SMS notifications enabled")
    email_frequency: NotificationFrequencyEnum = Field(NotificationFrequencyEnum.DAILY, description="Email frequency")
    push_frequency: NotificationFrequencyEnum = Field(NotificationFrequencyEnum.REALTIME, description="Push frequency")
    notification_types: List[str] = Field(["bill_updates", "mp_activity", "vote_results"], description="Notification types")


class NotificationPreferencesResponse(BaseModel):
    """Response model for notification preferences"""
    user_id: str = Field(..., description="User ID")
    settings: NotificationSettings = Field(..., description="Notification settings")
    updated_at: datetime = Field(..., description="Last update date")


# ============================================================================
# VALIDATION MODELS
# ============================================================================

class UserValidationResponse(BaseModel):
    """Response model for user validation"""
    is_valid: bool = Field(..., description="Validation result")
    errors: List[str] = Field(..., description="Validation errors")
    warnings: List[str] = Field(..., description="Validation warnings")
    suggestions: List[str] = Field(..., description="Improvement suggestions")


class UserImportResponse(BaseModel):
    """Response model for user import"""
    total_processed: int = Field(..., description="Total records processed")
    successful_imports: int = Field(..., description="Successful imports")
    failed_imports: int = Field(..., description="Failed imports")
    errors: List[Dict[str, Any]] = Field(..., description="Import errors")
    warnings: List[str] = Field(..., description="Import warnings")
