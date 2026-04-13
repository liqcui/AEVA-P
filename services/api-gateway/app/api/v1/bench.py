"""
Benchmark Service Proxy Endpoints

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
async def create_benchmark(benchmark_data: Dict[str, Any]):
    """Create a new benchmark"""
    return await service_client.post(
        settings.BENCH_SERVICE_URL,
        "/v1/benchmark/",
        benchmark_data
    )


@router.get("/{benchmark_id}")
async def get_benchmark(benchmark_id: UUID):
    """Get benchmark by ID"""
    return await service_client.get(
        settings.BENCH_SERVICE_URL,
        f"/v1/benchmark/{benchmark_id}"
    )


@router.get("/")
async def list_benchmarks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """List all benchmarks"""
    return await service_client.get(
        settings.BENCH_SERVICE_URL,
        "/v1/benchmark/",
        params={"skip": skip, "limit": limit}
    )


@router.put("/{benchmark_id}")
async def update_benchmark(benchmark_id: UUID, benchmark_data: Dict[str, Any]):
    """Update benchmark"""
    return await service_client.put(
        settings.BENCH_SERVICE_URL,
        f"/v1/benchmark/{benchmark_id}",
        benchmark_data
    )


@router.delete("/{benchmark_id}")
async def delete_benchmark(benchmark_id: UUID):
    """Delete benchmark"""
    return await service_client.delete(
        settings.BENCH_SERVICE_URL,
        f"/v1/benchmark/{benchmark_id}"
    )


@router.post("/{benchmark_id}/run")
async def run_benchmark(benchmark_id: UUID):
    """Run benchmark"""
    return await service_client.post(
        settings.BENCH_SERVICE_URL,
        f"/v1/benchmark/{benchmark_id}/run",
        {}
    )


@router.get("/{benchmark_id}/results")
async def get_benchmark_results(benchmark_id: UUID):
    """Get benchmark results"""
    return await service_client.get(
        settings.BENCH_SERVICE_URL,
        f"/v1/benchmark/{benchmark_id}/results"
    )


@router.get("/{benchmark_id}/history")
async def get_benchmark_history(
    benchmark_id: UUID,
    limit: int = Query(10, ge=1, le=100)
):
    """Get benchmark execution history"""
    return await service_client.get(
        settings.BENCH_SERVICE_URL,
        f"/v1/benchmark/{benchmark_id}/history",
        params={"limit": limit}
    )
