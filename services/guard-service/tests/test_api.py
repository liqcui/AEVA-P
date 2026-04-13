"""
Guard Service API Tests

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from app.main import app
from app.models.gate import Gate, GateStatus, ValidationResult
from app.core.redis_client import RedisClient


@pytest.fixture
def mock_redis():
    """Mock Redis client for testing"""
    redis = AsyncMock(spec=RedisClient)
    return redis


@pytest.fixture
def sample_gate():
    """Sample gate for testing"""
    return Gate(
        name="test_gate",
        description="Test quality gate",
        threshold=0.85,
        metrics=["accuracy", "f1_score"],
        strict_mode=False,
        auto_block=True,
    )


@pytest.fixture
def sample_validation_result(sample_gate):
    """Sample validation result for testing"""
    return ValidationResult(
        gate_id=sample_gate.id,
        passed=True,
        score=0.90,
        threshold=0.85,
        blocked=False,
        reason=None,
        metrics={"accuracy": 0.92, "f1_score": 0.88},
        metadata={"model": "test"},
    )


@pytest.mark.asyncio
async def test_create_gate(mock_redis, sample_gate):
    """Test creating a new gate"""
    with patch("app.api.v1.endpoints.gates.get_redis", return_value=mock_redis):
        with patch("app.services.gate_service.GateService.create_gate", return_value=sample_gate):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post(
                    "/v1/gate/",
                    json={
                        "name": "test_gate",
                        "description": "Test quality gate",
                        "threshold": 0.85,
                        "metrics": ["accuracy", "f1_score"],
                        "strict_mode": False,
                        "auto_block": True,
                    }
                )
                assert response.status_code == 201
                data = response.json()
                assert data["name"] == "test_gate"
                assert data["threshold"] == 0.85


@pytest.mark.asyncio
async def test_get_gate(mock_redis, sample_gate):
    """Test getting a gate by ID"""
    with patch("app.api.v1.endpoints.gates.get_redis", return_value=mock_redis):
        with patch("app.services.gate_service.GateService.get_gate", return_value=sample_gate):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get(f"/v1/gate/{sample_gate.id}")
                assert response.status_code == 200
                data = response.json()
                assert data["name"] == "test_gate"


@pytest.mark.asyncio
async def test_get_gate_not_found(mock_redis):
    """Test getting a non-existent gate"""
    gate_id = uuid4()
    with patch("app.api.v1.endpoints.gates.get_redis", return_value=mock_redis):
        with patch("app.services.gate_service.GateService.get_gate", return_value=None):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get(f"/v1/gate/{gate_id}")
                assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_gates(mock_redis, sample_gate):
    """Test listing all gates"""
    gates = [sample_gate]
    with patch("app.api.v1.endpoints.gates.get_redis", return_value=mock_redis):
        with patch("app.services.gate_service.GateService.list_gates", return_value=gates):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/v1/gate/")
                assert response.status_code == 200
                data = response.json()
                assert data["total"] == 1
                assert len(data["gates"]) == 1


@pytest.mark.asyncio
async def test_update_gate(mock_redis, sample_gate):
    """Test updating a gate"""
    updated_gate = sample_gate.model_copy()
    updated_gate.threshold = 0.90

    with patch("app.api.v1.endpoints.gates.get_redis", return_value=mock_redis):
        with patch("app.services.gate_service.GateService.update_gate", return_value=updated_gate):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.put(
                    f"/v1/gate/{sample_gate.id}",
                    json={"threshold": 0.90}
                )
                assert response.status_code == 200
                data = response.json()
                assert data["threshold"] == 0.90


@pytest.mark.asyncio
async def test_delete_gate(mock_redis, sample_gate):
    """Test deleting a gate"""
    with patch("app.api.v1.endpoints.gates.get_redis", return_value=mock_redis):
        with patch("app.services.gate_service.GateService.delete_gate", return_value=True):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.delete(f"/v1/gate/{sample_gate.id}")
                assert response.status_code == 204


@pytest.mark.asyncio
async def test_validate_metrics_pass(mock_redis, sample_gate, sample_validation_result):
    """Test validating metrics that pass the gate"""
    with patch("app.api.v1.endpoints.gates.get_redis", return_value=mock_redis):
        with patch("app.services.gate_service.GateService.validate", return_value=sample_validation_result):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post(
                    f"/v1/gate/{sample_gate.id}/validate",
                    json={
                        "metrics": {
                            "accuracy": 0.92,
                            "f1_score": 0.88
                        },
                        "metadata": {"model": "test"}
                    }
                )
                assert response.status_code == 200
                data = response.json()
                assert data["passed"] is True
                assert data["blocked"] is False
                assert data["score"] == 0.90


@pytest.mark.asyncio
async def test_validate_metrics_fail(mock_redis, sample_gate):
    """Test validating metrics that fail the gate"""
    failed_result = ValidationResult(
        gate_id=sample_gate.id,
        passed=False,
        score=0.75,
        threshold=0.85,
        blocked=True,
        reason="Score 0.7500 below threshold 0.85",
        metrics={"accuracy": 0.80, "f1_score": 0.70},
        metadata={},
    )

    with patch("app.api.v1.endpoints.gates.get_redis", return_value=mock_redis):
        with patch("app.services.gate_service.GateService.validate", return_value=failed_result):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post(
                    f"/v1/gate/{sample_gate.id}/validate",
                    json={
                        "metrics": {
                            "accuracy": 0.80,
                            "f1_score": 0.70
                        }
                    }
                )
                assert response.status_code == 200
                data = response.json()
                assert data["passed"] is False
                assert data["blocked"] is True


@pytest.mark.asyncio
async def test_get_history(mock_redis, sample_gate, sample_validation_result):
    """Test getting validation history"""
    history = [sample_validation_result]

    with patch("app.api.v1.endpoints.gates.get_redis", return_value=mock_redis):
        with patch("app.services.gate_service.GateService.get_history", return_value=history):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get(f"/v1/gate/{sample_gate.id}/history")
                assert response.status_code == 200
                data = response.json()
                assert len(data) == 1
                assert data[0]["passed"] is True


@pytest.mark.asyncio
async def test_get_statistics(mock_redis, sample_gate):
    """Test getting gate statistics"""
    stats = {
        "gate_id": str(sample_gate.id),
        "gate_name": "test_gate",
        "total_validations": 100,
        "passed_validations": 85,
        "failed_validations": 12,
        "blocked_validations": 3,
        "success_rate": 85.0,
        "block_rate": 3.0,
    }

    with patch("app.api.v1.endpoints.gates.get_redis", return_value=mock_redis):
        with patch("app.services.gate_service.GateService.get_statistics", return_value=stats):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get(f"/v1/gate/{sample_gate.id}/statistics")
                assert response.status_code == 200
                data = response.json()
                assert data["total_validations"] == 100
                assert data["success_rate"] == 85.0


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_root():
    """Test root endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data
