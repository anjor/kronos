from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .base import Base

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
    is_master = Column(Boolean, default=False)  # The one true calendar that Cal.com connects to
    
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
    
    # Simplified - no relationships for now