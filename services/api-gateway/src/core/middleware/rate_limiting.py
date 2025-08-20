"""
Rate limiting middleware for API Gateway
Adapted from legacy openparliament rate limiting patterns
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time
from typing import Dict, Tuple
import asyncio
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    """
    Rate limiter implementation based on legacy rate_limit decorator
    from summaries/llm.py
    """
    def __init__(self):
        # Store request counts per IP
        self.requests: Dict[str, list] = defaultdict(list)
        # Different rate limits for different endpoints
        self.limits = {
            'default': (100, 60),  # 100 requests per minute
            'search': (30, 60),    # 30 searches per minute
            'export': (10, 300),   # 10 exports per 5 minutes
            'api': (1000, 3600),   # 1000 API calls per hour
        }
        
    def _clean_old_requests(self, ip: str, window_seconds: int):
        """Remove requests older than the time window"""
        cutoff = time.time() - window_seconds
        self.requests[ip] = [req_time for req_time in self.requests[ip] if req_time > cutoff]
    
    def check_rate_limit(self, ip: str, endpoint_type: str = 'default') -> Tuple[bool, dict]:
        """
        Check if request is within rate limit
        Returns (allowed, metadata)
        """
        limit, window = self.limits.get(endpoint_type, self.limits['default'])
        
        # Clean old requests
        self._clean_old_requests(ip, window)
        
        # Check current count
        current_count = len(self.requests[ip])
        
        if current_count >= limit:
            # Calculate when the oldest request will expire
            oldest_request = min(self.requests[ip])
            retry_after = int(oldest_request + window - time.time())
            
            return False, {
                'limit': limit,
                'window': window,
                'retry_after': retry_after,
                'current': current_count
            }
        
        # Add current request
        self.requests[ip].append(time.time())
        
        return True, {
            'limit': limit,
            'window': window,
            'remaining': limit - current_count - 1,
            'reset': int(time.time() + window)
        }

# Global rate limiter instance
rate_limiter = RateLimiter()

async def rate_limit_middleware(request: Request, call_next):
    """
    FastAPI middleware for rate limiting
    Based on legacy feed_wrapper pattern
    """
    # Get client IP
    ip = request.client.host
    
    # Determine endpoint type
    endpoint_type = 'default'
    if '/search' in request.url.path:
        endpoint_type = 'search'
    elif '/export' in request.url.path:
        endpoint_type = 'export'
    elif '/api/v' in request.url.path:
        endpoint_type = 'api'
    
    # Check rate limit
    allowed, metadata = rate_limiter.check_rate_limit(ip, endpoint_type)
    
    if not allowed:
        # Return 429 Too Many Requests
        return JSONResponse(
            status_code=429,
            content={
                "error": "Rate limit exceeded",
                "retry_after": metadata['retry_after'],
                "limit": metadata['limit'],
                "window": metadata['window']
            },
            headers={
                "X-RateLimit-Limit": str(metadata['limit']),
                "X-RateLimit-Window": str(metadata['window']),
                "Retry-After": str(metadata['retry_after'])
            }
        )
    
    # Process request
    response = await call_next(request)
    
    # Add rate limit headers
    response.headers["X-RateLimit-Limit"] = str(metadata['limit'])
    response.headers["X-RateLimit-Remaining"] = str(metadata['remaining'])
    response.headers["X-RateLimit-Reset"] = str(metadata['reset'])
    
    return response
