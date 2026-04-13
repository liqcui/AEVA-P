"""
AEVA Base Configuration

Shared infrastructure configuration schemas.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Optional
from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    """Database configuration"""
    host: str = "localhost"
    port: int = 5432
    database: str = "aeva"
    username: str = "aeva"
    password: str = ""
    pool_size: int = 10

    def get_connection_string(self) -> str:
        """Generate PostgreSQL connection string"""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class RedisConfig(BaseModel):
    """Redis configuration"""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None

    def get_connection_string(self) -> str:
        """Generate Redis connection string"""
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"
