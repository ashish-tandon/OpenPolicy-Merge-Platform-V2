"""
Health check endpoints
"""

from fastapi import APIRouter
import time

router = APIRouter()

@router.get("/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "api-gateway"
    }

@router.get("/detailed")
async def detailed_health_check():
    """Detailed health check without database dependency for now"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "api-gateway",
        "database": "not_configured",
        "version": "1.0.0"
    }
