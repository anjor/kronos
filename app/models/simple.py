from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

# Single base for all models
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    timezone = Column(String, default="UTC")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CalendarProvider(enum.Enum):
    GOOGLE = "google"
    MICROSOFT = "microsoft"
    CALDOTCOM = "caldotcom"


class Calendar(Base):
    __tablename__ = "calendars"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(SQLEnum(CalendarProvider), nullable=False)
    provider_calendar_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    is_primary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_master = Column(Boolean, default=False)  # The one true calendar
    
    # OAuth tokens (encrypted)
    access_token = Column(Text)
    refresh_token = Column(Text)
    token_expires_at = Column(DateTime)
    
    # Sync tracking
    last_sync_at = Column(DateTime)
    last_sync_token = Column(String)
    sync_errors = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    calendar_id = Column(Integer, ForeignKey("calendars.id"), nullable=False)
    provider_event_id = Column(String, nullable=False)
    
    title = Column(String, nullable=False)
    description = Column(Text)
    location = Column(String)
    
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False, index=True)
    timezone = Column(String, default="UTC")
    is_all_day = Column(Boolean, default=False)
    
    # Event metadata
    status = Column(String, default="confirmed")  # confirmed, tentative, cancelled
    visibility = Column(String, default="default")  # default, public, private
    
    # Meeting info
    meeting_url = Column(String)
    meeting_id = Column(String)
    
    # Sync tracking
    last_modified = Column(DateTime)
    etag = Column(String)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)