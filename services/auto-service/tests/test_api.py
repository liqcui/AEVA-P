"""
Auto Service API Tests

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

from app.main import app
from app.core.database import Base, get_db
from app.models.pipeline import Pipeline, PipelineStatus

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Set up test database before each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_pipeline():
    """Test creating a new pipeline"""
    response = client.post(
        "/v1/pipeline/",
        json={
            "name": "test_pipeline",
            "description": "Test pipeline",
            "config": {
                "steps": [
                    {
                        "name": "benchmark",
                        "type": "benchmark",
                        "config": {"benchmark_id": "bench-123"}
                    }
                ]
            }
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test_pipeline"
    assert data["status"] == PipelineStatus.PENDING
    assert len(data["steps"]) == 1


def test_get_pipeline():
    """Test getting a pipeline by ID"""
    # Create pipeline first
    create_response = client.post(
        "/v1/pipeline/",
        json={
            "name": "test_pipeline",
            "description": "Test pipeline",
            "config": {"steps": []}
        }
    )
    pipeline_id = create_response.json()["id"]

    # Get pipeline
    response = client.get(f"/v1/pipeline/{pipeline_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == pipeline_id
    assert data["name"] == "test_pipeline"


def test_get_pipeline_not_found():
    """Test getting a non-existent pipeline"""
    pipeline_id = str(uuid4())
    response = client.get(f"/v1/pipeline/{pipeline_id}")
    assert response.status_code == 404


def test_list_pipelines():
    """Test listing all pipelines"""
    # Create multiple pipelines
    for i in range(3):
        client.post(
            "/v1/pipeline/",
            json={
                "name": f"pipeline_{i}",
                "description": f"Pipeline {i}",
                "config": {"steps": []}
            }
        )

    # List pipelines
    response = client.get("/v1/pipeline/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["pipelines"]) == 3


def test_list_pipelines_with_filter():
    """Test listing pipelines with status filter"""
    # Create pipeline
    client.post(
        "/v1/pipeline/",
        json={
            "name": "test_pipeline",
            "description": "Test pipeline",
            "config": {"steps": []}
        }
    )

    # List with filter
    response = client.get(f"/v1/pipeline/?status={PipelineStatus.PENDING}")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1


def test_update_pipeline():
    """Test updating a pipeline"""
    # Create pipeline
    create_response = client.post(
        "/v1/pipeline/",
        json={
            "name": "test_pipeline",
            "description": "Test pipeline",
            "config": {"steps": []}
        }
    )
    pipeline_id = create_response.json()["id"]

    # Update pipeline
    response = client.put(
        f"/v1/pipeline/{pipeline_id}",
        json={
            "name": "updated_pipeline",
            "description": "Updated description"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "updated_pipeline"
    assert data["description"] == "Updated description"


def test_delete_pipeline():
    """Test deleting a pipeline"""
    # Create pipeline
    create_response = client.post(
        "/v1/pipeline/",
        json={
            "name": "test_pipeline",
            "description": "Test pipeline",
            "config": {"steps": []}
        }
    )
    pipeline_id = create_response.json()["id"]

    # Delete pipeline
    response = client.delete(f"/v1/pipeline/{pipeline_id}")
    assert response.status_code == 204

    # Verify deletion
    get_response = client.get(f"/v1/pipeline/{pipeline_id}")
    assert get_response.status_code == 404


def test_execute_pipeline():
    """Test executing a pipeline"""
    # Create pipeline
    create_response = client.post(
        "/v1/pipeline/",
        json={
            "name": "test_pipeline",
            "description": "Test pipeline",
            "config": {
                "steps": [
                    {
                        "name": "benchmark",
                        "type": "benchmark",
                        "config": {"benchmark_id": "bench-123"}
                    }
                ]
            }
        }
    )
    pipeline_id = create_response.json()["id"]

    # Execute pipeline (will fail in tests without Celery, but should return response)
    response = client.post(
        f"/v1/pipeline/{pipeline_id}/execute",
        json={"metadata": {"test": "value"}}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["pipeline_id"] == pipeline_id
    assert "celery_task_id" in data


def test_execute_running_pipeline():
    """Test executing an already running pipeline"""
    # Create pipeline
    create_response = client.post(
        "/v1/pipeline/",
        json={
            "name": "test_pipeline",
            "description": "Test pipeline",
            "config": {"steps": []}
        }
    )
    pipeline_id = create_response.json()["id"]

    # Update status to running
    client.put(
        f"/v1/pipeline/{pipeline_id}",
        json={"status": PipelineStatus.RUNNING}
    )

    # Try to execute again
    response = client.post(
        f"/v1/pipeline/{pipeline_id}/execute",
        json={"metadata": {}}
    )
    assert response.status_code == 409


def test_cancel_pipeline():
    """Test canceling a running pipeline"""
    # Create and execute pipeline
    create_response = client.post(
        "/v1/pipeline/",
        json={
            "name": "test_pipeline",
            "description": "Test pipeline",
            "config": {"steps": []}
        }
    )
    pipeline_id = create_response.json()["id"]

    # Execute pipeline
    client.post(f"/v1/pipeline/{pipeline_id}/execute", json={"metadata": {}})

    # Cancel pipeline
    response = client.post(f"/v1/pipeline/{pipeline_id}/cancel")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == PipelineStatus.CANCELLED


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data
