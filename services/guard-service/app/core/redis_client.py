"""
Redis Client

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import json
from typing import Optional, Any
import redis.asyncio as redis

from app.core.config import settings


class RedisClient:
    """Redis client wrapper"""

    def __init__(self):
        self.client: Optional[redis.Redis] = None

    async def connect(self):
        """Connect to Redis"""
        self.client = await redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )

    async def disconnect(self):
        """Disconnect from Redis"""
        if self.client:
            await self.client.close()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis"""
        if not self.client:
            return None
        value = await self.client.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in Redis"""
        if not self.client:
            return
        await self.client.set(
            key,
            json.dumps(value, default=str),
            ex=ttl or settings.REDIS_CACHE_TTL
        )

    async def delete(self, key: str):
        """Delete key from Redis"""
        if not self.client:
            return
        await self.client.delete(key)

    async def keys(self, pattern: str) -> list[str]:
        """Get keys matching pattern"""
        if not self.client:
            return []
        return await self.client.keys(pattern)

    async def lpush(self, key: str, value: Any):
        """Push to list"""
        if not self.client:
            return
        await self.client.lpush(key, json.dumps(value, default=str))

    async def lrange(self, key: str, start: int, end: int) -> list[Any]:
        """Get range from list"""
        if not self.client:
            return []
        values = await self.client.lrange(key, start, end)
        return [json.loads(v) for v in values]

    async def ltrim(self, key: str, start: int, end: int):
        """Trim list"""
        if not self.client:
            return
        await self.client.ltrim(key, start, end)

    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.client:
            return False
        return await self.client.exists(key) > 0


# Global Redis client instance
redis_client = RedisClient()


async def get_redis() -> RedisClient:
    """Dependency for Redis client"""
    return redis_client
