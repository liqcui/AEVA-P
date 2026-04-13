# API Gateway

Unified API Gateway for the AEVA microservices platform.

## Overview

The API Gateway provides a single entry point for all AEVA microservices. It handles request routing, rate limiting, and provides a unified API interface for client applications.

## Features

- **Unified API**: Single endpoint for all microservices
- **Request Routing**: Intelligent routing to backend services
- **Rate Limiting**: Configurable request rate limiting per client
- **Error Handling**: Unified error responses across services
- **CORS Support**: Configurable cross-origin resource sharing
- **Health Checks**: Monitoring and health status for all services
- **Auto Retry**: Automatic retry logic for failed requests
- **Timeout Management**: Configurable request timeouts
- **Load Balancing**: Ready for horizontal scaling (future)
- **Authentication**: JWT-based auth support (future implementation)

## Technology Stack

- **Framework**: FastAPI
- **HTTP Client**: httpx (async)
- **Language**: Python 3.11
- **Testing**: Pytest with async support

## Project Structure

```
api-gateway/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── bench.py         # Benchmark proxy
│   │       ├── guard.py         # Gate proxy
│   │       ├── auto.py          # Pipeline proxy
│   │       └── brain.py         # Analysis proxy
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration
│   │   └── service_client.py   # Service client
│   └── middleware/
│       ├── __init__.py
│       └── rate_limit.py       # Rate limiting
├── tests/
│   ├── __init__.py
│   └── test_api.py             # API tests
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
# Edit .env with service URLs
```

3. Ensure backend services are running:
```bash
# Bench Service on port 8001
# Guard Service on port 8002
# Auto Service on port 8003
# Brain Service on port 8004
```

4. Run the gateway:
```bash
uvicorn app.main:app --reload --port 8000
```

### Docker Compose

```bash
# Create network if needed
docker network create aeva-network

# Start gateway
docker-compose up -d
```

## API Endpoints

All endpoints are prefixed with `/api/v1`.

### Benchmark Service (`/api/v1/benchmark`)

- `POST /api/v1/benchmark/` - Create benchmark
- `GET /api/v1/benchmark/{id}` - Get benchmark
- `GET /api/v1/benchmark/` - List benchmarks
- `PUT /api/v1/benchmark/{id}` - Update benchmark
- `DELETE /api/v1/benchmark/{id}` - Delete benchmark
- `POST /api/v1/benchmark/{id}/run` - Run benchmark
- `GET /api/v1/benchmark/{id}/results` - Get results
- `GET /api/v1/benchmark/{id}/history` - Get history

### Gate Service (`/api/v1/gate`)

- `POST /api/v1/gate/` - Create gate
- `GET /api/v1/gate/{id}` - Get gate
- `GET /api/v1/gate/` - List gates
- `PUT /api/v1/gate/{id}` - Update gate
- `DELETE /api/v1/gate/{id}` - Delete gate
- `POST /api/v1/gate/{id}/validate` - Validate metrics
- `GET /api/v1/gate/{id}/history` - Get validation history
- `GET /api/v1/gate/{id}/statistics` - Get statistics

### Pipeline Service (`/api/v1/pipeline`)

- `POST /api/v1/pipeline/` - Create pipeline
- `GET /api/v1/pipeline/{id}` - Get pipeline
- `GET /api/v1/pipeline/` - List pipelines
- `PUT /api/v1/pipeline/{id}` - Update pipeline
- `DELETE /api/v1/pipeline/{id}` - Delete pipeline
- `POST /api/v1/pipeline/{id}/execute` - Execute pipeline
- `POST /api/v1/pipeline/{id}/cancel` - Cancel pipeline

### Analysis Service (`/api/v1/analysis`)

- `POST /api/v1/analysis/` - Create analysis
- `GET /api/v1/analysis/{id}` - Get analysis
- `GET /api/v1/analysis/` - List analyses
- `DELETE /api/v1/analysis/{id}` - Delete analysis
- `POST /api/v1/analysis/quick` - Quick analysis
- `POST /api/v1/analysis/{id}/reprocess` - Reprocess analysis

### Gateway Endpoints

- `GET /health` - Health check
- `GET /` - Service information

## Usage Examples

### Create and Run Benchmark

```bash
# Create benchmark
curl -X POST http://localhost:8000/api/v1/benchmark/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "model_evaluation",
    "algorithm": "RandomForest",
    "dataset": "test_data"
  }'

# Run benchmark
curl -X POST http://localhost:8000/api/v1/benchmark/{id}/run
```

### Validate Against Quality Gate

```bash
curl -X POST http://localhost:8000/api/v1/gate/{gate_id}/validate \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": {
      "accuracy": 0.95,
      "f1_score": 0.93
    }
  }'
```

### Execute Pipeline

```bash
curl -X POST http://localhost:8000/api/v1/pipeline/{pipeline_id}/execute \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {
      "triggered_by": "api",
      "environment": "production"
    }
  }'
```

### Quick Analysis

```bash
curl -X POST http://localhost:8000/api/v1/analysis/quick \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_type": "basic",
    "data": {
      "metrics": {
        "accuracy": 0.95,
        "precision": 0.93
      }
    }
  }'
```

## Configuration

Environment variables (see `.env.example`):

- `API_V1_STR` - API version prefix (default: /api/v1)
- `BENCH_SERVICE_URL` - Bench Service URL
- `GUARD_SERVICE_URL` - Guard Service URL
- `AUTO_SERVICE_URL` - Auto Service URL
- `BRAIN_SERVICE_URL` - Brain Service URL
- `REQUEST_TIMEOUT` - Request timeout in seconds (default: 300)
- `MAX_RETRIES` - Maximum retry attempts (default: 3)
- `RETRY_DELAY` - Delay between retries in seconds (default: 1)
- `ENABLE_RATE_LIMITING` - Enable rate limiting (default: true)
- `RATE_LIMIT_PER_MINUTE` - Max requests per minute per client (default: 100)
- `CORS_ORIGINS` - Allowed CORS origins (default: ["*"])

## Rate Limiting

The gateway implements in-memory rate limiting:

- Per-client IP address tracking
- Configurable limits (default: 100 requests/minute)
- Rate limit headers in responses:
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Remaining requests in current window

When rate limit is exceeded:
```json
{
  "detail": "Rate limit exceeded. Maximum 100 requests per minute."
}
```

## Error Handling

The gateway provides unified error responses:

- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Gateway error
- `503 Service Unavailable` - Backend service unavailable
- `504 Gateway Timeout` - Backend service timeout

## Service Client

The `ServiceClient` handles all backend communication:

- Automatic retry logic for failed requests
- Timeout management
- Error translation and propagation
- Request/response logging (future)

## Testing

Run tests:
```bash
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## Monitoring

The gateway exposes:

- Health check endpoint at `/health`
- Backend service URLs in health response
- Rate limit metrics in response headers
- Structured logging for request tracking (future)

## Future Enhancements

- **Authentication**: JWT-based authentication
- **Authorization**: Role-based access control
- **Load Balancing**: Round-robin across service instances
- **Circuit Breaker**: Automatic failover for unhealthy services
- **Caching**: Response caching for read-heavy endpoints
- **Metrics**: Prometheus metrics export
- **Tracing**: Distributed tracing with OpenTelemetry
- **API Versioning**: Support for multiple API versions
- **GraphQL**: GraphQL gateway alongside REST
- **WebSocket**: WebSocket proxy for real-time features

## API Documentation

Interactive API documentation is available at:

- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Architecture

```
┌─────────────┐
│   Clients   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  API Gateway    │
│  (Port 8000)    │
│                 │
│  - Routing      │
│  - Rate Limit   │
│  - Auth (future)│
└────────┬────────┘
         │
    ┌────┴────┬────────┬─────────┐
    ▼         ▼        ▼         ▼
┌────────┐ ┌──────┐ ┌──────┐ ┌───────┐
│ Bench  │ │Guard │ │ Auto │ │ Brain │
│ :8001  │ │:8002 │ │:8003 │ │ :8004 │
└────────┘ └──────┘ └──────┘ └───────┘
```

## Network Configuration

For Docker deployment, all services should be on the same network:

```bash
docker network create aeva-network
```

Then reference this network in each service's `docker-compose.yml`.

---

Copyright © 2024-2026 AEVA Development Team
