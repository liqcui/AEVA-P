# AEVA Project Structure

**Version**: 2.0 - Microservices Architecture
**Date**: 2026-04-13
**Project ID**: AEVA-2026-LQC-dc68e33

---

## 📁 Repository Structure

```
AVEA-P/
├── aeva/                        # Original monolithic modules (kept for reference)
│   ├── core/                    # Shared core utilities
│   ├── dashboard/               # Streamlit dashboard
│   ├── api/                     # Original monolithic API
│   ├── bench/                   # Benchmark module
│   ├── guard/                   # Guard module
│   ├── auto/                    # Auto pipeline module
│   ├── brain/                   # Brain module
│   └── [19 more modules]/       # Additional modules
│
├── aeva-common/                 # ⭐ Shared SDK for microservices
│   ├── aeva_common/
│   │   ├── models/              # Shared data models
│   │   ├── config/              # Configuration schemas
│   │   ├── interfaces/          # Service interfaces
│   │   └── clients/             # HTTP clients
│   ├── docs/                    # API documentation
│   ├── setup.py                 # Package configuration
│   └── README.md
│
├── services/                    # ⭐ Microservices implementations
│   ├── bench-service/           # Benchmark service (Port 8001)
│   ├── guard-service/           # Quality gate service (Port 8002)
│   ├── auto-service/            # Pipeline service (Port 8003)
│   ├── brain-service/           # AI analysis service (Port 8004)
│   ├── gateway/                 # API Gateway (Port 8000)
│   └── README.md
│
├── infrastructure/              # ⭐ Infrastructure & deployment
│   ├── docker/                  # Docker configurations
│   │   ├── base/                # Base images
│   │   ├── services/            # Service Dockerfiles
│   │   └── compose/             # Docker Compose files
│   ├── kubernetes/              # Kubernetes manifests
│   │   ├── base/                # Base configs
│   │   ├── services/            # Service deployments
│   │   ├── ingress/             # Ingress configs
│   │   └── monitoring/          # Monitoring stack
│   ├── monitoring/              # Observability
│   │   ├── prometheus/          # Metrics
│   │   ├── grafana/             # Dashboards
│   │   └── jaeger/              # Tracing
│   └── README.md
│
├── deployments/                 # ⭐ Deployment configurations
│   ├── docker-compose.yml       # All services (dev)
│   ├── docker-compose.prod.yml  # Production setup
│   └── k8s/                     # Kubernetes deployment
│
├── docs/                        # Documentation
│   ├── MICROSERVICE_DECOUPLING_PHASE1.md
│   ├── DASHBOARD_9_4_VERIFICATION.md
│   └── api/                     # API documentation
│
├── demo/                        # Interactive demo
│   └── index.html               # Offline HTML demo
│
├── scripts/                     # Utility scripts
│   ├── deploy.sh                # Deployment script
│   ├── test.sh                  # Test runner
│   └── setup-dev.sh             # Dev environment setup
│
├── .github/                     # GitHub Actions
│   └── workflows/               # CI/CD pipelines
│       ├── build-services.yml
│       ├── deploy-k8s.yml
│       └── test.yml
│
├── README.md                    # Main project README
├── DEPLOYMENT_MODE.md           # Deployment comparison guide
├── PROJECT_STRUCTURE.md         # This file
├── LICENSE                      # License file
└── requirements.txt             # Python dependencies (monolithic)
```

---

## 🎯 Key Directories

### 1. `aeva-common/` - Shared SDK ⭐

**Purpose**: Shared data structures, interfaces, and clients for all microservices

**Contents**:
- Data models: `EvaluationResult`, `MetricResult`, `GateResult`, `Analysis`
- Service interfaces: Protocol-based API contracts
- HTTP clients: Async service clients
- Configuration schemas: Pydantic models

**Installation**:
```bash
cd aeva-common
pip install -e .
```

**Import Example**:
```python
from aeva_common.models import EvaluationResult
from aeva_common.clients import BenchClient
```

---

### 2. `services/` - Microservices ⭐

**Purpose**: Individual service implementations

**Standard Service Structure**:
```
service-name/
├── app/
│   ├── main.py              # FastAPI app
│   ├── api/v1/              # API routes
│   ├── core/                # Core logic
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   └── services/            # Business logic
├── tests/                   # Unit & integration tests
├── Dockerfile               # Container image
├── requirements.txt         # Dependencies
└── README.md
```

**Services**:
- `bench-service` (8001) - Benchmark testing
- `guard-service` (8002) - Quality gates
- `auto-service` (8003) - Pipeline orchestration
- `brain-service` (8004) - AI analysis
- `gateway` (8000) - API Gateway

---

### 3. `infrastructure/` - Deployment & Ops ⭐

**Purpose**: Infrastructure as Code for deployment

**Contents**:
- Docker: Base images, Dockerfiles, Compose files
- Kubernetes: Deployments, Services, Ingress, ConfigMaps
- Monitoring: Prometheus, Grafana, Jaeger configs

**Quick Deploy**:
```bash
# Docker Compose (local)
docker-compose -f deployments/docker-compose.yml up

# Kubernetes (production)
kubectl apply -f infrastructure/kubernetes/
```

---

### 4. `aeva/` - Legacy Monolithic Code

**Purpose**: Original monolithic implementation (kept for reference)

**Status**: Maintained on `deployment/monolithic` branch

**Migration Path**: Code being extracted to microservices

---

## 🚀 Development Workflow

### Local Development

**Option 1: Run Individual Service**
```bash
cd services/bench-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

**Option 2: Run All Services (Docker Compose)**
```bash
docker-compose -f deployments/docker-compose.yml up
```

**Option 3: Run on Local Kubernetes**
```bash
k3d cluster create aeva-dev
kubectl apply -f infrastructure/kubernetes/
```

---

### Testing

**Unit Tests**:
```bash
cd services/bench-service
pytest tests/
```

**Integration Tests**:
```bash
# Start all services
docker-compose up -d

# Run integration tests
pytest tests/integration/
```

**End-to-End Tests**:
```bash
./scripts/test.sh --e2e
```

---

### Deployment

**Development**:
```bash
./scripts/deploy.sh --env dev
```

**Staging**:
```bash
./scripts/deploy.sh --env staging
```

**Production**:
```bash
./scripts/deploy.sh --env production
```

---

## 📦 Artifacts & Outputs

### Docker Images

Built images:
- `aeva/bench-service:latest`
- `aeva/guard-service:latest`
- `aeva/auto-service:latest`
- `aeva/brain-service:latest`
- `aeva/gateway:latest`

Registry: Docker Hub or private registry

---

### Kubernetes Resources

Deployed resources:
- Deployments (5 services)
- Services (network exposure)
- ConfigMaps (configuration)
- Secrets (sensitive data)
- Ingress (external access)
- HPA (autoscaling)

---

## 🔧 Configuration Management

### Environment Variables

**Development**: `.env` files per service
**Staging/Production**: Kubernetes ConfigMaps & Secrets

**Example** (`services/bench-service/.env`):
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/bench
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=INFO
API_KEY=dev-api-key
```

---

### Configuration Files

**Local**: YAML files in `infrastructure/`
**Kubernetes**: ConfigMaps applied via kubectl

---

## 📊 Monitoring & Observability

### Metrics (Prometheus)

- Endpoint: `http://service:port/metrics`
- Format: Prometheus exposition format
- Metrics: requests, latency, errors, custom business metrics

### Dashboards (Grafana)

- Service overview
- Database performance
- Resource utilization
- Business KPIs

### Tracing (Jaeger)

- Distributed request tracing
- Service dependency mapping
- Performance analysis

### Logs

- Centralized: ELK Stack or Loki
- Format: Structured JSON logs
- Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

---

## 🔐 Security

### Authentication

- **Service-to-Service**: API keys (via headers)
- **User Authentication**: JWT tokens (via Gateway)
- **Admin Access**: RBAC with Kubernetes

### Secrets Management

- **Development**: `.env` files (not committed)
- **Production**: Kubernetes Secrets or external vault

### Network Security

- Kubernetes NetworkPolicies
- Service mesh (Istio - optional)
- TLS/HTTPS for all external traffic

---

## 🎯 Migration Status

### Phase 1: Shared SDK ✅
- ✅ Created `aeva-common` package
- ✅ Defined service interfaces
- ✅ Created HTTP clients
- ✅ Documented API contracts

### Phase 2: Project Structure ✅
- ✅ Created `services/` directory
- ✅ Created `infrastructure/` directory
- ✅ Created `deployments/` directory
- ✅ Documented structure

### Phase 3: Service Implementation ⏳
- ⏳ Implement Bench Service
- ⏳ Implement Guard Service
- ⏳ Implement Brain Service
- ⏳ Implement Auto Service
- ⏳ Implement API Gateway

### Phase 4: Infrastructure ⏳
- ⏳ Create Dockerfiles
- ⏳ Create Docker Compose
- ⏳ Create Kubernetes manifests
- ⏳ Setup monitoring

### Phase 5: CI/CD ⏳
- ⏳ GitHub Actions workflows
- ⏳ Automated testing
- ⏳ Automated deployment

---

## 📚 Documentation

### For Developers

- [services/README.md](services/README.md) - Service development guide
- [infrastructure/README.md](infrastructure/README.md) - Infrastructure guide
- [aeva-common/README.md](aeva-common/README.md) - SDK usage
- [aeva-common/docs/API_CONTRACTS.md](aeva-common/docs/API_CONTRACTS.md) - API specs

### For Operators

- [DEPLOYMENT_MODE.md](DEPLOYMENT_MODE.md) - Deployment comparison
- [infrastructure/kubernetes/](infrastructure/kubernetes/) - K8s manifests
- [deployments/](deployments/) - Deployment configs

### For Users

- [README.md](README.md) - Project overview
- [demo/index.html](demo/index.html) - Interactive demo
- [docs/](docs/) - Additional documentation

---

## 🔄 Version Control Strategy

### Branches

- `main` - Microservices architecture (default)
- `deployment/monolithic` - Monolithic architecture alternative
- `feature/*` - Feature development branches
- `release/*` - Release branches

### Tags

Format: `v{major}.{minor}.{patch}`
- `v2.0.0` - Microservices architecture launch
- `v2.1.0` - New features
- `v2.1.1` - Bug fixes

---

## 📈 Scaling Strategy

### Horizontal Scaling

- Services scale independently via HPA
- Database read replicas
- Redis cluster mode

### Vertical Scaling

- Increase pod resources via VPA
- Upgrade node sizes

### Geographic Distribution

- Multi-region deployment
- CDN for static assets
- Database replication

---

## 💡 Best Practices

### Code Organization

✅ Keep services small and focused
✅ Share code via `aeva-common` package
✅ Use consistent naming conventions
✅ Write comprehensive tests

### Infrastructure

✅ Use Infrastructure as Code (IaC)
✅ Version all configurations
✅ Automate deployments
✅ Monitor everything

### Security

✅ Never commit secrets
✅ Use least privilege principle
✅ Regular security scans
✅ Keep dependencies updated

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/liqcui/AEVA-P.git
cd AEVA-P
```

### 2. Install Shared SDK
```bash
cd aeva-common
pip install -e .
```

### 3. Start Services (Docker Compose)
```bash
docker-compose -f deployments/docker-compose.yml up
```

### 4. Access Services
- Gateway: http://localhost:8000
- Bench: http://localhost:8001
- Guard: http://localhost:8002
- Auto: http://localhost:8003
- Brain: http://localhost:8004

---

**Status**: 📁 Project Structure Complete
**Next**: Implement first service (Bench Service recommended)

Copyright © 2024-2026 AEVA Development Team
