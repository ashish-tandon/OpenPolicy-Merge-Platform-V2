"""
RSS Feed Schemas for OpenPolicy V2

Comprehensive Pydantic schemas for RSS feed generation and management.
Implements P2 priority feature for enhanced content distribution.
"""

from pydantic import BaseModel, Field, ConfigDict, HttpUrl, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class FeedTypeEnum(str, Enum):
    """RSS feed type enumeration."""
    BILLS = "bills"
    VOTES = "votes"
    COMMITTEES = "committees"
    MEMBERS = "members"
    DEBATES = "debates"
    ALL = "all"


class ContentTypeEnum(str, Enum):
    """RSS content type enumeration."""
    BILL = "bill"
    VOTE = "vote"
    COMMITTEE = "committee"
    MEMBER = "member"
    DEBATE = "debate"
    ANNOUNCEMENT = "announcement"


class LanguageEnum(str, Enum):
    """Language enumeration."""
    ENGLISH = "en"
    FRENCH = "fr"


class SubscriptionSourceEnum(str, Enum):
    """Subscription source enumeration."""
    DIRECT = "direct"
    EMAIL = "email"
    API = "api"
    WIDGET = "widget"


# ============================================================================
# BASE MODELS
# ============================================================================

class RSSFeedBase(BaseModel):
    """Base model for RSS feeds."""
    model_config = ConfigDict(from_attributes=True)
    
    feed_name: str = Field(..., min_length=1, max_length=200, description="Feed name (URL-friendly)")
    feed_title: str = Field(..., min_length=1, max_length=500, description="Feed title")
    feed_description: str = Field(..., min_length=1, description="Feed description")
    feed_type: FeedTypeEnum = Field(..., description="Type of content in feed")
    feed_url: str = Field(..., min_length=1, max_length=500, description="Feed URL path")
    feed_language: LanguageEnum = Field(LanguageEnum.ENGLISH, description="Feed language")
    is_active: bool = Field(True, description="Whether feed is active")
    is_public: bool = Field(True, description="Whether feed is publicly accessible")
    max_items: int = Field(50, ge=1, le=1000, description="Maximum items in feed")
    update_frequency_minutes: int = Field(60, ge=5, le=1440, description="Update frequency in minutes")
    filter_criteria: Optional[Dict[str, Any]] = Field(None, description="Additional filtering options")
    custom_styling: Optional[Dict[str, Any]] = Field(None, description="Custom RSS styling options")


class RSSFeedItemBase(BaseModel):
    """Base model for RSS feed items."""
    model_config = ConfigDict(from_attributes=True)
    
    feed_id: str = Field(..., description="Feed ID")
    item_title: str = Field(..., min_length=1, max_length=500, description="Item title")
    item_description: str = Field(..., min_length=1, description="Item description")
    item_link: str = Field(..., min_length=1, max_length=1000, description="Item link URL")
    item_guid: str = Field(..., min_length=1, max_length=500, description="Unique item identifier")
    item_pub_date: datetime = Field(..., description="Publication date")
    item_category: Optional[str] = Field(None, max_length=100, description="Item category")
    item_author: Optional[str] = Field(None, max_length=200, description="Item author")
    content_type: ContentTypeEnum = Field(..., description="Type of content")
    content_id: str = Field(..., min_length=1, max_length=100, description="Content ID")
    item_content: Optional[str] = Field(None, description="Full item content")
    item_summary: Optional[str] = Field(None, description="Item summary/excerpt")
    is_featured: bool = Field(False, description="Whether item is featured")
    item_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class RSSSubscriptionBase(BaseModel):
    """Base model for RSS subscriptions."""
    model_config = ConfigDict(from_attributes=True)
    
    feed_id: str = Field(..., description="Feed ID")
    subscriber_email: Optional[str] = Field(None, description="Subscriber email")
    subscriber_ip: Optional[str] = Field(None, description="Subscriber IP address")
    subscriber_user_agent: Optional[str] = Field(None, description="Subscriber user agent")
    subscription_source: SubscriptionSourceEnum = Field(SubscriptionSourceEnum.DIRECT, description="Subscription source")


class RSSAnalyticsBase(BaseModel):
    """Base model for RSS analytics."""
    model_config = ConfigDict(from_attributes=True)
    
    feed_id: str = Field(..., description="Feed ID")
    analytics_date: datetime = Field(..., description="Analytics date")
    daily_views: int = Field(0, ge=0, description="Daily views")
    daily_subscribers: int = Field(0, ge=0, description="Daily new subscribers")
    daily_unsubscribes: int = Field(0, ge=0, description="Daily unsubscribes")
    items_generated: int = Field(0, ge=0, description="Items generated")
    generation_time_ms: int = Field(0, ge=0, description="Generation time in milliseconds")
    error_count: int = Field(0, ge=0, description="Error count")
    top_items: Optional[List[Dict[str, Any]]] = Field(None, description="Most viewed items")
    top_categories: Optional[List[Dict[str, Any]]] = Field(None, description="Most viewed categories")
    subscriber_countries: Optional[Dict[str, int]] = Field(None, description="Subscriber countries")
    user_agents: Optional[Dict[str, int]] = Field(None, description="User agent statistics")
    referrers: Optional[Dict[str, int]] = Field(None, description="Referrer statistics")


# ============================================================================
# REQUEST MODELS
# ============================================================================

class RSSFeedCreateRequest(RSSFeedBase):
    """Request model for creating RSS feeds."""
    
    @validator('feed_name')
    def validate_feed_name(cls, v):
        """Validate feed name is URL-friendly."""
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Feed name must be URL-friendly (alphanumeric, hyphens, underscores only)')
        return v.lower()
    
    @validator('feed_url')
    def validate_feed_url(cls, v):
        """Validate feed URL starts with slash."""
        if not v.startswith('/'):
            v = '/' + v
        if not v.endswith('.xml'):
            v = v + '.xml'
        return v


class RSSFeedUpdateRequest(BaseModel):
    """Request model for updating RSS feeds."""
    feed_title: Optional[str] = Field(None, min_length=1, max_length=500)
    feed_description: Optional[str] = Field(None, min_length=1)
    feed_language: Optional[LanguageEnum] = None
    is_active: Optional[bool] = None
    is_public: Optional[bool] = None
    max_items: Optional[int] = Field(None, ge=1, le=1000)
    update_frequency_minutes: Optional[int] = Field(None, ge=5, le=1440)
    filter_criteria: Optional[Dict[str, Any]] = None
    custom_styling: Optional[Dict[str, Any]] = None


class RSSFeedItemCreateRequest(RSSFeedItemBase):
    """Request model for creating RSS feed items."""
    pass


class RSSFeedItemUpdateRequest(BaseModel):
    """Request model for updating RSS feed items."""
    item_title: Optional[str] = Field(None, min_length=1, max_length=500)
    item_description: Optional[str] = Field(None, min_length=1)
    item_link: Optional[str] = Field(None, min_length=1, max_length=1000)
    item_category: Optional[str] = Field(None, max_length=100)
    item_author: Optional[str] = Field(None, max_length=200)
    item_content: Optional[str] = None
    item_summary: Optional[str] = None
    is_featured: Optional[bool] = None
    item_metadata: Optional[Dict[str, Any]] = None


class RSSSubscriptionCreateRequest(RSSSubscriptionBase):
    """Request model for creating RSS subscriptions."""
    pass


class RSSFeedGenerateRequest(BaseModel):
    """Request model for generating RSS feeds."""
    force_regenerate: bool = Field(False, description="Force regeneration even if cached")
    include_content: bool = Field(False, description="Include full content in items")
    custom_filters: Optional[Dict[str, Any]] = Field(None, description="Custom filters for this generation")


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class RSSFeedResponse(RSSFeedBase):
    """Response model for RSS feeds."""
    id: str
    last_generated: Optional[datetime]
    last_error: Optional[str]
    generation_count: int
    subscriber_count: int
    created_at: datetime
    updated_at: datetime


class RSSFeedItemResponse(RSSFeedItemBase):
    """Response model for RSS feed items."""
    id: str
    view_count: int
    created_at: datetime
    updated_at: datetime


class RSSSubscriptionResponse(RSSSubscriptionBase):
    """Response model for RSS subscriptions."""
    id: str
    subscription_date: datetime
    last_accessed: datetime
    access_count: int
    is_active: bool
    unsubscribe_token: Optional[str]


class RSSAnalyticsResponse(RSSAnalyticsBase):
    """Response model for RSS analytics."""
    id: str
    created_at: datetime


# ============================================================================
# LIST RESPONSE MODELS
# ============================================================================

class RSSFeedListResponse(BaseModel):
    """List response model for RSS feeds."""
    feeds: List[RSSFeedResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class RSSFeedItemListResponse(BaseModel):
    """List response model for RSS feed items."""
    items: List[RSSFeedItemResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class RSSSubscriptionListResponse(BaseModel):
    """List response model for RSS subscriptions."""
    subscriptions: List[RSSSubscriptionResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class RSSAnalyticsListResponse(BaseModel):
    """List response model for RSS analytics."""
    analytics: List[RSSAnalyticsResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


# ============================================================================
# RSS GENERATION MODELS
# ============================================================================

class RSSChannelInfo(BaseModel):
    """Model for RSS channel information."""
    title: str = Field(..., description="Channel title")
    description: str = Field(..., description="Channel description")
    link: str = Field(..., description="Channel link")
    language: str = Field("en", description="Channel language")
    copyright: str = Field("OpenPolicy V2", description="Copyright information")
    managing_editor: str = Field("editor@openpolicy.ca", description="Managing editor email")
    web_master: str = Field("webmaster@openpolicy.ca", description="Web master email")
    pub_date: datetime = Field(..., description="Publication date")
    last_build_date: datetime = Field(..., description="Last build date")
    category: Optional[str] = Field(None, description="Channel category")
    generator: str = Field("OpenPolicy V2 RSS Generator", description="Generator information")
    docs: str = Field("https://cyber.harvard.edu/rss/rss.html", description="RSS specification docs")
    ttl: int = Field(60, description="Time to live in minutes")


class RSSItemInfo(BaseModel):
    """Model for RSS item information."""
    title: str = Field(..., description="Item title")
    description: str = Field(..., description="Item description")
    link: str = Field(..., description="Item link")
    guid: str = Field(..., description="Globally unique identifier")
    pub_date: datetime = Field(..., description="Publication date")
    category: Optional[str] = Field(None, description="Item category")
    author: Optional[str] = Field(None, description="Item author")
    comments: Optional[str] = Field(None, description="Comments URL")
    enclosure: Optional[Dict[str, str]] = Field(None, description="Enclosure information")
    source: Optional[str] = Field(None, description="Source information")


class RSSFeedContent(BaseModel):
    """Model for complete RSS feed content."""
    channel: RSSChannelInfo = Field(..., description="RSS channel information")
    items: List[RSSItemInfo] = Field(..., description="RSS items")
    generation_time: datetime = Field(..., description="Generation timestamp")
    item_count: int = Field(..., description="Number of items")
    cache_expires: datetime = Field(..., description="Cache expiration time")


# ============================================================================
# ANALYTICS AND STATISTICS MODELS
# ============================================================================

class RSSFeedStatistics(BaseModel):
    """Model for RSS feed statistics."""
    feed_id: str = Field(..., description="Feed ID")
    feed_name: str = Field(..., description="Feed name")
    total_items: int = Field(..., description="Total items generated")
    total_subscribers: int = Field(..., description="Total subscribers")
    total_views: int = Field(..., description="Total views")
    avg_generation_time: float = Field(..., description="Average generation time in ms")
    last_24h_views: int = Field(..., description="Views in last 24 hours")
    last_7d_views: int = Field(..., description="Views in last 7 days")
    last_30d_views: int = Field(..., description="Views in last 30 days")
    top_categories: List[Dict[str, Union[str, int]]] = Field(..., description="Top categories")
    subscriber_growth: List[Dict[str, Union[str, int]]] = Field(..., description="Subscriber growth")
    error_rate: float = Field(..., description="Error rate percentage")
    cache_hit_rate: float = Field(..., description="Cache hit rate percentage")
    generated_at: datetime = Field(..., description="When statistics were generated")


class RSSSystemStatistics(BaseModel):
    """Model for RSS system-wide statistics."""
    total_feeds: int = Field(..., description="Total number of feeds")
    active_feeds: int = Field(..., description="Number of active feeds")
    total_items: int = Field(..., description="Total items across all feeds")
    total_subscribers: int = Field(..., description="Total subscribers across all feeds")
    total_views_24h: int = Field(..., description="Total views in last 24 hours")
    avg_items_per_feed: float = Field(..., description="Average items per feed")
    avg_subscribers_per_feed: float = Field(..., description="Average subscribers per feed")
    top_performing_feeds: List[Dict[str, Union[str, int]]] = Field(..., description="Top performing feeds")
    feed_type_distribution: Dict[str, int] = Field(..., description="Distribution by feed type")
    language_distribution: Dict[str, int] = Field(..., description="Distribution by language")
    error_summary: Dict[str, int] = Field(..., description="Error summary")
    cache_performance: Dict[str, float] = Field(..., description="Cache performance metrics")
    generated_at: datetime = Field(..., description="When statistics were generated")


# ============================================================================
# UTILITY MODELS
# ============================================================================

class RSSValidationResult(BaseModel):
    """Model for RSS validation results."""
    is_valid: bool = Field(..., description="Whether RSS is valid")
    errors: List[str] = Field(..., description="Validation errors")
    warnings: List[str] = Field(..., description="Validation warnings")
    item_count: int = Field(..., description="Number of items")
    feed_size: int = Field(..., description="Feed size in bytes")
    validation_time: float = Field(..., description="Validation time in seconds")


class RSSCacheStatus(BaseModel):
    """Model for RSS cache status."""
    cache_key: str = Field(..., description="Cache key")
    is_cached: bool = Field(..., description="Whether content is cached")
    cache_age: Optional[int] = Field(None, description="Cache age in seconds")
    expires_in: Optional[int] = Field(None, description="Cache expires in seconds")
    cache_size: Optional[int] = Field(None, description="Cache size in bytes")
    hit_count: int = Field(0, description="Number of cache hits")
    last_hit: Optional[datetime] = Field(None, description="Last cache hit time")


class RSSFeedPreview(BaseModel):
    """Model for RSS feed preview."""
    feed_info: RSSFeedResponse = Field(..., description="Feed information")
    sample_items: List[RSSFeedItemResponse] = Field(..., description="Sample items")
    estimated_size: int = Field(..., description="Estimated feed size in bytes")
    generation_estimate: float = Field(..., description="Estimated generation time in seconds")
    xml_preview: str = Field(..., description="XML preview (first 1000 characters)")
