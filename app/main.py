from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

# Create FastAPI app
app = FastAPI(
    title="Kronos Calendar Management System",
    description="Multi-calendar management system for freelancers",
    version="0.1.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting
from app.middleware.rate_limit import AuthenticatedRateLimitMiddleware
from datetime import timedelta

app.add_middleware(
    AuthenticatedRateLimitMiddleware,
    calls=100,  # 100 requests
    period=timedelta(minutes=1)  # per minute
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Kronos Calendar Management System",
        "version": "0.1.0",
        "docs": "/docs" if settings.debug else "Disabled in production",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Models will be imported through the API modules

# Include API v1 router
from app.api.v1.router import api_router

app.include_router(api_router, prefix="/api/v1")