"""
Data Dashboard Schemas

Pydantic schemas for enhanced dashboard functionality.
Implements FEAT-005 Data Dashboard (P2 priority).
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum


# Enums (matching model enums)
class DashboardType(str, Enum):
    """Types of dashboards."""
    OVERVIEW = "overview"
    ANALYTICS = "analytics"
    PERFORMANCE = "performance"
    LEGISLATIVE = "legislative"
    MEMBER = "member"
    BILL = "bill"
    COMMITTEE = "committee"
    CUSTOM = "custom"


class WidgetType(str, Enum):
    """Types of dashboard widgets."""
    CHART = "chart"
    METRIC = "metric"
    TABLE = "table"
    MAP = "map"
    TIMELINE = "timeline"
    ACTIVITY_FEED = "activity_feed"
    COMPARISON = "comparison"
    HEATMAP = "heatmap"


class RefreshInterval(str, Enum):
    """Data refresh intervals."""
    REAL_TIME = "real_time"
    MINUTE_1 = "1m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    HOUR_1 = "1h"
    HOUR_6 = "6h"
    DAILY = "daily"
    MANUAL = "manual"


class TrendDirection(str, Enum):
    """Trend directions for metrics."""
    UP = "up"
    DOWN = "down"
    STABLE = "stable"


# Template schemas
class DashboardTemplateBase(BaseModel):
    """Base dashboard template schema."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    type: DashboardType
    is_public: bool = True
    requires_auth: bool = False
    layout_config: Dict[str, Any] = Field(..., description="Grid layout configuration")
    widget_configs: List[Dict[str, Any]] = Field(..., description="Widget configurations")
    tags: Optional[List[str]] = None
    category: Optional[str] = Field(None, max_length=100)
    icon: Optional[str] = Field(None, max_length=100)


class DashboardTemplateCreate(DashboardTemplateBase):
    """Schema for creating dashboard template."""
    pass


class DashboardTemplateUpdate(BaseModel):
    """Schema for updating dashboard template."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    is_public: Optional[bool] = None
    layout_config: Optional[Dict[str, Any]] = None
    widget_configs: Optional[List[Dict[str, Any]]] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = Field(None, max_length=100)
    icon: Optional[str] = Field(None, max_length=100)


class DashboardTemplateResponse(DashboardTemplateBase):
    """Schema for dashboard template responses."""
    id: UUID
    slug: str
    is_default: bool
    created_at: datetime
    updated_at: datetime
    usage_count: int = 0
    
    class Config:
        orm_mode = True


# Dashboard schemas
class DashboardBase(BaseModel):
    """Base dashboard schema."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    type: DashboardType
    layout_config: Dict[str, Any]
    theme: Optional[Dict[str, Any]] = None
    is_public: bool = False
    refresh_interval: RefreshInterval = RefreshInterval.MINUTE_5


class DashboardCreate(DashboardBase):
    """Schema for creating dashboard."""
    template_id: Optional[UUID] = Field(None, description="Template to base dashboard on")
    is_favorite: bool = False


class DashboardUpdate(BaseModel):
    """Schema for updating dashboard."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    layout_config: Optional[Dict[str, Any]] = None
    theme: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None
    is_favorite: Optional[bool] = None
    refresh_interval: Optional[RefreshInterval] = None


class DashboardResponse(DashboardBase):
    """Schema for dashboard responses."""
    id: UUID
    user_id: UUID
    template_id: Optional[UUID]
    slug: str
    is_favorite: bool
    share_token: Optional[str]
    share_expires_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    last_accessed_at: Optional[datetime]
    widget_count: int = 0
    
    class Config:
        orm_mode = True


class DashboardListResponse(BaseModel):
    """Schema for dashboard list responses."""
    results: List[DashboardResponse]
    pagination: Dict[str, Any]
    
    class Config:
        orm_mode = True


# Widget schemas
class WidgetBase(BaseModel):
    """Base widget schema."""
    widget_type: WidgetType
    title: str = Field(..., min_length=1, max_length=200)
    subtitle: Optional[str] = Field(None, max_length=500)
    data_source: str = Field(..., description="API endpoint or query ID")
    data_query: Dict[str, Any] = Field(..., description="Query parameters")
    data_filters: Optional[Dict[str, Any]] = None
    display_config: Dict[str, Any] = Field(..., description="Display configuration")
    position: Dict[str, int] = Field(..., description="Grid position {x, y, w, h}")
    
    @validator('position')
    def validate_position(cls, v):
        required_keys = {'x', 'y', 'w', 'h'}
        if not all(key in v for key in required_keys):
            raise ValueError(f'Position must contain keys: {required_keys}')
        if any(v[key] < 0 for key in required_keys):
            raise ValueError('Position values must be non-negative')
        return v


class WidgetCreate(WidgetBase):
    """Schema for creating widget."""
    is_interactive: bool = True
    click_action: Optional[Dict[str, Any]] = None
    drill_down_config: Optional[Dict[str, Any]] = None
    cache_duration: Optional[int] = Field(None, ge=0, description="Cache duration in seconds")


class WidgetUpdate(BaseModel):
    """Schema for updating widget."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    subtitle: Optional[str] = Field(None, max_length=500)
    data_query: Optional[Dict[str, Any]] = None
    data_filters: Optional[Dict[str, Any]] = None
    display_config: Optional[Dict[str, Any]] = None
    position: Optional[Dict[str, int]] = None
    is_interactive: Optional[bool] = None
    click_action: Optional[Dict[str, Any]] = None
    cache_duration: Optional[int] = Field(None, ge=0)


class WidgetResponse(WidgetBase):
    """Schema for widget responses."""
    id: UUID
    dashboard_id: UUID
    is_interactive: bool
    click_action: Optional[Dict[str, Any]]
    drill_down_config: Optional[Dict[str, Any]]
    cache_duration: Optional[int]
    last_refresh: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Metric schemas
class MetricValue(BaseModel):
    """Schema for metric values."""
    value: Any
    formatted: str
    raw: Any


class WidgetMetricResponse(BaseModel):
    """Schema for widget metric responses."""
    id: UUID
    metric_key: str
    metric_label: str
    metric_value: MetricValue
    previous_value: Optional[MetricValue]
    change_percentage: Optional[float]
    trend_direction: Optional[TrendDirection]
    format_type: Optional[str]
    unit: Optional[str]
    icon: Optional[str]
    color: Optional[str]
    calculated_at: datetime
    
    class Config:
        orm_mode = True


# Alert schemas
class AlertCondition(BaseModel):
    """Schema for alert conditions."""
    metric_key: str
    operator: str = Field(..., regex="^(gt|lt|gte|lte|eq|ne|contains|change_pct)$")
    threshold: Any
    time_window: Optional[int] = Field(None, description="Time window in minutes")


class AlertBase(BaseModel):
    """Base alert schema."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    condition: AlertCondition
    notification_channels: List[str] = Field(..., min_items=1)
    check_interval: RefreshInterval = RefreshInterval.MINUTE_15


class AlertCreate(AlertBase):
    """Schema for creating alert."""
    dashboard_id: Optional[UUID] = None
    widget_id: Optional[UUID] = None


class AlertUpdate(BaseModel):
    """Schema for updating alert."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    condition: Optional[AlertCondition] = None
    notification_channels: Optional[List[str]] = Field(None, min_items=1)
    is_active: Optional[bool] = None
    check_interval: Optional[RefreshInterval] = None


class AlertResponse(AlertBase):
    """Schema for alert responses."""
    id: UUID
    user_id: UUID
    dashboard_id: Optional[UUID]
    widget_id: Optional[UUID]
    is_active: bool
    last_checked: Optional[datetime]
    last_triggered: Optional[datetime]
    trigger_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Query schemas
class QueryBase(BaseModel):
    """Base query schema."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    query_type: str = Field(..., regex="^(sql|api|aggregate)$")
    query_config: Dict[str, Any]
    parameters: Optional[Dict[str, Any]] = None
    timeout_seconds: int = Field(30, ge=1, le=300)


class QueryCreate(QueryBase):
    """Schema for creating query."""
    is_public: bool = False
    required_permissions: Optional[List[str]] = None


class QueryUpdate(BaseModel):
    """Schema for updating query."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    query_config: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None
    timeout_seconds: Optional[int] = Field(None, ge=1, le=300)


class QueryResponse(QueryBase):
    """Schema for query responses."""
    id: UUID
    user_id: Optional[UUID]
    is_public: bool
    is_system: bool
    required_permissions: Optional[List[str]]
    estimated_cost: Optional[int]
    created_at: datetime
    updated_at: datetime
    last_executed: Optional[datetime]
    execution_count: int
    
    class Config:
        orm_mode = True


# Snapshot schemas
class SnapshotCreate(BaseModel):
    """Schema for creating snapshot."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    is_public: bool = False
    expires_at: Optional[datetime] = None
    tags: Optional[List[str]] = None


class SnapshotResponse(BaseModel):
    """Schema for snapshot responses."""
    id: UUID
    dashboard_id: UUID
    user_id: UUID
    name: str
    description: Optional[str]
    is_public: bool
    share_token: Optional[str]
    expires_at: Optional[datetime]
    tags: Optional[List[str]]
    view_count: int
    created_at: datetime
    
    class Config:
        orm_mode = True


# Data response schemas
class WidgetDataResponse(BaseModel):
    """Schema for widget data responses."""
    widget_id: UUID
    data: Any
    metadata: Dict[str, Any]
    cached: bool
    cache_expires_at: Optional[datetime]
    generated_at: datetime


class DashboardDataResponse(BaseModel):
    """Schema for dashboard data responses."""
    dashboard_id: UUID
    widgets: List[WidgetDataResponse]
    refresh_interval: RefreshInterval
    generated_at: datetime


# Analytics schemas
class DashboardAnalytics(BaseModel):
    """Schema for dashboard analytics."""
    dashboard_id: UUID
    view_count: int
    unique_viewers: int
    avg_session_duration: float
    most_viewed_widgets: List[Dict[str, Any]]
    peak_usage_times: List[Dict[str, Any]]
    performance_metrics: Dict[str, float]