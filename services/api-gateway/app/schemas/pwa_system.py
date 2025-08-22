"""
PWA System Schemas for OpenPolicy V2

Comprehensive Pydantic schemas for Progressive Web App (PWA) system.
Implements P2 priority feature for enhanced mobile accessibility and user experience.
"""

from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class DisplayModeEnum(str, Enum):
    """Display mode enumeration."""
    STANDALONE = "standalone"
    FULLSCREEN = "fullscreen"
    MINIMAL_UI = "minimal-ui"
    BROWSER = "browser"


class OrientationEnum(str, Enum):
    """Orientation enumeration."""
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"
    ANY = "any"


class CacheStrategyEnum(str, Enum):
    """Cache strategy enumeration."""
    CACHE_FIRST = "cache-first"
    NETWORK_FIRST = "network-first"
    STALE_WHILE_REVALIDATE = "stale-while-revalidate"
    NETWORK_ONLY = "network-only"
    CACHE_ONLY = "cache-only"


class ResourceTypeEnum(str, Enum):
    """Resource type enumeration."""
    HTML = "html"
    CSS = "css"
    JS = "js"
    IMAGE = "image"
    FONT = "font"
    API = "api"
    DOCUMENT = "document"
    MEDIA = "media"


class ResourceCategoryEnum(str, Enum):
    """Resource category enumeration."""
    CRITICAL = "critical"
    IMPORTANT = "important"
    OPTIONAL = "optional"


class DeviceTypeEnum(str, Enum):
    """Device type enumeration."""
    MOBILE = "mobile"
    TABLET = "tablet"
    DESKTOP = "desktop"


class PlatformEnum(str, Enum):
    """Platform enumeration."""
    IOS = "ios"
    ANDROID = "android"
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"


class InstallMethodEnum(str, Enum):
    """Install method enumeration."""
    MANUAL = "manual"
    PROMPT = "prompt"
    BANNER = "banner"
    AUTO = "auto"


# ============================================================================
# BASE MODELS
# ============================================================================

class PWAManifestBase(BaseModel):
    """Base model for PWA manifests."""
    model_config = ConfigDict(from_attributes=True)
    
    manifest_name: str = Field(..., min_length=1, max_length=200, description="Manifest identifier")
    app_name: str = Field(..., min_length=1, max_length=200, description="Application name")
    short_name: str = Field(..., min_length=1, max_length=100, description="Short application name")
    description: Optional[str] = Field(None, description="Application description")
    start_url: str = Field(..., min_length=1, max_length=500, description="Start URL for the app")
    display_mode: DisplayModeEnum = Field(DisplayModeEnum.STANDALONE, description="Display mode")
    orientation: OrientationEnum = Field(OrientationEnum.PORTRAIT, description="Orientation")
    theme_color: str = Field("#000000", max_length=7, description="Theme color in hex")
    background_color: str = Field("#ffffff", max_length=7, description="Background color in hex")
    scope: Optional[str] = Field(None, max_length=500, description="App scope")
    lang: str = Field("en", max_length=10, description="Language code")
    dir: str = Field("ltr", max_length=10, description="Text direction")
    categories: Optional[List[str]] = Field(None, description="App categories")
    icons: Dict[str, Any] = Field(..., description="App icons configuration")
    screenshots: Optional[List[Dict[str, Any]]] = Field(None, description="App screenshots")
    shortcuts: Optional[List[Dict[str, Any]]] = Field(None, description="App shortcuts")
    related_applications: Optional[List[Dict[str, Any]]] = Field(None, description="Related applications")
    prefer_related_applications: bool = Field(False, description="Prefer native apps")
    is_active: bool = Field(True, description="Whether manifest is active")
    is_default: bool = Field(False, description="Whether this is the default manifest")
    created_by: str = Field(..., min_length=1, max_length=100, description="Who created the manifest")


class ServiceWorkerBase(BaseModel):
    """Base model for service workers."""
    model_config = ConfigDict(from_attributes=True)
    
    manifest_id: str = Field(..., description="Manifest ID")
    worker_name: str = Field(..., min_length=1, max_length=200, description="Service worker name")
    worker_url: str = Field(..., min_length=1, max_length=500, description="Service worker URL")
    worker_scope: str = Field(..., min_length=1, max_length=500, description="Service worker scope")
    worker_version: str = Field(..., min_length=1, max_length=50, description="Service worker version")
    worker_script: str = Field(..., min_length=1, description="Service worker JavaScript code")
    is_active: bool = Field(True, description="Whether worker is active")
    is_default: bool = Field(False, description="Whether this is the default worker")
    cache_strategy: CacheStrategyEnum = Field(CacheStrategyEnum.NETWORK_FIRST, description="Cache strategy")
    offline_fallback: Optional[str] = Field(None, max_length=500, description="Offline fallback page")
    push_enabled: bool = Field(False, description="Whether push notifications are enabled")
    background_sync_enabled: bool = Field(False, description="Whether background sync is enabled")
    created_by: str = Field(..., min_length=1, max_length=100, description="Who created the worker")


class OfflineResourceBase(BaseModel):
    """Base model for offline resources."""
    model_config = ConfigDict(from_attributes=True)
    
    manifest_id: str = Field(..., description="Manifest ID")
    resource_url: str = Field(..., min_length=1, max_length=500, description="Resource URL")
    resource_type: ResourceTypeEnum = Field(..., description="Type of resource")
    resource_category: ResourceCategoryEnum = Field(..., description="Resource category")
    cache_duration: int = Field(86400, ge=0, description="Cache duration in seconds")
    is_offline_available: bool = Field(True, description="Whether resource is available offline")
    compression_enabled: bool = Field(True, description="Whether compression is enabled")
    version_hash: Optional[str] = Field(None, max_length=64, description="Resource version hash")
    file_size: Optional[int] = Field(None, ge=0, description="Resource file size in bytes")
    last_updated: Optional[datetime] = Field(None, description="When resource was last updated")


class CacheEntryBase(BaseModel):
    """Base model for cache entries."""
    model_config = ConfigDict(from_attributes=True)
    
    service_worker_id: str = Field(..., description="Service worker ID")
    cache_name: str = Field(..., min_length=1, max_length=200, description="Cache name")
    resource_url: str = Field(..., min_length=1, max_length=500, description="Cached resource URL")
    resource_type: ResourceTypeEnum = Field(..., description="Type of cached resource")
    cache_timestamp: datetime = Field(..., description="When resource was cached")
    cache_expiry: Optional[datetime] = Field(None, description="When cache expires")
    cache_size: Optional[int] = Field(None, ge=0, description="Cache size in bytes")
    cache_hits: int = Field(0, ge=0, description="Number of cache hits")
    last_accessed: Optional[datetime] = Field(None, description="Last time cache was accessed")
    is_valid: bool = Field(True, description="Whether cache entry is valid")


class PWAInstallationBase(BaseModel):
    """Base model for PWA installations."""
    model_config = ConfigDict(from_attributes=True)
    
    manifest_id: str = Field(..., description="Manifest ID")
    user_id: Optional[str] = Field(None, max_length=100, description="User ID if authenticated")
    session_id: str = Field(..., min_length=1, max_length=100, description="Session identifier")
    device_type: DeviceTypeEnum = Field(..., description="Device type")
    platform: PlatformEnum = Field(..., description="Platform")
    browser: str = Field(..., min_length=1, max_length=100, description="Browser name and version")
    install_method: InstallMethodEnum = Field(..., description="Install method")
    install_timestamp: datetime = Field(..., description="When PWA was installed")
    uninstall_timestamp: Optional[datetime] = Field(None, description="When PWA was uninstalled")
    is_active: bool = Field(True, description="Whether installation is active")
    last_used: Optional[datetime] = Field(None, description="Last time PWA was used")
    usage_count: int = Field(0, ge=0, description="Number of times PWA was used")


class PWAPushSubscriptionBase(BaseModel):
    """Base model for PWA push subscriptions."""
    model_config = ConfigDict(from_attributes=True)
    
    manifest_id: str = Field(..., description="Manifest ID")
    user_id: Optional[str] = Field(None, max_length=100, description="User ID if authenticated")
    endpoint: str = Field(..., min_length=1, description="Push subscription endpoint")
    p256dh_key: str = Field(..., min_length=1, max_length=200, description="P-256 DH key")
    auth_secret: str = Field(..., min_length=1, max_length=200, description="Authentication secret")
    subscription_data: Optional[Dict[str, Any]] = Field(None, description="Additional subscription data")
    is_active: bool = Field(True, description="Whether subscription is active")


class PWAAnalyticsBase(BaseModel):
    """Base model for PWA analytics."""
    model_config = ConfigDict(from_attributes=True)
    
    manifest_id: str = Field(..., description="Manifest ID")
    analytics_date: datetime = Field(..., description="Date of analytics record")
    daily_installations: int = Field(0, ge=0, description="Daily installations")
    daily_uninstallations: int = Field(0, ge=0, description="Daily uninstallations")
    daily_active_users: int = Field(0, ge=0, description="Daily active users")
    daily_sessions: int = Field(0, ge=0, description="Daily sessions")
    daily_page_views: int = Field(0, ge=0, description="Daily page views")
    avg_session_duration: float = Field(0.0, ge=0.0, description="Average session duration in seconds")
    offline_usage_percentage: float = Field(0.0, ge=0.0, le=100.0, description="Percentage of offline usage")
    cache_hit_rate: float = Field(0.0, ge=0.0, le=100.0, description="Cache hit rate percentage")
    push_notification_sent: int = Field(0, ge=0, description="Push notifications sent")
    push_notification_opened: int = Field(0, ge=0, description="Push notifications opened")


class PWAFeatureBase(BaseModel):
    """Base model for PWA features."""
    model_config = ConfigDict(from_attributes=True)
    
    manifest_id: str = Field(..., description="Manifest ID")
    feature_name: str = Field(..., min_length=1, max_length=200, description="Feature name")
    feature_description: Optional[str] = Field(None, description="Feature description")
    is_enabled: bool = Field(True, description="Whether feature is enabled")
    feature_config: Optional[Dict[str, Any]] = Field(None, description="Feature configuration")
    browser_support: Optional[Dict[str, Any]] = Field(None, description="Browser support matrix")
    platform_support: Optional[Dict[str, Any]] = Field(None, description="Platform support matrix")


# ============================================================================
# REQUEST MODELS
# ============================================================================

class PWAManifestCreateRequest(PWAManifestBase):
    """Request model for creating PWA manifests."""
    pass


class PWAManifestUpdateRequest(BaseModel):
    """Request model for updating PWA manifests."""
    app_name: Optional[str] = Field(None, min_length=1, max_length=200)
    short_name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    start_url: Optional[str] = Field(None, min_length=1, max_length=500)
    display_mode: Optional[DisplayModeEnum] = None
    orientation: Optional[OrientationEnum] = None
    theme_color: Optional[str] = Field(None, max_length=7)
    background_color: Optional[str] = Field(None, max_length=7)
    scope: Optional[str] = Field(None, max_length=500)
    lang: Optional[str] = Field(None, max_length=10)
    dir: Optional[str] = Field(None, max_length=10)
    categories: Optional[List[str]] = None
    icons: Optional[Dict[str, Any]] = None
    screenshots: Optional[List[Dict[str, Any]]] = None
    shortcuts: Optional[List[Dict[str, Any]]] = None
    related_applications: Optional[List[Dict[str, Any]]] = None
    prefer_related_applications: Optional[bool] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None


class ServiceWorkerCreateRequest(ServiceWorkerBase):
    """Request model for creating service workers."""
    pass


class ServiceWorkerUpdateRequest(BaseModel):
    """Request model for updating service workers."""
    worker_name: Optional[str] = Field(None, min_length=1, max_length=200)
    worker_url: Optional[str] = Field(None, min_length=1, max_length=500)
    worker_scope: Optional[str] = Field(None, min_length=1, max_length=500)
    worker_version: Optional[str] = Field(None, min_length=1, max_length=50)
    worker_script: Optional[str] = Field(None, min_length=1)
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None
    cache_strategy: Optional[CacheStrategyEnum] = None
    offline_fallback: Optional[str] = Field(None, max_length=500)
    push_enabled: Optional[bool] = None
    background_sync_enabled: Optional[bool] = None


class OfflineResourceCreateRequest(OfflineResourceBase):
    """Request model for creating offline resources."""
    pass


class OfflineResourceUpdateRequest(BaseModel):
    """Request model for updating offline resources."""
    resource_type: Optional[ResourceTypeEnum] = None
    resource_category: Optional[ResourceCategoryEnum] = None
    cache_duration: Optional[int] = Field(None, ge=0)
    is_offline_available: Optional[bool] = None
    compression_enabled: Optional[bool] = None
    version_hash: Optional[str] = Field(None, max_length=64)
    file_size: Optional[int] = Field(None, ge=0)
    last_updated: Optional[datetime] = None


class PWAInstallationCreateRequest(PWAInstallationBase):
    """Request model for creating PWA installations."""
    pass


class PWAInstallationUpdateRequest(BaseModel):
    """Request model for updating PWA installations."""
    is_active: Optional[bool] = None
    last_used: Optional[datetime] = None
    usage_count: Optional[int] = Field(None, ge=0)
    uninstall_timestamp: Optional[datetime] = None


class PWAPushSubscriptionCreateRequest(PWAPushSubscriptionBase):
    """Request model for creating PWA push subscriptions."""
    pass


class PWAPushSubscriptionUpdateRequest(BaseModel):
    """Request model for updating PWA push subscriptions."""
    is_active: Optional[bool] = None
    subscription_data: Optional[Dict[str, Any]] = None


class PWAFeatureCreateRequest(PWAFeatureBase):
    """Request model for creating PWA features."""
    pass


class PWAFeatureUpdateRequest(BaseModel):
    """Request model for updating PWA features."""
    feature_description: Optional[str] = None
    is_enabled: Optional[bool] = None
    feature_config: Optional[Dict[str, Any]] = None
    browser_support: Optional[Dict[str, Any]] = None
    platform_support: Optional[Dict[str, Any]] = None


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class PWAManifestResponse(PWAManifestBase):
    """Response model for PWA manifests."""
    id: str
    created_at: datetime
    updated_at: datetime


class ServiceWorkerResponse(ServiceWorkerBase):
    """Response model for service workers."""
    id: str
    created_at: datetime
    updated_at: datetime


class OfflineResourceResponse(OfflineResourceBase):
    """Response model for offline resources."""
    id: str
    created_at: datetime
    updated_at: datetime


class CacheEntryResponse(CacheEntryBase):
    """Response model for cache entries."""
    id: str
    created_at: datetime


class PWAInstallationResponse(PWAInstallationBase):
    """Response model for PWA installations."""
    id: str
    created_at: datetime
    updated_at: datetime


class PWAPushSubscriptionResponse(PWAPushSubscriptionBase):
    """Response model for PWA push subscriptions."""
    id: str
    created_at: datetime
    updated_at: datetime


class PWAAnalyticsResponse(PWAAnalyticsBase):
    """Response model for PWA analytics."""
    id: str
    created_at: datetime


class PWAFeatureResponse(PWAFeatureBase):
    """Response model for PWA features."""
    id: str
    created_at: datetime
    updated_at: datetime


# ============================================================================
# LIST RESPONSE MODELS
# ============================================================================

class PWAManifestListResponse(BaseModel):
    """List response model for PWA manifests."""
    manifests: List[PWAManifestResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class ServiceWorkerListResponse(BaseModel):
    """List response model for service workers."""
    workers: List[ServiceWorkerResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class OfflineResourceListResponse(BaseModel):
    """List response model for offline resources."""
    resources: List[OfflineResourceResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class CacheEntryListResponse(BaseModel):
    """List response model for cache entries."""
    entries: List[CacheEntryResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class PWAInstallationListResponse(BaseModel):
    """List response model for PWA installations."""
    installations: List[PWAInstallationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class PWAPushSubscriptionListResponse(BaseModel):
    """List response model for PWA push subscriptions."""
    subscriptions: List[PWAPushSubscriptionResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class PWAAnalyticsListResponse(BaseModel):
    """List response model for PWA analytics."""
    analytics: List[PWAAnalyticsResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class PWAFeatureListResponse(BaseModel):
    """List response model for PWA features."""
    features: List[PWAFeatureResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


# ============================================================================
# SPECIALIZED MODELS
# ============================================================================

class ManifestGenerationRequest(BaseModel):
    """Request model for generating PWA manifest."""
    app_name: str = Field(..., min_length=1, max_length=200, description="Application name")
    short_name: str = Field(..., min_length=1, max_length=100, description="Short application name")
    description: Optional[str] = Field(None, description="Application description")
    theme_color: str = Field("#000000", max_length=7, description="Theme color")
    background_color: str = Field("#ffffff", max_length=7, description="Background color")
    start_url: str = Field("/", description="Start URL")
    scope: str = Field("/", description="App scope")
    display_mode: DisplayModeEnum = Field(DisplayModeEnum.STANDALONE, description="Display mode")
    orientation: OrientationEnum = Field(OrientationEnum.PORTRAIT, description="Orientation")
    lang: str = Field("en", description="Language code")
    categories: Optional[List[str]] = Field(None, description="App categories")


class ServiceWorkerGenerationRequest(BaseModel):
    """Request model for generating service worker."""
    manifest_id: str = Field(..., description="Manifest ID")
    worker_name: str = Field(..., min_length=1, max_length=200, description="Worker name")
    cache_strategy: CacheStrategyEnum = Field(CacheStrategyEnum.NETWORK_FIRST, description="Cache strategy")
    offline_fallback: Optional[str] = Field(None, description="Offline fallback page")
    push_enabled: bool = Field(False, description="Enable push notifications")
    background_sync_enabled: bool = Field(False, description="Enable background sync")
    custom_script: Optional[str] = Field(None, description="Custom service worker code")


class PWAInstallationTrackingRequest(BaseModel):
    """Request model for tracking PWA installation."""
    manifest_id: str = Field(..., description="Manifest ID")
    session_id: str = Field(..., min_length=1, max_length=100, description="Session identifier")
    device_type: DeviceTypeEnum = Field(..., description="Device type")
    platform: PlatformEnum = Field(..., description="Platform")
    browser: str = Field(..., min_length=1, max_length=100, description="Browser information")
    install_method: InstallMethodEnum = Field(..., description="Install method")


class PWAPushNotificationRequest(BaseModel):
    """Request model for sending push notifications."""
    subscription_id: str = Field(..., description="Push subscription ID")
    title: str = Field(..., min_length=1, max_length=200, description="Notification title")
    body: str = Field(..., min_length=1, description="Notification body")
    icon: Optional[str] = Field(None, description="Notification icon URL")
    badge: Optional[str] = Field(None, description="Notification badge URL")
    image: Optional[str] = Field(None, description="Notification image URL")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional notification data")
    actions: Optional[List[Dict[str, Any]]] = Field(None, description="Notification actions")
    tag: Optional[str] = Field(None, description="Notification tag")
    require_interaction: bool = Field(False, description="Require user interaction")
    silent: bool = Field(False, description="Silent notification")


class PWAStatistics(BaseModel):
    """Model for PWA statistics."""
    manifest_id: str = Field(..., description="Manifest ID")
    app_name: str = Field(..., description="Application name")
    total_installations: int = Field(..., description="Total installations")
    active_installations: int = Field(..., description="Active installations")
    total_users: int = Field(..., description="Total users")
    daily_active_users: int = Field(..., description="Daily active users")
    avg_session_duration: float = Field(..., description="Average session duration")
    offline_usage_percentage: float = Field(..., description="Offline usage percentage")
    cache_hit_rate: float = Field(..., description="Cache hit rate")
    push_notification_rate: float = Field(..., description="Push notification open rate")
    generated_at: datetime = Field(..., description="When statistics were generated")


class SystemPWAOverview(BaseModel):
    """Model for system-wide PWA overview."""
    total_manifests: int = Field(..., description="Total PWA manifests")
    active_manifests: int = Field(..., description="Active PWA manifests")
    total_installations: int = Field(..., description="Total PWA installations")
    total_service_workers: int = Field(..., description="Total service workers")
    total_offline_resources: int = Field(..., description="Total offline resources")
    total_push_subscriptions: int = Field(..., description="Total push subscriptions")
    avg_installation_rate: float = Field(..., description="Average daily installation rate")
    avg_engagement_score: float = Field(..., description="Average user engagement score")
    popular_platforms: List[Dict[str, Union[str, int]]] = Field(..., description="Most popular platforms")
    popular_browsers: List[Dict[str, Union[str, int]]] = Field(..., description="Most popular browsers")
    generated_at: datetime = Field(..., description="When overview was generated")


class PWAHealthCheck(BaseModel):
    """Model for PWA health check."""
    manifest_id: str = Field(..., description="Manifest ID")
    manifest_status: str = Field(..., description="Manifest status")
    service_worker_status: str = Field(..., description="Service worker status")
    offline_resources_status: str = Field(..., description="Offline resources status")
    cache_status: str = Field(..., description="Cache status")
    push_notification_status: str = Field(..., description="Push notification status")
    overall_health: str = Field(..., description="Overall health status")
    issues: List[str] = Field(..., description="List of issues found")
    recommendations: List[str] = Field(..., description="List of recommendations")
    checked_at: datetime = Field(..., description="When health check was performed")
