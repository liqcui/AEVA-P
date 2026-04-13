"""API v1"""

from fastapi import APIRouter
from app.api.v1.endpoints import benchmarks

api_router = APIRouter()

# Include routers
api_router.include_router(
    benchmarks.router,
    prefix="/benchmark",
    tags=["benchmarks"]
)

__all__ = ["api_router"]
