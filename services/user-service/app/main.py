"""
Main FastAPI application for the User Service.

This service handles all user authentication and management,
completely separate from legislative data.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time

from app.config.settings import settings
from app.api.v1 import health, auth_simple, profile_simple

# Initialize FastAPI app
app = FastAPI(
    title=settings.SERVICE_NAME.title().replace("-", " "),
    description="User authentication and management service for OpenPolicy",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc),
            "path": str(request.url)
        }
    )


# Include API routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(auth_simple.router, prefix="/api/v1/auth")
app.include_router(profile_simple.router, prefix="/api/v1/profile")
# Temporarily commented out due to Pydantic model compatibility issues
# app.include_router(auth.router, prefix="/api/v1")
# app.include_router(users.router, prefix="/api/v1")
# app.include_router(profile.router, prefix="/api/v1")
# app.include_router(engagement.router, prefix="/api/v1")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {
        "service": settings.SERVICE_NAME,
        "version": "1.0.0",
        "status": "healthy",
        "message": "User Service is running"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "timestamp": time.time()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.SERVICE_PORT,
        reload=settings.DEBUG
    )
