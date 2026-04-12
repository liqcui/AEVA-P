# AEVA Kubernetes Deployment Guide

本目录包含AEVA平台的Kubernetes生产部署配置文件。

## 📋 目录结构

```
k8s/
├── README.md                        # 本文件
├── configmap.yaml                   # 配置和密钥
├── aeva-api-deployment.yaml         # API服务器部署
├── aeva-worker-statefulset.yaml     # Worker集群部署
├── ingress.yaml                     # 入口和负载均衡
└── monitoring.yaml                  # Prometheus监控
```

## 🚀 快速开始

### 前置条件

1. Kubernetes集群 (v1.24+)
2. kubectl 配置完成
3. Helm 3 (用于依赖服务)
4. 足够的集群资源 (至少 16 CPU, 32GB RAM)

### 第一步: 创建命名空间

```bash
kubectl create namespace aeva
```

### 第二步: 部署依赖服务

#### 2.1 PostgreSQL (使用Helm)

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami

helm install postgres-ha bitnami/postgresql-ha \
  --namespace aeva \
  --set global.postgresql.password=CHANGE_ME \
  --set postgresql.replicaCount=2 \
  --set persistence.size=100Gi
```

#### 2.2 Redis Sentinel (使用Helm)

```bash
helm install redis bitnami/redis \
  --namespace aeva \
  --set architecture=replication \
  --set sentinel.enabled=true \
  --set master.persistence.size=20Gi
```

#### 2.3 RabbitMQ (使用Helm)

```bash
helm install rabbitmq bitnami/rabbitmq \
  --namespace aeva \
  --set auth.username=aeva \
  --set auth.password=CHANGE_ME \
  --set replicaCount=3 \
  --set persistence.size=20Gi
```

### 第三步: 配置密钥

**重要**: 修改 `configmap.yaml` 中的密钥：

```bash
# 编辑配置文件
vi configmap.yaml

# 修改以下字段:
# - db_password
# - brain_api_key
# - rabbitmq_password

# 应用配置
kubectl apply -f configmap.yaml
```

### 第四步: 构建和推送Docker镜像

```bash
# 构建镜像
docker build -t your-registry/aeva:latest .

# 推送到镜像仓库
docker push your-registry/aeva:latest

# 更新deployment中的镜像地址
sed -i 's|image: aeva:latest|image: your-registry/aeva:latest|g' *.yaml
```

### 第五步: 部署AEVA组件

```bash
# 部署API服务器 (3副本 + HPA)
kubectl apply -f aeva-api-deployment.yaml

# 部署Worker集群 (5副本 + HPA)
kubectl apply -f aeva-worker-statefulset.yaml

# 部署Ingress和Dashboard
kubectl apply -f ingress.yaml

# 部署监控 (Prometheus)
kubectl apply -f monitoring.yaml
```

### 第六步: 验证部署

```bash
# 检查所有Pod状态
kubectl get pods -n aeva

# 应该看到:
# - aeva-api-xxx (3个)
# - aeva-worker-0/1/2/3/4 (5个)
# - aeva-dashboard-xxx (2个)
# - prometheus-xxx (1个)

# 检查服务
kubectl get svc -n aeva

# 检查HPA
kubectl get hpa -n aeva
```

### 第七步: 配置域名和SSL

```bash
# 安装cert-manager (如果还没有)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.0/cert-manager.yaml

# 创建Let's Encrypt issuer
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

# 更新ingress.yaml中的域名
# - aeva.example.com -> your-domain.com
# - api.aeva.example.com -> api.your-domain.com

# 重新应用ingress
kubectl apply -f ingress.yaml
```

### 第八步: 访问服务

```bash
# 获取Ingress地址
kubectl get ingress -n aeva

# 访问:
# - https://api.your-domain.com  (API服务)
# - https://your-domain.com      (Dashboard)
```

## 📊 监控和日志

### 访问Prometheus

```bash
# 端口转发
kubectl port-forward -n aeva svc/prometheus 9090:9090

# 访问 http://localhost:9090
```

### 访问Grafana (如果已安装)

```bash
# 安装Grafana
helm install grafana grafana/grafana \
  --namespace aeva \
  --set persistence.enabled=true \
  --set persistence.size=10Gi \
  --set adminPassword=admin

# 端口转发
kubectl port-forward -n aeva svc/grafana 3000:3000

# 访问 http://localhost:3000
# 添加Prometheus数据源: http://prometheus:9090
```

### 查看日志

```bash
# API日志
kubectl logs -n aeva -l app=aeva-api --tail=100 -f

# Worker日志
kubectl logs -n aeva -l app=aeva-worker --tail=100 -f

# 所有容器日志
kubectl logs -n aeva --all-containers=true -l app=aeva-api -f
```

## 🔧 扩缩容

### 手动扩容

```bash
# 扩容API服务器到10个
kubectl scale deployment aeva-api -n aeva --replicas=10

# 扩容Worker到20个
kubectl scale statefulset aeva-worker -n aeva --replicas=20
```

### 自动扩容 (HPA)

HPA已配置:
- **API**: 3-20副本 (基于CPU 70%, Memory 80%)
- **Worker**: 3-50副本 (基于CPU 70%, Memory 80%, Queue Length)

```bash
# 查看HPA状态
kubectl get hpa -n aeva

# 查看HPA详情
kubectl describe hpa aeva-api-hpa -n aeva
kubectl describe hpa aeva-worker-hpa -n aeva
```

## 🔐 安全最佳实践

### 1. 密钥管理

使用Kubernetes Secrets或外部密钥管理:

```bash
# 使用sealed-secrets
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.18.0/controller.yaml

# 或使用外部密钥管理 (AWS Secrets Manager, Vault)
```

### 2. 网络策略

```bash
# 创建网络策略限制流量
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: aeva-network-policy
  namespace: aeva
spec:
  podSelector:
    matchLabels:
      app: aeva-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres-ha
    ports:
    - protocol: TCP
      port: 5432
EOF
```

### 3. Pod Security Policy

```bash
# 启用Pod Security Standards
kubectl label namespace aeva pod-security.kubernetes.io/enforce=restricted
```

## 🧪 测试部署

```bash
# 测试API健康检查
kubectl run test-pod --rm -it --image=curlimages/curl --restart=Never -- \
  curl http://aeva-api:8000/health

# 测试任务提交
kubectl run test-pod --rm -it --image=curlimages/curl --restart=Never -- \
  curl -X POST http://aeva-api:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"type": "benchmark", "params": {}}'
```

## 📈 性能调优

### 资源请求和限制

根据实际负载调整 `resources` 配置:

```yaml
resources:
  requests:
    memory: "512Mi"    # 初始申请
    cpu: "500m"
  limits:
    memory: "2Gi"      # 最大限制
    cpu: "2000m"
```

### Worker并发数

调整Celery worker并发:

```yaml
args:
- "-c"
- "8"  # 每个worker 8个并发
```

### 数据库连接池

在configmap中调整:

```yaml
db_pool_size: "20"
db_max_overflow: "10"
```

## 🔄 滚动更新

```bash
# 更新镜像
kubectl set image deployment/aeva-api aeva-api=your-registry/aeva:v2.0 -n aeva

# 查看滚动更新状态
kubectl rollout status deployment/aeva-api -n aeva

# 回滚
kubectl rollout undo deployment/aeva-api -n aeva
```

## 💾 备份和恢复

### 数据库备份

```bash
# 创建CronJob定时备份
cat <<EOF | kubectl apply -f -
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
  namespace: aeva
spec:
  schedule: "0 2 * * *"  # 每天凌晨2点
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:14-alpine
            command:
            - /bin/sh
            - -c
            - |
              pg_dump -h postgres-ha -U aeva aeva > /backup/backup-\$(date +%Y%m%d).sql
            volumeMounts:
            - name: backup
              mountPath: /backup
          volumes:
          - name: backup
            persistentVolumeClaim:
              claimName: backup-pvc
          restartPolicy: OnFailure
EOF
```

## 🆘 故障排查

### Pod无法启动

```bash
# 查看Pod事件
kubectl describe pod <pod-name> -n aeva

# 查看日志
kubectl logs <pod-name> -n aeva --previous
```

### 服务连接失败

```bash
# 检查服务端点
kubectl get endpoints -n aeva

# 测试DNS解析
kubectl run test-dns --rm -it --image=busybox --restart=Never -- \
  nslookup aeva-api.aeva.svc.cluster.local
```

### HPA不工作

```bash
# 检查metrics-server
kubectl get deployment metrics-server -n kube-system

# 如果没有，安装:
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

## 📚 更多资源

- [Kubernetes文档](https://kubernetes.io/docs/)
- [Celery文档](https://docs.celeryq.dev/)
- [AEVA架构文档](../SCALABILITY_ARCHITECTURE.md)
- [AEVA LLM评测文档](../LLM_EVALUATION_IMPLEMENTATION.md)

## 🤝 支持

遇到问题?

- GitHub Issues: https://github.com/liqcui/AEVA-P/issues
- Email: liquan_cui@126.com

---

**AEVA v2.0 - Production Kubernetes Deployment**
**Copyright © 2024-2026 AEVA Development Team**
**Watermark: AEVA-2026-LQC-dc68e33**
