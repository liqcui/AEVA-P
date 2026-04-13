"""API v1 module"""

from fastapi import APIRouter
from app.api.v1.endpoints import pipelines

api_router = APIRouter()
api_router.include_router(pipelines.router, prefix="/pipeline", tags=["pipelines"])

__all__ = ["api_router"]
