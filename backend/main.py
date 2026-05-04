from fastapi import FastAPI, HTTPException
import backend.db.engine
import httpx
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from backend.db.models import Base, GeoPoliticalEvent
app = FastAPI(title="GeoAir API", description="API for GeoAir application", version="1.0.0")
@app.get("/")
async def read_root():
    news_data = await fetch_news_data()
    return {"message": f'{news_data}'}

@app.get("/news")
async def get_news():
    news_data = await fetch_news_data()
    return news_data


async def fetch_news_data():
    api_key = backend.db.engine.getenv("NEWS_API_KEY")  # Replace with your actual API key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            list_of_articles = []
            for articles in response.json().get("articles", []):
                list_of_articles.append({
                    "title": articles.get("title"),
                    "outlet": articles.get("source", {}).get("name"),
                    "description": articles.get("description"),
                    "url": articles.get("url"),
                    "published_at": articles.get("publishedAt"),
                    "region": "US"  
                })
            return list_of_articles
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"News API error: {str(e)}")