"""Test configuration and fixtures"""

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from backend.api import create_app
from fastapi.testclient import TestClient


@pytest.fixture
async def db_session():
    """Create a test database session"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    # Create tables
    from backend.db.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session() as session:
        yield session


@pytest.fixture
def client():
    """Create a test client"""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def test_event_data():
    """Sample event data for testing"""
    return {
        "title": "Military Exercise in Region X",
        "description": "NATO military exercise detected",
        "published_at": "2026-05-04T10:00:00Z",
        "location": "Eastern Europe",
        "outlet": "News Agency",
        "region": "Europe",
        "url": "https://example.com/news"
    }
