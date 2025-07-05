from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, date

from app.database import get_db
from app.models.simple import Event as EventModel
from app.schemas.event import Event, EventCreate, EventUpdate, EventList

router = APIRouter()


@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """Create a new event"""
    db_event = EventModel(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.get("/", response_model=EventList)
def get_events(
    calendar_id: Optional[int] = Query(None, description="Filter by calendar ID"),
    start_date: Optional[date] = Query(None, description="Filter events after this date"),
    end_date: Optional[date] = Query(None, description="Filter events before this date"),
    skip: int = Query(0, description="Number of events to skip"),
    limit: int = Query(100, description="Maximum number of events to return"),
    db: Session = Depends(get_db)
):
    """Get events with optional filtering"""
    query = db.query(EventModel)
    
    if calendar_id:
        query = query.filter(EventModel.calendar_id == calendar_id)
    
    if start_date:
        query = query.filter(EventModel.start_time >= start_date)
    
    if end_date:
        query = query.filter(EventModel.end_time <= end_date)
    
    total = query.count()
    events = query.offset(skip).limit(limit).all()
    
    return EventList(
        events=events,
        total=total,
        page=skip // limit + 1,
        size=len(events)
    )


@router.get("/{event_id}", response_model=Event)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a specific event by ID"""
    db_event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return db_event


@router.patch("/{event_id}", response_model=Event)
def update_event(event_id: int, event_update: EventUpdate, db: Session = Depends(get_db)):
    """Update an event"""
    db_event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    update_data = event_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event


@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Delete an event"""
    db_event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted successfully"}


@router.get("/conflicts/", response_model=List[Event])
def get_conflicts(
    start_date: Optional[date] = Query(None, description="Check conflicts after this date"),
    end_date: Optional[date] = Query(None, description="Check conflicts before this date"),
    db: Session = Depends(get_db)
):
    """Get events that have scheduling conflicts"""
    query = db.query(EventModel)
    
    if start_date:
        query = query.filter(EventModel.start_time >= start_date)
    
    if end_date:
        query = query.filter(EventModel.end_time <= end_date)
    
    # This is a simplified conflict detection
    # In a real implementation, you'd want more sophisticated logic
    events = query.order_by(EventModel.start_time).all()
    
    conflicts = []
    for i, event in enumerate(events):
        for j, other_event in enumerate(events[i+1:], i+1):
            if (event.start_time < other_event.end_time and 
                event.end_time > other_event.start_time):
                if event not in conflicts:
                    conflicts.append(event)
                if other_event not in conflicts:
                    conflicts.append(other_event)
    
    return conflicts