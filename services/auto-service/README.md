# Auto Service

Pipeline orchestration and automation service for the AEVA platform.

## Overview

The Auto Service provides pipeline orchestration capabilities using Celery for asynchronous task execution. It coordinates multi-step evaluation workflows across Bench, Guard, and Brain services.

## Features

- **Pipeline Management**: Create, update, and manage evaluation pipelines
- **Async Execution**: Celery-based asynchronous task processing
- **Multi-step Workflows**: Orchestrate benchmark → validation → analysis workflows
- **Step Tracking**: Monitor individual step execution and status
- **Error Handling**: Automatic retries and error tracking
- **Service Integration**: Seamless integration with Bench, Guard, and Brain services
- **Pipeline Cancellation**: Cancel running pipelines
- **PostgreSQL Storage**: Persistent pipeline and step data

## Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (pipeline data)
- **Task Queue**: Celery with Redis broker
- **ORM**: SQLAlchemy
- **Language**: Python 3.11
- **Testing**: Pytest

## Project Structure

```
auto-service/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI application
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── pipelines.py    # Pipeline API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration settings
│   │   ├── database.py            # Database configuration
│   │   └── celery_app.py          # Celery configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── pipeline.py            # Pipeline and Step models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── pipeline.py            # Pydantic schemas
│   ├── services/
│   │   ├── __init__.py
│   │   └── pipeline_service.py    # Business logic
│   └── tasks/
│       ├── __init__.py
│       └── pipeline_tasks.py      # Celery tasks
├── tests/
│   ├── __init__.py
│   └── test_api.py                # API tests
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

## Installation

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start PostgreSQL and Redis:
```bash
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=aeva postgres:15-alpine
docker run -d -p 6379:6379 redis:7-alpine
```

4. Run the service:
```bash
uvicorn app.main:app --reload --port 8003
```

5. Start Celery worker:
```bash
celery -A app.core.celery_app worker --loglevel=info
```

### Docker Compose

```bash
docker-compose up -d
```

This starts the Auto Service, Celery worker, PostgreSQL, and Redis.

## API Endpoints

### Pipelines

- `POST /v1/pipeline/` - Create a new pipeline
- `GET /v1/pipeline/{id}` - Get pipeline details
- `GET /v1/pipeline/` - List all pipelines
- `PUT /v1/pipeline/{id}` - Update pipeline configuration
- `DELETE /v1/pipeline/{id}` - Delete a pipeline

### Execution

- `POST /v1/pipeline/{id}/execute` - Execute a pipeline asynchronously
- `POST /v1/pipeline/{id}/cancel` - Cancel a running pipeline

### Health

- `GET /health` - Health check (for Kubernetes probes)
- `GET /` - Service information

## Usage Examples

### Create a Pipeline

```bash
curl -X POST http://localhost:8003/v1/pipeline/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ml_evaluation_pipeline",
    "description": "Complete ML model evaluation pipeline",
    "config": {
      "steps": [
        {
          "name": "run_benchmark",
          "type": "benchmark",
          "config": {
            "benchmark_id": "bench-123"
          }
        },
        {
          "name": "validate_quality",
          "type": "validate",
          "config": {
            "gate_id": "gate-456"
          }
        },
        {
          "name": "ai_analysis",
          "type": "analyze",
          "config": {
            "analysis_type": "comprehensive"
          }
        }
      ]
    }
  }'
```

### Execute a Pipeline

```bash
curl -X POST http://localhost:8003/v1/pipeline/{pipeline_id}/execute \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {
      "triggered_by": "user",
      "environment": "production"
    }
  }'
```

### Get Pipeline Status

```bash
curl http://localhost:8003/v1/pipeline/{pipeline_id}
```

## Configuration

Environment variables (see `.env.example`):

- `DATABASE_URL` - PostgreSQL connection URL
- `REDIS_URL` - Redis connection URL
- `CELERY_BROKER_URL` - Celery broker URL (Redis)
- `CELERY_RESULT_BACKEND` - Celery result backend URL (Redis)
- `BENCH_SERVICE_URL` - Bench Service URL
- `GUARD_SERVICE_URL` - Guard Service URL
- `BRAIN_SERVICE_URL` - Brain Service URL
- `DEFAULT_TIMEOUT` - Task timeout in seconds (default: 3600)
- `MAX_RETRIES` - Maximum retry attempts (default: 3)
- `RETRY_DELAY` - Delay between retries in seconds (default: 60)

## Pipeline Workflow

### Step Types

1. **Benchmark Step** (`benchmark`):
   - Calls Bench Service to run benchmarks
   - Returns evaluation metrics

2. **Validation Step** (`validate`):
   - Calls Guard Service to validate metrics
   - Can block pipeline if quality gate fails

3. **Analysis Step** (`analyze`):
   - Calls Brain Service for AI analysis
   - Provides insights and recommendations

### Execution Flow

1. Pipeline created with configuration
2. Execute endpoint triggers Celery task
3. Celery worker processes each step sequentially
4. Each step calls appropriate service
5. Results stored in database
6. Pipeline status updated (completed/failed/blocked)

### Status Flow

- `pending` → `running` → `completed`/`failed`/`blocked`/`cancelled`

## Testing

Run tests:
```bash
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## Data Storage

The service uses PostgreSQL for:

- **Pipelines**: Pipeline configuration and execution data
- **Steps**: Individual step tracking and results

Redis is used for:

- **Celery Broker**: Task queue management
- **Result Backend**: Task result storage

## Integration with Other Services

The Auto Service orchestrates:

- **Bench Service** (Port 8001): Runs benchmarks
- **Guard Service** (Port 8002): Validates quality gates
- **Brain Service** (Port 8004): Performs AI analysis

## Celery Worker

The Celery worker processes pipeline tasks asynchronously:

```bash
celery -A app.core.celery_app worker --loglevel=info
```

Monitor tasks with Flower (optional):
```bash
celery -A app.core.celery_app flower
```

## API Documentation

Interactive API documentation is available at:

- Swagger UI: http://localhost:8003/v1/docs
- ReDoc: http://localhost:8003/v1/redoc

## Monitoring

The service exposes:

- Health check endpoint at `/health` for Kubernetes liveness/readiness probes
- Celery task monitoring through Flower
- Structured logging for centralized log aggregation

---

Copyright © 2024-2026 AEVA Development Team
