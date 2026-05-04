"""Core application infrastructure"""

from backend.core.config import settings
from backend.core.exceptions import GeoAirException, NewsAPIError, DatabaseError
from backend.core.logger import logger

__all__ = ["settings", "logger", "GeoAirException", "NewsAPIError", "DatabaseError"]
