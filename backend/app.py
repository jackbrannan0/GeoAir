from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from backend.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.queries import insert_single_event
from backend.api.routes.news import fetch_news_data
from fastapi import Depends











app = FastAPI(title="GeoAir API", description="API for GeoAir application", version="1.0.0")


from backend.api.routes.news import router as news_router
app.include_router(news_router, prefix="/api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        update_news_db()
    except Exception as e:
        print(f"Failed to fetch news on startup: {e}")
    yield    
app = FastAPI(lifespan=lifespan)
async def update_news_db(db: AsyncSession = Depends(get_db)):
    news_data = await fetch_news_data()
    if not news_data:
        return {"message": "No news data found."}
    
    inserted_events = []
    for event in news_data:
        try:
            new_event = await insert_single_event(db, event)
            inserted_events.append({
                "id": new_event.id,
                "title": new_event.title,
                "description": new_event.description,
                "published_at": new_event.published_at,
                "location": new_event.location,
                "outlet": new_event.outlet,
                "region": new_event.region,
                "url": new_event.url
            })
        except Exception as e:
            print(f"Error inserting event: {e}")
    

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
print(f"DEBUG: Resolving absolute path to: {FRONTEND_DIR}")