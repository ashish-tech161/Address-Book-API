from fastapi import APIRouter
from .base import router as base_router
from .address import router as address_router
from app.core.config import settings

api_router = APIRouter()

# Root and health checks
api_router.include_router(base_router)

# Resource routes with prefix
api_router.include_router(address_router, prefix=settings.API_V1_STR)
