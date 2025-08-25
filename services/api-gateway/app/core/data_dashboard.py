"""
Core Data Dashboard Service

Business logic for enhanced dashboard functionality.
Implements FEAT-005 Data Dashboard (P2 priority).
"""

from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from uuid import UUID, uuid4
import json
import hashlib
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_, and_, desc, asc
from fastapi import HTTPException, status
from app.models.data_dashboard import (
    DashboardTemplate, UserDashboard, DashboardWidget,
    WidgetMetric, DashboardAlert, DataQuery, DashboardSnapshot,
    DashboardType, WidgetType, RefreshInterval
)
from app.models.users import User
from app.schemas.data_dashboard import (
    DashboardTemplateCreate, DashboardTemplateUpdate,
    DashboardCreate, DashboardUpdate,
    WidgetCreate, WidgetUpdate,
    AlertCreate, AlertUpdate,
    QueryCreate, QueryUpdate,
    SnapshotCreate
)
from app.core.cache import cache_service
import logging
from collections import defaultdict
import asyncio

logger = logging.getLogger(__name__)


class DashboardService:
    """Service for managing enhanced dashboards."""
    
    def __init__(self, db: Session):
        self.db = db
        self.data_providers = {}  # Registry of data providers
        
    # Template management
    def create_template(
        self,
        template_data: DashboardTemplateCreate,
        user: User
    ) -> DashboardTemplate:
        """Create dashboard template."""
        # Generate slug
        slug = self._generate_slug(template_data.name)
        
        # Check for duplicate
        existing = self.db.query(DashboardTemplate).filter(
            DashboardTemplate.slug == slug
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Template with this name already exists"
            )
        
        template = DashboardTemplate(
            **template_data.dict(),
            slug=slug
        )
        
        self.db.add(template)
        self.db.commit()
        
        logger.info(f"Created dashboard template: {template.name}")
        return template
    
    def get_templates(
        self,
        type: Optional[DashboardType] = None,
        category: Optional[str] = None,
        is_public: bool = True
    ) -> List[DashboardTemplate]:
        """Get available templates."""
        query = self.db.query(DashboardTemplate)
        
        if type:
            query = query.filter(DashboardTemplate.type == type)
        if category:
            query = query.filter(DashboardTemplate.category == category)
        query = query.filter(DashboardTemplate.is_public == is_public)
        
        return query.order_by(DashboardTemplate.name).all()
    
    # Dashboard CRUD
    def create_dashboard(
        self,
        dashboard_data: DashboardCreate,
        user: User
    ) -> UserDashboard:
        """Create user dashboard."""
        # Generate slug
        slug = self._generate_slug(dashboard_data.name)
        
        # Check for duplicate for this user
        existing = self.db.query(UserDashboard).filter(
            and_(
                UserDashboard.user_id == user.id,
                UserDashboard.slug == slug
            )
        ).first()
        
        if existing:
            # Add number suffix
            count = 1
            while existing:
                new_slug = f"{slug}-{count}"
                existing = self.db.query(UserDashboard).filter(
                    and_(
                        UserDashboard.user_id == user.id,
                        UserDashboard.slug == new_slug
                    )
                ).first()
                if not existing:
                    slug = new_slug
                    break
                count += 1
        
        # If based on template, copy configuration
        if dashboard_data.template_id:
            template = self.db.query(DashboardTemplate).filter(
                DashboardTemplate.id == dashboard_data.template_id
            ).first()
            
            if not template:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Template not found"
                )
            
            # Use template's layout if not provided
            if not dashboard_data.layout_config:
                dashboard_data.layout_config = template.layout_config
        
        dashboard = UserDashboard(
            **dashboard_data.dict(exclude={'template_id'}),
            user_id=user.id,
            slug=slug,
            template_id=dashboard_data.template_id
        )
        
        self.db.add(dashboard)
        self.db.flush()
        
        # If template provided, create widgets from template
        if dashboard_data.template_id and template:
            for widget_config in template.widget_configs:
                widget = DashboardWidget(
                    dashboard_id=dashboard.id,
                    **widget_config
                )
                self.db.add(widget)
        
        self.db.commit()
        
        logger.info(f"Created dashboard: {dashboard.name} for user {user.id}")
        return dashboard
    
    def get_dashboard(self, dashboard_id: UUID, user: User) -> UserDashboard:
        """Get dashboard by ID."""
        dashboard = self.db.query(UserDashboard).options(
            joinedload(UserDashboard.widgets),
            joinedload(UserDashboard.template)
        ).filter(UserDashboard.id == dashboard_id).first()
        
        if not dashboard:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dashboard not found"
            )
        
        # Check permissions
        if dashboard.user_id != user.id and not dashboard.is_public:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this dashboard"
            )
        
        # Update last accessed
        dashboard.last_accessed_at = datetime.utcnow()
        self.db.commit()
        
        return dashboard
    
    def update_dashboard(
        self,
        dashboard_id: UUID,
        dashboard_data: DashboardUpdate,
        user: User
    ) -> UserDashboard:
        """Update dashboard."""
        dashboard = self.get_dashboard(dashboard_id, user)
        
        # Check ownership
        if dashboard.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this dashboard"
            )
        
        for field, value in dashboard_data.dict(exclude_unset=True).items():
            setattr(dashboard, field, value)
        
        self.db.commit()
        return dashboard
    
    def delete_dashboard(self, dashboard_id: UUID, user: User) -> None:
        """Delete dashboard."""
        dashboard = self.get_dashboard(dashboard_id, user)
        
        # Check ownership
        if dashboard.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this dashboard"
            )
        
        self.db.delete(dashboard)
        self.db.commit()
        
        logger.info(f"Deleted dashboard: {dashboard_id}")
    
    def list_dashboards(
        self,
        user: User,
        type: Optional[DashboardType] = None,
        is_favorite: Optional[bool] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[UserDashboard], int]:
        """List user's dashboards."""
        query = self.db.query(UserDashboard).filter(
            UserDashboard.user_id == user.id
        )
        
        if type:
            query = query.filter(UserDashboard.type == type)
        if is_favorite is not None:
            query = query.filter(UserDashboard.is_favorite == is_favorite)
        
        total_count = query.count()
        
        # Order by favorites first, then by last accessed
        query = query.order_by(
            desc(UserDashboard.is_favorite),
            desc(UserDashboard.last_accessed_at)
        )
        
        # Pagination
        offset = (page - 1) * page_size
        dashboards = query.offset(offset).limit(page_size).all()
        
        return dashboards, total_count
    
    # Widget management
    def add_widget(
        self,
        dashboard_id: UUID,
        widget_data: WidgetCreate,
        user: User
    ) -> DashboardWidget:
        """Add widget to dashboard."""
        dashboard = self.get_dashboard(dashboard_id, user)
        
        # Check ownership
        if dashboard.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this dashboard"
            )
        
        widget = DashboardWidget(
            dashboard_id=dashboard_id,
            **widget_data.dict()
        )
        
        self.db.add(widget)
        self.db.commit()
        
        logger.info(f"Added widget to dashboard {dashboard_id}")
        return widget
    
    def update_widget(
        self,
        widget_id: UUID,
        widget_data: WidgetUpdate,
        user: User
    ) -> DashboardWidget:
        """Update widget."""
        widget = self.db.query(DashboardWidget).join(
            UserDashboard
        ).filter(
            DashboardWidget.id == widget_id
        ).first()
        
        if not widget:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Widget not found"
            )
        
        # Check ownership through dashboard
        if widget.dashboard.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this widget"
            )
        
        for field, value in widget_data.dict(exclude_unset=True).items():
            setattr(widget, field, value)
        
        self.db.commit()
        return widget
    
    def delete_widget(self, widget_id: UUID, user: User) -> None:
        """Delete widget."""
        widget = self.db.query(DashboardWidget).join(
            UserDashboard
        ).filter(
            DashboardWidget.id == widget_id
        ).first()
        
        if not widget:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Widget not found"
            )
        
        # Check ownership through dashboard
        if widget.dashboard.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this widget"
            )
        
        self.db.delete(widget)
        self.db.commit()
        
        logger.info(f"Deleted widget: {widget_id}")
    
    # Data fetching
    async def get_widget_data(
        self,
        widget: DashboardWidget,
        user: User
    ) -> Dict[str, Any]:
        """Get data for a widget."""
        # Check cache first
        cache_key = self._get_widget_cache_key(widget)
        cached_data = cache_service.get(cache_key)
        
        if cached_data:
            return {
                "widget_id": str(widget.id),
                "data": cached_data,
                "metadata": {
                    "source": widget.data_source,
                    "filters": widget.data_filters
                },
                "cached": True,
                "cache_expires_at": datetime.utcnow() + timedelta(seconds=widget.cache_duration or 300),
                "generated_at": datetime.utcnow()
            }
        
        # Fetch fresh data
        data = await self._fetch_widget_data(widget, user)
        
        # Cache if configured
        if widget.cache_duration and widget.cache_duration > 0:
            cache_service.set(
                cache_key,
                data,
                ttl=widget.cache_duration
            )
        
        # Update last refresh
        widget.last_refresh = datetime.utcnow()
        self.db.commit()
        
        return {
            "widget_id": str(widget.id),
            "data": data,
            "metadata": {
                "source": widget.data_source,
                "filters": widget.data_filters
            },
            "cached": False,
            "cache_expires_at": None,
            "generated_at": datetime.utcnow()
        }
    
    async def get_dashboard_data(
        self,
        dashboard_id: UUID,
        user: User
    ) -> Dict[str, Any]:
        """Get data for all widgets in a dashboard."""
        dashboard = self.get_dashboard(dashboard_id, user)
        
        # Fetch data for all widgets in parallel
        widget_data_tasks = [
            self.get_widget_data(widget, user)
            for widget in dashboard.widgets
        ]
        
        widget_data = await asyncio.gather(*widget_data_tasks)
        
        return {
            "dashboard_id": str(dashboard.id),
            "widgets": widget_data,
            "refresh_interval": dashboard.refresh_interval,
            "generated_at": datetime.utcnow()
        }
    
    # Alert management
    def create_alert(
        self,
        alert_data: AlertCreate,
        user: User
    ) -> DashboardAlert:
        """Create dashboard alert."""
        # Verify dashboard/widget ownership
        if alert_data.dashboard_id:
            dashboard = self.get_dashboard(alert_data.dashboard_id, user)
            if dashboard.user_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to create alerts for this dashboard"
                )
        
        alert = DashboardAlert(
            **alert_data.dict(),
            user_id=user.id
        )
        
        self.db.add(alert)
        self.db.commit()
        
        logger.info(f"Created alert: {alert.name} for user {user.id}")
        return alert
    
    def check_alerts(self) -> List[Tuple[DashboardAlert, bool]]:
        """Check all active alerts and return triggered ones."""
        # Get alerts that need checking
        now = datetime.utcnow()
        alerts_to_check = self.db.query(DashboardAlert).filter(
            and_(
                DashboardAlert.is_active == True,
                or_(
                    DashboardAlert.last_checked.is_(None),
                    DashboardAlert.last_checked < now - timedelta(minutes=1)  # Based on interval
                )
            )
        ).all()
        
        triggered_alerts = []
        
        for alert in alerts_to_check:
            # Check if alert should be checked based on interval
            if not self._should_check_alert(alert, now):
                continue
            
            # Evaluate alert condition
            triggered = self._evaluate_alert_condition(alert)
            
            # Update alert
            alert.last_checked = now
            if triggered:
                alert.last_triggered = now
                alert.trigger_count += 1
                triggered_alerts.append((alert, True))
            else:
                triggered_alerts.append((alert, False))
        
        self.db.commit()
        
        return triggered_alerts
    
    # Query management
    def create_query(
        self,
        query_data: QueryCreate,
        user: User
    ) -> DataQuery:
        """Create saved query."""
        # Check for duplicate name
        existing = self.db.query(DataQuery).filter(
            DataQuery.name == query_data.name
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Query with this name already exists"
            )
        
        query = DataQuery(
            **query_data.dict(),
            user_id=user.id
        )
        
        self.db.add(query)
        self.db.commit()
        
        logger.info(f"Created query: {query.name}")
        return query
    
    def execute_query(
        self,
        query_id: UUID,
        parameters: Optional[Dict[str, Any]] = None,
        user: Optional[User] = None
    ) -> Any:
        """Execute a saved query."""
        query = self.db.query(DataQuery).filter(
            DataQuery.id == query_id
        ).first()
        
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Query not found"
            )
        
        # Check permissions
        if not query.is_public and (not user or query.user_id != user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to execute this query"
            )
        
        # Execute based on query type
        if query.query_type == "sql":
            result = self._execute_sql_query(query, parameters)
        elif query.query_type == "api":
            result = self._execute_api_query(query, parameters)
        else:  # aggregate
            result = self._execute_aggregate_query(query, parameters)
        
        # Update execution stats
        query.last_executed = datetime.utcnow()
        query.execution_count += 1
        self.db.commit()
        
        return result
    
    # Snapshot management
    def create_snapshot(
        self,
        dashboard_id: UUID,
        snapshot_data: SnapshotCreate,
        user: User
    ) -> DashboardSnapshot:
        """Create dashboard snapshot."""
        dashboard = self.get_dashboard(dashboard_id, user)
        
        # Check ownership
        if dashboard.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create snapshot of this dashboard"
            )
        
        # Capture current state
        dashboard_state = {
            "name": dashboard.name,
            "type": dashboard.type,
            "layout_config": dashboard.layout_config,
            "theme": dashboard.theme,
            "widgets": []
        }
        
        # Capture widget configurations and data
        widget_data = {}
        for widget in dashboard.widgets:
            widget_config = {
                "id": str(widget.id),
                "type": widget.widget_type,
                "title": widget.title,
                "position": widget.position,
                "display_config": widget.display_config
            }
            dashboard_state["widgets"].append(widget_config)
            
            # Get current widget data
            widget_data[str(widget.id)] = self._fetch_widget_data_sync(widget, user)
        
        # Generate share token if public
        share_token = None
        if snapshot_data.is_public:
            share_token = self._generate_share_token()
        
        snapshot = DashboardSnapshot(
            dashboard_id=dashboard_id,
            user_id=user.id,
            name=snapshot_data.name,
            description=snapshot_data.description,
            dashboard_state=dashboard_state,
            widget_data=widget_data,
            is_public=snapshot_data.is_public,
            share_token=share_token,
            expires_at=snapshot_data.expires_at,
            tags=snapshot_data.tags
        )
        
        self.db.add(snapshot)
        self.db.commit()
        
        logger.info(f"Created snapshot for dashboard {dashboard_id}")
        return snapshot
    
    # Helper methods
    def _generate_slug(self, text: str) -> str:
        """Generate URL-safe slug from text."""
        import re
        slug = text.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[\s_-]+', '-', slug)
        slug = re.sub(r'^-+|-+$', '', slug)
        return slug
    
    def _get_widget_cache_key(self, widget: DashboardWidget) -> str:
        """Generate cache key for widget data."""
        # Include filters in cache key
        filter_hash = hashlib.md5(
            json.dumps(widget.data_filters or {}, sort_keys=True).encode()
        ).hexdigest()
        
        return f"widget_data:{widget.id}:{filter_hash}"
    
    async def _fetch_widget_data(self, widget: DashboardWidget, user: User) -> Any:
        """Fetch data for a widget from its data source."""
        # This would integrate with various data sources
        # For now, return mock data based on widget type
        
        if widget.widget_type == WidgetType.METRIC:
            return {
                "value": 12345,
                "change": 12.5,
                "trend": "up"
            }
        elif widget.widget_type == WidgetType.CHART:
            return {
                "labels": ["Jan", "Feb", "Mar", "Apr", "May"],
                "datasets": [{
                    "label": "Data",
                    "data": [10, 20, 30, 25, 35]
                }]
            }
        elif widget.widget_type == WidgetType.TABLE:
            return {
                "columns": ["Name", "Value", "Change"],
                "rows": [
                    ["Item 1", 100, "+10%"],
                    ["Item 2", 200, "-5%"],
                    ["Item 3", 150, "+15%"]
                ]
            }
        else:
            return {"data": "Sample data for " + widget.widget_type}
    
    def _fetch_widget_data_sync(self, widget: DashboardWidget, user: User) -> Any:
        """Synchronous version of fetch widget data."""
        # Simplified sync version for snapshots
        return {
            "type": widget.widget_type,
            "title": widget.title,
            "sample_data": True
        }
    
    def _should_check_alert(self, alert: DashboardAlert, now: datetime) -> bool:
        """Determine if alert should be checked based on interval."""
        if not alert.last_checked:
            return True
        
        interval_minutes = {
            RefreshInterval.MINUTE_1: 1,
            RefreshInterval.MINUTE_5: 5,
            RefreshInterval.MINUTE_15: 15,
            RefreshInterval.HOUR_1: 60,
            RefreshInterval.HOUR_6: 360,
            RefreshInterval.DAILY: 1440
        }
        
        minutes = interval_minutes.get(alert.check_interval, 15)
        return alert.last_checked < now - timedelta(minutes=minutes)
    
    def _evaluate_alert_condition(self, alert: DashboardAlert) -> bool:
        """Evaluate if alert condition is met."""
        # This would check actual data against condition
        # For now, return mock result
        return False
    
    def _execute_sql_query(
        self,
        query: DataQuery,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Execute SQL query."""
        # This would execute actual SQL with proper sandboxing
        # For now, return mock data
        return {"results": [], "row_count": 0}
    
    def _execute_api_query(
        self,
        query: DataQuery,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Execute API query."""
        # This would call internal APIs
        # For now, return mock data
        return {"data": {}}
    
    def _execute_aggregate_query(
        self,
        query: DataQuery,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Execute aggregate query."""
        # This would perform aggregations
        # For now, return mock data
        return {"aggregations": {}}
    
    def _generate_share_token(self) -> str:
        """Generate unique share token."""
        return hashlib.sha256(
            f"{uuid4()}{datetime.utcnow()}".encode()
        ).hexdigest()[:32]


# Dependency injection helper
def get_dashboard_service(db: Session) -> DashboardService:
    """Get dashboard service instance."""
    return DashboardService(db)