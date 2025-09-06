# FastAPI + Vue.js Starter Template

A modern full-stack web application template with FastAPI backend and Vue.js 3 frontend, featuring comprehensive authentication and user management.

## Features

### Authentication
- Email & Password authentication
- Google OAuth2 integration
- LinkedIn OAuth2 integration  
- Magic link authentication
- JWT token-based sessions

### User Management
- User roles (Admin, User)
- Role-based permissions
- User dashboard with settings
- Admin dashboard

### Frontend
- Vue.js 3 with Composition API
- Modern tooling (Vite, TypeScript)
- Responsive design
- Component library integration

### Backend
- FastAPI with async support
- SQLite for development
- PostgreSQL for production
- Alembic database migrations
- Comprehensive API documentation

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

## Development Phases

### Phase 1: Core Setup
- [ ] Backend structure with FastAPI
- [ ] Database configuration (SQLite/PostgreSQL)
- [ ] Frontend structure with Vue 3
- [ ] Basic authentication (email/password)

### Phase 2: Enhanced Authentication  
- [ ] OAuth integrations (Google, LinkedIn)
- [ ] Magic link authentication
- [ ] User roles and permissions

### Phase 3: User Interface
- [ ] Public home page
- [ ] Login/registration pages
- [ ] User dashboard
- [ ] Admin dashboard

### Phase 4: Production Ready
- [ ] Environment configuration
- [ ] Testing setup
- [ ] Deployment documentation
- [ ] Security hardening

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Tech Stack

**Backend:**
- FastAPI
- SQLAlchemy + Alembic
- Pydantic
- JWT authentication
- OAuth2 providers

**Frontend:**
- Vue.js 3
- TypeScript
- Vite
- Pinia (state management)
- Vue Router
- Tailwind CSS

**Database:**
- SQLite (development)
- PostgreSQL (production)