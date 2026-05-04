"""Event service for managing geopolitical events"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.db.models import GeoPoliticalEvent
from backend.core.repository import BaseRepository
from backend.core.logger import logger
from backend.core.exceptions import DatabaseError


class EventRepository(BaseRepository[GeoPoliticalEvent]):
    """Repository for GeoPoliticalEvent operations"""
    pass


class EventService:
    """Service for managing geopolitical events"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = EventRepository(db, GeoPoliticalEvent)
    
    async def create_event(self, event_data: dict) -> GeoPoliticalEvent:
        """
        Create a new geopolitical event
        
        Args:
            event_data: Dictionary with event information
            
        Returns:
            Created GeoPoliticalEvent
            
        Raises:
            DatabaseError: If creation fails
        """
        try:
            # Parse published_at if it's a string
            published_at = event_data.get("published_at")
            if isinstance(published_at, str):
                try:
                    published_at = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
                except (ValueError, AttributeError):
                    published_at = datetime.utcnow()
            
            event = GeoPoliticalEvent(
                title=event_data.get("title"),
                description=event_data.get("description", ""),
                published_at=published_at or datetime.utcnow(),
                location=event_data.get("location"),
                outlet=event_data.get("outlet"),
                region=event_data.get("region"),
                url=event_data.get("url")
            )
            
            created = await self.repository.create(event)
            logger.info(f"Created event: {created.id} - {created.title}")
            return created
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to create event: {str(e)}")
            raise DatabaseError(f"Failed to create event: {str(e)}")
    
    async def get_event(self, event_id: int) -> Optional[GeoPoliticalEvent]:
        """Get event by ID"""
        return await self.repository.get_by_id(event_id)
    
    async def get_all_events(self, skip: int = 0, limit: int = 100) -> List[GeoPoliticalEvent]:
        """Get all events with pagination"""
        return await self.repository.get_all(skip, limit)
    
    async def bulk_create_events(self, events_data: List[dict]) -> tuple[List[GeoPoliticalEvent], List[dict]]:
        """
        Create multiple events
        
        Args:
            events_data: List of event data dictionaries
            
        Returns:
            Tuple of (successful_events, errors)
        """
        created_events = []
        errors = []
        
        for event_data in events_data:
            try:
                event = await self.create_event(event_data)
                created_events.append(event)
            except DatabaseError as e:
                errors.append({
                    "title": event_data.get("title"),
                    "error": str(e)
                })
        
        logger.info(f"Bulk created {len(created_events)} events, {len(errors)} errors")
        return created_events, errors
