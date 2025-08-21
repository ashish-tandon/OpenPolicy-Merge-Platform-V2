"""
OpenPolicy API Gateway - Main Application

FastAPI application providing unified access to parliamentary and civic data
from multiple jurisdictions including federal, provincial, and municipal sources.
"""

import os
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import engine, init_db

# Import API routers
from app.api.v1 import (
    bills, members, represent, debates, committees, search,
    house_mentions, user_profiles, saved_items, bill_voting, chat, issues,
    mobile_app
)
# Temporarily commented out due to Pydantic schema issues
# votes,

# Import Multi-Level Government API routers
from app.api.v1 import multi_level_government, multi_level_government_extended

# Import new infrastructure components
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.middleware.rate_limiting import rate_limit_middleware

# Initialize database tables (in development)
if settings.ENV == "local":
    try:
        init_db()
        print("✅ Database tables initialized successfully")
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")
        print("   This is normal if the database schema already exists")

# Initialize FastAPI app
app = FastAPI(
    title="OpenPolicy API",
    version="0.1.0",
    openapi_url="/openapi.json" if settings.DEBUG else None,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Add custom middleware
app.middleware("http")(rate_limit_middleware)
# TODO: Fix versioning middleware - currently causing routing issues
# app.middleware("http")(version_middleware)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "code": "INTERNAL_ERROR",
            "details": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )

@app.get("/healthz")
async def healthz() -> Dict[str, Any]:
    """
    Health check endpoint for load balancers and monitoring.
    
    Returns:
        Dict containing service status, timestamp, and version
    """
    try:
        # Test database connection
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0",
        "environment": settings.ENV,
        "database": db_status
    }

@app.get("/version")
async def version() -> Dict[str, Any]:
    """
    API version information endpoint.
    
    Returns:
        Dict containing version, build date, and git commit info
    """
    return {
        "version": "0.1.0",
        "build_date": datetime.utcnow().isoformat(),
        "git_commit": os.getenv("GIT_COMMIT", "unknown"),
        "environment": settings.ENV
    }

@app.get("/")
async def root() -> Dict[str, str]:
    """
    Root endpoint with API information.
    
    Returns:
        Dict containing welcome message and documentation links
    """
    return {
        "message": "Welcome to OpenPolicy API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/healthz",
        "api_versions": "/api/versions"
    }

# Legacy route mounting (will be deprecated)
app.include_router(
    bills.router,
    prefix="/api/v1/bills",
    tags=["bills"]
)

app.include_router(
    members.router,
    prefix="/api/v1/members",
    tags=["members"]
)

app.include_router(
    represent.router,
    prefix="/api/v1/represent",
    tags=["represent"]
)

app.include_router(
    debates.router,
    prefix="/api/v1/debates",
    tags=["debates"]
)

app.include_router(
    committees.router,
    prefix="/api/v1/committees",
    tags=["committees"]
)

app.include_router(
    search.router,
    prefix="/api/v1/search",
    tags=["search"]
)

# Temporarily commented out due to Pydantic schema issues
# app.include_router(
#     votes.router,
#     prefix="/api/v1/votes",
#     tags=["votes"]
# )

app.include_router(
    house_mentions.router,
    prefix="/api/v1/house-mentions",
    tags=["house-mentions"]
)

app.include_router(
    user_profiles.router,
    prefix="/api/v1/user-profiles",
    tags=["user-profiles"]
)

app.include_router(
    saved_items.router,
    prefix="/api/v1/saved-items",
    tags=["saved-items"]
)

app.include_router(
    bill_voting.router,
    prefix="/api/v1/bill-voting",
    tags=["bill-voting"]
)

app.include_router(
    chat.router,
    prefix="/api/v1/chat",
    tags=["chat"]
)

app.include_router(
    issues.router,
    prefix="/api/v1/issues",
    tags=["issues"]
)

# Include Mobile App API router for compatibility
app.include_router(
    mobile_app.router,
    tags=["mobile-app"]
)

# Include new infrastructure routes
try:
    from src.api.v1 import export, feeds
    
    app.include_router(
        export.router,
        prefix="/api/v1/export",
        tags=["export"]
    )
    
    app.include_router(
        feeds.router,
        prefix="/api/v1/feeds",
        tags=["feeds"]
    )
except ImportError:
    print("⚠️  Export and feeds modules not found, skipping...")

# Include Multi-Level Government API routers
app.include_router(
    multi_level_government.router,
    prefix="/api/v1/multi-level-government",
    tags=["multi-level-government"]
)

app.include_router(
    multi_level_government_extended.router,
    prefix="/api/v1/multi-level-government",
    tags=["multi-level-government"]
)

# app.include_router(
#     votes.router,
#     prefix="/api/v1/votes",
#     tags=["votes"]
# )

# Set up API versioning
# TODO: Fix versioning system - currently causing routing issues
# try:
#     create_versioned_app(app)
# except Exception as e:
#     print(f"⚠️  Could not set up API versioning: {e}")

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        workers=settings.API_WORKERS
    )
