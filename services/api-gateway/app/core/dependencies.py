"""
FastAPI dependency functions for authentication and authorization.

Implements FEAT-014 Authentication System (P0 priority).
"""

from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.auth import AuthService, get_auth_service
from app.models.users import User
from app.models.auth import APIKey
from app.core.exceptions import AuthenticationError, AuthorizationError
import logging

logger = logging.getLogger(__name__)

# Security schemes
bearer_scheme = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


# Authentication dependencies
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    api_key: Optional[str] = Depends(api_key_header),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get current user if authenticated (optional)."""
    auth_service = get_auth_service(db)
    
    # Try bearer token first
    if credentials:
        try:
            user = auth_service.get_current_user(credentials.credentials)
            return user
        except AuthenticationError:
            pass
    
    # Try API key
    if api_key:
        try:
            api_key_obj = auth_service.authenticate_api_key(api_key)
            if api_key_obj and api_key_obj.user:
                return api_key_obj.user
        except AuthenticationError:
            pass
    
    return None


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    api_key: Optional[str] = Depends(api_key_header),
    db: Session = Depends(get_db)
) -> User:
    """Get current user (required)."""
    user = await get_current_user_optional(credentials, api_key, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


# Authorization dependencies
def require_role(role: str):
    """Require user to have a specific role."""
    async def role_checker(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        if not any(r.name == role for r in current_user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User lacks required role: {role}"
            )
        return current_user
    
    return role_checker


def require_roles(roles: List[str]):
    """Require user to have one of the specified roles."""
    async def roles_checker(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        user_roles = [r.name for r in current_user.roles]
        if not any(role in user_roles for role in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User lacks required roles: {', '.join(roles)}"
            )
        return current_user
    
    return roles_checker


def require_permission(resource: str, action: str):
    """Require user to have specific permission."""
    async def permission_checker(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ) -> User:
        auth_service = get_auth_service(db)
        
        if not auth_service.check_permission(current_user, resource, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User lacks permission: {resource}.{action}"
            )
        
        return current_user
    
    return permission_checker


# Convenience dependencies
require_admin = require_role("admin")
require_superuser = require_role("superuser")
require_moderator = require_roles(["moderator", "admin", "superuser"])


# API Key authentication
async def get_api_key(
    api_key: Optional[str] = Depends(api_key_header),
    db: Session = Depends(get_db)
) -> Optional[APIKey]:
    """Get API key if provided."""
    if not api_key:
        return None
    
    auth_service = get_auth_service(db)
    
    try:
        api_key_obj = auth_service.authenticate_api_key(api_key)
        return api_key_obj
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )


async def require_api_key(
    api_key_obj: Optional[APIKey] = Depends(get_api_key)
) -> APIKey:
    """Require valid API key."""
    if not api_key_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required"
        )
    
    return api_key_obj


def require_api_scope(scope: str):
    """Require API key to have specific scope."""
    async def scope_checker(
        api_key_obj: APIKey = Depends(require_api_key)
    ) -> APIKey:
        if not api_key_obj.has_scope(scope):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"API key lacks required scope: {scope}"
            )
        return api_key_obj
    
    return scope_checker