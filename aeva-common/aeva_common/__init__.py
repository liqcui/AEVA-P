"""
AEVA Common SDK

Shared data structures, interfaces, and clients for AEVA microservices.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

__version__ = "0.1.0"

from .models import (
    EvaluationResult,
    MetricResult,
    GateResult,
    Analysis,
    ResultStatus,
)

from .config import (
    BenchConfig,
    GuardConfig,
    AutoConfig,
    BrainConfig,
    DatabaseConfig,
    RedisConfig,
)

__all__ = [
    # Models
    "EvaluationResult",
    "MetricResult",
    "GateResult",
    "Analysis",
    "ResultStatus",
    # Config
    "BenchConfig",
    "GuardConfig",
    "AutoConfig",
    "BrainConfig",
    "DatabaseConfig",
    "RedisConfig",
]
