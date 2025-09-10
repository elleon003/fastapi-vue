import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from pathlib import Path
import logging

from .config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending various types of emails"""
    
    def __init__(self):
        self.smtp_server = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.FROM_EMAIL
        self.from_name = settings.FROM_NAME
    
    def _create_smtp_connection(self):
        """Create and authenticate SMTP connection"""
        context = ssl.create_default_context()
        
        if self.smtp_port == 587:
            # TLS connection
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls(context=context)
        else:
            # SSL connection (port 465)
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context)
        
        server.login(self.smtp_user, self.smtp_password)
        return server
    
    def _send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Send email with HTML and optional text content"""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email
            
            # Add text content if provided
            if text_content:
                text_part = MIMEText(text_content, "plain")
                msg.attach(text_part)
            
            # Add HTML content
            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)
            
            # Send email
            with self._create_smtp_connection() as server:
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_magic_link(self, to_email: str, magic_link: str) -> bool:
        """Send magic link email"""
        subject = "Your Magic Link - Sign in to your account"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Magic Link</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px;">
                <div style="text-align: center; padding: 20px 0; border-bottom: 1px solid #eee;">
                    <h1 style="color: #333; margin: 0;">{settings.APP_NAME}</h1>
                </div>
                
                <div style="padding: 30px 20px;">
                    <h2 style="color: #333; margin-bottom: 20px;">Sign in to your account</h2>
                    <p style="color: #666; line-height: 1.6; margin-bottom: 30px;">
                        Click the button below to sign in to your account. This link will expire in 15 minutes.
                    </p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{magic_link}" 
                           style="background-color: #007bff; color: white; padding: 12px 30px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            Sign In
                        </a>
                    </div>
                    
                    <p style="color: #999; font-size: 14px; margin-top: 30px;">
                        If the button doesn't work, copy and paste this link into your browser:<br>
                        <a href="{magic_link}" style="color: #007bff; word-break: break-all;">{magic_link}</a>
                    </p>
                    
                    <p style="color: #999; font-size: 14px; margin-top: 20px;">
                        If you didn't request this email, you can safely ignore it.
                    </p>
                </div>
                
                <div style="text-align: center; padding: 20px; border-top: 1px solid #eee; color: #999; font-size: 12px;">
                    © {settings.APP_NAME}
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Sign in to your account
        
        Click the link below to sign in to your account. This link will expire in 15 minutes.
        
        {magic_link}
        
        If you didn't request this email, you can safely ignore it.
        
        © {settings.APP_NAME}
        """
        
        return self._send_email(to_email, subject, html_content, text_content)
    
    def send_password_reset(self, to_email: str, reset_link: str) -> bool:
        """Send password reset email"""
        subject = "Reset your password"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reset Password</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px;">
                <div style="text-align: center; padding: 20px 0; border-bottom: 1px solid #eee;">
                    <h1 style="color: #333; margin: 0;">{settings.APP_NAME}</h1>
                </div>
                
                <div style="padding: 30px 20px;">
                    <h2 style="color: #333; margin-bottom: 20px;">Reset your password</h2>
                    <p style="color: #666; line-height: 1.6; margin-bottom: 30px;">
                        We received a request to reset your password. Click the button below to create a new password.
                        This link will expire in 30 minutes.
                    </p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_link}" 
                           style="background-color: #dc3545; color: white; padding: 12px 30px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            Reset Password
                        </a>
                    </div>
                    
                    <p style="color: #999; font-size: 14px; margin-top: 30px;">
                        If the button doesn't work, copy and paste this link into your browser:<br>
                        <a href="{reset_link}" style="color: #dc3545; word-break: break-all;">{reset_link}</a>
                    </p>
                    
                    <p style="color: #999; font-size: 14px; margin-top: 20px;">
                        If you didn't request this password reset, you can safely ignore this email.
                    </p>
                </div>
                
                <div style="text-align: center; padding: 20px; border-top: 1px solid #eee; color: #999; font-size: 12px;">
                    © {settings.APP_NAME}
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Reset your password
        
        We received a request to reset your password. Click the link below to create a new password.
        This link will expire in 30 minutes.
        
        {reset_link}
        
        If you didn't request this password reset, you can safely ignore this email.
        
        © {settings.APP_NAME}
        """
        
        return self._send_email(to_email, subject, html_content, text_content)
    
    def send_email_verification(self, to_email: str, verification_link: str, user_name: Optional[str] = None) -> bool:
        """Send email verification email"""
        subject = "Verify your email address"
        greeting = f"Hi {user_name}," if user_name else "Hi,"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verify Email</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px;">
                <div style="text-align: center; padding: 20px 0; border-bottom: 1px solid #eee;">
                    <h1 style="color: #333; margin: 0;">{settings.APP_NAME}</h1>
                </div>
                
                <div style="padding: 30px 20px;">
                    <h2 style="color: #333; margin-bottom: 20px;">Verify your email address</h2>
                    <p style="color: #666; line-height: 1.6; margin-bottom: 20px;">{greeting}</p>
                    <p style="color: #666; line-height: 1.6; margin-bottom: 30px;">
                        Thanks for signing up! Please verify your email address by clicking the button below.
                        This link will expire in 24 hours.
                    </p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{verification_link}" 
                           style="background-color: #28a745; color: white; padding: 12px 30px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            Verify Email
                        </a>
                    </div>
                    
                    <p style="color: #999; font-size: 14px; margin-top: 30px;">
                        If the button doesn't work, copy and paste this link into your browser:<br>
                        <a href="{verification_link}" style="color: #28a745; word-break: break-all;">{verification_link}</a>
                    </p>
                    
                    <p style="color: #999; font-size: 14px; margin-top: 20px;">
                        If you didn't create an account, you can safely ignore this email.
                    </p>
                </div>
                
                <div style="text-align: center; padding: 20px; border-top: 1px solid #eee; color: #999; font-size: 12px;">
                    © {settings.APP_NAME}
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Verify your email address
        
        {greeting}
        
        Thanks for signing up! Please verify your email address by clicking the link below.
        This link will expire in 24 hours.
        
        {verification_link}
        
        If you didn't create an account, you can safely ignore this email.
        
        © {settings.APP_NAME}
        """
        
        return self._send_email(to_email, subject, html_content, text_content)


# Global email service instance
email_service = EmailService()