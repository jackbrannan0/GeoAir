"""Application middleware"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.core.exceptions import GeoAirException
from backend.core.logger import logger
import time


def add_middleware(app: FastAPI):
    """Add middleware to the FastAPI application"""
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure as needed for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Exception handlers
    @app.exception_handler(GeoAirException)
    async def geoair_exception_handler(request: Request, exc: GeoAirException):
        """Handle custom GeoAir exceptions"""
        logger.error(f"GeoAir Exception: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message, "error_type": exc.__class__.__name__}
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions"""
        logger.error(f"Unexpected error: {str(exc)}", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
    
    # Logging middleware for all requests
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Log all HTTP requests and responses"""
        start_time = time.time()
        
        # Log request
        logger.info(f"→ {request.method} {request.url.path}")
        
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            logger.info(f"← {request.method} {request.url.path} {response.status_code} ({duration:.3f}s)")
            return response
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"✗ {request.method} {request.url.path} failed after {duration:.3f}s: {str(e)}")
            raise
