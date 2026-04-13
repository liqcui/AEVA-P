"""API v1 module"""

from fastapi import APIRouter
from app.api.v1 import bench, guard, auto, brain

api_router = APIRouter()

# Include service routers
api_router.include_router(bench.router, prefix="/benchmark", tags=["benchmark"])
api_router.include_router(guard.router, prefix="/gate", tags=["gate"])
api_router.include_router(auto.router, prefix="/pipeline", tags=["pipeline"])
api_router.include_router(brain.router, prefix="/analysis", tags=["analysis"])

__all__ = ["api_router"]
