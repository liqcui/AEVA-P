"""
Guard Service Configuration

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = "AEVA Guard Service"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Quality gate validation and enforcement service"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8002

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600  # 1 hour

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Security
    API_KEY: Optional[str] = None
    SECRET_KEY: str = "dev-secret-key-change-in-production"

    # Logging
    LOG_LEVEL: str = "INFO"

    # Gate Settings
    DEFAULT_THRESHOLD: float = 0.85
    STRICT_MODE: bool = False
    AUTO_BLOCK: bool = True
    MAX_GATE_NAME_LENGTH: int = 255
    MAX_HISTORY_SIZE: int = 1000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
