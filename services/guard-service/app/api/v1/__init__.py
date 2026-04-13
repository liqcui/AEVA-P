"""API v1 module"""

from fastapi import APIRouter
from app.api.v1.endpoints import gates

api_router = APIRouter()
api_router.include_router(gates.router, prefix="/gate", tags=["gates"])

__all__ = ["api_router"]
