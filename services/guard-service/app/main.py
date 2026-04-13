"""
Guard Service Main Application

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core.config import settings
from app.core.redis_client import redis_client

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="1.0.0",
    description="AEVA Quality Gate Validation Service",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    """Initialize Redis connection on startup"""
    await redis_client.connect()


@app.on_event("shutdown")
async def shutdown_event():
    """Close Redis connection on shutdown"""
    await redis_client.disconnect()


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
        "version": "1.0.0"
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
        "description": "Quality gate validation and blocking service",
        "docs": f"{settings.API_V1_STR}/docs",
    }
