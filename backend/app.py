from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.db.queries import process_and_save_data
from backend.api.routes.news import fetch_news_data
from backend.db.session import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.routes.news import router as news_router
from pathlib import Path 

async def update_news_db(db: AsyncSession):
    # Sync fresh news articles into the local database
    news_data = await fetch_news_data()
    if not news_data:
        return {"message": "No news data found."}
    
    inserted_events = []
    for event in news_data:
        try:
            new_event = await process_and_save_data(db, event, event.get('url'))
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Warm-up tasks: populate DB on startup
    async with AsyncSessionLocal() as db:
        await update_news_db(db)

    yield





app = FastAPI(title="GeoAir API", description="API for GeoAir application", version="1.0.0", lifespan=lifespan)

app.include_router(news_router, prefix="/api")





    

    

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
print(f"DEBUG: Resolving absolute path to: {FRONTEND_DIR}")