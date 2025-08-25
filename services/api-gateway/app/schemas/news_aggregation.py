"""
News Aggregation Schemas

Pydantic schemas for news aggregation functionality.
Implements FEAT-020 News Aggregation (P2 priority).
"""

from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum


# Enums (matching model enums)
class NewsSourceType(str, Enum):
    """Types of news sources."""
    RSS = "rss"
    API = "api"
    SCRAPER = "scraper"
    TWITTER = "twitter"
    PRESS_RELEASE = "press_release"
    MANUAL = "manual"


class NewsCategory(str, Enum):
    """News categories."""
    LEGISLATION = "legislation"
    POLITICS = "politics"
    POLICY = "policy"
    COMMITTEES = "committees"
    ELECTIONS = "elections"
    BUDGET = "budget"
    INTERNATIONAL = "international"
    PROVINCIAL = "provincial"
    MUNICIPAL = "municipal"
    OPINION = "opinion"
    ANALYSIS = "analysis"
    GENERAL = "general"


class NewsSentiment(str, Enum):
    """Article sentiment."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class PoliticalLeaning(str, Enum):
    """Political leaning of sources."""
    LEFT = "left"
    CENTER_LEFT = "center-left"
    CENTER = "center"
    CENTER_RIGHT = "center-right"
    RIGHT = "right"


# Source schemas
class NewsSourceBase(BaseModel):
    """Base news source schema."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    website_url: HttpUrl
    logo_url: Optional[HttpUrl] = None
    source_type: NewsSourceType
    language: str = Field("en", regex="^[a-z]{2}$")
    country: str = Field("CA", regex="^[A-Z]{2}$")
    province: Optional[str] = Field(None, regex="^[A-Z]{2}$")


class NewsSourceCreate(NewsSourceBase):
    """Schema for creating news source."""
    feed_url: Optional[HttpUrl] = None
    api_endpoint: Optional[HttpUrl] = None
    api_config: Optional[Dict[str, Any]] = None
    is_trusted: bool = False
    is_partisan: bool = False
    political_leaning: Optional[PoliticalLeaning] = None
    fetch_frequency_minutes: int = Field(60, ge=5, le=1440)
    max_items_per_fetch: int = Field(50, ge=1, le=200)


class NewsSourceUpdate(BaseModel):
    """Schema for updating news source."""
    description: Optional[str] = None
    logo_url: Optional[HttpUrl] = None
    feed_url: Optional[HttpUrl] = None
    api_config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_trusted: Optional[bool] = None
    is_partisan: Optional[bool] = None
    political_leaning: Optional[PoliticalLeaning] = None
    fetch_frequency_minutes: Optional[int] = Field(None, ge=5, le=1440)
    reliability_score: Optional[float] = Field(None, ge=0, le=1)
    accuracy_score: Optional[float] = Field(None, ge=0, le=1)


class NewsSourceResponse(NewsSourceBase):
    """Schema for news source responses."""
    id: UUID
    slug: str
    is_active: bool
    is_trusted: bool
    is_partisan: bool
    political_leaning: Optional[PoliticalLeaning]
    fetch_frequency_minutes: int
    max_items_per_fetch: int
    reliability_score: float
    accuracy_score: float
    total_articles: int
    last_fetched: Optional[datetime]
    last_error: Optional[str]
    error_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Article schemas
class NewsArticleBase(BaseModel):
    """Base news article schema."""
    title: str = Field(..., min_length=1)
    url: HttpUrl
    author: Optional[str] = Field(None, max_length=200)
    published_at: datetime
    summary: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    video_url: Optional[HttpUrl] = None


class NewsArticleCreate(NewsArticleBase):
    """Schema for creating news article."""
    source_id: UUID
    content: Optional[str] = None
    categories: Optional[List[NewsCategory]] = None
    tags: Optional[List[str]] = None
    entities: Optional[Dict[str, List[str]]] = None
    relevance_score: float = Field(0.5, ge=0, le=1)
    sentiment: NewsSentiment = NewsSentiment.NEUTRAL
    sentiment_score: Optional[float] = Field(None, ge=-1, le=1)
    is_featured: bool = False
    is_breaking: bool = False


class NewsArticleUpdate(BaseModel):
    """Schema for updating news article."""
    summary: Optional[str] = None
    categories: Optional[List[NewsCategory]] = None
    tags: Optional[List[str]] = None
    entities: Optional[Dict[str, List[str]]] = None
    relevance_score: Optional[float] = Field(None, ge=0, le=1)
    sentiment: Optional[NewsSentiment] = None
    sentiment_score: Optional[float] = Field(None, ge=-1, le=1)
    is_featured: Optional[bool] = None
    is_breaking: Optional[bool] = None
    is_verified: Optional[bool] = None


class NewsArticleResponse(NewsArticleBase):
    """Schema for news article responses."""
    id: UUID
    source_id: UUID
    source_name: str  # Populated from relationship
    source_slug: str  # Populated from relationship
    content: Optional[str]
    content_hash: Optional[str]
    categories: Optional[List[NewsCategory]]
    tags: Optional[List[str]]
    entities: Optional[Dict[str, List[str]]]
    relevance_score: float
    sentiment: NewsSentiment
    sentiment_score: Optional[float]
    view_count: int
    share_count: int
    save_count: int
    is_featured: bool
    is_breaking: bool
    is_verified: bool
    is_duplicate: bool
    duplicate_of_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class NewsArticleListResponse(BaseModel):
    """Schema for article list responses."""
    results: List[NewsArticleResponse]
    pagination: Dict[str, Any]
    facets: Optional[Dict[str, Dict[str, int]]] = None
    
    class Config:
        orm_mode = True


# Related article schemas
class RelatedArticleResponse(BaseModel):
    """Schema for related article responses."""
    article_id: UUID
    article_title: str
    article_url: str
    similarity_score: float
    relationship_type: Optional[str]
    
    class Config:
        orm_mode = True


# Mention schemas
class ArticleMentionResponse(BaseModel):
    """Schema for article mention responses."""
    entity_type: str
    entity_id: str
    entity_name: str
    mention_count: int
    sentiment: Optional[NewsSentiment]
    context: Optional[str]
    
    class Config:
        orm_mode = True


# Topic schemas
class NewsTopicBase(BaseModel):
    """Base news topic schema."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: NewsCategory
    keywords: Optional[List[str]] = None


class NewsTopicCreate(NewsTopicBase):
    """Schema for creating news topic."""
    pass


class NewsTopicUpdate(BaseModel):
    """Schema for updating news topic."""
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    is_trending: Optional[bool] = None
    trend_score: Optional[float] = Field(None, ge=0)


class NewsTopicResponse(NewsTopicBase):
    """Schema for news topic responses."""
    id: UUID
    slug: str
    is_trending: bool
    trend_score: float
    article_count_24h: int
    article_count_7d: int
    trending_since: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Digest schemas
class NewsDigestCreate(BaseModel):
    """Schema for creating news digest."""
    digest_type: str = Field(..., regex="^(daily|weekly|special)$")
    digest_date: datetime
    title: str = Field(..., min_length=1, max_length=500)
    summary: Optional[str] = None
    featured_articles: List[UUID]
    topic_summaries: Optional[Dict[str, str]] = None
    trending_topics: Optional[List[str]] = None


class NewsDigestResponse(BaseModel):
    """Schema for news digest responses."""
    id: UUID
    digest_type: str
    digest_date: datetime
    title: str
    summary: Optional[str]
    featured_articles: List[Dict[str, Any]]  # Expanded with article details
    topic_summaries: Optional[Dict[str, str]]
    trending_topics: Optional[List[str]]
    total_articles: int
    sources_included: int
    email_sent: bool
    email_sent_at: Optional[datetime]
    email_recipients: int
    created_at: datetime
    published_at: Optional[datetime]
    
    class Config:
        orm_mode = True


# Alert schemas
class NewsAlertBase(BaseModel):
    """Base news alert schema."""
    name: str = Field(..., min_length=1, max_length=200)
    alert_type: str = Field(..., regex="^(keyword|entity|topic|category)$")
    alert_config: Dict[str, Any]
    notification_channels: List[str] = Field(..., min_items=1)
    frequency: str = Field("realtime", regex="^(realtime|hourly|daily)$")


class NewsAlertCreate(NewsAlertBase):
    """Schema for creating news alert."""
    pass


class NewsAlertUpdate(BaseModel):
    """Schema for updating news alert."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    alert_config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    notification_channels: Optional[List[str]] = Field(None, min_items=1)
    frequency: Optional[str] = Field(None, regex="^(realtime|hourly|daily)$")


class NewsAlertResponse(NewsAlertBase):
    """Schema for news alert responses."""
    id: UUID
    user_id: UUID
    is_active: bool
    trigger_count: int
    last_triggered: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Search and filter schemas
class NewsSearchRequest(BaseModel):
    """Schema for news search requests."""
    query: Optional[str] = Field(None, description="Full-text search query")
    sources: Optional[List[UUID]] = None
    categories: Optional[List[NewsCategory]] = None
    tags: Optional[List[str]] = None
    entities: Optional[Dict[str, List[str]]] = None
    sentiment: Optional[NewsSentiment] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_featured: Optional[bool] = None
    is_breaking: Optional[bool] = None
    is_verified: Optional[bool] = None
    min_relevance: Optional[float] = Field(None, ge=0, le=1)
    
    # Pagination
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    
    # Sorting
    sort_by: str = Field("published_at", regex="^(published_at|relevance|views|shares)$")
    sort_order: str = Field("desc", regex="^(asc|desc)$")
    
    @validator('end_date')
    def validate_date_range(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v


# Analytics schemas
class NewsAnalytics(BaseModel):
    """News analytics data."""
    period: str  # day, week, month
    total_articles: int
    total_sources: int
    total_views: int
    total_shares: int
    total_saves: int
    
    # By category
    articles_by_category: Dict[str, int]
    views_by_category: Dict[str, int]
    
    # By source
    articles_by_source: Dict[str, int]
    reliability_by_source: Dict[str, float]
    
    # By sentiment
    articles_by_sentiment: Dict[str, int]
    
    # Trending
    trending_topics: List[Dict[str, Any]]
    trending_entities: List[Dict[str, Any]]
    
    # Time series
    articles_over_time: List[Dict[str, Any]]
    engagement_over_time: List[Dict[str, Any]]


class SourceMetrics(BaseModel):
    """Source performance metrics."""
    source_id: UUID
    source_name: str
    metric_date: datetime
    metric_type: str
    articles_published: int
    articles_featured: int
    total_views: int
    total_shares: int
    avg_relevance_score: Optional[float]
    avg_sentiment_score: Optional[float]
    duplicate_rate: Optional[float]
    error_rate: Optional[float]
    
    class Config:
        orm_mode = True


# Interaction schemas
class ArticleInteractionCreate(BaseModel):
    """Schema for creating article interaction."""
    interaction_type: str = Field(..., regex="^(view|save|share|report)$")
    interaction_data: Optional[Dict[str, Any]] = None


class SavedArticleResponse(BaseModel):
    """Schema for saved article responses."""
    article: NewsArticleResponse
    saved_at: datetime
    
    class Config:
        orm_mode = True


# Aggregation job schemas
class AggregationJobStatus(BaseModel):
    """Schema for aggregation job status."""
    source_id: UUID
    source_name: str
    status: str  # pending, running, completed, failed
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    articles_fetched: int
    articles_new: int
    articles_updated: int
    errors: List[str]
    next_run: datetime