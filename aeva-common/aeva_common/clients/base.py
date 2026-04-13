"""
AEVA Base Service Client

Base HTTP client for AEVA microservices.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Dict, Any, Optional
import httpx


class ServiceError(Exception):
    """Service call error"""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Service error {status_code}: {message}")


class ServiceTimeout(Exception):
    """Service timeout error"""
    pass


class BaseServiceClient:
    """
    Base HTTP client for AEVA services

    Provides common HTTP operations with error handling,
    timeout management, and retry logic.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        retries: int = 3
    ):
        """
        Initialize service client

        Args:
            base_url: Service base URL (e.g., http://bench-service:8001)
            timeout: Request timeout in seconds
            retries: Number of retry attempts
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self.client = httpx.AsyncClient(timeout=timeout)

    async def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send GET request

        Args:
            path: API endpoint path
            params: Query parameters

        Returns:
            response: JSON response data

        Raises:
            ServiceError: On HTTP error
            ServiceTimeout: On timeout
        """
        url = f"{self.base_url}{path}"
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            raise ServiceTimeout(f"Request to {url} timed out")
        except httpx.HTTPStatusError as e:
            raise ServiceError(e.response.status_code, str(e))

    async def post(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send POST request

        Args:
            path: API endpoint path
            json: JSON request body
            data: Form data

        Returns:
            response: JSON response data

        Raises:
            ServiceError: On HTTP error
            ServiceTimeout: On timeout
        """
        url = f"{self.base_url}{path}"
        try:
            response = await self.client.post(url, json=json, data=data)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            raise ServiceTimeout(f"Request to {url} timed out")
        except httpx.HTTPStatusError as e:
            raise ServiceError(e.response.status_code, str(e))

    async def put(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send PUT request

        Args:
            path: API endpoint path
            json: JSON request body

        Returns:
            response: JSON response data

        Raises:
            ServiceError: On HTTP error
            ServiceTimeout: On timeout
        """
        url = f"{self.base_url}{path}"
        try:
            response = await self.client.put(url, json=json)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            raise ServiceTimeout(f"Request to {url} timed out")
        except httpx.HTTPStatusError as e:
            raise ServiceError(e.response.status_code, str(e))

    async def delete(self, path: str) -> Dict[str, Any]:
        """
        Send DELETE request

        Args:
            path: API endpoint path

        Returns:
            response: JSON response data

        Raises:
            ServiceError: On HTTP error
            ServiceTimeout: On timeout
        """
        url = f"{self.base_url}{path}"
        try:
            response = await self.client.delete(url)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            raise ServiceTimeout(f"Request to {url} timed out")
        except httpx.HTTPStatusError as e:
            raise ServiceError(e.response.status_code, str(e))

    async def health_check(self) -> bool:
        """
        Check service health

        Returns:
            healthy: True if service is healthy
        """
        try:
            response = await self.get("/health")
            return response.get("status") == "healthy"
        except:
            return False

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

    async def __aenter__(self):
        """Context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        await self.close()
