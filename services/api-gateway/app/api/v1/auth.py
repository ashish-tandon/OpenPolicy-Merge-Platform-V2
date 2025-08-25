"""
Authentication API endpoints.

Implements FEAT-014 Authentication System (P0 priority).
"""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.auth import AuthService, get_auth_service
from app.core.dependencies import (
    get_current_user, 
    get_current_active_user,
    require_admin
)
from app.models.users import User
from app.models.auth import Role, Permission, APIKey
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    TokenRefreshRequest,
    TokenVerifyRequest,
    UserCreate,
    UserResponse,
    UserUpdate,
    UserPasswordReset,
    RoleCreate,
    RoleUpdate,
    RoleResponse,
    PermissionCreate,
    PermissionResponse,
    UserRoleAssignment,
    UserRoleResponse,
    APIKeyCreate,
    APIKeyResponse,
    APIKeyCreateResponse,
    PermissionCheckRequest,
    PermissionCheckResponse,
    SessionResponse
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# Authentication endpoints
@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Authenticate user and return tokens."""
    auth_service = get_auth_service(db)
    
    # Authenticate user
    user = auth_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Create tokens
    access_token, refresh_token = auth_service.create_user_tokens(user)
    
    # Calculate expiration
    access_expires = timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token if login_data.remember_me else None,
        token_type="bearer",
        expires_in=int(access_expires.total_seconds()),
        user=UserResponse.from_orm(user)
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    auth_service = get_auth_service(db)
    
    try:
        user = auth_service.register_user(user_data)
        return UserResponse.from_orm(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: TokenRefreshRequest,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token."""
    auth_service = get_auth_service(db)
    
    try:
        access_token = auth_service.refresh_access_token(refresh_data.refresh_token)
        
        # Get user from refresh token to return user data
        payload = auth_service.decode_token(refresh_data.refresh_token)
        user = db.query(User).filter(User.id == payload.sub).first()
        
        # Calculate expiration
        access_expires = timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_data.refresh_token,
            token_type="bearer",
            expires_in=int(access_expires.total_seconds()),
            user=UserResponse.from_orm(user)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.post("/verify")
async def verify_token(
    verify_data: TokenVerifyRequest,
    db: Session = Depends(get_db)
):
    """Verify if a token is valid."""
    auth_service = get_auth_service(db)
    
    try:
        payload = auth_service.decode_token(verify_data.token)
        return {"valid": True, "user_id": payload.sub, "type": payload.type}
    except Exception:
        return {"valid": False}


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout user (invalidate session if using session storage)."""
    # In a JWT-only system, logout is handled client-side
    # This endpoint can be used for audit logging
    logger.info(f"User {current_user.email} logged out")
    return {"message": "Logged out successfully"}


# User management endpoints
@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user's profile."""
    return UserResponse.from_orm(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile."""
    # Update user fields
    update_data = user_update.dict(exclude_unset=True)
    
    # Handle password update separately
    if "password" in update_data:
        auth_service = get_auth_service(db)
        current_user.hashed_password = auth_service.hash_password(update_data.pop("password"))
    
    # Update other fields
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    current_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(current_user)
    
    return UserResponse.from_orm(current_user)


@router.get("/me/permissions", response_model=list[str])
async def get_current_user_permissions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's permissions."""
    auth_service = get_auth_service(db)
    return auth_service.get_user_permissions(current_user)


@router.get("/session", response_model=SessionResponse)
async def get_session_info(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current session information."""
    auth_service = get_auth_service(db)
    permissions = auth_service.get_user_permissions(current_user)
    
    # Calculate session expiration (approximate based on token creation)
    expires_at = datetime.utcnow() + timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return SessionResponse(
        user=UserResponse.from_orm(current_user),
        permissions=permissions,
        expires_at=expires_at
    )


# Password reset endpoints
@router.post("/password-reset/request")
async def request_password_reset(
    email: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """Request password reset email."""
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        # TODO: Generate reset token and send email
        logger.info(f"Password reset requested for {email}")
    
    # Always return success to avoid user enumeration
    return {"message": "If the email exists, a password reset link has been sent"}


@router.post("/password-reset/confirm")
async def confirm_password_reset(
    reset_data: UserPasswordReset,
    db: Session = Depends(get_db)
):
    """Reset password using token."""
    # TODO: Implement password reset token validation
    return {"message": "Password reset successfully"}


# Role management endpoints (admin only)
@router.get("/roles", response_model=list[RoleResponse])
async def list_roles(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """List all roles."""
    roles = db.query(Role).offset(skip).limit(limit).all()
    return [RoleResponse.from_orm(role) for role in roles]


@router.post("/roles", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new role."""
    # Check if role already exists
    existing_role = db.query(Role).filter(Role.name == role_data.name).first()
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role already exists"
        )
    
    # Create role
    role = Role(
        name=role_data.name,
        description=role_data.description
    )
    
    # Assign permissions
    if role_data.permission_ids:
        permissions = db.query(Permission).filter(
            Permission.id.in_(role_data.permission_ids)
        ).all()
        role.permissions = permissions
    
    db.add(role)
    db.commit()
    db.refresh(role)
    
    return RoleResponse.from_orm(role)


@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: str,
    role_update: RoleUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update a role."""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    if role.is_system:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot modify system roles"
        )
    
    # Update fields
    update_data = role_update.dict(exclude_unset=True)
    
    if "permission_ids" in update_data:
        permission_ids = update_data.pop("permission_ids")
        if permission_ids is not None:
            permissions = db.query(Permission).filter(
                Permission.id.in_(permission_ids)
            ).all()
            role.permissions = permissions
    
    for field, value in update_data.items():
        setattr(role, field, value)
    
    db.commit()
    db.refresh(role)
    
    return RoleResponse.from_orm(role)


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete a role."""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    if role.is_system:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete system roles"
        )
    
    db.delete(role)
    db.commit()


# Permission endpoints (admin only)
@router.get("/permissions", response_model=list[PermissionResponse])
async def list_permissions(
    resource: Optional[str] = None,
    action: Optional[str] = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """List all permissions."""
    query = db.query(Permission)
    
    if resource:
        query = query.filter(Permission.resource == resource)
    if action:
        query = query.filter(Permission.action == action)
    
    permissions = query.all()
    return [PermissionResponse.from_orm(perm) for perm in permissions]


@router.post("/permissions/check", response_model=PermissionCheckResponse)
async def check_permission(
    check_request: PermissionCheckRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Check if a user has a specific permission."""
    auth_service = get_auth_service(db)
    
    user = db.query(User).filter(User.id == check_request.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    allowed = auth_service.check_permission(
        user,
        check_request.resource,
        check_request.action
    )
    
    return PermissionCheckResponse(
        allowed=allowed,
        user_id=check_request.user_id,
        resource=check_request.resource,
        action=check_request.action,
        roles=[role.name for role in user.roles]
    )


# User-Role management endpoints (admin only)
@router.post("/users/{user_id}/roles", response_model=UserRoleResponse)
async def assign_user_roles(
    user_id: str,
    assignment: UserRoleAssignment,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Assign roles to a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get roles
    roles = db.query(Role).filter(Role.id.in_(assignment.role_ids)).all()
    if len(roles) != len(assignment.role_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more roles not found"
        )
    
    # Assign roles
    user.roles = roles
    db.commit()
    db.refresh(user)
    
    return UserRoleResponse(
        user_id=user.id,
        roles=[RoleResponse.from_orm(role) for role in user.roles]
    )


@router.get("/users/{user_id}/roles", response_model=UserRoleResponse)
async def get_user_roles(
    user_id: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get user's roles."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserRoleResponse(
        user_id=user.id,
        roles=[RoleResponse.from_orm(role) for role in user.roles]
    )


# API Key management endpoints
@router.post("/api-keys", response_model=APIKeyCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    key_data: APIKeyCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new API key."""
    auth_service = get_auth_service(db)
    
    # Generate API key
    full_key, key_hash, prefix = auth_service.generate_api_key()
    
    # Create API key object
    api_key = APIKey(
        name=key_data.name,
        key_hash=key_hash,
        prefix=prefix,
        user_id=current_user.id,
        service_name=key_data.service_name,
        scopes=key_data.scopes,
        expires_at=key_data.expires_at,
        created_by=current_user.id
    )
    
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    
    # Return response with the full key (only time it's shown)
    response = APIKeyCreateResponse.from_orm(api_key)
    response.api_key = full_key
    
    return response


@router.get("/api-keys", response_model=list[APIKeyResponse])
async def list_api_keys(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List user's API keys."""
    api_keys = db.query(APIKey).filter(APIKey.user_id == current_user.id).all()
    return [APIKeyResponse.from_orm(key) for key in api_keys]


@router.delete("/api-keys/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(
    key_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete an API key."""
    api_key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.user_id == current_user.id
    ).first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    db.delete(api_key)
    db.commit()
