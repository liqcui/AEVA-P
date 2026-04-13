"""
Rate Limiting Middleware

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import time
from collections import defaultdict
from typing import Dict

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware"""

    def __init__(self, app):
        super().__init__(app)
        self.requests: Dict[str, list] = defaultdict(list)
        self.limit = settings.RATE_LIMIT_PER_MINUTE
        self.window = 60  # 1 minute in seconds

    async def dispatch(self, request: Request, call_next):
        if not settings.ENABLE_RATE_LIMITING:
            return await call_next(request)

        # Get client identifier (IP address)
        client_ip = request.client.host

        # Clean old requests
        current_time = time.time()
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < self.window
        ]

        # Check rate limit
        if len(self.requests[client_ip]) >= self.limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {self.limit} requests per minute."
            )

        # Add current request
        self.requests[client_ip].append(current_time)

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.limit)
        response.headers["X-RateLimit-Remaining"] = str(
            max(0, self.limit - len(self.requests[client_ip]))
        )

        return response
