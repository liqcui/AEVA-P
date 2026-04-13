"""
Gate API Endpoints

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, status

from app.core.redis_client import RedisClient, get_redis
from app.services.gate_service import GateService
from app.schemas.gate import (
    GateCreate,
    GateUpdate,
    GateResponse,
    GateListResponse,
    ValidationRequest,
    ValidationResponse,
    GateStatistics,
)

router = APIRouter()


@router.post("/", response_model=GateResponse, status_code=status.HTTP_201_CREATED)
async def create_gate(
    gate_create: GateCreate,
    redis: RedisClient = Depends(get_redis)
):
    """
    Register a new quality gate.

    Args:
        gate_create: Gate configuration
        redis: Redis client dependency

    Returns:
        Created gate information
    """
    gate = await GateService.create_gate(redis, gate_create)
    return gate


@router.get("/{gate_id}", response_model=GateResponse)
async def get_gate(
    gate_id: UUID,
    redis: RedisClient = Depends(get_redis)
):
    """
    Get gate details by ID.

    Args:
        gate_id: Gate UUID
        redis: Redis client dependency

    Returns:
        Gate information

    Raises:
        HTTPException: 404 if gate not found
    """
    gate = await GateService.get_gate(redis, gate_id)
    if not gate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gate {gate_id} not found"
        )
    return gate


@router.get("/", response_model=GateListResponse)
async def list_gates(redis: RedisClient = Depends(get_redis)):
    """
    List all quality gates.

    Args:
        redis: Redis client dependency

    Returns:
        List of all gates with total count
    """
    gates = await GateService.list_gates(redis)
    return GateListResponse(gates=gates, total=len(gates))


@router.put("/{gate_id}", response_model=GateResponse)
async def update_gate(
    gate_id: UUID,
    gate_update: GateUpdate,
    redis: RedisClient = Depends(get_redis)
):
    """
    Update gate configuration.

    Args:
        gate_id: Gate UUID
        gate_update: Fields to update
        redis: Redis client dependency

    Returns:
        Updated gate information

    Raises:
        HTTPException: 404 if gate not found
    """
    gate = await GateService.update_gate(redis, gate_id, gate_update)
    if not gate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gate {gate_id} not found"
        )
    return gate


@router.delete("/{gate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gate(
    gate_id: UUID,
    redis: RedisClient = Depends(get_redis)
):
    """
    Delete a quality gate.

    Args:
        gate_id: Gate UUID
        redis: Redis client dependency

    Raises:
        HTTPException: 404 if gate not found
    """
    success = await GateService.delete_gate(redis, gate_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gate {gate_id} not found"
        )


@router.post("/{gate_id}/validate", response_model=ValidationResponse)
async def validate_metrics(
    gate_id: UUID,
    validation_request: ValidationRequest,
    redis: RedisClient = Depends(get_redis)
):
    """
    Validate metrics against a quality gate.

    Args:
        gate_id: Gate UUID
        validation_request: Metrics and metadata to validate
        redis: Redis client dependency

    Returns:
        Validation result with pass/fail status, score, and blocking decision

    Raises:
        HTTPException: 404 if gate not found or disabled
    """
    result = await GateService.validate(redis, gate_id, validation_request)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gate {gate_id} not found or disabled"
        )
    return result


@router.get("/{gate_id}/history", response_model=List[ValidationResponse])
async def get_validation_history(
    gate_id: UUID,
    limit: int = 100,
    redis: RedisClient = Depends(get_redis)
):
    """
    Get validation history for a gate.

    Args:
        gate_id: Gate UUID
        limit: Maximum number of results to return (default: 100)
        redis: Redis client dependency

    Returns:
        List of recent validation results
    """
    history = await GateService.get_history(redis, gate_id, limit)
    return history


@router.get("/{gate_id}/statistics", response_model=GateStatistics)
async def get_gate_statistics(
    gate_id: UUID,
    redis: RedisClient = Depends(get_redis)
):
    """
    Get statistics for a gate.

    Args:
        gate_id: Gate UUID
        redis: Redis client dependency

    Returns:
        Gate statistics including success rate and block rate

    Raises:
        HTTPException: 404 if gate not found
    """
    stats = await GateService.get_statistics(redis, gate_id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gate {gate_id} not found"
        )
    return stats
