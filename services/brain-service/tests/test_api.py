"""
Brain Service API Tests

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
from app.models.analysis import AnalysisType, AnalysisStatus

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


def test_create_analysis():
    """Test creating a new analysis"""
    response = client.post(
        "/v1/analysis/",
        json={
            "analysis_type": "basic",
            "input_data": {
                "metrics": {
                    "accuracy": 0.95,
                    "precision": 0.93
                }
            },
            "config": {
                "include_recommendations": True
            }
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["analysis_type"] == AnalysisType.BASIC
    assert data["status"] in [AnalysisStatus.PENDING, AnalysisStatus.PROCESSING]


def test_get_analysis():
    """Test getting an analysis by ID"""
    # Create analysis first
    create_response = client.post(
        "/v1/analysis/",
        json={
            "analysis_type": "comprehensive",
            "input_data": {"metrics": {"accuracy": 0.90}},
            "config": {}
        }
    )
    analysis_id = create_response.json()["id"]

    # Get analysis
    response = client.get(f"/v1/analysis/{analysis_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == analysis_id
    assert data["analysis_type"] == AnalysisType.COMPREHENSIVE


def test_get_analysis_not_found():
    """Test getting a non-existent analysis"""
    analysis_id = str(uuid4())
    response = client.get(f"/v1/analysis/{analysis_id}")
    assert response.status_code == 404


def test_list_analyses():
    """Test listing all analyses"""
    # Create multiple analyses
    for analysis_type in ["basic", "comprehensive", "diagnostic"]:
        client.post(
            "/v1/analysis/",
            json={
                "analysis_type": analysis_type,
                "input_data": {"metrics": {"accuracy": 0.90}},
                "config": {}
            }
        )

    # List analyses
    response = client.get("/v1/analysis/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["analyses"]) == 3


def test_list_analyses_with_type_filter():
    """Test listing analyses with type filter"""
    # Create analyses
    client.post(
        "/v1/analysis/",
        json={
            "analysis_type": "basic",
            "input_data": {"metrics": {}},
            "config": {}
        }
    )
    client.post(
        "/v1/analysis/",
        json={
            "analysis_type": "comprehensive",
            "input_data": {"metrics": {}},
            "config": {}
        }
    )

    # List with filter
    response = client.get(f"/v1/analysis/?type={AnalysisType.BASIC}")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1


def test_delete_analysis():
    """Test deleting an analysis"""
    # Create analysis
    create_response = client.post(
        "/v1/analysis/",
        json={
            "analysis_type": "basic",
            "input_data": {"metrics": {}},
            "config": {}
        }
    )
    analysis_id = create_response.json()["id"]

    # Delete analysis
    response = client.delete(f"/v1/analysis/{analysis_id}")
    assert response.status_code == 204

    # Verify deletion
    get_response = client.get(f"/v1/analysis/{analysis_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_quick_analysis():
    """Test quick analysis endpoint"""
    response = client.post(
        "/v1/analysis/quick",
        json={
            "analysis_type": "basic",
            "data": {
                "metrics": {
                    "accuracy": 0.95,
                    "precision": 0.93,
                    "recall": 0.92
                }
            },
            "config": {
                "include_recommendations": True
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["analysis_type"] == AnalysisType.BASIC
    assert "summary" in data
    assert "findings" in data
    assert "recommendations" in data
    assert "confidence_score" in data
    assert "processing_time" in data


def test_reprocess_analysis():
    """Test reprocessing an analysis"""
    # Create analysis
    create_response = client.post(
        "/v1/analysis/",
        json={
            "analysis_type": "basic",
            "input_data": {"metrics": {"accuracy": 0.90}},
            "config": {}
        }
    )
    analysis_id = create_response.json()["id"]

    # Reprocess analysis
    response = client.post(f"/v1/analysis/{analysis_id}/reprocess")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == analysis_id
    assert data["status"] == AnalysisStatus.PENDING


def test_reprocess_nonexistent_analysis():
    """Test reprocessing a non-existent analysis"""
    analysis_id = str(uuid4())
    response = client.post(f"/v1/analysis/{analysis_id}/reprocess")
    assert response.status_code == 404


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "llm_provider" in data
    assert "llm_model" in data


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data
    assert "llm_provider" in data
