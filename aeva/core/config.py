"""
AEVA Configuration Management

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Optional, Dict, Any
from pathlib import Path
import yaml
from pydantic import BaseModel, Field


class DatabaseConfig(BaseModel):
    """Database configuration"""
    host: str = "localhost"
    port: int = 5432
    database: str = "aeva"
    username: str = "aeva"
    password: str = ""
    pool_size: int = 10


class RedisConfig(BaseModel):
    """Redis configuration"""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None


class BrainConfig(BaseModel):
    """AEVA-Brain configuration"""
    provider: str = "anthropic"  # anthropic, openai, etc.
    model: str = "claude-3-5-sonnet-20241022"
    api_key: Optional[str] = None
    max_tokens: int = 4096
    temperature: float = 0.7


class GuardConfig(BaseModel):
    """AEVA-Guard configuration"""
    enabled: bool = True
    default_threshold: float = 0.85
    strict_mode: bool = False
    auto_block: bool = True


class BenchConfig(BaseModel):
    """AEVA-Bench configuration"""
    benchmark_dir: str = "./benchmarks"
    cache_enabled: bool = True
    parallel_execution: bool = True
    max_workers: int = 4


class AutoConfig(BaseModel):
    """AEVA-Auto configuration"""
    worker_concurrency: int = 4
    task_timeout: int = 3600  # seconds
    retry_limit: int = 3
    queue_backend: str = "redis"


class AEVAConfig(BaseModel):
    """Main AEVA configuration"""
    project_name: str = "AEVA"
    version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"

    # Module configurations
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    brain: BrainConfig = Field(default_factory=BrainConfig)
    guard: GuardConfig = Field(default_factory=GuardConfig)
    bench: BenchConfig = Field(default_factory=BenchConfig)
    auto: AutoConfig = Field(default_factory=AutoConfig)

    # API configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4

    @classmethod
    def from_yaml(cls, path: str) -> "AEVAConfig":
        """Load configuration from YAML file"""
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        with open(config_path, "r") as f:
            config_dict = yaml.safe_load(f)

        return cls(**config_dict)

    def to_yaml(self, path: str) -> None:
        """Save configuration to YAML file"""
        config_dict = self.model_dump()

        with open(path, "w") as f:
            yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)

    @classmethod
    def from_env(cls) -> "AEVAConfig":
        """Load configuration from environment variables"""
        import os
        from dotenv import load_dotenv

        load_dotenv()

        config_dict = {}

        # Parse environment variables
        if api_key := os.getenv("AEVA_BRAIN_API_KEY"):
            config_dict.setdefault("brain", {})["api_key"] = api_key

        if db_host := os.getenv("AEVA_DB_HOST"):
            config_dict.setdefault("database", {})["host"] = db_host

        if db_password := os.getenv("AEVA_DB_PASSWORD"):
            config_dict.setdefault("database", {})["password"] = db_password

        if redis_host := os.getenv("AEVA_REDIS_HOST"):
            config_dict.setdefault("redis", {})["host"] = redis_host

        return cls(**config_dict)
