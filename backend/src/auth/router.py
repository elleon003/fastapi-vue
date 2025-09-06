from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth

from ..database.database import get_db
from ..database.models import AuthProvider
from ..users.schemas import UserCreate, UserLogin, Token, MagicLinkRequest, UserResponse
from ..users.service import UserService
from ..users.dependencies import get_current_active_user
from ..core.config import get_settings
from ..core.security import create_access_token
from .service import AuthService

settings = get_settings()
router = APIRouter()

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
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = UserService.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = UserService.create_user(db=db, user=user)
    return AuthService.generate_tokens(db_user)


@router.post("/login", response_model=dict)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = UserService.authenticate_user(
        db, user_credentials.email, user_credentials.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return AuthService.generate_tokens(user)


@router.post("/magic-link", response_model=dict)
async def request_magic_link(magic_link_request: MagicLinkRequest, db: Session = Depends(get_db)):
    token = AuthService.create_magic_link_token(db, magic_link_request.email)
    
    # In a real application, you would send this via email
    # For development, we'll return the magic link
    magic_link_url = f"{settings.FRONTEND_URL}/auth/magic-link?token={token}"
    
    if settings.ENVIRONMENT == "development":
        return {
            "message": "Magic link generated",
            "magic_link": magic_link_url,  # Only in development
            "expires_in_minutes": 15
        }
    else:
        # In production, send email and don't return the link
        # TODO: Implement email sending
        return {
            "message": "Magic link sent to your email",
            "expires_in_minutes": 15
        }


@router.post("/magic-link/verify", response_model=dict)
async def verify_magic_link(token: str, db: Session = Depends(get_db)):
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
    
    return AuthService.generate_tokens(user)


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
        tokens = AuthService.generate_tokens(user)
        
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
        tokens = AuthService.generate_tokens(user)
        
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