from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class ConflictType(enum.Enum):
    OVERLAP = "overlap"
    BACK_TO_BACK = "back_to_back"
    TRAVEL_TIME = "travel_time"
    DOUBLE_BOOKING = "double_booking"

class ConflictSeverity(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Conflict(Base):
    __tablename__ = "conflicts"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    conflicting_event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    
    conflict_type = Column(SQLEnum(ConflictType), nullable=False)
    severity = Column(SQLEnum(ConflictSeverity), nullable=False)
    
    description = Column(Text)
    suggested_resolution = Column(Text)
    
    # Resolution tracking
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime)
    resolution_notes = Column(Text)
    
    # Time overlap details
    overlap_start = Column(DateTime)
    overlap_end = Column(DateTime)
    overlap_duration_minutes = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    event = relationship("Event", foreign_keys=[event_id])
    conflicting_event = relationship("Event", foreign_keys=[conflicting_event_id])