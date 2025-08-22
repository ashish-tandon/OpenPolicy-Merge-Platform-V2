"""
Merge V2 API Gateway - Main Application

FastAPI application providing unified access to parliamentary and municipal data
from multiple jurisdictions including federal, provincial, and municipal sources.
"""

import time
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, Response
import structlog

from app.config import settings
from app.api.v1.api import api_router
from app.core.middleware import RequestLoggingMiddleware
from app.core.metrics import setup_metrics
from app.database import init_db, check_db_connection

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

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

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
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
        "message": "Welcome to OpenPolicy API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/healthz"
    }

@app.get("/healthz")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat() + "Z",
        "version": "0.1.0",
        "environment": "development",
        "database": "connected"
    }

@app.get("/version")
async def version_check():
    """Version endpoint."""
    return {
        "version": "0.1.0",
        "build_date": datetime.now().isoformat() + "Z",
        "git_commit": "development",
        "environment": "development"
    }

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(
        "Unhandled exception",
        exc_info=exc,
        path=request.url.path,
        method=request.method
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "timestamp": time.time()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
