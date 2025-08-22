"""
WebSocket API endpoints for real-time parliamentary data.

This module provides WebSocket endpoints for:
- Real-time vote updates
- Live debate statements
- Bill status changes
- Committee meeting updates
- User presence and notifications
"""

import json
import logging
from typing import Dict, Any
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException

from app.core.websocket import connection_manager, WebSocketService
from app.core.events import (
    EventPriority,
    create_notification_event
)
from app.core.redis_service import redis_service, publish_event

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    """
    Main WebSocket endpoint for real-time parliamentary data.
    
    This endpoint handles:
    - Connection management
    - Event broadcasting
    - Room management
    - Heartbeat monitoring
    """
    connection_id = f"ws_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{id(websocket)}"
    
    try:
        # Accept the WebSocket connection
        await connection_manager.connect(websocket, connection_id)
        
        # Send welcome message
        await WebSocketService.send_notification(
            connection_id,
            "Connected to Parliamentary Real-time Service",
            EventPriority.NORMAL
        )
        
        # Main message loop
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle different message types
                await handle_client_message(connection_id, message)
                
            except WebSocketDisconnect:
                logger.info(f"WebSocket disconnected: {connection_id}")
                break
            except json.JSONDecodeError:
                await WebSocketService.send_notification(
                    connection_id,
                    "Invalid JSON message format",
                    EventPriority.LOW
                )
            except Exception as e:
                logger.error(f"Error handling WebSocket message: {e}")
                await WebSocketService.send_notification(
                    connection_id,
                    f"Error processing message: {str(e)}",
                    EventPriority.HIGH
                )
                
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
    finally:
        # Clean up connection
        connection_manager.disconnect(connection_id)


@router.websocket("/votes")
async def votes_websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint specifically for vote updates.
    
    Automatically joins the 'votes' room for real-time vote notifications.
    """
    connection_id = f"votes_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{id(websocket)}"
    
    try:
        await connection_manager.connect(websocket, connection_id)
        
        # Automatically join votes room
        connection_manager.join_room(connection_id, "votes")
        
        await WebSocketService.send_notification(
            connection_id,
            "Connected to Vote Updates Service",
            EventPriority.NORMAL
        )
        
        # Main message loop
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle vote-specific messages
                await handle_vote_message(connection_id, message)
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Vote WebSocket error: {e}")
                break
                
    finally:
        connection_manager.disconnect(connection_id)


@router.websocket("/debates")
async def debates_websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint specifically for debate updates.
    
    Automatically joins the 'debates' room for real-time debate notifications.
    """
    connection_id = f"debates_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{id(websocket)}"
    
    try:
        await connection_manager.connect(websocket, connection_id)
        
        # Automatically join debates room
        connection_manager.join_room(connection_id, "debates")
        
        await WebSocketService.send_notification(
            connection_id,
            "Connected to Debate Updates Service",
            EventPriority.NORMAL
        )
        
        # Main message loop
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle debate-specific messages
                await handle_debate_message(connection_id, message)
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Debate WebSocket error: {e}")
                break
                
    finally:
        connection_manager.disconnect(connection_id)


@router.websocket("/bills")
async def bills_websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint specifically for bill updates.
    
    Automatically joins the 'bills' room for real-time bill notifications.
    """
    connection_id = f"bills_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{id(websocket)}"
    
    try:
        await connection_manager.connect(websocket, connection_id)
        
        # Automatically join bills room
        connection_manager.join_room(connection_id, "bills")
        
        await WebSocketService.send_notification(
            connection_id,
            "Connected to Bill Updates Service",
            EventPriority.NORMAL
        )
        
        # Main message loop
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle bill-specific messages
                await handle_bill_message(connection_id, message)
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Bill WebSocket error: {e}")
                break
                
    finally:
        connection_manager.disconnect(connection_id)


@router.websocket("/committees")
async def committees_websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint specifically for committee updates.
    
    Automatically joins the 'committees' room for real-time committee notifications.
    """
    connection_id = f"committees_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{id(websocket)}"
    
    try:
        await connection_manager.connect(websocket, connection_id)
        
        # Automatically join committees room
        connection_manager.join_room(connection_id, "committees")
        
        await WebSocketService.send_notification(
            connection_id,
            "Connected to Committee Updates Service",
            EventPriority.NORMAL
        )
        
        # Main message loop
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle committee-specific messages
                await handle_committee_message(connection_id, message)
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Committee WebSocket error: {e}")
                break
                
    finally:
        connection_manager.disconnect(connection_id)


# Message Handlers

async def handle_client_message(connection_id: str, message: Dict[str, Any]):
    """Handle general client messages."""
    message_type = message.get("type")
    
    if message_type == "join_room":
        room = message.get("room")
        if room:
            connection_manager.join_room(connection_id, room)
            await WebSocketService.send_notification(
                connection_id,
                f"Joined room: {room}",
                EventPriority.LOW
            )
    
    elif message_type == "leave_room":
        room = message.get("room")
        if room:
            connection_manager.leave_room(connection_id, room)
            await WebSocketService.send_notification(
                connection_id,
                f"Left room: {room}",
                EventPriority.LOW
            )
    
    elif message_type == "ping":
        # Respond to heartbeat
        await WebSocketService.send_notification(
            connection_id,
            "pong",
            EventPriority.LOW
        )
    
    elif message_type == "get_rooms":
        # Send list of rooms the connection is in
        rooms = list(connection_manager.connection_rooms.get(connection_id, []))
        await connection_manager.send_personal_message(
            connection_id,
            create_notification_event(
                message="",
                data={"rooms": rooms}
            )
        )
    
    else:
        await WebSocketService.send_notification(
            connection_id,
            f"Unknown message type: {message_type}",
            EventPriority.LOW
        )


async def handle_vote_message(connection_id: str, message: Dict[str, Any]):
    """Handle vote-specific messages."""
    message_type = message.get("type")
    
    if message_type == "subscribe_bill":
        bill_id = message.get("bill_id")
        if bill_id:
            room = f"bill_{bill_id}_votes"
            connection_manager.join_room(connection_id, room)
            await WebSocketService.send_notification(
                connection_id,
                f"Subscribed to votes for bill {bill_id}",
                EventPriority.LOW
            )
    
    elif message_type == "unsubscribe_bill":
        bill_id = message.get("bill_id")
        if bill_id:
            room = f"bill_{bill_id}_votes"
            connection_manager.leave_room(connection_id, room)
            await WebSocketService.send_notification(
                connection_id,
                f"Unsubscribed from votes for bill {bill_id}",
                EventPriority.LOW
            )
    
    else:
        await handle_client_message(connection_id, message)


async def handle_debate_message(connection_id: str, message: Dict[str, Any]):
    """Handle debate-specific messages."""
    message_type = message.get("type")
    
    if message_type == "subscribe_date":
        date = message.get("date")
        if date:
            room = f"debate_{date}"
            connection_manager.join_room(connection_id, room)
            await WebSocketService.send_notification(
                connection_id,
                f"Subscribed to debates for {date}",
                EventPriority.LOW
            )
    
    elif message_type == "unsubscribe_date":
        date = message.get("date")
        if date:
            room = f"debate_{date}"
            connection_manager.leave_room(connection_id, room)
            await WebSocketService.send_notification(
                connection_id,
                f"Unsubscribed from debates for {date}",
                EventPriority.LOW
            )
    
    else:
        await handle_client_message(connection_id, message)


async def handle_bill_message(connection_id: str, message: Dict[str, Any]):
    """Handle bill-specific messages."""
    message_type = message.get("type")
    
    if message_type == "subscribe_bill":
        bill_id = message.get("bill_id")
        if bill_id:
            room = f"bill_{bill_id}"
            connection_manager.join_room(connection_id, room)
            await WebSocketService.send_notification(
                connection_id,
                f"Subscribed to updates for bill {bill_id}",
                EventPriority.LOW
            )
    
    elif message_type == "unsubscribe_bill":
        bill_id = message.get("bill_id")
        if bill_id:
            room = f"bill_{bill_id}"
            connection_manager.leave_room(connection_id, room)
            await WebSocketService.send_notification(
                connection_id,
                f"Unsubscribed from updates for bill {bill_id}",
                EventPriority.LOW
            )
    
    else:
        await handle_client_message(connection_id, message)


async def handle_committee_message(connection_id: str, message: Dict[str, Any]):
    """Handle committee-specific messages."""
    message_type = message.get("type")
    
    if message_type == "subscribe_committee":
        committee_id = message.get("committee_id")
        if committee_id:
            room = f"committee_{committee_id}"
            connection_manager.join_room(connection_id, room)
            await WebSocketService.send_notification(
                connection_id,
                f"Subscribed to updates for committee {committee_id}",
                EventPriority.LOW
            )
    
    elif message_type == "unsubscribe_committee":
        committee_id = message.get("committee_id")
        if committee_id:
            room = f"committee_{committee_id}"
            connection_manager.leave_room(connection_id, room)
            await WebSocketService.send_notification(
                connection_id,
                f"Unsubscribed from updates for committee {committee_id}",
                EventPriority.LOW
            )
    
    else:
        await handle_client_message(connection_id, message)


# REST API endpoints for WebSocket management

@router.get("/status")
async def get_websocket_status():
    """Get WebSocket connection status and statistics."""
    try:
        stats = connection_manager.get_stats()
        redis_info = await redis_service.get_redis_info()
        
        return {
            "status": "active",
            "websocket_stats": stats,
            "redis_info": redis_info,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting WebSocket status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get WebSocket status") from e


@router.post("/heartbeat/{connection_id}")
async def update_connection_heartbeat(connection_id: str):
    """Update heartbeat for a specific WebSocket connection."""
    try:
        connection_manager.update_heartbeat(connection_id)
        return {"status": "success", "message": "Heartbeat updated"}
    except Exception as e:
        logger.error(f"Error updating heartbeat: {e}")
        raise HTTPException(status_code=500, detail="Failed to update heartbeat") from e


@router.get("/health/{connection_id}")
async def get_connection_health(connection_id: str):
    """Get health information for a specific WebSocket connection."""
    try:
        health_info = connection_manager.get_connection_health(connection_id)
        return health_info
    except Exception as e:
        logger.error(f"Error getting connection health: {e}")
        raise HTTPException(status_code=500, detail="Failed to get connection health") from e


@router.post("/cleanup")
async def cleanup_idle_connections():
    """Clean up idle WebSocket connections."""
    try:
        cleaned_count = connection_manager.cleanup_idle_connections()
        return {"status": "success", "cleaned_connections": cleaned_count}
    except Exception as e:
        logger.error(f"Error cleaning up connections: {e}")
        raise HTTPException(status_code=500, detail="Failed to cleanup connections") from e


@router.get("/connections/{connection_id}")
async def get_connection_info(connection_id: str):
    """Get information about a specific WebSocket connection."""
    info = connection_manager.get_connection_info(connection_id)
    if not info:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    return info


@router.get("/rooms/{room}")
async def get_room_info(room: str):
    """Get information about a specific room."""
    info = connection_manager.get_room_info(room)
    return info


@router.post("/broadcast")
async def broadcast_message(message: Dict[str, Any]):
    """
    Broadcast a message to all WebSocket connections.
    
    This endpoint allows external services to broadcast messages
    to all connected WebSocket clients.
    """
    try:
        message_text = message.get("message", "")
        priority = message.get("priority", "normal")
        room = message.get("room")
        
        # Create notification event
        event = create_notification_event(
            message=message_text,
            priority=EventPriority(priority)
        )
        
        # Broadcast to room or all connections
        if room:
            await connection_manager.broadcast_to_room(room, event)
            # Also publish to Redis for other instances
            await publish_event(f"broadcast_{room}", event.dict())
        else:
            await connection_manager.broadcast_to_all(event)
            # Also publish to Redis for other instances
            await publish_event("broadcast_all", event.dict())
        
        return {"status": "success", "message": "Message broadcasted"}
        
    except Exception as e:
        logger.error(f"Error broadcasting message: {e}")
        raise HTTPException(status_code=500, detail="Failed to broadcast message") from e


@router.post("/notify/{connection_id}")
async def send_notification(connection_id: str, notification: Dict[str, Any]):
    """
    Send a notification to a specific WebSocket connection.
    
    This endpoint allows external services to send notifications
    to specific connected clients.
    """
    try:
        message = notification.get("message", "")
        priority = notification.get("priority", "normal")
        
        await WebSocketService.send_notification(
            connection_id,
            message,
            EventPriority(priority)
        )
        
        return {"status": "success", "message": "Notification sent"}
        
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        raise HTTPException(status_code=500, detail="Failed to send notification") from e
