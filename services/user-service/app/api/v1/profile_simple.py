"""
Simplified Profile API endpoints for User Service.

This is a temporary version that avoids complex Pydantic model issues.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from app.auth.simple_auth import current_active_user

router = APIRouter()


@router.get("/me")
async def get_profile():
    """Get current user's profile."""
    try:
        # TODO: Implement actual profile retrieval from database
        # For now, return a mock profile
        
        return {
            "success": True,
            "profile": {
                "id": "mock-user-id",
                "first_name": "Mock",
                "last_name": "User",
                "email": "mock@example.com",
                "phone": None,
                "postal_code": None,
                "role": "normal",
                "account_type": "consumer",
                "status": "active",
                "avatar_url": None,
                "preferences": {
                    "notifications": True,
                    "privacy": "public"
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get profile: {str(e)}"
        )


@router.put("/me")
async def update_profile(profile_update):
    """Update current user's profile."""
    try:
        # TODO: Implement actual profile update with database
        # For now, return a mock response
        
        return {
            "success": True,
            "message": "Profile updated successfully (mock)",
            "profile": {
                "id": "mock-user-id",
                "first_name": profile_update.get("first_name", "Mock"),
                "last_name": profile_update.get("last_name", "User"),
                "email": profile_update.get("email", "mock@example.com"),
                "phone": profile_update.get("phone"),
                "postal_code": profile_update.get("postal_code"),
                "role": "normal",
                "account_type": "consumer",
                "status": "active"
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile: {str(e)}"
        )


@router.get("/preferences")
async def get_preferences():
    """Get current user's preferences."""
    try:
        # TODO: Implement actual preferences retrieval
        # For now, return mock preferences
        
        return {
            "success": True,
            "preferences": {
                "notifications": {
                    "email": True,
                    "sms": False,
                    "push": True
                },
                "privacy": "public",
                "language": "en",
                "timezone": "UTC"
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get preferences: {str(e)}"
        )
