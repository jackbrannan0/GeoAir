from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.db.queries import process_and_save_data
from backend.api.routes.news import fetch_news_data, run_rss_ingestion
from backend.db.session import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.routes.news import router as news_router
from backend.api.routes.alerts import router as alerts_router
from pathlib import Path 
from backend.nlp.pipeline import process_data

async def update_db(db: AsyncSession):
    # Sync fresh news articles into the local database
    news_data_newsAPI = await fetch_news_data(db)
    news_data_rss = await run_rss_ingestion(db)
    if not news_data_newsAPI and not news_data_rss:
        return {"message": "No news data found."}
    
    

    inserted_news = []
    for news in news_data_newsAPI:
        try:
            new_event = await process_and_save_data(db, news, news.get('url'))
            inserted_news.append({
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
            print(f"Error inserting news: {e}")

    for news in news_data_rss:
        try:
            new_event = await process_and_save_data(db, news, news.get('url'))
            inserted_news.append({
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
            print(f"Error inserting RSS news: {e}")        

    await process_data(db)  # Run the NLP pipeline to extract locations and create map alerts
    await db.commit()  # Commit all changes after processing


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Warm-up tasks: populate DB on startup
    async with AsyncSessionLocal() as db:
        try:
            await update_db(db)
        except Exception as e:
            await db.rollback()
            print(f" Startup failed, rolling back: {e}")
    yield





app = FastAPI(title="GeoAir API", description="API for GeoAir application", version="1.0.0", lifespan=lifespan)

app.include_router(news_router, prefix="/api")
app.include_router(alerts_router, prefix="/api")




    

    

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
print(f"DEBUG: Resolving absolute path to: {FRONTEND_DIR}")