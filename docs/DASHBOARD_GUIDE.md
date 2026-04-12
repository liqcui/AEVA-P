# AEVA仪表板使用指南

**版本**: AEVA v2.0
**框架**: Streamlit
**状态**: ✅ Production Ready

---

## 概览

AEVA提供基于Streamlit的交互式Web仪表板，用于可视化和分析模型评估结果。

**功能模块**:
- 🏠 主页 - 系统概览和快速导航
- 🔍 可解释性分析 - SHAP, LIME, 特征重要性
- 🛡️ 对抗鲁棒性 - FGSM, PGD等攻击测试
- 📊 数据质量 - 数据画像和质量指标
- 📈 A/B测试 - 统计检验和模型对比
- 📝 模型卡片 - 自动生成文档
- ⚙️ 生产级集成 - ART, GE, statsmodels状态

---

## 快速开始

### 1. 安装依赖

```bash
pip install streamlit plotly
```

### 2. 启动仪表板

```bash
# 从项目根目录
streamlit run aeva/dashboard/app.py

# 或使用自定义端口
streamlit run aeva/dashboard/app.py --server.port=8502
```

### 3. 访问

打开浏览器访问: http://localhost:8501

---

## 使用Docker运行

### 使用Docker命令

```bash
# 构建镜像
docker build -t aeva:latest .

# 运行仪表板
docker run -p 8501:8501 aeva:latest dashboard
```

### 使用Docker Compose

```bash
# 启动仪表板
docker-compose up aeva-dashboard

# 后台运行
docker-compose up -d aeva-dashboard
```

访问: http://localhost:8501

---

## 页面功能

### 🏠 主页

**功能**:
- 系统概览（模块数、测试覆盖率等）
- 核心功能介绍
- 快速操作按钮
- 系统状态检查
- 文档导航

**亮点**:
- 实时检查生产库状态
- 一键导航到各功能模块

---

### 🔍 可解释性分析

**功能**:
- **SHAP分析**: 运行SHAP解释器，获取top特征
- **LIME分析**: 运行LIME解释器，局部可解释
- **特征重要性**: 计算并可视化特征重要性
- **代码示例**: 完整使用代码

**交互特性**:
- ✅ 一键运行演示
- ✅ 实时结果展示
- ✅ 可视化图表
- ✅ 可复制代码

**示例流程**:
1. 点击"运行SHAP演示"
2. 查看预测结果和Top特征
3. 分析特征值
4. 理解模型决策

---

### 🛡️ 对抗鲁棒性

**功能**:
- **FGSM攻击**: 快速梯度攻击演示
- **PGD攻击**: 投影梯度下降攻击
- **综合测试**: 多种攻击方法评估
- **代码示例**: 攻击代码模板

**演示内容**:
- 原始预测 vs 对抗预测
- 攻击成功率
- 扰动大小
- 鲁棒性评分

---

### 📊 数据质量

**功能**:
- **数据画像**: 自动分析数据集
- **质量指标**: 完整性、唯一性等
- **期望验证**: Great Expectations集成
- **代码示例**: 数据质量检查代码

**指标展示**:
- 行数、列数
- 缺失值统计
- 重复行检测
- 综合质量分

---

### 📈 A/B测试

**功能**:
- **模型对比**: 交互式参数设置
- **统计检验**: 多种检验方法
- **功效分析**: 样本量计算
- **代码示例**: A/B测试代码

**交互特性**:
- 可调节样本量和准确率
- 实时计算p值和效应量
- 显著性判断
- 样本量估算

---

### 📝 模型卡片

**功能**:
- **生成卡片**: 表单式输入生成
- **验证卡片**: 上传JSON验证
- **模板参考**: 标准字段说明
- **代码示例**: 卡片生成代码

**生成流程**:
1. 填写基本信息（名称、版本、类型）
2. 输入性能指标（准确率、精确率、召回率）
3. 描述用途与限制
4. 点击生成
5. 下载JSON文件

---

### ⚙️ 生产级集成

**功能**:
- **库状态检查**: 实时检测安装状态
- **ART集成**: 功能和使用说明
- **GE集成**: 期望类型介绍
- **statsmodels集成**: 高级统计功能
- **安装指南**: 完整安装命令
- **代码示例**: 集成使用代码

**状态显示**:
- ✅ 已安装 - 显示可用功能
- ⚠️ 未安装 - 提供安装命令
- 功能对比（基础版 vs 生产版）

---

## 自定义配置

### 端口配置

```bash
# 使用8502端口
streamlit run aeva/dashboard/app.py --server.port=8502

# 绑定所有地址（Docker）
streamlit run aeva/dashboard/app.py --server.address=0.0.0.0
```

### 主题配置

创建 `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
```

### 缓存配置

仪表板使用Streamlit缓存优化性能:

```python
@st.cache_data
def load_data():
    # 数据加载逻辑
    pass

@st.cache_resource
def load_model():
    # 模型加载逻辑
    pass
```

---

## 性能优化

### 1. 数据缓存

```python
@st.cache_data(ttl=3600)
def expensive_computation():
    # 缓存1小时
    pass
```

### 2. 分页显示

```python
# 大数据集分页
page_size = 100
page = st.slider("页码", 1, total_pages)
start_idx = (page - 1) * page_size
end_idx = start_idx + page_size
st.dataframe(df.iloc[start_idx:end_idx])
```

### 3. 异步加载

```python
with st.spinner("正在加载..."):
    data = load_large_dataset()
```

---

## 故障排除

### 问题1: 端口被占用

**症状**: `Address already in use`

**解决**:
```bash
# 查找占用进程
lsof -i :8501

# 使用其他端口
streamlit run aeva/dashboard/app.py --server.port=8502
```

### 问题2: 模块导入失败

**症状**: `ModuleNotFoundError: No module named 'aeva'`

**解决**:
```bash
# 确保在项目根目录
cd /path/to/AVEA-P

# 设置PYTHONPATH
export PYTHONPATH=$(pwd)

# 或安装AEVA
pip install -e .
```

### 问题3: 演示运行失败

**症状**: 点击演示按钮报错

**检查**:
1. 确认依赖已安装（scikit-learn, shap, lime）
2. 查看错误详情
3. 检查数据可用性

### 问题4: 页面加载慢

**原因**: 首次运行需要初始化

**优化**:
- 使用缓存
- 减少同时展示的数据量
- 使用分页

---

## 部署到生产

### 本地部署

```bash
streamlit run aeva/dashboard/app.py \
    --server.port=8501 \
    --server.address=0.0.0.0
```

### Docker部署

```bash
docker run -d \
    -p 8501:8501 \
    --name aeva-dashboard \
    aeva:latest \
    dashboard
```

### Kubernetes部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aeva-dashboard
spec:
  replicas: 2
  selector:
    matchLabels:
      app: aeva-dashboard
  template:
    metadata:
      labels:
        app: aeva-dashboard
    spec:
      containers:
      - name: dashboard
        image: aeva:latest
        command: ["streamlit", "run", "aeva/dashboard/app.py"]
        ports:
        - containerPort: 8501
---
apiVersion: v1
kind: Service
metadata:
  name: aeva-dashboard-service
spec:
  selector:
    app: aeva-dashboard
  ports:
  - port: 80
    targetPort: 8501
  type: LoadBalancer
```

### 云平台部署

#### Streamlit Cloud

1. 推送代码到GitHub
2. 访问 https://streamlit.io/cloud
3. 连接仓库
4. 选择 `aeva/dashboard/app.py`
5. 部署

#### Heroku

```bash
# 创建Procfile
echo "web: streamlit run aeva/dashboard/app.py --server.port=\$PORT" > Procfile

# 部署
heroku create aeva-dashboard
git push heroku main
```

---

## 安全建议

### 1. 认证

```python
# 使用streamlit-authenticator
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    credentials,
    "aeva_dashboard",
    "secret_key",
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # 显示仪表板
    pass
elif authentication_status == False:
    st.error('用户名或密码错误')
```

### 2. HTTPS

```bash
streamlit run aeva/dashboard/app.py \
    --server.sslCertFile=cert.pem \
    --server.sslKeyFile=key.pem
```

### 3. 访问控制

```python
# IP白名单
allowed_ips = ['192.168.1.0/24']

# 检查IP
if not is_ip_allowed(get_client_ip()):
    st.error("访问被拒绝")
    st.stop()
```

---

## 扩展开发

### 添加新页面

1. 创建页面文件:

```python
# aeva/dashboard/pages/my_page.py
import streamlit as st

def render():
    st.title("My Custom Page")
    # 页面逻辑
```

2. 注册页面:

```python
# aeva/dashboard/app.py
from aeva.dashboard.pages import my_page

# 添加到导航
page = st.sidebar.radio(
    "导航",
    [..., "📌 My Page"]
)

# 添加路由
if page == "📌 My Page":
    my_page.render()
```

### 自定义组件

```python
import streamlit.components.v1 as components

# HTML组件
components.html("<h1>Custom HTML</h1>")

# React组件
my_component = components.declare_component(
    "my_component",
    path="frontend/build"
)
```

---

## 最佳实践

### 1. 代码组织

```
aeva/dashboard/
├── app.py              # 主应用
├── pages/              # 页面模块
│   ├── __init__.py
│   ├── home.py
│   └── ...
├── components/         # 可复用组件
│   ├── charts.py
│   └── metrics.py
└── utils/              # 工具函数
    └── helpers.py
```

### 2. 状态管理

```python
# 使用session_state
if 'model' not in st.session_state:
    st.session_state.model = load_model()

# 使用缓存
@st.cache_resource
def load_model():
    return train_model()
```

### 3. 用户体验

- ✅ 使用进度条（`st.spinner`, `st.progress`）
- ✅ 提供清晰的错误信息
- ✅ 添加帮助提示（`st.info`, `st.help`）
- ✅ 使用列布局美化界面
- ✅ 添加下载按钮导出结果

---

## 总结

### 仪表板特性

- ✅ 7个功能页面
- ✅ 完整交互演示
- ✅ 实时状态检测
- ✅ 代码示例
- ✅ 响应式设计
- ✅ Docker支持
- ✅ 生产就绪

### 快速命令

```bash
# 本地运行
streamlit run aeva/dashboard/app.py

# Docker运行
docker-compose up aeva-dashboard

# 自定义端口
streamlit run aeva/dashboard/app.py --server.port=8502
```

---

**项目**: AEVA v2.0
**文档**: 仪表板使用指南
**状态**: ✅ 完整
**更新**: 2026-04-12
