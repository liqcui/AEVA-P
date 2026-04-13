"""
Service Client for Backend Communication

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import httpx
from typing import Dict, Any, Optional
from fastapi import HTTPException, status

from app.core.config import settings


class ServiceClient:
    """Client for communicating with backend services"""

    def __init__(self):
        self.timeout = settings.REQUEST_TIMEOUT
        self.max_retries = settings.MAX_RETRIES
        self.retry_delay = settings.RETRY_DELAY

    async def request(
        self,
        method: str,
        service_url: str,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to backend service.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            service_url: Base URL of the service
            path: API path
            json_data: JSON body data
            params: Query parameters
            headers: HTTP headers

        Returns:
            Response data

        Raises:
            HTTPException: If request fails
        """
        url = f"{service_url}{path}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    json=json_data,
                    params=params,
                    headers=headers
                )

                # Handle different status codes
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 201:
                    return response.json()
                elif response.status_code == 204:
                    return {"message": "Success"}
                elif response.status_code == 404:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=response.json().get("detail", "Resource not found")
                    )
                elif response.status_code == 400:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=response.json().get("detail", "Bad request")
                    )
                elif response.status_code == 409:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=response.json().get("detail", "Conflict")
                    )
                elif response.status_code >= 500:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail=f"Service temporarily unavailable"
                    )
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=response.json().get("detail", "Unknown error")
                    )

            except httpx.TimeoutException:
                raise HTTPException(
                    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                    detail=f"Service request timed out"
                )
            except httpx.ConnectError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Unable to connect to service"
                )
            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"HTTP error: {str(e)}"
                )

    async def get(self, service_url: str, path: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET request"""
        return await self.request("GET", service_url, path, params=params)

    async def post(self, service_url: str, path: str, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """POST request"""
        return await self.request("POST", service_url, path, json_data=json_data)

    async def put(self, service_url: str, path: str, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """PUT request"""
        return await self.request("PUT", service_url, path, json_data=json_data)

    async def delete(self, service_url: str, path: str) -> Dict[str, Any]:
        """DELETE request"""
        return await self.request("DELETE", service_url, path)


# Global service client instance
service_client = ServiceClient()
