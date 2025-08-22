"""
Main API router for Merge V2 API Gateway
"""

from fastapi import APIRouter
from app.api.v1.endpoints import entities, users, health

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(entities.router, prefix="/entities", tags=["entities"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
