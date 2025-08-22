"""
Merge V2 API Gateway - Main Application

FastAPI application providing unified access to parliamentary and municipal data
from multiple jurisdictions including federal, provincial, and municipal sources.
"""

import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.config import settings
from app.api.v1.api import api_router
from app.core.middleware import RequestLoggingMiddleware
from app.core.metrics import setup_metrics
from app.database import init_db, check_db_connection

# Initialize FastAPI app
app = FastAPI(
    title="Merge V2 API Gateway",
    description="Unified API for parliamentary and municipal data",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

app.add_middleware(RequestLoggingMiddleware)

# Setup metrics
setup_metrics(app)

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        if check_db_connection():
            init_db()
            print("✅ Database initialized successfully")
        else:
            print("⚠️  Database connection failed - running in mock mode")
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")
        print("   This is normal if the database schema already exists")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Merge V2 API Gateway",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "api-gateway"
    }

@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "api-gateway",
        "database": "not_configured",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
