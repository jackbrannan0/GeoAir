from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.db.queries import process_and_save_data
from backend.api.routes.news import fetch_news_data, run_rss_ingestion
from backend.db.session import AsyncSessionLocal, engine
from backend.db.models import Base
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.routes.news import router as news_router
from backend.api.routes.alerts import router as alerts_router
from pathlib import Path 
from backend.nlp.pipeline import process_data

async def update_db(db: AsyncSession):

    
    await run_rss_ingestion(db)
    print("RSS ingestion completed.")  

    news_data_newsAPI = await fetch_news_data(db)
    print("Fetched news data from NewsAPI.")


    if news_data_newsAPI and isinstance(news_data_newsAPI[0], dict):
        for news in news_data_newsAPI:
            try:
                await process_and_save_data(db, news, news.get('url'))
                print("Data saved to database.")
            except Exception as e:
                print(f"Error inserting NewsAPI article: {e}")


    await process_data(db)  
    print("Processed NLP pipeline.")
    
    await db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        try:
            await update_db(db)
            print("Startup tasks completed successfully.")
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