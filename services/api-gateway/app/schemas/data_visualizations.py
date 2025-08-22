"""
Data Visualization Schemas for OpenPolicy V2

Comprehensive Pydantic schemas for data visualization and dashboard system.
Implements P2 priority feature for enhanced user insights and engagement.
"""

from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class ChartTypeEnum(str, Enum):
    """Chart type enumeration."""
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    SCATTER = "scatter"
    AREA = "area"
    HISTOGRAM = "histogram"
    BOX_PLOT = "box_plot"
    HEATMAP = "heatmap"
    RADAR = "radar"
    FUNNEL = "funnel"
    TREE_MAP = "tree_map"
    SANKEY = "sankey"
    WATERFALL = "waterfall"


class VisualizationCategoryEnum(str, Enum):
    """Visualization category enumeration."""
    CHARTS = "charts"
    MAPS = "maps"
    TABLES = "tables"
    GAUGES = "gauges"
    NETWORKS = "networks"
    TIMELINES = "timelines"
    HIERARCHIES = "hierarchies"
    FLOWS = "flows"


class DataSourceEnum(str, Enum):
    """Data source enumeration."""
    BILLS = "bills"
    VOTES = "votes"
    MEMBERS = "members"
    COMMITTEES = "committees"
    DEBATES = "debates"
    GOVERNMENT_LEVELS = "government_levels"
    USER_VOTING = "user_voting"
    EMAIL_ALERTS = "email_alerts"
    HOUSE_STATUS = "house_status"
    RSS_FEEDS = "rss_feeds"
    LANGUAGE_SUPPORT = "language_support"


class ThemeEnum(str, Enum):
    """Dashboard theme enumeration."""
    DEFAULT = "default"
    DARK = "dark"
    LIGHT = "light"
    PARLIAMENTARY = "parliamentary"
    ACCESSIBLE = "accessible"
    HIGH_CONTRAST = "high_contrast"


class ColorSchemeEnum(str, Enum):
    """Color scheme enumeration."""
    DEFAULT = "default"
    PARLIAMENTARY = "parliamentary"
    ACCESSIBLE = "accessible"
    HIGH_CONTRAST = "high_contrast"
    CUSTOM = "custom"


# ============================================================================
# BASE MODELS
# ============================================================================

class VisualizationTypeBase(BaseModel):
    """Base model for visualization types."""
    model_config = ConfigDict(from_attributes=True)
    
    type_name: str = Field(..., min_length=1, max_length=100, description="Visualization type name")
    display_name: str = Field(..., min_length=1, max_length=200, description="Human-readable name")
    description: str = Field(..., min_length=1, description="Description of the visualization type")
    category: VisualizationCategoryEnum = Field(..., description="Visualization category")
    is_active: bool = Field(True, description="Whether visualization type is active")
    supported_data_types: List[str] = Field(..., description="Array of supported data types")
    configuration_schema: Dict[str, Any] = Field(..., description="JSON schema for configuration")
    default_options: Optional[Dict[str, Any]] = Field(None, description="Default configuration options")


class DataVisualizationBase(BaseModel):
    """Base model for data visualizations."""
    model_config = ConfigDict(from_attributes=True)
    
    title: str = Field(..., min_length=1, max_length=500, description="Visualization title")
    description: Optional[str] = Field(None, description="Visualization description")
    visualization_type_id: str = Field(..., description="Visualization type ID")
    data_source: DataSourceEnum = Field(..., description="Source of data")
    data_query: Dict[str, Any] = Field(..., description="Query parameters for data retrieval")
    configuration: Dict[str, Any] = Field(..., description="Visualization configuration")
    is_public: bool = Field(True, description="Whether visualization is publicly accessible")
    is_featured: bool = Field(False, description="Whether visualization is featured")
    created_by: str = Field(..., min_length=1, max_length=100, description="Who created the visualization")
    tags: Optional[List[str]] = Field(None, description="Array of tags for categorization")


class DashboardBase(BaseModel):
    """Base model for dashboards."""
    model_config = ConfigDict(from_attributes=True)
    
    title: str = Field(..., min_length=1, max_length=500, description="Dashboard title")
    description: Optional[str] = Field(None, description="Dashboard description")
    layout_config: Dict[str, Any] = Field(..., description="Dashboard layout configuration")
    theme: ThemeEnum = Field(ThemeEnum.DEFAULT, description="Dashboard theme")
    is_public: bool = Field(True, description="Whether dashboard is publicly accessible")
    is_featured: bool = Field(False, description="Whether dashboard is featured")
    created_by: str = Field(..., min_length=1, max_length=100, description="Who created the dashboard")
    tags: Optional[List[str]] = Field(None, description="Array of tags for categorization")
    refresh_interval: int = Field(300, ge=30, le=3600, description="Refresh interval in seconds")


class DashboardVisualizationBase(BaseModel):
    """Base model for dashboard visualizations."""
    model_config = ConfigDict(from_attributes=True)
    
    dashboard_id: str = Field(..., description="Dashboard ID")
    visualization_id: str = Field(..., description="Visualization ID")
    position_x: int = Field(..., ge=0, description="X position in dashboard grid")
    position_y: int = Field(..., ge=0, description="Y position in dashboard grid")
    width: int = Field(..., ge=1, le=12, description="Width in grid units")
    height: int = Field(..., ge=1, le=12, description="Height in grid units")
    title_override: Optional[str] = Field(None, max_length=500, description="Override visualization title")
    is_visible: bool = Field(True, description="Whether visualization is visible")
    refresh_interval: Optional[int] = Field(None, ge=30, le=3600, description="Individual refresh interval")
    custom_config: Optional[Dict[str, Any]] = Field(None, description="Custom configuration for this instance")


class VisualizationTemplateBase(BaseModel):
    """Base model for visualization templates."""
    model_config = ConfigDict(from_attributes=True)
    
    template_name: str = Field(..., min_length=1, max_length=200, description="Template name")
    display_name: str = Field(..., min_length=1, max_length=500, description="Human-readable name")
    description: str = Field(..., min_length=1, description="Template description")
    category: VisualizationCategoryEnum = Field(..., description="Template category")
    visualization_type_id: str = Field(..., description="Visualization type ID")
    default_configuration: Dict[str, Any] = Field(..., description="Default configuration")
    sample_data: Optional[Dict[str, Any]] = Field(None, description="Sample data for preview")
    is_active: bool = Field(True, description="Whether template is active")
    created_by: str = Field(..., min_length=1, max_length=100, description="Who created the template")


class ChartConfigurationBase(BaseModel):
    """Base model for chart configurations."""
    model_config = ConfigDict(from_attributes=True)
    
    visualization_id: str = Field(..., description="Visualization ID")
    chart_type: ChartTypeEnum = Field(..., description="Specific chart type")
    axis_config: Optional[Dict[str, Any]] = Field(None, description="Axis configuration")
    color_scheme: ColorSchemeEnum = Field(ColorSchemeEnum.DEFAULT, description="Color scheme")
    legend_config: Optional[Dict[str, Any]] = Field(None, description="Legend configuration")
    tooltip_config: Optional[Dict[str, Any]] = Field(None, description="Tooltip configuration")
    animation_config: Optional[Dict[str, Any]] = Field(None, description="Animation configuration")
    responsive_config: Optional[Dict[str, Any]] = Field(None, description="Responsive behavior configuration")
    accessibility_config: Optional[Dict[str, Any]] = Field(None, description="Accessibility configuration")


# ============================================================================
# REQUEST MODELS
# ============================================================================

class VisualizationTypeCreateRequest(VisualizationTypeBase):
    """Request model for creating visualization types."""
    pass


class VisualizationTypeUpdateRequest(BaseModel):
    """Request model for updating visualization types."""
    display_name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    category: Optional[VisualizationCategoryEnum] = None
    is_active: Optional[bool] = None
    supported_data_types: Optional[List[str]] = None
    configuration_schema: Optional[Dict[str, Any]] = None
    default_options: Optional[Dict[str, Any]] = None


class DataVisualizationCreateRequest(DataVisualizationBase):
    """Request model for creating data visualizations."""
    pass


class DataVisualizationUpdateRequest(BaseModel):
    """Request model for updating data visualizations."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    data_query: Optional[Dict[str, Any]] = None
    configuration: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None
    is_featured: Optional[bool] = None
    tags: Optional[List[str]] = None


class DashboardCreateRequest(DashboardBase):
    """Request model for creating dashboards."""
    pass


class DashboardUpdateRequest(BaseModel):
    """Request model for updating dashboards."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    layout_config: Optional[Dict[str, Any]] = None
    theme: Optional[ThemeEnum] = None
    is_public: Optional[bool] = None
    is_featured: Optional[bool] = None
    tags: Optional[List[str]] = None
    refresh_interval: Optional[int] = Field(None, ge=30, le=3600)


class DashboardVisualizationCreateRequest(DashboardVisualizationBase):
    """Request model for creating dashboard visualizations."""
    pass


class DashboardVisualizationUpdateRequest(BaseModel):
    """Request model for updating dashboard visualizations."""
    position_x: Optional[int] = Field(None, ge=0)
    position_y: Optional[int] = Field(None, ge=0)
    width: Optional[int] = Field(None, ge=1, le=12)
    height: Optional[int] = Field(None, ge=1, le=12)
    title_override: Optional[str] = Field(None, max_length=500)
    is_visible: Optional[bool] = None
    refresh_interval: Optional[int] = Field(None, ge=30, le=3600)
    custom_config: Optional[Dict[str, Any]] = None


class VisualizationTemplateCreateRequest(VisualizationTemplateBase):
    """Request model for creating visualization templates."""
    pass


class VisualizationTemplateUpdateRequest(BaseModel):
    """Request model for updating visualization templates."""
    display_name: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = Field(None, min_length=1)
    category: Optional[VisualizationCategoryEnum] = None
    default_configuration: Optional[Dict[str, Any]] = None
    sample_data: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class ChartConfigurationCreateRequest(ChartConfigurationBase):
    """Request model for creating chart configurations."""
    pass


class ChartConfigurationUpdateRequest(BaseModel):
    """Request model for updating chart configurations."""
    chart_type: Optional[ChartTypeEnum] = None
    axis_config: Optional[Dict[str, Any]] = None
    color_scheme: Optional[ColorSchemeEnum] = None
    legend_config: Optional[Dict[str, Any]] = None
    tooltip_config: Optional[Dict[str, Any]] = None
    animation_config: Optional[Dict[str, Any]] = None
    responsive_config: Optional[Dict[str, Any]] = None
    accessibility_config: Optional[Dict[str, Any]] = None


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class VisualizationTypeResponse(VisualizationTypeBase):
    """Response model for visualization types."""
    id: str
    created_at: datetime
    updated_at: datetime


class DataVisualizationResponse(DataVisualizationBase):
    """Response model for data visualizations."""
    id: str
    view_count: int
    last_generated: Optional[datetime]
    generation_time_ms: Optional[int]
    cache_key: Optional[str]
    cache_expires: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class DashboardResponse(DashboardBase):
    """Response model for dashboards."""
    id: str
    view_count: int
    last_accessed: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class DashboardVisualizationResponse(DashboardVisualizationBase):
    """Response model for dashboard visualizations."""
    id: str
    created_at: datetime
    updated_at: datetime


class VisualizationTemplateResponse(VisualizationTemplateBase):
    """Response model for visualization templates."""
    id: str
    usage_count: int
    created_at: datetime
    updated_at: datetime


class ChartConfigurationResponse(ChartConfigurationBase):
    """Response model for chart configurations."""
    id: str
    created_at: datetime
    updated_at: datetime


# ============================================================================
# LIST RESPONSE MODELS
# ============================================================================

class VisualizationTypeListResponse(BaseModel):
    """List response model for visualization types."""
    types: List[VisualizationTypeResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class DataVisualizationListResponse(BaseModel):
    """List response model for data visualizations."""
    visualizations: List[DataVisualizationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class DashboardListResponse(BaseModel):
    """List response model for dashboards."""
    dashboards: List[DashboardResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class DashboardVisualizationListResponse(BaseModel):
    """List response model for dashboard visualizations."""
    dashboard_visualizations: List[DashboardVisualizationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class VisualizationTemplateListResponse(BaseModel):
    """List response model for visualization templates."""
    templates: List[VisualizationTemplateResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


# ============================================================================
# SPECIALIZED MODELS
# ============================================================================

class VisualizationDataRequest(BaseModel):
    """Request model for generating visualization data."""
    visualization_id: str = Field(..., description="Visualization ID")
    force_regenerate: bool = Field(False, description="Force regeneration even if cached")
    custom_filters: Optional[Dict[str, Any]] = Field(None, description="Custom filters for this generation")
    output_format: str = Field("json", description="Output format (json, image, svg)")


class DashboardLayoutRequest(BaseModel):
    """Request model for updating dashboard layout."""
    dashboard_id: str = Field(..., description="Dashboard ID")
    layout_config: Dict[str, Any] = Field(..., description="New layout configuration")
    preserve_data: bool = Field(True, description="Whether to preserve existing data")


class VisualizationPreviewRequest(BaseModel):
    """Request model for previewing visualizations."""
    template_id: str = Field(..., description="Template ID")
    sample_data: Optional[Dict[str, Any]] = Field(None, description="Sample data for preview")
    configuration_overrides: Optional[Dict[str, Any]] = Field(None, description="Configuration overrides")


class ChartDataResponse(BaseModel):
    """Response model for chart data."""
    visualization_id: str = Field(..., description="Visualization ID")
    chart_type: ChartTypeEnum = Field(..., description="Chart type")
    data: Dict[str, Any] = Field(..., description="Chart data")
    configuration: Dict[str, Any] = Field(..., description="Chart configuration")
    metadata: Dict[str, Any] = Field(..., description="Chart metadata")
    generated_at: datetime = Field(..., description="When data was generated")
    cache_key: Optional[str] = Field(None, description="Cache key if cached")
    expires_at: Optional[datetime] = Field(None, description="When cache expires")


class DashboardFullResponse(BaseModel):
    """Full dashboard response with visualizations."""
    dashboard: DashboardResponse = Field(..., description="Dashboard information")
    visualizations: List[Dict[str, Any]] = Field(..., description="Dashboard visualizations with data")
    layout: Dict[str, Any] = Field(..., description="Layout configuration")
    theme: Dict[str, Any] = Field(..., description="Theme configuration")
    generated_at: datetime = Field(..., description="When dashboard was generated")


class VisualizationStatistics(BaseModel):
    """Model for visualization statistics."""
    visualization_id: str = Field(..., description="Visualization ID")
    title: str = Field(..., description="Visualization title")
    total_views: int = Field(..., description="Total views")
    total_generations: int = Field(..., description="Total generations")
    avg_generation_time: float = Field(..., description="Average generation time in ms")
    cache_hit_rate: float = Field(..., description="Cache hit rate percentage")
    last_24h_views: int = Field(..., description="Views in last 24 hours")
    last_7d_views: int = Field(..., description="Views in last 7 days")
    user_engagement_score: float = Field(..., description="User engagement score")
    generated_at: datetime = Field(..., description="When statistics were generated")


class SystemVisualizationOverview(BaseModel):
    """Model for system-wide visualization overview."""
    total_visualizations: int = Field(..., description="Total visualizations")
    total_dashboards: int = Field(..., description="Total dashboards")
    total_templates: int = Field(..., description="Total templates")
    total_views_24h: int = Field(..., description="Total views in last 24 hours")
    avg_generation_time: float = Field(..., description="Average generation time across all visualizations")
    cache_performance: Dict[str, float] = Field(..., description="Cache performance metrics")
    popular_visualizations: List[Dict[str, Union[str, int]]] = Field(..., description="Most popular visualizations")
    popular_dashboards: List[Dict[str, Union[str, int]]] = Field(..., description="Most popular dashboards")
    generated_at: datetime = Field(..., description="When overview was generated")


class VisualizationExportRequest(BaseModel):
    """Request model for exporting visualizations."""
    visualization_id: str = Field(..., description="Visualization ID")
    export_format: str = Field("png", description="Export format (png, jpg, svg, pdf)")
    width: Optional[int] = Field(None, ge=100, le=4000, description="Export width in pixels")
    height: Optional[int] = Field(None, ge=100, le=4000, description="Export height in pixels")
    include_data: bool = Field(False, description="Whether to include data in export")
    custom_styling: Optional[Dict[str, Any]] = Field(None, description="Custom styling for export")
