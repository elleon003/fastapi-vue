from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings
from .database.database import engine, Base
from .auth.router import router as auth_router
from .users.router import router as users_router

settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Vue Starter",
    description="A modern FastAPI + Vue.js starter template with authentication",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users_router.router, prefix="/api/users", tags=["Users"])


@app.get("/")
async def root():
    return {"message": "FastAPI Vue Starter API", "environment": settings.ENVIRONMENT}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}