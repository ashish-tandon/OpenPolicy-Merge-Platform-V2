"""
User Management API endpoints for User Service.

Handles user CRUD operations, profile management, and role updates.
Separate from legislative data management.
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from datetime import datetime

from app.api.schemas import (
    UserResponse, UserUpdate, UserListResponse, UserRoleUpdate, UserStatusUpdate
)
from app.auth.simple_auth import current_active_user, require_role
from app.models.user import User, UserRole, AccountType, UserStatus

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user = Depends(current_active_user)
):
    """Get current user's profile information."""
    try:
        # Convert to response schema
        return UserResponse(
            id=str(current_user.id),
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            email=current_user.email,
            phone=current_user.phone,
            postal_code=current_user.postal_code,
            role=current_user.role,
            account_type=current_user.account_type,
            email_verified_at=current_user.email_verified_at,
            phone_verified_at=current_user.phone_verified_at,
            two_factor_enabled=current_user.two_factor_enabled,
            status=current_user.status,
            avatar_url=current_user.avatar_url,
            preferences=current_user.preferences,
            created_at=current_user.created_at,
            updated_at=current_user.updated_at,
            last_login_at=current_user.last_login_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user profile: {str(e)}"
        )


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user = Depends(current_active_user)
):
    """Update current user's profile information."""
    try:
        # TODO: Implement actual user update with database
        # For now, update mock user
        
        # Update user fields
        if user_update.first_name is not None:
            current_user.first_name = user_update.first_name
        if user_update.last_name is not None:
            current_user.last_name = user_update.last_name
        if user_update.phone is not None:
            current_user.phone = user_update.phone
        if user_update.postal_code is not None:
            current_user.postal_code = user_update.postal_code
        if user_update.avatar_url is not None:
            current_user.avatar_url = user_update.avatar_url
        if user_update.preferences is not None:
            current_user.preferences = user_update.preferences
        
        current_user.updated_at = datetime.utcnow()
        
        # Convert to response schema
        return UserResponse(
            id=str(current_user.id),
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            email=current_user.email,
            phone=current_user.phone,
            postal_code=current_user.postal_code,
            role=current_user.role,
            account_type=current_user.account_type,
            email_verified_at=current_user.email_verified_at,
            phone_verified_at=current_user.phone_verified_at,
            two_factor_enabled=current_user.two_factor_enabled,
            status=current_user.status,
            avatar_url=current_user.avatar_url,
            preferences=current_user.preferences,
            created_at=current_user.created_at,
            updated_at=current_user.updated_at,
            last_login_at=current_user.last_login_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user profile: {str(e)}"
        )


@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    role: Optional[str] = Query(None, description="Filter by user role"),
    status: Optional[str] = Query(None, description="Filter by user status"),
    search: Optional[str] = Query(None, description="Search by name or email"),
    current_user = Depends(require_role("admin"))
):
    """List users with pagination and filtering (admin only)."""
    try:
        # TODO: Implement actual user listing with database
        # For now, return mock data
        
        # Create mock users
        mock_users = [
            User(
                id="user-1",
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                role=UserRole.NORMAL,
                account_type=AccountType.CONSUMER,
                status=UserStatus.ACTIVE,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            User(
                id="user-2",
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@example.com",
                role=UserRole.ENTERPRISE,
                account_type=AccountType.CONSUMER,
                status=UserStatus.ACTIVE,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        
        # Apply filters
        if role:
            mock_users = [u for u in mock_users if u.role.value == role]
        if status:
            mock_users = [u for u in mock_users if u.status.value == status]
        if search:
            search_lower = search.lower()
            mock_users = [
                u for u in mock_users 
                if search_lower in u.first_name.lower() 
                or search_lower in u.last_name.lower() 
                or search_lower in u.email.lower()
            ]
        
        # Convert to response schemas
        user_responses = [
            UserResponse(
                id=str(u.id),
                first_name=u.first_name,
                last_name=u.last_name,
                email=u.email,
                phone=u.phone,
                postal_code=u.postal_code,
                role=u.role,
                account_type=u.account_type,
                email_verified_at=u.email_verified_at,
                phone_verified_at=u.phone_verified_at,
                two_factor_enabled=u.two_factor_enabled,
                status=u.status,
                avatar_url=u.avatar_url,
                preferences=u.preferences,
                created_at=u.created_at,
                updated_at=u.updated_at,
                last_login_at=u.last_login_at
            )
            for u in mock_users
        ]
        
        total = len(user_responses)
        total_pages = (total + per_page - 1) // per_page
        
        return UserListResponse(
            users=user_responses,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list users: {str(e)}"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: User = Depends(JWTAuthDependency.require_role("admin"))
):
    """Get user by ID (admin only)."""
    try:
        # TODO: Implement actual user retrieval with database
        # For now, return mock user
        
        mock_user = User(
            id=user_id,
            first_name="Mock",
            last_name="User",
            email="mock@example.com",
            role=UserRole.NORMAL,
            account_type=AccountType.CONSUMER,
            status=UserStatus.ACTIVE,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        return UserResponse(
            id=str(mock_user.id),
            first_name=mock_user.first_name,
            last_name=mock_user.last_name,
            email=mock_user.email,
            phone=mock_user.phone,
            postal_code=mock_user.postal_code,
            role=mock_user.role,
            account_type=mock_user.account_type,
            email_verified_at=mock_user.email_verified_at,
            phone_verified_at=mock_user.phone_verified_at,
            two_factor_enabled=mock_user.two_factor_enabled,
            status=mock_user.status,
            avatar_url=mock_user.avatar_url,
            preferences=mock_user.preferences,
            created_at=mock_user.created_at,
            updated_at=mock_user.updated_at,
            last_login_at=mock_user.last_login_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user: {str(e)}"
        )


@router.put("/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: str,
    role_update: UserRoleUpdate,
    current_user: User = Depends(JWTAuthDependency.require_role("admin"))
):
    """Update user role (admin only)."""
    try:
        # TODO: Implement actual user role update with database
        # For now, return mock response
        
        mock_user = User(
            id=user_id,
            first_name="Mock",
            last_name="User",
            email="mock@example.com",
            role=role_update.role,
            account_type=AccountType.CONSUMER,
            status=UserStatus.ACTIVE,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        return UserResponse(
            id=str(mock_user.id),
            first_name=mock_user.first_name,
            last_name=mock_user.last_name,
            email=mock_user.email,
            phone=mock_user.phone,
            postal_code=mock_user.postal_code,
            role=mock_user.role,
            account_type=mock_user.account_type,
            email_verified_at=mock_user.email_verified_at,
            phone_verified_at=mock_user.phone_verified_at,
            two_factor_enabled=mock_user.two_factor_enabled,
            status=mock_user.status,
            avatar_url=mock_user.avatar_url,
            preferences=mock_user.preferences,
            created_at=mock_user.created_at,
            updated_at=mock_user.updated_at,
            last_login_at=mock_user.last_login_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user role: {str(e)}"
        )


@router.put("/{user_id}/status", response_model=UserResponse)
async def update_user_status(
    user_id: str,
    status_update: UserStatusUpdate,
    current_user: User = Depends(JWTAuthDependency.require_role("admin"))
):
    """Update user status (admin only)."""
    try:
        # TODO: Implement actual user status update with database
        # For now, return mock response
        
        mock_user = User(
            id=user_id,
            first_name="Mock",
            last_name="User",
            email="mock@example.com",
            role=UserRole.NORMAL,
            account_type=AccountType.CONSUMER,
            status=status_update.status,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        return UserResponse(
            id=str(mock_user.id),
            first_name=mock_user.first_name,
            last_name=mock_user.last_name,
            email=mock_user.email,
            phone=mock_user.phone,
            postal_code=mock_user.postal_code,
            role=mock_user.role,
            account_type=mock_user.account_type,
            email_verified_at=mock_user.email_verified_at,
            phone_verified_at=mock_user.phone_verified_at,
            two_factor_enabled=mock_user.two_factor_enabled,
            status=mock_user.status,
            avatar_url=mock_user.avatar_url,
            preferences=mock_user.preferences,
            created_at=mock_user.created_at,
            updated_at=mock_user.updated_at,
            last_login_at=mock_user.last_login_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user status: {str(e)}"
        )
