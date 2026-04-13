"""
AEVA Benchmark Service Client

HTTP client for AEVA-Bench microservice.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import List
from .base import BaseServiceClient
from ..models import EvaluationResult
from ..interfaces import BenchmarkRequest, BenchmarkInfo


class BenchClient(BaseServiceClient):
    """Client for AEVA-Bench service"""

    async def create_benchmark(self, request: BenchmarkRequest) -> str:
        """Create a new benchmark"""
        response = await self.post(
            "/benchmark/create",
            json=request.model_dump()
        )
        return response["benchmark_id"]

    async def run_benchmark(self, benchmark_id: str) -> EvaluationResult:
        """Execute a benchmark"""
        response = await self.post(
            f"/benchmark/{benchmark_id}/run"
        )
        return EvaluationResult.from_dict(response["result"])

    async def get_results(self, benchmark_id: str) -> List[EvaluationResult]:
        """Get benchmark results"""
        response = await self.get(f"/benchmark/{benchmark_id}/results")
        return [
            EvaluationResult.from_dict(r)
            for r in response["results"]
        ]

    async def list_benchmarks(self) -> List[BenchmarkInfo]:
        """List all benchmarks"""
        response = await self.get("/benchmark/list")
        return [
            BenchmarkInfo(**b)
            for b in response["benchmarks"]
        ]

    async def delete_benchmark(self, benchmark_id: str) -> bool:
        """Delete a benchmark"""
        response = await self.delete(f"/benchmark/{benchmark_id}")
        return response["success"]
