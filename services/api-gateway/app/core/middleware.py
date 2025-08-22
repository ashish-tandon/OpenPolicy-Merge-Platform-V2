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
    """Middleware for logging HTTP requests"""
    
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
    """Middleware for rate limiting"""
    
    def __init__(self, app: ASGIApp, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = {}
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Clean old requests
        self.requests = {
            ip: times for ip, times in self.requests.items()
            if current_time - times[-1] < 60
        }
        
        # Check rate limit
        if client_ip in self.requests:
            if len(self.requests[client_ip]) >= self.requests_per_minute:
                logger.warning(
                    "Rate limit exceeded",
                    client_ip=client_ip,
                    requests=len(self.requests[client_ip])
                )
                return Response(
                    content="Rate limit exceeded",
                    status_code=429,
                    media_type="text/plain"
                )
            self.requests[client_ip].append(current_time)
        else:
            self.requests[client_ip] = [current_time]
        
        return await call_next(request)
