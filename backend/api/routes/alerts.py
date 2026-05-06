from backend.db.session import get_db
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter()

@router.get("/map/alerts")
async def fetch_alerts(db: AsyncSession = Depends(get_db)):
    from backend.db.models import MapAlerts
    result = await db.execute(select(MapAlerts).limit(100))
    events = result.scalars().all()
    return [
        {
            "id": event.id,
            "latitude": event.latitude,
            "longitude": event.longitude,
            "location_name": event.location_name,
            "raw_event_id": event.raw_event_id,
            "signals": event.signals
        }
        for event in events
    ]