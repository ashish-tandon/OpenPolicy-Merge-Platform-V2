"""
Redis service for pub/sub event distribution.

This module provides Redis-based event publishing and subscription for
scalable real-time event distribution across multiple API instances.
"""

import json
import logging
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
import redis.asyncio as redis
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class RedisConfig(BaseModel):
    """Configuration for Redis connection."""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    ssl: bool = False
    decode_responses: bool = True
    max_connections: int = 20


class RedisService:
    """Redis service for event publishing and subscription."""
    
    def __init__(self, config: RedisConfig):
        self.config = config
        self.redis_client: Optional[redis.Redis] = None
        self.pubsub: Optional[redis.client.PubSub] = None
        self.subscribers: Dict[str, List[Callable]] = {}
        self._is_connected = False
    
    async def connect(self):
        """Establish connection to Redis."""
        try:
            self.redis_client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                ssl=self.config.ssl,
                decode_responses=self.config.decode_responses,
                max_connections=self.config.max_connections
            )
            
            # Test connection
            await self.redis_client.ping()
            self._is_connected = True
            logger.info(f"Connected to Redis at {self.config.host}:{self.config.port}")
            
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self._is_connected = False
            raise
    
    async def disconnect(self):
        """Close Redis connection."""
        if self.redis_client:
            await self.redis_client.close()
            self._is_connected = False
            logger.info("Disconnected from Redis")
    
    async def is_connected(self) -> bool:
        """Check if Redis connection is active."""
        if not self._is_connected or not self.redis_client:
            return False
        
        try:
            await self.redis_client.ping()
            return True
        except Exception:
            self._is_connected = False
            return False
    
    async def publish_event(self, channel: str, event_data: Dict[str, Any]) -> int:
        """Publish an event to a Redis channel."""
        if not await self.is_connected():
            logger.error("Cannot publish event: Redis not connected")
            return 0
        
        try:
            # Add timestamp if not present
            if "timestamp" not in event_data:
                event_data["timestamp"] = datetime.utcnow().isoformat()
            
            # Serialize event data
            message = json.dumps(event_data, default=str)
            
            # Publish to Redis channel
            subscribers = await self.redis_client.publish(channel, message)
            logger.debug(f"Published event to channel {channel}: {subscribers} subscribers")
            return subscribers
            
        except Exception as e:
            logger.error(f"Failed to publish event to channel {channel}: {e}")
            return 0
    
    async def subscribe_to_channel(self, channel: str, callback: Callable[[Dict[str, Any]], None]):
        """Subscribe to a Redis channel with a callback function."""
        if not await self.is_connected():
            logger.error("Cannot subscribe: Redis not connected")
            return False
        
        try:
            # Initialize pubsub if not exists
            if not self.pubsub:
                self.pubsub = self.redis_client.pubsub()
            
            # Subscribe to channel
            await self.pubsub.subscribe(channel)
            
            # Store callback
            if channel not in self.subscribers:
                self.subscribers[channel] = []
            self.subscribers[channel].append(callback)
            
            logger.info(f"Subscribed to Redis channel: {channel}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to subscribe to channel {channel}: {e}")
            return False
    
    async def unsubscribe_from_channel(self, channel: str, callback: Optional[Callable] = None):
        """Unsubscribe from a Redis channel."""
        if not self.pubsub:
            return
        
        try:
            if callback:
                # Remove specific callback
                if channel in self.subscribers:
                    self.subscribers[channel] = [cb for cb in self.subscribers[channel] if cb != callback]
                    if not self.subscribers[channel]:
                        del self.subscribers[channel]
                        await self.pubsub.unsubscribe(channel)
            else:
                # Remove all callbacks for channel
                if channel in self.subscribers:
                    del self.subscribers[channel]
                    await self.pubsub.unsubscribe(channel)
            
            logger.info(f"Unsubscribed from Redis channel: {channel}")
            
        except Exception as e:
            logger.error(f"Failed to unsubscribe from channel {channel}: {e}")
    
    async def listen_for_events(self):
        """Listen for events from subscribed channels."""
        if not self.pubsub:
            logger.error("Cannot listen: No pubsub connection")
            return
        
        try:
            async for message in self.pubsub.listen():
                if message["type"] == "message":
                    channel = message["channel"]
                    data = message["data"]
                    
                    # Parse JSON data
                    try:
                        event_data = json.loads(data)
                        
                        # Call all registered callbacks for this channel
                        if channel in self.subscribers:
                            for callback in self.subscribers[channel]:
                                try:
                                    callback(event_data)
                                except Exception as e:
                                    logger.error(f"Error in callback for channel {channel}: {e}")
                        
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse event data from channel {channel}: {e}")
                
        except Exception as e:
            logger.error(f"Error listening for events: {e}")
    
    async def get_channel_info(self, channel: str) -> Dict[str, Any]:
        """Get information about a Redis channel."""
        if not await self.is_connected():
            return {"error": "Redis not connected"}
        
        try:
            # Get number of subscribers
            subscribers = await self.redis_client.pubsub_numsub(channel)
            
            # Get channel patterns
            patterns = await self.redis_client.pubsub_numpat()
            
            return {
                "channel": channel,
                "subscribers": subscribers.get(channel, 0),
                "total_patterns": patterns,
                "local_subscribers": len(self.subscribers.get(channel, []))
            }
            
        except Exception as e:
            logger.error(f"Failed to get channel info for {channel}: {e}")
            return {"error": str(e)}
    
    async def get_redis_info(self) -> Dict[str, Any]:
        """Get Redis server information."""
        if not await self.is_connected():
            return {"error": "Redis not connected"}
        
        try:
            info = await self.redis_client.info()
            return {
                "redis_version": info.get("redis_version"),
                "connected_clients": info.get("connected_clients"),
                "used_memory_human": info.get("used_memory_human"),
                "total_commands_processed": info.get("total_commands_processed"),
                "keyspace_hits": info.get("keyspace_hits"),
                "keyspace_misses": info.get("keyspace_misses")
            }
            
        except Exception as e:
            logger.error(f"Failed to get Redis info: {e}")
            return {"error": str(e)}


# Default Redis configuration
default_redis_config = RedisConfig(
    host="localhost",
    port=6379,
    db=0
)

# Global Redis service instance
redis_service = RedisService(default_redis_config)


# Convenience functions for external use
async def publish_event(channel: str, event_data: Dict[str, Any]) -> int:
    """Convenience function to publish an event."""
    return await redis_service.publish_event(channel, event_data)


async def subscribe_to_channel(channel: str, callback: Callable[[Dict[str, Any]], None]):
    """Convenience function to subscribe to a channel."""
    return await redis_service.subscribe_to_channel(channel, callback)


async def unsubscribe_from_channel(channel: str, callback: Optional[Callable] = None):
    """Convenience function to unsubscribe from a channel."""
    return await redis_service.unsubscribe_from_channel(channel, callback)


async def get_channel_info(channel: str) -> Dict[str, Any]:
    """Convenience function to get channel information."""
    return await redis_service.get_channel_info(channel)


async def get_redis_info() -> Dict[str, Any]:
    """Convenience function to get Redis information."""
    return await redis_service.get_redis_info()
