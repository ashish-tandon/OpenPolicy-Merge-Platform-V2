"""
Performance Optimization Schemas for OpenPolicy V2

Comprehensive Pydantic schemas for performance optimization and system monitoring.
Implements P2 priority feature for enhanced system performance and user experience.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class MetricTypeEnum(str, Enum):
    """Metric type enumeration."""
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    DISK_USAGE = "disk_usage"
    NETWORK_LATENCY = "network_latency"
    CACHE_HIT_RATE = "cache_hit_rate"
    DATABASE_CONNECTIONS = "database_connections"
    SLOW_QUERIES = "slow_queries"


class MetricCategoryEnum(str, Enum):
    """Metric category enumeration."""
    API = "api"
    DATABASE = "database"
    CACHE = "cache"
    EXTERNAL = "external"
    INFRASTRUCTURE = "infrastructure"
    APPLICATION = "application"
    SECURITY = "security"


class AlertTypeEnum(str, Enum):
    """Alert type enumeration."""
    WARNING = "warning"
    CRITICAL = "critical"
    INFO = "info"
    SUCCESS = "success"


class AlertSeverityEnum(str, Enum):
    """Alert severity enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class StrategyCategoryEnum(str, Enum):
    """Strategy category enumeration."""
    CACHING = "caching"
    INDEXING = "indexing"
    QUERY_OPTIMIZATION = "query_optimization"
    CONNECTION_POOLING = "connection_pooling"
    LOAD_BALANCING = "load_balancing"
    COMPRESSION = "compression"
    CDN = "cdn"
    DATABASE_OPTIMIZATION = "database_optimization"
    CODE_OPTIMIZATION = "code_optimization"
    INFRASTRUCTURE = "infrastructure"


class ImplementationStatusEnum(str, Enum):
    """Implementation status enumeration."""
    PROPOSED = "proposed"
    PLANNING = "planning"
    IMPLEMENTING = "implementing"
    TESTING = "testing"
    ACTIVE = "active"
    INACTIVE = "inactive"
    FAILED = "failed"


class PriorityEnum(str, Enum):
    """Priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ImpactLevelEnum(str, Enum):
    """Impact level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class EffortLevelEnum(str, Enum):
    """Effort level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class HealthStatusEnum(str, Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class HealthCheckTypeEnum(str, Enum):
    """Health check type enumeration."""
    DATABASE = "database"
    API = "api"
    CACHE = "cache"
    EXTERNAL_SERVICE = "external_service"
    INFRASTRUCTURE = "infrastructure"
    SECURITY = "security"


class ReportTypeEnum(str, Enum):
    """Report type enumeration."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"
    REAL_TIME = "real_time"


class CacheTypeEnum(str, Enum):
    """Cache type enumeration."""
    REDIS = "redis"
    MEMORY = "memory"
    DATABASE = "database"
    FILE = "file"
    CDN = "cdn"


# ============================================================================
# BASE MODELS
# ============================================================================

class PerformanceMetricBase(BaseModel):
    """Base model for performance metrics."""
    model_config = ConfigDict(from_attributes=True)
    
    metric_name: str = Field(..., min_length=1, max_length=200, description="Metric identifier")
    metric_type: MetricTypeEnum = Field(..., description="Type of metric")
    metric_category: MetricCategoryEnum = Field(..., description="Category of metric")
    metric_value: float = Field(..., description="Actual metric value")
    metric_unit: str = Field(..., min_length=1, max_length=50, description="Unit of measurement")
    threshold_warning: Optional[float] = Field(None, description="Warning threshold")
    threshold_critical: Optional[float] = Field(None, description="Critical threshold")
    is_alert_enabled: bool = Field(True, description="Whether alerts are enabled")
    collection_timestamp: datetime = Field(..., description="When metric was collected")
    source_endpoint: Optional[str] = Field(None, max_length=500, description="Source endpoint or service")
    user_agent: Optional[str] = Field(None, max_length=500, description="User agent information")
    ip_address: Optional[str] = Field(None, max_length=45, description="IP address of request")
    session_id: Optional[str] = Field(None, max_length=100, description="Session identifier")


class PerformanceAlertBase(BaseModel):
    """Base model for performance alerts."""
    model_config = ConfigDict(from_attributes=True)
    
    metric_id: str = Field(..., description="Performance metric ID")
    alert_type: AlertTypeEnum = Field(..., description="Type of alert")
    alert_message: str = Field(..., min_length=1, description="Alert message")
    alert_severity: AlertSeverityEnum = Field(..., description="Alert severity")
    is_resolved: bool = Field(False, description="Whether alert is resolved")
    resolved_at: Optional[datetime] = Field(None, description="When alert was resolved")
    resolved_by: Optional[str] = Field(None, max_length=100, description="Who resolved the alert")
    resolution_notes: Optional[str] = Field(None, description="Notes about resolution")
    notification_sent: bool = Field(False, description="Whether notification was sent")
    notification_channels: Optional[List[str]] = Field(None, description="Channels where notification was sent")


class PerformanceBaselineBase(BaseModel):
    """Base model for performance baselines."""
    model_config = ConfigDict(from_attributes=True)
    
    baseline_name: str = Field(..., min_length=1, max_length=200, description="Baseline identifier")
    metric_type: MetricTypeEnum = Field(..., description="Type of metric this baseline applies to")
    metric_category: MetricCategoryEnum = Field(..., description="Category of metric")
    baseline_value: float = Field(..., description="Baseline value")
    baseline_unit: str = Field(..., min_length=1, max_length=50, description="Unit of measurement")
    confidence_interval: Optional[float] = Field(None, description="Confidence interval percentage")
    sample_size: Optional[int] = Field(None, ge=1, description="Number of samples used")
    calculation_method: str = Field(..., min_length=1, max_length=100, description="Method used to calculate baseline")
    is_active: bool = Field(True, description="Whether baseline is active")
    valid_from: datetime = Field(..., description="When baseline becomes valid")
    valid_until: Optional[datetime] = Field(None, description="When baseline expires")
    created_by: str = Field(..., min_length=1, max_length=100, description="Who created the baseline")


class OptimizationStrategyBase(BaseModel):
    """Base model for optimization strategies."""
    model_config = ConfigDict(from_attributes=True)
    
    strategy_name: str = Field(..., min_length=1, max_length=200, description="Strategy identifier")
    strategy_description: str = Field(..., min_length=1, description="Strategy description")
    strategy_category: StrategyCategoryEnum = Field(..., description="Strategy category")
    target_metrics: List[str] = Field(..., description="Metrics this strategy targets")
    implementation_status: ImplementationStatusEnum = Field(ImplementationStatusEnum.PROPOSED, description="Implementation status")
    priority: PriorityEnum = Field(PriorityEnum.MEDIUM, description="Strategy priority")
    estimated_impact: Optional[ImpactLevelEnum] = Field(None, description="Estimated impact level")
    estimated_effort: Optional[EffortLevelEnum] = Field(None, description="Estimated effort level")
    implementation_notes: Optional[str] = Field(None, description="Implementation notes")
    performance_improvement: Optional[float] = Field(None, ge=0.0, le=100.0, description="Expected performance improvement percentage")
    created_by: str = Field(..., min_length=1, max_length=100, description="Who created the strategy")


class OptimizationImplementationBase(BaseModel):
    """Base model for optimization implementations."""
    model_config = ConfigDict(from_attributes=True)
    
    strategy_id: str = Field(..., description="Optimization strategy ID")
    implementation_name: str = Field(..., min_length=1, max_length=200, description="Implementation identifier")
    implementation_type: str = Field(..., min_length=1, max_length=100, description="Type of implementation")
    status: str = Field("planned", min_length=1, max_length=50, description="Implementation status")
    start_date: Optional[datetime] = Field(None, description="When implementation started")
    completion_date: Optional[datetime] = Field(None, description="When implementation completed")
    implementation_notes: Optional[str] = Field(None, description="Implementation details")
    rollback_plan: Optional[str] = Field(None, description="Rollback plan if needed")
    performance_impact: Optional[Dict[str, Any]] = Field(None, description="Measured performance impact")
    created_by: str = Field(..., min_length=1, max_length=100, description="Who created the implementation")


class SystemHealthBase(BaseModel):
    """Base model for system health."""
    model_config = ConfigDict(from_attributes=True)
    
    health_check_name: str = Field(..., min_length=1, max_length=200, description="Health check identifier")
    health_check_type: HealthCheckTypeEnum = Field(..., description="Type of health check")
    health_status: HealthStatusEnum = Field(..., description="Health status")
    response_time: Optional[float] = Field(None, ge=0.0, description="Response time in milliseconds")
    error_count: int = Field(0, ge=0, description="Number of errors")
    last_error: Optional[str] = Field(None, description="Last error message")
    last_check: datetime = Field(..., description="When last health check was performed")
    next_check: datetime = Field(..., description="When next health check should be performed")
    check_interval: int = Field(..., ge=1, description="Check interval in seconds")
    is_critical: bool = Field(False, description="Whether this is a critical health check")
    alert_threshold: int = Field(3, ge=1, description="Number of failures before alert")
    consecutive_failures: int = Field(0, ge=0, description="Current consecutive failures")


class PerformanceReportBase(BaseModel):
    """Base model for performance reports."""
    model_config = ConfigDict(from_attributes=True)
    
    report_name: str = Field(..., min_length=1, max_length=200, description="Report identifier")
    report_type: ReportTypeEnum = Field(..., description="Type of report")
    report_period_start: datetime = Field(..., description="Report period start")
    report_period_end: datetime = Field(..., description="Report period end")
    report_data: Dict[str, Any] = Field(..., description="Report data and metrics")
    summary_metrics: Optional[Dict[str, Any]] = Field(None, description="Summary metrics")
    recommendations: Optional[List[str]] = Field(None, description="Performance recommendations")
    generated_by: str = Field(..., min_length=1, max_length=100, description="Who generated the report")
    is_automated: bool = Field(True, description="Whether report was auto-generated")


class CachePerformanceBase(BaseModel):
    """Base model for cache performance."""
    model_config = ConfigDict(from_attributes=True)
    
    cache_name: str = Field(..., min_length=1, max_length=200, description="Cache identifier")
    cache_type: CacheTypeEnum = Field(..., description="Type of cache")
    hit_count: int = Field(0, ge=0, description="Number of cache hits")
    miss_count: int = Field(0, ge=0, description="Number of cache misses")
    hit_rate: float = Field(0.0, ge=0.0, le=100.0, description="Cache hit rate percentage")
    total_requests: int = Field(0, ge=0, description="Total cache requests")
    avg_response_time: float = Field(0.0, ge=0.0, description="Average response time in ms")
    memory_usage: Optional[float] = Field(None, ge=0.0, description="Memory usage in bytes")
    memory_limit: Optional[float] = Field(None, ge=0.0, description="Memory limit in bytes")
    eviction_count: int = Field(0, ge=0, description="Number of evictions")
    last_updated: datetime = Field(..., description="When metrics were last updated")


class DatabasePerformanceBase(BaseModel):
    """Base model for database performance."""
    model_config = ConfigDict(from_attributes=True)
    
    database_name: str = Field(..., min_length=1, max_length=200, description="Database identifier")
    connection_count: int = Field(0, ge=0, description="Active connections")
    max_connections: Optional[int] = Field(None, ge=1, description="Maximum connections")
    query_count: int = Field(0, ge=0, description="Total queries executed")
    slow_query_count: int = Field(0, ge=0, description="Number of slow queries")
    avg_query_time: float = Field(0.0, ge=0.0, description="Average query time in ms")
    slow_query_threshold: float = Field(1000.0, ge=0.0, description="Slow query threshold in ms")
    lock_wait_time: float = Field(0.0, ge=0.0, description="Total lock wait time")
    deadlock_count: int = Field(0, ge=0, description="Number of deadlocks")
    buffer_hit_ratio: float = Field(0.0, ge=0.0, le=100.0, description="Buffer hit ratio percentage")
    table_size: Optional[float] = Field(None, ge=0.0, description="Total table size in bytes")
    index_size: Optional[float] = Field(None, ge=0.0, description="Total index size in bytes")
    last_updated: datetime = Field(..., description="When metrics were last updated")


# ============================================================================
# REQUEST MODELS
# ============================================================================

class PerformanceMetricCreateRequest(PerformanceMetricBase):
    """Request model for creating performance metrics."""
    pass


class PerformanceMetricUpdateRequest(BaseModel):
    """Request model for updating performance metrics."""
    threshold_warning: Optional[float] = None
    threshold_critical: Optional[float] = None
    is_alert_enabled: Optional[bool] = None


class PerformanceAlertCreateRequest(PerformanceAlertBase):
    """Request model for creating performance alerts."""
    pass


class PerformanceAlertUpdateRequest(BaseModel):
    """Request model for updating performance alerts."""
    is_resolved: Optional[bool] = None
    resolved_by: Optional[str] = Field(None, max_length=100)
    resolution_notes: Optional[str] = None
    notification_sent: Optional[bool] = None
    notification_channels: Optional[List[str]] = None


class PerformanceBaselineCreateRequest(PerformanceBaselineBase):
    """Request model for creating performance baselines."""
    pass


class PerformanceBaselineUpdateRequest(BaseModel):
    """Request model for updating performance baselines."""
    baseline_value: Optional[float] = None
    confidence_interval: Optional[float] = None
    sample_size: Optional[int] = Field(None, ge=1)
    calculation_method: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None
    valid_until: Optional[datetime] = None


class OptimizationStrategyCreateRequest(OptimizationStrategyBase):
    """Request model for creating optimization strategies."""
    pass


class OptimizationStrategyUpdateRequest(BaseModel):
    """Request model for updating optimization strategies."""
    strategy_description: Optional[str] = Field(None, min_length=1)
    target_metrics: Optional[List[str]] = None
    implementation_status: Optional[ImplementationStatusEnum] = None
    priority: Optional[PriorityEnum] = None
    estimated_impact: Optional[ImpactLevelEnum] = None
    estimated_effort: Optional[EffortLevelEnum] = None
    implementation_notes: Optional[str] = None
    performance_improvement: Optional[float] = Field(None, ge=0.0, le=100.0)


class OptimizationImplementationCreateRequest(OptimizationImplementationBase):
    """Request model for creating optimization implementations."""
    pass


class OptimizationImplementationUpdateRequest(BaseModel):
    """Request model for updating optimization implementations."""
    status: Optional[str] = Field(None, min_length=1, max_length=50)
    start_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    implementation_notes: Optional[str] = None
    rollback_plan: Optional[str] = None
    performance_impact: Optional[Dict[str, Any]] = None


class SystemHealthCreateRequest(SystemHealthBase):
    """Request model for creating system health checks."""
    pass


class SystemHealthUpdateRequest(BaseModel):
    """Request model for updating system health checks."""
    health_status: Optional[HealthStatusEnum] = None
    response_time: Optional[float] = Field(None, ge=0.0)
    error_count: Optional[int] = Field(None, ge=0)
    last_error: Optional[str] = None
    next_check: Optional[datetime] = None
    check_interval: Optional[int] = Field(None, ge=1)
    is_critical: Optional[bool] = None
    alert_threshold: Optional[int] = Field(None, ge=1)
    consecutive_failures: Optional[int] = Field(None, ge=0)


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class PerformanceMetricResponse(PerformanceMetricBase):
    """Response model for performance metrics."""
    id: str
    created_at: datetime


class PerformanceAlertResponse(PerformanceAlertBase):
    """Response model for performance alerts."""
    id: str
    created_at: datetime
    updated_at: datetime


class PerformanceBaselineResponse(PerformanceBaselineBase):
    """Response model for performance baselines."""
    id: str
    created_at: datetime
    updated_at: datetime


class OptimizationStrategyResponse(OptimizationStrategyBase):
    """Response model for optimization strategies."""
    id: str
    created_at: datetime
    updated_at: datetime


class OptimizationImplementationResponse(OptimizationImplementationBase):
    """Response model for optimization implementations."""
    id: str
    created_at: datetime
    updated_at: datetime


class SystemHealthResponse(SystemHealthBase):
    """Response model for system health."""
    id: str
    created_at: datetime
    updated_at: datetime


class PerformanceReportResponse(PerformanceReportBase):
    """Response model for performance reports."""
    id: str
    created_at: datetime


class CachePerformanceResponse(CachePerformanceBase):
    """Response model for cache performance."""
    id: str
    created_at: datetime


class DatabasePerformanceResponse(DatabasePerformanceBase):
    """Response model for database performance."""
    id: str
    created_at: datetime


# ============================================================================
# LIST RESPONSE MODELS
# ============================================================================

class PerformanceMetricListResponse(BaseModel):
    """List response model for performance metrics."""
    metrics: List[PerformanceMetricResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class PerformanceAlertListResponse(BaseModel):
    """List response model for performance alerts."""
    alerts: List[PerformanceAlertResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class PerformanceBaselineListResponse(BaseModel):
    """List response model for performance baselines."""
    baselines: List[PerformanceBaselineResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class OptimizationStrategyListResponse(BaseModel):
    """List response model for optimization strategies."""
    strategies: List[OptimizationStrategyResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class OptimizationImplementationListResponse(BaseModel):
    """List response model for optimization implementations."""
    implementations: List[OptimizationImplementationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class SystemHealthListResponse(BaseModel):
    """List response model for system health."""
    health_checks: List[SystemHealthResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class PerformanceReportListResponse(BaseModel):
    """List response model for performance reports."""
    reports: List[PerformanceReportResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class CachePerformanceListResponse(BaseModel):
    """List response model for cache performance."""
    cache_performance: List[CachePerformanceResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class DatabasePerformanceListResponse(BaseModel):
    """List response model for database performance."""
    database_performance: List[DatabasePerformanceResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


# ============================================================================
# SPECIALIZED MODELS
# ============================================================================

class MetricCollectionRequest(BaseModel):
    """Request model for collecting performance metrics."""
    metric_name: str = Field(..., min_length=1, max_length=200, description="Metric identifier")
    metric_type: MetricTypeEnum = Field(..., description="Type of metric")
    metric_category: MetricCategoryEnum = Field(..., description="Category of metric")
    metric_value: float = Field(..., description="Actual metric value")
    metric_unit: str = Field(..., min_length=1, max_length=50, description="Unit of measurement")
    source_endpoint: Optional[str] = Field(None, max_length=500, description="Source endpoint or service")
    user_agent: Optional[str] = Field(None, max_length=500, description="User agent information")
    ip_address: Optional[str] = Field(None, max_length=45, description="IP address of request")
    session_id: Optional[str] = Field(None, max_length=100, description="Session identifier")


class HealthCheckRequest(BaseModel):
    """Request model for health checks."""
    health_check_name: str = Field(..., min_length=1, max_length=200, description="Health check identifier")
    health_check_type: HealthCheckTypeEnum = Field(..., description="Type of health check")
    response_time: Optional[float] = Field(None, ge=0.0, description="Response time in milliseconds")
    error_message: Optional[str] = Field(None, description="Error message if health check failed")
    additional_data: Optional[Dict[str, Any]] = Field(None, description="Additional health check data")


class PerformanceAnalysisRequest(BaseModel):
    """Request model for performance analysis."""
    metric_type: Optional[MetricTypeEnum] = Field(None, description="Type of metric to analyze")
    metric_category: Optional[MetricCategoryEnum] = Field(None, description="Category of metric to analyze")
    start_date: datetime = Field(..., description="Analysis start date")
    end_date: datetime = Field(..., description="Analysis end date")
    include_baselines: bool = Field(True, description="Whether to include baseline comparisons")
    include_recommendations: bool = Field(True, description="Whether to include optimization recommendations")


class SystemOverview(BaseModel):
    """Model for system performance overview."""
    total_metrics: int = Field(..., description="Total performance metrics")
    active_alerts: int = Field(..., description="Active performance alerts")
    critical_alerts: int = Field(..., description="Critical performance alerts")
    system_health_score: float = Field(..., ge=0.0, le=100.0, description="Overall system health score")
    avg_response_time: float = Field(..., description="Average response time across all endpoints")
    error_rate: float = Field(..., ge=0.0, le=100.0, description="Overall error rate percentage")
    cache_hit_rate: float = Field(..., ge=0.0, le=100.0, description="Overall cache hit rate")
    database_performance_score: float = Field(..., ge=0.0, le=100.0, description="Database performance score")
    last_updated: datetime = Field(..., description="When overview was last updated")


class PerformanceTrend(BaseModel):
    """Model for performance trends."""
    metric_name: str = Field(..., description="Metric name")
    metric_type: MetricTypeEnum = Field(..., description="Metric type")
    trend_direction: str = Field(..., description="Trend direction (improving, declining, stable)")
    change_percentage: float = Field(..., description="Percentage change over period")
    period_start: datetime = Field(..., description="Trend period start")
    period_end: datetime = Field(..., description="Trend period end")
    data_points: List[Dict[str, Union[datetime, float]]] = Field(..., description="Trend data points")
    confidence_level: float = Field(..., ge=0.0, le=100.0, description="Trend confidence level")
    generated_at: datetime = Field(..., description="When trend was generated")


class OptimizationRecommendation(BaseModel):
    """Model for optimization recommendations."""
    strategy_name: str = Field(..., description="Strategy name")
    strategy_category: StrategyCategoryEnum = Field(..., description="Strategy category")
    priority: PriorityEnum = Field(..., description="Recommendation priority")
    estimated_impact: ImpactLevelEnum = Field(..., description="Estimated impact level")
    estimated_effort: EffortLevelEnum = Field(..., description="Estimated effort level")
    description: str = Field(..., description="Recommendation description")
    rationale: str = Field(..., description="Why this recommendation is made")
    target_metrics: List[str] = Field(..., description="Metrics this recommendation targets")
    expected_improvement: float = Field(..., ge=0.0, le=100.0, description="Expected performance improvement percentage")
    implementation_steps: List[str] = Field(..., description="Steps to implement recommendation")
    created_at: datetime = Field(..., description="When recommendation was created")
