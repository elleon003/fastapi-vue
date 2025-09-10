# FastAPI + Vue.js Starter Template

A modern full-stack web application template with FastAPI backend and Vue.js 3 frontend, featuring comprehensive authentication, security, and user management.

## Features

### 🔐 Authentication & Security
- **Multiple Login Methods**: Email/password, Google OAuth2, LinkedIn OAuth2, Magic links
- **Password Reset**: Secure token-based password reset via email
- **Email Verification**: Account verification with email confirmation
- **Session Management**: Track and manage user sessions across devices
- **Rate Limiting**: Protection against brute force attacks
- **JWT Tokens**: Secure token-based authentication with session tracking

### 👥 User Management
- **User Roles**: Admin and User roles with permissions
- **Account Security**: Password strength validation, session revocation
- **User Dashboard**: Personal settings and account management
- **Admin Dashboard**: User management and system administration
- **Profile Management**: Update user information and preferences

### 📧 Email System
- **HTML Email Templates**: Professional email templates for all notifications
- **Multiple Providers**: Support for Gmail, SendGrid, Mailgun, and other SMTP services
- **Email Types**: Welcome emails, password resets, magic links, verification emails
- **Development Mode**: Email preview in development without SMTP configuration

### 🎨 Frontend
- **Vue.js 3**: Modern framework with Composition API
- **TypeScript**: Full type safety throughout the application
- **Responsive Design**: Mobile-first responsive interface
- **Modern UI**: Clean, professional interface with Tailwind CSS
- **State Management**: Pinia for reactive state management
- **Route Protection**: Authentication guards and role-based access

### ⚡ Backend
- **FastAPI**: High-performance async Python web framework
- **Database**: SQLite for development, PostgreSQL for production
- **Security**: Comprehensive security features and rate limiting
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Database Migrations**: Alembic for version-controlled database changes
- **Testing Ready**: Built-in testing infrastructure

## Project Structure

```
fastapi-vue/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── auth/           # Authentication logic
│   │   ├── users/          # User management
│   │   ├── core/           # Core configurations
│   │   └── database/       # Database models & config
│   ├── tests/              # Backend tests
│   ├── alembic/            # Database migrations
│   └── requirements.txt
├── frontend/               # Vue.js frontend
│   ├── src/
│   │   ├── api/           # API clients
│   │   ├── components/    # Reusable components
│   │   ├── composables/   # Vue composables
│   │   ├── layouts/       # Page layouts
│   │   ├── router/        # Vue router config
│   │   ├── services/      # Business logic
│   │   ├── store/         # Pinia state management
│   │   ├── views/         # Page components
│   │   └── constants/     # App constants
│   ├── public/            # Static assets
│   └── tests/             # Frontend tests
└── docs/                  # Documentation
```

## Authentication Features

### 🔑 Login Methods
- **Email/Password**: Traditional authentication with password strength validation
- **Google OAuth2**: Sign in with Google account
- **LinkedIn OAuth2**: Sign in with LinkedIn account  
- **Magic Links**: Passwordless authentication via email

### 🛡️ Security Features
- **Rate Limiting**: Configurable limits on login attempts, magic links, and password resets
- **Session Management**: Track user sessions across devices with revocation capabilities
- **Password Reset**: Secure token-based password reset (30-minute expiry)
- **Email Verification**: Account verification with 24-hour token expiry
- **JWT Security**: Session-aware tokens with automatic cleanup

### 📧 Email Notifications
- **Magic Link Emails**: Secure passwordless login links
- **Password Reset**: Professional password reset emails with secure links
- **Email Verification**: Welcome emails with account verification
- **Multiple Providers**: Gmail, SendGrid, Mailgun support out of the box

## Configuration

### Environment Setup

1. **Backend Configuration**:
```bash
cd backend
cp .env.example .env
# Edit .env with your configuration
```

2. **Email Configuration** (Optional but recommended):
```bash
# Gmail SMTP
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="your-email@gmail.com"
SMTP_PASSWORD="your-app-password"
FROM_EMAIL="your-email@gmail.com"

# SendGrid
SMTP_HOST="smtp.sendgrid.net"
SMTP_USER="apikey"
SMTP_PASSWORD="your-sendgrid-api-key"

# Mailgun
SMTP_HOST="smtp.mailgun.org"
SMTP_USER="your-mailgun-username"
SMTP_PASSWORD="your-mailgun-password"
```

3. **OAuth Configuration** (Optional):
```bash
# Google OAuth
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"

# LinkedIn OAuth  
LINKEDIN_CLIENT_ID="your-linkedin-client-id"
LINKEDIN_CLIENT_SECRET="your-linkedin-client-secret"
```

### Database Migrations

After updating your environment configuration:

```bash
cd backend
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Quick Start

### 1. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Setup environment (optional)
cp .env.example .env.local
# Edit .env.local if needed

# Start development server
npm run dev
```

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - Email/password login
- `POST /api/auth/magic-link` - Request magic link
- `POST /api/auth/magic-link/verify` - Verify magic link
- `GET /api/auth/google` - Google OAuth login
- `GET /api/auth/linkedin` - LinkedIn OAuth login
- `GET /api/auth/me` - Get current user

### Password Reset
- `POST /api/auth/password-reset/request` - Request password reset
- `POST /api/auth/password-reset/verify` - Verify reset token
- `POST /api/auth/password-reset/confirm` - Confirm new password

### Email Verification
- `POST /api/auth/verify-email` - Verify email with token
- `POST /api/auth/resend-verification` - Resend verification email

### Session Management
- `GET /api/auth/sessions` - Get user sessions
- `DELETE /api/auth/sessions/{id}` - Revoke specific session
- `POST /api/auth/sessions/revoke-all` - Revoke all other sessions

## Tech Stack

### Backend
- **FastAPI**: High-performance async web framework
- **SQLAlchemy + Alembic**: ORM and database migrations
- **Pydantic**: Data validation and serialization
- **JWT**: Secure token-based authentication
- **OAuth2**: Google and LinkedIn integration
- **SMTP**: Email service integration
- **Rate Limiting**: Built-in security protection

### Frontend
- **Vue.js 3**: Progressive JavaScript framework with Composition API
- **TypeScript**: Static type checking
- **Vite**: Next generation build tool
- **Pinia**: State management library
- **Vue Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API communication

### Database & Infrastructure
- **SQLite**: Development database
- **PostgreSQL**: Production database
- **Docker**: Containerization support
- **Alembic**: Database version control

## Security Features

- **Password Hashing**: Bcrypt with salt
- **Rate Limiting**: Configurable limits on sensitive endpoints
- **Session Management**: Track and revoke user sessions
- **Token Security**: JWT with session tracking and automatic cleanup
- **Email Verification**: Prevent account creation with invalid emails
- **CORS Protection**: Configurable cross-origin request handling
- **Input Validation**: Comprehensive request validation with Pydantic