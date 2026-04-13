# AEVA Deployment Modes

**Project**: AEVA v2.0 - Algorithm Evaluation & Validation Agent
**Date**: 2026-04-13
**Project ID**: AEVA-2026-LQC-dc68e33

---

## 🎯 Overview

AEVA supports **multiple deployment architectures** to fit different use cases, scales, and infrastructure requirements. Choose the deployment mode that best fits your needs.

---

## 📦 Deployment Modes

### 1. Monolithic Deployment (Single Application)

**Branch**: `deployment/monolithic`

**Architecture**:
```
Single AEVA Application
├── All 23 modules in one process
├── Shared memory and configuration
├── Direct function calls between modules
└── Single deployment unit
```

**Best For**:
- ✅ Small to medium deployments (< 1000 evaluations/day)
- ✅ Development and testing environments
- ✅ Single-server deployments
- ✅ Quick setup and prototyping
- ✅ Limited infrastructure resources

**Advantages**:
- Simple deployment (single application)
- Fast communication (direct function calls)
- Easy debugging (single process)
- Lower operational complexity
- Minimal infrastructure requirements

**Resource Requirements**:
- CPU: 4-8 cores
- RAM: 8-16 GB
- Storage: 50 GB

**Deployment**:
```bash
git checkout deployment/monolithic
pip install -r requirements.txt
streamlit run aeva/dashboard/app.py
```

---

### 2. Microservices Deployment (Distributed)

**Branch**: `deployment/microservices` (or `feature/microservice-decoupling`)

**Architecture**:
```
API Gateway (Port 8000)
    ├─ Bench Service (Port 8001) - 4C 8G
    ├─ Guard Service (Port 8002) - 2C 4G
    ├─ Auto Service (Port 8003) - 4C 8G
    └─ Brain Service (Port 8004) - 2C 4G

Shared Infrastructure:
    ├─ PostgreSQL
    ├─ Redis
    └─ Message Queue (optional)
```

**Best For**:
- ✅ Large scale deployments (> 1000 evaluations/day)
- ✅ High availability requirements
- ✅ Need to scale services independently
- ✅ Multiple teams working in parallel
- ✅ Cloud-native deployments (Kubernetes)

**Advantages**:
- Independent scaling per service
- Fault isolation (one service failure doesn't crash all)
- Technology flexibility (different languages/frameworks per service)
- Parallel development by multiple teams
- Optimized resource allocation

**Resource Requirements**:
- CPU: 16+ cores (distributed)
- RAM: 32+ GB (distributed)
- Storage: 100+ GB
- Network: High bandwidth between services

**Deployment**:
```bash
git checkout deployment/microservices
docker-compose up -d
# or
kubectl apply -f k8s/
```

---

### 3. Hybrid Deployment (Recommended)

**Branch**: Can be configured on either branch

**Architecture**:
```
Core Services (Microservices):
    ├─ Bench Service (Port 8001)
    ├─ Guard Service (Port 8002)
    ├─ Brain Service (Port 8004)

Extended Modules (Monolithic):
    └─ Dashboard + Other modules
```

**Best For**:
- ✅ Medium to large deployments
- ✅ Gradual migration from monolithic
- ✅ Balance between simplicity and scalability
- ✅ Cost optimization

**Advantages**:
- Scale critical services independently
- Keep non-critical modules simple
- Lower complexity than full microservices
- Easier migration path

---

## 🔄 Switching Between Modes

### From Monolithic to Microservices
```bash
# Current state
git checkout deployment/monolithic

# Switch to microservices
git checkout deployment/microservices

# Migrate data if needed
python scripts/migrate_to_microservices.py
```

### From Microservices to Monolithic
```bash
# Current state
git checkout deployment/microservices

# Switch back to monolithic
git checkout deployment/monolithic

# Consolidate data if needed
python scripts/consolidate_data.py
```

---

## 📊 Comparison Matrix

| Feature | Monolithic | Microservices | Hybrid |
|---------|------------|---------------|--------|
| **Deployment Complexity** | Low | High | Medium |
| **Scaling Flexibility** | Low | High | Medium |
| **Development Speed** | Fast | Slower | Medium |
| **Operational Overhead** | Low | High | Medium |
| **Fault Isolation** | No | Yes | Partial |
| **Resource Efficiency** | Medium | High | High |
| **Cost** | Low | High | Medium |
| **Best for Team Size** | 1-5 | 10+ | 5-10 |

---

## 🎯 Choosing Your Deployment Mode

### Choose Monolithic If:
- Small team (1-5 developers)
- Limited infrastructure budget
- Development/testing environment
- Evaluation volume < 1000/day
- Need quick setup

### Choose Microservices If:
- Large team (10+ developers)
- High availability requirements (99.99%+)
- Evaluation volume > 5000/day
- Need independent scaling
- Cloud-native infrastructure

### Choose Hybrid If:
- Medium team (5-10 developers)
- Growing evaluation volume
- Migrating from monolithic
- Want balance of simplicity and scalability
- Cost-conscious but need some scaling

---

## 🚀 Branch Maintenance

Both branches are **actively maintained**:

**`deployment/monolithic`**:
- Regular updates for bug fixes
- Feature parity with microservices
- Performance optimizations for single-server deployment
- Dashboard and UI improvements

**`deployment/microservices`**:
- Service independence improvements
- API contract updates
- Performance optimizations for distributed systems
- Kubernetes and cloud deployment enhancements

---

## 📝 Migration Paths

### Gradual Migration (Recommended)
1. Start with `deployment/monolithic`
2. Move to Hybrid mode (core services as microservices)
3. Gradually migrate more modules to services
4. Eventually reach full `deployment/microservices`

### Direct Migration
1. Deploy `deployment/microservices` in parallel
2. Migrate data and configuration
3. Switch traffic gradually
4. Decommission monolithic deployment

---

## 🔧 Configuration

### Monolithic Mode
```yaml
# config.yaml
deployment_mode: monolithic
server:
  host: 0.0.0.0
  port: 8501
database:
  type: sqlite  # or postgresql
  path: ./aeva.db
```

### Microservices Mode
```yaml
# config.yaml
deployment_mode: microservices
services:
  bench:
    url: http://bench-service:8001
  guard:
    url: http://guard-service:8002
  auto:
    url: http://auto-service:8003
  brain:
    url: http://brain-service:8004
database:
  type: postgresql
  host: postgres-service
  port: 5432
```

---

## 📚 Documentation

- **Monolithic**: See main `README.md`
- **Microservices**: See `aeva-common/README.md` and `docs/MICROSERVICE_DECOUPLING_PHASE1.md`
- **API Contracts**: See `aeva-common/docs/API_CONTRACTS.md`

---

**Current Branches**:
- `main` - Main development branch
- `deployment/monolithic` - Monolithic deployment mode
- `feature/microservice-decoupling` - Microservices development (will become `deployment/microservices`)

**Both deployment modes are fully supported and will receive updates.** ✨
