"""
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.core.middleware import LoggingMiddleware
from app.db import engine, Base
from app.routers import api_router

# Setup logging first
setup_logging()
logger = get_logger(__name__)

# Create database tables
logger.info("Creating database tables...")
Base.metadata.create_all(bind=engine)
logger.info("Database tables created successfully")

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A RESTful API for managing addresses and finding nearby locations",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Include API routers
app.include_router(api_router)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info(
        f"Starting {settings.PROJECT_NAME} v{settings.VERSION}",
        extra={
            "extra_fields": {
                "environment": settings.ENVIRONMENT,
                "debug": settings.DEBUG,
                "log_level": settings.LOG_LEVEL
            }
        }
    )


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info(f"Shutting down {settings.PROJECT_NAME}")
