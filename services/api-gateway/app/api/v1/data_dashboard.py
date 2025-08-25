"""
Data Dashboard API endpoints.

Implements FEAT-005 Data Dashboard (P2 priority).
Provides comprehensive dashboard and analytics functionality.
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.core.dependencies import get_current_user, require_permission
from app.core.data_dashboard import DashboardService, get_dashboard_service
from app.models.users import User
from app.schemas.data_dashboard import (
    DashboardTemplateCreate, DashboardTemplateUpdate, DashboardTemplateResponse,
    DashboardCreate, DashboardUpdate, DashboardResponse, DashboardListResponse,
    WidgetCreate, WidgetUpdate, WidgetResponse,
    AlertCreate, AlertUpdate, AlertResponse,
    QueryCreate, QueryUpdate, QueryResponse,
    SnapshotCreate, SnapshotResponse,
    WidgetDataResponse, DashboardDataResponse,
    DashboardAnalytics, DashboardType, RefreshInterval
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# Template endpoints
@router.post("/templates", response_model=DashboardTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_dashboard_template(
    template_data: DashboardTemplateCreate,
    current_user: User = Depends(require_permission("dashboards", "write")),
    db: Session = Depends(get_db)
):
    """Create a new dashboard template (admin only)."""
    service = get_dashboard_service(db)
    template = service.create_template(template_data, current_user)
    
    response = DashboardTemplateResponse.from_orm(template)
    response.usage_count = len(template.dashboards)
    
    return response


@router.get("/templates", response_model=List[DashboardTemplateResponse])
async def list_dashboard_templates(
    type: Optional[DashboardType] = Query(None),
    category: Optional[str] = Query(None),
    is_public: bool = Query(True),
    db: Session = Depends(get_db)
):
    """List available dashboard templates."""
    service = get_dashboard_service(db)
    templates = service.get_templates(type=type, category=category, is_public=is_public)
    
    responses = []
    for template in templates:
        response = DashboardTemplateResponse.from_orm(template)
        response.usage_count = len(template.dashboards)
        responses.append(response)
    
    return responses


@router.get("/templates/{template_id}", response_model=DashboardTemplateResponse)
async def get_dashboard_template(
    template_id: UUID,
    db: Session = Depends(get_db)
):
    """Get dashboard template details."""
    from app.models.data_dashboard import DashboardTemplate
    
    template = db.query(DashboardTemplate).filter(
        DashboardTemplate.id == template_id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    response = DashboardTemplateResponse.from_orm(template)
    response.usage_count = len(template.dashboards)
    
    return response


# Dashboard endpoints
@router.post("/", response_model=DashboardResponse, status_code=status.HTTP_201_CREATED)
async def create_dashboard(
    dashboard_data: DashboardCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new dashboard."""
    service = get_dashboard_service(db)
    dashboard = service.create_dashboard(dashboard_data, current_user)
    
    response = DashboardResponse.from_orm(dashboard)
    response.widget_count = len(dashboard.widgets)
    
    return response


@router.get("/", response_model=DashboardListResponse)
async def list_dashboards(
    type: Optional[DashboardType] = Query(None),
    is_favorite: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's dashboards."""
    service = get_dashboard_service(db)
    dashboards, total_count = service.list_dashboards(
        current_user,
        type=type,
        is_favorite=is_favorite,
        page=page,
        page_size=page_size
    )
    
    results = []
    for dashboard in dashboards:
        response = DashboardResponse.from_orm(dashboard)
        response.widget_count = len(dashboard.widgets)
        results.append(response)
    
    return DashboardListResponse(
        results=results,
        pagination={
            "page": page,
            "page_size": page_size,
            "total": total_count,
            "total_pages": (total_count + page_size - 1) // page_size
        }
    )


@router.get("/shared/{share_token}", response_model=DashboardResponse)
async def get_shared_dashboard(
    share_token: str,
    db: Session = Depends(get_db)
):
    """Get shared dashboard by token."""
    from app.models.data_dashboard import UserDashboard
    
    dashboard = db.query(UserDashboard).filter(
        UserDashboard.share_token == share_token,
        UserDashboard.is_public == True
    ).first()
    
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shared dashboard not found"
        )
    
    # Check if share has expired
    if dashboard.share_expires_at and dashboard.share_expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Share link has expired"
        )
    
    # Update last accessed
    dashboard.last_accessed_at = datetime.utcnow()
    db.commit()
    
    response = DashboardResponse.from_orm(dashboard)
    response.widget_count = len(dashboard.widgets)
    
    return response


@router.get("/{dashboard_id}", response_model=DashboardResponse)
async def get_dashboard(
    dashboard_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard details."""
    service = get_dashboard_service(db)
    dashboard = service.get_dashboard(dashboard_id, current_user)
    
    response = DashboardResponse.from_orm(dashboard)
    response.widget_count = len(dashboard.widgets)
    
    return response


@router.put("/{dashboard_id}", response_model=DashboardResponse)
async def update_dashboard(
    dashboard_id: UUID,
    dashboard_data: DashboardUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update dashboard."""
    service = get_dashboard_service(db)
    dashboard = service.update_dashboard(dashboard_id, dashboard_data, current_user)
    
    response = DashboardResponse.from_orm(dashboard)
    response.widget_count = len(dashboard.widgets)
    
    return response


@router.delete("/{dashboard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dashboard(
    dashboard_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete dashboard."""
    service = get_dashboard_service(db)
    service.delete_dashboard(dashboard_id, current_user)


@router.post("/{dashboard_id}/share", response_model=Dict[str, str])
async def share_dashboard(
    dashboard_id: UUID,
    expires_in_days: Optional[int] = Query(None, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate share link for dashboard."""
    service = get_dashboard_service(db)
    dashboard = service.get_dashboard(dashboard_id, current_user)
    
    # Check ownership
    if dashboard.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to share this dashboard"
        )
    
    # Generate share token
    import hashlib
    from datetime import timedelta
    
    share_token = hashlib.sha256(
        f"{dashboard.id}{datetime.utcnow()}".encode()
    ).hexdigest()[:32]
    
    dashboard.share_token = share_token
    dashboard.is_public = True
    
    if expires_in_days:
        dashboard.share_expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
    
    db.commit()
    
    return {
        "share_token": share_token,
        "share_url": f"/dashboards/shared/{share_token}",
        "expires_at": dashboard.share_expires_at.isoformat() if dashboard.share_expires_at else None
    }


# Widget endpoints
@router.get("/{dashboard_id}/widgets", response_model=List[WidgetResponse])
async def list_dashboard_widgets(
    dashboard_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List widgets in a dashboard."""
    service = get_dashboard_service(db)
    dashboard = service.get_dashboard(dashboard_id, current_user)
    
    return [WidgetResponse.from_orm(widget) for widget in dashboard.widgets]


@router.post("/{dashboard_id}/widgets", response_model=WidgetResponse, status_code=status.HTTP_201_CREATED)
async def add_widget_to_dashboard(
    dashboard_id: UUID,
    widget_data: WidgetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add widget to dashboard."""
    service = get_dashboard_service(db)
    widget = service.add_widget(dashboard_id, widget_data, current_user)
    
    return WidgetResponse.from_orm(widget)


@router.put("/widgets/{widget_id}", response_model=WidgetResponse)
async def update_widget(
    widget_id: UUID,
    widget_data: WidgetUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update widget."""
    service = get_dashboard_service(db)
    widget = service.update_widget(widget_id, widget_data, current_user)
    
    return WidgetResponse.from_orm(widget)


@router.delete("/widgets/{widget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_widget(
    widget_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete widget."""
    service = get_dashboard_service(db)
    service.delete_widget(widget_id, current_user)


# Data endpoints
@router.get("/{dashboard_id}/data", response_model=DashboardDataResponse)
async def get_dashboard_data(
    dashboard_id: UUID,
    refresh: bool = Query(False, description="Force refresh data"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get data for all widgets in a dashboard."""
    service = get_dashboard_service(db)
    
    # Note: In production, this would be properly async
    import asyncio
    data = asyncio.run(service.get_dashboard_data(dashboard_id, current_user))
    
    return DashboardDataResponse(**data)


@router.get("/widgets/{widget_id}/data", response_model=WidgetDataResponse)
async def get_widget_data(
    widget_id: UUID,
    refresh: bool = Query(False, description="Force refresh data"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get data for a specific widget."""
    from app.models.data_dashboard import DashboardWidget
    
    widget = db.query(DashboardWidget).filter(
        DashboardWidget.id == widget_id
    ).first()
    
    if not widget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found"
        )
    
    service = get_dashboard_service(db)
    
    # Check permissions through dashboard
    dashboard = service.get_dashboard(widget.dashboard_id, current_user)
    
    # Note: In production, this would be properly async
    import asyncio
    data = asyncio.run(service.get_widget_data(widget, current_user))
    
    return WidgetDataResponse(**data)


# Alert endpoints
@router.post("/alerts", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert_data: AlertCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create dashboard alert."""
    service = get_dashboard_service(db)
    alert = service.create_alert(alert_data, current_user)
    
    return AlertResponse.from_orm(alert)


@router.get("/alerts", response_model=List[AlertResponse])
async def list_alerts(
    dashboard_id: Optional[UUID] = Query(None),
    is_active: Optional[bool] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's alerts."""
    from app.models.data_dashboard import DashboardAlert
    
    query = db.query(DashboardAlert).filter(
        DashboardAlert.user_id == current_user.id
    )
    
    if dashboard_id:
        query = query.filter(DashboardAlert.dashboard_id == dashboard_id)
    
    if is_active is not None:
        query = query.filter(DashboardAlert.is_active == is_active)
    
    alerts = query.order_by(DashboardAlert.created_at.desc()).all()
    
    return [AlertResponse.from_orm(alert) for alert in alerts]


@router.put("/alerts/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: UUID,
    alert_data: AlertUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update alert."""
    from app.models.data_dashboard import DashboardAlert
    
    alert = db.query(DashboardAlert).filter(
        DashboardAlert.id == alert_id,
        DashboardAlert.user_id == current_user.id
    ).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    for field, value in alert_data.dict(exclude_unset=True).items():
        setattr(alert, field, value)
    
    db.commit()
    
    return AlertResponse.from_orm(alert)


@router.delete("/alerts/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete alert."""
    from app.models.data_dashboard import DashboardAlert
    
    alert = db.query(DashboardAlert).filter(
        DashboardAlert.id == alert_id,
        DashboardAlert.user_id == current_user.id
    ).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    db.delete(alert)
    db.commit()


# Query endpoints
@router.post("/queries", response_model=QueryResponse, status_code=status.HTTP_201_CREATED)
async def create_query(
    query_data: QueryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create saved query."""
    service = get_dashboard_service(db)
    query = service.create_query(query_data, current_user)
    
    return QueryResponse.from_orm(query)


@router.get("/queries", response_model=List[QueryResponse])
async def list_queries(
    query_type: Optional[str] = Query(None, regex="^(sql|api|aggregate)$"),
    is_public: Optional[bool] = Query(None),
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List available queries."""
    from app.models.data_dashboard import DataQuery
    
    query = db.query(DataQuery)
    
    if query_type:
        query = query.filter(DataQuery.query_type == query_type)
    
    # Show public queries or user's own queries
    if current_user:
        query = query.filter(
            or_(
                DataQuery.is_public == True,
                DataQuery.user_id == current_user.id
            )
        )
    else:
        query = query.filter(DataQuery.is_public == True)
    
    if is_public is not None:
        query = query.filter(DataQuery.is_public == is_public)
    
    queries = query.order_by(DataQuery.name).all()
    
    return [QueryResponse.from_orm(q) for q in queries]


@router.post("/queries/{query_id}/execute")
async def execute_query(
    query_id: UUID,
    parameters: Optional[Dict[str, Any]] = Body(None),
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute a saved query."""
    service = get_dashboard_service(db)
    result = service.execute_query(query_id, parameters, current_user)
    
    return result


# Snapshot endpoints
@router.post("/{dashboard_id}/snapshots", response_model=SnapshotResponse, status_code=status.HTTP_201_CREATED)
async def create_snapshot(
    dashboard_id: UUID,
    snapshot_data: SnapshotCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create dashboard snapshot."""
    service = get_dashboard_service(db)
    snapshot = service.create_snapshot(dashboard_id, snapshot_data, current_user)
    
    return SnapshotResponse.from_orm(snapshot)


@router.get("/snapshots/{snapshot_id}")
async def get_snapshot(
    snapshot_id: UUID,
    db: Session = Depends(get_db)
):
    """Get snapshot data."""
    from app.models.data_dashboard import DashboardSnapshot
    
    snapshot = db.query(DashboardSnapshot).filter(
        DashboardSnapshot.id == snapshot_id
    ).first()
    
    if not snapshot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Snapshot not found"
        )
    
    # Check if public or expired
    if not snapshot.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Snapshot is not public"
        )
    
    if snapshot.expires_at and snapshot.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Snapshot has expired"
        )
    
    # Update view count
    snapshot.view_count += 1
    db.commit()
    
    return {
        "snapshot": SnapshotResponse.from_orm(snapshot),
        "dashboard_state": snapshot.dashboard_state,
        "widget_data": snapshot.widget_data
    }


# Analytics endpoint
@router.get("/{dashboard_id}/analytics", response_model=DashboardAnalytics)
async def get_dashboard_analytics(
    dashboard_id: UUID,
    current_user: User = Depends(require_permission("dashboards", "read")),
    db: Session = Depends(get_db)
):
    """Get dashboard analytics (admin only)."""
    # This would calculate real analytics
    # For now, return mock data
    
    return DashboardAnalytics(
        dashboard_id=dashboard_id,
        view_count=150,
        unique_viewers=45,
        avg_session_duration=312.5,
        most_viewed_widgets=[
            {"widget_id": "mock-1", "views": 450},
            {"widget_id": "mock-2", "views": 380}
        ],
        peak_usage_times=[
            {"hour": 9, "views": 50},
            {"hour": 14, "views": 65}
        ],
        performance_metrics={
            "avg_load_time": 1.2,
            "cache_hit_rate": 0.85,
            "error_rate": 0.02
        }
    )


# Background task for checking alerts
async def check_alerts_task(db: Session):
    """Background task to check alerts."""
    service = get_dashboard_service(db)
    triggered_alerts = service.check_alerts()
    
    # Send notifications for triggered alerts
    for alert, triggered in triggered_alerts:
        if triggered:
            logger.info(f"Alert triggered: {alert.name}")
            # TODO: Send actual notifications