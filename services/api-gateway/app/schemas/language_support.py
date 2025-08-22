"""
Language Support Schemas for OpenPolicy V2

Comprehensive Pydantic schemas for bilingual (French/English) language support.
Implements P1 priority feature for legal compliance and accessibility.
"""

from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class LanguageCodeEnum(str, Enum):
    """Language code enumeration."""
    ENGLISH = "en"
    FRENCH = "fr"


class DirectionEnum(str, Enum):
    """Text direction enumeration."""
    LEFT_TO_RIGHT = "ltr"
    RIGHT_TO_LEFT = "rtl"


class TimeFormatEnum(str, Enum):
    """Time format enumeration."""
    TWELVE_HOUR = "12h"
    TWENTY_FOUR_HOUR = "24h"


class ProficiencyLevelEnum(str, Enum):
    """Language proficiency level enumeration."""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    FLUENT = "fluent"


class TranslationStatusEnum(str, Enum):
    """Translation status enumeration."""
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    PUBLISHED = "published"


class TranslationQualityEnum(str, Enum):
    """Translation quality enumeration."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


# ============================================================================
# BASE MODELS
# ============================================================================

class LanguageBase(BaseModel):
    """Base model for languages."""
    model_config = ConfigDict(from_attributes=True)
    
    language_code: LanguageCodeEnum = Field(..., description="Language code (en, fr)")
    language_name: str = Field(..., min_length=1, max_length=100, description="Language name in English")
    language_name_native: str = Field(..., min_length=1, max_length=100, description="Language name in native language")
    is_active: bool = Field(True, description="Whether language is active")
    is_default: bool = Field(False, description="Whether language is default")
    direction: DirectionEnum = Field(DirectionEnum.LEFT_TO_RIGHT, description="Text direction")
    date_format: str = Field("YYYY-MM-DD", max_length=50, description="Date format")
    time_format: TimeFormatEnum = Field(TimeFormatEnum.TWENTY_FOUR_HOUR, description="Time format")
    number_format: str = Field("1,234.56", max_length=50, description="Number format")
    currency_code: str = Field("CAD", max_length=3, description="Currency code")


class TranslationBase(BaseModel):
    """Base model for translations."""
    model_config = ConfigDict(from_attributes=True)
    
    language_id: str = Field(..., description="Language ID")
    translation_key: str = Field(..., min_length=1, max_length=500, description="Translation key")
    translation_value: str = Field(..., min_length=1, description="Translated text")
    translation_context: Optional[str] = Field(None, max_length=200, description="Translation context")
    translation_notes: Optional[str] = Field(None, description="Notes for translators")
    is_approved: bool = Field(False, description="Whether translation is approved")
    approved_by: Optional[str] = Field(None, max_length=100, description="Who approved the translation")
    approved_at: Optional[datetime] = Field(None, description="When translation was approved")
    version: int = Field(1, ge=1, description="Translation version")


class UserLanguagePreferenceBase(BaseModel):
    """Base model for user language preferences."""
    model_config = ConfigDict(from_attributes=True)
    
    user_id: str = Field(..., description="User ID")
    language_id: str = Field(..., description="Language ID")
    is_primary: bool = Field(True, description="Whether this is primary language")
    is_secondary: bool = Field(False, description="Whether this is secondary language")
    proficiency_level: ProficiencyLevelEnum = Field(ProficiencyLevelEnum.FLUENT, description="Language proficiency level")


class ContentTranslationBase(BaseModel):
    """Base model for content translations."""
    model_config = ConfigDict(from_attributes=True)
    
    content_type: str = Field(..., min_length=1, max_length=100, description="Content type")
    content_id: str = Field(..., min_length=1, max_length=100, description="Content ID")
    language_id: str = Field(..., description="Language ID")
    field_name: str = Field(..., min_length=1, max_length=100, description="Field name being translated")
    translated_value: str = Field(..., min_length=1, description="Translated content")
    translation_status: TranslationStatusEnum = Field(TranslationStatusEnum.DRAFT, description="Translation status")
    translator_id: Optional[str] = Field(None, max_length=100, description="Translator ID")
    reviewer_id: Optional[str] = Field(None, max_length=100, description="Reviewer ID")
    review_notes: Optional[str] = Field(None, description="Review comments and notes")
    translation_quality: Optional[TranslationQualityEnum] = Field(None, description="Translation quality")


class LanguageContextBase(BaseModel):
    """Base model for language contexts."""
    model_config = ConfigDict(from_attributes=True)
    
    language_id: str = Field(..., description="Language ID")
    context_key: str = Field(..., min_length=1, max_length=200, description="Context key")
    context_value: Dict[str, Any] = Field(..., description="Context-specific settings and data")
    is_active: bool = Field(True, description="Whether context is active")


class TranslationMemoryBase(BaseModel):
    """Base model for translation memory."""
    model_config = ConfigDict(from_attributes=True)
    
    source_language_id: str = Field(..., description="Source language ID")
    target_language_id: str = Field(..., description="Target language ID")
    source_text: str = Field(..., min_length=1, description="Original text")
    target_text: str = Field(..., min_length=1, description="Translated text")
    source_hash: str = Field(..., min_length=64, max_length=64, description="Hash of source text")
    context: Optional[str] = Field(None, max_length=200, description="Translation context")
    domain: Optional[str] = Field(None, max_length=100, description="Translation domain")
    confidence_score: int = Field(100, ge=0, le=100, description="Confidence in translation quality")
    usage_count: int = Field(1, ge=1, description="Usage count")


class LanguageAnalyticsBase(BaseModel):
    """Base model for language analytics."""
    model_config = ConfigDict(from_attributes=True)
    
    language_id: str = Field(..., description="Language ID")
    analytics_date: datetime = Field(..., description="Analytics date")
    daily_active_users: int = Field(0, ge=0, description="Daily active users")
    daily_page_views: int = Field(0, ge=0, description="Daily page views")
    daily_translations_requested: int = Field(0, ge=0, description="Daily translation requests")
    daily_content_created: int = Field(0, ge=0, description="Daily content created")
    daily_content_updated: int = Field(0, ge=0, description="Daily content updated")
    translation_quality_score: float = Field(0.0, ge=0.0, le=100.0, description="Translation quality score")
    user_satisfaction_score: float = Field(0.0, ge=0.0, le=100.0, description="User satisfaction score")


# ============================================================================
# REQUEST MODELS
# ============================================================================

class LanguageCreateRequest(LanguageBase):
    """Request model for creating languages."""
    pass


class LanguageUpdateRequest(BaseModel):
    """Request model for updating languages."""
    language_name: Optional[str] = Field(None, min_length=1, max_length=100)
    language_name_native: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None
    direction: Optional[DirectionEnum] = None
    date_format: Optional[str] = Field(None, max_length=50)
    time_format: Optional[TimeFormatEnum] = None
    number_format: Optional[str] = Field(None, max_length=50)
    currency_code: Optional[str] = Field(None, max_length=3)


class TranslationCreateRequest(TranslationBase):
    """Request model for creating translations."""
    pass


class TranslationUpdateRequest(BaseModel):
    """Request model for updating translations."""
    translation_value: Optional[str] = Field(None, min_length=1)
    translation_context: Optional[str] = Field(None, max_length=200)
    translation_notes: Optional[str] = None
    is_approved: Optional[bool] = None
    approved_by: Optional[str] = Field(None, max_length=100)
    approved_at: Optional[datetime] = None
    version: Optional[int] = Field(None, ge=1)


class UserLanguagePreferenceCreateRequest(UserLanguagePreferenceBase):
    """Request model for creating user language preferences."""
    pass


class UserLanguagePreferenceUpdateRequest(BaseModel):
    """Request model for updating user language preferences."""
    is_primary: Optional[bool] = None
    is_secondary: Optional[bool] = None
    proficiency_level: Optional[ProficiencyLevelEnum] = None


class ContentTranslationCreateRequest(ContentTranslationBase):
    """Request model for creating content translations."""
    pass


class ContentTranslationUpdateRequest(BaseModel):
    """Request model for updating content translations."""
    translated_value: Optional[str] = Field(None, min_length=1)
    translation_status: Optional[TranslationStatusEnum] = None
    translator_id: Optional[str] = Field(None, max_length=100)
    reviewer_id: Optional[str] = Field(None, max_length=100)
    review_notes: Optional[str] = None
    translation_quality: Optional[TranslationQualityEnum] = None


class LanguageContextCreateRequest(LanguageContextBase):
    """Request model for creating language contexts."""
    pass


class LanguageContextUpdateRequest(BaseModel):
    """Request model for updating language contexts."""
    context_value: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class TranslationMemoryCreateRequest(TranslationMemoryBase):
    """Request model for creating translation memory."""
    pass


class TranslationMemoryUpdateRequest(BaseModel):
    """Request model for updating translation memory."""
    target_text: Optional[str] = Field(None, min_length=1)
    context: Optional[str] = Field(None, max_length=200)
    domain: Optional[str] = Field(None, max_length=100)
    confidence_score: Optional[int] = Field(None, ge=0, le=100)
    usage_count: Optional[int] = Field(None, ge=1)


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class LanguageResponse(LanguageBase):
    """Response model for languages."""
    id: str
    created_at: datetime
    updated_at: datetime


class TranslationResponse(TranslationBase):
    """Response model for translations."""
    id: str
    created_at: datetime
    updated_at: datetime


class UserLanguagePreferenceResponse(UserLanguagePreferenceBase):
    """Response model for user language preferences."""
    id: str
    created_at: datetime
    updated_at: datetime


class ContentTranslationResponse(ContentTranslationBase):
    """Response model for content translations."""
    id: str
    created_at: datetime
    updated_at: datetime


class LanguageContextResponse(LanguageContextBase):
    """Response model for language contexts."""
    id: str
    created_at: datetime
    updated_at: datetime


class TranslationMemoryResponse(TranslationMemoryBase):
    """Response model for translation memory."""
    id: str
    last_used: datetime
    created_at: datetime
    updated_at: datetime


class LanguageAnalyticsResponse(LanguageAnalyticsBase):
    """Response model for language analytics."""
    id: str
    created_at: datetime


# ============================================================================
# LIST RESPONSE MODELS
# ============================================================================

class LanguageListResponse(BaseModel):
    """List response model for languages."""
    languages: List[LanguageResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class TranslationListResponse(BaseModel):
    """List response model for translations."""
    translations: List[TranslationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class UserLanguagePreferenceListResponse(BaseModel):
    """List response model for user language preferences."""
    preferences: List[UserLanguagePreferenceResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class ContentTranslationListResponse(BaseModel):
    """List response model for content translations."""
    translations: List[ContentTranslationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class LanguageContextListResponse(BaseModel):
    """List response model for language contexts."""
    contexts: List[LanguageContextResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class TranslationMemoryListResponse(BaseModel):
    """List response model for translation memory."""
    memory: List[TranslationMemoryResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class LanguageAnalyticsListResponse(BaseModel):
    """List response model for language analytics."""
    analytics: List[LanguageAnalyticsResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


# ============================================================================
# UTILITY AND SPECIALIZED MODELS
# ============================================================================

class LanguageToggleRequest(BaseModel):
    """Request model for toggling user language."""
    language_code: LanguageCodeEnum = Field(..., description="Language code to switch to")
    remember_preference: bool = Field(True, description="Whether to remember this preference")


class TranslationSearchRequest(BaseModel):
    """Request model for searching translations."""
    query: str = Field(..., min_length=1, description="Search query")
    language_code: Optional[LanguageCodeEnum] = Field(None, description="Language to search in")
    context: Optional[str] = Field(None, description="Context to search in")
    is_approved: Optional[bool] = Field(None, description="Filter by approval status")
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")


class TranslationBulkRequest(BaseModel):
    """Request model for bulk translation operations."""
    translations: List[Dict[str, Any]] = Field(..., description="List of translations to process")
    operation: str = Field(..., description="Operation to perform (create, update, delete)")
    language_code: LanguageCodeEnum = Field(..., description="Target language code")


class LanguageStatistics(BaseModel):
    """Model for language usage statistics."""
    language_code: LanguageCodeEnum = Field(..., description="Language code")
    language_name: str = Field(..., description="Language name")
    total_users: int = Field(..., description="Total users using this language")
    total_translations: int = Field(..., description="Total translations available")
    total_content: int = Field(..., description="Total content in this language")
    coverage_percentage: float = Field(..., description="Translation coverage percentage")
    quality_score: float = Field(..., description="Average translation quality score")
    user_satisfaction: float = Field(..., description="User satisfaction score")
    last_updated: datetime = Field(..., description="Last update timestamp")


class SystemLanguageOverview(BaseModel):
    """Model for system-wide language overview."""
    total_languages: int = Field(..., description="Total supported languages")
    active_languages: int = Field(..., description="Number of active languages")
    default_language: LanguageCodeEnum = Field(..., description="Default language code")
    total_translations: int = Field(..., description="Total translations across all languages")
    total_users: int = Field(..., description="Total users with language preferences")
    coverage_by_language: Dict[str, float] = Field(..., description="Coverage percentage by language")
    quality_by_language: Dict[str, float] = Field(..., description="Quality score by language")
    generated_at: datetime = Field(..., description="When overview was generated")


class TranslationContext(BaseModel):
    """Model for translation context information."""
    context_key: str = Field(..., description="Context key")
    context_name: str = Field(..., description="Human-readable context name")
    description: str = Field(..., description="Context description")
    is_required: bool = Field(..., description="Whether context is required")
    supported_languages: List[LanguageCodeEnum] = Field(..., description="Supported languages for this context")
    translation_count: int = Field(..., description="Number of translations in this context")
    last_updated: datetime = Field(..., description="Last update timestamp")


class UserLanguageProfile(BaseModel):
    """Model for user language profile."""
    user_id: str = Field(..., description="User ID")
    primary_language: LanguageCodeEnum = Field(..., description="Primary language")
    secondary_languages: List[LanguageCodeEnum] = Field(..., description="Secondary languages")
    proficiency_levels: Dict[str, ProficiencyLevelEnum] = Field(..., description="Proficiency by language")
    preferred_interface_language: LanguageCodeEnum = Field(..., description="Preferred interface language")
    content_language_preferences: Dict[str, LanguageCodeEnum] = Field(..., description="Content language preferences by type")
    created_at: datetime = Field(..., description="Profile creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
