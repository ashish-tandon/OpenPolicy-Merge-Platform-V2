"""
Simple Authentication - Simplified version for basic functionality.

TODO: Implement proper JWT authentication when the service is stable.
"""

from fastapi import HTTPException, status
from app.models.user import User, UserRole, AccountType, UserStatus
from datetime import datetime


# Current user dependency - simplified for now
async def current_active_user():
    """Simplified current user dependency that returns a Pydantic user model."""
    # TODO: Implement proper JWT authentication
    # For now, return a mock user to get the service running
    from app.api.schemas import UserResponse
    mock_user_response = UserResponse(
        id="mock-user-id",
        first_name="Mock",
        last_name="User",
        email="mock@example.com",
        phone=None,
        postal_code=None,
        role=UserRole.NORMAL,
        account_type=AccountType.CONSUMER,
        email_verified_at=datetime.utcnow(),
        phone_verified_at=None,
        two_factor_enabled=False,
        status=UserStatus.ACTIVE,
        avatar_url=None,
        preferences=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        last_login_at=datetime.utcnow()
    )
    return mock_user_response


# Role-based access control
def require_role(required_role: str):
    """Require a specific role for access."""
    async def role_checker(current_user: User):
        if current_user.role.value != required_role and current_user.role.value != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {required_role} required"
            )
        return current_user
    return role_checker
