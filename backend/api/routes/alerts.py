from backend.db.session import get_db
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter()

@router.get("/map/alerts")
async def fetch_alerts(db: AsyncSession = Depends(get_db)):
    from backend.db.models import MapAlerts, GeoPoliticalEvent
    query =  (
        select(MapAlerts, GeoPoliticalEvent.title, GeoPoliticalEvent.description) 
        .join(GeoPoliticalEvent, MapAlerts.raw_event_id == GeoPoliticalEvent.id)
        .limit(100)
        )
    result = await db.execute(query)
    rows = result.all()
    return [
        {
            "id": alert.id,
            "latitude": alert.latitude,
            "longitude": alert.longitude,
            "location_name": alert.location_name,
            "description": description,
            "title": title,
            "signals": alert.signals,
            "sentiment_score": alert.sentiment_score,
            "severity_label": alert.severity_label
        }
        for alert, title, description in rows
    ]