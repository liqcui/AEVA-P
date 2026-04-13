"""
Brain Service Proxy Endpoints

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Dict, Any, Optional
from uuid import UUID

from fastapi import APIRouter, Query

from app.core.config import settings
from app.core.service_client import service_client

router = APIRouter()


@router.post("/")
async def create_analysis(analysis_data: Dict[str, Any]):
    """Create a new analysis"""
    return await service_client.post(
        settings.BRAIN_SERVICE_URL,
        "/v1/analysis/",
        analysis_data
    )


@router.get("/{analysis_id}")
async def get_analysis(analysis_id: UUID):
    """Get analysis by ID"""
    return await service_client.get(
        settings.BRAIN_SERVICE_URL,
        f"/v1/analysis/{analysis_id}"
    )


@router.get("/")
async def list_analyses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    analysis_type: Optional[str] = Query(None, alias="type"),
    status: Optional[str] = Query(None)
):
    """List all analyses"""
    params = {"skip": skip, "limit": limit}
    if analysis_type:
        params["type"] = analysis_type
    if status:
        params["status"] = status

    return await service_client.get(
        settings.BRAIN_SERVICE_URL,
        "/v1/analysis/",
        params=params
    )


@router.delete("/{analysis_id}")
async def delete_analysis(analysis_id: UUID):
    """Delete analysis"""
    return await service_client.delete(
        settings.BRAIN_SERVICE_URL,
        f"/v1/analysis/{analysis_id}"
    )


@router.post("/quick")
async def quick_analysis(analysis_data: Dict[str, Any]):
    """Quick analysis without persistence"""
    return await service_client.post(
        settings.BRAIN_SERVICE_URL,
        "/v1/analysis/quick",
        analysis_data
    )


@router.post("/{analysis_id}/reprocess")
async def reprocess_analysis(analysis_id: UUID):
    """Reprocess analysis"""
    return await service_client.post(
        settings.BRAIN_SERVICE_URL,
        f"/v1/analysis/{analysis_id}/reprocess",
        {}
    )
