# AEVA Infrastructure

**Project**: AEVA v2.0 - Infrastructure & Deployment
**Date**: 2026-04-13
**Project ID**: AEVA-2026-LQC-dc68e33

---

## 📁 Directory Structure

```
infrastructure/
├── docker/              # Docker configurations
│   ├── base/           # Base Docker images
│   ├── services/       # Service-specific Dockerfiles
│   └── compose/        # Docker Compose files
├── kubernetes/          # Kubernetes manifests
│   ├── base/           # Base configurations
│   ├── services/       # Service deployments
│   ├── ingress/        # Ingress configurations
│   └── monitoring/     # Monitoring stack
└── monitoring/          # Monitoring & observability
    ├── prometheus/     # Prometheus configs
    ├── grafana/        # Grafana dashboards
    └── jaeger/         # Distributed tracing
```

---

## 🐳 Docker Infrastructure

### Base Images

**Location**: `infrastructure/docker/base/`

Standard base images for all services:
- `python-base.Dockerfile` - Python 3.11 + common dependencies
- `fastapi-base.Dockerfile` - FastAPI service base
- `worker-base.Dockerfile` - Celery worker base

### Service Dockerfiles

Each service has optimized multi-stage build:

```dockerfile
# Stage 1: Build
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

**Development**: `infrastructure/docker/compose/docker-compose.dev.yml`
**Production**: `infrastructure/docker/compose/docker-compose.prod.yml`

---

## ☸️ Kubernetes Infrastructure

### Namespace Organization

```
aeva-system          # Core AEVA services
├── bench-service
├── guard-service
├── auto-service
├── brain-service
└── gateway

aeva-infra           # Infrastructure services
├── postgresql
├── redis
└── monitoring

aeva-monitoring      # Observability stack
├── prometheus
├── grafana
└── jaeger
```

### Resource Structure

Each service includes:
- **Deployment** - Service pods
- **Service** - Internal networking
- **ConfigMap** - Configuration
- **Secret** - Sensitive data
- **HPA** - Horizontal Pod Autoscaler
- **PDB** - Pod Disruption Budget

### Example Service Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bench-service
  namespace: aeva-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bench-service
  template:
    metadata:
      labels:
        app: bench-service
    spec:
      containers:
      - name: bench-service
        image: aeva/bench-service:latest
        ports:
        - containerPort: 8001
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: bench-service-secret
              key: database-url
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8001
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## 📊 Monitoring & Observability

### Prometheus

**Metrics Collection**:
- Service metrics (requests, latency, errors)
- Infrastructure metrics (CPU, memory, disk)
- Custom business metrics

**Scrape Configs**:
```yaml
scrape_configs:
  - job_name: 'bench-service'
    static_configs:
      - targets: ['bench-service:8001']
    metrics_path: '/metrics'
```

### Grafana

**Dashboards**:
- Service Overview (requests, latency, error rate)
- Database Performance
- Resource Utilization
- Business Metrics (benchmarks/day, gates validated)

### Jaeger

**Distributed Tracing**:
- Request flow across services
- Performance bottleneck identification
- Error propagation tracking

---

## 🔐 Security

### Secrets Management

**Development**: Environment variables
**Production**: Kubernetes Secrets or External Secret Manager

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: bench-service-secret
type: Opaque
data:
  database-url: <base64-encoded>
  api-key: <base64-encoded>
```

### Network Policies

Restrict service-to-service communication:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: bench-service-policy
spec:
  podSelector:
    matchLabels:
      app: bench-service
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: gateway
    ports:
    - protocol: TCP
      port: 8001
```

---

## 🚀 Deployment Strategies

### Rolling Update (Default)

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```

### Blue-Green Deployment

Use service selectors to switch traffic:
```bash
kubectl set selector service bench-service 'version=green'
```

### Canary Deployment

Use Istio or NGINX for traffic splitting:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: bench-service
spec:
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: bench-service
        subset: v2
      weight: 10
  - route:
    - destination:
        host: bench-service
        subset: v1
      weight: 90
```

---

## 📈 Scaling

### Horizontal Pod Autoscaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: bench-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: bench-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Vertical Pod Autoscaling

For services with variable resource needs:
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: brain-service-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: brain-service
  updatePolicy:
    updateMode: "Auto"
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

```yaml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Build Docker image
        run: docker build -t aeva/bench-service:${{ github.sha }} .

      - name: Push to registry
        run: docker push aeva/bench-service:${{ github.sha }}

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/bench-service \
            bench-service=aeva/bench-service:${{ github.sha }}
```

---

## 🗄️ Database Infrastructure

### PostgreSQL

**Deployment**: StatefulSet with persistent volumes

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgresql
spec:
  serviceName: postgresql
  replicas: 1
  template:
    spec:
      containers:
      - name: postgresql
        image: postgres:15
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi
```

### Redis

**Deployment**: StatefulSet with persistence

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
spec:
  serviceName: redis
  replicas: 1
  template:
    spec:
      containers:
      - name: redis
        image: redis:7
        command: ["redis-server", "--appendonly", "yes"]
        volumeMounts:
        - name: data
          mountPath: /data
```

---

## 🌐 Ingress

### NGINX Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: aeva-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: api.aeva.example.com
    http:
      paths:
      - path: /v1/benchmark
        pathType: Prefix
        backend:
          service:
            name: bench-service
            port:
              number: 8001
      - path: /v1/gate
        pathType: Prefix
        backend:
          service:
            name: guard-service
            port:
              number: 8002
```

---

## 📦 Resource Requirements

### Recommended Node Specs

**Development**:
- 1 node: 8 CPU, 16 GB RAM

**Staging**:
- 3 nodes: 4 CPU, 8 GB RAM each

**Production**:
- 5+ nodes: 8 CPU, 16 GB RAM each
- Auto-scaling enabled

### Service Resource Allocation

| Service | CPU Request | CPU Limit | Memory Request | Memory Limit |
|---------|-------------|-----------|----------------|--------------|
| Gateway | 500m | 1000m | 512Mi | 1Gi |
| Bench | 1000m | 2000m | 2Gi | 4Gi |
| Guard | 500m | 1000m | 1Gi | 2Gi |
| Auto | 1000m | 2000m | 2Gi | 4Gi |
| Brain | 1000m | 2000m | 2Gi | 4Gi |
| PostgreSQL | 2000m | 4000m | 4Gi | 8Gi |
| Redis | 500m | 1000m | 1Gi | 2Gi |

---

## 🔧 Local Development Setup

### Prerequisites
```bash
# Install Docker Desktop
# Install kubectl
# Install helm (optional)
# Install k3d or minikube (for local Kubernetes)
```

### Quick Start
```bash
# Start local Kubernetes cluster
k3d cluster create aeva-dev

# Deploy infrastructure
kubectl apply -f infrastructure/kubernetes/base/

# Deploy services
kubectl apply -f infrastructure/kubernetes/services/

# Port forward for local access
kubectl port-forward svc/gateway 8000:8000
```

---

## 📝 Next Steps

1. ✅ Infrastructure structure created
2. ⏳ Create base Docker images
3. ⏳ Create service Dockerfiles
4. ⏳ Create Docker Compose files
5. ⏳ Create Kubernetes manifests
6. ⏳ Setup monitoring stack
7. ⏳ Configure CI/CD pipeline
8. ⏳ Setup secrets management
9. ⏳ Test deployment

---

**Status**: 📁 Infrastructure Structure Created
**Next**: Create Docker and Kubernetes configurations

Copyright © 2024-2026 AEVA Development Team
