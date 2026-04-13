"""API v1 module"""

from fastapi import APIRouter
from app.api.v1.endpoints import analyses

api_router = APIRouter()
api_router.include_router(analyses.router, prefix="/analysis", tags=["analyses"])

__all__ = ["api_router"]
