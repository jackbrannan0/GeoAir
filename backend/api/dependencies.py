"""Dependency injection container for API endpoints"""

from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.session import AsyncSessionLocal
from backend.services import NewsService
from backend.services.event_service import EventService


async def get_db() -> AsyncSession:
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        yield session


def get_news_service() -> NewsService:
    """Dependency to get news service"""
    return NewsService()


async def get_event_service(db: AsyncSession = None) -> EventService:
    """Dependency to get event service"""
    if db is None:
        async with AsyncSessionLocal() as session:
            return EventService(session)
    return EventService(db)
