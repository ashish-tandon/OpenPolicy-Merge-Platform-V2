from fastapi import APIRouter
import time
from app.database import check_db_connection

router = APIRouter()

@router.get("/")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "api-gateway"
    }

@router.get("/detailed")
async def detailed_health_check():
    db_status = "connected" if check_db_connection() else "disconnected"
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "api-gateway",
        "database": db_status,
        "version": "1.0.0"
    }
