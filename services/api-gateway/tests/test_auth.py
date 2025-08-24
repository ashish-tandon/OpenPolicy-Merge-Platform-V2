"""
Tests for authentication system.

Tests FEAT-014 Authentication System (P0 priority).
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from jose import jwt
from app.core.auth import AuthService, ALGORITHM
from app.core.config import settings
from app.models.users import User
from app.models.auth import Role, Permission, APIKey, user_roles
from app.schemas.auth import UserCreate, TokenPayload
from app.core.exceptions import AuthenticationError, AuthorizationError


class TestAuthService:
    """Test authentication service functionality."""
    
    @pytest.fixture
    def auth_service(self, db_session):
        """Create auth service instance."""
        return AuthService(db_session)
    
    @pytest.fixture
    def test_user(self, db_session):
        """Create a test user."""
        user = User(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            hashed_password="hashed_password",
            is_active=True,
            email_verified=True
        )
        db_session.add(user)
        db_session.commit()
        return user
    
    @pytest.fixture
    def test_role(self, db_session):
        """Create a test role."""
        role = Role(
            name="test_role",
            description="Test role"
        )
        db_session.add(role)
        db_session.commit()
        return role
    
    @pytest.fixture
    def test_permission(self, db_session):
        """Create a test permission."""
        permission = Permission(
            name="test.read",
            resource="test",
            action="read",
            description="Test read permission"
        )
        db_session.add(permission)
        db_session.commit()
        return permission
    
    def test_password_hashing(self, auth_service):
        """Test password hashing and verification."""
        password = "SecurePassword123!"
        
        # Hash password
        hashed = auth_service.hash_password(password)
        assert hashed != password
        assert len(hashed) > 20
        
        # Verify correct password
        assert auth_service.verify_password(password, hashed) is True
        
        # Verify incorrect password
        assert auth_service.verify_password("WrongPassword", hashed) is False
    
    def test_create_access_token(self, auth_service):
        """Test JWT access token creation."""
        user_id = "test-user-id"
        roles = ["user", "admin"]
        permissions = ["read", "write"]
        
        token = auth_service.create_access_token(
            subject=user_id,
            roles=roles,
            permissions=permissions
        )
        
        # Decode token
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        
        assert payload["sub"] == user_id
        assert payload["type"] == "access"
        assert payload["roles"] == roles
        assert payload["permissions"] == permissions
        assert "exp" in payload
        assert "iat" in payload
    
    def test_create_refresh_token(self, auth_service):
        """Test JWT refresh token creation."""
        user_id = "test-user-id"
        
        token = auth_service.create_refresh_token(subject=user_id)
        
        # Decode token
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        
        assert payload["sub"] == user_id
        assert payload["type"] == "refresh"
        assert "exp" in payload
        assert "iat" in payload
    
    def test_decode_token_valid(self, auth_service):
        """Test decoding valid token."""
        user_id = "test-user-id"
        token = auth_service.create_access_token(subject=user_id)
        
        payload = auth_service.decode_token(token)
        
        assert isinstance(payload, TokenPayload)
        assert payload.sub == user_id
        assert payload.type == "access"
    
    def test_decode_token_invalid(self, auth_service):
        """Test decoding invalid token."""
        with pytest.raises(AuthenticationError):
            auth_service.decode_token("invalid_token")
    
    def test_decode_token_expired(self, auth_service):
        """Test decoding expired token."""
        # Create token that expires immediately
        token = auth_service.create_access_token(
            subject="test",
            expires_delta=timedelta(seconds=-1)
        )
        
        with pytest.raises(AuthenticationError):
            auth_service.decode_token(token)
    
    def test_authenticate_user_success(self, auth_service, test_user):
        """Test successful user authentication."""
        # Set up password
        password = "TestPassword123!"
        test_user.hashed_password = auth_service.hash_password(password)
        
        # Authenticate with username
        user = auth_service.authenticate_user(test_user.username, password)
        assert user is not None
        assert user.id == test_user.id
        
        # Authenticate with email
        user = auth_service.authenticate_user(test_user.email, password)
        assert user is not None
        assert user.id == test_user.id
    
    def test_authenticate_user_wrong_password(self, auth_service, test_user):
        """Test authentication with wrong password."""
        test_user.hashed_password = auth_service.hash_password("correct_password")
        
        user = auth_service.authenticate_user(test_user.username, "wrong_password")
        assert user is None
    
    def test_authenticate_user_inactive(self, auth_service, test_user):
        """Test authentication with inactive user."""
        password = "TestPassword123!"
        test_user.hashed_password = auth_service.hash_password(password)
        test_user.is_active = False
        
        with pytest.raises(AuthenticationError, match="User account is disabled"):
            auth_service.authenticate_user(test_user.username, password)
    
    def test_authenticate_user_not_found(self, auth_service):
        """Test authentication with non-existent user."""
        user = auth_service.authenticate_user("nonexistent", "password")
        assert user is None
    
    def test_get_user_permissions(self, auth_service, test_user, test_role, test_permission, db_session):
        """Test getting user permissions."""
        # Set up role with permission
        test_role.permissions = [test_permission]
        test_user.roles = [test_role]
        db_session.commit()
        
        permissions = auth_service.get_user_permissions(test_user)
        
        assert len(permissions) == 1
        assert permissions[0] == "test.read"
    
    def test_get_user_permissions_superuser(self, auth_service, test_user, db_session):
        """Test superuser gets all permissions."""
        # Create superuser role
        superuser_role = Role(name="superuser", description="Superuser")
        test_user.roles = [superuser_role]
        
        # Create multiple permissions
        perm1 = Permission(name="perm1", resource="res1", action="read")
        perm2 = Permission(name="perm2", resource="res2", action="write")
        db_session.add_all([superuser_role, perm1, perm2])
        db_session.commit()
        
        permissions = auth_service.get_user_permissions(test_user)
        
        assert len(permissions) == 2
        assert "perm1" in permissions
        assert "perm2" in permissions
    
    def test_create_user_tokens(self, auth_service, test_user, test_role):
        """Test creating access and refresh tokens for user."""
        test_user.roles = [test_role]
        
        access_token, refresh_token = auth_service.create_user_tokens(test_user)
        
        # Verify access token
        access_payload = auth_service.decode_token(access_token)
        assert access_payload.sub == str(test_user.id)
        assert access_payload.type == "access"
        assert test_role.name in access_payload.roles
        
        # Verify refresh token
        refresh_payload = auth_service.decode_token(refresh_token)
        assert refresh_payload.sub == str(test_user.id)
        assert refresh_payload.type == "refresh"
    
    def test_generate_api_key(self, auth_service):
        """Test API key generation."""
        full_key, key_hash, prefix = auth_service.generate_api_key()
        
        assert full_key.startswith("op_")
        assert len(full_key) > 20
        assert len(key_hash) == 64  # SHA-256 hex digest
        assert prefix.startswith("op_")
        assert full_key.startswith(prefix)
    
    def test_authenticate_api_key_success(self, auth_service, test_user, db_session):
        """Test successful API key authentication."""
        # Generate and store API key
        full_key, key_hash, prefix = auth_service.generate_api_key()
        
        api_key = APIKey(
            name="Test API Key",
            key_hash=key_hash,
            prefix=prefix,
            user_id=test_user.id,
            is_active=True
        )
        db_session.add(api_key)
        db_session.commit()
        
        # Authenticate
        result = auth_service.authenticate_api_key(full_key)
        
        assert result is not None
        assert result.id == api_key.id
        assert result.last_used_at is not None
    
    def test_authenticate_api_key_invalid(self, auth_service):
        """Test authentication with invalid API key."""
        result = auth_service.authenticate_api_key("invalid_key")
        assert result is None
    
    def test_authenticate_api_key_disabled(self, auth_service, test_user, db_session):
        """Test authentication with disabled API key."""
        # Generate and store disabled API key
        full_key, key_hash, prefix = auth_service.generate_api_key()
        
        api_key = APIKey(
            name="Disabled API Key",
            key_hash=key_hash,
            prefix=prefix,
            user_id=test_user.id,
            is_active=False
        )
        db_session.add(api_key)
        db_session.commit()
        
        with pytest.raises(AuthenticationError, match="API key is disabled"):
            auth_service.authenticate_api_key(full_key)
    
    def test_authenticate_api_key_expired(self, auth_service, test_user, db_session):
        """Test authentication with expired API key."""
        # Generate and store expired API key
        full_key, key_hash, prefix = auth_service.generate_api_key()
        
        api_key = APIKey(
            name="Expired API Key",
            key_hash=key_hash,
            prefix=prefix,
            user_id=test_user.id,
            is_active=True,
            expires_at=datetime.utcnow() - timedelta(days=1)
        )
        db_session.add(api_key)
        db_session.commit()
        
        with pytest.raises(AuthenticationError, match="API key has expired"):
            auth_service.authenticate_api_key(full_key)
    
    def test_check_permission(self, auth_service, test_user, test_role, test_permission, db_session):
        """Test permission checking."""
        # Set up role with permission
        test_role.permissions = [test_permission]
        test_user.roles = [test_role]
        db_session.commit()
        
        # Check existing permission
        assert auth_service.check_permission(test_user, "test", "read") is True
        
        # Check non-existing permission
        assert auth_service.check_permission(test_user, "test", "write") is False
        assert auth_service.check_permission(test_user, "other", "read") is False
    
    def test_check_permission_superuser(self, auth_service, test_user, db_session):
        """Test superuser has all permissions."""
        # Create superuser role
        superuser_role = Role(name="superuser", description="Superuser")
        test_user.roles = [superuser_role]
        db_session.commit()
        
        # Check any permission
        assert auth_service.check_permission(test_user, "any", "action") is True
        assert auth_service.check_permission(test_user, "resource", "delete") is True
    
    def test_require_permission(self, auth_service, test_user, test_role, test_permission, db_session):
        """Test requiring permission (raises exception)."""
        # Set up role with permission
        test_role.permissions = [test_permission]
        test_user.roles = [test_role]
        db_session.commit()
        
        # Require existing permission (should not raise)
        auth_service.require_permission(test_user, "test", "read")
        
        # Require non-existing permission (should raise)
        with pytest.raises(AuthorizationError, match="User lacks permission"):
            auth_service.require_permission(test_user, "test", "write")
    
    def test_register_user_success(self, auth_service, db_session):
        """Test successful user registration."""
        user_data = UserCreate(
            email="newuser@example.com",
            username="newuser",
            full_name="New User",
            password="SecurePassword123!"
        )
        
        user = auth_service.register_user(user_data)
        
        assert user.email == user_data.email
        assert user.username == user_data.username
        assert user.full_name == user_data.full_name
        assert auth_service.verify_password(user_data.password, user.hashed_password)
        
        # Check default role assigned
        assert len(user.roles) == 1
        assert user.roles[0].name == "user"
    
    def test_register_user_duplicate_email(self, auth_service, test_user):
        """Test registration with duplicate email."""
        user_data = UserCreate(
            email=test_user.email,  # Duplicate
            username="newusername",
            full_name="New User",
            password="SecurePassword123!"
        )
        
        with pytest.raises(ValueError, match="Email already registered"):
            auth_service.register_user(user_data)
    
    def test_register_user_duplicate_username(self, auth_service, test_user):
        """Test registration with duplicate username."""
        user_data = UserCreate(
            email="newemail@example.com",
            username=test_user.username,  # Duplicate
            full_name="New User",
            password="SecurePassword123!"
        )
        
        with pytest.raises(ValueError, match="Username already taken"):
            auth_service.register_user(user_data)
    
    def test_register_user_with_roles(self, auth_service, test_role, db_session):
        """Test registration with specific roles."""
        user_data = UserCreate(
            email="newuser@example.com",
            username="newuser",
            full_name="New User",
            password="SecurePassword123!"
        )
        
        user = auth_service.register_user(user_data, initial_roles=[test_role.name])
        
        assert len(user.roles) == 1
        assert user.roles[0].name == test_role.name
    
    def test_get_current_user_valid_token(self, auth_service, test_user):
        """Test getting current user from valid token."""
        token = auth_service.create_access_token(subject=str(test_user.id))
        
        user = auth_service.get_current_user(token)
        
        assert user.id == test_user.id
    
    def test_get_current_user_invalid_token(self, auth_service):
        """Test getting current user from invalid token."""
        with pytest.raises(AuthenticationError):
            auth_service.get_current_user("invalid_token")
    
    def test_get_current_user_wrong_token_type(self, auth_service, test_user):
        """Test getting current user from refresh token (wrong type)."""
        token = auth_service.create_refresh_token(subject=str(test_user.id))
        
        with pytest.raises(AuthenticationError, match="Invalid token type"):
            auth_service.get_current_user(token)
    
    def test_get_current_user_not_found(self, auth_service, db_session):
        """Test getting current user when user doesn't exist."""
        # Create token for non-existent user
        token = auth_service.create_access_token(subject="non-existent-id")
        
        with pytest.raises(AuthenticationError, match="User not found"):
            auth_service.get_current_user(token)
    
    def test_get_current_user_inactive(self, auth_service, test_user):
        """Test getting current user when user is inactive."""
        test_user.is_active = False
        token = auth_service.create_access_token(subject=str(test_user.id))
        
        with pytest.raises(AuthenticationError, match="User account is disabled"):
            auth_service.get_current_user(token)
    
    def test_refresh_access_token_valid(self, auth_service, test_user, test_role):
        """Test refreshing access token with valid refresh token."""
        test_user.roles = [test_role]
        refresh_token = auth_service.create_refresh_token(subject=str(test_user.id))
        
        new_access_token = auth_service.refresh_access_token(refresh_token)
        
        # Verify new access token
        payload = auth_service.decode_token(new_access_token)
        assert payload.sub == str(test_user.id)
        assert payload.type == "access"
        assert test_role.name in payload.roles
    
    def test_refresh_access_token_invalid(self, auth_service):
        """Test refreshing with invalid refresh token."""
        with pytest.raises(AuthenticationError):
            auth_service.refresh_access_token("invalid_token")
    
    def test_refresh_access_token_wrong_type(self, auth_service, test_user):
        """Test refreshing with access token instead of refresh token."""
        access_token = auth_service.create_access_token(subject=str(test_user.id))
        
        with pytest.raises(AuthenticationError, match="Invalid token type"):
            auth_service.refresh_access_token(access_token)


class TestAuthenticationEndpoints:
    """Test authentication API endpoints."""
    
    def test_login_success(self, client, db_session):
        """Test successful login."""
        # Create user
        auth_service = AuthService(db_session)
        password = "TestPassword123!"
        user = User(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            hashed_password=auth_service.hash_password(password),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # Login
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": password,
                "remember_me": True
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == user.email
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "nonexistent",
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 401
        assert "Invalid username or password" in response.json()["detail"]
    
    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "full_name": "New User",
                "password": "SecurePassword123!"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert "id" in data
    
    def test_register_weak_password(self, client):
        """Test registration with weak password."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "full_name": "New User",
                "password": "weak"  # Too short, no uppercase, no digits, no special chars
            }
        )
        
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("at least 8 characters" in str(err) for err in errors)
    
    def test_get_current_user(self, client, auth_headers):
        """Test getting current user profile."""
        response = client.get(
            "/api/v1/auth/me",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert "username" in data
        assert "roles" in data
    
    def test_get_current_user_unauthorized(self, client):
        """Test getting current user without authentication."""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == 401


# Fixtures for testing
@pytest.fixture
def auth_headers(db_session):
    """Create authentication headers for testing."""
    auth_service = AuthService(db_session)
    
    # Create test user
    user = User(
        email="authtest@example.com",
        username="authtest",
        full_name="Auth Test User",
        hashed_password=auth_service.hash_password("TestPassword123!"),
        is_active=True
    )
    
    # Create user role
    user_role = db_session.query(Role).filter(Role.name == "user").first()
    if not user_role:
        user_role = Role(name="user", description="Regular user")
        db_session.add(user_role)
    
    user.roles = [user_role]
    db_session.add(user)
    db_session.commit()
    
    # Create access token
    access_token, _ = auth_service.create_user_tokens(user)
    
    return {"Authorization": f"Bearer {access_token}"}