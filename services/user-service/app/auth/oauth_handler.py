"""
OAuth Authentication Handler for User Service.

Handles Google and GitHub OAuth authentication.
Based on legacy OpenParliament patterns.
"""

import httpx
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from app.config.settings import settings


class OAuthHandler:
    """OAuth authentication handler for external providers."""
    
    @classmethod
    async def verify_google_token(cls, token: str) -> Optional[Dict[str, Any]]:
        """Verify Google ID token and return user information."""
        if not settings.GOOGLE_CLIENT_ID:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Google OAuth not configured"
            )
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Verify the token is for our application
                    if data.get("aud") != settings.GOOGLE_CLIENT_ID:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Google token audience"
                        )
                    
                    # Verify the issuer
                    if data.get("iss") not in ["accounts.google.com", "https://accounts.google.com"]:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Google token issuer"
                        )
                    
                    return {
                        "email": data.get("email"),
                        "email_verified": data.get("email_verified", False),
                        "name": data.get("name"),
                        "given_name": data.get("given_name"),
                        "family_name": data.get("family_name"),
                        "picture": data.get("picture"),
                        "sub": data.get("sub")  # Google's unique user ID
                    }
                else:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid Google token"
                    )
                    
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to verify Google token"
            )
    
    @classmethod
    async def verify_github_token(cls, token: str) -> Optional[Dict[str, Any]]:
        """Verify GitHub access token and return user information."""
        if not settings.GITHUB_CLIENT_ID:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="GitHub OAuth not configured"
            )
        
        try:
            headers = {"Authorization": f"Bearer {token}"}
            
            async with httpx.AsyncClient() as client:
                # Get user information
                response = await client.get(
                    "https://api.github.com/user",
                    headers=headers
                )
                
                if response.status_code == 200:
                    user_data = response.json()
                    
                    # Get user emails
                    emails_response = await client.get(
                        "https://api.github.com/user/emails",
                        headers=headers
                    )
                    
                    emails = []
                    if emails_response.status_code == 200:
                        emails = emails_response.json()
                    
                    # Find primary email
                    primary_email = next(
                        (email["email"] for email in emails if email["primary"]),
                        user_data.get("email")
                    )
                    
                    return {
                        "email": primary_email,
                        "email_verified": True,  # GitHub emails are verified
                        "name": user_data.get("name"),
                        "login": user_data.get("login"),  # GitHub username
                        "avatar_url": user_data.get("avatar_url"),
                        "sub": str(user_data.get("id")),  # GitHub user ID
                        "bio": user_data.get("bio"),
                        "location": user_data.get("location"),
                        "company": user_data.get("company")
                    }
                else:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid GitHub token"
                    )
                    
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to verify GitHub token"
            )
    
    @classmethod
    async def get_oauth_user_info(cls, provider: str, token: str) -> Dict[str, Any]:
        """Get user information from OAuth provider."""
        if provider == "google":
            return await cls.verify_google_token(token)
        elif provider == "github":
            return await cls.verify_github_token(token)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported OAuth provider: {provider}"
            )
    
    @classmethod
    def get_oauth_login_url(cls, provider: str, redirect_uri: str) -> str:
        """Get OAuth login URL for the specified provider."""
        if provider == "google":
            return (
                f"https://accounts.google.com/o/oauth2/v2/auth?"
                f"client_id={settings.GOOGLE_CLIENT_ID}&"
                f"redirect_uri={redirect_uri}&"
                f"scope=openid email profile&"
                f"response_type=code"
            )
        elif provider == "github":
            return (
                f"https://github.com/login/oauth/authorize?"
                f"client_id={settings.GITHUB_CLIENT_ID}&"
                f"redirect_uri={redirect_uri}&"
                f"scope=user:email read:user&"
                f"response_type=code"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported OAuth provider: {provider}"
            )
