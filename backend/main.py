import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api import api_router
from core.config import settings
from db.base import init_db
from db.models import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Starting up application and initializing database...")
    await init_db()
    logger.info("Database initialization complete.")
    yield
    # Shutdown
    logger.info("Shutting down application...")
    # Add any shutdown logic here if needed
    logger.info("Application shutdown complete.")

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# --- CORS Middleware ---
if settings.BACKEND_CORS_ORIGINS:
    logger.info(f"Setting up CORS middleware for origins: {settings.BACKEND_CORS_ORIGINS}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS], # Convert Pydantic URLs to strings
        allow_credentials=True,
        allow_methods=["*"], # Allow all standard methods
        allow_headers=["*"], # Allow all headers
    )
else:
     logger.info("No CORS origins specified. Skipping CORS middleware setup.")


app.include_router(api_router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Simple root endpoint to check if the API is running."""
    logger.info("Root endpoint accessed.")
    return {"message": f"Welcome to the {settings.PROJECT_NAME} API!"}
