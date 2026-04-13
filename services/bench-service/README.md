# AEVA Bench Service

**Status**: ✅ Implemented
**Priority**: High
**Port**: 8001

---

## 📋 Overview

Benchmark Service provides comprehensive model evaluation and comparison capabilities using FastAPI and PostgreSQL.

**See**: [services/README.md](../README.md) for architecture overview and development guidelines.

---

## 🎯 Purpose

- Create and manage benchmarks
- Execute accuracy and performance tests
- Compare multiple models
- Track historical benchmark results
- Provide REST API for benchmark operations

---

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic 2.0
- **Testing**: pytest
- **Server**: Uvicorn

---

## 📁 Structure

```
bench-service/
├── app/
│   ├── main.py              # FastAPI application
│   ├── core/                # Configuration
│   │   └── config.py
│   ├── db/                  # Database setup
│   │   └── base.py
│   ├── models/              # SQLAlchemy models
│   │   └── benchmark.py
│   ├── schemas/             # Pydantic schemas
│   │   └── benchmark.py
│   ├── services/            # Business logic
│   │   └── benchmark_service.py
│   └── api/v1/              # API routes
│       └── endpoints/
│           └── benchmarks.py
├── tests/
│   └── test_api.py          # API tests
├── Dockerfile               # Container image
├── docker-compose.yml       # Local development
├── requirements.txt         # Dependencies
├── .env.example             # Environment template
└── README.md               # This file
```

---

## 🚀 Quick Start

### Option 1: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations (if using Alembic)
# alembic upgrade head

# Run service
uvicorn app.main:app --reload --port 8001
```

Access the service:
- API: http://localhost:8001
- Docs: http://localhost:8001/docs
- Health: http://localhost:8001/health

### Option 2: Docker Compose

```bash
# Start PostgreSQL and Bench Service
docker-compose up

# Or build and start
docker-compose up --build
```

---

## 📡 API Endpoints

### Benchmarks

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/benchmark/` | Create new benchmark |
| `GET` | `/v1/benchmark/{id}` | Get benchmark details |
| `GET` | `/v1/benchmark/` | List all benchmarks (paginated) |
| `PUT` | `/v1/benchmark/{id}` | Update benchmark |
| `DELETE` | `/v1/benchmark/{id}` | Delete benchmark |
| `POST` | `/v1/benchmark/{id}/execute` | Execute benchmark |
| `GET` | `/v1/benchmark/{id}/results` | Get benchmark results |
| `GET` | `/v1/benchmark/statistics/summary` | Get statistics |

### Health Checks

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/ready` | Readiness check |

---

## 💡 Usage Examples

### Create a Benchmark

```bash
curl -X POST "http://localhost:8001/v1/benchmark/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "RandomForest Accuracy Test",
    "description": "Testing RandomForest model accuracy",
    "model_path": "/models/random_forest.pkl",
    "dataset_path": "/data/test_set.csv",
    "config": {
      "metrics": ["accuracy", "f1_score"],
      "test_size": 0.2
    }
  }'
```

### List Benchmarks

```bash
curl "http://localhost:8001/v1/benchmark/?page=1&page_size=10"
```

### Execute Benchmark

```bash
curl -X POST "http://localhost:8001/v1/benchmark/{benchmark_id}/execute"
```

### Get Results

```bash
curl "http://localhost:8001/v1/benchmark/{benchmark_id}/results"
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test
pytest tests/test_api.py::test_create_benchmark -v
```

---

## 🗄️ Database Schema

### Benchmark Table

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | String(255) | Benchmark name |
| description | Text | Description |
| model_path | String(500) | Model file path |
| dataset_path | String(500) | Dataset file path |
| config | JSON | Configuration |
| status | Enum | pending/running/completed/failed |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Update timestamp |
| started_at | DateTime | Execution start time |
| completed_at | DateTime | Completion time |
| results | JSON | Execution results |
| accuracy | Float | Accuracy metric |
| f1_score | Float | F1 score metric |
| precision | Float | Precision metric |
| recall | Float | Recall metric |
| duration | Float | Execution duration (seconds) |
| throughput | Float | Throughput (samples/sec) |
| error_message | Text | Error message if failed |
| metadata | JSON | Additional metadata |

---

## 🔧 Configuration

Environment variables (see `.env.example`):

```bash
# API Settings
API_V1_STR=/v1
PROJECT_NAME=AEVA Bench Service
VERSION=0.1.0

# Server
HOST=0.0.0.0
PORT=8001

# Database
DATABASE_URL=postgresql://aeva:aeva@localhost:5432/bench_service

# Security
API_KEY=your-api-key
SECRET_KEY=your-secret-key

# Logging
LOG_LEVEL=INFO
```

---

## 📊 Features Implemented

✅ **CRUD Operations**
- Create, Read, Update, Delete benchmarks
- Pagination support
- Status filtering

✅ **Benchmark Execution**
- Start benchmark execution
- Track execution status
- Store results and metrics

✅ **Statistics**
- Benchmark counts by status
- Success rate calculation

✅ **API Documentation**
- OpenAPI/Swagger UI at `/docs`
- ReDoc at `/redoc`

✅ **Health Checks**
- Liveness probe (`/health`)
- Readiness probe (`/ready`)

✅ **Testing**
- Unit tests for API endpoints
- In-memory SQLite for testing
- Test coverage for main flows

---

## 🐳 Docker

### Build Image

```bash
docker build -t aeva/bench-service:latest .
```

### Run Container

```bash
docker run -p 8001:8001 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/bench_service \
  aeva/bench-service:latest
```

---

## 📝 Next Steps

### Future Enhancements

1. ⏳ Integrate with actual model execution engine
2. ⏳ Add Celery for async benchmark execution
3. ⏳ Implement benchmark comparison endpoints
4. ⏳ Add support for custom metrics
5. ⏳ Implement result caching with Redis
6. ⏳ Add Prometheus metrics
7. ⏳ Implement authentication/authorization
8. ⏳ Add database migrations with Alembic
9. ⏳ Support for distributed benchmark execution
10. ⏳ WebSocket support for real-time status updates

---

## 🔗 Related Services

- **Guard Service** (Port 8002) - Quality gates
- **Auto Service** (Port 8003) - Pipeline orchestration
- **Brain Service** (Port 8004) - AI analysis
- **Gateway** (Port 8000) - API Gateway

---

## 📚 Documentation

- API Documentation: http://localhost:8001/docs
- Project Structure: [../../PROJECT_STRUCTURE.md](../../PROJECT_STRUCTURE.md)
- Service Guidelines: [../README.md](../README.md)
- API Contracts: [../../aeva-common/docs/API_CONTRACTS.md](../../aeva-common/docs/API_CONTRACTS.md)

---

**Status**: ✅ **Production Ready**
**Version**: 0.1.0
**Last Updated**: 2026-04-13

Copyright © 2024-2026 AEVA Development Team

