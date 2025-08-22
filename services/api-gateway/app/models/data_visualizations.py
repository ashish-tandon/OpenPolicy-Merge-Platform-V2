"""
Data Visualization Models for OpenPolicy V2

Comprehensive models for data visualization and dashboard system.
Implements P2 priority feature for enhanced user insights and engagement.
"""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, ForeignKey, Index, UniqueConstraint, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base


class VisualizationType(Base):
    """Model for supported visualization types."""
    
    __tablename__ = "visualization_types"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_name = Column(String(100), nullable=False, unique=True)  # bar, line, pie, scatter, etc.
    display_name = Column(String(200), nullable=False)  # Human-readable name
    description = Column(Text, nullable=False)  # Description of the visualization type
    category = Column(String(100), nullable=False)  # charts, maps, tables, etc.
    is_active = Column(Boolean, default=True, nullable=False)
    supported_data_types = Column(JSONB, nullable=False)  # Array of supported data types
    configuration_schema = Column(JSONB, nullable=False)  # JSON schema for configuration
    default_options = Column(JSONB, nullable=True)  # Default configuration options
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    visualizations = relationship("DataVisualization", back_populates="visualization_type")
    
    # Indexes
    __table_args__ = (
        Index('ix_visualization_types_type_name', 'type_name'),
        Index('ix_visualization_types_category', 'category'),
        Index('ix_visualization_types_is_active', 'is_active'),
    )


class DataVisualization(Base):
    """Model for individual data visualizations."""
    
    __tablename__ = "data_visualizations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)  # Visualization title
    description = Column(Text, nullable=True)  # Visualization description
    visualization_type_id = Column(UUID(as_uuid=True), ForeignKey("visualization_types.id"), nullable=False)
    data_source = Column(String(200), nullable=False)  # Source of data (e.g., "bills", "votes", "members")
    data_query = Column(JSONB, nullable=False)  # Query parameters for data retrieval
    configuration = Column(JSONB, nullable=False)  # Visualization configuration
    is_public = Column(Boolean, default=True, nullable=False)  # Whether visualization is publicly accessible
    is_featured = Column(Boolean, default=False, nullable=False)  # Whether visualization is featured
    created_by = Column(String(100), nullable=False)  # Who created the visualization
    tags = Column(JSONB, nullable=True)  # Array of tags for categorization
    view_count = Column(Integer, default=0, nullable=False)  # Number of views
    last_generated = Column(DateTime, nullable=True)  # When visualization was last generated
    generation_time_ms = Column(Integer, nullable=True)  # Time taken to generate in milliseconds
    cache_key = Column(String(255), nullable=True, unique=True)  # Cache key for generated visualization
    cache_expires = Column(DateTime, nullable=True)  # When cache expires
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    visualization_type = relationship("VisualizationType", back_populates="visualizations")
    dashboard_visualizations = relationship("DashboardVisualization", back_populates="visualization", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_data_visualizations_visualization_type_id', 'visualization_type_id'),
        Index('ix_data_visualizations_data_source', 'data_source'),
        Index('ix_data_visualizations_is_public', 'is_public'),
        Index('ix_data_visualizations_is_featured', 'is_featured'),
        Index('ix_data_visualizations_created_by', 'created_by'),
        Index('ix_data_visualizations_view_count', 'view_count'),
        Index('ix_data_visualizations_last_generated', 'last_generated'),
        Index('ix_data_visualizations_cache_key', 'cache_key'),
    )


class Dashboard(Base):
    """Model for dashboard configurations."""
    
    __tablename__ = "dashboards"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)  # Dashboard title
    description = Column(Text, nullable=True)  # Dashboard description
    layout_config = Column(JSONB, nullable=False)  # Dashboard layout configuration
    theme = Column(String(100), default="default", nullable=False)  # Dashboard theme
    is_public = Column(Boolean, default=True, nullable=False)  # Whether dashboard is publicly accessible
    is_featured = Column(Boolean, default=False, nullable=False)  # Whether dashboard is featured
    created_by = Column(String(100), nullable=False)  # Who created the dashboard
    tags = Column(JSONB, nullable=True)  # Array of tags for categorization
    view_count = Column(Integer, default=0, nullable=False)  # Number of views
    last_accessed = Column(DateTime, nullable=True)  # When dashboard was last accessed
    refresh_interval = Column(Integer, default=300, nullable=False)  # Refresh interval in seconds
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    dashboard_visualizations = relationship("DashboardVisualization", back_populates="dashboard", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_dashboards_is_public', 'is_public'),
        Index('ix_dashboards_is_featured', 'is_featured'),
        Index('ix_dashboards_created_by', 'created_by'),
        Index('ix_dashboards_view_count', 'view_count'),
        Index('ix_dashboards_last_accessed', 'last_accessed'),
    )


class DashboardVisualization(Base):
    """Model for linking visualizations to dashboards."""
    
    __tablename__ = "dashboard_visualizations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dashboard_id = Column(UUID(as_uuid=True), ForeignKey("dashboards.id"), nullable=False)
    visualization_id = Column(UUID(as_uuid=True), ForeignKey("data_visualizations.id"), nullable=False)
    position_x = Column(Integer, nullable=False)  # X position in dashboard grid
    position_y = Column(Integer, nullable=False)  # Y position in dashboard grid
    width = Column(Integer, nullable=False)  # Width in grid units
    height = Column(Integer, nullable=False)  # Height in grid units
    title_override = Column(String(500), nullable=True)  # Override visualization title
    is_visible = Column(Boolean, default=True, nullable=False)  # Whether visualization is visible
    refresh_interval = Column(Integer, nullable=True)  # Individual refresh interval
    custom_config = Column(JSONB, nullable=True)  # Custom configuration for this instance
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    dashboard = relationship("Dashboard", back_populates="dashboard_visualizations")
    visualization = relationship("DataVisualization", back_populates="dashboard_visualizations")
    
    # Indexes and constraints
    __table_args__ = (
        Index('ix_dashboard_visualizations_dashboard_id', 'dashboard_id'),
        Index('ix_dashboard_visualizations_visualization_id', 'visualization_id'),
        Index('ix_dashboard_visualizations_position', 'position_x', 'position_y'),
        UniqueConstraint('dashboard_id', 'visualization_id', name='uq_dashboard_visualization_unique'),
    )


class VisualizationTemplate(Base):
    """Model for reusable visualization templates."""
    
    __tablename__ = "visualization_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_name = Column(String(200), nullable=False, unique=True)  # Template name
    display_name = Column(String(500), nullable=False)  # Human-readable name
    description = Column(Text, nullable=False)  # Template description
    category = Column(String(100), nullable=False)  # Template category
    visualization_type_id = Column(UUID(as_uuid=True), ForeignKey("visualization_types.id"), nullable=False)
    default_configuration = Column(JSONB, nullable=False)  # Default configuration
    sample_data = Column(JSONB, nullable=True)  # Sample data for preview
    is_active = Column(Boolean, default=True, nullable=False)
    created_by = Column(String(100), nullable=False)  # Who created the template
    usage_count = Column(Integer, default=0, nullable=False)  # How many times template was used
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    visualization_type = relationship("VisualizationType", foreign_keys=[visualization_type_id])
    
    # Indexes
    __table_args__ = (
        Index('ix_visualization_templates_template_name', 'template_name'),
        Index('ix_visualization_templates_category', 'category'),
        Index('ix_visualization_templates_is_active', 'is_active'),
        Index('ix_visualization_templates_usage_count', 'usage_count'),
    )


class VisualizationCache(Base):
    """Model for caching generated visualizations."""
    
    __tablename__ = "visualization_cache"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cache_key = Column(String(255), nullable=False, unique=True)  # Unique cache key
    visualization_id = Column(UUID(as_uuid=True), ForeignKey("data_visualizations.id"), nullable=False)
    data_hash = Column(String(64), nullable=False)  # Hash of input data
    config_hash = Column(String(64), nullable=False)  # Hash of configuration
    generated_data = Column(JSONB, nullable=False)  # Generated visualization data
    generated_image = Column(Text, nullable=True)  # Base64 encoded image (if applicable)
    data_size = Column(Integer, nullable=False)  # Size of generated data in bytes
    generation_time_ms = Column(Integer, nullable=False)  # Time taken to generate
    expires_at = Column(DateTime, nullable=False)  # When cache expires
    hits = Column(Integer, default=0, nullable=False)  # Number of cache hits
    last_hit = Column(DateTime, nullable=True)  # Last cache hit time
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    visualization = relationship("DataVisualization", foreign_keys=[visualization_id])
    
    # Indexes
    __table_args__ = (
        Index('ix_visualization_cache_cache_key', 'cache_key'),
        Index('ix_visualization_cache_visualization_id', 'visualization_id'),
        Index('ix_visualization_cache_expires_at', 'expires_at'),
        Index('ix_visualization_cache_data_hash', 'data_hash'),
        Index('ix_visualization_cache_last_hit', 'last_hit'),
    )


class VisualizationAnalytics(Base):
    """Model for tracking visualization usage and performance analytics."""
    
    __tablename__ = "visualization_analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    visualization_id = Column(UUID(as_uuid=True), ForeignKey("data_visualizations.id"), nullable=False)
    analytics_date = Column(DateTime, nullable=False)  # Date of analytics record
    daily_views = Column(Integer, default=0, nullable=False)  # Daily views
    daily_unique_users = Column(Integer, default=0, nullable=False)  # Daily unique users
    daily_generations = Column(Integer, default=0, nullable=False)  # Daily generations
    daily_cache_hits = Column(Integer, default=0, nullable=False)  # Daily cache hits
    avg_generation_time = Column(Float, default=0.0, nullable=False)  # Average generation time
    avg_data_size = Column(Float, default=0.0, nullable=False)  # Average data size
    error_count = Column(Integer, default=0, nullable=False)  # Error count
    user_engagement_score = Column(Float, default=0.0, nullable=False)  # User engagement score
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    visualization = relationship("DataVisualization", foreign_keys=[visualization_id])
    
    # Indexes
    __table_args__ = (
        Index('ix_visualization_analytics_visualization_id', 'visualization_id'),
        Index('ix_visualization_analytics_analytics_date', 'analytics_date'),
        Index('ix_visualization_analytics_daily_views', 'daily_views'),
    )


class ChartConfiguration(Base):
    """Model for chart-specific configuration options."""
    
    __tablename__ = "chart_configurations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    visualization_id = Column(UUID(as_uuid=True), ForeignKey("data_visualizations.id"), nullable=False)
    chart_type = Column(String(100), nullable=False)  # Specific chart type
    axis_config = Column(JSONB, nullable=True)  # Axis configuration
    color_scheme = Column(String(100), default="default", nullable=False)  # Color scheme
    legend_config = Column(JSONB, nullable=True)  # Legend configuration
    tooltip_config = Column(JSONB, nullable=True)  # Tooltip configuration
    animation_config = Column(JSONB, nullable=True)  # Animation configuration
    responsive_config = Column(JSONB, nullable=True)  # Responsive behavior configuration
    accessibility_config = Column(JSONB, nullable=True)  # Accessibility configuration
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    visualization = relationship("DataVisualization", foreign_keys=[visualization_id])
    
    # Indexes
    __table_args__ = (
        Index('ix_chart_configurations_visualization_id', 'visualization_id'),
        Index('ix_chart_configurations_chart_type', 'chart_type'),
        UniqueConstraint('visualization_id', name='uq_chart_configuration_visualization'),
    )
