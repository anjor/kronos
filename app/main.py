from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

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

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/app")
async def app_redirect():
    return {
        "message": "Kronos UI is available via Streamlit",
        "instructions": "Run 'streamlit run frontend.py' to access the full application interface",
        "api_docs": "/docs" if settings.debug else "API documentation disabled in production"
    }


# Models will be imported through the API modules

# Include routers
from app.api import users, calendars, events, sync

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(calendars.router, prefix="/api/calendars", tags=["calendars"])
app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(sync.router, prefix="/api/sync", tags=["sync"])