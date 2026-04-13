"""
Bench Service Configuration

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = "AEVA Bench Service"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Benchmark testing and evaluation service"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8001

    # Database
    DATABASE_URL: str = "postgresql://aeva:aeva@localhost:5432/bench_service"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Security
    API_KEY: Optional[str] = None
    SECRET_KEY: str = "dev-secret-key-change-in-production"

    # Logging
    LOG_LEVEL: str = "INFO"

    # Benchmark Settings
    MAX_BENCHMARK_NAME_LENGTH: int = 255
    MAX_BENCHMARKS_PER_PAGE: int = 100
    DEFAULT_PAGE_SIZE: int = 50

    # Performance
    BENCHMARK_TIMEOUT: int = 3600  # 1 hour
    MAX_CONCURRENT_BENCHMARKS: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
