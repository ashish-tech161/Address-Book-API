"""
FastAPI dependencies
"""
from typing import Generator
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.core.logging import get_logger

logger = get_logger(__name__)


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        logger.debug("Database session created")
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}", exc_info=True)
        db.rollback()
        raise
    finally:
        logger.debug("Closing database session")
        db.close()
