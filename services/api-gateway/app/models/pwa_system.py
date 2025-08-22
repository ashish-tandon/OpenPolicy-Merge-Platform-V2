"""
PWA System Models for OpenPolicy V2

Comprehensive models for Progressive Web App (PWA) system.
Implements P2 priority feature for enhanced mobile accessibility and user experience.
"""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, ForeignKey, Index, UniqueConstraint, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base


class PWAManifest(Base):
    """Model for PWA manifest configurations."""
    
    __tablename__ = "pwa_manifests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifest_name = Column(String(200), nullable=False, unique=True)  # Manifest identifier
    app_name = Column(String(200), nullable=False)  # Application name
    short_name = Column(String(100), nullable=False)  # Short application name
    description = Column(Text, nullable=True)  # Application description
    start_url = Column(String(500), nullable=False)  # Start URL for the app
    display_mode = Column(String(50), default="standalone", nullable=False)  # standalone, fullscreen, minimal-ui, browser
    orientation = Column(String(50), default="portrait", nullable=False)  # portrait, landscape, any
    theme_color = Column(String(7), default="#000000", nullable=False)  # Theme color in hex
    background_color = Column(String(7), default="#ffffff", nullable=False)  # Background color in hex
    scope = Column(String(500), nullable=True)  # App scope
    lang = Column(String(10), default="en", nullable=False)  # Language code
    dir = Column(String(10), default="ltr", nullable=False)  # Text direction
    categories = Column(JSONB, nullable=True)  # App categories
    icons = Column(JSONB, nullable=False)  # App icons configuration
    screenshots = Column(JSONB, nullable=True)  # App screenshots
    shortcuts = Column(JSONB, nullable=True)  # App shortcuts
    related_applications = Column(JSONB, nullable=True)  # Related applications
    prefer_related_applications = Column(Boolean, default=False, nullable=False)  # Prefer native apps
    is_active = Column(Boolean, default=True, nullable=False)  # Whether manifest is active
    is_default = Column(Boolean, default=False, nullable=False)  # Whether this is the default manifest
    created_by = Column(String(100), nullable=False)  # Who created the manifest
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    service_workers = relationship("ServiceWorker", back_populates="manifest", cascade="all, delete-orphan")
    offline_resources = relationship("OfflineResource", back_populates="manifest", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_pwa_manifests_manifest_name', 'manifest_name'),
        Index('ix_pwa_manifests_is_active', 'is_active'),
        Index('ix_pwa_manifests_is_default', 'is_default'),
        Index('ix_pwa_manifests_created_by', 'created_by'),
    )


class ServiceWorker(Base):
    """Model for service worker configurations."""
    
    __tablename__ = "service_workers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifest_id = Column(UUID(as_uuid=True), ForeignKey("pwa_manifests.id"), nullable=False)
    worker_name = Column(String(200), nullable=False)  # Service worker name
    worker_url = Column(String(500), nullable=False)  # Service worker URL
    worker_scope = Column(String(500), nullable=False)  # Service worker scope
    worker_version = Column(String(50), nullable=False)  # Service worker version
    worker_script = Column(Text, nullable=False)  # Service worker JavaScript code
    is_active = Column(Boolean, default=True, nullable=False)  # Whether worker is active
    is_default = Column(Boolean, default=False, nullable=False)  # Whether this is the default worker
    cache_strategy = Column(String(50), default="network-first", nullable=False)  # cache-first, network-first, stale-while-revalidate
    offline_fallback = Column(String(500), nullable=True)  # Offline fallback page
    push_enabled = Column(Boolean, default=False, nullable=False)  # Whether push notifications are enabled
    background_sync_enabled = Column(Boolean, default=False, nullable=False)  # Whether background sync is enabled
    created_by = Column(String(100), nullable=False)  # Who created the worker
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    manifest = relationship("PWAManifest", back_populates="service_workers")
    cache_entries = relationship("CacheEntry", back_populates="service_worker", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_service_workers_manifest_id', 'manifest_id'),
        Index('ix_service_workers_worker_name', 'worker_name'),
        Index('ix_service_workers_is_active', 'is_active'),
        Index('ix_service_workers_is_default', 'is_default'),
        Index('ix_service_workers_cache_strategy', 'cache_strategy'),
    )


class OfflineResource(Base):
    """Model for offline resources and caching."""
    
    __tablename__ = "offline_resources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifest_id = Column(UUID(as_uuid=True), ForeignKey("pwa_manifests.id"), nullable=False)
    resource_url = Column(String(500), nullable=False)  # Resource URL
    resource_type = Column(String(50), nullable=False)  # html, css, js, image, font, api
    resource_category = Column(String(100), nullable=False)  # critical, important, optional
    cache_duration = Column(Integer, default=86400, nullable=False)  # Cache duration in seconds
    is_offline_available = Column(Boolean, default=True, nullable=False)  # Whether resource is available offline
    compression_enabled = Column(Boolean, default=True, nullable=False)  # Whether compression is enabled
    version_hash = Column(String(64), nullable=True)  # Resource version hash
    file_size = Column(Integer, nullable=True)  # Resource file size in bytes
    last_updated = Column(DateTime, nullable=True)  # When resource was last updated
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    manifest = relationship("PWAManifest", back_populates="offline_resources")
    
    # Indexes and constraints
    __table_args__ = (
        Index('ix_offline_resources_manifest_id', 'manifest_id'),
        Index('ix_offline_resources_resource_url', 'resource_url'),
        Index('ix_offline_resources_resource_type', 'resource_type'),
        Index('ix_offline_resources_resource_category', 'resource_category'),
        Index('ix_offline_resources_is_offline_available', 'is_offline_available'),
        UniqueConstraint('manifest_id', 'resource_url', name='uq_offline_resource_manifest_url'),
    )


class CacheEntry(Base):
    """Model for service worker cache entries."""
    
    __tablename__ = "cache_entries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_worker_id = Column(UUID(as_uuid=True), ForeignKey("service_workers.id"), nullable=False)
    cache_name = Column(String(200), nullable=False)  # Cache name
    resource_url = Column(String(500), nullable=False)  # Cached resource URL
    resource_type = Column(String(50), nullable=False)  # Type of cached resource
    cache_timestamp = Column(DateTime, nullable=False)  # When resource was cached
    cache_expiry = Column(DateTime, nullable=True)  # When cache expires
    cache_size = Column(Integer, nullable=True)  # Cache size in bytes
    cache_hits = Column(Integer, default=0, nullable=False)  # Number of cache hits
    last_accessed = Column(DateTime, nullable=True)  # Last time cache was accessed
    is_valid = Column(Boolean, default=True, nullable=False)  # Whether cache entry is valid
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    service_worker = relationship("ServiceWorker", back_populates="cache_entries")
    
    # Indexes
    __table_args__ = (
        Index('ix_cache_entries_service_worker_id', 'service_worker_id'),
        Index('ix_cache_entries_cache_name', 'cache_name'),
        Index('ix_cache_entries_resource_url', 'resource_url'),
        Index('ix_cache_entries_cache_timestamp', 'cache_timestamp'),
        Index('ix_cache_entries_cache_expiry', 'cache_expiry'),
        Index('ix_cache_entries_is_valid', 'is_valid'),
    )


class PWAInstallation(Base):
    """Model for tracking PWA installations."""
    
    __tablename__ = "pwa_installations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifest_id = Column(UUID(as_uuid=True), ForeignKey("pwa_manifests.id"), nullable=False)
    user_id = Column(String(100), nullable=True)  # User ID if authenticated
    session_id = Column(String(100), nullable=False)  # Session identifier
    device_type = Column(String(50), nullable=False)  # mobile, tablet, desktop
    platform = Column(String(50), nullable=False)  # ios, android, windows, macos, linux
    browser = Column(String(100), nullable=False)  # Browser name and version
    install_method = Column(String(50), nullable=False)  # manual, prompt, banner
    install_timestamp = Column(DateTime, nullable=False)  # When PWA was installed
    uninstall_timestamp = Column(DateTime, nullable=True)  # When PWA was uninstalled
    is_active = Column(Boolean, default=True, nullable=False)  # Whether installation is active
    last_used = Column(DateTime, nullable=True)  # Last time PWA was used
    usage_count = Column(Integer, default=0, nullable=False)  # Number of times PWA was used
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    manifest = relationship("PWAManifest", foreign_keys=[manifest_id])
    
    # Indexes
    __table_args__ = (
        Index('ix_pwa_installations_manifest_id', 'manifest_id'),
        Index('ix_pwa_installations_user_id', 'user_id'),
        Index('ix_pwa_installations_device_type', 'device_type'),
        Index('ix_pwa_installations_platform', 'platform'),
        Index('ix_pwa_installations_install_timestamp', 'install_timestamp'),
        Index('ix_pwa_installations_is_active', 'is_active'),
    )


class PWAPushSubscription(Base):
    """Model for push notification subscriptions."""
    
    __tablename__ = "pwa_push_subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifest_id = Column(UUID(as_uuid=True), ForeignKey("pwa_manifests.id"), nullable=False)
    user_id = Column(String(100), nullable=True)  # User ID if authenticated
    endpoint = Column(Text, nullable=False)  # Push subscription endpoint
    p256dh_key = Column(String(200), nullable=False)  # P-256 DH key
    auth_secret = Column(String(200), nullable=False)  # Authentication secret
    subscription_data = Column(JSONB, nullable=True)  # Additional subscription data
    is_active = Column(Boolean, default=True, nullable=False)  # Whether subscription is active
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    manifest = relationship("PWAManifest", foreign_keys=[manifest_id])
    
    # Indexes
    __table_args__ = (
        Index('ix_pwa_push_subscriptions_manifest_id', 'manifest_id'),
        Index('ix_pwa_push_subscriptions_user_id', 'user_id'),
        Index('ix_pwa_push_subscriptions_endpoint', 'endpoint'),
        Index('ix_pwa_push_subscriptions_is_active', 'is_active'),
    )


class PWAAnalytics(Base):
    """Model for PWA usage analytics."""
    
    __tablename__ = "pwa_analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifest_id = Column(UUID(as_uuid=True), ForeignKey("pwa_manifests.id"), nullable=False)
    analytics_date = Column(DateTime, nullable=False)  # Date of analytics record
    daily_installations = Column(Integer, default=0, nullable=False)  # Daily installations
    daily_uninstallations = Column(Integer, default=0, nullable=False)  # Daily uninstallations
    daily_active_users = Column(Integer, default=0, nullable=False)  # Daily active users
    daily_sessions = Column(Integer, default=0, nullable=False)  # Daily sessions
    daily_page_views = Column(Integer, default=0, nullable=False)  # Daily page views
    avg_session_duration = Column(Float, default=0.0, nullable=False)  # Average session duration in seconds
    offline_usage_percentage = Column(Float, default=0.0, nullable=False)  # Percentage of offline usage
    cache_hit_rate = Column(Float, default=0.0, nullable=False)  # Cache hit rate percentage
    push_notification_sent = Column(Integer, default=0, nullable=False)  # Push notifications sent
    push_notification_opened = Column(Integer, default=0, nullable=False)  # Push notifications opened
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    manifest = relationship("PWAManifest", foreign_keys=[manifest_id])
    
    # Indexes
    __table_args__ = (
        Index('ix_pwa_analytics_manifest_id', 'manifest_id'),
        Index('ix_pwa_analytics_analytics_date', 'analytics_date'),
        Index('ix_pwa_analytics_daily_active_users', 'daily_active_users'),
    )


class PWAFeature(Base):
    """Model for PWA feature flags and capabilities."""
    
    __tablename__ = "pwa_features"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifest_id = Column(UUID(as_uuid=True), ForeignKey("pwa_manifests.id"), nullable=False)
    feature_name = Column(String(200), nullable=False)  # Feature name
    feature_description = Column(Text, nullable=True)  # Feature description
    is_enabled = Column(Boolean, default=True, nullable=False)  # Whether feature is enabled
    feature_config = Column(JSONB, nullable=True)  # Feature configuration
    browser_support = Column(JSONB, nullable=True)  # Browser support matrix
    platform_support = Column(JSONB, nullable=True)  # Platform support matrix
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    manifest = relationship("PWAManifest", foreign_keys=[manifest_id])
    
    # Indexes and constraints
    __table_args__ = (
        Index('ix_pwa_features_manifest_id', 'manifest_id'),
        Index('ix_pwa_features_feature_name', 'feature_name'),
        Index('ix_pwa_features_is_enabled', 'is_enabled'),
        UniqueConstraint('manifest_id', 'feature_name', name='uq_pwa_feature_manifest_name'),
    )
