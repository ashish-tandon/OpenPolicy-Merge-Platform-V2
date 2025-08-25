"""
Tests for enhanced data dashboard system.

Tests FEAT-005 Data Dashboard (P2 priority).
"""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy.orm import Session
from app.core.data_dashboard import DashboardService
from app.models.data_dashboard import (
    DashboardTemplate, UserDashboard, DashboardWidget,
    DashboardAlert, DataQuery, DashboardSnapshot,
    DashboardType, WidgetType, RefreshInterval
)
from app.models.users import User
from app.schemas.data_dashboard import (
    DashboardTemplateCreate, DashboardCreate, DashboardUpdate,
    WidgetCreate, WidgetUpdate, AlertCreate, QueryCreate,
    SnapshotCreate
)


class TestDashboardService:
    """Test dashboard service functionality."""
    
    @pytest.fixture
    def service(self, db_session):
        """Create service instance."""
        return DashboardService(db_session)
    
    @pytest.fixture
    def test_user(self, db_session):
        """Create test user."""
        user = User(
            email="dashboard@example.com",
            username="dashuser",
            full_name="Dashboard User",
            hashed_password="hashed"
        )
        db_session.add(user)
        db_session.commit()
        return user
    
    @pytest.fixture
    def test_template(self, db_session):
        """Create test template."""
        template = DashboardTemplate(
            name="Test Template",
            slug="test-template",
            description="Test dashboard template",
            type=DashboardType.ANALYTICS,
            layout_config={"rows": 12, "cols": 12},
            widget_configs=[
                {
                    "widget_type": "metric",
                    "title": "Test Metric",
                    "data_source": "/api/test",
                    "data_query": {},
                    "display_config": {"format": "number"},
                    "position": {"x": 0, "y": 0, "w": 3, "h": 2}
                }
            ]
        )
        db_session.add(template)
        db_session.commit()
        return template
    
    def test_create_template(self, service, test_user):
        """Test creating dashboard template."""
        template_data = DashboardTemplateCreate(
            name="Analytics Template",
            description="Template for analytics dashboards",
            type=DashboardType.ANALYTICS,
            is_public=True,
            requires_auth=False,
            layout_config={"rows": 12, "cols": 12},
            widget_configs=[],
            tags=["analytics", "performance"],
            category="analytics"
        )
        
        template = service.create_template(template_data, test_user)
        
        assert template.name == "Analytics Template"
        assert template.slug == "analytics-template"
        assert template.type == DashboardType.ANALYTICS
        assert template.tags == ["analytics", "performance"]
    
    def test_create_dashboard_from_template(self, service, test_user, test_template):
        """Test creating dashboard from template."""
        dashboard_data = DashboardCreate(
            name="My Analytics Dashboard",
            type=DashboardType.ANALYTICS,
            template_id=test_template.id,
            layout_config=None,  # Should use template's layout
            is_favorite=True
        )
        
        dashboard = service.create_dashboard(dashboard_data, test_user)
        
        assert dashboard.name == "My Analytics Dashboard"
        assert dashboard.slug == "my-analytics-dashboard"
        assert dashboard.template_id == test_template.id
        assert dashboard.is_favorite is True
        assert len(dashboard.widgets) == 1  # Widget from template
        assert dashboard.widgets[0].title == "Test Metric"
    
    def test_create_custom_dashboard(self, service, test_user):
        """Test creating custom dashboard without template."""
        dashboard_data = DashboardCreate(
            name="Custom Dashboard",
            description="My custom dashboard",
            type=DashboardType.CUSTOM,
            layout_config={"rows": 10, "cols": 10},
            theme={"primaryColor": "#007bff"},
            refresh_interval=RefreshInterval.MINUTE_1
        )
        
        dashboard = service.create_dashboard(dashboard_data, test_user)
        
        assert dashboard.name == "Custom Dashboard"
        assert dashboard.type == DashboardType.CUSTOM
        assert dashboard.theme["primaryColor"] == "#007bff"
        assert dashboard.refresh_interval == RefreshInterval.MINUTE_1
    
    def test_list_dashboards(self, service, test_user):
        """Test listing user's dashboards."""
        # Create multiple dashboards
        for i in range(3):
            dashboard_data = DashboardCreate(
                name=f"Dashboard {i}",
                type=DashboardType.OVERVIEW,
                layout_config={},
                is_favorite=(i == 0)
            )
            service.create_dashboard(dashboard_data, test_user)
        
        # List all dashboards
        dashboards, total = service.list_dashboards(test_user)
        assert total == 3
        assert dashboards[0].is_favorite is True  # Favorites first
        
        # Filter by favorite
        dashboards, total = service.list_dashboards(test_user, is_favorite=True)
        assert total == 1
    
    def test_add_widget_to_dashboard(self, service, test_user):
        """Test adding widget to dashboard."""
        # Create dashboard
        dashboard_data = DashboardCreate(
            name="Widget Test Dashboard",
            type=DashboardType.ANALYTICS,
            layout_config={"rows": 12, "cols": 12}
        )
        dashboard = service.create_dashboard(dashboard_data, test_user)
        
        # Add widget
        widget_data = WidgetCreate(
            widget_type=WidgetType.CHART,
            title="Revenue Chart",
            subtitle="Monthly revenue trends",
            data_source="/api/v1/revenue/monthly",
            data_query={"year": 2024},
            display_config={"chartType": "line", "color": "blue"},
            position={"x": 0, "y": 0, "w": 6, "h": 4},
            cache_duration=300
        )
        
        widget = service.add_widget(dashboard.id, widget_data, test_user)
        
        assert widget.title == "Revenue Chart"
        assert widget.widget_type == WidgetType.CHART
        assert widget.cache_duration == 300
        assert widget.dashboard_id == dashboard.id
    
    def test_update_widget(self, service, test_user):
        """Test updating widget."""
        # Create dashboard with widget
        dashboard_data = DashboardCreate(
            name="Update Widget Test",
            type=DashboardType.ANALYTICS,
            layout_config={}
        )
        dashboard = service.create_dashboard(dashboard_data, test_user)
        
        widget_data = WidgetCreate(
            widget_type=WidgetType.METRIC,
            title="Original Title",
            data_source="/api/test",
            data_query={},
            display_config={},
            position={"x": 0, "y": 0, "w": 3, "h": 2}
        )
        widget = service.add_widget(dashboard.id, widget_data, test_user)
        
        # Update widget
        update_data = WidgetUpdate(
            title="Updated Title",
            position={"x": 3, "y": 0, "w": 3, "h": 2}
        )
        
        updated_widget = service.update_widget(widget.id, update_data, test_user)
        
        assert updated_widget.title == "Updated Title"
        assert updated_widget.position["x"] == 3
    
    def test_create_alert(self, service, test_user):
        """Test creating dashboard alert."""
        # Create dashboard
        dashboard_data = DashboardCreate(
            name="Alert Test Dashboard",
            type=DashboardType.PERFORMANCE,
            layout_config={}
        )
        dashboard = service.create_dashboard(dashboard_data, test_user)
        
        # Create alert
        alert_data = AlertCreate(
            name="High Response Time Alert",
            description="Alert when API response time is high",
            condition={
                "metric_key": "response_time_p95",
                "operator": "gt",
                "threshold": 1000
            },
            notification_channels=["email", "in_app"],
            dashboard_id=dashboard.id,
            check_interval=RefreshInterval.MINUTE_5
        )
        
        alert = service.create_alert(alert_data, test_user)
        
        assert alert.name == "High Response Time Alert"
        assert alert.condition["threshold"] == 1000
        assert "email" in alert.notification_channels
        assert alert.is_active is True
    
    def test_create_query(self, service, test_user):
        """Test creating saved query."""
        query_data = QueryCreate(
            name="Active Bills Query",
            description="Get all active bills",
            query_type="api",
            query_config={
                "endpoint": "/api/v1/bills",
                "params": {"status": "active"}
            },
            is_public=True,
            timeout_seconds=30
        )
        
        query = service.create_query(query_data, test_user)
        
        assert query.name == "Active Bills Query"
        assert query.query_type == "api"
        assert query.is_public is True
        assert query.user_id == test_user.id
    
    def test_create_snapshot(self, service, test_user):
        """Test creating dashboard snapshot."""
        # Create dashboard with widget
        dashboard_data = DashboardCreate(
            name="Snapshot Test Dashboard",
            type=DashboardType.OVERVIEW,
            layout_config={"rows": 12, "cols": 12}
        )
        dashboard = service.create_dashboard(dashboard_data, test_user)
        
        # Add widget
        widget_data = WidgetCreate(
            widget_type=WidgetType.METRIC,
            title="Test Metric",
            data_source="/api/test",
            data_query={},
            display_config={},
            position={"x": 0, "y": 0, "w": 3, "h": 2}
        )
        service.add_widget(dashboard.id, widget_data, test_user)
        
        # Create snapshot
        snapshot_data = SnapshotCreate(
            name="Q4 2024 Snapshot",
            description="End of Q4 dashboard state",
            is_public=True,
            expires_at=datetime.utcnow() + timedelta(days=30),
            tags=["quarterly", "2024"]
        )
        
        snapshot = service.create_snapshot(dashboard.id, snapshot_data, test_user)
        
        assert snapshot.name == "Q4 2024 Snapshot"
        assert snapshot.is_public is True
        assert snapshot.share_token is not None
        assert len(snapshot.dashboard_state["widgets"]) == 1
    
    @pytest.mark.asyncio
    async def test_get_widget_data(self, service, test_user):
        """Test fetching widget data."""
        # Create widget
        widget = DashboardWidget(
            id=uuid4(),
            dashboard_id=uuid4(),
            widget_type=WidgetType.METRIC,
            title="Test Metric",
            data_source="/api/test",
            data_query={"metric": "total_users"},
            display_config={"format": "number"},
            position={"x": 0, "y": 0, "w": 3, "h": 2},
            cache_duration=60
        )
        
        # Get data
        data = await service.get_widget_data(widget, test_user)
        
        assert data["widget_id"] == str(widget.id)
        assert "data" in data
        assert "metadata" in data
        assert data["cached"] is False  # First fetch
    
    def test_dashboard_sharing(self, service, test_user):
        """Test dashboard sharing functionality."""
        # Create dashboard
        dashboard_data = DashboardCreate(
            name="Shareable Dashboard",
            type=DashboardType.ANALYTICS,
            layout_config={}
        )
        dashboard = service.create_dashboard(dashboard_data, test_user)
        
        # Initially not public
        assert dashboard.is_public is False
        assert dashboard.share_token is None
        
        # Make it shareable
        dashboard.is_public = True
        dashboard.share_token = service._generate_share_token()
        dashboard.share_expires_at = datetime.utcnow() + timedelta(days=7)
        
        assert dashboard.share_token is not None
        assert len(dashboard.share_token) == 32


class TestDashboardEndpoints:
    """Test dashboard API endpoints."""
    
    def test_create_dashboard(self, client, auth_headers):
        """Test creating dashboard via API."""
        response = client.post(
            "/api/v1/data-dashboard/",
            json={
                "name": "My Dashboard",
                "type": "analytics",
                "layout_config": {"rows": 12, "cols": 12},
                "refresh_interval": "5m"
            },
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "My Dashboard"
        assert data["slug"] == "my-dashboard"
    
    def test_list_templates(self, client):
        """Test listing dashboard templates."""
        response = client.get("/api/v1/data-dashboard/templates")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_add_widget(self, client, auth_headers, db_session):
        """Test adding widget to dashboard."""
        # Create dashboard first
        user = db_session.query(User).filter(User.email == "test@example.com").first()
        dashboard = UserDashboard(
            user_id=user.id,
            name="Test Dashboard",
            slug="test-dashboard",
            type=DashboardType.ANALYTICS,
            layout_config={}
        )
        db_session.add(dashboard)
        db_session.commit()
        
        # Add widget
        response = client.post(
            f"/api/v1/data-dashboard/{dashboard.id}/widgets",
            json={
                "widget_type": "chart",
                "title": "Test Chart",
                "data_source": "/api/v1/test",
                "data_query": {},
                "display_config": {"chartType": "bar"},
                "position": {"x": 0, "y": 0, "w": 6, "h": 4}
            },
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Chart"
    
    def test_dashboard_analytics(self, client, auth_headers, admin_headers, db_session):
        """Test getting dashboard analytics."""
        # Create dashboard
        user = db_session.query(User).filter(User.email == "test@example.com").first()
        dashboard = UserDashboard(
            id=uuid4(),
            user_id=user.id,
            name="Analytics Test",
            slug="analytics-test",
            type=DashboardType.ANALYTICS,
            layout_config={}
        )
        db_session.add(dashboard)
        db_session.commit()
        
        # Get analytics (requires admin permissions)
        response = client.get(
            f"/api/v1/data-dashboard/{dashboard.id}/analytics",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "view_count" in data
        assert "unique_viewers" in data
        assert "performance_metrics" in data