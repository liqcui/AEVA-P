"""
Pipeline API Endpoints

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.pipeline_service import PipelineService
from app.schemas.pipeline import (
    PipelineCreate,
    PipelineUpdate,
    PipelineResponse,
    PipelineListResponse,
    PipelineExecutionRequest,
    PipelineExecutionResponse,
)
from app.models.pipeline import PipelineStatus
from app.tasks.pipeline_tasks import execute_pipeline

router = APIRouter()


@router.post("/", response_model=PipelineResponse, status_code=status.HTTP_201_CREATED)
def create_pipeline(
    pipeline_create: PipelineCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new pipeline.

    Args:
        pipeline_create: Pipeline configuration
        db: Database session dependency

    Returns:
        Created pipeline information
    """
    pipeline = PipelineService.create_pipeline(db, pipeline_create)
    return pipeline


@router.get("/{pipeline_id}", response_model=PipelineResponse)
def get_pipeline(
    pipeline_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get pipeline details by ID.

    Args:
        pipeline_id: Pipeline UUID
        db: Database session dependency

    Returns:
        Pipeline information

    Raises:
        HTTPException: 404 if pipeline not found
    """
    pipeline = PipelineService.get_pipeline(db, pipeline_id)
    if not pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline {pipeline_id} not found"
        )
    return pipeline


@router.get("/", response_model=PipelineListResponse)
def list_pipelines(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[PipelineStatus] = Query(None, alias="status"),
    db: Session = Depends(get_db)
):
    """
    List all pipelines with optional filtering.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        status_filter: Filter by pipeline status
        db: Database session dependency

    Returns:
        List of pipelines with total count
    """
    pipelines = PipelineService.list_pipelines(db, skip, limit, status_filter)
    total = PipelineService.count_pipelines(db, status_filter)
    return PipelineListResponse(pipelines=pipelines, total=total)


@router.put("/{pipeline_id}", response_model=PipelineResponse)
def update_pipeline(
    pipeline_id: UUID,
    pipeline_update: PipelineUpdate,
    db: Session = Depends(get_db)
):
    """
    Update pipeline configuration.

    Args:
        pipeline_id: Pipeline UUID
        pipeline_update: Fields to update
        db: Database session dependency

    Returns:
        Updated pipeline information

    Raises:
        HTTPException: 404 if pipeline not found
    """
    pipeline = PipelineService.update_pipeline(db, pipeline_id, pipeline_update)
    if not pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline {pipeline_id} not found"
        )
    return pipeline


@router.delete("/{pipeline_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pipeline(
    pipeline_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Delete a pipeline.

    Args:
        pipeline_id: Pipeline UUID
        db: Database session dependency

    Raises:
        HTTPException: 404 if pipeline not found
    """
    success = PipelineService.delete_pipeline(db, pipeline_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline {pipeline_id} not found"
        )


@router.post("/{pipeline_id}/execute", response_model=PipelineExecutionResponse)
def execute_pipeline_endpoint(
    pipeline_id: UUID,
    execution_request: PipelineExecutionRequest,
    db: Session = Depends(get_db)
):
    """
    Execute a pipeline asynchronously.

    Args:
        pipeline_id: Pipeline UUID
        execution_request: Execution configuration
        db: Database session dependency

    Returns:
        Execution status with Celery task ID

    Raises:
        HTTPException: 404 if pipeline not found
    """
    pipeline = PipelineService.get_pipeline(db, pipeline_id)
    if not pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline {pipeline_id} not found"
        )

    # Check if pipeline is already running
    if pipeline.status == PipelineStatus.RUNNING:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Pipeline {pipeline_id} is already running"
        )

    # Start Celery task
    task = execute_pipeline.apply_async(
        args=[str(pipeline_id)],
        kwargs={"metadata": execution_request.metadata}
    )

    # Update pipeline with task ID
    pipeline.celery_task_id = task.id
    pipeline.status = PipelineStatus.RUNNING
    db.commit()

    return PipelineExecutionResponse(
        pipeline_id=pipeline_id,
        celery_task_id=task.id,
        status=PipelineStatus.RUNNING,
        message="Pipeline execution started"
    )


@router.post("/{pipeline_id}/cancel", response_model=PipelineResponse)
def cancel_pipeline(
    pipeline_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Cancel a running pipeline.

    Args:
        pipeline_id: Pipeline UUID
        db: Database session dependency

    Returns:
        Updated pipeline information

    Raises:
        HTTPException: 404 if pipeline not found or not running
    """
    pipeline = PipelineService.get_pipeline(db, pipeline_id)
    if not pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline {pipeline_id} not found"
        )

    if pipeline.status != PipelineStatus.RUNNING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Pipeline {pipeline_id} is not running"
        )

    # Revoke Celery task
    if pipeline.celery_task_id:
        from app.core.celery_app import celery_app
        celery_app.control.revoke(pipeline.celery_task_id, terminate=True)

    # Update pipeline status
    pipeline = PipelineService.update_pipeline_status(
        db,
        pipeline_id,
        PipelineStatus.CANCELLED
    )

    return pipeline
