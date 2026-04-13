"""
AEVA Service Interfaces

Standardized API contracts for AEVA microservices.
"""

from .bench import IBenchmarkService, BenchmarkRequest, BenchmarkInfo
from .guard import IGuardService, GateConfig, GateStatus
from .auto import IAutoService, PipelineConfig, PipelineStatus
from .brain import IBrainService, AnalysisRequest

__all__ = [
    # Benchmark
    "IBenchmarkService",
    "BenchmarkRequest",
    "BenchmarkInfo",
    # Guard
    "IGuardService",
    "GateConfig",
    "GateStatus",
    # Auto
    "IAutoService",
    "PipelineConfig",
    "PipelineStatus",
    # Brain
    "IBrainService",
    "AnalysisRequest",
]
