"""
Data Dashboard Models

Enhanced dashboard models for comprehensive data analytics.
Implements FEAT-005 Data Dashboard (P2 priority).
"""

from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey, Index, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime


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


class DashboardTemplate(Base):
    """Pre-defined dashboard templates."""
    
    __tablename__ = "dashboard_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Template details
    name = Column(String(200), unique=True, nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    type = Column(SQLEnum(DashboardType), nullable=False)
    
    # Configuration
    is_public = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    requires_auth = Column(Boolean, default=False, nullable=False)
    
    # Layout and widgets
    layout_config = Column(JSONB, nullable=False)  # Grid layout configuration
    widget_configs = Column(JSONB, nullable=False)  # Array of widget configurations
    
    # Metadata
    tags = Column(JSONB, nullable=True)  # Array of tags
    category = Column(String(100), nullable=True)
    icon = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    dashboards = relationship("UserDashboard", back_populates="template")
    
    # Indexes
    __table_args__ = (
        Index('idx_template_slug', 'slug'),
        Index('idx_template_type', 'type'),
        Index('idx_template_public', 'is_public'),
    )


class UserDashboard(Base):
    """User-specific dashboard instances."""
    
    __tablename__ = "user_dashboards"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    template_id = Column(UUID(as_uuid=True), ForeignKey("dashboard_templates.id"), nullable=True)
    
    # Dashboard details
    name = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(SQLEnum(DashboardType), nullable=False)
    
    # Customization
    layout_config = Column(JSONB, nullable=False)  # User's custom layout
    theme = Column(JSONB, nullable=True)  # Custom theme settings
    
    # Settings
    is_public = Column(Boolean, default=False, nullable=False)
    is_favorite = Column(Boolean, default=False, nullable=False)
    refresh_interval = Column(SQLEnum(RefreshInterval), default=RefreshInterval.MINUTE_5, nullable=False)
    
    # Sharing
    share_token = Column(String(100), unique=True, nullable=True)
    share_expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_accessed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", backref="dashboards")
    template = relationship("DashboardTemplate", back_populates="dashboards")
    widgets = relationship("DashboardWidget", back_populates="dashboard", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_dashboard_user', 'user_id'),
        Index('idx_dashboard_slug', 'user_id', 'slug', unique=True),
        Index('idx_dashboard_favorite', 'user_id', 'is_favorite'),
        Index('idx_dashboard_share_token', 'share_token'),
    )


class DashboardWidget(Base):
    """Individual widgets within a dashboard."""
    
    __tablename__ = "dashboard_widgets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dashboard_id = Column(UUID(as_uuid=True), ForeignKey("user_dashboards.id"), nullable=False)
    
    # Widget details
    widget_type = Column(SQLEnum(WidgetType), nullable=False)
    title = Column(String(200), nullable=False)
    subtitle = Column(String(500), nullable=True)
    
    # Data configuration
    data_source = Column(String(100), nullable=False)  # API endpoint or query ID
    data_query = Column(JSONB, nullable=False)  # Query parameters
    data_filters = Column(JSONB, nullable=True)  # Active filters
    
    # Display configuration
    display_config = Column(JSONB, nullable=False)  # Chart type, colors, etc.
    position = Column(JSONB, nullable=False)  # Grid position {x, y, w, h}
    
    # Interactivity
    is_interactive = Column(Boolean, default=True, nullable=False)
    click_action = Column(JSONB, nullable=True)  # Action on click
    drill_down_config = Column(JSONB, nullable=True)  # Drill-down settings
    
    # Caching
    cache_duration = Column(Integer, nullable=True)  # Seconds to cache
    last_refresh = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    dashboard = relationship("UserDashboard", back_populates="widgets")
    metrics = relationship("WidgetMetric", back_populates="widget", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_widget_dashboard', 'dashboard_id'),
        Index('idx_widget_type', 'widget_type'),
    )


class WidgetMetric(Base):
    """Metrics displayed in widgets."""
    
    __tablename__ = "widget_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    widget_id = Column(UUID(as_uuid=True), ForeignKey("dashboard_widgets.id"), nullable=False)
    
    # Metric details
    metric_key = Column(String(100), nullable=False)
    metric_label = Column(String(200), nullable=False)
    metric_value = Column(JSONB, nullable=False)  # Current value
    
    # Comparison data
    previous_value = Column(JSONB, nullable=True)  # For trend calculation
    change_percentage = Column(JSONB, nullable=True)
    trend_direction = Column(String(20), nullable=True)  # up, down, stable
    
    # Display
    format_type = Column(String(50), nullable=True)  # number, currency, percentage
    unit = Column(String(50), nullable=True)
    icon = Column(String(100), nullable=True)
    color = Column(String(50), nullable=True)
    
    # Timestamps
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    widget = relationship("DashboardWidget", back_populates="metrics")
    
    # Indexes
    __table_args__ = (
        Index('idx_metric_widget', 'widget_id'),
        Index('idx_metric_key', 'metric_key'),
    )


class DashboardAlert(Base):
    """Alerts based on dashboard metrics."""
    
    __tablename__ = "dashboard_alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    dashboard_id = Column(UUID(as_uuid=True), ForeignKey("user_dashboards.id"), nullable=True)
    widget_id = Column(UUID(as_uuid=True), ForeignKey("dashboard_widgets.id"), nullable=True)
    
    # Alert configuration
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    condition = Column(JSONB, nullable=False)  # Alert condition configuration
    
    # Notification settings
    is_active = Column(Boolean, default=True, nullable=False)
    notification_channels = Column(JSONB, nullable=False)  # email, in-app, etc.
    
    # Frequency control
    check_interval = Column(SQLEnum(RefreshInterval), default=RefreshInterval.MINUTE_15, nullable=False)
    last_checked = Column(DateTime(timezone=True), nullable=True)
    last_triggered = Column(DateTime(timezone=True), nullable=True)
    trigger_count = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    dashboard = relationship("UserDashboard")
    widget = relationship("DashboardWidget")
    
    # Indexes
    __table_args__ = (
        Index('idx_alert_user', 'user_id'),
        Index('idx_alert_active', 'is_active'),
        Index('idx_alert_check', 'is_active', 'check_interval'),
    )


class DataQuery(Base):
    """Saved data queries for dashboards."""
    
    __tablename__ = "data_queries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Query details
    name = Column(String(200), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    query_type = Column(String(50), nullable=False)  # sql, api, aggregate
    
    # Query configuration
    query_config = Column(JSONB, nullable=False)  # SQL query, API params, etc.
    parameters = Column(JSONB, nullable=True)  # Query parameters
    
    # Permissions
    is_public = Column(Boolean, default=False, nullable=False)
    is_system = Column(Boolean, default=False, nullable=False)
    required_permissions = Column(JSONB, nullable=True)
    
    # Performance
    estimated_cost = Column(Integer, nullable=True)  # Query cost estimate
    timeout_seconds = Column(Integer, default=30, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_executed = Column(DateTime(timezone=True), nullable=True)
    execution_count = Column(Integer, default=0, nullable=False)
    
    # Relationships
    user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_query_name', 'name'),
        Index('idx_query_type', 'query_type'),
        Index('idx_query_public', 'is_public'),
    )


class DashboardSnapshot(Base):
    """Snapshots of dashboard states for sharing or history."""
    
    __tablename__ = "dashboard_snapshots"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dashboard_id = Column(UUID(as_uuid=True), ForeignKey("user_dashboards.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Snapshot details
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Snapshot data
    dashboard_state = Column(JSONB, nullable=False)  # Complete dashboard state
    widget_data = Column(JSONB, nullable=False)  # All widget data at time of snapshot
    
    # Sharing
    is_public = Column(Boolean, default=False, nullable=False)
    share_token = Column(String(100), unique=True, nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    tags = Column(JSONB, nullable=True)
    view_count = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    dashboard = relationship("UserDashboard")
    user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_snapshot_dashboard', 'dashboard_id'),
        Index('idx_snapshot_user', 'user_id'),
        Index('idx_snapshot_public', 'is_public'),
        Index('idx_snapshot_token', 'share_token'),
    )