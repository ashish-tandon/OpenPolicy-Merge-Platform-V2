"""
WebSocket service for real-time parliamentary data updates.

This module provides WebSocket functionality for live updates including:
- Vote results
- Debate statements
- Bill status changes
- Committee meeting updates
- Real-time notifications
"""

import logging
from typing import Dict, List, Optional, Set, Any
from datetime import datetime
from enum import Enum
from fastapi import WebSocket
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    """Types of real-time events that can be broadcast."""
    VOTE_UPDATE = "vote_update"
    BILL_STATUS_CHANGE = "bill_status_change"
    DEBATE_STATEMENT = "debate_statement"
    COMMITTEE_MEETING_UPDATE = "committee_meeting_update"
    NOTIFICATION = "notification"
    PRESENCE_UPDATE = "presence_update"
    HEARTBEAT = "heartbeat"


class EventPriority(str, Enum):
    """Priority levels for events."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class WebSocketEvent(BaseModel):
    """Base model for WebSocket events."""
    type: EventType
    priority: EventPriority = EventPriority.NORMAL
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = Field(default_factory=dict)
    source: Optional[str] = None
    target_rooms: Optional[List[str]] = None


class ConnectionManager:
    """Manages WebSocket connections and broadcasting."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.connection_rooms: Dict[str, Set[str]] = {}  # connection_id -> set of room names
        self.room_connections: Dict[str, Set[str]] = {}  # room_name -> set of connection_ids
        self.connection_metadata: Dict[str, Dict[str, Any]] = {}  # connection_id -> metadata
        self.connection_heartbeats: Dict[str, datetime] = {}  # connection_id -> last heartbeat
        self.connection_status: Dict[str, str] = {}  # connection_id -> status (connected, idle, disconnected)
        self.max_idle_time = 300  # 5 minutes in seconds
        
    async def connect(self, websocket: WebSocket, connection_id: str, metadata: Optional[Dict[str, Any]] = None):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        self.connection_rooms[connection_id] = set()
        self.connection_metadata[connection_id] = metadata or {}
        
        # Initialize connection status and heartbeat
        self.connection_status[connection_id] = "connected"
        self.connection_heartbeats[connection_id] = datetime.utcnow()
        
        # Send connection confirmation
        await self.send_personal_message(
            connection_id,
            WebSocketEvent(
                type=EventType.NOTIFICATION,
                data={"message": "Connected to parliamentary real-time service", "connection_id": connection_id}
            )
        )
        
        logger.info(f"WebSocket connected: {connection_id}")
    
    def disconnect(self, connection_id: str):
        """Remove a WebSocket connection."""
        if connection_id in self.active_connections:
            # Remove from all rooms
            if connection_id in self.connection_rooms:
                for room in self.connection_rooms[connection_id]:
                    if room in self.room_connections:
                        self.room_connections[room].discard(connection_id)
                        if not self.room_connections[room]:
                            del self.room_connections[room]
                del self.connection_rooms[connection_id]
            
                    # Clean up connection data
        del self.active_connections[connection_id]
        if connection_id in self.connection_metadata:
            del self.connection_metadata[connection_id]
        if connection_id in self.connection_heartbeats:
            del self.connection_heartbeats[connection_id]
        if connection_id in self.connection_status:
            del self.connection_status[connection_id]
        
        logger.info(f"WebSocket disconnected: {connection_id}")
    
    async def send_personal_message(self, connection_id: str, event: WebSocketEvent):
        """Send a message to a specific connection."""
        if connection_id in self.active_connections:
            try:
                await self.active_connections[connection_id].send_text(event.json())
            except Exception as e:
                logger.error(f"Error sending message to {connection_id}: {e}")
                self.disconnect(connection_id)
    
    async def broadcast_to_room(self, room: str, event: WebSocketEvent):
        """Broadcast an event to all connections in a specific room."""
        if room in self.room_connections:
            disconnected = []
            for connection_id in self.room_connections[room]:
                try:
                    await self.active_connections[connection_id].send_text(event.json())
                except Exception as e:
                    logger.error(f"Error broadcasting to {connection_id} in room {room}: {e}")
                    disconnected.append(connection_id)
            
            # Clean up disconnected connections
            for connection_id in disconnected:
                self.disconnect(connection_id)
    
    async def broadcast_to_all(self, event: WebSocketEvent):
        """Broadcast an event to all active connections."""
        disconnected = []
        for connection_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(event.json())
            except Exception as e:
                logger.error(f"Error broadcasting to {connection_id}: {e}")
                disconnected.append(connection_id)
        
        # Clean up disconnected connections
        for connection_id in disconnected:
            self.disconnect(connection_id)
    
    def join_room(self, connection_id: str, room: str):
        """Add a connection to a room."""
        if connection_id not in self.active_connections:
            return False
        
        # Initialize room if it doesn't exist
        if room not in self.room_connections:
            self.room_connections[room] = set()
        
        # Add connection to room
        self.room_connections[room].add(connection_id)
        self.connection_rooms[connection_id].add(room)
        
        logger.info(f"Connection {connection_id} joined room: {room}")
        return True
    
    def leave_room(self, connection_id: str, room: str):
        """Remove a connection from a room."""
        if connection_id in self.connection_rooms and room in self.connection_rooms[connection_id]:
            self.connection_rooms[connection_id].discard(room)
            
        if room in self.room_connections and connection_id in self.room_connections[room]:
            self.room_connections[room].discard(connection_id)
            if not self.room_connections[room]:
                del self.room_connections[room]
        
        logger.info(f"Connection {connection_id} left room: {room}")
    
    def get_connection_info(self, connection_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific connection."""
        if connection_id in self.active_connections:
            return {
                "connection_id": connection_id,
                "rooms": list(self.connection_rooms.get(connection_id, [])),
                "metadata": self.connection_metadata.get(connection_id, {}),
                "connected_at": self.connection_metadata.get(connection_id, {}).get("connected_at")
            }
        return None
    
    def get_room_info(self, room: str) -> Dict[str, Any]:
        """Get information about a specific room."""
        connections = self.room_connections.get(room, set())
        return {
            "room": room,
            "connection_count": len(connections),
            "connections": list(connections)
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get overall connection statistics."""
        total_rooms = len(self.room_connections)
        total_connections = len(self.active_connections)
        
        room_stats = {}
        for room, connections in self.room_connections.items():
            room_stats[room] = len(connections)
        
        return {
            "total_connections": total_connections,
            "total_rooms": total_rooms,
            "room_stats": room_stats,
            "active_connections": list(self.active_connections.keys())
        }
    
    def update_heartbeat(self, connection_id: str):
        """Update the heartbeat timestamp for a connection."""
        if connection_id in self.active_connections:
            self.connection_heartbeats[connection_id] = datetime.utcnow()
            self.connection_status[connection_id] = "connected"
            logger.debug(f"Heartbeat updated for connection: {connection_id}")
    
    def check_connection_health(self, connection_id: str) -> bool:
        """Check if a connection is healthy based on heartbeat."""
        if connection_id not in self.connection_heartbeats:
            return False
        
        last_heartbeat = self.connection_heartbeats[connection_id]
        time_since_heartbeat = (datetime.utcnow() - last_heartbeat).total_seconds()
        
        if time_since_heartbeat > self.max_idle_time:
            self.connection_status[connection_id] = "idle"
            return False
        
        return True
    
    def get_connection_health(self, connection_id: str) -> Dict[str, Any]:
        """Get health information for a specific connection."""
        if connection_id not in self.active_connections:
            return {"status": "not_found"}
        
        last_heartbeat = self.connection_heartbeats.get(connection_id)
        status = self.connection_status.get(connection_id, "unknown")
        
        if last_heartbeat:
            time_since_heartbeat = (datetime.utcnow() - last_heartbeat).total_seconds()
            is_healthy = time_since_heartbeat <= self.max_idle_time
        else:
            time_since_heartbeat = None
            is_healthy = False
        
        return {
            "connection_id": connection_id,
            "status": status,
            "last_heartbeat": last_heartbeat.isoformat() if last_heartbeat else None,
            "time_since_heartbeat": time_since_heartbeat,
            "is_healthy": is_healthy,
            "max_idle_time": self.max_idle_time
        }
    
    def cleanup_idle_connections(self):
        """Clean up connections that have been idle for too long."""
        idle_connections = []
        
        for connection_id in list(self.active_connections.keys()):
            if not self.check_connection_health(connection_id):
                idle_connections.append(connection_id)
        
        for connection_id in idle_connections:
            logger.info(f"Cleaning up idle connection: {connection_id}")
            self.disconnect(connection_id)
        
        if idle_connections:
            logger.info(f"Cleaned up {len(idle_connections)} idle connections")
        
        return len(idle_connections)
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get detailed connection statistics."""
        total_connections = len(self.active_connections)
        healthy_connections = 0
        idle_connections = 0
        disconnected_connections = 0
        
        for connection_id in self.active_connections:
            if self.check_connection_health(connection_id):
                healthy_connections += 1
            else:
                idle_connections += 1
        
        return {
            "total_connections": total_connections,
            "healthy_connections": healthy_connections,
            "idle_connections": idle_connections,
            "disconnected_connections": disconnected_connections,
            "max_idle_time": self.max_idle_time,
            "cleanup_last_run": getattr(self, '_last_cleanup', None)
        }


# Global connection manager instance
connection_manager = ConnectionManager()


class WebSocketService:
    """High-level WebSocket service for parliamentary events."""
    
    @staticmethod
    async def broadcast_vote_update(vote_data: Dict[str, Any], room: Optional[str] = None):
        """Broadcast a vote update event."""
        event = WebSocketEvent(
            type=EventType.VOTE_UPDATE,
            priority=EventPriority.HIGH,
            data=vote_data,
            source="vote_service"
        )
        
        if room:
            await connection_manager.broadcast_to_room(room, event)
        else:
            await connection_manager.broadcast_to_all(event)
    
    @staticmethod
    async def broadcast_bill_status_change(bill_data: Dict[str, Any], room: Optional[str] = None):
        """Broadcast a bill status change event."""
        event = WebSocketEvent(
            type=EventType.BILL_STATUS_CHANGE,
            priority=EventPriority.NORMAL,
            data=bill_data,
            source="bill_service"
        )
        
        if room:
            await connection_manager.broadcast_to_room(room, event)
        else:
            await connection_manager.broadcast_to_all(event)
    
    @staticmethod
    async def broadcast_debate_statement(statement_data: Dict[str, Any], room: Optional[str] = None):
        """Broadcast a debate statement event."""
        event = WebSocketEvent(
            type=EventType.DEBATE_STATEMENT,
            priority=EventPriority.LOW,
            data=statement_data,
            source="debate_service"
        )
        
        if room:
            await connection_manager.broadcast_to_room(room, event)
        else:
            await connection_manager.broadcast_to_all(event)
    
    @staticmethod
    async def broadcast_committee_meeting_update(meeting_data: Dict[str, Any], room: Optional[str] = None):
        """Broadcast a committee meeting update event."""
        event = WebSocketEvent(
            type=EventType.COMMITTEE_MEETING_UPDATE,
            priority=EventPriority.NORMAL,
            data=meeting_data,
            source="committee_service"
        )
        
        if room:
            await connection_manager.broadcast_to_room(room, event)
        else:
            await connection_manager.broadcast_to_all(event)
    
    @staticmethod
    async def send_notification(connection_id: str, message: str, priority: EventPriority = EventPriority.NORMAL):
        """Send a notification to a specific connection."""
        event = WebSocketEvent(
            type=EventType.NOTIFICATION,
            priority=priority,
            data={"message": message},
            source="notification_service"
        )
        
        await connection_manager.send_personal_message(connection_id, event)
    
    @staticmethod
    async def broadcast_notification(message: str, priority: EventPriority = EventPriority.NORMAL, room: Optional[str] = None):
        """Broadcast a notification to all connections or a specific room."""
        event = WebSocketEvent(
            type=EventType.NOTIFICATION,
            priority=priority,
            data={"message": message},
            source="notification_service"
        )
        
        if room:
            await connection_manager.broadcast_to_room(room, event)
        else:
            await connection_manager.broadcast_to_all(event)


# Convenience functions for external use
async def broadcast_vote_update(vote_data: Dict[str, Any], room: Optional[str] = None):
    """Convenience function to broadcast vote updates."""
    await WebSocketService.broadcast_vote_update(vote_data, room)


async def broadcast_bill_status_change(bill_data: Dict[str, Any], room: Optional[str] = None):
    """Convenience function to broadcast bill status changes."""
    await WebSocketService.broadcast_bill_status_change(bill_data, room)


async def broadcast_debate_statement(statement_data: Dict[str, Any], room: Optional[str] = None):
    """Convenience function to broadcast debate statements."""
    await WebSocketService.broadcast_debate_statement(statement_data, room)


async def broadcast_committee_meeting_update(meeting_data: Dict[str, Any], room: Optional[str] = None):
    """Convenience function to broadcast committee meeting updates."""
    await WebSocketService.broadcast_committee_meeting_update(meeting_data, room)
