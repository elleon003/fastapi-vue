# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack web application template using:
- **Backend**: FastAPI with async support, SQLAlchemy ORM, Alembic migrations
- **Frontend**: Vue.js 3 with Composition API, TypeScript, Vite build system
- **Database**: SQLite for development, PostgreSQL for production
- **Authentication**: JWT tokens, OAuth2 (Google, LinkedIn), magic links
- **State Management**: Pinia for Vue.js frontend
- **Styling**: Tailwind CSS with Headless UI components

## Architecture

### Backend Structure (`backend/src/`)
- `main.py` - FastAPI application entry point with CORS and router configuration
- `core/` - Configuration, security utilities, shared dependencies
- `auth/` - Authentication services, JWT handling, OAuth providers
- `users/` - User management, roles, permissions
- `database/` - SQLAlchemy models, database configuration
- `alembic/` - Database migration files

### Frontend Structure (`frontend/src/`)
- `main.ts` - Vue.js application entry point
- `api/` - HTTP clients for backend communication (using axios)
- `store/` - Pinia state management stores
- `composables/` - Vue composables for shared logic
- `router/` - Vue Router configuration with route guards
- `layouts/` - Page layout components (Default, Auth, Dashboard)
- `views/` - Page components organized by feature
- `components/` - Reusable UI components

## Development Commands

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
npm run format       # Format with Prettier
npm run test         # Run Vitest tests
npm run test:ui      # Run tests with UI
```

### Database Management
```bash
cd backend
alembic revision --autogenerate -m "Description"  # Create migration
alembic upgrade head                               # Apply migrations
alembic downgrade -1                              # Rollback last migration
```

### Docker Commands
```bash
docker-compose up --build                    # Development environment
docker-compose --profile production up -d    # Production with Nginx
docker-compose exec backend alembic upgrade head  # Run migrations in container
```

## Testing

- Backend: Use `pytest` (installed in requirements.txt)
- Frontend: Use `npm run test` (Vitest with @vue/test-utils)

## Key Configuration Files

- `backend/.env` - Backend environment variables (copy from .env.example)
- `frontend/.env` - Frontend environment variables (copy from .env.example)
- `docker-compose.yml` - Multi-service containerization
- `backend/alembic.ini` - Database migration configuration

## Authentication Flow

The application uses a comprehensive auth system:
1. JWT tokens stored in HTTP-only cookies
2. Role-based access control (Admin, User roles)
3. OAuth2 integration with Google and LinkedIn
4. Magic link authentication via email
5. Protected routes using Vue Router guards and FastAPI dependencies

## API Structure

- Base URL: `http://localhost:8000` (development)
- Auth endpoints: `/api/auth/*`
- User endpoints: `/api/users/*`
- Health check: `/health`
- API docs: `/docs` (Swagger UI)

## State Management

Frontend uses Pinia stores located in `frontend/src/store/`:
- `auth.ts` - Authentication state, user session management
- Additional stores follow similar patterns for feature-specific state