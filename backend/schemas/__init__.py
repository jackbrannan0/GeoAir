"""Data schemas for API requests and responses"""

from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import Optional


class NewsArticleIn(BaseModel):
    """Input schema for news article"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    url: Optional[HttpUrl] = None
    published_at: Optional[datetime] = None
    outlet: Optional[str] = None


class GeoPoliticalEventCreate(BaseModel):
    """Schema for creating a geopolitical event"""
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    published_at: datetime
    location: Optional[str] = None
    outlet: Optional[str] = None
    region: Optional[str] = None
    url: Optional[str] = None


class GeoPoliticalEventOut(GeoPoliticalEventCreate):
    """Schema for geopolitical event response"""
    id: int
    
    class Config:
        from_attributes = True


class NewsProcessResult(BaseModel):
    """Result of news processing"""
    total_fetched: int
    filtered_count: int
    inserted_count: int
    inserted_events: list[GeoPoliticalEventOut]
    errors: list[dict] = []


class HealthCheck(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: str
    database: str = "connected"
