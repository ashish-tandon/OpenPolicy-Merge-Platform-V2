"""
Users endpoints for user management
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel, EmailStr
import time

router = APIRouter()

# Pydantic models
class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: str
    created_at: str
    updated_at: str

class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    page: int
    size: int

@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size")
):
    """List users with pagination"""
    # TODO: Implement actual database query
    # For now, return mock data
    mock_users = [
        {
            "id": "user-1",
            "username": "admin",
            "email": "admin@example.com",
            "is_active": True,
            "created_at": "2025-08-21T00:00:00Z",
            "updated_at": "2025-08-21T00:00:00Z"
        }
    ]
    
    return UserListResponse(
        users=mock_users,
        total=1,
        page=page,
        size=size
    )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get a specific user by ID"""
    # TODO: Implement actual database query
    # For now, return mock data
    if user_id == "user-1":
        return {
            "id": user_id,
            "username": "admin",
            "email": "admin@example.com",
            "is_active": True,
            "created_at": "2025-08-21T00:00:00Z",
            "updated_at": "2025-08-21T00:00:00Z"
        }
    
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    """Create a new user"""
    # TODO: Implement actual database creation with password hashing
    # For now, return mock response
    return {
        "id": "new-user-id",
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate):
    """Update an existing user"""
    # TODO: Implement actual database update
    # For now, return mock response
    return {
        "id": user_id,
        "username": user_update.username or "admin",
        "email": user_update.email or "admin@example.com",
        "is_active": user_update.is_active if user_update.is_active is not None else True,
        "created_at": "2025-08-21T00:00:00Z",
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """Delete a user"""
    # TODO: Implement actual database deletion
    # For now, return success
    return {"message": "User deleted successfully"}
