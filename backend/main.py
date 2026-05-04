from fastapi import FastAPI, HTTPException, Depends
import httpx
#from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from backend.db.models import Base, GeoPoliticalEven
from backend.db.session import get_db
from backend.db.queries import insert_single_event


KEYWORDS = {
                    
                    "strike", "military", "troop", "withdrawal", "border", "tensions",
                    "government", "ministry", "sanctions", "treaty", "ambassador",
                    
                    "airlines", "aviation", "airspace", "flight", "faa", "nato", 
                    "airport", "missile", "drone"
                }





app = FastAPI(title="GeoAir API", description="API for GeoAir application", version="1.0.0")
@app.get("/")
async def read_root(db: AsyncSession = Depends(get_db)):
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
    return {"status": "success", "inserted_events": inserted_events}

@app.get("/news")
async def get_news():
    news_data = await fetch_news_data()
    return news_data



def contains_keywords(text: str) -> bool:
    if not text:
        return False
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in KEYWORDS)







async def fetch_news_data():
    from backend.db.session import api_url
    url = f"https://newsapi.org/v2/everything?q=aviation&language=en&apiKey={api_url}"
    async with httpx.AsyncClient() as client:
        try:
            
            response = await client.get(url)
            print(response.json())
            filtered_articles = []
            for articles in response.json().get("articles", []):
                title = articles.get("title") or "",
                description = articles.get("description") or "",

                combined_text = f"{title} {description}"

                if contains_keywords(combined_text):
                    filtered_articles.append({
                        "title": title,
                        "outlet": articles.get("source", {}).get("name"),
                        "description": description,
                        "url": articles.get("url"),
                        "published_at": articles.get("publishedAt")
                    })
                    
                
            return filtered_articles
        
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"News API error: {str(e)}")