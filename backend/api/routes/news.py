from backend.db.session import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
import os
import httpx
load_dotenv()
KEYWORDS = {
                    
                    "strike", "military", "troop", "withdrawal", "border", "tensions",
                    "government", "ministry", "sanctions", "treaty", "ambassador",
                    
                    "airlines", "aviation", "airspace", "flight", "faa", "nato", 
                    "airport", "missile", "drone"
                }
router = APIRouter()





def contains_keywords(text: str) -> bool:
    # Basic keyword matching to keep results relevant to aviation/conflict
    if not text:
        return False
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in KEYWORDS)




async def fetch_news_data(db: AsyncSession):
    # Pull from NewsAPI and apply local filtering logic
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q=aviation&language=en&apiKey={api_key}"

    from backend.db.models import GeoPoliticalEvent
    result = await db.execute(select(GeoPoliticalEvent).order_by(GeoPoliticalEvent.published_at.desc()).limit(1))
    event = result.scalars().all()
    if not event:
        print("No events in DB, fetching from NewsAPI...")
        async with httpx.AsyncClient() as client:
            try:
                
                response = await client.get(url)
                response.raise_for_status()
                filtered_articles = []
                for article in response.json().get("articles", []):
                    title = article.get("title") or ""
                    description = article.get("description") or ""

                    combined_text = f"{title} {description}"

                    if contains_keywords(combined_text):
                        filtered_articles.append({
                            "title": title,
                            "outlet": article.get("source", {}).get("name"),
                            "description": description,
                            "url": article.get("url"),
                            "published_at": article.get("publishedAt")
                        })
                        
                    
                return filtered_articles
            
            except httpx.HTTPError as e:
                raise HTTPException(status_code=502, detail=f"News API error: {str(e)}")
    else:   
        print("Events already in DB, skipping NewsAPI fetch.")
        from backend.db.models import GeoPoliticalEvent
        result = await db.execute(select(GeoPoliticalEvent).order_by(GeoPoliticalEvent.published_at.desc()).limit(100))
        events = result.scalars().all()
        return [
            {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "published_at": event.published_at,
                "location": event.location,
                "outlet": event.outlet,
                "region": event.region,
                "url": event.url
            }
            for event in events
        ]      
        
@router.get("/news/db")
async def fetch_news_data_db(db: AsyncSession = Depends(get_db)):
    from backend.db.models import GeoPoliticalEvent
    result = await db.execute(select(GeoPoliticalEvent).order_by(GeoPoliticalEvent.published_at.desc()).limit(100))
    events = result.scalars().all()
    return [
        {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "published_at": event.published_at,
            "location": event.location,
            "outlet": event.outlet,
            "region": event.region,
            "url": event.url
        }
        for event in events
    ]