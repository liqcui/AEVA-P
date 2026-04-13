"""
API Gateway Configuration

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AEVA API Gateway"

    # Service URLs
    BENCH_SERVICE_URL: str = "http://localhost:8001"
    GUARD_SERVICE_URL: str = "http://localhost:8002"
    AUTO_SERVICE_URL: str = "http://localhost:8003"
    BRAIN_SERVICE_URL: str = "http://localhost:8004"

    # Gateway Configuration
    REQUEST_TIMEOUT: int = 300  # 5 minutes
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 1  # seconds

    # Rate Limiting
    ENABLE_RATE_LIMITING: bool = True
    RATE_LIMIT_PER_MINUTE: int = 100

    # Authentication (future implementation)
    ENABLE_AUTH: bool = False
    JWT_SECRET_KEY: str = "change-this-secret-key-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS Configuration
    CORS_ORIGINS: list = ["*"]

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
