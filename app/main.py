from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import create_tables
import uvicorn

app = FastAPI(
    title="Kronos Calendar Management System",
    description="Multi-calendar management system for freelancers",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    create_tables()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Kronos Calendar Management System", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "environment": settings.environment}

# Import and include routers
# from app.api import auth, calendars, events, conflicts, availability
# app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
# app.include_router(calendars.router, prefix="/api/calendars", tags=["calendars"])
# app.include_router(events.router, prefix="/api/events", tags=["events"])
# app.include_router(conflicts.router, prefix="/api/conflicts", tags=["conflicts"])
# app.include_router(availability.router, prefix="/api/availability", tags=["availability"])

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )