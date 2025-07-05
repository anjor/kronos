from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class CalendarProvider(str, Enum):
    GOOGLE = "google"
    MICROSOFT = "microsoft"
    CALDOTCOM = "caldotcom"


class CalendarBase(BaseModel):
    provider: CalendarProvider
    provider_calendar_id: str
    name: str
    description: Optional[str] = None
    is_primary: bool = False
    is_active: bool = True
    is_master: bool = False


class CalendarCreate(CalendarBase):
    pass


class CalendarUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_primary: Optional[bool] = None
    is_active: Optional[bool] = None


class Calendar(CalendarBase):
    id: int
    user_id: int
    last_sync_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True