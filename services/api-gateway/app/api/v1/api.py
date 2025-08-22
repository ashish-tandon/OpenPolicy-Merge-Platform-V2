"""
Main API router for Merge V2 API Gateway
"""

from fastapi import APIRouter
from app.api.v1.endpoints import entities, users, health
from app.api.v1 import votes, debates, auth, committees, members, bills, search, websocket

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(entities.router, prefix="/entities", tags=["entities"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(votes.router, prefix="/votes", tags=["votes"])
api_router.include_router(debates.router, prefix="/debates", tags=["debates"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(committees.router, prefix="/committees", tags=["committees"])
api_router.include_router(members.router, prefix="/members", tags=["members"])
api_router.include_router(bills.router, prefix="/bills", tags=["bills"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
