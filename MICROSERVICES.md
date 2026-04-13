# AEVA Microservices Deployment Guide

This guide covers deploying the AEVA platform as microservices using Docker Compose.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Clients                              │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │   API Gateway    │
                  │   Port 8000      │
                  └────────┬─────────┘
                           │
        ┌──────────────────┼──────────────────┬───────────┐
        │                  │                  │           │
        ▼                  ▼                  ▼           ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Bench Service│  │Guard Service │  │ Auto Service │  │Brain Service │
│  Port 8001   │  │  Port 8002   │  │  Port 8003   │  │  Port 8004   │
│              │  │              │  │              │  │              │
│ PostgreSQL   │  │    Redis     │  │ PostgreSQL   │  │ PostgreSQL   │
│ Port 5433    │  │  Port 6379   │  │ Port 5434    │  │ Port 5435    │
└──────────────┘  └──────────────┘  │    Redis     │  └──────────────┘
                                    │  Port 6380   │
                                    │              │
                                    │Celery Worker │
                                    └──────────────┘
```

## Services

### 1. API Gateway (Port 8000)
- **Purpose**: Unified entry point for all services
- **Features**: Request routing, rate limiting, CORS
- **Endpoints**: `/api/v1/*`

### 2. Bench Service (Port 8001)
- **Purpose**: Benchmark evaluation and comparison
- **Database**: PostgreSQL (Port 5433)
- **Features**: Model evaluation, performance testing

### 3. Guard Service (Port 8002)
- **Purpose**: Quality gate validation
- **Database**: Redis (Port 6379)
- **Features**: Metric validation, auto-blocking

### 4. Auto Service (Port 8003)
- **Purpose**: Pipeline orchestration
- **Database**: PostgreSQL (Port 5434)
- **Message Broker**: Redis (Port 6380)
- **Features**: Multi-step workflows, Celery workers

### 5. Brain Service (Port 8004)
- **Purpose**: AI-powered analysis
- **Database**: PostgreSQL (Port 5435)
- **Features**: LLM integration, intelligent insights

## Quick Start

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- 8GB RAM minimum
- 20GB disk space

### Environment Setup

1. Create environment file for LLM configuration:

```bash
# Create .env file in project root
cat > .env << EOF
# LLM Configuration for Brain Service
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_API_KEY=your-api-key-here
LLM_BASE_URL=

# Optional: Use Anthropic instead
# LLM_PROVIDER=anthropic
# LLM_MODEL=claude-3-opus-20240229
# LLM_API_KEY=your-anthropic-key

# Optional: Use Ollama (local)
# LLM_PROVIDER=ollama
# LLM_MODEL=llama2
# LLM_BASE_URL=http://host.docker.internal:11434
EOF
```

### Start All Services

```bash
# Start all microservices
docker-compose -f docker-compose.microservices.yml up -d

# View logs
docker-compose -f docker-compose.microservices.yml logs -f

# Check service health
curl http://localhost:8000/health
```

### Service URLs

- **API Gateway**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/v1/docs
- **Bench Service**: http://localhost:8001/v1/docs
- **Guard Service**: http://localhost:8002/v1/docs
- **Auto Service**: http://localhost:8003/v1/docs
- **Brain Service**: http://localhost:8004/v1/docs

## Usage Examples

### Via API Gateway (Recommended)

All examples use the API Gateway at `http://localhost:8000/api/v1`.

#### 1. Create and Run Benchmark

```bash
# Create benchmark
curl -X POST http://localhost:8000/api/v1/benchmark/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "model_evaluation",
    "algorithm": "RandomForest",
    "dataset": "test_data",
    "parameters": {
      "n_estimators": 100,
      "max_depth": 10
    }
  }'

# Run benchmark (use ID from response)
curl -X POST http://localhost:8000/api/v1/benchmark/{benchmark_id}/run
```

#### 2. Create Quality Gate and Validate

```bash
# Create quality gate
curl -X POST http://localhost:8000/api/v1/gate/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "production_gate",
    "description": "Production deployment gate",
    "threshold": 0.85,
    "metrics": ["accuracy", "f1_score"],
    "strict_mode": false,
    "auto_block": true
  }'

# Validate metrics
curl -X POST http://localhost:8000/api/v1/gate/{gate_id}/validate \
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

#### 3. Execute Pipeline

```bash
# Create pipeline
curl -X POST http://localhost:8000/api/v1/pipeline/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ml_evaluation_pipeline",
    "description": "Complete ML evaluation workflow",
    "config": {
      "steps": [
        {
          "name": "run_benchmark",
          "type": "benchmark",
          "config": {"benchmark_id": "bench-123"}
        },
        {
          "name": "validate_quality",
          "type": "validate",
          "config": {"gate_id": "gate-456"}
        },
        {
          "name": "ai_analysis",
          "type": "analyze",
          "config": {"analysis_type": "comprehensive"}
        }
      ]
    }
  }'

# Execute pipeline
curl -X POST http://localhost:8000/api/v1/pipeline/{pipeline_id}/execute \
  -H "Content-Type: application/json" \
  -d '{"metadata": {"triggered_by": "api"}}'
```

#### 4. AI Analysis

```bash
# Quick analysis (no persistence)
curl -X POST http://localhost:8000/api/v1/analysis/quick \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_type": "comprehensive",
    "data": {
      "metrics": {
        "accuracy": 0.95,
        "precision": 0.93,
        "recall": 0.92,
        "f1_score": 0.925
      }
    },
    "config": {
      "focus_areas": ["performance", "quality"],
      "include_recommendations": true
    }
  }'
```

### Direct Service Access

You can also access services directly (bypassing the gateway):

```bash
# Bench Service
curl http://localhost:8001/v1/benchmark/

# Guard Service
curl http://localhost:8002/v1/gate/

# Auto Service
curl http://localhost:8003/v1/pipeline/

# Brain Service
curl http://localhost:8004/v1/analysis/
```

## Service Management

### View Service Status

```bash
# List all services
docker-compose -f docker-compose.microservices.yml ps

# Check specific service
docker-compose -f docker-compose.microservices.yml ps api-gateway
```

### View Logs

```bash
# All services
docker-compose -f docker-compose.microservices.yml logs -f

# Specific service
docker-compose -f docker-compose.microservices.yml logs -f bench-service

# Last 100 lines
docker-compose -f docker-compose.microservices.yml logs --tail=100 api-gateway
```

### Restart Services

```bash
# Restart all services
docker-compose -f docker-compose.microservices.yml restart

# Restart specific service
docker-compose -f docker-compose.microservices.yml restart api-gateway
```

### Scale Services

```bash
# Scale Auto Service Celery workers
docker-compose -f docker-compose.microservices.yml up -d --scale auto-celery-worker=3

# Scale API Gateway
docker-compose -f docker-compose.microservices.yml up -d --scale api-gateway=2
```

### Stop Services

```bash
# Stop all services
docker-compose -f docker-compose.microservices.yml down

# Stop and remove volumes (destructive!)
docker-compose -f docker-compose.microservices.yml down -v
```

## Database Access

### PostgreSQL Databases

```bash
# Bench Service Database
docker exec -it bench-postgres psql -U aeva -d bench_service

# Auto Service Database
docker exec -it auto-postgres psql -U aeva -d auto_service

# Brain Service Database
docker exec -it brain-postgres psql -U aeva -d brain_service
```

### Redis Databases

```bash
# Guard Service Redis
docker exec -it guard-redis redis-cli

# Auto Service Redis (Celery)
docker exec -it auto-redis redis-cli
```

## Monitoring

### Health Checks

```bash
# API Gateway health (includes all backend services)
curl http://localhost:8000/health

# Individual service health
curl http://localhost:8001/health  # Bench
curl http://localhost:8002/health  # Guard
curl http://localhost:8003/health  # Auto
curl http://localhost:8004/health  # Brain
```

### Resource Usage

```bash
# View resource usage
docker stats

# View specific container
docker stats api-gateway
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose -f docker-compose.microservices.yml logs service-name

# Check if ports are available
netstat -an | grep LISTEN | grep 8000

# Rebuild service
docker-compose -f docker-compose.microservices.yml build service-name
docker-compose -f docker-compose.microservices.yml up -d service-name
```

### Database Connection Issues

```bash
# Check if database is healthy
docker-compose -f docker-compose.microservices.yml ps

# Wait for database to be ready
docker-compose -f docker-compose.microservices.yml up -d bench-postgres
# Wait ~10 seconds
docker-compose -f docker-compose.microservices.yml up -d bench-service
```

### Celery Worker Not Processing Tasks

```bash
# Check worker logs
docker-compose -f docker-compose.microservices.yml logs auto-celery-worker

# Restart worker
docker-compose -f docker-compose.microservices.yml restart auto-celery-worker
```

### LLM API Errors (Brain Service)

```bash
# Verify LLM_API_KEY is set
docker-compose -f docker-compose.microservices.yml exec brain-service env | grep LLM

# Use mock mode for testing (no API key needed)
# Edit .env and remove LLM_API_KEY or set LLM_PROVIDER=mock
```

## Performance Optimization

### Database Optimization

```bash
# Increase PostgreSQL shared_buffers
# Add to docker-compose.microservices.yml under postgres services:
command: postgres -c shared_buffers=256MB -c max_connections=200
```

### Redis Optimization

```bash
# Increase maxmemory
# Add to docker-compose.microservices.yml under redis services:
command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
```

### Gateway Rate Limiting

Adjust in API Gateway environment variables:
```yaml
- RATE_LIMIT_PER_MINUTE=200  # Increase from 100
```

## Production Deployment

### Use Production Configuration

1. Update `.env` with production LLM credentials
2. Set strong database passwords
3. Configure CORS origins properly
4. Enable authentication (when implemented)
5. Use reverse proxy (nginx) in front of API Gateway
6. Set up SSL/TLS certificates
7. Configure log aggregation
8. Set up monitoring (Prometheus/Grafana)

### Docker Swarm Deployment

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.microservices.yml aeva

# Scale services
docker service scale aeva_api-gateway=3
docker service scale aeva_auto-celery-worker=5
```

### Kubernetes Deployment

See `infrastructure/kubernetes/` for Kubernetes manifests and Helm charts.

## Cleanup

### Remove All Services and Data

```bash
# Stop and remove containers, networks
docker-compose -f docker-compose.microservices.yml down

# Remove volumes (all data will be lost!)
docker-compose -f docker-compose.microservices.yml down -v

# Remove images
docker-compose -f docker-compose.microservices.yml down --rmi all
```

## Support

For issues and questions:
- Check service logs: `docker-compose logs -f service-name`
- Review individual service READMEs in `services/*/README.md`
- Check API documentation at `http://localhost:8000/api/v1/docs`

---

Copyright © 2024-2026 AEVA Development Team
