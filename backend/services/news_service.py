"""Service layer package"""

from backend.services.news_service import NewsService
from backend.services.event_service import EventService

__all__ = ["NewsService", "EventService"]
