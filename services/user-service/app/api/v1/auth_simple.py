"""
Simplified Authentication API endpoints for User Service.

This is a temporary version that avoids complex Pydantic model issues.
"""

from fastapi import APIRouter, HTTPException, status
from app.api.schemas import UserCreate

router = APIRouter()


@router.post("/register")
async def register_user(user_data: UserCreate):
    """Register a new user account."""
    try:
        # TODO: Implement actual user creation with database
        # For now, return a mock response
        
        return {
            "success": True,
            "message": "User registered successfully (mock)",
            "user": {
                "id": "mock-user-id",
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
                "email": user_data.email,
                "phone": user_data.phone,
                "postal_code": user_data.postal_code,
                "role": user_data.role.value,
                "account_type": user_data.account_type.value,
                "status": "active"
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register user: {str(e)}"
        )


@router.post("/login")
async def login_user(login_data: dict):
    """Authenticate user with email and password."""
    try:
        # TODO: Implement actual user authentication with database
        # For now, return a mock response
        
        return {
            "success": True,
            "message": "Login successful (mock)",
            "user": {
                "id": "mock-user-id",
                "first_name": "Mock",
                "last_name": "User",
                "email": login_data.get("email", "mock@example.com"),
                "role": "normal",
                "account_type": "consumer",
                "status": "active"
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to login: {str(e)}"
        )


@router.get("/me")
async def get_current_user():
    """Get current user information."""
    try:
        # TODO: Implement actual user retrieval
        # For now, return a mock user
        
        return {
            "success": True,
            "user": {
                "id": "mock-user-id",
                "first_name": "Mock",
                "last_name": "User",
                "email": "mock@example.com",
                "role": "normal",
                "account_type": "consumer",
                "status": "active"
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user: {str(e)}"
        )
