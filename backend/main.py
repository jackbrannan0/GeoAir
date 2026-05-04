"""GeoAir API Application Entry Point"""

from backend.api import create_app
from backend.core.logger import logger

# Create the FastAPI application
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting GeoAir API server...")
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )