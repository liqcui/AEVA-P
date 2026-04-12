# AEVA Docker 部署指南

**版本**: AEVA v2.0
**日期**: 2026-04-12
**状态**: ✅ Production Ready

---

## 概览

AEVA提供完整的Docker支持，包括：

- ✅ 多阶段优化构建
- ✅ 基础版和生产版镜像
- ✅ Docker Compose编排
- ✅ 健康检查
- ✅ 智能入口脚本

---

## 快速开始

### 1. 构建镜像

```bash
# 生产版（包含所有库，~2GB）
docker build -t aeva:latest .

# 基础版（仅核心依赖，~800MB）
docker build -f Dockerfile.basic -t aeva:basic .
```

### 2. 运行快速测试

```bash
# 使用生产版
docker run --rm aeva:latest quick-tests

# 使用基础版
docker run --rm aeva:basic python examples/run_all_quick_tests.py
```

### 3. 启动仪表板

```bash
docker run --rm -p 8501:8501 aeva:latest dashboard
```

访问: http://localhost:8501

---

## Docker镜像说明

### 生产版镜像 (Dockerfile)

**特点**:
- 包含所有生产级库（ART, GE, statsmodels, Streamlit）
- 多阶段构建优化
- 完整功能
- 镜像大小: ~2GB

**适用场景**:
- 生产环境
- 完整功能测试
- 仪表板部署
- 性能关键应用

**构建**:
```bash
docker build -t aeva:prod .
```

---

### 基础版镜像 (Dockerfile.basic)

**特点**:
- 仅核心依赖（scikit-learn, shap, lime, scipy）
- 使用Fallback实现
- 快速构建
- 镜像大小: ~800MB

**适用场景**:
- 开发环境
- CI/CD测试
- 资源受限环境
- 快速原型

**构建**:
```bash
docker build -f Dockerfile.basic -t aeva:basic .
```

---

## 使用Docker Compose

### 配置文件

#### docker-compose.yml (生产版)

包含服务:
- `aeva` - 核心服务
- `aeva-dashboard` - Streamlit仪表板
- `aeva-examples` - 示例运行器
- `aeva-production` - 生产集成演示

#### docker-compose.basic.yml (基础版)

包含服务:
- `aeva-basic` - 基础测试
- `aeva-tests` - 单元测试

---

### 常用命令

#### 启动所有服务

```bash
# 生产版
docker-compose up

# 基础版
docker-compose -f docker-compose.basic.yml up
```

#### 启动特定服务

```bash
# 启动仪表板
docker-compose up aeva-dashboard

# 运行示例
docker-compose up aeva-examples

# 运行生产集成
docker-compose up aeva-production
```

#### 后台运行

```bash
docker-compose up -d aeva-dashboard
```

#### 查看日志

```bash
docker-compose logs -f aeva-dashboard
```

#### 停止服务

```bash
docker-compose down
```

---

## 入口脚本命令

AEVA容器支持以下命令:

### 测试命令

```bash
# 快速功能测试
docker run --rm aeva:latest quick-tests

# 完整单元测试
docker run --rm aeva:latest full-tests

# 生产集成演示
docker run --rm aeva:latest production-demo
```

### 仪表板命令

```bash
# 启动仪表板（需要映射端口）
docker run --rm -p 8501:8501 aeva:latest dashboard
```

### 工具命令

```bash
# 检查生产库可用性
docker run --rm aeva:latest check-libs

# 进入交互式Shell
docker run --rm -it aeva:latest shell

# 启动Python REPL
docker run --rm -it aeva:latest python

# 显示帮助
docker run --rm aeva:latest help
```

### 自定义命令

```bash
# 运行特定Python脚本
docker run --rm aeva:latest python examples/quick_robustness.py

# 运行特定pytest测试
docker run --rm aeva:latest pytest tests/test_model_cards.py -v
```

---

## 数据持久化

### 挂载卷

```bash
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/results:/app/results \
  -v $(pwd)/logs:/app/logs \
  aeva:latest quick-tests
```

### Docker Compose卷

已在`docker-compose.yml`中配置:

```yaml
volumes:
  - ./data:/app/data
  - ./results:/app/results
  - ./logs:/app/logs
  - ./config:/app/config
```

---

## 环境变量

### 支持的环境变量

```bash
# Python相关
PYTHONUNBUFFERED=1        # 禁用Python输出缓冲
PYTHONPATH=/app           # Python路径

# AEVA相关
AEVA_ENV=production       # 环境（development/production）
AEVA_LOG_LEVEL=INFO       # 日志级别（DEBUG/INFO/WARNING/ERROR）
```

### 设置环境变量

```bash
# 命令行
docker run --rm -e AEVA_LOG_LEVEL=DEBUG aeva:latest quick-tests

# Docker Compose
environment:
  - AEVA_ENV=production
  - AEVA_LOG_LEVEL=INFO
```

---

## 高级用法

### 多阶段构建优化

Dockerfile使用多阶段构建:

1. **Builder阶段**: 编译依赖
2. **Runtime阶段**: 仅复制必要文件

**优势**:
- 减小镜像大小
- 提高安全性
- 加快部署速度

### 健康检查

容器包含健康检查:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import aeva; print('OK')" || exit 1
```

**查看健康状态**:

```bash
docker ps
# STATUS列会显示 (healthy) 或 (unhealthy)
```

### 网络配置

所有服务使用自定义网络:

```yaml
networks:
  aeva-network:
    driver: bridge
```

**服务间通信**:
```bash
# 在aeva容器中可以访问
curl http://aeva-dashboard:8501
```

---

## 常见场景

### 场景1: 开发测试

```bash
# 使用基础版快速测试
docker-compose -f docker-compose.basic.yml run aeva-basic

# 运行单元测试
docker-compose -f docker-compose.basic.yml run aeva-tests
```

### 场景2: 生产部署

```bash
# 构建生产镜像
docker build -t aeva:prod .

# 启动仪表板
docker run -d \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/results:/app/results \
  --name aeva-dashboard \
  aeva:prod dashboard
```

### 场景3: CI/CD集成

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build image
        run: docker build -f Dockerfile.basic -t aeva:test .
      - name: Run tests
        run: docker run --rm aeva:test full-tests
```

### 场景4: 演示环境

```bash
# 启动所有服务
docker-compose up -d

# 访问
# - 仪表板: http://localhost:8501
# - 查看示例日志: docker-compose logs -f aeva-examples
```

---

## 性能优化

### 构建优化

```bash
# 使用BuildKit加速
DOCKER_BUILDKIT=1 docker build -t aeva:latest .

# 使用缓存
docker build --cache-from aeva:latest -t aeva:latest .
```

### 运行优化

```bash
# 限制资源
docker run --rm \
  --cpus=2 \
  --memory=4g \
  aeva:latest quick-tests

# 使用tmpfs加速I/O
docker run --rm \
  --tmpfs /tmp:rw,size=1g \
  aeva:latest quick-tests
```

---

## 故障排除

### 问题1: 镜像构建失败

**症状**: 依赖安装失败

**解决**:
```bash
# 清理Docker缓存
docker builder prune -a

# 重新构建
docker build --no-cache -t aeva:latest .
```

### 问题2: 容器无法启动

**症状**: 容器立即退出

**诊断**:
```bash
# 查看日志
docker logs <container_id>

# 进入调试模式
docker run --rm -it aeva:latest shell
python -c "import aeva; print(aeva.__version__)"
```

### 问题3: 仪表板无法访问

**症状**: 浏览器无法连接到8501端口

**检查**:
```bash
# 确认端口映射
docker ps | grep 8501

# 确认容器运行
docker-compose logs aeva-dashboard

# 测试连接
curl http://localhost:8501
```

### 问题4: 性能慢

**症状**: 测试运行缓慢

**解决**:
```bash
# 增加资源
docker run --rm --cpus=4 --memory=8g aeva:latest quick-tests

# 使用生产镜像（有性能优化）
docker build -t aeva:prod .
docker run --rm aeva:prod quick-tests
```

---

## 镜像管理

### 清理镜像

```bash
# 删除未使用的镜像
docker image prune

# 删除所有AEVA镜像
docker rmi $(docker images -q aeva)

# 清理所有未使用资源
docker system prune -a
```

### 镜像标签

```bash
# 构建并标签
docker build -t aeva:v2.0 .
docker tag aeva:v2.0 aeva:latest

# 推送到仓库
docker tag aeva:v2.0 yourregistry/aeva:v2.0
docker push yourregistry/aeva:v2.0
```

---

## 安全建议

### 1. 非root用户运行

```dockerfile
# 在Dockerfile中添加
RUN useradd -m -u 1000 aeva
USER aeva
```

### 2. 只读文件系统

```bash
docker run --rm --read-only \
  --tmpfs /tmp \
  aeva:latest quick-tests
```

### 3. 限制能力

```bash
docker run --rm \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  aeva:latest dashboard
```

### 4. 安全扫描

```bash
# 使用trivy扫描
trivy image aeva:latest

# 使用Snyk扫描
snyk container test aeva:latest
```

---

## 最佳实践

### 开发环境

```bash
# 使用基础镜像快速迭代
docker build -f Dockerfile.basic -t aeva:dev .

# 挂载源代码实现热重载
docker run --rm -it \
  -v $(pwd)/aeva:/app/aeva \
  aeva:dev shell
```

### 生产环境

```bash
# 使用生产镜像
docker build -t aeva:prod .

# 使用docker-compose管理
docker-compose -f docker-compose.yml up -d

# 配置日志
docker-compose logs -f > aeva.log
```

### CI/CD环境

```bash
# 使用基础镜像快速测试
docker build -f Dockerfile.basic -t aeva:ci .
docker run --rm aeva:ci full-tests
```

---

## 资源需求

### 最小要求

- **CPU**: 2核
- **内存**: 4GB
- **磁盘**: 10GB

### 推荐配置

- **CPU**: 4核
- **内存**: 8GB
- **磁盘**: 20GB

### 生产环境

- **CPU**: 8核
- **内存**: 16GB
- **磁盘**: 50GB

---

## 总结

### Docker支持特性

- ✅ 多阶段优化构建
- ✅ 基础版和生产版镜像
- ✅ Docker Compose编排
- ✅ 健康检查
- ✅ 入口脚本
- ✅ 数据持久化
- ✅ 环境变量配置
- ✅ 完整文档

### 常用命令速查

```bash
# 构建
docker build -t aeva:latest .                    # 生产版
docker build -f Dockerfile.basic -t aeva:basic . # 基础版

# 运行
docker run --rm aeva:latest quick-tests          # 快速测试
docker run --rm -p 8501:8501 aeva:latest dashboard # 仪表板

# Compose
docker-compose up                                # 启动所有
docker-compose up aeva-dashboard                 # 启动仪表板
docker-compose down                              # 停止

# 管理
docker ps                                        # 查看运行容器
docker logs -f <container>                       # 查看日志
docker exec -it <container> bash                 # 进入容器
```

---

**项目**: AEVA v2.0
**文档**: Docker部署指南
**状态**: ✅ 完整
**更新**: 2026-04-12
