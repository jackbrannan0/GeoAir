from backend.db.session import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
from datetime import datetime
from time import mktime
import os
import feedparser
import httpx
load_dotenv()
KEYWORDS = {
                    
                    "strike", "military", "troop", "withdrawal", "border", "tensions",
                    "government", "ministry", "sanctions", "treaty", "ambassador",
                    
                    "airlines", "aviation", "airspace", "flight", "faa", "nato", 
                    "airport", "missile", "drone"
                }



RSS_FEEDS = {
    "BBC": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
}
router = APIRouter()





def contains_keywords(text: str) -> bool:

    if not text:
        return False
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in KEYWORDS)



    
async def run_rss_ingestion(db: AsyncSession):
    from backend.db.queries import process_and_save_data
    inserted_news = []
    for outlet, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        
        for entry in feed.entries:

            combined_text = f"{entry.title} {getattr(entry, 'summary', '')}"
            if not contains_keywords(combined_text):
                continue


            published_dt = datetime.fromtimestamp(mktime(entry.published_parsed))
            
            article_data = {
                "title": entry.title,
                "url": entry.link,
                "description": getattr(entry, 'summary', ""),
                "outlet": outlet,
                "published_at": published_dt
            }
            
            
            new_event = await process_and_save_data(db, article_data, article_data.get('url'))
            print("found rss data")
            inserted_news.append(new_event)

    return inserted_news

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