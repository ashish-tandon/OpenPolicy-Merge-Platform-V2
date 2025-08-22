"""
Middleware for Merge V2 API Gateway
"""

import time
import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = structlog.get_logger()

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(
            "Request started",
            method=request.method,
            url=str(request.url),
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            "Request completed",
            method=request.method,
            url=str(request.url),
            status_code=response.status_code,
            duration=duration
        )
        
        # Add response headers
        response.headers["X-Response-Time"] = str(duration)
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Advanced middleware for implementing IP-based rate limiting with endpoint-specific limits."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        # Different rate limits for different endpoints
        self.limits = {
            'default': (100, 60),      # 100 requests per minute
            'search': (30, 60),        # 30 searches per minute
            'export': (10, 300),       # 10 exports per 5 minutes
            'api': (1000, 3600),      # 1000 API calls per hour
            'auth': (20, 60),          # 20 auth attempts per minute
            'voting': (50, 60),        # 50 voting operations per minute
            'bills': (100, 60),        # 100 bill operations per minute
            'members': (80, 60),       # 80 member operations per minute
        }
        self.request_counts = {}
    
    def _clean_old_requests(self, ip: str, window_seconds: int):
        """Remove requests older than the time window"""
        current_time = time.time()
        cutoff = current_time - window_seconds
        if ip in self.request_counts:
            self.request_counts[ip] = [req_time for req_time in self.request_counts[ip] if req_time > cutoff]
    
    def _get_endpoint_type(self, path: str) -> str:
        """Determine endpoint type based on URL path"""
        if '/search' in path:
            return 'search'
        elif '/export' in path:
            return 'export'
        elif '/auth' in path:
            return 'auth'
        elif '/votes' in path:
            return 'voting'
        elif '/bills' in path:
            return 'bills'
        elif '/members' in path:
            return 'members'
        elif '/api/v' in path:
            return 'api'
        else:
            return 'default'
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        endpoint_type = self._get_endpoint_type(str(request.url.path))
        limit, window = self.limits.get(endpoint_type, self.limits['default'])
        
        # Clean old requests
        self._clean_old_requests(client_ip, window)
        
        # Initialize request tracking for this IP if not exists
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = []
        
        # Check rate limit
        current_count = len(self.request_counts[client_ip])
        
        if current_count >= limit:
            # Calculate retry after time
            oldest_request = min(self.request_counts[client_ip])
            retry_after = int(oldest_request + window - time.time())
            
            logger.warning(
                "Rate limit exceeded",
                client_ip=client_ip,
                endpoint_type=endpoint_type,
                requests=current_count,
                limit=limit,
                window=window
            )
            
            return Response(
                content=f"Rate limit exceeded. Maximum {limit} requests per {window} seconds.",
                status_code=429,
                media_type="text/plain",
                headers={
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Window": str(window),
                    "X-RateLimit-Reset": str(int(time.time() + window)),
                    "Retry-After": str(retry_after)
                }
            )
        
        # Add current request
        self.request_counts[client_ip].append(time.time())
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(limit - current_count - 1)
        response.headers["X-RateLimit-Reset"] = str(int(time.time() + window))
        
        return response


class RedisRateLimitMiddleware(BaseHTTPMiddleware):
    """Redis-based rate limiting middleware for production scalability."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        try:
            import redis
            from app.config import settings
            self.redis_client = redis.from_url(settings.REDIS_URL)
            self.redis_available = True
            logger.info("Redis rate limiting enabled")
        except ImportError:
            logger.warning("Redis not available, falling back to in-memory rate limiting")
            self.redis_available = False
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}, falling back to in-memory rate limiting")
            self.redis_available = False
        
        # Rate limits (same as in-memory version)
        self.limits = {
            'default': (100, 60),      # 100 requests per minute
            'search': (30, 60),        # 30 searches per minute
            'export': (10, 300),       # 10 exports per 5 minutes
            'api': (1000, 3600),      # 1000 API calls per hour
            'auth': (20, 60),          # 20 auth attempts per minute
            'voting': (50, 60),        # 50 voting operations per minute
            'bills': (100, 60),        # 100 bill operations per minute
            'members': (80, 60),       # 80 member operations per minute
        }
    
    def _get_endpoint_type(self, path: str) -> str:
        """Determine endpoint type based on URL path"""
        if '/search' in path:
            return 'search'
        elif '/export' in path:
            return 'export'
        elif '/auth' in path:
            return 'auth'
        elif '/votes' in path:
            return 'voting'
        elif '/bills' in path:
            return 'bills'
        elif '/members' in path:
            return 'members'
        elif '/api/v' in path:
            return 'api'
        else:
            return 'default'
    
    async def dispatch(self, request: Request, call_next):
        if not self.redis_available:
            # Fall back to in-memory rate limiting
            return await call_next(request)
        
        client_ip = request.client.host if request.client else "unknown"
        endpoint_type = self._get_endpoint_type(str(request.url.path))
        limit, window = self.limits.get(endpoint_type, self.limits['default'])
        
        # Redis key for this IP and endpoint type
        redis_key = f"rate_limit:{client_ip}:{endpoint_type}"
        
        try:
            # Use Redis pipeline for atomic operations
            pipe = self.redis_client.pipeline()
            
            # Get current count and set expiry
            pipe.get(redis_key)
            pipe.expire(redis_key, window)
            results = pipe.execute()
            
            current_count = int(results[0]) if results[0] else 0
            
            if current_count >= limit:
                # Calculate retry after time
                ttl = self.redis_client.ttl(redis_key)
                retry_after = max(0, ttl)
                
                logger.warning(
                    "Redis rate limit exceeded",
                    client_ip=client_ip,
                    endpoint_type=endpoint_type,
                    requests=current_count,
                    limit=limit,
                    window=window
                )
                
                return Response(
                    content=f"Rate limit exceeded. Maximum {limit} requests per {window} seconds.",
                    status_code=429,
                    media_type="text/plain",
                    headers={
                        "X-RateLimit-Limit": str(limit),
                        "X-RateLimit-Window": str(window),
                        "X-RateLimit-Reset": str(int(time.time() + window)),
                        "Retry-After": str(retry_after)
                    }
                )
            
            # Increment counter
            self.redis_client.incr(redis_key)
            
            # Process request
            response = await call_next(request)
            
            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(limit)
            response.headers["X-RateLimit-Remaining"] = str(limit - current_count - 1)
            response.headers["X-RateLimit-Reset"] = str(int(time.time() + window))
            
            return response
            
        except Exception as e:
            logger.error(f"Redis rate limiting error: {e}, allowing request through")
            # If Redis fails, allow the request through
            return await call_next(request)
