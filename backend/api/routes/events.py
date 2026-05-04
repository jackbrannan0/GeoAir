"""News and geopolitical event endpoints"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.services import NewsService
from backend.services.event_service import EventService
from backend.api.dependencies import get_db, get_news_service
from backend.schemas import GeoPoliticalEventOut, NewsProcessResult
from backend.core.logger import logger

router = APIRouter(prefix="/api/v1", tags=["events"])


@router.get("/news/fetch", response_model=NewsProcessResult)
async def fetch_and_process_news(
    db: AsyncSession = Depends(get_db),
    news_service: NewsService = Depends(get_news_service)
):
    """
    Fetch news articles, filter by keywords, and insert into database
    
    Returns:
        NewsProcessResult with processing statistics
    """
    try:
        # Fetch and filter articles
        filtered_articles = await news_service.fetch_and_filter()
        
        # Create events from articles
        event_service = EventService(db)
        created_events, errors = await event_service.bulk_create_events(filtered_articles)
        
        logger.info(f"News processing complete: {len(created_events)} created, {len(errors)} errors")
        
        return NewsProcessResult(
            total_fetched=len(filtered_articles),
            filtered_count=len(filtered_articles),
            inserted_count=len(created_events),
            inserted_events=[GeoPoliticalEventOut.model_validate(e) for e in created_events],
            errors=errors
        )
        
    except Exception as e:
        logger.error(f"Failed to process news: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events/{event_id}", response_model=GeoPoliticalEventOut)
async def get_event(
    event_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific event by ID"""
    event_service = EventService(db)
    event = await event_service.get_event(event_id)
    
    if not event:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")
    
    return GeoPoliticalEventOut.model_validate(event)


@router.get("/events", response_model=list[GeoPoliticalEventOut])
async def list_events(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all events with pagination"""
    event_service = EventService(db)
    events = await event_service.get_all_events(skip, limit)
    return [GeoPoliticalEventOut.model_validate(e) for e in events]
