"""
API Gateway Main Application

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core.config import settings
from app.middleware.rate_limit import RateLimitMiddleware

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="1.0.0",
    description="AEVA API Gateway - Unified access to all microservices",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware
if settings.ENABLE_RATE_LIMITING:
    app.add_middleware(RateLimitMiddleware)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health_check():
    """
    Health check endpoint for Kubernetes liveness/readiness probes.

    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0",
        "services": {
            "bench": settings.BENCH_SERVICE_URL,
            "guard": settings.GUARD_SERVICE_URL,
            "auto": settings.AUTO_SERVICE_URL,
            "brain": settings.BRAIN_SERVICE_URL,
        }
    }


@app.get("/")
async def root():
    """
    Root endpoint with service information.

    Returns:
        Service metadata
    """
    return {
        "service": settings.PROJECT_NAME,
        "version": "1.0.0",
        "description": "Unified API Gateway for AEVA microservices platform",
        "docs": f"{settings.API_V1_STR}/docs",
        "endpoints": {
            "benchmark": f"{settings.API_V1_STR}/benchmark",
            "gate": f"{settings.API_V1_STR}/gate",
            "pipeline": f"{settings.API_V1_STR}/pipeline",
            "analysis": f"{settings.API_V1_STR}/analysis",
        }
    }
