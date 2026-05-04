"""Tests for news service"""

import pytest
from unittest.mock import AsyncMock, patch
from backend.services import NewsService
from backend.core.exceptions import NewsAPIError


@pytest.mark.asyncio
async def test_news_service_fetch_articles():
    """Test fetching articles from News API"""
    service = NewsService()
    
    mock_response_data = {
        "articles": [
            {
                "title": "Aviation Safety Alert",
                "description": "NATO military exercise detected",
                "url": "https://example.com/1",
                "source": {"name": "News Agency"},
                "publishedAt": "2026-05-04T10:00:00Z"
            }
        ]
    }
    
    with patch('backend.services.httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = AsyncMock()
        
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        
        articles = await service.fetch_articles()
        assert len(articles) == 1
        assert articles[0]["title"] == "Aviation Safety Alert"


def test_news_service_filter_articles():
    """Test filtering articles by keywords"""
    service = NewsService()
    
    articles = [
        {
            "title": "Aviation Safety",
            "description": "Military exercise",
            "source": {"name": "News"},
            "url": "https://example.com/1",
            "publishedAt": "2026-05-04T10:00:00Z"
        },
        {
            "title": "Weather Report",
            "description": "Sunny day",
            "source": {"name": "Weather"},
            "url": "https://example.com/2",
            "publishedAt": "2026-05-04T10:00:00Z"
        }
    ]
    
    filtered = service.filter_articles(articles)
    assert len(filtered) == 1
    assert filtered[0]["title"] == "Aviation Safety"


def test_contains_keywords():
    """Test keyword detection"""
    service = NewsService()
    
    assert service.contains_keywords("military exercise in the area")
    assert service.contains_keywords("NATO tensions rising")
    assert service.contains_keywords("sunny day") is False
    assert service.contains_keywords("") is False
    assert service.contains_keywords(None) is False
