from fastapi import APIRouter
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.get("/", tags=["root"])
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Address Book API",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


