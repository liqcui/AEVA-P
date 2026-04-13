"""
Brain Service Configuration

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = "AEVA Brain Service"

    # Database Configuration
    DATABASE_URL: str = "postgresql://aeva:aeva@localhost:5432/brain_service"

    # LLM Configuration
    LLM_PROVIDER: str = "openai"  # openai, anthropic, ollama
    LLM_MODEL: str = "gpt-4"
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = ""  # For custom endpoints
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2000

    # Service URLs
    BENCH_SERVICE_URL: str = "http://localhost:8001"
    GUARD_SERVICE_URL: str = "http://localhost:8002"

    # Analysis Configuration
    MAX_CONTEXT_LENGTH: int = 8000
    ENABLE_CACHING: bool = True
    CACHE_TTL: int = 3600  # seconds

    class Config:
        env_file = ".env"


settings = Settings()
