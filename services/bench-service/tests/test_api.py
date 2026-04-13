"""
API Tests for Bench Service

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db import Base, get_db

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_benchmark():
    """Test creating a benchmark"""
    response = client.post(
        "/v1/benchmark/",
        json={
            "name": "Test Benchmark",
            "description": "A test benchmark",
            "model_path": "/models/test.pkl",
            "dataset_path": "/data/test.csv",
            "config": {"metrics": ["accuracy"]},
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Benchmark"
    assert data["status"] == "pending"
    assert "id" in data


def test_get_benchmark():
    """Test getting a benchmark"""
    # Create a benchmark first
    create_response = client.post(
        "/v1/benchmark/",
        json={
            "name": "Test Benchmark 2",
            "model_path": "/models/test2.pkl",
        },
    )
    benchmark_id = create_response.json()["id"]

    # Get the benchmark
    response = client.get(f"/v1/benchmark/{benchmark_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == benchmark_id
    assert data["name"] == "Test Benchmark 2"


def test_list_benchmarks():
    """Test listing benchmarks"""
    # Create a few benchmarks
    for i in range(3):
        client.post(
            "/v1/benchmark/",
            json={
                "name": f"Test Benchmark {i}",
                "model_path": f"/models/test{i}.pkl",
            },
        )

    # List benchmarks
    response = client.get("/v1/benchmark/")
    assert response.status_code == 200
    data = response.json()
    assert "benchmarks" in data
    assert "total" in data
    assert data["total"] >= 3


def test_update_benchmark():
    """Test updating a benchmark"""
    # Create a benchmark
    create_response = client.post(
        "/v1/benchmark/",
        json={
            "name": "Original Name",
            "model_path": "/models/test.pkl",
        },
    )
    benchmark_id = create_response.json()["id"]

    # Update the benchmark
    response = client.put(
        f"/v1/benchmark/{benchmark_id}",
        json={
            "name": "Updated Name",
            "description": "Updated description",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["description"] == "Updated description"


def test_delete_benchmark():
    """Test deleting a benchmark"""
    # Create a benchmark
    create_response = client.post(
        "/v1/benchmark/",
        json={
            "name": "To Delete",
            "model_path": "/models/test.pkl",
        },
    )
    benchmark_id = create_response.json()["id"]

    # Delete the benchmark
    response = client.delete(f"/v1/benchmark/{benchmark_id}")
    assert response.status_code == 204

    # Verify it's deleted
    get_response = client.get(f"/v1/benchmark/{benchmark_id}")
    assert get_response.status_code == 404


def test_execute_benchmark():
    """Test executing a benchmark"""
    # Create a benchmark
    create_response = client.post(
        "/v1/benchmark/",
        json={
            "name": "Execute Test",
            "model_path": "/models/test.pkl",
        },
    )
    benchmark_id = create_response.json()["id"]

    # Execute the benchmark
    response = client.post(f"/v1/benchmark/{benchmark_id}/execute")
    assert response.status_code == 200
    data = response.json()
    assert data["benchmark_id"] == benchmark_id
    assert data["status"] in ["completed", "running"]


def test_get_statistics():
    """Test getting benchmark statistics"""
    response = client.get("/v1/benchmark/statistics/summary")
    assert response.status_code == 200
    data = response.json()
    assert "statistics" in data
    assert "success_rate" in data
