from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.simple import Calendar as CalendarModel
from app.schemas.calendar import Calendar, CalendarCreate, CalendarUpdate

router = APIRouter()


@router.post("/", response_model=Calendar, status_code=status.HTTP_201_CREATED)
def create_calendar(calendar: CalendarCreate, user_id: int, db: Session = Depends(get_db)):
    """Create a new calendar for a user"""
    # Check if calendar already exists for this user and provider
    existing_calendar = db.query(CalendarModel).filter(
        CalendarModel.user_id == user_id,
        CalendarModel.provider == calendar.provider,
        CalendarModel.provider_calendar_id == calendar.provider_calendar_id
    ).first()
    
    if existing_calendar:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Calendar already exists for this provider"
        )
    
    db_calendar = CalendarModel(**calendar.dict(), user_id=user_id)
    db.add(db_calendar)
    db.commit()
    db.refresh(db_calendar)
    return db_calendar


@router.get("/", response_model=List[Calendar])
def get_calendars(user_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get calendars, optionally filtered by user"""
    query = db.query(CalendarModel)
    if user_id:
        query = query.filter(CalendarModel.user_id == user_id)
    
    calendars = query.offset(skip).limit(limit).all()
    return calendars


@router.get("/{calendar_id}", response_model=Calendar)
def get_calendar(calendar_id: int, db: Session = Depends(get_db)):
    """Get a specific calendar by ID"""
    db_calendar = db.query(CalendarModel).filter(CalendarModel.id == calendar_id).first()
    if not db_calendar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calendar not found"
        )
    return db_calendar


@router.patch("/{calendar_id}", response_model=Calendar)
def update_calendar(calendar_id: int, calendar_update: CalendarUpdate, db: Session = Depends(get_db)):
    """Update a calendar"""
    db_calendar = db.query(CalendarModel).filter(CalendarModel.id == calendar_id).first()
    if not db_calendar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calendar not found"
        )
    
    update_data = calendar_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_calendar, field, value)
    
    db.commit()
    db.refresh(db_calendar)
    return db_calendar


@router.delete("/{calendar_id}")
def delete_calendar(calendar_id: int, db: Session = Depends(get_db)):
    """Delete a calendar"""
    db_calendar = db.query(CalendarModel).filter(CalendarModel.id == calendar_id).first()
    if not db_calendar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calendar not found"
        )
    
    db.delete(db_calendar)
    db.commit()
    return {"message": "Calendar deleted successfully"}


@router.post("/{calendar_id}/sync")
def sync_calendar(calendar_id: int, db: Session = Depends(get_db)):
    """Trigger manual calendar sync"""
    db_calendar = db.query(CalendarModel).filter(CalendarModel.id == calendar_id).first()
    if not db_calendar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calendar not found"
        )
    
    # This would trigger a background task to sync the calendar
    # For now, just return a success message
    return {"message": f"Sync triggered for calendar {calendar_id}", "status": "initiated"}