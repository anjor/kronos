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

# Include routers
from app.api import users, calendars, events, sync

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(calendars.router, prefix="/api/calendars", tags=["calendars"])
app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(sync.router, prefix="/api/sync", tags=["sync"])