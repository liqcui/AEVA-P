# AEVA Common SDK

**Version**: 0.1.0
**License**: Dual License (Free for Personal/Academic, Commercial Requires Permission)
**Project ID**: AEVA-2026-LQC-dc68e33

---

## 🎯 Overview

AEVA Common SDK is a shared library providing standardized data structures, interfaces, and client libraries for AEVA microservices architecture.

This package enables:
- ✅ **Shared Data Models** - Consistent data structures across all services
- ✅ **Service Interfaces** - Standardized API contracts
- ✅ **Client Libraries** - Easy service-to-service communication
- ✅ **Configuration Management** - Unified configuration schemas

---

## 📦 Installation

### From Source
```bash
pip install -e ./aeva-common
```

### From PyPI (future)
```bash
pip install aeva-common
```

---

## 🏗️ Package Structure

```
aeva-common/
├── aeva_common/
│   ├── models/          # Shared data models
│   │   ├── result.py    # EvaluationResult, MetricResult, GateResult, Analysis
│   │   └── types.py     # Common enums and types
│   ├── interfaces/      # Service interface definitions
│   │   ├── bench.py     # Benchmark service interface
│   │   ├── guard.py     # Guard service interface
│   │   ├── auto.py      # Auto pipeline service interface
│   │   └── brain.py     # Brain service interface
│   ├── clients/         # Service client libraries
│   │   ├── base.py      # Base HTTP client
│   │   ├── bench.py     # Benchmark service client
│   │   ├── guard.py     # Guard service client
│   │   ├── auto.py      # Auto pipeline service client
│   │   └── brain.py     # Brain service client
│   └── config/          # Configuration schemas
│       ├── base.py      # Base configurations
│       └── services.py  # Service-specific configs
├── setup.py
└── README.md
```

---

## 🚀 Quick Start

### Using Shared Data Models

```python
from aeva_common.models import EvaluationResult, MetricResult, ResultStatus

# Create evaluation result
result = EvaluationResult(
    pipeline_name="ml_pipeline",
    algorithm_name="RandomForest"
)

# Add metrics
result.add_metric("accuracy", 0.95, threshold=0.85)
result.add_metric("f1_score", 0.92)

# Set status
result.set_status(ResultStatus.PASSED)

# Convert to dict
result_dict = result.to_dict()
```

### Using Service Clients

```python
from aeva_common.clients import BenchClient, GuardClient

# Initialize clients
bench_client = BenchClient(base_url="http://bench-service:8001")
guard_client = GuardClient(base_url="http://guard-service:8002")

# Call benchmark service
benchmark_result = await bench_client.run_benchmark(
    benchmark_name="accuracy_test",
    model_path="/models/my_model.pkl"
)

# Validate with guard
gate_result = await guard_client.validate(
    result=benchmark_result,
    gate_name="production_gate"
)
```

### Using Configuration

```python
from aeva_common.config import BenchConfig, GuardConfig

# Load configurations
bench_config = BenchConfig(
    cache_enabled=True,
    parallel_execution=True,
    max_workers=8
)

guard_config = GuardConfig(
    enabled=True,
    default_threshold=0.85,
    strict_mode=True
)
```

---

## 📋 Core Data Models

### EvaluationResult
Complete evaluation result with metrics, gates, and analysis.

```python
@dataclass
class EvaluationResult:
    pipeline_name: str
    algorithm_name: str
    timestamp: datetime
    status: ResultStatus
    metrics: Dict[str, MetricResult]
    gate_result: Optional[GateResult]
    analysis: Optional[Analysis]
    errors: List[str]
    warnings: List[str]
```

### MetricResult
Individual metric measurement.

```python
@dataclass
class MetricResult:
    name: str
    value: float
    threshold: Optional[float]
    passed: bool
    unit: str
    description: str
```

### GateResult
Quality gate validation result.

```python
@dataclass
class GateResult:
    passed: bool
    threshold: float
    score: float
    blocked: bool
    reason: Optional[str]
```

### Analysis
AI-powered analysis from AEVA-Brain.

```python
@dataclass
class Analysis:
    summary: str
    root_causes: List[str]
    recommendations: List[str]
    severity: str  # info, warning, error, critical
    confidence: float
```

---

## 🔌 Service Interfaces

All services implement standardized interfaces for consistency.

### Benchmark Service Interface

```python
class IBenchmarkService(Protocol):
    async def create_benchmark(self, config: BenchmarkConfig) -> str
    async def run_benchmark(self, benchmark_id: str) -> EvaluationResult
    async def get_results(self, benchmark_id: str) -> List[EvaluationResult]
    async def list_benchmarks(self) -> List[BenchmarkInfo]
```

### Guard Service Interface

```python
class IGuardService(Protocol):
    async def register_gate(self, gate: GateConfig) -> str
    async def validate(self, result: EvaluationResult, gate_id: str) -> GateResult
    async def get_gate_status(self, gate_id: str) -> GateStatus
    async def get_history(self, filters: Dict) -> List[GateResult]
```

---

## 🔧 Configuration Schemas

### Service Discovery Configuration

```python
from aeva_common.config import ServiceRegistry

registry = ServiceRegistry.from_yaml("services.yaml")
bench_url = registry.get_service_url("bench")
guard_url = registry.get_service_url("guard")
```

### Example `services.yaml`

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

## 🌐 HTTP Client Usage

### Base Client

```python
from aeva_common.clients import BaseServiceClient

class CustomClient(BaseServiceClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)

    async def custom_call(self, data: dict) -> dict:
        return await self.post("/custom/endpoint", json=data)
```

### Error Handling

```python
from aeva_common.clients import ServiceError, ServiceTimeout

try:
    result = await bench_client.run_benchmark(...)
except ServiceTimeout:
    # Handle timeout
    pass
except ServiceError as e:
    # Handle service error
    print(f"Service error: {e.status_code} - {e.message}")
```

---

## 📊 API Contracts

All services follow REST API conventions:

### Common Endpoints
- `GET /health` - Service health check
- `GET /version` - Service version info
- `GET /metrics` - Prometheus metrics

### Standard Response Format

```json
{
  "status": "success|error",
  "data": {...},
  "error": null,
  "timestamp": "2026-04-13T10:00:00Z"
}
```

---

## 🧪 Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Type checking
mypy aeva_common/

# Code formatting
black aeva_common/
```

---

## 📝 Development

### Adding New Models

1. Define model in `aeva_common/models/`
2. Export in `__init__.py`
3. Add tests
4. Update documentation

### Adding New Service Interface

1. Define interface in `aeva_common/interfaces/`
2. Create client in `aeva_common/clients/`
3. Add configuration schema
4. Update documentation

---

## 🔄 Version Compatibility

| aeva-common | AEVA Platform | Python |
|-------------|---------------|---------|
| 0.1.x       | 2.0.x         | >=3.8   |

---

## 📄 License

Dual License:
- **Personal/Academic Use**: Free
- **Commercial Use**: Requires Permission

Copyright © 2024-2026 AEVA Development Team

---

## 🤝 Contributing

This is part of the AEVA platform microservices architecture initiative.

For questions or contributions, please refer to the main AEVA repository.

---

**Status**: ✅ Phase 1 - SDK Extraction Complete
**Next**: Phase 2 - Service Implementation
