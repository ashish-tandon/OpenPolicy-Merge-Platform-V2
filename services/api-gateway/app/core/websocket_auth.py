"""
WebSocket authentication and authorization.

This module provides authentication and authorization for WebSocket connections,
including JWT token validation and user session management.
"""

import logging
from typing import Optional, Dict
from datetime import datetime, timedelta
from fastapi import WebSocket, HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel

from app.config import settings

logger = logging.getLogger(__name__)


class WebSocketAuthConfig(BaseModel):
    """Configuration for WebSocket authentication."""
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    require_auth: bool = True
    allow_anonymous: bool = False


class WebSocketUser(BaseModel):
    """User information for WebSocket connections."""
    user_id: str
    username: str
    email: Optional[str] = None
    roles: list[str] = []
    permissions: list[str] = []
    session_id: Optional[str] = None
    connected_at: datetime
    last_activity: datetime


class WebSocketAuthenticator:
    """Handles WebSocket authentication and authorization."""
    
    def __init__(self, config: WebSocketAuthConfig):
        self.config = config
        self.active_sessions: Dict[str, WebSocketUser] = {}
        self.session_tokens: Dict[str, str] = {}  # session_id -> token
    
    async def authenticate_connection(self, websocket: WebSocket, token: Optional[str] = None) -> Optional[WebSocketUser]:
        """
        Authenticate a WebSocket connection.
        
        Args:
            websocket: The WebSocket connection
            token: JWT token for authentication
            
        Returns:
            WebSocketUser if authenticated, None if anonymous allowed
            
        Raises:
            HTTPException: If authentication fails
        """
        if not self.config.require_auth:
            return None
        
        if not token:
            if self.config.allow_anonymous:
                return None
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication token required"
                )
        
        try:
            # Validate JWT token
            payload = jwt.decode(
                token, 
                self.config.secret_key, 
                algorithms=[self.config.algorithm]
            )
            
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload"
                )
            
            # Check token expiration
            exp = payload.get("exp")
            if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired"
                )
            
            # Create user object
            user = WebSocketUser(
                user_id=user_id,
                username=payload.get("username", user_id),
                email=payload.get("email"),
                roles=payload.get("roles", []),
                permissions=payload.get("permissions", []),
                session_id=payload.get("session_id"),
                connected_at=datetime.utcnow(),
                last_activity=datetime.utcnow()
            )
            
            # Store active session
            self.active_sessions[user_id] = user
            if user.session_id:
                self.session_tokens[user.session_id] = token
            
            logger.info(f"WebSocket authenticated: {user.username} ({user_id})")
            return user
            
        except JWTError as e:
            logger.warning(f"JWT validation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            ) from e
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication failed"
            ) from e
    
    def validate_user_permission(self, user: WebSocketUser, permission: str) -> bool:
        """
        Validate if a user has a specific permission.
        
        Args:
            user: The authenticated user
            permission: Permission to check
            
        Returns:
            True if user has permission, False otherwise
        """
        if not user:
            return False
        
        # Check if user has the required permission
        if permission in user.permissions:
            return True
        
        # Check if user has admin role
        if "admin" in user.roles:
            return True
        
        return False
    
    def validate_user_role(self, user: WebSocketUser, role: str) -> bool:
        """
        Validate if a user has a specific role.
        
        Args:
            user: The authenticated user
            role: Role to check
            
        Returns:
            True if user has role, False otherwise
        """
        if not user:
            return False
        
        return role in user.roles
    
    def update_user_activity(self, user_id: str):
        """Update user's last activity timestamp."""
        if user_id in self.active_sessions:
            self.active_sessions[user_id].last_activity = datetime.utcnow()
    
    def remove_user_session(self, user_id: str):
        """Remove a user's active session."""
        if user_id in self.active_sessions:
            user = self.active_sessions[user_id]
            if user.session_id and user.session_id in self.session_tokens:
                del self.session_tokens[user.session_id]
            del self.active_sessions[user_id]
            logger.info(f"WebSocket session removed: {user.username} ({user_id})")
    
    def get_user_by_id(self, user_id: str) -> Optional[WebSocketUser]:
        """Get user by ID."""
        return self.active_sessions.get(user_id)
    
    def get_user_by_session(self, session_id: str) -> Optional[WebSocketUser]:
        """Get user by session ID."""
        for user in self.active_sessions.values():
            if user.session_id == session_id:
                return user
        return None
    
    def get_active_users(self) -> list[WebSocketUser]:
        """Get list of all active users."""
        return list(self.active_sessions.values())
    
    def get_active_sessions_count(self) -> int:
        """Get count of active sessions."""
        return len(self.active_sessions)
    
    def cleanup_expired_sessions(self, max_idle_minutes: int = 60):
        """Clean up expired user sessions."""
        now = datetime.utcnow()
        expired_users = []
        
        for user_id, user in self.active_sessions.items():
            idle_time = now - user.last_activity
            if idle_time > timedelta(minutes=max_idle_minutes):
                expired_users.append(user_id)
        
        for user_id in expired_users:
            self.remove_user_session(user_id)
        
        if expired_users:
            logger.info(f"Cleaned up {len(expired_users)} expired WebSocket sessions")


class WebSocketAuthMiddleware:
    """Middleware for WebSocket authentication."""
    
    def __init__(self, authenticator: WebSocketAuthenticator):
        self.authenticator = authenticator
    
    async def __call__(self, websocket: WebSocket, call_next):
        """Process WebSocket connection with authentication."""
        try:
            # Extract token from query parameters or headers
            token = None
            
            # Check query parameters first
            if "token" in websocket.query_params:
                token = websocket.query_params["token"]
            
            # Check headers if no token in query params
            elif "authorization" in websocket.headers:
                auth_header = websocket.headers["authorization"]
                if auth_header.startswith("Bearer "):
                    token = auth_header[7:]  # Remove "Bearer " prefix
            
            # Authenticate the connection
            user = await self.authenticator.authenticate_connection(websocket, token)
            
            # Store user in websocket state for later use
            websocket.state.user = user
            
            # Continue with the connection
            return await call_next(websocket)
            
        except HTTPException as e:
            # Send error message and close connection
            await websocket.accept()
            await websocket.send_text(f'{{"error": "authentication_failed", "detail": "{e.detail}"}}')
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None
        except Exception as e:
            logger.error(f"WebSocket authentication error: {e}")
            await websocket.accept()
            await websocket.send_text('{"error": "authentication_error", "detail": "Internal server error"}')
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
            return None


# Default authentication configuration
default_auth_config = WebSocketAuthConfig(
    secret_key=settings.SECRET_KEY,
    algorithm="HS256",
    access_token_expire_minutes=30,
    require_auth=True,
    allow_anonymous=False
)

# Global authenticator instance
websocket_authenticator = WebSocketAuthenticator(default_auth_config)

# Global middleware instance
websocket_auth_middleware = WebSocketAuthMiddleware(websocket_authenticator)


# Utility functions for external use
def get_websocket_user(websocket: WebSocket) -> Optional[WebSocketUser]:
    """Get the authenticated user from a WebSocket connection."""
    return getattr(websocket.state, 'user', None)


def require_websocket_auth(websocket: WebSocket) -> WebSocketUser:
    """Require authentication for a WebSocket connection."""
    user = get_websocket_user(websocket)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return user


def require_websocket_permission(websocket: WebSocket, permission: str) -> WebSocketUser:
    """Require a specific permission for a WebSocket connection."""
    user = require_websocket_auth(websocket)
    if not websocket_authenticator.validate_user_permission(user, permission):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission '{permission}' required"
        )
    return user


def require_websocket_role(websocket: WebSocket, role: str) -> WebSocketUser:
    """Require a specific role for a WebSocket connection."""
    user = require_websocket_auth(websocket)
    if not websocket_authenticator.validate_user_role(user, role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role '{role}' required"
        )
    return user
