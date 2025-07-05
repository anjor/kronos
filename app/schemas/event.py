from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: datetime
    end_time: datetime
    timezone: str = "UTC"
    is_all_day: bool = False


class EventCreate(EventBase):
    provider_event_id: str
    calendar_id: int


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    timezone: Optional[str] = None
    is_all_day: Optional[bool] = None


class Event(EventBase):
    id: int
    calendar_id: int
    provider_event_id: str
    status: str
    visibility: str
    attendees: Optional[Dict[str, Any]] = None
    is_recurring: bool
    meeting_url: Optional[str] = None
    meeting_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EventList(BaseModel):
    events: List[Event]
    total: int
    page: int
    size: int