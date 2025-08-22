from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import structlog

logger = structlog.get_logger()

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""
    
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
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for implementing IP-based rate limiting."""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_counts = {}
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Clean old entries (older than 1 minute)
        self.request_counts = {
            ip: count for ip, count in self.request_counts.items()
            if current_time - count["timestamp"] < 60
        }
        
        # Check rate limit
        if client_ip in self.request_counts:
            if self.request_counts[client_ip]["count"] >= self.requests_per_minute:
                return Response(
                    content="Rate limit exceeded",
                    status_code=429,
                    media_type="text/plain"
                )
            self.request_counts[client_ip]["count"] += 1
        else:
            self.request_counts[client_ip] = {
                "count": 1,
                "timestamp": current_time
            }
        
        return await call_next(request)
