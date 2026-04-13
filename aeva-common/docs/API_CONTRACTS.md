# AEVA Microservices API Contracts

**Version**: 1.0.0
**Date**: 2026-04-13
**Project ID**: AEVA-2026-LQC-dc68e33

---

## 🎯 Overview

This document defines the standardized API contracts for all AEVA microservices. All services must implement these interfaces to ensure consistency and interoperability.

---

## 🏗️ Common Standards

### Response Format

All API endpoints return responses in the following format:

```json
{
  "status": "success" | "error",
  "data": {...},
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message"
  } | null,
  "timestamp": "2026-04-13T10:00:00Z"
}
```

### HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request parameters
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service temporarily unavailable

### Common Headers

**Request Headers**:
```
Content-Type: application/json
X-Request-ID: <uuid>
X-API-Key: <optional>
```

**Response Headers**:
```
Content-Type: application/json
X-Request-ID: <uuid>
X-Service-Version: <version>
```

### Health Check Endpoint

All services must implement:

```
GET /health

Response:
{
  "status": "success",
  "data": {
    "status": "healthy" | "degraded" | "unhealthy",
    "version": "0.1.0",
    "uptime": 3600,
    "dependencies": {
      "database": "healthy",
      "redis": "healthy"
    }
  },
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

## 🏆 Benchmark Service API (Port 8001)

### POST /benchmark/create

Create a new benchmark.

**Request**:
```json
{
  "benchmark_name": "accuracy_test",
  "model_path": "/models/my_model.pkl",
  "dataset_path": "/data/test.csv",
  "config": {
    "metrics": ["accuracy", "f1_score"],
    "test_size": 0.2
  }
}
```

**Response** (201):
```json
{
  "status": "success",
  "data": {
    "benchmark_id": "bench_abc123",
    "status": "created"
  },
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

### POST /benchmark/{benchmark_id}/run

Execute a benchmark.

**Response** (200):
```json
{
  "status": "success",
  "data": {
    "result": {
      "pipeline_name": "accuracy_test",
      "algorithm_name": "RandomForest",
      "status": "passed",
      "metrics": {
        "accuracy": {
          "value": 0.95,
          "threshold": 0.85,
          "passed": true
        }
      }
    }
  },
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

### GET /benchmark/{benchmark_id}/results

Get benchmark results.

**Response** (200):
```json
{
  "status": "success",
  "data": {
    "results": [
      {
        "pipeline_name": "accuracy_test",
        "timestamp": "2026-04-13T10:00:00Z",
        "metrics": {...}
      }
    ]
  },
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

### GET /benchmark/list

List all benchmarks.

**Query Parameters**:
- `page` (int): Page number (default: 1)
- `limit` (int): Results per page (default: 50)
- `status` (string): Filter by status

**Response** (200):
```json
{
  "status": "success",
  "data": {
    "benchmarks": [
      {
        "id": "bench_abc123",
        "name": "accuracy_test",
        "description": "Accuracy benchmark",
        "created_at": "2026-04-13T10:00:00Z",
        "status": "completed"
      }
    ],
    "total": 42,
    "page": 1,
    "limit": 50
  },
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

### DELETE /benchmark/{benchmark_id}

Delete a benchmark.

**Response** (200):
```json
{
  "status": "success",
  "data": {
    "success": true,
    "deleted_id": "bench_abc123"
  },
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

## 🛡️ Guard Service API (Port 8002)

### POST /gate/register

Register a new quality gate.

**Request**:
```json
{
  "name": "production_gate",
  "threshold": 0.85,
  "metrics": ["accuracy", "f1_score"],
  "strict_mode": false,
  "auto_block": true
}
```

**Response** (201):
```json
{
  "status": "success",
  "data": {
    "gate_id": "gate_xyz789",
    "status": "registered"
  },
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

### POST /gate/{gate_id}/validate

Validate evaluation result against quality gate.

**Request**:
```json
{
  "pipeline_name": "ml_pipeline",
  "metrics": {
    "accuracy": {"value": 0.95, "passed": true},
    "f1_score": {"value": 0.92, "passed": true}
  },
  "status": "passed"
}
```

**Response** (200):
```json
{
  "status": "success",
  "data": {
    "gate_result": {
      "passed": true,
      "score": 0.935,
      "threshold": 0.85,
      "blocked": false,
      "reason": null
    }
  },
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

### GET /gate/{gate_id}/status

Get quality gate status.

**Response** (200):
```json
{
  "status": "success",
  "data": {
    "status": {
      "id": "gate_xyz789",
      "name": "production_gate",
      "enabled": true,
      "threshold": 0.85,
      "total_validations": 156,
      "passed_validations": 142,
      "blocked_validations": 3
    }
  },
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

### GET /gate/{gate_id}/history

Get gate validation history.

**Query Parameters**:
- `limit` (int): Maximum results (default: 100)
- `offset` (int): Offset for pagination (default: 0)

**Response** (200):
```json
{
  "status": "success",
  "data": {
    "history": [
      {
        "passed": true,
        "score": 0.935,
        "threshold": 0.85,
        "blocked": false,
        "timestamp": "2026-04-13T10:00:00Z"
      }
    ],
    "total": 156,
    "limit": 100,
    "offset": 0
  },
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

## 🤖 Auto Pipeline Service API (Port 8003)

### POST /pipeline/create

Create a new pipeline.

**Request**:
```json
{
  "name": "ml_eval_pipeline",
  "stages": [
    {
      "name": "data_quality",
      "service": "data-quality-service",
      "config": {...}
    },
    {
      "name": "benchmark",
      "service": "bench-service",
      "config": {...}
    }
  ],
  "schedule": "0 0 * * *",
  "enabled": true
}
```

**Response** (201):
```json
{
  "status": "success",
  "data": {
    "pipeline_id": "pipe_def456",
    "status": "created"
  },
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

### POST /pipeline/{pipeline_id}/execute

Execute a pipeline.

**Request**:
```json
{
  "params": {
    "model_path": "/models/my_model.pkl",
    "dataset_path": "/data/test.csv"
  }
}
```

**Response** (202):
```json
{
  "status": "success",
  "data": {
    "execution_id": "exec_ghi789",
    "status": "pending"
  },
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

### GET /pipeline/execution/{execution_id}/status

Get pipeline execution status.

**Response** (200):
```json
{
  "status": "success",
  "data": {
    "status": {
      "id": "exec_ghi789",
      "pipeline_name": "ml_eval_pipeline",
      "status": "running",
      "started_at": "2026-04-13T10:00:00Z",
      "completed_at": null,
      "current_stage": "benchmark",
      "progress": 0.65
    }
  },
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

### GET /pipeline/execution/{execution_id}/results

Get pipeline execution results.

**Response** (200):
```json
{
  "status": "success",
  "data": {
    "result": {
      "pipeline_name": "ml_eval_pipeline",
      "status": "passed",
      "metrics": {...},
      "duration": 123.45
    }
  },
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

## 🧠 Brain Service API (Port 8004)

### POST /analyze

Perform intelligent analysis.

**Request**:
```json
{
  "result": {
    "pipeline_name": "ml_pipeline",
    "status": "failed",
    "metrics": {
      "accuracy": {"value": 0.65, "threshold": 0.85, "passed": false}
    },
    "errors": ["Accuracy below threshold"]
  },
  "analysis_type": "full",
  "context": "Production model evaluation"
}
```

**Response** (200):
```json
{
  "status": "success",
  "data": {
    "analysis": {
      "summary": "Model accuracy is significantly below threshold",
      "root_causes": [
        "Training data may be outdated",
        "Feature drift detected in production"
      ],
      "recommendations": [
        "Retrain model with recent data",
        "Review feature engineering pipeline",
        "Add data quality monitoring"
      ],
      "severity": "error",
      "confidence": 0.85
    }
  },
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

### POST /analyze/root-cause

Analyze root causes of failures.

**Request**: Same as EvaluationResult

**Response** (200):
```json
{
  "status": "success",
  "data": {
    "analysis": {
      "summary": "Root cause analysis",
      "root_causes": [...],
      "severity": "error",
      "confidence": 0.85
    }
  },
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

### POST /analyze/suggestions

Get improvement suggestions.

**Request**: Same as EvaluationResult

**Response** (200):
```json
{
  "status": "success",
  "data": {
    "analysis": {
      "summary": "Improvement suggestions",
      "recommendations": [...],
      "severity": "info",
      "confidence": 0.75
    }
  },
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

## 🔄 Service Discovery

Services are registered in the service registry:

```yaml
services:
  bench:
    url: http://bench-service:8001
    health: /health
    timeout: 30
  guard:
    url: http://guard-service:8002
    health: /health
    timeout: 10
  auto:
    url: http://auto-service:8003
    health: /health
    timeout: 60
  brain:
    url: http://brain-service:8004
    health: /health
    timeout: 120
```

---

## 📊 Error Codes

| Code | Description |
|------|-------------|
| `INVALID_REQUEST` | Request validation failed |
| `RESOURCE_NOT_FOUND` | Requested resource not found |
| `SERVICE_UNAVAILABLE` | Downstream service unavailable |
| `TIMEOUT` | Request timed out |
| `INTERNAL_ERROR` | Internal server error |
| `UNAUTHORIZED` | Authentication required |
| `FORBIDDEN` | Insufficient permissions |

---

## 🔒 Authentication

All services support optional API key authentication:

```
X-API-Key: <your-api-key>
```

---

## 📝 Versioning

API version is specified in the URL path:

```
/v1/benchmark/create
/v1/gate/validate
```

Current version: `v1`

---

**Status**: ✅ API Contracts Defined
**Next**: Service Implementation

Copyright © 2024-2026 AEVA Development Team
