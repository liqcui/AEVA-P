"""
Auto Service Configuration

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = "AEVA Auto Service"

    # Database Configuration
    DATABASE_URL: str = "postgresql://aeva:aeva@localhost:5432/auto_service"

    # Redis Configuration (for Celery broker and result backend)
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"

    # Service URLs
    BENCH_SERVICE_URL: str = "http://localhost:8001"
    GUARD_SERVICE_URL: str = "http://localhost:8002"
    BRAIN_SERVICE_URL: str = "http://localhost:8004"

    # Pipeline Configuration
    DEFAULT_TIMEOUT: int = 3600  # 1 hour
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 60  # seconds

    class Config:
        env_file = ".env"


settings = Settings()
