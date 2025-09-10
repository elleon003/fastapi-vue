import secrets
import uuid
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request
from authlib.integrations.httpx_client import AsyncOAuth2Client
import httpx

from ..database.models import (
    User, MagicLink, AuthProvider, PasswordResetToken, 
    EmailVerificationToken, UserSession
)
from ..users.service import UserService
from ..users.schemas import UserCreateOAuth, UserResponse
from ..core.security import create_access_token, get_password_hash
from ..core.config import get_settings
from ..core.email import email_service

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
    def create_password_reset_token(db: Session, email: str) -> Optional[str]:
        """Create password reset token for user"""
        user = UserService.get_user_by_email(db, email)
        if not user:
            # Don't reveal if email exists or not
            return None
        
        # Delete any existing password reset tokens for this user
        db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id
        ).delete()
        
        # Generate secure token
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(minutes=30)  # 30 minutes expiry
        
        reset_token = PasswordResetToken(
            user_id=user.id,
            token=token,
            expires_at=expires_at
        )
        
        db.add(reset_token)
        db.commit()
        
        return token
    
    @staticmethod
    def verify_password_reset_token(db: Session, token: str) -> Optional[User]:
        """Verify password reset token and return user"""
        reset_token = db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token,
            PasswordResetToken.used == False,
            PasswordResetToken.expires_at > datetime.utcnow()
        ).first()
        
        if not reset_token:
            return None
        
        return reset_token.user
    
    @staticmethod
    def reset_password(db: Session, token: str, new_password: str) -> bool:
        """Reset user password using token"""
        reset_token = db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token,
            PasswordResetToken.used == False,
            PasswordResetToken.expires_at > datetime.utcnow()
        ).first()
        
        if not reset_token:
            return False
        
        # Update user password
        user = reset_token.user
        user.hashed_password = get_password_hash(new_password)
        
        # Mark token as used
        reset_token.used = True
        
        # Invalidate all existing sessions for security
        db.query(UserSession).filter(
            UserSession.user_id == user.id,
            UserSession.is_active == True
        ).update({"is_active": False})
        
        db.commit()
        return True
    
    @staticmethod
    def create_email_verification_token(db: Session, user_id: int) -> str:
        """Create email verification token"""
        # Delete any existing verification tokens for this user
        db.query(EmailVerificationToken).filter(
            EmailVerificationToken.user_id == user_id
        ).delete()
        
        # Generate secure token
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=24)  # 24 hours expiry
        
        verification_token = EmailVerificationToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        
        db.add(verification_token)
        db.commit()
        
        return token
    
    @staticmethod
    def verify_email_token(db: Session, token: str) -> Optional[User]:
        """Verify email verification token"""
        verification_token = db.query(EmailVerificationToken).filter(
            EmailVerificationToken.token == token,
            EmailVerificationToken.used == False,
            EmailVerificationToken.expires_at > datetime.utcnow()
        ).first()
        
        if not verification_token:
            return None
        
        # Mark user as verified
        user = verification_token.user
        user.is_verified = True
        
        # Mark token as used
        verification_token.used = True
        
        db.commit()
        return user
    
    @staticmethod
    def create_user_session(db: Session, user: User, request: Request) -> str:
        """Create user session record"""
        token_id = str(uuid.uuid4())
        device_info = request.headers.get("User-Agent", "Unknown")
        ip_address = request.client.host if request.client else "unknown"
        
        session = UserSession(
            user_id=user.id,
            token_id=token_id,
            device_info=device_info,
            ip_address=ip_address,
            expires_at=datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        db.add(session)
        db.commit()
        
        return token_id
    
    @staticmethod
    def invalidate_user_session(db: Session, token_id: str) -> bool:
        """Invalidate a specific user session"""
        session = db.query(UserSession).filter(
            UserSession.token_id == token_id,
            UserSession.is_active == True
        ).first()
        
        if session:
            session.is_active = False
            db.commit()
            return True
        
        return False
    
    @staticmethod
    def invalidate_all_user_sessions(db: Session, user_id: int, except_token_id: Optional[str] = None) -> int:
        """Invalidate all user sessions except the current one"""
        query = db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True
        )
        
        if except_token_id:
            query = query.filter(UserSession.token_id != except_token_id)
        
        count = query.update({"is_active": False})
        db.commit()
        
        return count
    
    @staticmethod
    def get_user_sessions(db: Session, user_id: int) -> list:
        """Get all active sessions for a user"""
        return db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True,
            UserSession.expires_at > datetime.utcnow()
        ).order_by(UserSession.last_used.desc()).all()
    
    @staticmethod
    def generate_tokens(user: User, request: Optional[Request] = None, db: Optional[Session] = None) -> dict:
        """Generate access token and optionally create session"""
        token_data = {"sub": user.email}
        
        # Add session tracking if request and db are provided
        if request and db:
            token_id = AuthService.create_user_session(db, user, request)
            token_data["session_id"] = token_id
        
        access_token = create_access_token(data=token_data)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse.model_validate(user)
        }
    
    @staticmethod
    def send_magic_link_email(email: str, token: str) -> bool:
        """Send magic link via email"""
        if not settings.SMTP_HOST:
            # Email not configured, skip sending
            return False
        
        magic_link_url = f"{settings.FRONTEND_URL}/auth/magic-link?token={token}"
        return email_service.send_magic_link(email, magic_link_url)
    
    @staticmethod
    def send_password_reset_email(email: str, token: str) -> bool:
        """Send password reset email"""
        if not settings.SMTP_HOST:
            return False
        
        reset_url = f"{settings.FRONTEND_URL}/auth/reset-password?token={token}"
        return email_service.send_password_reset(email, reset_url)
    
    @staticmethod
    def send_email_verification(user: User, token: str) -> bool:
        """Send email verification email"""
        if not settings.SMTP_HOST:
            return False
        
        verification_url = f"{settings.FRONTEND_URL}/auth/verify-email?token={token}"
        user_name = f"{user.first_name} {user.last_name}".strip() if user.first_name or user.last_name else None
        return email_service.send_email_verification(user.email, verification_url, user_name)