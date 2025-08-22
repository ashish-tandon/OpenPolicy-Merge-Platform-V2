"""
Performance Optimization Models for OpenPolicy V2

Comprehensive models for performance optimization and system monitoring.
Implements P2 priority feature for enhanced system performance and user experience.
"""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, ForeignKey, Index, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base


class PerformanceMetric(Base):
    """Model for tracking performance metrics."""
    
    __tablename__ = "performance_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_name = Column(String(200), nullable=False)  # Metric identifier
    metric_type = Column(String(100), nullable=False)  # response_time, throughput, error_rate, etc.
    metric_category = Column(String(100), nullable=False)  # api, database, cache, external
    metric_value = Column(Float, nullable=False)  # Actual metric value
    metric_unit = Column(String(50), nullable=False)  # ms, requests/sec, percentage, etc.
    threshold_warning = Column(Float, nullable=True)  # Warning threshold
    threshold_critical = Column(Float, nullable=True)  # Critical threshold
    is_alert_enabled = Column(Boolean, default=True, nullable=False)  # Whether alerts are enabled
    collection_timestamp = Column(DateTime, nullable=False)  # When metric was collected
    source_endpoint = Column(String(500), nullable=True)  # Source endpoint or service
    user_agent = Column(String(500), nullable=True)  # User agent information
    ip_address = Column(String(45), nullable=True)  # IP address of request
    session_id = Column(String(100), nullable=True)  # Session identifier
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    alerts = relationship("PerformanceAlert", back_populates="metric", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_performance_metrics_metric_name', 'metric_name'),
        Index('ix_performance_metrics_metric_type', 'metric_type'),
        Index('ix_performance_metrics_metric_category', 'metric_category'),
        Index('ix_performance_metrics_collection_timestamp', 'collection_timestamp'),
        Index('ix_performance_metrics_source_endpoint', 'source_endpoint'),
    )


class PerformanceAlert(Base):
    """Model for performance alerts and notifications."""
    
    __tablename__ = "performance_alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_id = Column(UUID(as_uuid=True), ForeignKey("performance_metrics.id"), nullable=False)
    alert_type = Column(String(50), nullable=False)  # warning, critical, info
    alert_message = Column(Text, nullable=False)  # Alert message
    alert_severity = Column(String(50), nullable=False)  # low, medium, high, critical
    is_resolved = Column(Boolean, default=False, nullable=False)  # Whether alert is resolved
    resolved_at = Column(DateTime, nullable=True)  # When alert was resolved
    resolved_by = Column(String(100), nullable=True)  # Who resolved the alert
    resolution_notes = Column(Text, nullable=True)  # Notes about resolution
    notification_sent = Column(Boolean, default=False, nullable=False)  # Whether notification was sent
    notification_channels = Column(JSONB, nullable=True)  # Channels where notification was sent
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    metric = relationship("PerformanceMetric", back_populates="alerts")
    
    # Indexes
    __table_args__ = (
        Index('ix_performance_alerts_metric_id', 'metric_id'),
        Index('ix_performance_alerts_alert_type', 'alert_type'),
        Index('ix_performance_alerts_alert_severity', 'alert_severity'),
        Index('ix_performance_alerts_is_resolved', 'is_resolved'),
        Index('ix_performance_alerts_created_at', 'created_at'),
    )


class PerformanceBaseline(Base):
    """Model for performance baselines and thresholds."""
    
    __tablename__ = "performance_baselines"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    baseline_name = Column(String(200), nullable=False, unique=True)  # Baseline identifier
    metric_type = Column(String(100), nullable=False)  # Type of metric this baseline applies to
    metric_category = Column(String(100), nullable=False)  # Category of metric
    baseline_value = Column(Float, nullable=False)  # Baseline value
    baseline_unit = Column(String(50), nullable=False)  # Unit of measurement
    confidence_interval = Column(Float, nullable=True)  # Confidence interval percentage
    sample_size = Column(Integer, nullable=True)  # Number of samples used
    calculation_method = Column(String(100), nullable=False)  # Method used to calculate baseline
    is_active = Column(Boolean, default=True, nullable=False)  # Whether baseline is active
    valid_from = Column(DateTime, nullable=False)  # When baseline becomes valid
    valid_until = Column(DateTime, nullable=True)  # When baseline expires
    created_by = Column(String(100), nullable=False)  # Who created the baseline
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('ix_performance_baselines_baseline_name', 'baseline_name'),
        Index('ix_performance_baselines_metric_type', 'metric_type'),
        Index('ix_performance_baselines_metric_category', 'metric_category'),
        Index('ix_performance_baselines_is_active', 'is_active'),
        Index('ix_performance_baselines_valid_from', 'valid_from'),
    )


class OptimizationStrategy(Base):
    """Model for performance optimization strategies."""
    
    __tablename__ = "optimization_strategies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_name = Column(String(200), nullable=False, unique=True)  # Strategy identifier
    strategy_description = Column(Text, nullable=False)  # Strategy description
    strategy_category = Column(String(100), nullable=False)  # caching, indexing, query_optimization, etc.
    target_metrics = Column(JSONB, nullable=False)  # Metrics this strategy targets
    implementation_status = Column(String(50), default="proposed", nullable=False)  # proposed, implementing, active, inactive
    priority = Column(String(50), default="medium", nullable=False)  # low, medium, high, critical
    estimated_impact = Column(String(50), nullable=True)  # low, medium, high
    estimated_effort = Column(String(50), nullable=True)  # low, medium, high
    implementation_notes = Column(Text, nullable=True)  # Implementation notes
    performance_improvement = Column(Float, nullable=True)  # Expected performance improvement percentage
    created_by = Column(String(100), nullable=False)  # Who created the strategy
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    implementations = relationship("OptimizationImplementation", back_populates="strategy", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_optimization_strategies_strategy_name', 'strategy_name'),
        Index('ix_optimization_strategies_strategy_category', 'strategy_category'),
        Index('ix_optimization_strategies_implementation_status', 'implementation_status'),
        Index('ix_optimization_strategies_priority', 'priority'),
    )


class OptimizationImplementation(Base):
    """Model for tracking optimization strategy implementations."""
    
    __tablename__ = "optimization_implementations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey("optimization_strategies.id"), nullable=False)
    implementation_name = Column(String(200), nullable=False)  # Implementation identifier
    implementation_type = Column(String(100), nullable=False)  # code_change, configuration, infrastructure
    status = Column(String(50), default="planned", nullable=False)  # planned, in_progress, completed, failed
    start_date = Column(DateTime, nullable=True)  # When implementation started
    completion_date = Column(DateTime, nullable=True)  # When implementation completed
    implementation_notes = Column(Text, nullable=True)  # Implementation details
    rollback_plan = Column(Text, nullable=True)  # Rollback plan if needed
    performance_impact = Column(JSONB, nullable=True)  # Measured performance impact
    created_by = Column(String(100), nullable=False)  # Who created the implementation
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    strategy = relationship("OptimizationStrategy", back_populates="implementations")
    
    # Indexes
    __table_args__ = (
        Index('ix_optimization_implementations_strategy_id', 'strategy_id'),
        Index('ix_optimization_implementations_implementation_name', 'implementation_name'),
        Index('ix_optimization_implementations_status', 'status'),
        Index('ix_optimization_implementations_start_date', 'start_date'),
    )


class SystemHealth(Base):
    """Model for system health monitoring."""
    
    __tablename__ = "system_health"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    health_check_name = Column(String(200), nullable=False)  # Health check identifier
    health_check_type = Column(String(100), nullable=False)  # database, api, cache, external_service
    health_status = Column(String(50), nullable=False)  # healthy, degraded, unhealthy
    response_time = Column(Float, nullable=True)  # Response time in milliseconds
    error_count = Column(Integer, default=0, nullable=False)  # Number of errors
    last_error = Column(Text, nullable=True)  # Last error message
    last_check = Column(DateTime, nullable=False)  # When last health check was performed
    next_check = Column(DateTime, nullable=False)  # When next health check should be performed
    check_interval = Column(Integer, nullable=False)  # Check interval in seconds
    is_critical = Column(Boolean, default=False, nullable=False)  # Whether this is a critical health check
    alert_threshold = Column(Integer, default=3, nullable=False)  # Number of failures before alert
    consecutive_failures = Column(Integer, default=0, nullable=False)  # Current consecutive failures
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('ix_system_health_health_check_name', 'health_check_name'),
        Index('ix_system_health_health_check_type', 'health_check_type'),
        Index('ix_system_health_health_status', 'health_status'),
        Index('ix_system_health_last_check', 'last_check'),
        Index('ix_system_health_is_critical', 'is_critical'),
    )


class PerformanceReport(Base):
    """Model for performance reports and analytics."""
    
    __tablename__ = "performance_reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_name = Column(String(200), nullable=False)  # Report identifier
    report_type = Column(String(100), nullable=False)  # daily, weekly, monthly, custom
    report_period_start = Column(DateTime, nullable=False)  # Report period start
    report_period_end = Column(DateTime, nullable=False)  # Report period end
    report_data = Column(JSONB, nullable=False)  # Report data and metrics
    summary_metrics = Column(JSONB, nullable=True)  # Summary metrics
    recommendations = Column(JSONB, nullable=True)  # Performance recommendations
    generated_by = Column(String(100), nullable=False)  # Who generated the report
    is_automated = Column(Boolean, default=True, nullable=False)  # Whether report was auto-generated
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('ix_performance_reports_report_name', 'report_name'),
        Index('ix_performance_reports_report_type', 'report_type'),
        Index('ix_performance_reports_report_period_start', 'report_period_start'),
        Index('ix_performance_reports_report_period_end', 'report_period_end'),
    )


class CachePerformance(Base):
    """Model for cache performance monitoring."""
    
    __tablename__ = "cache_performance"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cache_name = Column(String(200), nullable=False)  # Cache identifier
    cache_type = Column(String(100), nullable=False)  # redis, memory, database, file
    hit_count = Column(Integer, default=0, nullable=False)  # Number of cache hits
    miss_count = Column(Integer, default=0, nullable=False)  # Number of cache misses
    hit_rate = Column(Float, default=0.0, nullable=False)  # Cache hit rate percentage
    total_requests = Column(Integer, default=0, nullable=False)  # Total cache requests
    avg_response_time = Column(Float, default=0.0, nullable=False)  # Average response time in ms
    memory_usage = Column(Float, nullable=True)  # Memory usage in bytes
    memory_limit = Column(Float, nullable=True)  # Memory limit in bytes
    eviction_count = Column(Integer, default=0, nullable=False)  # Number of evictions
    last_updated = Column(DateTime, nullable=False)  # When metrics were last updated
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('ix_cache_performance_cache_name', 'cache_name'),
        Index('ix_cache_performance_cache_type', 'cache_type'),
        Index('ix_cache_performance_hit_rate', 'hit_rate'),
        Index('ix_cache_performance_last_updated', 'last_updated'),
    )


class DatabasePerformance(Base):
    """Model for database performance monitoring."""
    
    __tablename__ = "database_performance"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    database_name = Column(String(200), nullable=False)  # Database identifier
    connection_count = Column(Integer, default=0, nullable=False)  # Active connections
    max_connections = Column(Integer, nullable=True)  # Maximum connections
    query_count = Column(Integer, default=0, nullable=False)  # Total queries executed
    slow_query_count = Column(Integer, default=0, nullable=False)  # Number of slow queries
    avg_query_time = Column(Float, default=0.0, nullable=False)  # Average query time in ms
    slow_query_threshold = Column(Float, default=1000.0, nullable=False)  # Slow query threshold in ms
    lock_wait_time = Column(Float, default=0.0, nullable=False)  # Total lock wait time
    deadlock_count = Column(Integer, default=0, nullable=False)  # Number of deadlocks
    buffer_hit_ratio = Column(Float, default=0.0, nullable=False)  # Buffer hit ratio percentage
    table_size = Column(Float, nullable=True)  # Total table size in bytes
    index_size = Column(Float, nullable=True)  # Total index size in bytes
    last_updated = Column(DateTime, nullable=False)  # When metrics were last updated
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('ix_database_performance_database_name', 'database_name'),
        Index('ix_database_performance_avg_query_time', 'avg_query_time'),
        Index('ix_database_performance_slow_query_count', 'slow_query_count'),
        Index('ix_database_performance_last_updated', 'last_updated'),
    )
