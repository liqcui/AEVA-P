"""
AEVA Service Configuration

Configuration schemas for AEVA microservices.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Optional
from pydantic import BaseModel


class BenchConfig(BaseModel):
    """AEVA-Bench service configuration"""
    benchmark_dir: str = "./benchmarks"
    cache_enabled: bool = True
    parallel_execution: bool = True
    max_workers: int = 4


class GuardConfig(BaseModel):
    """AEVA-Guard service configuration"""
    enabled: bool = True
    default_threshold: float = 0.85
    strict_mode: bool = False
    auto_block: bool = True


class AutoConfig(BaseModel):
    """AEVA-Auto service configuration"""
    worker_concurrency: int = 4
    task_timeout: int = 3600  # seconds
    retry_limit: int = 3
    queue_backend: str = "redis"


class BrainConfig(BaseModel):
    """AEVA-Brain service configuration"""
    provider: str = "anthropic"  # anthropic, openai, etc.
    model: str = "claude-3-5-sonnet-20241022"
    api_key: Optional[str] = None
    max_tokens: int = 4096
    temperature: float = 0.7
