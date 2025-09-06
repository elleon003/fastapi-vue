import secrets
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from authlib.integrations.httpx_client import AsyncOAuth2Client
import httpx

from ..database.models import User, MagicLink, AuthProvider
from ..users.service import UserService
from ..users.schemas import UserCreateOAuth
from ..core.security import create_access_token
from ..core.config import get_settings

settings = get_settings()


class AuthService:
    
    @staticmethod
    def create_magic_link_token(db: Session, email: str) -> str:
        # Delete any existing magic links for this email
        db.query(MagicLink).filter(MagicLink.email == email).delete()
        
        # Generate secure token
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(minutes=15)  # 15 minutes expiry
        
        magic_link = MagicLink(
            email=email,
            token=token,
            expires_at=expires_at
        )
        
        db.add(magic_link)
        db.commit()
        
        return token
    
    @staticmethod
    def verify_magic_link_token(db: Session, token: str) -> Optional[str]:
        magic_link = db.query(MagicLink).filter(
            MagicLink.token == token,
            MagicLink.used == False,
            MagicLink.expires_at > datetime.utcnow()
        ).first()
        
        if not magic_link:
            return None
        
        # Mark as used
        magic_link.used = True
        db.commit()
        
        return magic_link.email
    
    @staticmethod
    async def get_google_user_info(access_token: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to get user info from Google"
                )
            return response.json()
    
    @staticmethod
    async def get_linkedin_user_info(access_token: str) -> dict:
        async with httpx.AsyncClient() as client:
            # Get basic profile
            profile_response = await client.get(
                "https://api.linkedin.com/v2/people/~",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            # Get email
            email_response = await client.get(
                "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if profile_response.status_code != 200 or email_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to get user info from LinkedIn"
                )
            
            profile_data = profile_response.json()
            email_data = email_response.json()
            
            return {
                "id": profile_data.get("id"),
                "firstName": profile_data.get("firstName", {}).get("localized", {}),
                "lastName": profile_data.get("lastName", {}).get("localized", {}),
                "email": email_data.get("elements", [{}])[0].get("handle~", {}).get("emailAddress")
            }
    
    @staticmethod
    def create_or_get_oauth_user(db: Session, user_info: dict, provider: AuthProvider) -> User:
        email = user_info.get("email")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not provided by OAuth provider"
            )
        
        # Check if user already exists
        existing_user = UserService.get_user_by_email(db, email)
        if existing_user:
            return existing_user
        
        # Create new user
        if provider == AuthProvider.GOOGLE:
            user_data = UserCreateOAuth(
                email=email,
                first_name=user_info.get("given_name"),
                last_name=user_info.get("family_name"),
                auth_provider=provider,
                provider_id=user_info.get("id"),
                avatar_url=user_info.get("picture")
            )
        elif provider == AuthProvider.LINKEDIN:
            # LinkedIn names come in different format
            first_names = user_info.get("firstName", {})
            last_names = user_info.get("lastName", {})
            
            first_name = None
            last_name = None
            
            # Extract localized names (usually in English)
            if isinstance(first_names, dict):
                first_name = next(iter(first_names.values()), None)
            if isinstance(last_names, dict):
                last_name = next(iter(last_names.values()), None)
            
            user_data = UserCreateOAuth(
                email=email,
                first_name=first_name,
                last_name=last_name,
                auth_provider=provider,
                provider_id=user_info.get("id")
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported OAuth provider"
            )
        
        return UserService.create_oauth_user(db, user_data)
    
    @staticmethod
    def generate_tokens(user: User) -> dict:
        access_token = create_access_token(subject=user.email)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }