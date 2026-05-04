from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from backend.db.models import GeoPoliticalEvent






async def process_and_save_data(db: AsyncSession, event_data: dict, url: str):


    result = await db.execute(select(GeoPoliticalEvent).where(GeoPoliticalEvent.url == url))
    existing_event = result.scalar_one_or_none()
    if existing_event is None:
        raw_date = event_data.get("published_at")
        if raw_date:
            try:
                event_data["published_at"] = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
            except ValueError:
                event_data["published_at"] = datetime.now(timezone.utc)
        new_event = GeoPoliticalEvent(
            title=event_data.get("title"),
            description=event_data.get("description"),
            published_at=event_data.get("published_at"),
            location=event_data.get("location"),
            outlet=event_data.get("outlet"),
            region=event_data.get("region"),
            url=url
            )
        
        db.add(new_event)
        try:
            await db.commit()
        except Exception as e: 
            await db.rollback()
            raise e   
        return new_event

    else:    
        return existing_event

    























































'''async def insert_single_event(db: AsyncSession, event_data: dict):
    
    raw_date = event_data.get("published_at")
    if raw_date:
        try:
            event_data["published_at"] = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
        except ValueError:
            event_data["published_at"] = datetime.utcnow()
    new_event = GeoPoliticalEvent(
        title=event_data.get("title"),
        description=event_data.get("description"),
        published_at=event_data.get("published_at"),
        location=event_data.get("location"),
        outlet=event_data.get("outlet"),
        region=event_data.get("region"),
        url=event_data.get("url")
    )

    
    db.add(new_event)
    try:
        await db.commit()
    except Exception as e: 
        await db.rollback()
        raise e   
    return new_event  

async def get_event_by_url(db: AsyncSession, url: str):
    result = await db.execute(select(GeoPoliticalEvent).where(GeoPoliticalEvent.url == url))
    return result.scalars.first()
'''