"""
Tests for WebSocket functionality.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.core.websocket import connection_manager, WebSocketService
from app.core.events import EventType, EventPriority, EventCategory


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


class TestWebSocketEndpoints:
    """Test suite for WebSocket endpoints."""
    
    def test_websocket_router_included(self):
        """Test that WebSocket router is included in main API."""
        from app.api.v1.api import api_router
        
        # Check that WebSocket router is included
        assert any("/ws" in str(route) for route in api_router.routes), "WebSocket router not found"
    
    def test_websocket_schemas_import(self):
        """Test that WebSocket schemas can be imported."""
        from app.core.events import (
            EventType, EventPriority, EventCategory, BaseEvent
        )
        assert EventType is not None
        assert EventPriority is not None
        assert EventCategory is not None
        assert BaseEvent is not None
    
    def test_websocket_service_import(self):
        """Test that WebSocket service can be imported."""
        from app.core.websocket import WebSocketService, connection_manager
        assert WebSocketService is not None
        assert connection_manager is not None
    
    def test_redis_service_import(self):
        """Test that Redis service can be imported."""
        from app.core.redis_service import RedisService, redis_service
        assert RedisService is not None
        assert redis_service is not None
    
    def test_websocket_status_endpoint(self, client):
        """Test WebSocket status endpoint."""
        # Mock the connection manager and Redis service
        with patch('app.api.v1.websocket.connection_manager') as mock_cm, \
             patch('app.api.v1.websocket.redis_service') as mock_redis:
            
            # Mock the stats and Redis info
            mock_cm.get_stats.return_value = {
                "total_connections": 0,
                "total_rooms": 0,
                "room_stats": {},
                "active_connections": []
            }
            
            # Mock the async Redis method
            async def mock_get_redis_info():
                return {"error": "Redis not connected"}
            
            mock_redis.get_redis_info = mock_get_redis_info
            
            response = client.get("/api/v1/ws/status")
            assert response.status_code == 200
            
            data = response.json()
            assert "status" in data
            assert "websocket_stats" in data
            assert "redis_info" in data
            assert "timestamp" in data
    
    def test_websocket_connection_info_endpoint(self, client):
        """Test WebSocket connection info endpoint."""
        with patch('app.api.v1.websocket.connection_manager') as mock_cm:
            # Mock connection not found
            mock_cm.get_connection_info.return_value = None
            
            response = client.get("/api/v1/ws/connections/nonexistent")
            assert response.status_code == 404
            assert "Connection not found" in response.json()["detail"]
    
    def test_websocket_room_info_endpoint(self, client):
        """Test WebSocket room info endpoint."""
        with patch('app.api.v1.websocket.connection_manager') as mock_cm:
            # Mock room info
            mock_cm.get_room_info.return_value = {
                "room": "test_room",
                "connection_count": 0,
                "connections": []
            }
            
            response = client.get("/api/v1/ws/rooms/test_room")
            assert response.status_code == 200
            
            data = response.json()
            assert "room" in data
            assert "connection_count" in data
            assert "connections" in data
    
    def test_broadcast_message_endpoint(self, client):
        """Test broadcast message endpoint."""
        with patch('app.api.v1.websocket.connection_manager') as mock_cm, \
             patch('app.api.v1.websocket.publish_event') as mock_publish:
            
            # Mock the async broadcast methods
            async def mock_broadcast_to_room(*args, **kwargs):
                return None
            
            async def mock_broadcast_to_all(*args, **kwargs):
                return None
            
            mock_cm.broadcast_to_room = mock_broadcast_to_room
            mock_cm.broadcast_to_all = mock_broadcast_to_all
            
            # Mock the async publish method
            async def mock_publish(*args, **kwargs):
                return 1
            
            mock_publish = mock_publish
            
            # Test broadcasting to a room
            message_data = {
                "type": "notification",
                "message": "Test broadcast message",
                "priority": "normal",
                "room": "test_room"
            }
            
            response = client.post("/api/v1/ws/broadcast", json=message_data)
            assert response.status_code == 200
            
            data = response.json()
            assert "status" in data
            assert data["status"] == "success"
    
    def test_send_notification_endpoint(self, client):
        """Test send notification endpoint."""
        with patch('app.api.v1.websocket.WebSocketService') as mock_service:
            # Mock the async send_notification method
            async def mock_send_notification(*args, **kwargs):
                return None
            
            mock_service.send_notification = mock_send_notification
            
            notification_data = {
                "message": "Test notification",
                "priority": "normal"
            }
            
            response = client.post("/api/v1/ws/notify/test_connection", json=notification_data)
            assert response.status_code == 200
            
            data = response.json()
            assert "status" in data
            assert data["status"] == "success"


class TestWebSocketService:
    """Test suite for WebSocket service functionality."""
    
    def test_connection_manager_initialization(self):
        """Test that connection manager is properly initialized."""
        assert connection_manager is not None
        assert hasattr(connection_manager, 'active_connections')
        assert hasattr(connection_manager, 'connection_rooms')
        assert hasattr(connection_manager, 'room_connections')
    
    def test_websocket_service_methods(self):
        """Test that WebSocket service has required methods."""
        assert hasattr(WebSocketService, 'broadcast_vote_update')
        assert hasattr(WebSocketService, 'broadcast_bill_status_change')
        assert hasattr(WebSocketService, 'broadcast_debate_statement')
        assert hasattr(WebSocketService, 'broadcast_committee_meeting_update')
        assert hasattr(WebSocketService, 'send_notification')
        assert hasattr(WebSocketService, 'broadcast_notification')


class TestEventSystem:
    """Test suite for event system."""
    
    def test_event_types(self):
        """Test that all event types are defined."""
        expected_types = [
            "vote_update", "bill_status_change", "bill_amendment",
            "debate_statement", "committee_meeting_update",
            "notification", "presence_update", "heartbeat"
        ]
        
        for event_type in expected_types:
            assert hasattr(EventType, event_type.upper())
    
    def test_event_priorities(self):
        """Test that all event priorities are defined."""
        expected_priorities = ["low", "normal", "high", "critical"]
        
        for priority in expected_priorities:
            assert hasattr(EventPriority, priority.upper())
    
    def test_event_categories(self):
        """Test that all event categories are defined."""
        expected_categories = [
            "parliamentary", "debate", "committee", "member",
            "system", "user"
        ]
        
        for category in expected_categories:
            assert hasattr(EventCategory, category.upper())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
