"""News service for fetching and processing news data"""

from typing import List, Dict, Any
import httpx
from backend.core.config import settings
from backend.core.exceptions import NewsAPIError
from backend.core.logger import logger


class NewsService:
    """Service for fetching and filtering news articles"""
    
    def __init__(self):
        self.api_key = settings.news_api_key
        self.base_url = settings.news_api_base_url
        self.keywords = settings.news_fetch_keywords
        self.query = settings.news_query
    
    def contains_keywords(self, text: str) -> bool:
        """Check if text contains any of the configured keywords"""
        if not text:
            return False
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.keywords)
    
    async def fetch_articles(self) -> List[Dict[str, Any]]:
        """
        Fetch articles from News API
        
        Returns:
            List of article dictionaries
            
        Raises:
            NewsAPIError: If API request fails
        """
        url = f"{self.base_url}/everything?q={self.query}&language=en&apiKey={self.api_key}"
        
        try:
            async with httpx.AsyncClient() as client:
                logger.info(f"Fetching news from {self.query}...")
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                
                data = response.json()
                articles = data.get("articles", [])
                logger.info(f"Fetched {len(articles)} articles from News API")
                
                return articles
                
        except httpx.HTTPStatusError as e:
            logger.error(f"News API HTTP error: {e.status_code} - {e.response.text}")
            raise NewsAPIError(
                f"News API returned status {e.status_code}",
                status_code=e.response.status_code
            )
        except httpx.RequestError as e:
            logger.error(f"News API request error: {str(e)}")
            raise NewsAPIError(f"Failed to fetch news: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching news: {str(e)}")
            raise NewsAPIError(f"Unexpected error: {str(e)}")
    
    def filter_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter articles by keywords
        
        Args:
            articles: List of article dictionaries from News API
            
        Returns:
            List of filtered articles
        """
        filtered = []
        
        for article in articles:
            title = article.get("title") or ""
            description = article.get("description") or ""
            combined_text = f"{title} {description}"
            
            if self.contains_keywords(combined_text):
                filtered.append({
                    "title": title,
                    "outlet": article.get("source", {}).get("name"),
                    "description": description,
                    "url": article.get("url"),
                    "published_at": article.get("publishedAt")
                })
        
        logger.info(f"Filtered {len(filtered)} articles from {len(articles)} total")
        return filtered
    
    async def fetch_and_filter(self) -> List[Dict[str, Any]]:
        """
        Fetch and filter articles in one operation
        
        Returns:
            List of filtered articles
        """
        articles = await self.fetch_articles()
        return self.filter_articles(articles)
