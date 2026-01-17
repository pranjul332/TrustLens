"""
Main application entry point for Report Service
"""
from fastapi import FastAPI
import logging

from .config import settings
from .routes import router
from .database import connect_to_mongo, close_mongo_connection

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.SERVICE_NAME,
    version=settings.SERVICE_VERSION,
    description=settings.SERVICE_DESCRIPTION
)

# Include routes
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info(f"Starting {settings.SERVICE_NAME} v{settings.SERVICE_VERSION}")
    await connect_to_mongo()
    logger.info("Application ready")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    logger.info("Shutting down application")
    await close_mongo_connection()
    logger.info("Shutdown complete")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower()
    )