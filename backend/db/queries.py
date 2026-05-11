from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from backend.db.models import GeoPoliticalEvent






async def process_and_save_data(db: AsyncSession, event_data: dict, url: str):


    result = await db.execute(select(GeoPoliticalEvent).where(GeoPoliticalEvent.url == url))
    existing_event = result.scalar_one_or_none()
    if existing_event is None:
        raw_date = event_data.get("published_at")
        if isinstance(raw_date, str):
            try:
                event_data["published_at"] = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
            except ValueError:
                event_data["published_at"] = datetime.now(timezone.utc)
        elif raw_date is None:
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
    






async def load_db(db: AsyncSession): 
    from backend.db.models import GeoPoliticalEvent
    stmt = select(GeoPoliticalEvent).where(GeoPoliticalEvent.processed == False)
    need_processing = await db.execute(stmt)
    return need_processing.scalars().all()

   
    
             


    
async def save_alerts(db: AsyncSession, location_data_list):
    from backend.db.models import MapAlerts
    from backend.geo.geocoder import geocode_location # Ensure this is imported
    
    for item in location_data_list:
        loc_name = item["name"]
        # This returns a list, e.g., [('32.64', '54.56')] or ['23.5, 121.0']
        geo_results = await geocode_location(loc_name)
        
        if not geo_results:
            continue

        for res in geo_results:
            lat, lon = None, None

            # 1. Handle Tuple format: ('51.50', '-0.12')
            if isinstance(res, (tuple, list)) and len(res) >= 2:
                lat, lon = res[0], res[1]
            
            # 2. Handle String format from overrides: '23.5, 121.0'
            elif isinstance(res, str) and "," in res:
                parts = res.split(",")
                lat, lon = parts[0].strip(), parts[1].strip()
            
            # 3. Handle Dictionary format: {"lat": 23.5, "lon": 121.0}
            elif isinstance(res, dict):
                lat, lon = res.get("lat"), res.get("lon")

            if lat and lon:
                new_alert = MapAlerts(
                    raw_event_id=item["event_id"],
                    location_name=loc_name,
                    latitude=float(lat), # Convert string coords to floats
                    longitude=float(lon),
                    signals={"source": "nlp_pipeline"}
                )
                db.add(new_alert)
                print(f"   📍 Staged MapAlert: {loc_name} at {lat}, {lon}")

    try:
        await db.commit()
        print(f"✅ Successfully inserted alerts for {len(location_data_list)} items")
    except Exception as e:
        await db.rollback()
        print(f"❌ Failed to insert map alerts: {e}")
        raise e
    # Note: Removed db.close() as it often causes 'Session is closed' errors 
    # if the session is managed by a FastAPI lifecycle or caller.























































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