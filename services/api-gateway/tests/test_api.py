"""
API Gateway Tests

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.main import app

# Create test client
client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "services" in data
    assert "bench" in data["services"]
    assert "guard" in data["services"]
    assert "auto" in data["services"]
    assert "brain" in data["services"]


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data
    assert "endpoints" in data
    assert "benchmark" in data["endpoints"]
    assert "gate" in data["endpoints"]
    assert "pipeline" in data["endpoints"]
    assert "analysis" in data["endpoints"]


@pytest.mark.asyncio
async def test_benchmark_proxy():
    """Test benchmark service proxy"""
    mock_response = {"id": "test-123", "name": "test_benchmark"}

    with patch("app.core.service_client.service_client.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        response = client.post(
            "/api/v1/benchmark/",
            json={"name": "test_benchmark"}
        )
        assert response.status_code == 200
        assert response.json() == mock_response


@pytest.mark.asyncio
async def test_gate_proxy():
    """Test gate service proxy"""
    mock_response = {"id": "gate-123", "name": "test_gate"}

    with patch("app.core.service_client.service_client.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        response = client.post(
            "/api/v1/gate/",
            json={"name": "test_gate", "threshold": 0.85}
        )
        assert response.status_code == 200
        assert response.json() == mock_response


@pytest.mark.asyncio
async def test_pipeline_proxy():
    """Test pipeline service proxy"""
    mock_response = {"id": "pipeline-123", "name": "test_pipeline"}

    with patch("app.core.service_client.service_client.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        response = client.post(
            "/api/v1/pipeline/",
            json={"name": "test_pipeline", "config": {}}
        )
        assert response.status_code == 200
        assert response.json() == mock_response


@pytest.mark.asyncio
async def test_analysis_proxy():
    """Test analysis service proxy"""
    mock_response = {"id": "analysis-123", "analysis_type": "basic"}

    with patch("app.core.service_client.service_client.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        response = client.post(
            "/api/v1/analysis/",
            json={"analysis_type": "basic", "input_data": {}}
        )
        assert response.status_code == 200
        assert response.json() == mock_response


@pytest.mark.asyncio
async def test_get_benchmark():
    """Test GET benchmark endpoint"""
    mock_response = {"id": "test-123", "name": "test_benchmark"}

    with patch("app.core.service_client.service_client.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response

        response = client.get("/api/v1/benchmark/test-123")
        assert response.status_code == 200
        assert response.json() == mock_response


@pytest.mark.asyncio
async def test_list_benchmarks():
    """Test list benchmarks endpoint"""
    mock_response = {"benchmarks": [], "total": 0}

    with patch("app.core.service_client.service_client.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response

        response = client.get("/api/v1/benchmark/")
        assert response.status_code == 200
        assert response.json() == mock_response


@pytest.mark.asyncio
async def test_delete_benchmark():
    """Test DELETE benchmark endpoint"""
    mock_response = {"message": "Success"}

    with patch("app.core.service_client.service_client.delete", new_callable=AsyncMock) as mock_delete:
        mock_delete.return_value = mock_response

        response = client.delete("/api/v1/benchmark/test-123")
        assert response.status_code == 200
        assert response.json() == mock_response


def test_rate_limiting_headers():
    """Test rate limiting headers are present"""
    response = client.get("/health")
    assert response.status_code == 200
    # Rate limit headers should be present if rate limiting is enabled
    if "X-RateLimit-Limit" in response.headers:
        assert "X-RateLimit-Remaining" in response.headers


def test_cors_headers():
    """Test CORS headers"""
    response = client.options("/api/v1/benchmark/")
    assert "access-control-allow-origin" in response.headers


def test_openapi_docs():
    """Test OpenAPI documentation is accessible"""
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "paths" in data
