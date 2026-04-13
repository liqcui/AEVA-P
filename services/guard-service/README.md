# Guard Service

Quality gate validation and blocking service for the AEVA platform.

## Overview

The Guard Service provides quality gate validation for ML model evaluations. It allows you to define thresholds, validate metrics, and automatically block deployments that don't meet quality standards.

## Features

- **Quality Gate Management**: Create, update, and manage quality gates
- **Metric Validation**: Validate evaluation metrics against defined thresholds
- **Strict Mode**: Require ALL metrics to pass (not just average)
- **Auto-blocking**: Automatically block deployments on validation failure
- **Validation History**: Track all validation attempts with full history
- **Statistics**: Monitor success rates and blocking rates
- **Redis Storage**: Fast, in-memory data storage with persistence

## Technology Stack

- **Framework**: FastAPI
- **Storage**: Redis
- **Language**: Python 3.11
- **Testing**: Pytest with async support

## Project Structure

```
guard-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── gates.py    # Gate API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration settings
│   │   └── redis_client.py    # Redis client wrapper
│   ├── models/
│   │   ├── __init__.py
│   │   └── gate.py            # Gate and ValidationResult models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── gate.py            # Pydantic schemas
│   └── services/
│       ├── __init__.py
│       └── gate_service.py    # Business logic
├── tests/
│   ├── __init__.py
│   └── test_api.py            # API tests
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

3. Start Redis:
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

4. Run the service:
```bash
uvicorn app.main:app --reload --port 8002
```

### Docker Compose

```bash
docker-compose up -d
```

This starts both the Guard Service and Redis.

## API Endpoints

### Gates

- `POST /v1/gate/` - Register a new quality gate
- `GET /v1/gate/{id}` - Get gate details
- `GET /v1/gate/` - List all gates
- `PUT /v1/gate/{id}` - Update gate configuration
- `DELETE /v1/gate/{id}` - Delete a gate

### Validation

- `POST /v1/gate/{id}/validate` - Validate metrics against a gate
- `GET /v1/gate/{id}/history` - Get validation history
- `GET /v1/gate/{id}/statistics` - Get gate statistics

### Health

- `GET /health` - Health check (for Kubernetes probes)
- `GET /` - Service information

## Usage Examples

### Create a Quality Gate

```bash
curl -X POST http://localhost:8002/v1/gate/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "production_gate",
    "description": "Production deployment quality gate",
    "threshold": 0.85,
    "metrics": ["accuracy", "f1_score"],
    "strict_mode": false,
    "auto_block": true
  }'
```

### Validate Metrics

```bash
curl -X POST http://localhost:8002/v1/gate/{gate_id}/validate \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": {
      "accuracy": 0.92,
      "f1_score": 0.88,
      "precision": 0.90
    },
    "metadata": {
      "model": "RandomForest",
      "dataset": "test_v2"
    }
  }'
```

### Get Gate Statistics

```bash
curl http://localhost:8002/v1/gate/{gate_id}/statistics
```

## Configuration

Environment variables (see `.env.example`):

- `REDIS_URL` - Redis connection URL (default: redis://localhost:6379/0)
- `REDIS_CACHE_TTL` - Cache TTL in seconds (default: 3600)
- `DEFAULT_THRESHOLD` - Default quality threshold (default: 0.85)
- `DEFAULT_STRICT_MODE` - Default strict mode (default: false)
- `DEFAULT_AUTO_BLOCK` - Default auto-block (default: true)
- `MAX_HISTORY_SIZE` - Maximum validation history size (default: 1000)

## Validation Logic

### Normal Mode (strict_mode=false)

- Calculates average score of all requested metrics that match gate metrics
- Passes if average score >= threshold

### Strict Mode (strict_mode=true)

- ALL metrics must individually pass the threshold
- More stringent validation for critical deployments

### Auto-blocking

When `auto_block=true`, failed validations result in `blocked=true` in the response, allowing downstream systems to prevent deployment.

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

The service uses Redis for all data storage:

- **Gates**: Stored with key pattern `gate:{id}`
- **Gate List**: Stored with key `gates:all`
- **Validation History**: Stored with key pattern `history:{id}` (Redis list)

All data is automatically persisted to disk by Redis (AOF mode in docker-compose).

## Integration with Other Services

The Guard Service integrates with:

- **Bench Service**: Validates benchmark results before deployment
- **Auto Service**: Provides blocking decisions for pipeline orchestration
- **Brain Service**: Receives quality metrics from AI analysis

## API Documentation

Interactive API documentation is available at:

- Swagger UI: http://localhost:8002/v1/docs
- ReDoc: http://localhost:8002/v1/redoc

## Monitoring

The service exposes:

- Health check endpoint at `/health` for Kubernetes liveness/readiness probes
- Metrics endpoint (planned) for Prometheus monitoring
- Structured logging for centralized log aggregation

---

Copyright © 2024-2026 AEVA Development Team
