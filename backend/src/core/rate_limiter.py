from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request

from ..database.models import RateLimitAttempt
from .config import get_settings

settings = get_settings()


class RateLimiter:
    """Rate limiting service for authentication endpoints"""
    
    @staticmethod
    def get_client_ip(request: Request) -> str:
        """Extract client IP address from request"""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
            
        return request.client.host if request.client else "unknown"
    
    @staticmethod
    def check_rate_limit(
        db: Session,
        identifier: str,
        endpoint: str,
        max_attempts: int,
        window_minutes: int
    ) -> bool:
        """
        Check if the rate limit has been exceeded
        Returns True if within limits, False if exceeded
        """
        window_start = datetime.utcnow() - timedelta(minutes=window_minutes)
        
        # Get existing rate limit record within the window
        rate_limit = db.query(RateLimitAttempt).filter(
            RateLimitAttempt.identifier == identifier,
            RateLimitAttempt.endpoint == endpoint,
            RateLimitAttempt.window_start >= window_start
        ).first()
        
        if not rate_limit:
            # Create new rate limit record
            rate_limit = RateLimitAttempt(
                identifier=identifier,
                endpoint=endpoint,
                attempts=1
            )
            db.add(rate_limit)
            db.commit()
            return True
        
        if rate_limit.attempts >= max_attempts:
            return False
        
        # Increment attempts
        rate_limit.attempts += 1
        rate_limit.updated_at = datetime.utcnow()
        db.commit()
        
        return True
    
    @staticmethod
    def check_login_rate_limit(db: Session, request: Request) -> None:
        """Check rate limit for login attempts"""
        client_ip = RateLimiter.get_client_ip(request)
        
        if not RateLimiter.check_rate_limit(
            db=db,
            identifier=client_ip,
            endpoint="login",
            max_attempts=settings.RATE_LIMIT_LOGIN_ATTEMPTS,
            window_minutes=settings.RATE_LIMIT_WINDOW_MINUTES
        ):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too many login attempts. Please try again in {settings.RATE_LIMIT_WINDOW_MINUTES} minutes."
            )
    
    @staticmethod
    def check_magic_link_rate_limit(db: Session, request: Request) -> None:
        """Check rate limit for magic link requests"""
        client_ip = RateLimiter.get_client_ip(request)
        
        if not RateLimiter.check_rate_limit(
            db=db,
            identifier=client_ip,
            endpoint="magic_link",
            max_attempts=settings.RATE_LIMIT_MAGIC_LINK_ATTEMPTS,
            window_minutes=settings.RATE_LIMIT_MAGIC_LINK_WINDOW_MINUTES
        ):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too many magic link requests. Please try again in {settings.RATE_LIMIT_MAGIC_LINK_WINDOW_MINUTES} minutes."
            )
    
    @staticmethod
    def check_password_reset_rate_limit(db: Session, request: Request) -> None:
        """Check rate limit for password reset requests"""
        client_ip = RateLimiter.get_client_ip(request)
        
        if not RateLimiter.check_rate_limit(
            db=db,
            identifier=client_ip,
            endpoint="password_reset",
            max_attempts=settings.RATE_LIMIT_PASSWORD_RESET_ATTEMPTS,
            window_minutes=settings.RATE_LIMIT_PASSWORD_RESET_WINDOW_MINUTES
        ):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too many password reset requests. Please try again in {settings.RATE_LIMIT_PASSWORD_RESET_WINDOW_MINUTES} minutes."
            )
    
    @staticmethod
    def clear_rate_limit(db: Session, identifier: str, endpoint: str) -> None:
        """Clear rate limit for successful authentication"""
        db.query(RateLimitAttempt).filter(
            RateLimitAttempt.identifier == identifier,
            RateLimitAttempt.endpoint == endpoint
        ).delete()
        db.commit()
    
    @staticmethod
    def cleanup_old_attempts(db: Session) -> None:
        """Clean up old rate limit attempts (run this periodically)"""
        cutoff_time = datetime.utcnow() - timedelta(hours=24)  # Keep for 24 hours
        
        deleted_count = db.query(RateLimitAttempt).filter(
            RateLimitAttempt.created_at < cutoff_time
        ).delete()
        
        db.commit()
        return deleted_count