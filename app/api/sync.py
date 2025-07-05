from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.simple import Calendar as CalendarModel, Event as EventModel
from app.schemas.calendar import Calendar

router = APIRouter()


@router.post("/master-calendar", response_model=Calendar)
def create_master_calendar(user_id: int, db: Session = Depends(get_db)):
    """Create or designate the master calendar that Cal.com will connect to"""
    
    # Check if master calendar already exists for this user
    existing_master = db.query(CalendarModel).filter(
        CalendarModel.user_id == user_id,
        CalendarModel.is_master == True
    ).first()
    
    if existing_master:
        return existing_master
    
    # Create new master calendar
    master_calendar = CalendarModel(
        user_id=user_id,
        provider="google",  # Default to Google for Cal.com integration
        provider_calendar_id="kronos_master",
        name="Kronos Master Calendar",
        description="Aggregated calendar for Cal.com booking conflicts",
        is_master=True,
        is_active=True
    )
    
    db.add(master_calendar)
    db.commit()
    db.refresh(master_calendar)
    return master_calendar


@router.get("/master-calendar/{user_id}", response_model=Calendar)
def get_master_calendar(user_id: int, db: Session = Depends(get_db)):
    """Get the master calendar for a user"""
    master_calendar = db.query(CalendarModel).filter(
        CalendarModel.user_id == user_id,
        CalendarModel.is_master == True
    ).first()
    
    if not master_calendar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master calendar not found. Create one first."
        )
    
    return master_calendar


@router.post("/sync-to-master/{user_id}")
def sync_to_master_calendar(user_id: int, create_busy_blocks: bool = True, db: Session = Depends(get_db)):
    """Sync all events from source calendars to the master calendar"""
    
    # Get master calendar
    master_calendar = db.query(CalendarModel).filter(
        CalendarModel.user_id == user_id,
        CalendarModel.is_master == True
    ).first()
    
    if not master_calendar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master calendar not found. Create one first."
        )
    
    # Get all source calendars (non-master calendars)
    source_calendars = db.query(CalendarModel).filter(
        CalendarModel.user_id == user_id,
        CalendarModel.is_master == False,
        CalendarModel.is_active == True
    ).all()
    
    # Get all events from source calendars
    source_calendar_ids = [cal.id for cal in source_calendars]
    source_events = db.query(EventModel).filter(
        EventModel.calendar_id.in_(source_calendar_ids)
    ).all()
    
    # Track what we sync
    synced_count = 0
    
    for source_event in source_events:
        # Check if this event is already synced to master calendar
        existing_sync = db.query(EventModel).filter(
            EventModel.calendar_id == master_calendar.id,
            EventModel.provider_event_id == f"sync_{source_event.id}"
        ).first()
        
        if not existing_sync:
            # Create a copy in the master calendar
            master_event = EventModel(
                calendar_id=master_calendar.id,
                provider_event_id=f"sync_{source_event.id}",
                title=f"[{source_event.title}]",  # Mark as synced
                description=f"Synced from {source_event.calendar_id}: {source_event.description or ''}",
                location=source_event.location,
                start_time=source_event.start_time,
                end_time=source_event.end_time,
                timezone=source_event.timezone,
                is_all_day=source_event.is_all_day,
                status=source_event.status
            )
            
            db.add(master_event)
            synced_count += 1
    
    db.commit()
    
    # Optionally create busy blocks on source calendars
    busy_blocks_created = 0
    if create_busy_blocks:
        busy_blocks_created = create_cross_calendar_busy_blocks(user_id, db)
    
    return {
        "message": f"Synced {synced_count} events to master calendar",
        "master_calendar_id": master_calendar.id,
        "source_calendars_count": len(source_calendars),
        "total_events_in_master": db.query(EventModel).filter(
            EventModel.calendar_id == master_calendar.id
        ).count(),
        "busy_blocks_created": busy_blocks_created
    }


@router.post("/sync-from-external/{calendar_id}")
def sync_from_external_calendar(calendar_id: int, db: Session = Depends(get_db)):
    """Placeholder for syncing events FROM external calendars (Google, Outlook, etc.)"""
    
    calendar = db.query(CalendarModel).filter(CalendarModel.id == calendar_id).first()
    if not calendar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calendar not found"
        )
    
    if calendar.is_master:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot sync external events to master calendar directly"
        )
    
    # TODO: Implement actual Google/Microsoft API calls here
    # For now, return placeholder
    
    return {
        "message": f"External sync not yet implemented for {calendar.provider}",
        "calendar_id": calendar_id,
        "provider": calendar.provider,
        "next_steps": "Implement Google/Microsoft Calendar API integration"
    }


@router.get("/sync-status/{user_id}")
def get_sync_status(user_id: int, db: Session = Depends(get_db)):
    """Get overview of sync status for a user"""
    
    # Get all calendars
    all_calendars = db.query(CalendarModel).filter(
        CalendarModel.user_id == user_id
    ).all()
    
    master_calendar = next((cal for cal in all_calendars if cal.is_master), None)
    source_calendars = [cal for cal in all_calendars if not cal.is_master]
    
    # Count events
    master_events_count = 0
    if master_calendar:
        master_events_count = db.query(EventModel).filter(
            EventModel.calendar_id == master_calendar.id
        ).count()
    
    source_events_count = db.query(EventModel).filter(
        EventModel.calendar_id.in_([cal.id for cal in source_calendars])
    ).count()
    
    return {
        "user_id": user_id,
        "master_calendar": {
            "exists": master_calendar is not None,
            "id": master_calendar.id if master_calendar else None,
            "events_count": master_events_count
        },
        "source_calendars": {
            "count": len(source_calendars),
            "calendars": [{"id": cal.id, "name": cal.name, "provider": cal.provider} for cal in source_calendars],
            "total_events": source_events_count
        },
        "last_sync": "Not yet implemented"  # TODO: Add last sync tracking
    }


def create_cross_calendar_busy_blocks(user_id: int, db: Session) -> int:
    """Create 'BUSY' blocks on each source calendar for events from OTHER calendars"""
    
    # Get all calendars for this user
    all_calendars = db.query(CalendarModel).filter(
        CalendarModel.user_id == user_id,
        CalendarModel.is_active == True
    ).all()
    
    source_calendars = [cal for cal in all_calendars if not cal.is_master]
    
    if len(source_calendars) <= 1:
        return 0  # Need at least 2 source calendars for cross-sync
    
    busy_blocks_created = 0
    
    # For each source calendar
    for target_calendar in source_calendars:
        # Get events from ALL OTHER calendars (excluding this one and master)
        other_calendar_ids = [cal.id for cal in source_calendars if cal.id != target_calendar.id]
        
        # Get events from other calendars
        other_events = db.query(EventModel).filter(
            EventModel.calendar_id.in_(other_calendar_ids)
        ).all()
        
        # Create busy blocks on target calendar for each other event
        for other_event in other_events:
            # Check if busy block already exists
            existing_busy = db.query(EventModel).filter(
                EventModel.calendar_id == target_calendar.id,
                EventModel.provider_event_id == f"busy_{other_event.id}"
            ).first()
            
            if not existing_busy:
                # Create busy block
                busy_block = EventModel(
                    calendar_id=target_calendar.id,
                    provider_event_id=f"busy_{other_event.id}",
                    title="BUSY",
                    description=f"Busy due to event in another calendar: {other_event.title}",
                    start_time=other_event.start_time,
                    end_time=other_event.end_time,
                    timezone=other_event.timezone,
                    is_all_day=other_event.is_all_day,
                    status="confirmed",
                    visibility="private"  # Private so it doesn't show details
                )
                
                db.add(busy_block)
                busy_blocks_created += 1
    
    db.commit()
    return busy_blocks_created


@router.post("/create-busy-blocks/{user_id}")
def create_busy_blocks_only(user_id: int, db: Session = Depends(get_db)):
    """Create busy blocks on all source calendars without doing a full sync"""
    
    busy_blocks_created = create_cross_calendar_busy_blocks(user_id, db)
    
    return {
        "message": f"Created {busy_blocks_created} busy blocks across calendars",
        "user_id": user_id,
        "busy_blocks_created": busy_blocks_created
    }


@router.delete("/clear-busy-blocks/{user_id}")
def clear_busy_blocks(user_id: int, db: Session = Depends(get_db)):
    """Clear all busy blocks (events with title 'BUSY') for a user"""
    
    # Get all calendars for this user
    user_calendars = db.query(CalendarModel).filter(
        CalendarModel.user_id == user_id
    ).all()
    
    calendar_ids = [cal.id for cal in user_calendars]
    
    # Delete all busy block events
    deleted_count = db.query(EventModel).filter(
        EventModel.calendar_id.in_(calendar_ids),
        EventModel.title == "BUSY"
    ).delete(synchronize_session=False)
    
    db.commit()
    
    return {
        "message": f"Cleared {deleted_count} busy blocks",
        "user_id": user_id,
        "deleted_count": deleted_count
    }