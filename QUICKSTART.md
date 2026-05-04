"""
GeoAir Backend Quick Start Guide

This guide will help you get started with the refactored GeoAir backend.
"""

# ==============================================================================
# 1. SETUP ENVIRONMENT
# ==============================================================================

# 1.1 Create and activate virtual environment
# python -m venv venv
# source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate     # On Windows

# 1.2 Install dependencies
# pip install -r backend/requirements.txt

# 1.3 Create .env file from template
# cp .env.example .env
# Edit .env and fill in your actual values:
#   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/geoair
#   NEWS_API_KEY=your_actual_api_key

# ==============================================================================
# 2. RUNNING THE APPLICATION
# ==============================================================================

# Option 1: Using uvicorn directly
# uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using the main.py script
# python backend/main.py

# Option 3: Development with hot reload
# pip install watchfiles
# uvicorn backend.main:app --reload

# ==============================================================================
# 3. TESTING THE API
# ==============================================================================

# 3.1 Health Check
# curl http://localhost:8000/health
# Expected: {"status":"healthy","version":"1.0.0","database":"connected"}

# 3.2 Status Endpoint
# curl http://localhost:8000/status
# Expected: {"status":"running","app_name":"GeoAir API","version":"1.0.0","debug":false}

# 3.3 Fetch and Process News
# curl http://localhost:8000/api/v1/news/fetch
# This will:
#   - Fetch articles from News API
#   - Filter by geopolitical keywords
#   - Store in database
#   - Return processing results

# 3.4 List Events (paginated)
# curl "http://localhost:8000/api/v1/events?skip=0&limit=10"

# 3.5 Get Specific Event
# curl http://localhost:8000/api/v1/events/1

# ==============================================================================
# 4. RUNNING TESTS
# ==============================================================================

# 4.1 Run all tests
# pytest

# 4.2 Run tests with verbose output
# pytest -v

# 4.3 Run specific test file
# pytest tests/unit/services/test_news_service.py

# 4.4 Run tests with coverage
# pip install pytest-cov
# pytest --cov=backend --cov-report=html

# 4.5 Run only API tests
# pytest tests/unit/api/

# 4.6 Run only service tests
# pytest tests/unit/services/

# ==============================================================================
# 5. ACCESSING API DOCUMENTATION
# ==============================================================================

# The API is self-documenting via FastAPI/Swagger UI
# Open in browser: http://localhost:8000/docs
# Alternative Redoc: http://localhost:8000/redoc

# ==============================================================================
# 6. DEVELOPMENT WORKFLOW
# ==============================================================================

# 6.1 Creating a new service
# 1. Create backend/services/my_service.py
# 2. Implement MyService class with business logic
# 3. Add get_my_service() dependency in backend/api/dependencies.py
# 4. Use in routes with dependency injection

# 6.2 Creating a new route
# 1. Create backend/api/routes/my_feature.py
# 2. Define APIRouter with handlers
# 3. Import and include_router in backend/api/__init__.py create_app()

# 6.3 Adding new schema
# 1. Add Pydantic model to backend/schemas/__init__.py
# 2. Use in route handlers for validation
# 3. Import in relevant routes/services

# 6.4 Error handling
# from backend.core.exceptions import NewsAPIError, DatabaseError
# try:
#     result = await operation()
# except NewsAPIError as e:
#     logger.error(f"News API error: {e.message}")
#     # Middleware automatically converts to HTTP response

# 6.5 Logging
# from backend.core.logger import logger
# logger.info("Starting operation...")
# logger.error(f"Failed: {str(e)}", exc_info=e)

# ==============================================================================
# 7. COMMON ISSUES & SOLUTIONS
# ==============================================================================

# Issue: "DATABASE_URL environment variable not set"
# Solution: Create .env file with DATABASE_URL set

# Issue: "ModuleNotFoundError: No module named 'backend'"
# Solution: Make sure you're running from project root (where pyproject.toml is)

# Issue: "News API key invalid"
# Solution: Verify NEWS_API_KEY in .env is correct

# Issue: Database connection refused
# Solution: Check DATABASE_URL in .env and ensure PostgreSQL is running

# ==============================================================================
# 8. DIRECTORY STRUCTURE REFERENCE
# ==============================================================================

# backend/
#   ├── core/              # Infrastructure (config, exceptions, logger, middleware)
#   ├── services/          # Business logic (NewsService, EventService)
#   ├── schemas/           # Data validation (Pydantic models)
#   ├── api/               # API layer (routes, dependencies, middleware)
#   ├── db/                # Database (models, session, queries)
#   ├── nlp/               # NLP module (placeholder)
#   ├── geo/               # Geospatial module (placeholder)
#   ├── correlation/       # Correlation analysis (placeholder)
#   └── main.py            # Entry point
#
# tests/
#   ├── conftest.py        # Pytest fixtures
#   └── unit/              # Unit tests
#       ├── services/      # Service layer tests
#       └── api/           # API endpoint tests

# ==============================================================================
# 9. USEFUL PYTHON IMPORTS FOR DEVELOPMENT
# ==============================================================================

# # Configuration
# from backend.core.config import settings
#
# # Logging
# from backend.core.logger import logger
#
# # Exceptions
# from backend.core.exceptions import (
#     GeoAirException,
#     NewsAPIError,
#     DatabaseError,
#     ValidationError,
#     ResourceNotFoundError
# )
#
# # Services
# from backend.services import NewsService
# from backend.services.event_service import EventService
#
# # Database
# from backend.db.models import GeoPoliticalEvent
# from backend.db.session import get_db, engine, AsyncSessionLocal
#
# # Schemas
# from backend.schemas import (
#     GeoPoliticalEventCreate,
#     GeoPoliticalEventOut,
#     NewsProcessResult,
#     HealthCheck
# )

# ==============================================================================
# 10. NEXT STEPS
# ==============================================================================

# 1. Start the server: python backend/main.py
# 2. Visit http://localhost:8000/docs to explore API
# 3. Read REFACTORING.md for architectural details
# 4. Review REFACTOR_SUMMARY.md for what changed
# 5. Check tests/conftest.py for testing patterns
# 6. Begin implementing NLP, geospatial, and correlation modules

print(__doc__)
