"""
News Aggregation Models

Comprehensive news aggregation system models.
Implements FEAT-020 News Aggregation (P2 priority).
"""

from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, Float, ForeignKey, Index, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB, TSVECTOR
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime


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


class NewsSource(Base):
    """News sources configuration."""
    
    __tablename__ = "news_sources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Source details
    name = Column(String(200), unique=True, nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    website_url = Column(String(500), nullable=False)
    logo_url = Column(String(500), nullable=True)
    
    # Source configuration
    source_type = Column(SQLEnum(NewsSourceType), nullable=False)
    feed_url = Column(String(500), nullable=True)  # For RSS
    api_endpoint = Column(String(500), nullable=True)  # For APIs
    api_config = Column(JSONB, nullable=True)  # API keys, headers, etc.
    
    # Source metadata
    language = Column(String(10), default="en", nullable=False)
    country = Column(String(2), default="CA", nullable=False)
    province = Column(String(2), nullable=True)  # For provincial sources
    
    # Settings
    is_active = Column(Boolean, default=True, nullable=False)
    is_trusted = Column(Boolean, default=False, nullable=False)  # Verified sources
    is_partisan = Column(Boolean, default=False, nullable=False)
    political_leaning = Column(String(20), nullable=True)  # left, center-left, center, center-right, right
    
    # Collection settings
    fetch_frequency_minutes = Column(Integer, default=60, nullable=False)
    max_items_per_fetch = Column(Integer, default=50, nullable=False)
    
    # Quality metrics
    reliability_score = Column(Float, default=0.5, nullable=False)  # 0-1
    accuracy_score = Column(Float, default=0.5, nullable=False)  # 0-1
    
    # Statistics
    total_articles = Column(Integer, default=0, nullable=False)
    last_fetched = Column(DateTime(timezone=True), nullable=True)
    last_error = Column(Text, nullable=True)
    error_count = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    articles = relationship("NewsArticle", back_populates="source", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_source_slug', 'slug'),
        Index('idx_source_type', 'source_type'),
        Index('idx_source_active', 'is_active'),
        Index('idx_source_trusted', 'is_trusted'),
    )


class NewsArticle(Base):
    """Individual news articles."""
    
    __tablename__ = "news_articles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("news_sources.id"), nullable=False)
    
    # Article details
    title = Column(Text, nullable=False)
    url = Column(String(1000), unique=True, nullable=False)
    author = Column(String(200), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=False)
    
    # Content
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=True)  # Full article if available
    content_hash = Column(String(64), nullable=True)  # For duplicate detection
    
    # Media
    image_url = Column(String(1000), nullable=True)
    video_url = Column(String(1000), nullable=True)
    
    # Categorization
    categories = Column(JSONB, nullable=True)  # Array of categories
    tags = Column(JSONB, nullable=True)  # Array of tags
    entities = Column(JSONB, nullable=True)  # Mentioned MPs, bills, etc.
    
    # Relevance and sentiment
    relevance_score = Column(Float, default=0.5, nullable=False)  # 0-1
    sentiment = Column(SQLEnum(NewsSentiment), default=NewsSentiment.NEUTRAL, nullable=False)
    sentiment_score = Column(Float, nullable=True)  # -1 to 1
    
    # Engagement metrics
    view_count = Column(Integer, default=0, nullable=False)
    share_count = Column(Integer, default=0, nullable=False)
    save_count = Column(Integer, default=0, nullable=False)
    
    # Full-text search
    search_vector = Column(TSVECTOR, nullable=True)
    
    # Flags
    is_featured = Column(Boolean, default=False, nullable=False)
    is_breaking = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_duplicate = Column(Boolean, default=False, nullable=False)
    duplicate_of_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    source = relationship("NewsSource", back_populates="articles")
    related_articles = relationship("RelatedArticle", 
                                  foreign_keys='RelatedArticle.article_id',
                                  back_populates="article",
                                  cascade="all, delete-orphan")
    mentions = relationship("ArticleMention", back_populates="article", cascade="all, delete-orphan")
    user_interactions = relationship("ArticleInteraction", back_populates="article", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_article_source', 'source_id'),
        Index('idx_article_published', 'published_at'),
        Index('idx_article_relevance', 'relevance_score'),
        Index('idx_article_featured', 'is_featured'),
        Index('idx_article_breaking', 'is_breaking'),
        Index('idx_article_search', 'search_vector', postgresql_using='gin'),
        Index('idx_article_url_hash', 'content_hash'),
    )


class RelatedArticle(Base):
    """Related articles mapping."""
    
    __tablename__ = "related_articles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID(as_uuid=True), ForeignKey("news_articles.id"), nullable=False)
    related_article_id = Column(UUID(as_uuid=True), ForeignKey("news_articles.id"), nullable=False)
    
    # Relationship metadata
    similarity_score = Column(Float, nullable=False)  # 0-1
    relationship_type = Column(String(50), nullable=True)  # follow-up, contradiction, analysis, etc.
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    article = relationship("NewsArticle", foreign_keys=[article_id], back_populates="related_articles")
    related = relationship("NewsArticle", foreign_keys=[related_article_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_related_article', 'article_id'),
        Index('idx_related_related', 'related_article_id'),
        Index('idx_related_similarity', 'similarity_score'),
    )


class ArticleMention(Base):
    """Entities mentioned in articles."""
    
    __tablename__ = "article_mentions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID(as_uuid=True), ForeignKey("news_articles.id"), nullable=False)
    
    # Entity details
    entity_type = Column(String(50), nullable=False)  # member, bill, committee, party, etc.
    entity_id = Column(String(100), nullable=False)
    entity_name = Column(String(200), nullable=False)
    
    # Mention context
    mention_count = Column(Integer, default=1, nullable=False)
    sentiment = Column(SQLEnum(NewsSentiment), nullable=True)
    context = Column(Text, nullable=True)  # Surrounding text
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    article = relationship("NewsArticle", back_populates="mentions")
    
    # Indexes
    __table_args__ = (
        Index('idx_mention_article', 'article_id'),
        Index('idx_mention_entity', 'entity_type', 'entity_id'),
    )


class ArticleInteraction(Base):
    """User interactions with articles."""
    
    __tablename__ = "article_interactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID(as_uuid=True), ForeignKey("news_articles.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Interaction type
    interaction_type = Column(String(20), nullable=False)  # view, save, share, report
    interaction_data = Column(JSONB, nullable=True)  # Additional data
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    article = relationship("NewsArticle", back_populates="user_interactions")
    user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_interaction_article', 'article_id'),
        Index('idx_interaction_user', 'user_id'),
        Index('idx_interaction_type', 'interaction_type'),
        Index('idx_interaction_created', 'created_at'),
    )


class NewsTopic(Base):
    """News topics and trends."""
    
    __tablename__ = "news_topics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Topic details
    name = Column(String(200), unique=True, nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Topic metadata
    category = Column(SQLEnum(NewsCategory), nullable=False)
    keywords = Column(JSONB, nullable=True)  # Keywords for auto-detection
    
    # Trending data
    is_trending = Column(Boolean, default=False, nullable=False)
    trend_score = Column(Float, default=0.0, nullable=False)
    article_count_24h = Column(Integer, default=0, nullable=False)
    article_count_7d = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    trending_since = Column(DateTime(timezone=True), nullable=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_topic_slug', 'slug'),
        Index('idx_topic_trending', 'is_trending', 'trend_score'),
        Index('idx_topic_category', 'category'),
    )


class NewsDigest(Base):
    """Daily/weekly news digests."""
    
    __tablename__ = "news_digests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Digest details
    digest_type = Column(String(20), nullable=False)  # daily, weekly, special
    digest_date = Column(DateTime(timezone=True), nullable=False)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=True)
    
    # Content
    featured_articles = Column(JSONB, nullable=False)  # Array of article IDs
    topic_summaries = Column(JSONB, nullable=True)  # Summary by topic
    trending_topics = Column(JSONB, nullable=True)  # Top trending topics
    
    # Statistics
    total_articles = Column(Integer, default=0, nullable=False)
    sources_included = Column(Integer, default=0, nullable=False)
    
    # Email campaign
    email_sent = Column(Boolean, default=False, nullable=False)
    email_sent_at = Column(DateTime(timezone=True), nullable=True)
    email_recipients = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    published_at = Column(DateTime(timezone=True), nullable=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_digest_type', 'digest_type'),
        Index('idx_digest_date', 'digest_date'),
        Index('idx_digest_published', 'published_at'),
    )


class NewsAlert(Base):
    """User news alerts."""
    
    __tablename__ = "news_alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Alert configuration
    name = Column(String(200), nullable=False)
    alert_type = Column(String(50), nullable=False)  # keyword, entity, topic, category
    alert_config = Column(JSONB, nullable=False)  # Keywords, entities, etc.
    
    # Settings
    is_active = Column(Boolean, default=True, nullable=False)
    notification_channels = Column(JSONB, nullable=False)  # email, push, in-app
    frequency = Column(String(20), default="realtime", nullable=False)  # realtime, hourly, daily
    
    # Statistics
    trigger_count = Column(Integer, default=0, nullable=False)
    last_triggered = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_alert_user', 'user_id'),
        Index('idx_alert_active', 'is_active'),
        Index('idx_alert_type', 'alert_type'),
    )


class NewsSourceMetrics(Base):
    """Metrics for news sources."""
    
    __tablename__ = "news_source_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("news_sources.id"), nullable=False)
    
    # Time period
    metric_date = Column(DateTime(timezone=True), nullable=False)
    metric_type = Column(String(20), nullable=False)  # daily, weekly, monthly
    
    # Metrics
    articles_published = Column(Integer, default=0, nullable=False)
    articles_featured = Column(Integer, default=0, nullable=False)
    total_views = Column(Integer, default=0, nullable=False)
    total_shares = Column(Integer, default=0, nullable=False)
    avg_relevance_score = Column(Float, nullable=True)
    avg_sentiment_score = Column(Float, nullable=True)
    
    # Quality metrics
    duplicate_rate = Column(Float, nullable=True)  # Percentage of duplicates
    error_rate = Column(Float, nullable=True)  # Fetch errors
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    source = relationship("NewsSource")
    
    # Indexes
    __table_args__ = (
        Index('idx_metric_source', 'source_id'),
        Index('idx_metric_date', 'metric_date'),
        Index('idx_metric_type', 'metric_type'),
    )