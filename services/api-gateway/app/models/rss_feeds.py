"""
RSS Feed Models for OpenPolicy V2

Comprehensive models for RSS feed generation and management.
Implements P2 priority feature for enhanced content distribution.
"""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base


class RSSFeed(Base):
    """Model for RSS feed definitions and configuration."""
    
    __tablename__ = "rss_feeds"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feed_name = Column(String(200), nullable=False, unique=True)
    feed_title = Column(String(500), nullable=False)
    feed_description = Column(Text, nullable=False)
    feed_type = Column(String(50), nullable=False)  # bills, votes, committees, members, debates
    feed_url = Column(String(500), nullable=False, unique=True)
    feed_language = Column(String(10), default="en", nullable=False)  # en, fr
    is_active = Column(Boolean, default=True, nullable=False)
    is_public = Column(Boolean, default=True, nullable=False)
    max_items = Column(Integer, default=50, nullable=False)
    update_frequency_minutes = Column(Integer, default=60, nullable=False)  # How often to regenerate
    last_generated = Column(DateTime, nullable=True)
    last_error = Column(Text, nullable=True)
    generation_count = Column(Integer, default=0, nullable=False)
    subscriber_count = Column(Integer, default=0, nullable=False)
    filter_criteria = Column(JSONB, nullable=True)  # Additional filtering options
    custom_styling = Column(JSONB, nullable=True)  # Custom RSS styling options
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    feed_items = relationship("RSSFeedItem", back_populates="feed", cascade="all, delete-orphan")
    subscriptions = relationship("RSSSubscription", back_populates="feed", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_rss_feeds_feed_name', 'feed_name'),
        Index('ix_rss_feeds_feed_type', 'feed_type'),
        Index('ix_rss_feeds_is_active', 'is_active'),
        Index('ix_rss_feeds_is_public', 'is_public'),
        Index('ix_rss_feeds_feed_language', 'feed_language'),
        Index('ix_rss_feeds_last_generated', 'last_generated'),
    )


class RSSFeedItem(Base):
    """Model for individual RSS feed items."""
    
    __tablename__ = "rss_feed_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feed_id = Column(UUID(as_uuid=True), ForeignKey("rss_feeds.id"), nullable=False)
    item_title = Column(String(500), nullable=False)
    item_description = Column(Text, nullable=False)
    item_link = Column(String(1000), nullable=False)
    item_guid = Column(String(500), nullable=False, unique=True)  # Unique identifier
    item_pub_date = Column(DateTime, nullable=False)
    item_category = Column(String(100), nullable=True)
    item_author = Column(String(200), nullable=True)
    content_type = Column(String(50), nullable=False)  # bill, vote, committee, member, debate
    content_id = Column(String(100), nullable=False)  # ID of the actual content
    item_content = Column(Text, nullable=True)  # Full content if needed
    item_summary = Column(Text, nullable=True)  # Summary/excerpt
    is_featured = Column(Boolean, default=False, nullable=False)
    view_count = Column(Integer, default=0, nullable=False)
    item_metadata = Column(JSONB, nullable=True)  # Additional metadata
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    feed = relationship("RSSFeed", back_populates="feed_items")
    
    # Indexes
    __table_args__ = (
        Index('ix_rss_feed_items_feed_id', 'feed_id'),
        Index('ix_rss_feed_items_item_guid', 'item_guid'),
        Index('ix_rss_feed_items_item_pub_date', 'item_pub_date'),
        Index('ix_rss_feed_items_content_type', 'content_type'),
        Index('ix_rss_feed_items_content_id', 'content_id'),
        Index('ix_rss_feed_items_is_featured', 'is_featured'),
        Index('ix_rss_feed_items_item_category', 'item_category'),
    )


class RSSSubscription(Base):
    """Model for tracking RSS feed subscriptions."""
    
    __tablename__ = "rss_subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feed_id = Column(UUID(as_uuid=True), ForeignKey("rss_feeds.id"), nullable=False)
    subscriber_email = Column(String(255), nullable=True)  # Optional email for notifications
    subscriber_ip = Column(String(45), nullable=True)  # Track IP for analytics
    subscriber_user_agent = Column(String(500), nullable=True)  # Track user agent
    subscription_date = Column(DateTime, server_default=func.now(), nullable=False)
    last_accessed = Column(DateTime, server_default=func.now(), nullable=False)
    access_count = Column(Integer, default=1, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    unsubscribe_token = Column(String(100), nullable=True)  # For email unsubscription
    subscription_source = Column(String(100), default="direct", nullable=False)  # direct, email, api
    
    # Relationships
    feed = relationship("RSSFeed", back_populates="subscriptions")
    
    # Indexes
    __table_args__ = (
        Index('ix_rss_subscriptions_feed_id', 'feed_id'),
        Index('ix_rss_subscriptions_subscriber_email', 'subscriber_email'),
        Index('ix_rss_subscriptions_subscription_date', 'subscription_date'),
        Index('ix_rss_subscriptions_last_accessed', 'last_accessed'),
        Index('ix_rss_subscriptions_is_active', 'is_active'),
        Index('ix_rss_subscriptions_unsubscribe_token', 'unsubscribe_token'),
    )


class RSSAnalytics(Base):
    """Model for RSS feed analytics and statistics."""
    
    __tablename__ = "rss_analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feed_id = Column(UUID(as_uuid=True), ForeignKey("rss_feeds.id"), nullable=False)
    analytics_date = Column(DateTime, nullable=False)  # Date of analytics record
    daily_views = Column(Integer, default=0, nullable=False)
    daily_subscribers = Column(Integer, default=0, nullable=False)
    daily_unsubscribes = Column(Integer, default=0, nullable=False)
    items_generated = Column(Integer, default=0, nullable=False)
    generation_time_ms = Column(Integer, default=0, nullable=False)  # Time to generate feed
    error_count = Column(Integer, default=0, nullable=False)
    top_items = Column(JSONB, nullable=True)  # Most viewed items
    top_categories = Column(JSONB, nullable=True)  # Most viewed categories
    subscriber_countries = Column(JSONB, nullable=True)  # Geographic data
    user_agents = Column(JSONB, nullable=True)  # User agent statistics
    referrers = Column(JSONB, nullable=True)  # Referrer statistics
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    feed = relationship("RSSFeed", foreign_keys=[feed_id])
    
    # Indexes
    __table_args__ = (
        Index('ix_rss_analytics_feed_id', 'feed_id'),
        Index('ix_rss_analytics_analytics_date', 'analytics_date'),
        Index('ix_rss_analytics_daily_views', 'daily_views'),
        Index('ix_rss_analytics_created_at', 'created_at'),
    )


class RSSCache(Base):
    """Model for caching generated RSS feed content."""
    
    __tablename__ = "rss_cache"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feed_id = Column(UUID(as_uuid=True), ForeignKey("rss_feeds.id"), nullable=False)
    cache_key = Column(String(255), nullable=False, unique=True)
    rss_content = Column(Text, nullable=False)  # Generated RSS XML
    content_hash = Column(String(64), nullable=False)  # MD5 hash for change detection
    item_count = Column(Integer, nullable=False)
    generation_time_ms = Column(Integer, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    hits = Column(Integer, default=0, nullable=False)
    last_hit = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    feed = relationship("RSSFeed", foreign_keys=[feed_id])
    
    # Indexes
    __table_args__ = (
        Index('ix_rss_cache_feed_id', 'feed_id'),
        Index('ix_rss_cache_cache_key', 'cache_key'),
        Index('ix_rss_cache_expires_at', 'expires_at'),
        Index('ix_rss_cache_content_hash', 'content_hash'),
        Index('ix_rss_cache_last_hit', 'last_hit'),
    )
