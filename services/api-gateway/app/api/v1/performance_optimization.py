"""
Performance Optimization API for OpenPolicy V2

Comprehensive performance optimization and system monitoring system.
Implements P2 priority feature for enhanced system performance and user experience.
"""

from fastapi import APIRouter, HTTPException, Query, Depends, Path, Body
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime, timedelta
import math

from app.database import get_db
from app.models.performance_optimization import (
    PerformanceMetric, PerformanceAlert, SystemHealth
)
from app.models.users import User
from app.schemas.performance_optimization import (
    PerformanceMetricResponse, PerformanceAlertResponse,
    PerformanceMetricListResponse, PerformanceAlertListResponse,
    PerformanceMetricCreateRequest, PerformanceAlertCreateRequest,
    HealthCheckRequest, PerformanceAnalysisRequest,
    SystemOverview, PerformanceTrend, OptimizationRecommendation,
    MetricTypeEnum, MetricCategoryEnum, AlertTypeEnum, AlertSeverityEnum,
    StrategyCategoryEnum, PriorityEnum,
    HealthStatusEnum, HealthCheckTypeEnum, ImpactLevelEnum, EffortLevelEnum
)
from app.api.v1.auth import get_current_user
import structlog

logger = structlog.get_logger(__name__)
router = APIRouter()


# ============================================================================
# PERFORMANCE METRICS MANAGEMENT
# ============================================================================

@router.post("/metrics", response_model=PerformanceMetricResponse)
async def create_performance_metric(
    metric_data: PerformanceMetricCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new performance metric.
    
    This creates a new performance metric for monitoring system performance.
    """
    # Create new metric
    metric = PerformanceMetric(**metric_data.dict())
    db.add(metric)
    db.commit()
    db.refresh(metric)
    
    # Check if alert should be triggered
    if metric.is_alert_enabled:
        await _check_and_create_alerts(db, metric)
    
    logger.info(f"Performance metric created: {current_user.username} - {metric_data.metric_name}")
    
    return PerformanceMetricResponse(
        id=str(metric.id),
        metric_name=metric.metric_name,
        metric_type=metric.metric_type,
        metric_category=metric.metric_category,
        metric_value=metric.metric_value,
        metric_unit=metric.metric_unit,
        threshold_warning=metric.threshold_warning,
        threshold_critical=metric.threshold_critical,
        is_alert_enabled=metric.is_alert_enabled,
        collection_timestamp=metric.collection_timestamp,
        source_endpoint=metric.source_endpoint,
        user_agent=metric.user_agent,
        ip_address=metric.ip_address,
        session_id=metric.session_id,
        created_at=metric.created_at
    )


@router.get("/metrics", response_model=PerformanceMetricListResponse)
async def list_performance_metrics(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    metric_type: Optional[MetricTypeEnum] = Query(None, description="Filter by metric type"),
    metric_category: Optional[MetricCategoryEnum] = Query(None, description="Filter by metric category"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    search: Optional[str] = Query(None, description="Search in metric names"),
    db: DBSession = Depends(get_db)
):
    """
    List performance metrics with filtering and pagination.
    """
    # Build base query
    query = db.query(PerformanceMetric)
    
    # Apply filters
    if metric_type:
        query = query.filter(PerformanceMetric.metric_type == metric_type)
    
    if metric_category:
        query = query.filter(PerformanceMetric.metric_category == metric_category)
    
    if start_date:
        query = query.filter(PerformanceMetric.collection_timestamp >= start_date)
    
    if end_date:
        query = query.filter(PerformanceMetric.collection_timestamp <= end_date)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(PerformanceMetric.metric_name.ilike(search_term))
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get metrics
    metrics = query.order_by(PerformanceMetric.collection_timestamp.desc()).offset(offset).limit(page_size).all()
    
    # Convert to response format
    metric_responses = []
    for metric in metrics:
        metric_responses.append(PerformanceMetricResponse(
            id=str(metric.id),
            metric_name=metric.metric_name,
            metric_type=metric.metric_type,
            metric_category=metric.metric_category,
            metric_value=metric.metric_value,
            metric_unit=metric.metric_unit,
            threshold_warning=metric.threshold_warning,
            threshold_critical=metric.threshold_critical,
            is_alert_enabled=metric.is_alert_enabled,
            collection_timestamp=metric.collection_timestamp,
            source_endpoint=metric.source_endpoint,
            user_agent=metric.user_agent,
            ip_address=metric.ip_address,
            session_id=metric.session_id,
            created_at=metric.created_at
        ))
    
    return PerformanceMetricListResponse(
        metrics=metric_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


@router.get("/metrics/{metric_id}", response_model=PerformanceMetricResponse)
async def get_performance_metric(
    metric_id: str = Path(..., description="Performance metric ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get a specific performance metric by ID.
    """
    metric = db.query(PerformanceMetric).filter(PerformanceMetric.id == metric_id).first()
    
    if not metric:
        raise HTTPException(status_code=404, detail="Performance metric not found")
    
    return PerformanceMetricResponse(
        id=str(metric.id),
        metric_name=metric.metric_name,
        metric_type=metric.metric_type,
        metric_category=metric.metric_category,
        metric_value=metric.metric_value,
        metric_unit=metric.metric_unit,
        threshold_warning=metric.threshold_warning,
        threshold_critical=metric.threshold_critical,
        is_alert_enabled=metric.is_alert_enabled,
        collection_timestamp=metric.collection_timestamp,
        source_endpoint=metric.source_endpoint,
        user_agent=metric.user_agent,
        ip_address=metric.ip_address,
        session_id=metric.session_id,
        created_at=metric.created_at
    )


# ============================================================================
# PERFORMANCE ALERTS MANAGEMENT
# ============================================================================

@router.post("/alerts", response_model=PerformanceAlertResponse)
async def create_performance_alert(
    alert_data: PerformanceAlertCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new performance alert.
    
    This creates a new performance alert for critical performance issues.
    """
    # Verify metric exists
    metric = db.query(PerformanceMetric).filter(PerformanceMetric.id == alert_data.metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Performance metric not found")
    
    # Create new alert
    alert = PerformanceAlert(**alert_data.dict())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    
    logger.info(f"Performance alert created: {current_user.username} - {alert_data.alert_message}")
    
    return PerformanceAlertResponse(
        id=str(alert.id),
        metric_id=str(alert.metric_id),
        alert_type=alert.alert_type,
        alert_message=alert.alert_message,
        alert_severity=alert.alert_severity,
        is_resolved=alert.is_resolved,
        resolved_at=alert.resolved_at,
        resolved_by=alert.resolved_by,
        resolution_notes=alert.resolution_notes,
        notification_sent=alert.notification_sent,
        notification_channels=alert.notification_channels,
        created_at=alert.created_at,
        updated_at=alert.updated_at
    )


@router.get("/alerts", response_model=PerformanceAlertListResponse)
async def list_performance_alerts(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    alert_type: Optional[AlertTypeEnum] = Query(None, description="Filter by alert type"),
    alert_severity: Optional[AlertSeverityEnum] = Query(None, description="Filter by alert severity"),
    is_resolved: Optional[bool] = Query(None, description="Filter by resolution status"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    db: DBSession = Depends(get_db)
):
    """
    List performance alerts with filtering and pagination.
    """
    # Build base query
    query = db.query(PerformanceAlert)
    
    # Apply filters
    if alert_type:
        query = query.filter(PerformanceAlert.alert_type == alert_type)
    
    if alert_severity:
        query = query.filter(PerformanceAlert.alert_severity == alert_severity)
    
    if is_resolved is not None:
        query = query.filter(PerformanceAlert.is_resolved == is_resolved)
    
    if start_date:
        query = query.filter(PerformanceAlert.created_at >= start_date)
    
    if end_date:
        query = query.filter(PerformanceAlert.created_at <= end_date)
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get alerts
    alerts = query.order_by(PerformanceAlert.created_at.desc()).offset(offset).limit(page_size).all()
    
    # Convert to response format
    alert_responses = []
    for alert in alerts:
        alert_responses.append(PerformanceAlertResponse(
            id=str(alert.id),
            metric_id=str(alert.metric_id),
            alert_type=alert.alert_type,
            alert_message=alert.alert_message,
            alert_severity=alert.alert_severity,
            is_resolved=alert.is_resolved,
            resolved_at=alert.resolved_at,
            resolved_by=alert.resolved_by,
            resolution_notes=alert.resolution_notes,
            notification_sent=alert.notification_sent,
            notification_channels=alert.notification_channels,
            created_at=alert.created_at,
            updated_at=alert.updated_at
        ))
    
    return PerformanceAlertListResponse(
        alerts=alert_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


# ============================================================================
# SYSTEM HEALTH MONITORING
# ============================================================================

@router.post("/health/check")
async def perform_health_check(
    health_data: HealthCheckRequest = Body(...),
    db: DBSession = Depends(get_db)
):
    """
    Perform a system health check.
    
    This endpoint allows external systems to report health check results.
    """
    # Get or create health check record
    health_check = db.query(SystemHealth).filter(
        SystemHealth.health_check_name == health_data.health_check_name
    ).first()
    
    if not health_check:
        # Create new health check
        health_check = SystemHealth(
            health_check_name=health_data.health_check_name,
            health_check_type=health_data.health_check_type,
            health_status=HealthStatusEnum.HEALTHY,
            last_check=datetime.utcnow(),
            next_check=datetime.utcnow() + timedelta(minutes=5),
            check_interval=300,
            is_critical=False,
            alert_threshold=3,
            consecutive_failures=0
        )
        db.add(health_check)
    else:
        # Update existing health check
        health_check.last_check = datetime.utcnow()
        health_check.next_check = datetime.utcnow() + timedelta(minutes=5)
        
        if health_data.error_message:
            health_check.health_status = HealthStatusEnum.UNHEALTHY
            health_check.error_count += 1
            health_check.last_error = health_data.error_message
            health_check.consecutive_failures += 1
        else:
            health_check.health_status = HealthStatusEnum.HEALTHY
            health_check.consecutive_failures = 0
        
        if health_data.response_time:
            health_check.response_time = health_data.response_time
    
    db.commit()
    
    logger.info(f"Health check performed: {health_data.health_check_name} - {health_check.health_status}")
    
    return {
        "message": "Health check performed successfully",
        "health_check_name": health_data.health_check_name,
        "health_status": health_check.health_status,
        "next_check": health_check.next_check,
        "performed_at": datetime.utcnow()
    }


@router.get("/health/overview")
async def get_system_health_overview(
    db: DBSession = Depends(get_db)
):
    """
    Get system health overview.
    
    This provides a comprehensive overview of system health status.
    """
    # Get health checks
    health_checks = db.query(SystemHealth).all()
    
    # Calculate overall health score
    total_checks = len(health_checks)
    healthy_checks = len([h for h in health_checks if h.health_status == HealthStatusEnum.HEALTHY])
    degraded_checks = len([h for h in health_checks if h.health_status == HealthStatusEnum.DEGRADED])
    unhealthy_checks = len([h for h in health_checks if h.health_status == HealthStatusEnum.UNHEALTHY])
    
    if total_checks > 0:
        health_score = (healthy_checks / total_checks) * 100
    else:
        health_score = 100.0
    
    # Get performance metrics summary
    recent_metrics = db.query(PerformanceMetric).filter(
        PerformanceMetric.collection_timestamp >= datetime.utcnow() - timedelta(hours=1)
    ).all()
    
    avg_response_time = 0
    error_rate = 0
    cache_hit_rate = 0
    
    if recent_metrics:
        response_times = [m.metric_value for m in recent_metrics if m.metric_type == MetricTypeEnum.RESPONSE_TIME]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
        
        total_requests = len([m for m in recent_metrics if m.metric_type == MetricTypeEnum.THROUGHPUT])
        error_requests = len([m for m in recent_metrics if m.metric_type == MetricTypeEnum.ERROR_RATE])
        if total_requests > 0:
            error_rate = (error_requests / total_requests) * 100
        
        cache_metrics = [m for m in recent_metrics if m.metric_type == MetricTypeEnum.CACHE_HIT_RATE]
        if cache_metrics:
            cache_hit_rate = sum([m.metric_value for m in cache_metrics]) / len(cache_metrics)
    
    # Get active alerts
    active_alerts = db.query(PerformanceAlert).filter(PerformanceAlert.is_resolved == False).count()
    critical_alerts = db.query(PerformanceAlert).filter(
        and_(
            PerformanceAlert.is_resolved == False,
            PerformanceAlert.alert_severity == AlertSeverityEnum.CRITICAL
        )
    ).count()
    
    overview = SystemOverview(
        total_metrics=len(recent_metrics),
        active_alerts=active_alerts,
        critical_alerts=critical_alerts,
        system_health_score=round(health_score, 2),
        avg_response_time=round(avg_response_time, 2),
        error_rate=round(error_rate, 2),
        cache_hit_rate=round(cache_hit_rate, 2),
        database_performance_score=round(health_score, 2),  # Simplified for now
        last_updated=datetime.utcnow()
    )
    
    return overview


# ============================================================================
# PERFORMANCE ANALYSIS
# ============================================================================

@router.post("/analysis")
async def analyze_performance(
    analysis_request: PerformanceAnalysisRequest = Body(...),
    db: DBSession = Depends(get_db)
):
    """
    Analyze performance metrics and generate insights.
    
    This provides comprehensive performance analysis with trends and recommendations.
    """
    # Build query for metrics
    query = db.query(PerformanceMetric).filter(
        and_(
            PerformanceMetric.collection_timestamp >= analysis_request.start_date,
            PerformanceMetric.collection_timestamp <= analysis_request.end_date
        )
    )
    
    if analysis_request.metric_type:
        query = query.filter(PerformanceMetric.metric_type == analysis_request.metric_type)
    
    if analysis_request.metric_category:
        query = query.filter(PerformanceMetric.metric_category == analysis_request.metric_category)
    
    metrics = query.order_by(PerformanceMetric.collection_timestamp).all()
    
    if not metrics:
        raise HTTPException(status_code=404, detail="No metrics found for the specified period")
    
    # Calculate trends
    trends = []
    for metric_type in set([m.metric_type for m in metrics]):
        type_metrics = [m for m in metrics if m.metric_type == metric_type]
        if len(type_metrics) >= 2:
            first_value = type_metrics[0].metric_value
            last_value = type_metrics[-1].metric_value
            
            if first_value > 0:
                change_percentage = ((last_value - first_value) / first_value) * 100
            else:
                change_percentage = 0
            
            if change_percentage > 5:
                trend_direction = "improving"
            elif change_percentage < -5:
                trend_direction = "declining"
            else:
                trend_direction = "stable"
            
            trends.append(PerformanceTrend(
                metric_name=type_metrics[0].metric_name,
                metric_type=metric_type,
                trend_direction=trend_direction,
                change_percentage=round(change_percentage, 2),
                period_start=analysis_request.start_date,
                period_end=analysis_request.end_date,
                data_points=[{"timestamp": m.collection_timestamp, "value": m.metric_value} for m in type_metrics],
                confidence_level=85.0,  # Simplified confidence calculation
                generated_at=datetime.utcnow()
            ))
    
    # Generate recommendations if requested
    recommendations = []
    if analysis_request.include_recommendations:
        recommendations = await _generate_optimization_recommendations(db, metrics, trends)
    
    return {
        "analysis_period": {
            "start_date": analysis_request.start_date,
            "end_date": analysis_request.end_date
        },
        "total_metrics_analyzed": len(metrics),
        "trends": [trend.dict() for trend in trends],
        "recommendations": [rec.dict() for rec in recommendations] if recommendations else [],
        "generated_at": datetime.utcnow()
    }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

async def _check_and_create_alerts(db: DBSession, metric: PerformanceMetric) -> None:
    """Check if metric exceeds thresholds and create alerts if needed."""
    if metric.threshold_critical and metric.metric_value >= metric.threshold_critical:
        alert = PerformanceAlert(
            metric_id=str(metric.id),
            alert_type=AlertTypeEnum.CRITICAL,
            alert_message=f"Critical threshold exceeded: {metric.metric_name} = {metric.metric_value} {metric.metric_unit}",
            alert_severity=AlertSeverityEnum.CRITICAL,
            notification_channels=["email", "slack"]
        )
        db.add(alert)
        db.commit()
    
    elif metric.threshold_warning and metric.metric_value >= metric.threshold_warning:
        alert = PerformanceAlert(
            metric_id=str(metric.id),
            alert_type=AlertTypeEnum.WARNING,
            alert_message=f"Warning threshold exceeded: {metric.metric_name} = {metric.metric_value} {metric.metric_unit}",
            alert_severity=AlertSeverityEnum.MEDIUM,
            notification_channels=["email"]
        )
        db.add(alert)
        db.commit()


async def _generate_optimization_recommendations(
    db: DBSession, 
    metrics: List[PerformanceMetric], 
    trends: List[PerformanceTrend]
) -> List[OptimizationRecommendation]:
    """Generate optimization recommendations based on metrics and trends."""
    recommendations = []
    
    # Analyze response time trends
    response_time_metrics = [m for m in metrics if m.metric_type == MetricTypeEnum.RESPONSE_TIME]
    if response_time_metrics:
        avg_response_time = sum([m.metric_value for m in response_time_metrics]) / len(response_time_metrics)
        
        if avg_response_time > 1000:  # More than 1 second
            recommendations.append(OptimizationRecommendation(
                strategy_name="Database Query Optimization",
                strategy_category=StrategyCategoryEnum.QUERY_OPTIMIZATION,
                priority=PriorityEnum.HIGH,
                estimated_impact=ImpactLevelEnum.HIGH,
                estimated_effort=EffortLevelEnum.MEDIUM,
                description="Optimize database queries to reduce response times",
                rationale=f"Average response time is {avg_response_time:.2f}ms, exceeding optimal threshold",
                target_metrics=["response_time", "database_connections"],
                expected_improvement=30.0,
                implementation_steps=[
                    "Review slow query logs",
                    "Add database indexes",
                    "Optimize query patterns",
                    "Implement connection pooling"
                ],
                created_at=datetime.utcnow()
            ))
    
    # Analyze cache performance
    cache_metrics = [m for m in metrics if m.metric_type == MetricTypeEnum.CACHE_HIT_RATE]
    if cache_metrics:
        avg_cache_hit_rate = sum([m.metric_value for m in cache_metrics]) / len(cache_metrics)
        
        if avg_cache_hit_rate < 80:  # Less than 80% hit rate
            recommendations.append(OptimizationRecommendation(
                strategy_name="Cache Strategy Optimization",
                strategy_category=StrategyCategoryEnum.CACHING,
                priority=PriorityEnum.MEDIUM,
                estimated_impact=ImpactLevelEnum.MEDIUM,
                estimated_effort=EffortLevelEnum.LOW,
                description="Improve cache hit rates through better caching strategies",
                rationale=f"Cache hit rate is {avg_cache_hit_rate:.2f}%, below optimal threshold",
                target_metrics=["cache_hit_rate", "response_time"],
                expected_improvement=20.0,
                implementation_steps=[
                    "Review cache key strategies",
                    "Implement cache warming",
                    "Optimize cache expiration",
                    "Add cache monitoring"
                ],
                created_at=datetime.utcnow()
            ))
    
    return recommendations
