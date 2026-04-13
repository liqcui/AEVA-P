# Brain Service

AI-powered analysis service for the AEVA platform using LLM integration.

## Overview

The Brain Service provides intelligent analysis of evaluation data using Large Language Models (LLMs). It generates insights, identifies patterns, and provides actionable recommendations based on benchmark and validation results.

## Features

- **AI-Powered Analysis**: Leverage LLMs for intelligent evaluation insights
- **Multiple Analysis Types**: Basic, comprehensive, comparative, predictive, and diagnostic
- **Quick Analysis**: Stateless analysis without database persistence
- **LLM Provider Support**: OpenAI, Anthropic, Ollama, or custom endpoints
- **Background Processing**: Async analysis with FastAPI BackgroundTasks
- **Result Persistence**: Store analysis history in PostgreSQL
- **Reprocessing**: Re-analyze existing data with updated prompts
- **Configurable Prompts**: Custom system messages and analysis focus areas

## Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (analysis history)
- **LLM Integration**: OpenAI, Anthropic, Ollama support
- **ORM**: SQLAlchemy
- **Language**: Python 3.11
- **Testing**: Pytest with async support

## Project Structure

```
brain-service/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI application
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── analyses.py     # Analysis API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration settings
│   │   ├── database.py            # Database configuration
│   │   └── llm_client.py          # LLM client wrapper
│   ├── models/
│   │   ├── __init__.py
│   │   └── analysis.py            # Analysis models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── analysis.py            # Pydantic schemas
│   └── services/
│       ├── __init__.py
│       └── analysis_service.py    # Business logic
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
# Edit .env with your configuration and LLM API key
```

3. Start PostgreSQL:
```bash
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=aeva postgres:15-alpine
```

4. Run the service:
```bash
uvicorn app.main:app --reload --port 8004
```

### Docker Compose

```bash
# Set your LLM API key
export LLM_API_KEY=your-api-key-here

docker-compose up -d
```

## API Endpoints

### Analysis

- `POST /v1/analysis/` - Create and process a new analysis
- `GET /v1/analysis/{id}` - Get analysis details
- `GET /v1/analysis/` - List all analyses
- `DELETE /v1/analysis/{id}` - Delete an analysis
- `POST /v1/analysis/quick` - Quick analysis without persistence
- `POST /v1/analysis/{id}/reprocess` - Reprocess an existing analysis

### Health

- `GET /health` - Health check (for Kubernetes probes)
- `GET /` - Service information

## Usage Examples

### Create Analysis

```bash
curl -X POST http://localhost:8004/v1/analysis/ \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_type": "comprehensive",
    "input_data": {
      "benchmark": {
        "accuracy": 0.92,
        "f1_score": 0.88,
        "precision": 0.90
      },
      "validation": {
        "passed": true,
        "score": 0.90
      }
    },
    "config": {
      "focus_areas": ["performance", "quality"],
      "include_recommendations": true
    }
  }'
```

### Quick Analysis

```bash
curl -X POST http://localhost:8004/v1/analysis/quick \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_type": "basic",
    "data": {
      "metrics": {
        "accuracy": 0.95,
        "precision": 0.93,
        "recall": 0.92
      }
    },
    "config": {
      "include_recommendations": true
    }
  }'
```

### Get Analysis Results

```bash
curl http://localhost:8004/v1/analysis/{analysis_id}
```

## Configuration

Environment variables (see `.env.example`):

- `DATABASE_URL` - PostgreSQL connection URL
- `LLM_PROVIDER` - LLM provider (openai, anthropic, ollama)
- `LLM_MODEL` - Model name (e.g., gpt-4, claude-3-opus-20240229)
- `LLM_API_KEY` - API key for LLM provider
- `LLM_BASE_URL` - Custom API endpoint (optional)
- `LLM_TEMPERATURE` - Temperature for generation (default: 0.7)
- `LLM_MAX_TOKENS` - Maximum tokens to generate (default: 2000)
- `BENCH_SERVICE_URL` - Bench Service URL
- `GUARD_SERVICE_URL` - Guard Service URL

## Analysis Types

### Basic Analysis
Quick summary of key metrics and overall performance.

### Comprehensive Analysis
Detailed findings with patterns, quality assessment, and recommendations.

### Comparative Analysis
Compare results across models or experiments to identify best performers.

### Predictive Analysis
Forecast future performance based on trends and patterns.

### Diagnostic Analysis
Identify issues, anomalies, and root causes of poor performance.

## LLM Providers

### OpenAI
```bash
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_API_KEY=sk-...
```

### Anthropic
```bash
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-opus-20240229
LLM_API_KEY=sk-ant-...
```

### Ollama (Local)
```bash
LLM_PROVIDER=ollama
LLM_MODEL=llama2
LLM_BASE_URL=http://localhost:11434
```

### Mock (Testing)
No configuration needed - uses built-in mock responses.

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

- **Analyses**: Analysis requests and configurations
- **Results**: Generated insights, findings, and recommendations
- **Metadata**: Processing time, tokens used, LLM configuration

## Integration with Other Services

The Brain Service analyzes data from:

- **Bench Service** (Port 8001): Benchmark results
- **Guard Service** (Port 8002): Validation outcomes
- **Auto Service** (Port 8003): Pipeline execution results

## API Documentation

Interactive API documentation is available at:

- Swagger UI: http://localhost:8004/v1/docs
- ReDoc: http://localhost:8004/v1/redoc

## Example Analysis Response

```json
{
  "summary": "Model performance is excellent with high accuracy and balanced metrics.",
  "findings": [
    "Accuracy of 0.92 exceeds industry benchmarks",
    "F1-score of 0.88 indicates good precision-recall balance",
    "Validation passed with confidence score of 0.90"
  ],
  "recommendations": [
    "Deploy to production with gradual rollout",
    "Monitor edge case performance",
    "Implement A/B testing for validation"
  ],
  "confidence_score": 0.88
}
```

## Monitoring

The service exposes:

- Health check endpoint at `/health` for Kubernetes liveness/readiness probes
- LLM provider and model information in health checks
- Processing time and token usage tracking
- Structured logging for centralized log aggregation

---

Copyright © 2024-2026 AEVA Development Team
