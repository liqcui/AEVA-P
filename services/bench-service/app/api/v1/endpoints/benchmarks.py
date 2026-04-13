"""
Benchmark API Endpoints

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Optional
from uuid import UUID
import math

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.benchmark import (
    BenchmarkCreate,
    BenchmarkUpdate,
    BenchmarkResponse,
    BenchmarkListResponse,
    BenchmarkExecutionResponse,
)
from app.services.benchmark_service import BenchmarkService
from app.models.benchmark import BenchmarkStatus

router = APIRouter()


@router.post("/", response_model=BenchmarkResponse, status_code=status.HTTP_201_CREATED)
def create_benchmark(
    benchmark: BenchmarkCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new benchmark.

    - **name**: Benchmark name (required)
    - **description**: Benchmark description (optional)
    - **model_path**: Path to the model file (required)
    - **dataset_path**: Path to the dataset file (optional)
    - **config**: Additional configuration as JSON (optional)
    """
    db_benchmark = BenchmarkService.create_benchmark(db, benchmark)
    return db_benchmark


@router.get("/{benchmark_id}", response_model=BenchmarkResponse)
def get_benchmark(
    benchmark_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get a specific benchmark by ID.

    Returns the benchmark details including status, results, and metrics.
    """
    db_benchmark = BenchmarkService.get_benchmark(db, benchmark_id)
    if not db_benchmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Benchmark {benchmark_id} not found"
        )
    return db_benchmark


@router.get("/", response_model=BenchmarkListResponse)
def list_benchmarks(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    status_filter: Optional[BenchmarkStatus] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """
    List all benchmarks with pagination.

    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 50, max: 100)
    - **status_filter**: Filter by benchmark status (optional)

    Returns paginated list of benchmarks with total count.
    """
    skip = (page - 1) * page_size
    benchmarks, total = BenchmarkService.list_benchmarks(
        db, skip=skip, limit=page_size, status=status_filter
    )

    pages = math.ceil(total / page_size) if total > 0 else 0

    return {
        "benchmarks": benchmarks,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
    }


@router.put("/{benchmark_id}", response_model=BenchmarkResponse)
def update_benchmark(
    benchmark_id: UUID,
    benchmark_update: BenchmarkUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a benchmark.

    Only name, description, and status can be updated.
    Other fields are read-only after creation.
    """
    db_benchmark = BenchmarkService.update_benchmark(db, benchmark_id, benchmark_update)
    if not db_benchmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Benchmark {benchmark_id} not found"
        )
    return db_benchmark


@router.delete("/{benchmark_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_benchmark(
    benchmark_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Delete a benchmark.

    This permanently removes the benchmark and all associated data.
    """
    success = BenchmarkService.delete_benchmark(db, benchmark_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Benchmark {benchmark_id} not found"
        )
    return None


@router.post("/{benchmark_id}/execute", response_model=BenchmarkExecutionResponse)
def execute_benchmark(
    benchmark_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Execute a benchmark.

    This starts the benchmark execution asynchronously.
    Use GET /{benchmark_id} to check the status and results.

    **Note**: In this initial implementation, execution is simulated.
    Production version should integrate with actual benchmark execution engine.
    """
    db_benchmark = BenchmarkService.get_benchmark(db, benchmark_id)
    if not db_benchmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Benchmark {benchmark_id} not found"
        )

    if db_benchmark.status == BenchmarkStatus.RUNNING:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Benchmark is already running"
        )

    # Mark as running
    BenchmarkService.start_benchmark_execution(db, benchmark_id)

    # TODO: In production, trigger actual benchmark execution here
    # For now, we'll simulate immediate completion with dummy data
    import time
    import random

    # Simulate execution (remove in production)
    results = {
        "predictions": 1000,
        "correct": int(1000 * random.uniform(0.85, 0.98)),
        "execution_time": random.uniform(100, 300),
    }

    metrics = {
        "accuracy": random.uniform(0.85, 0.98),
        "f1_score": random.uniform(0.83, 0.96),
        "precision": random.uniform(0.82, 0.95),
        "recall": random.uniform(0.84, 0.97),
        "duration": random.uniform(100, 300),
        "throughput": random.uniform(2.5, 5.0),
    }

    BenchmarkService.complete_benchmark_execution(db, benchmark_id, results, metrics)

    return {
        "benchmark_id": benchmark_id,
        "status": "completed",  # Would be "running" in production
        "message": "Benchmark execution completed successfully"
    }


@router.get("/{benchmark_id}/results", response_model=dict)
def get_benchmark_results(
    benchmark_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get benchmark execution results.

    Returns detailed results if the benchmark has completed.
    """
    db_benchmark = BenchmarkService.get_benchmark(db, benchmark_id)
    if not db_benchmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Benchmark {benchmark_id} not found"
        )

    if db_benchmark.status != BenchmarkStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Benchmark is not completed (status: {db_benchmark.status.value})"
        )

    return {
        "benchmark_id": str(benchmark_id),
        "name": db_benchmark.name,
        "status": db_benchmark.status.value,
        "results": db_benchmark.results,
        "metrics": {
            "accuracy": db_benchmark.accuracy,
            "f1_score": db_benchmark.f1_score,
            "precision": db_benchmark.precision,
            "recall": db_benchmark.recall,
        },
        "performance": {
            "duration": db_benchmark.duration,
            "throughput": db_benchmark.throughput,
        },
        "started_at": db_benchmark.started_at.isoformat() if db_benchmark.started_at else None,
        "completed_at": db_benchmark.completed_at.isoformat() if db_benchmark.completed_at else None,
    }


@router.get("/statistics/summary", response_model=dict)
def get_statistics(db: Session = Depends(get_db)):
    """
    Get benchmark statistics.

    Returns counts of benchmarks by status.
    """
    stats = BenchmarkService.get_benchmark_statistics(db)
    return {
        "statistics": stats,
        "success_rate": round(stats["completed"] / stats["total"] * 100, 2) if stats["total"] > 0 else 0,
    }
