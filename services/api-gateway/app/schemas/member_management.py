"""
Member Management Schemas

Pydantic schemas for member management functionality.
Implements FEAT-015 Member Management (P0 priority).
"""

from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID
import re


# Base schemas
class MemberManagementBase(BaseModel):
    """Base schema for member management."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=500)
    district: Optional[str] = Field(None, max_length=200)
    role: Optional[str] = Field(None, max_length=100)
    party_id: Optional[UUID] = None
    jurisdiction_id: UUID
    
    @validator('phone')
    def validate_phone(cls, v):
        if v and not re.match(r'^[\d\s\-\+\(\)]+$', v):
            raise ValueError('Invalid phone number format')
        return v


class MemberCreate(MemberManagementBase):
    """Schema for creating a member."""
    start_date: date
    end_date: Optional[date] = None
    bio: Optional[str] = None
    photo_url: Optional[str] = None
    
    @validator('end_date')
    def validate_dates(cls, v, values):
        if v and 'start_date' in values and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v


class MemberUpdate(BaseModel):
    """Schema for updating a member."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=500)
    district: Optional[str] = Field(None, max_length=200)
    role: Optional[str] = Field(None, max_length=100)
    party_id: Optional[UUID] = None
    jurisdiction_id: Optional[UUID] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    bio: Optional[str] = None
    photo_url: Optional[str] = None


class MemberManagementResponse(MemberManagementBase):
    """Schema for member management responses."""
    id: UUID
    full_name: str
    start_date: date
    end_date: Optional[date]
    bio: Optional[str]
    photo_url: Optional[str]
    party_name: Optional[str]
    jurisdiction_name: str
    is_current: bool
    created_at: datetime
    updated_at: datetime
    
    # Related counts
    contact_count: int = 0
    social_media_count: int = 0
    education_count: int = 0
    profession_count: int = 0
    tag_count: int = 0
    
    # Metrics
    activity_score: Optional[float] = None
    influence_score: Optional[float] = None
    
    class Config:
        orm_mode = True


# Contact schemas
class ContactBase(BaseModel):
    """Base contact schema."""
    contact_type: str = Field(..., regex="^(office|constituency|personal)$")
    address_line1: Optional[str] = Field(None, max_length=200)
    address_line2: Optional[str] = Field(None, max_length=200)
    city: Optional[str] = Field(None, max_length=100)
    province: Optional[str] = Field(None, max_length=50)
    postal_code: Optional[str] = Field(None, max_length=20)
    phone: Optional[str] = Field(None, max_length=50)
    fax: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    hours: Optional[Dict[str, Any]] = None
    is_primary: bool = False


class ContactCreate(ContactBase):
    """Schema for creating a contact."""
    member_id: UUID


class ContactUpdate(ContactBase):
    """Schema for updating a contact."""
    contact_type: Optional[str] = Field(None, regex="^(office|constituency|personal)$")


class ContactResponse(ContactBase):
    """Schema for contact responses."""
    id: UUID
    member_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Social media schemas
class SocialMediaBase(BaseModel):
    """Base social media schema."""
    platform: str = Field(..., regex="^(twitter|facebook|instagram|linkedin|youtube|tiktok)$")
    handle: str = Field(..., min_length=1, max_length=100)
    url: Optional[str] = Field(None, max_length=500)
    verified: bool = False
    is_active: bool = True


class SocialMediaCreate(SocialMediaBase):
    """Schema for creating social media."""
    member_id: UUID


class SocialMediaUpdate(BaseModel):
    """Schema for updating social media."""
    handle: Optional[str] = Field(None, min_length=1, max_length=100)
    url: Optional[str] = Field(None, max_length=500)
    verified: Optional[bool] = None
    is_active: Optional[bool] = None


class SocialMediaResponse(SocialMediaBase):
    """Schema for social media responses."""
    id: UUID
    member_id: UUID
    follower_count: Optional[int] = None
    last_verified: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Education schemas
class EducationBase(BaseModel):
    """Base education schema."""
    institution: str = Field(..., min_length=1, max_length=200)
    degree: Optional[str] = Field(None, max_length=200)
    field_of_study: Optional[str] = Field(None, max_length=200)
    start_year: Optional[int] = Field(None, ge=1900, le=2100)
    end_year: Optional[int] = Field(None, ge=1900, le=2100)
    graduated: Optional[bool] = None
    notes: Optional[str] = None
    display_order: int = 0


class EducationCreate(EducationBase):
    """Schema for creating education."""
    member_id: UUID


class EducationResponse(EducationBase):
    """Schema for education responses."""
    id: UUID
    member_id: UUID
    
    class Config:
        orm_mode = True


# Profession schemas
class ProfessionBase(BaseModel):
    """Base profession schema."""
    title: str = Field(..., min_length=1, max_length=200)
    organization: Optional[str] = Field(None, max_length=200)
    industry: Optional[str] = Field(None, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: bool = False
    description: Optional[str] = None
    display_order: int = 0


class ProfessionCreate(ProfessionBase):
    """Schema for creating profession."""
    member_id: UUID


class ProfessionResponse(ProfessionBase):
    """Schema for profession responses."""
    id: UUID
    member_id: UUID
    
    class Config:
        orm_mode = True


# Tag schemas
class TagBase(BaseModel):
    """Base tag schema."""
    name: str = Field(..., min_length=1, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    color: Optional[str] = Field(None, regex="^#[0-9A-Fa-f]{6}$")
    is_active: bool = True


class TagCreate(TagBase):
    """Schema for creating tag."""
    pass


class TagResponse(TagBase):
    """Schema for tag responses."""
    id: UUID
    created_at: datetime
    member_count: int = 0
    
    class Config:
        orm_mode = True


# Bulk operations schemas
class BulkMemberImport(BaseModel):
    """Schema for bulk member import."""
    import_source: str = Field(..., regex="^(openparliament|manual|csv|api)$")
    import_type: str = Field(..., regex="^(full|incremental|update)$")
    data_url: Optional[str] = None
    csv_data: Optional[str] = None
    member_data: Optional[List[MemberCreate]] = None
    update_existing: bool = True
    dry_run: bool = False


class BulkOperationRequest(BaseModel):
    """Schema for bulk operations."""
    member_ids: List[UUID]
    operation: str = Field(..., regex="^(delete|archive|tag|untag|export)$")
    parameters: Optional[Dict[str, Any]] = None
    reason: Optional[str] = None


class BulkOperationResponse(BaseModel):
    """Schema for bulk operation responses."""
    operation: str
    total_count: int
    success_count: int
    error_count: int
    errors: Optional[List[Dict[str, Any]]] = None
    duration_seconds: float


# Import status schemas
class ImportStatusResponse(BaseModel):
    """Schema for import status responses."""
    id: UUID
    import_source: str
    import_type: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime]
    total_records: Optional[int]
    processed_records: int
    created_count: int
    updated_count: int
    error_count: int
    errors: Optional[List[Dict[str, Any]]]
    
    class Config:
        orm_mode = True


# Audit schemas
class AuditLogResponse(BaseModel):
    """Schema for audit log responses."""
    id: UUID
    member_id: UUID
    user_id: UUID
    user_email: str
    action: str
    timestamp: datetime
    changes: Optional[Dict[str, Any]]
    reason: Optional[str]
    metadata: Optional[Dict[str, Any]]
    
    class Config:
        orm_mode = True


# Member metrics schemas
class MemberMetricsUpdate(BaseModel):
    """Schema for updating member metrics."""
    bills_sponsored: Optional[int] = None
    bills_cosponsored: Optional[int] = None
    votes_total: Optional[int] = None
    votes_yea: Optional[int] = None
    votes_nay: Optional[int] = None
    votes_abstain: Optional[int] = None
    attendance_rate: Optional[float] = Field(None, ge=0, le=100)
    speeches_count: Optional[int] = None
    questions_asked: Optional[int] = None
    committee_memberships: Optional[int] = None
    twitter_followers: Optional[int] = None
    facebook_likes: Optional[int] = None


class MemberMetricsResponse(BaseModel):
    """Schema for member metrics responses."""
    id: UUID
    member_id: UUID
    bills_sponsored: int
    bills_cosponsored: int
    votes_total: int
    votes_yea: int
    votes_nay: int
    votes_abstain: int
    attendance_rate: Optional[float]
    speeches_count: int
    questions_asked: int
    committee_memberships: int
    twitter_followers: Optional[int]
    facebook_likes: Optional[int]
    social_engagement_score: Optional[float]
    activity_score: Optional[float]
    influence_score: Optional[float]
    transparency_score: Optional[float]
    last_calculated: datetime
    
    class Config:
        orm_mode = True


# Search and filter schemas
class MemberSearchRequest(BaseModel):
    """Schema for advanced member search."""
    query: Optional[str] = None
    jurisdiction_ids: Optional[List[UUID]] = None
    party_ids: Optional[List[UUID]] = None
    districts: Optional[List[str]] = None
    roles: Optional[List[str]] = None
    tag_ids: Optional[List[UUID]] = None
    is_current: Optional[bool] = None
    has_social_media: Optional[bool] = None
    min_activity_score: Optional[float] = Field(None, ge=0, le=100)
    max_activity_score: Optional[float] = Field(None, ge=0, le=100)
    sort_by: str = Field("last_name", regex="^(last_name|first_name|district|activity_score|influence_score|created_at|updated_at)$")
    sort_order: str = Field("asc", regex="^(asc|desc)$")
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class MemberExportRequest(BaseModel):
    """Schema for member export."""
    format: str = Field(..., regex="^(csv|json|excel)$")
    fields: Optional[List[str]] = None
    include_contacts: bool = False
    include_social_media: bool = False
    include_education: bool = False
    include_professions: bool = False
    include_metrics: bool = False


class MemberDuplicateCheck(BaseModel):
    """Schema for checking duplicate members."""
    first_name: str
    last_name: str
    email: Optional[str] = None
    district: Optional[str] = None
    jurisdiction_id: Optional[UUID] = None


class MemberMergeRequest(BaseModel):
    """Schema for merging duplicate members."""
    primary_member_id: UUID
    duplicate_member_ids: List[UUID]
    merge_contacts: bool = True
    merge_social_media: bool = True
    merge_education: bool = True
    merge_professions: bool = True
    merge_tags: bool = True
    reason: str