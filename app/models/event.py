from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON, Table
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base

# Association table for many-to-many relationship between events and clients
event_clients = Table(
    'event_clients',
    Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
    Column('client_id', Integer, ForeignKey('clients.id'), primary_key=True)
)

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
    attendees = Column(JSON)  # Store attendees as JSON
    
    # Recurrence information
    is_recurring = Column(Boolean, default=False)
    recurrence_rule = Column(String)
    recurring_event_id = Column(String)
    
    # Meeting links
    meeting_url = Column(String)
    meeting_id = Column(String)
    
    # Sync tracking
    last_modified = Column(DateTime)
    etag = Column(String)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Simplified - no relationships for now