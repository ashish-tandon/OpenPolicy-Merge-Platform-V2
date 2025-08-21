"""
Authentication API endpoints for User Service.

Handles user registration, login, OAuth, and password management.
Based on legacy Open Policy Infra patterns.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from typing import Optional
from datetime import datetime

from app.api.schemas import (
    UserCreate, UserResponse, LoginRequest, OAuthLoginRequest,
    OTPRequest, OTPVerifyRequest, ForgotPasswordRequest, ResetPasswordRequest,
    AuthResponse, OTPResponse, PasswordResetResponse, LogoutResponse
)
from app.auth.jwt_handler import JWTHandler, JWTAuthDependency
from app.auth.oauth_handler import OAuthHandler
from app.auth.mfa_handler import MFAHandler
from app.models.user import User, UserRole, AccountType, UserStatus

router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=AuthResponse)
async def register_user(user_data: UserCreate):
    """Register a new user account."""
    try:
        # TODO: Implement actual user creation with database
        # For now, create a mock user
        
        # Check if user already exists
        # existing_user = await User.get_by_email(user_data.email)
        # if existing_user:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="User with this email already exists"
        #     )
        
        # Create user
        mock_user = User(
            id="mock-user-id",
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            phone=user_data.phone,
            postal_code=user_data.postal_code,
            role=user_data.role,
            account_type=user_data.account_type,
            status=UserStatus.ACTIVE,
            email_verified_at=datetime.utcnow() if user_data.email else None,
            phone_verified_at=datetime.utcnow() if user_data.phone else None
        )
        
        # Generate tokens
        tokens = JWTHandler.create_user_tokens(mock_user)
        
        # Convert to response schema
        user_response = UserResponse(
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
        
        return AuthResponse(
            success=True,
            message="User registered successfully",
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            expires_in=30 * 60,  # 30 minutes
            user=user_response
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register user: {str(e)}"
        )


@router.post("/login", response_model=AuthResponse)
async def login_user(login_data: LoginRequest):
    """Authenticate user with email and password."""
    try:
        # TODO: Implement actual user authentication with database
        # For now, accept any valid email/password combination
        
        # Verify credentials
        # user = await User.authenticate(login_data.email, login_data.password)
        # if not user:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Invalid email or password"
        #     )
        
        # Check if user is active
        # if not user.is_active:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="User account is not active"
        #     )
        
        # Create mock user for now
        mock_user = User(
            id="mock-user-id",
            first_name="Mock",
            last_name="User",
            email=login_data.email,
            role=UserRole.NORMAL,
            account_type=AccountType.CONSUMER,
            status=UserStatus.ACTIVE,
            email_verified_at=datetime.utcnow(),
            last_login_at=datetime.utcnow()
        )
        
        # Generate tokens
        tokens = JWTHandler.create_user_tokens(mock_user)
        
        # Convert to response schema
        user_response = UserResponse(
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
        
        return AuthResponse(
            success=True,
            message="Logged in successfully",
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            expires_in=30 * 60,  # 30 minutes
            user=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.post("/oauth/login", response_model=AuthResponse)
async def oauth_login(oauth_data: OAuthLoginRequest):
    """Authenticate user with OAuth provider."""
    try:
        # Get user info from OAuth provider
        oauth_user_info = await OAuthHandler.get_oauth_user_info(
            oauth_data.provider, 
            oauth_data.token
        )
        
        # TODO: Check if user exists, create if not
        # existing_user = await User.get_by_email(oauth_user_info["email"])
        # if not existing_user:
        #     # Create new user from OAuth info
        #     user = await User.create_from_oauth(oauth_user_info, oauth_data.provider)
        # else:
        #     user = existing_user
        
        # Create mock user for now
        mock_user = User(
            id="mock-oauth-user-id",
            first_name=oauth_user_info.get("given_name", "OAuth"),
            last_name=oauth_user_info.get("family_name", "User"),
            email=oauth_user_info["email"],
            role=UserRole.NORMAL,
            account_type=AccountType.CONSUMER,
            status=UserStatus.ACTIVE,
            email_verified_at=datetime.utcnow() if oauth_user_info.get("email_verified") else None,
            avatar_url=oauth_user_info.get("picture"),
            last_login_at=datetime.utcnow()
        )
        
        # Generate tokens
        tokens = JWTHandler.create_user_tokens(mock_user)
        
        # Convert to response schema
        user_response = UserResponse(
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
        
        return AuthResponse(
            success=True,
            message=f"Logged in successfully with {oauth_data.provider}",
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            expires_in=30 * 60,  # 30 minutes
            user=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth login failed: {str(e)}"
        )


@router.post("/otp/request", response_model=OTPResponse)
async def request_otp(otp_request: OTPRequest):
    """Request an OTP for phone/email verification."""
    try:
        result = await MFAHandler.request_otp(
            otp_request.phone, 
            otp_request.otp_type
        )
        return OTPResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to request OTP: {str(e)}"
        )


@router.post("/otp/verify", response_model=OTPResponse)
async def verify_otp(otp_verify: OTPVerifyRequest):
    """Verify an OTP code."""
    try:
        is_valid = await MFAHandler.verify_otp(
            otp_verify.phone,
            otp_verify.otp,
            otp_verify.otp_type
        )
        
        if is_valid:
            return OTPResponse(
                success=True,
                message="OTP verified successfully",
                otp_sent=False,
                expires_in_minutes=0
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify OTP: {str(e)}"
        )


@router.post("/forgot-password", response_model=OTPResponse)
async def forgot_password(forgot_request: ForgotPasswordRequest):
    """Request password reset OTP."""
    try:
        # TODO: Check if user exists
        # user = await User.get_by_email(forgot_request.email)
        # if not user:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail="User not found"
        #     )
        
        # Send OTP
        result = await MFAHandler.request_otp(
            forgot_request.email, 
            "email"
        )
        
        return OTPResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process forgot password request: {str(e)}"
        )


@router.post("/reset-password", response_model=PasswordResetResponse)
async def reset_password(reset_request: ResetPasswordRequest):
    """Reset password using OTP."""
    try:
        # Verify OTP
        is_valid = await MFAHandler.verify_otp(
            reset_request.email,
            reset_request.otp,
            "email"
        )
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP"
            )
        
        # TODO: Update user password
        # await User.update_password(reset_request.email, reset_request.new_password)
        
        return PasswordResetResponse(
            success=True,
            message="Password reset successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset password: {str(e)}"
        )


@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(refresh_token: str):
    """Refresh access token using refresh token."""
    try:
        new_access_token = JWTHandler.refresh_access_token(refresh_token)
        
        # TODO: Get user info from refresh token
        # For now, return minimal response
        return AuthResponse(
            success=True,
            message="Token refreshed successfully",
            access_token=new_access_token,
            refresh_token=refresh_token,
            expires_in=30 * 60,  # 30 minutes
            user=None  # TODO: Include user info
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to refresh token: {str(e)}"
        )


@router.post("/logout", response_model=LogoutResponse)
async def logout(current_user: User = Depends(JWTAuthDependency.get_current_user)):
    """Logout user and invalidate tokens."""
    try:
        # TODO: Invalidate user sessions
        # await UserSession.invalidate_user_sessions(current_user.id)
        
        return LogoutResponse(
            success=True,
            message="Logged out successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}"
        )
