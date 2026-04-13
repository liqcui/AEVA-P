"""
Guard Service Proxy Endpoints

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Dict, Any
from uuid import UUID

from fastapi import APIRouter, Query

from app.core.config import settings
from app.core.service_client import service_client

router = APIRouter()


@router.post("/")
async def create_gate(gate_data: Dict[str, Any]):
    """Create a new quality gate"""
    return await service_client.post(
        settings.GUARD_SERVICE_URL,
        "/v1/gate/",
        gate_data
    )


@router.get("/{gate_id}")
async def get_gate(gate_id: UUID):
    """Get gate by ID"""
    return await service_client.get(
        settings.GUARD_SERVICE_URL,
        f"/v1/gate/{gate_id}"
    )


@router.get("/")
async def list_gates():
    """List all gates"""
    return await service_client.get(
        settings.GUARD_SERVICE_URL,
        "/v1/gate/"
    )


@router.put("/{gate_id}")
async def update_gate(gate_id: UUID, gate_data: Dict[str, Any]):
    """Update gate"""
    return await service_client.put(
        settings.GUARD_SERVICE_URL,
        f"/v1/gate/{gate_id}",
        gate_data
    )


@router.delete("/{gate_id}")
async def delete_gate(gate_id: UUID):
    """Delete gate"""
    return await service_client.delete(
        settings.GUARD_SERVICE_URL,
        f"/v1/gate/{gate_id}"
    )


@router.post("/{gate_id}/validate")
async def validate_metrics(gate_id: UUID, validation_data: Dict[str, Any]):
    """Validate metrics against gate"""
    return await service_client.post(
        settings.GUARD_SERVICE_URL,
        f"/v1/gate/{gate_id}/validate",
        validation_data
    )


@router.get("/{gate_id}/history")
async def get_validation_history(
    gate_id: UUID,
    limit: int = Query(100, ge=1, le=1000)
):
    """Get validation history"""
    return await service_client.get(
        settings.GUARD_SERVICE_URL,
        f"/v1/gate/{gate_id}/history",
        params={"limit": limit}
    )


@router.get("/{gate_id}/statistics")
async def get_gate_statistics(gate_id: UUID):
    """Get gate statistics"""
    return await service_client.get(
        settings.GUARD_SERVICE_URL,
        f"/v1/gate/{gate_id}/statistics"
    )
