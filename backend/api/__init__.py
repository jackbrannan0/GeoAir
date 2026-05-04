"""API package"""

from fastapi import FastAPI
from backend.api.routes import health, events

__all__ = ["health", "events"]


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    from backend.core.config import settings
    from backend.core.middleware import add_middleware
    
    app = FastAPI(
        title=settings.app_name,
        description="Real-time predictive alerting system for aviation assets",
        version=settings.app_version,
        debug=settings.debug
    )
    
    # Add middleware
    add_middleware(app)
    
    # Include routers
    app.include_router(health.router)
    app.include_router(events.router)
    
    return app
