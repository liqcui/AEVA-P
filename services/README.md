# AEVA Microservices

**Project**: AEVA v2.0 - Microservices Architecture
**Date**: 2026-04-13
**Project ID**: AEVA-2026-LQC-dc68e33

---

## 📦 Service Directory Structure

This directory contains all AEVA microservices implementations.

```
services/
├── bench-service/       # 🏆 Benchmark Service (Port 8001)
├── guard-service/       # 🛡️ Quality Gate Service (Port 8002)
├── auto-service/        # 🤖 Auto Pipeline Service (Port 8003)
├── brain-service/       # 🧠 AI Analysis Service (Port 8004)
└── gateway/             # 🌐 API Gateway (Port 8000)
```

---

## 🏗️ Service Overview

### 1. 🏆 Bench Service (Port 8001)
**Purpose**: Benchmark creation, execution, and comparison

**Tech Stack**:
- FastAPI - REST API framework
- PostgreSQL - Benchmark results storage
- SQLAlchemy - ORM
- Alembic - Database migrations

**Key Features**:
- Create and manage benchmarks
- Execute accuracy and performance tests
- Compare multiple models
- Historical benchmark tracking

**API Endpoints**:
- `POST /benchmark/create` - Create new benchmark
- `POST /benchmark/{id}/run` - Execute benchmark
- `GET /benchmark/{id}/results` - Get results
- `GET /benchmark/list` - List all benchmarks
- `DELETE /benchmark/{id}` - Delete benchmark

---

### 2. 🛡️ Guard Service (Port 8002)
**Purpose**: Quality gate validation and enforcement

**Tech Stack**:
- FastAPI - REST API framework
- Redis - Gate state and cache
- Celery - Async validation tasks (optional)

**Key Features**:
- Register quality gates
- Validate evaluation results
- Block/allow based on thresholds
- Gate validation history
- Real-time gate status

**API Endpoints**:
- `POST /gate/register` - Register quality gate
- `POST /gate/{id}/validate` - Validate result
- `GET /gate/{id}/status` - Get gate status
- `GET /gate/{id}/history` - Get validation history
- `PUT /gate/{id}` - Update gate config
- `DELETE /gate/{id}` - Delete gate

---

### 3. 🤖 Auto Service (Port 8003)
**Purpose**: Pipeline orchestration and workflow automation

**Tech Stack**:
- FastAPI - REST API framework
- Celery - Distributed task queue
- Redis - Celery backend
- PostgreSQL - Pipeline state storage

**Key Features**:
- Create multi-stage pipelines
- Execute workflows with dependencies
- Schedule periodic executions
- Monitor pipeline status
- Cancel running pipelines

**API Endpoints**:
- `POST /pipeline/create` - Create pipeline
- `POST /pipeline/{id}/execute` - Execute pipeline
- `GET /pipeline/execution/{id}/status` - Get status
- `GET /pipeline/execution/{id}/results` - Get results
- `POST /pipeline/{id}/schedule` - Schedule pipeline
- `POST /pipeline/execution/{id}/cancel` - Cancel execution

---

### 4. 🧠 Brain Service (Port 8004)
**Purpose**: AI-powered analysis and recommendations

**Tech Stack**:
- FastAPI - REST API framework
- Anthropic SDK - Claude API integration
- OpenAI SDK - GPT-4 API (optional)
- Redis - Response caching

**Key Features**:
- Intelligent failure analysis
- Root cause detection
- Improvement suggestions
- Batch analysis support
- Multiple LLM providers

**API Endpoints**:
- `POST /analyze` - Full analysis
- `POST /analyze/root-cause` - Root cause analysis
- `POST /analyze/suggestions` - Get recommendations
- `POST /analyze/batch` - Batch analysis

---

### 5. 🌐 API Gateway (Port 8000)
**Purpose**: Unified entry point for all services

**Tech Stack**:
- FastAPI - Gateway implementation
- httpx - Service communication
- Redis - Rate limiting & caching

**Key Features**:
- Request routing to services
- Load balancing
- Rate limiting
- Authentication & authorization
- Request/response logging
- API aggregation

**Routes**:
- `/v1/benchmark/*` → Bench Service (8001)
- `/v1/gate/*` → Guard Service (8002)
- `/v1/pipeline/*` → Auto Service (8003)
- `/v1/analyze/*` → Brain Service (8004)

---

## 📁 Standard Service Structure

Each service follows this structure:

```
service-name/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   └── endpoints/   # Endpoint handlers
│   │   └── deps.py          # Dependencies (DB, auth, etc.)
│   ├── core/                # Core logic
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration
│   │   └── security.py      # Auth & security
│   ├── models/              # Database models (SQLAlchemy)
│   │   └── __init__.py
│   ├── schemas/             # Pydantic schemas (request/response)
│   │   └── __init__.py
│   ├── services/            # Business logic
│   │   └── __init__.py
│   └── db/                  # Database utilities
│       ├── __init__.py
│       ├── base.py
│       └── session.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_services.py
├── alembic/                 # Database migrations (if needed)
│   ├── versions/
│   └── env.py
├── Dockerfile               # Container image
├── docker-compose.yml       # Local development
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md                # Service documentation
```

---

## 🔧 Development Workflow

### Local Development

1. **Start individual service**:
```bash
cd services/bench-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

2. **Run with Docker**:
```bash
cd services/bench-service
docker-compose up
```

3. **Run all services**:
```bash
# From project root
docker-compose -f deployments/docker-compose.yml up
```

---

## 🧪 Testing

### Unit Tests
```bash
cd services/bench-service
pytest tests/
```

### Integration Tests
```bash
cd services/bench-service
pytest tests/integration/
```

### API Tests
```bash
# Start service first
curl http://localhost:8001/health
```

---

## 🚀 Deployment

### Docker
```bash
# Build image
docker build -t aeva-bench-service:latest services/bench-service/

# Run container
docker run -p 8001:8001 aeva-bench-service:latest
```

### Kubernetes
```bash
# Deploy service
kubectl apply -f infrastructure/kubernetes/bench-service/

# Check status
kubectl get pods -l app=bench-service
```

---

## 📊 Service Communication

Services communicate via:
1. **HTTP/REST** - Synchronous requests using `aeva-common` clients
2. **Message Queue** - Asynchronous events (Celery/RabbitMQ)
3. **Shared Database** - For read-only data sharing (not recommended for writes)

### Using aeva-common SDK

```python
from aeva_common.clients import BenchClient, GuardClient

# Call Bench Service
async with BenchClient("http://bench-service:8001") as bench:
    result = await bench.run_benchmark("bench_123")

# Validate with Guard Service
async with GuardClient("http://guard-service:8002") as guard:
    gate_result = await guard.validate(result, "production_gate")
```

---

## 🔐 Security

Each service implements:
- **API Key Authentication** - For service-to-service calls
- **JWT Tokens** - For user authentication (via Gateway)
- **Rate Limiting** - Prevent abuse
- **Input Validation** - Pydantic schemas
- **HTTPS/TLS** - Encrypted communication

---

## 📈 Monitoring

Each service exposes:
- **Health Endpoint** - `GET /health`
- **Metrics Endpoint** - `GET /metrics` (Prometheus format)
- **Readiness Probe** - `GET /ready`
- **Liveness Probe** - `GET /live`

---

## 🔄 Service Dependencies

```
Gateway (8000)
  ↓ calls
  ├─ Bench Service (8001)
  ├─ Guard Service (8002)
  ├─ Auto Service (8003) → can call Bench, Guard, Brain
  └─ Brain Service (8004)

Infrastructure:
  ├─ PostgreSQL (shared or per-service)
  ├─ Redis (shared cache)
  └─ Message Queue (optional, for async)
```

---

## 📝 Next Steps

1. ✅ Service structure created
2. ⏳ Implement Bench Service
3. ⏳ Implement Guard Service
4. ⏳ Implement Brain Service
5. ⏳ Implement Auto Service
6. ⏳ Implement API Gateway
7. ⏳ Setup Docker Compose
8. ⏳ Setup Kubernetes manifests
9. ⏳ Add monitoring & logging
10. ⏳ CI/CD pipeline

---

**Status**: 📁 Project Structure Created
**Next**: Implement first service (Bench Service recommended)

Copyright © 2024-2026 AEVA Development Team
