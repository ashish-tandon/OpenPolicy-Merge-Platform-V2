"""
Cache Service

Simple in-memory cache service for feature flags.
In production, this would use Redis or similar.
"""

import asyncio
from typing import Any, Optional, Dict
from datetime import datetime, timedelta
import fnmatch


class CacheEntry:
    """Represents a cache entry with TTL."""
    def __init__(self, value: Any, ttl: int):
        self.value = value
        self.expires_at = datetime.utcnow() + timedelta(seconds=ttl)
    
    def is_expired(self) -> bool:
        """Check if entry has expired."""
        return datetime.utcnow() > self.expires_at


class CacheService:
    """Simple in-memory cache service."""
    
    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        async with self._lock:
            entry = self._cache.get(key)
            if entry:
                if entry.is_expired():
                    del self._cache[key]
                    return None
                return entry.value
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set value in cache with TTL."""
        async with self._lock:
            self._cache[key] = CacheEntry(value, ttl)
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern (synchronous for simplicity)."""
        deleted = 0
        keys_to_delete = []
        
        for key in self._cache.keys():
            if fnmatch.fnmatch(key, pattern):
                keys_to_delete.append(key)
        
        for key in keys_to_delete:
            if key in self._cache:
                del self._cache[key]
                deleted += 1
        
        return deleted
    
    async def clear(self) -> None:
        """Clear entire cache."""
        async with self._lock:
            self._cache.clear()
    
    async def cleanup_expired(self) -> int:
        """Remove expired entries."""
        async with self._lock:
            expired_keys = []
            for key, entry in self._cache.items():
                if entry.is_expired():
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._cache[key]
            
            return len(expired_keys)


# Global cache instance
cache_service = CacheService()


# Background task to cleanup expired entries
async def periodic_cleanup():
    """Run periodic cleanup of expired cache entries."""
    while True:
        try:
            await asyncio.sleep(60)  # Run every minute
            removed = await cache_service.cleanup_expired()
            if removed > 0:
                print(f"Cleaned up {removed} expired cache entries")
        except Exception as e:
            print(f"Error in cache cleanup: {e}")