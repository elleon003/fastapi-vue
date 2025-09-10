from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from pydantic import BaseModel, EmailStr

from ..database.database import get_db
from ..database.models import AuthProvider, UserSession
from ..users.schemas import UserCreate, UserLogin, Token, MagicLinkRequest, UserResponse
from ..users.service import UserService
from ..users.dependencies import get_current_active_user
from ..core.config import get_settings
from ..core.security import create_access_token
from ..core.rate_limiter import RateLimiter
from .service import AuthService

settings = get_settings()
router = APIRouter()


# Request/Response models
class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class SessionResponse(BaseModel):
    id: int
    device_info: str
    ip_address: str
    created_at: str
    last_used: str
    is_current: bool = False

# OAuth setup
oauth = OAuth()

if settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET:
    oauth.register(
        name='google',
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

if settings.LINKEDIN_CLIENT_ID and settings.LINKEDIN_CLIENT_SECRET:
    oauth.register(
        name='linkedin',
        client_id=settings.LINKEDIN_CLIENT_ID,
        client_secret=settings.LINKEDIN_CLIENT_SECRET,
        access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
        authorize_url='https://www.linkedin.com/oauth/v2/authorization',
        client_kwargs={
            'scope': 'r_liteprofile r_emailaddress'
        }
    )


@router.post("/register", response_model=dict)
async def register(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = UserService.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = UserService.create_user(db=db, user=user)
    
    # Send email verification if email is configured
    if settings.SMTP_HOST and not db_user.is_verified:
        try:
            verification_token = AuthService.create_email_verification_token(db, db_user.id)
            AuthService.send_email_verification(db_user, verification_token)
        except Exception as e:
            # Log email error but don't fail registration
            print(f"Email verification failed: {e}")
    
    return AuthService.generate_tokens(db_user, request, db)


@router.post("/login", response_model=dict)
async def login(user_credentials: UserLogin, request: Request, db: Session = Depends(get_db)):
    # Check rate limiting
    RateLimiter.check_login_rate_limit(db, request)
    
    user = UserService.authenticate_user(
        db, user_credentials.email, user_credentials.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Clear rate limit on successful login
    client_ip = RateLimiter.get_client_ip(request)
    RateLimiter.clear_rate_limit(db, client_ip, "login")
    
    return AuthService.generate_tokens(user, request, db)


@router.post("/magic-link", response_model=dict)
async def request_magic_link(magic_link_request: MagicLinkRequest, request: Request, db: Session = Depends(get_db)):
    # Check rate limiting
    RateLimiter.check_magic_link_rate_limit(db, request)
    
    token = AuthService.create_magic_link_token(db, magic_link_request.email)
    
    # Try to send email if configured
    email_sent = AuthService.send_magic_link_email(magic_link_request.email, token)
    
    if settings.ENVIRONMENT == "development" and not email_sent:
        # In development, return the magic link if email isn't configured
        magic_link_url = f"{settings.FRONTEND_URL}/auth/magic-link?token={token}"
        return {
            "message": "Magic link generated (email not configured)",
            "magic_link": magic_link_url,
            "expires_in_minutes": 15
        }
    elif email_sent:
        return {
            "message": "Magic link sent to your email",
            "expires_in_minutes": 15
        }
    else:
        return {
            "message": "Magic link generated",
            "expires_in_minutes": 15
        }


@router.post("/magic-link/verify", response_model=dict)
async def verify_magic_link(token: str, request: Request, db: Session = Depends(get_db)):
    email = AuthService.verify_magic_link_token(db, token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired magic link token"
        )
    
    # Get or create user
    user = UserService.get_user_by_email(db, email)
    if not user:
        # Create user without password (magic link user)
        user_create = UserCreate(email=email, password="")  # Empty password for magic link users
        user = UserService.create_user(db, user_create)
        user.auth_provider = AuthProvider.MAGIC_LINK
        user.is_verified = True
        db.commit()
    
    return AuthService.generate_tokens(user, request, db)


@router.get("/google")
async def google_login(request: Request):
    if not oauth.google:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Google OAuth not configured"
        )
    
    redirect_uri = f"{request.url_for('google_callback')}"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    if not oauth.google:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Google OAuth not configured"
        )
    
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = await AuthService.get_google_user_info(token.get('access_token'))
        
        user = AuthService.create_or_get_oauth_user(db, user_info, AuthProvider.GOOGLE)
        tokens = AuthService.generate_tokens(user, request, db)
        
        # Redirect to frontend with token
        redirect_url = f"{settings.FRONTEND_URL}/auth/callback?token={tokens['access_token']}"
        return RedirectResponse(url=redirect_url)
        
    except Exception as e:
        error_url = f"{settings.FRONTEND_URL}/auth/error?error=oauth_failed"
        return RedirectResponse(url=error_url)


@router.get("/linkedin")
async def linkedin_login(request: Request):
    if not oauth.linkedin:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="LinkedIn OAuth not configured"
        )
    
    redirect_uri = f"{request.url_for('linkedin_callback')}"
    return await oauth.linkedin.authorize_redirect(request, redirect_uri)


@router.get("/linkedin/callback")
async def linkedin_callback(request: Request, db: Session = Depends(get_db)):
    if not oauth.linkedin:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="LinkedIn OAuth not configured"
        )
    
    try:
        token = await oauth.linkedin.authorize_access_token(request)
        user_info = await AuthService.get_linkedin_user_info(token.get('access_token'))
        
        user = AuthService.create_or_get_oauth_user(db, user_info, AuthProvider.LINKEDIN)
        tokens = AuthService.generate_tokens(user, request, db)
        
        # Redirect to frontend with token
        redirect_url = f"{settings.FRONTEND_URL}/auth/callback?token={tokens['access_token']}"
        return RedirectResponse(url=redirect_url)
        
    except Exception as e:
        error_url = f"{settings.FRONTEND_URL}/auth/error?error=oauth_failed"
        return RedirectResponse(url=error_url)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user = Depends(get_current_active_user)
):
    return current_user


# Password Reset Endpoints
@router.post("/password-reset/request", response_model=dict)
async def request_password_reset(
    reset_request: PasswordResetRequest, 
    request: Request,
    db: Session = Depends(get_db)
):
    """Request password reset email"""
    # Check rate limiting
    RateLimiter.check_password_reset_rate_limit(db, request)
    
    # Create password reset token (this won't fail even if email doesn't exist)
    token = AuthService.create_password_reset_token(db, reset_request.email)
    
    if token:
        # Try to send email
        email_sent = AuthService.send_password_reset_email(reset_request.email, token)
        
        if settings.ENVIRONMENT == "development" and not email_sent:
            # In development, return the reset link if email isn't configured
            reset_url = f"{settings.FRONTEND_URL}/auth/reset-password?token={token}"
            return {
                "message": "Password reset token generated (email not configured)",
                "reset_link": reset_url,
                "expires_in_minutes": 30
            }
    
    # Always return success message to prevent email enumeration
    return {
        "message": "If an account with that email exists, you will receive a password reset email.",
        "expires_in_minutes": 30
    }


@router.post("/password-reset/verify", response_model=dict)
async def verify_password_reset_token(token: str, db: Session = Depends(get_db)):
    """Verify password reset token"""
    user = AuthService.verify_password_reset_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired password reset token"
        )
    
    return {
        "message": "Token is valid",
        "email": user.email
    }


@router.post("/password-reset/confirm", response_model=dict)
async def confirm_password_reset(
    reset_data: PasswordResetConfirm, 
    db: Session = Depends(get_db)
):
    """Complete password reset"""
    success = AuthService.reset_password(db, reset_data.token, reset_data.new_password)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired password reset token"
        )
    
    return {"message": "Password reset successfully"}


# Email Verification Endpoints
@router.post("/verify-email", response_model=dict)
async def verify_email(token: str, db: Session = Depends(get_db)):
    """Verify email address"""
    user = AuthService.verify_email_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired email verification token"
        )
    
    return {
        "message": "Email verified successfully",
        "user": user
    }


@router.post("/resend-verification", response_model=dict)
async def resend_verification_email(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Resend email verification"""
    if current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already verified"
        )
    
    if not settings.SMTP_HOST:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Email service not configured"
        )
    
    verification_token = AuthService.create_email_verification_token(db, current_user.id)
    email_sent = AuthService.send_email_verification(current_user, verification_token)
    
    if not email_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email"
        )
    
    return {"message": "Verification email sent"}


# Session Management Endpoints
@router.get("/sessions", response_model=list[SessionResponse])
async def get_user_sessions(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all active sessions for the current user"""
    sessions = AuthService.get_user_sessions(db, current_user.id)
    
    return [
        SessionResponse(
            id=session.id,
            device_info=session.device_info or "Unknown",
            ip_address=session.ip_address or "Unknown",
            created_at=session.created_at.isoformat(),
            last_used=session.last_used.isoformat(),
            is_current=False  # TODO: Identify current session
        )
        for session in sessions
    ]


@router.delete("/sessions/{session_id}")
async def revoke_session(
    session_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Revoke a specific session"""
    # Get the session to verify it belongs to the current user
    session = db.query(UserSession).filter(
        UserSession.id == session_id,
        UserSession.user_id == current_user.id,
        UserSession.is_active == True
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    AuthService.invalidate_user_session(db, session.token_id)
    return {"message": "Session revoked"}


@router.post("/sessions/revoke-all")
async def revoke_all_sessions(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Revoke all sessions except the current one"""
    # TODO: Get current session ID from JWT token
    count = AuthService.invalidate_all_user_sessions(db, current_user.id)
    
    return {
        "message": f"Revoked {count} sessions",
        "revoked_count": count
    }