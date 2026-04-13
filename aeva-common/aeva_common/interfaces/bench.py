"""
AEVA Benchmark Service Interface

API contract for AEVA-Bench microservice.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Protocol, List, Dict, Any, Optional
from pydantic import BaseModel
from ..models import EvaluationResult


class BenchmarkRequest(BaseModel):
    """Request to run a benchmark"""
    benchmark_name: str
    model_path: str
    dataset_path: Optional[str] = None
    config: Dict[str, Any] = {}


class BenchmarkInfo(BaseModel):
    """Benchmark metadata"""
    id: str
    name: str
    description: str
    created_at: str
    status: str  # pending, running, completed, failed


class IBenchmarkService(Protocol):
    """
    Benchmark Service Interface

    Defines the API contract for the AEVA-Bench microservice.
    """

    async def create_benchmark(self, request: BenchmarkRequest) -> str:
        """
        Create a new benchmark

        Args:
            request: Benchmark configuration

        Returns:
            benchmark_id: Unique identifier for the benchmark
        """
        ...

    async def run_benchmark(self, benchmark_id: str) -> EvaluationResult:
        """
        Execute a benchmark

        Args:
            benchmark_id: Unique identifier

        Returns:
            result: Evaluation result with metrics
        """
        ...

    async def get_results(self, benchmark_id: str) -> List[EvaluationResult]:
        """
        Get benchmark results

        Args:
            benchmark_id: Unique identifier

        Returns:
            results: List of evaluation results
        """
        ...

    async def list_benchmarks(self) -> List[BenchmarkInfo]:
        """
        List all available benchmarks

        Returns:
            benchmarks: List of benchmark metadata
        """
        ...

    async def delete_benchmark(self, benchmark_id: str) -> bool:
        """
        Delete a benchmark

        Args:
            benchmark_id: Unique identifier

        Returns:
            success: True if deleted successfully
        """
        ...
