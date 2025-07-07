from fastapi import APIRouter
from app.api.v1 import auth
from app.api import users, calendars, events, sync

api_router = APIRouter()

# Include auth routes
api_router.include_router(auth.router)

# Include existing routes with auth protection
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(calendars.router, prefix="/calendars", tags=["calendars"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(sync.router, prefix="/sync", tags=["sync"])