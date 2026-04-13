"""
Auto Service Proxy Endpoints

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
async def create_pipeline(pipeline_data: Dict[str, Any]):
    """Create a new pipeline"""
    return await service_client.post(
        settings.AUTO_SERVICE_URL,
        "/v1/pipeline/",
        pipeline_data
    )


@router.get("/{pipeline_id}")
async def get_pipeline(pipeline_id: UUID):
    """Get pipeline by ID"""
    return await service_client.get(
        settings.AUTO_SERVICE_URL,
        f"/v1/pipeline/{pipeline_id}"
    )


@router.get("/")
async def list_pipelines(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None)
):
    """List all pipelines"""
    params = {"skip": skip, "limit": limit}
    if status:
        params["status"] = status

    return await service_client.get(
        settings.AUTO_SERVICE_URL,
        "/v1/pipeline/",
        params=params
    )


@router.put("/{pipeline_id}")
async def update_pipeline(pipeline_id: UUID, pipeline_data: Dict[str, Any]):
    """Update pipeline"""
    return await service_client.put(
        settings.AUTO_SERVICE_URL,
        f"/v1/pipeline/{pipeline_id}",
        pipeline_data
    )


@router.delete("/{pipeline_id}")
async def delete_pipeline(pipeline_id: UUID):
    """Delete pipeline"""
    return await service_client.delete(
        settings.AUTO_SERVICE_URL,
        f"/v1/pipeline/{pipeline_id}"
    )


@router.post("/{pipeline_id}/execute")
async def execute_pipeline(pipeline_id: UUID, execution_data: Dict[str, Any]):
    """Execute pipeline"""
    return await service_client.post(
        settings.AUTO_SERVICE_URL,
        f"/v1/pipeline/{pipeline_id}/execute",
        execution_data
    )


@router.post("/{pipeline_id}/cancel")
async def cancel_pipeline(pipeline_id: UUID):
    """Cancel pipeline"""
    return await service_client.post(
        settings.AUTO_SERVICE_URL,
        f"/v1/pipeline/{pipeline_id}/cancel",
        {}
    )
