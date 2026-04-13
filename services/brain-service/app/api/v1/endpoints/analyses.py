"""
Analysis API Endpoints

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, status, Query, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.analysis_service import AnalysisService
from app.schemas.analysis import (
    AnalysisCreate,
    AnalysisResponse,
    AnalysisListResponse,
    QuickAnalysisRequest,
    QuickAnalysisResponse,
)
from app.models.analysis import AnalysisType, AnalysisStatus

router = APIRouter()


@router.post("/", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def create_analysis(
    analysis_create: AnalysisCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create a new analysis and process it asynchronously.

    Args:
        analysis_create: Analysis configuration
        background_tasks: FastAPI background tasks
        db: Database session dependency

    Returns:
        Created analysis information
    """
    analysis = AnalysisService.create_analysis(db, analysis_create)

    # Process analysis in background
    background_tasks.add_task(AnalysisService.perform_analysis, db, analysis.id)

    return analysis


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get analysis details by ID.

    Args:
        analysis_id: Analysis UUID
        db: Database session dependency

    Returns:
        Analysis information

    Raises:
        HTTPException: 404 if analysis not found
    """
    analysis = AnalysisService.get_analysis(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {analysis_id} not found"
        )
    return analysis


@router.get("/", response_model=AnalysisListResponse)
def list_analyses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    analysis_type: Optional[AnalysisType] = Query(None, alias="type"),
    status_filter: Optional[AnalysisStatus] = Query(None, alias="status"),
    db: Session = Depends(get_db)
):
    """
    List all analyses with optional filtering.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        analysis_type: Filter by analysis type
        status_filter: Filter by analysis status
        db: Database session dependency

    Returns:
        List of analyses with total count
    """
    analyses = AnalysisService.list_analyses(db, skip, limit, analysis_type, status_filter)
    total = AnalysisService.count_analyses(db, analysis_type, status_filter)
    return AnalysisListResponse(analyses=analyses, total=total)


@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_analysis(
    analysis_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Delete an analysis.

    Args:
        analysis_id: Analysis UUID
        db: Database session dependency

    Raises:
        HTTPException: 404 if analysis not found
    """
    success = AnalysisService.delete_analysis(db, analysis_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {analysis_id} not found"
        )


@router.post("/quick", response_model=QuickAnalysisResponse)
async def quick_analysis(request: QuickAnalysisRequest):
    """
    Perform quick analysis without database persistence.

    This endpoint provides immediate AI analysis without storing
    the request or results in the database.

    Args:
        request: Quick analysis request

    Returns:
        Analysis results
    """
    result = await AnalysisService.quick_analysis(
        analysis_type=request.analysis_type,
        data=request.data,
        config=request.config
    )

    return QuickAnalysisResponse(**result)


@router.post("/{analysis_id}/reprocess", response_model=AnalysisResponse)
async def reprocess_analysis(
    analysis_id: UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Reprocess an existing analysis.

    Args:
        analysis_id: Analysis UUID
        background_tasks: FastAPI background tasks
        db: Database session dependency

    Returns:
        Updated analysis information

    Raises:
        HTTPException: 404 if analysis not found
    """
    analysis = AnalysisService.get_analysis(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {analysis_id} not found"
        )

    # Reset status to pending
    analysis.status = AnalysisStatus.PENDING
    analysis.analysis_text = None
    analysis.findings = None
    analysis.recommendations = None
    analysis.error_message = None
    db.commit()

    # Process analysis in background
    background_tasks.add_task(AnalysisService.perform_analysis, db, analysis.id)

    return analysis
