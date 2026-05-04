"""Application configuration management"""

from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Database
    database_url: str
    database_echo: bool = False
    
    # News API
    news_api_key: str
    news_api_base_url: str = "https://newsapi.org/v2"
    
    # Application
    app_name: str = "GeoAir API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # News Processing
    news_fetch_keywords: set = {
        "strike", "military", "troop", "withdrawal", "border", "tensions",
        "government", "ministry", "sanctions", "treaty", "ambassador",
        "airlines", "aviation", "airspace", "flight", "faa", "nato", 
        "airport", "missile", "drone"
    }
    news_query: str = "aviation"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "allow"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
