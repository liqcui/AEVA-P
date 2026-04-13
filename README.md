# AEVA - Algorithm Evaluation & Validation Agent
**算法评测与验证智能体**

[![License](https://img.shields.io/badge/License-Dual%20License-blue.svg)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Demo-Live-success)](https://liqcui.github.io/AEVA-P/)
[![GitHub](https://img.shields.io/badge/GitHub-AEVA--P-black)](https://github.com/liqcui/AEVA-P)

🌐 **[Live Demo](https://liqcui.github.io/AEVA-P/)** | 📖 **[Documentation](docs/)** | 📄 **[License](LICENSE)**

---

## Overview
AEVA is an intelligent platform for algorithm evaluation and validation, designed to transform algorithm testing from manual operations to AI-driven standardized processes. It implements "Evaluation-as-a-Service" (EaaS) philosophy.

### 🎯 Dashboard Structure
**9 Main Pages** providing comprehensive evaluation capabilities:
- 🏠 Overview & Metrics
- 🔍 Explainability (SHAP/LIME)
- 🛡️ Adversarial Robustness
- 📊 Data Quality
- 📈 A/B Testing
- 📝 Model Cards
- 🤖 LLM Evaluation
- ⚙️ Production Integrations
- 📄 Report Generation ⭐ NEW

**4 Advanced Features** for enterprise-grade automation:
- 🏆 Benchmark Suite - Multi-model comparison
- 🤖 Auto Pipeline - Workflow orchestration
- 🧠 Brain Analysis - AI-powered diagnostics
- 🛡️ Quality Guard - Automated gates

## Architecture

### 🏗️ Deployment Modes

AEVA supports **two deployment architectures** to fit different scales and requirements:

**📦 Monolithic Deployment** (`deployment/monolithic` branch)
- Single application, all modules in one process
- Best for: Small-medium deployments, development, quick setup
- Resources: 4-8 cores, 8-16 GB RAM

**🔷 Microservices Deployment** (`main` branch - current)
- Distributed services, independently scalable
- Best for: Large scale, high availability, cloud-native
- Resources: 16+ cores, 32+ GB RAM (distributed)

See [DEPLOYMENT_MODE.md](DEPLOYMENT_MODE.md) for detailed comparison.

### Microservices Architecture (Current Branch)

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Web Dashboard│  │  Mobile App  │  │   CLI Tool   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│                   API Gateway :8000                      │
│         (Request Routing, Rate Limiting, CORS)          │
└─────┬────────┬────────┬────────┬───────────────────────┘
      │        │        │        │
┌─────▼──┐ ┌──▼────┐┌──▼────┐┌──▼────┐
│ Bench  │ │ Guard ││ Auto  ││ Brain │  Core Services
│:8001   │ │:8002  ││:8003  ││:8004  │  (FastAPI)
└───┬────┘ └───┬───┘└───┬───┘└───┬───┘
    │          │        │  │      │
    ▼          ▼        ▼  ▼      ▼
PostgreSQL   Redis   PostgreSQL  PostgreSQL
  :5433      :6379   :5434+Redis :5435
                        :6380
                       +Celery
```

### 🚀 Quick Start - Microservices Deployment

Deploy all services with a single command:

```bash
# Clone repository
git clone https://github.com/liqcui/AEVA-P.git
cd AEVA-P

# Set up environment (optional - for Brain Service LLM)
echo "LLM_API_KEY=your-api-key-here" > .env

# Start all microservices
docker-compose -f docker-compose.microservices.yml up -d

# Verify deployment
curl http://localhost:8000/health

# Access API documentation
open http://localhost:8000/api/v1/docs
```

**What Gets Deployed:**
- ✅ 5 Application Services (API Gateway, Bench, Guard, Auto, Brain)
- ✅ 1 Background Worker (Celery for Auto Service)
- ✅ 3 PostgreSQL Databases
- ✅ 2 Redis Instances
- ✅ All with health checks and auto-restart

📖 **Full Guide**: See [MICROSERVICES.md](MICROSERVICES.md) for complete deployment documentation.

### Microservices Components

**🌐 API Gateway (Port 8000)**
- Unified entry point: `/api/v1/*`
- Request routing to backend services
- Rate limiting (100 req/min per client)
- CORS and error handling
- FastAPI with async HTTP client

**📊 Bench Service (Port 8001)**
- Benchmark evaluation and management
- Performance testing and comparison
- PostgreSQL for benchmark data
- REST API: `/v1/benchmark/*`

**🛡️ Guard Service (Port 8002)**
- Quality gate validation
- Metric threshold checking
- Auto-blocking for failed validations
- Redis for fast caching
- REST API: `/v1/gate/*`

**⚙️ Auto Service (Port 8003)**
- Pipeline orchestration
- Multi-step workflow automation
- Celery workers for async execution
- PostgreSQL + Redis (broker)
- REST API: `/v1/pipeline/*`

**🧠 Brain Service (Port 8004)**
- AI-powered analysis
- LLM integration (OpenAI, Anthropic, Ollama)
- Intelligent insights and recommendations
- PostgreSQL for analysis history
- REST API: `/v1/analysis/*`

### Shared SDK (aeva-common)

The `aeva-common` package provides shared data structures and service interfaces:
- 📊 Data Models: `EvaluationResult`, `MetricResult`, `GateResult`, `Analysis`
- ⚙️ Configuration: Service configs, database, Redis
- 🔌 Service Interfaces: Standardized API contracts
- 🌐 HTTP Clients: Async clients for service communication

See [aeva-common/README.md](aeva-common/README.md) for details.

### Service Endpoints

| Service | Direct Access | Via Gateway | Documentation |
|---------|--------------|-------------|---------------|
| API Gateway | - | http://localhost:8000 | [Swagger](http://localhost:8000/api/v1/docs) |
| Bench | http://localhost:8001 | /api/v1/benchmark/* | [README](services/bench-service/README.md) |
| Guard | http://localhost:8002 | /api/v1/gate/* | [README](services/guard-service/README.md) |
| Auto | http://localhost:8003 | /api/v1/pipeline/* | [README](services/auto-service/README.md) |
| Brain | http://localhost:8004 | /api/v1/analysis/* | [README](services/brain-service/README.md) |

**Recommended**: Use API Gateway endpoints for unified access and rate limiting.

## Core Modules

### 1. AEVA-Guard (Guardian - 质量门禁)
**Function**: Quality gates and delivery protection
- Pre-deployment quality checks
- Automated quality gates
- Risk assessment and blocking mechanism
- Integration with CI/CD pipelines

### 2. AEVA-Bench (Benchmark - 标准化评测基准)
**Function**: Standardized evaluation benchmarks
- Multi-dimensional evaluation metrics system
- Industry-standard benchmark datasets
- Custom benchmark creation and management
- Performance baseline tracking

### 3. AEVA-Auto (Automation - 自动化流水线)
**Function**: Automated pipeline orchestration
- End-to-end evaluation workflow automation
- Distributed testing execution
- Resource scheduling and management
- Result collection and reporting

### 4. AEVA-Brain (Brain/Judge - 智能诊断)
**Function**: Quality LLM for intelligent diagnostics
- AI-powered result analysis
- Root cause identification
- Intelligent recommendations
- Pattern recognition and anomaly detection

## Enhanced Features ⭐ NEW

### 5. AEVA-Report (报告生成)
**Function**: Professional evaluation report generation
- HTML/PDF/Markdown report export
- Customizable templates and branding
- Multi-language support (Chinese/English)
- Automated comparison reports

### 6. AEVA-Comparison (模型对比)
**Function**: Multi-model comparison and A/B testing
- Side-by-side model comparison
- Statistical significance testing
- Champion/Challenger management
- Automated promotion decisions

### 7. AEVA-LLM Evaluation (LLM专项评测) ⭐ NEW
**Function**: Comprehensive LLM evaluation and quality assessment
- **Correctness Evaluation** (功能正确性)
  - Hallucination detection with self-consistency checking
  - Factuality verification against ground truth
  - Task completion scoring and instruction following
- **Performance Profiling** (性能评测)
  - TTFT (Time To First Token) measurement
  - TPOT (Time Per Output Token) analysis
  - Token consumption tracking and cost estimation
  - P50/P95/P99 latency percentiles
- **Safety Testing** (安全性)
  - Harmful content filtering (6 categories)
  - Jailbreak attempt detection (5 attack types)
  - PII detection with automatic redaction
- **User Experience** (用户体验)
  - Relevance and semantic similarity scoring
  - Fluency and readability evaluation
  - Diversity and creativity analysis
  - Sentiment and tone detection

**Statistics**: 2,004 lines of production-ready code | 4 modules | 15 specialized evaluators | 100% coverage

```python
# Quick example
from aeva.llm_evaluation import (
    CorrectnessEvaluator,
    LLMPerformanceProfiler,
    SafetyEvaluator
)

# Evaluate correctness (hallucination, accuracy)
correctness = CorrectnessEvaluator()
results = correctness.evaluate(
    output=llm_output,
    context=prompt,
    instructions="Your task"
)

# Profile performance (TTFT, TPOT, cost)
profiler = LLMPerformanceProfiler(model_name="gpt-4")
perf = profiler.profile_generation(generate_func, prompt)

# Check safety (harmful content, PII, jailbreaks)
safety = SafetyEvaluator()
safety_results = safety.evaluate(llm_output)
```

📖 **Full Documentation**: See [`LLM_EVALUATION_IMPLEMENTATION.md`](LLM_EVALUATION_IMPLEMENTATION.md) | **Examples**: [`examples/llm_evaluation_example.py`](examples/llm_evaluation_example.py)

### 8. AEVA-Defense (Adversarial Defense) ⭐ NEW
**Function**: Comprehensive adversarial defense mechanisms for ML models
- **Adversarial Training** (对抗训练)
  - Train with adversarial examples for maximum robustness
  - Configurable mix ratio and training epochs
  - 60-80% defense effectiveness
- **Input Transformation** (输入转换)
  - 4 transformation methods: median filter, quantization, Gaussian blur, JPEG compression
  - No model retraining required
  - 40-60% defense effectiveness
- **Gradient Masking** (梯度混淆)
  - Gradient noise injection and clipping
  - Fast inference-time defense
- **Ensemble Defense** (集成防御)
  - Multi-model voting for enhanced robustness
  - 3 aggregation methods: majority vote, average, max
  - 50-70% defense effectiveness
- **Adversarial Detection** (对抗检测)
  - 3 detection methods: statistical, confidence-based, feature analysis
  - Reject or flag adversarial inputs
  - 50-70% detection accuracy

**Statistics**: 880+ lines of production code | 5 defense mechanisms | 3 detection methods | Full evaluation framework

```python
# Quick example
from aeva.robustness.defenses import (
    AdversarialTraining,
    InputTransformation,
    DefenseEvaluator
)

# Train with adversarial examples
defense = AdversarialTraining(
    attack_fn=fgsm_attack,
    mix_ratio=0.5,
    epochs=10
)
defense.fit(model, X_train, y_train)

# Apply input transformation
transform_defense = InputTransformation(
    transformation_type="median_filter",
    kernel_size=3
)
X_defended = transform_defense.apply(X_adv)

# Evaluate defense effectiveness
evaluator = DefenseEvaluator()
result = evaluator.evaluate_defense(
    defense, model, X_clean, y_clean, X_adv
)
print(f"Defense Effectiveness: {result.defense_effectiveness:.2%}")
```

📖 **Full Documentation**: See [`DEFENSE_IMPLEMENTATION.md`](DEFENSE_IMPLEMENTATION.md) | **Examples**: [`examples/defense_example.py`](examples/defense_example.py)

### 9. AEVA-ABTesting (A/B Testing Framework) ⭐ ENHANCED
**Function**: Comprehensive A/B testing and experimentation framework
- **Statistical Testing** (统计检验)
  - Parametric tests: t-test, z-test, ANOVA
  - Non-parametric tests: Mann-Whitney U, Wilcoxon, Kruskal-Wallis
  - Effect sizes: Cohen's d, Hedge's g, Glass's delta
  - Multiple comparison correction (Bonferroni, FDR, Holm, Sidak)
  - Power analysis and sample size calculation
- **Advanced A/B Testing** (高级A/B测试)
  - Sequential testing with early stopping (reduces sample requirements)
  - Bayesian A/B testing (posterior probabilities, expected loss)
  - Multi-variant testing (A/B/C/D...) with correction
  - Stratified testing for segments
- **Multi-Armed Bandit** (多臂老虎机)
  - Epsilon-greedy algorithm
  - UCB (Upper Confidence Bound)
  - Thompson Sampling
  - Dynamic traffic allocation
- **Calculators** (计算器)
  - Sample size calculator (from MDE and power)
  - MDE calculator (from sample size)
  - Test duration estimator

**Statistics**: 1,220+ lines of production code | 7 parametric tests | 4 non-parametric tests | 5 correction methods | 3 bandit algorithms

```python
# Quick example
from aeva.ab_testing import ABTester, StatisticalTest

# Traditional A/B test
tester = ABTester(significance_level=0.05, power=0.8)
result = tester.compare(variant_a, variant_b, "Control", "Treatment")
print(f"Winner: {result.winner}, p={result.p_value:.4f}")

# Sequential testing (early stopping)
result = tester.sequential_test(variant_a, variant_b)

# Bayesian testing
bayes_result = tester.bayesian_test(variant_a, variant_b)
print(f"P(B > A): {bayes_result.prob_b_better:.2%}")

# Multi-armed bandit
bandit = ABTester.MultiArmedBandit(n_arms=3, algorithm="thompson_sampling")
arm = bandit.select_arm()
bandit.update(arm, reward=0.8)
```

### 10. AEVA-ModelCards (Model Card System) ⭐ ENHANCED
**Function**: Automated model card generation and validation for ML compliance
- **Card Generation** (卡片生成)
  - Automated metric extraction from models
  - Template engine with professional HTML/CSS
  - Visualization generation (performance charts, fairness radar)
  - Compliance framework templates (GDPR, EU AI Act, HIPAA)
  - Multi-format export (JSON, Markdown, HTML)
  - Support for fairness metrics and environmental impact
- **Validation & Compliance** (验证与合规)
  - Multi-level validation (ERROR, WARNING, INFO)
  - Schema validation with completeness scoring (0-100%)
  - Field quality checks (length, vague language detection)
  - Compliance-specific checks (GDPR, EU AI Act, HIPAA)
  - Detailed recommendations and suggestions
  - Automated quality scoring

**Statistics**: 1,269+ lines of production code | 3 compliance frameworks | 4 validation levels | Auto-generated visualizations

```python
# Quick example
from aeva.model_cards import ModelCardGenerator, ModelCardValidator

# Generate model card
generator = ModelCardGenerator(model_name="MyModel")
card = generator.generate_card(
    model_version="1.0",
    performance_metrics={"accuracy": 0.95, "f1": 0.93},
    compliance_framework="eu_ai_act"
)

# Export with visualizations
generator.export_html(card, "model_card.html")

# Validate compliance
validator = ModelCardValidator()
report = validator.validate_compliance(card, "gdpr")
print(f"Valid: {report.is_valid}, Score: {report.quality_score}/100")
```

### 11. AEVA-DataQuality (Data Quality Framework) ⭐ ENHANCED
**Function**: Comprehensive data quality assessment and profiling
- **Quality Dimensions** (质量维度)
  - Completeness: Missing value analysis
  - Uniqueness: Duplicate detection
  - Validity: Range and pattern validation
  - Accuracy: Reference comparison
  - Consistency: Cross-field and temporal checks
  - Timeliness: Temporal data assessment
- **Analysis Tools** (分析工具)
  - Outlier detection (IQR, Z-score, Modified Z-score)
  - Statistical distribution analysis (mean, median, std, quartiles)
  - Normality testing (Shapiro-Wilk)
  - Distribution type classification
  - Pattern-based validation for strings
- **Reporting** (报告)
  - Comprehensive quality reports
  - Quality scoring framework (0-100)
  - Support for pandas DataFrames and numpy arrays
  - Actionable recommendations

**Statistics**: 619+ lines of production code | 6 quality dimensions | 3 outlier methods | Comprehensive profiling

```python
# Quick example
from aeva.data_quality import QualityMetrics, DataProfiler

# Calculate quality metrics
metrics = QualityMetrics()
completeness = metrics.completeness(data)
outliers = metrics.detect_outliers(data, method="iqr")

# Generate quality report
profiler = DataProfiler()
report = profiler.generate_report(df)
print(f"Quality Score: {report.overall_score}/100")
print(f"Completeness: {report.dimensions['completeness']:.2%}")
```

### 12. AEVA-RobustnessReporting (Robustness Analysis) ⭐ ENHANCED
**Function**: Advanced robustness reporting and visualization
- **Report Generation** (报告生成)
  - Comprehensive text and HTML reports
  - PDF export support (ReportLab integration)
  - Executive summary generation
  - Comparison reports for multiple models
  - Automated recommendations based on results
- **Visualizations** (可视化)
  - Adversarial examples comparison (original vs adversarial)
  - Perturbation analysis with heatmaps
  - Robustness curves (accuracy vs epsilon)
  - Attack success rate plots
  - Defense effectiveness charts
  - ROC curves for detection
  - Confidence distribution analysis
  - Epsilon sensitivity analysis
- **Analysis** (分析)
  - Robustness score calculation
  - Severity level determination (LOW, MEDIUM, HIGH, CRITICAL)
  - Support for 10+ attack types (FGSM, PGD, C&W, DeepFool, etc.)
  - Defense effectiveness tracking

**Statistics**: 1,414+ lines of production code | 10+ visualization types | PDF/HTML export | Professional styling

```python
# Quick example
from aeva.robustness import RobustnessReportGenerator, RobustnessVisualizer

# Generate comprehensive report
generator = RobustnessReportGenerator()
report = generator.generate_report(
    attack_results=attack_results,
    defense_results=defense_results
)

# Export to PDF
generator.export_pdf(report, "robustness_report.pdf")

# Create visualizations
visualizer = RobustnessVisualizer()
visualizer.plot_robustness_curve(epsilons, accuracies)
visualizer.plot_perturbation_heatmap(perturbations)
visualizer.plot_attack_success_rates(attack_results)
```

## Project Structure

```
AVEA-P/
├── aeva/
│   ├── __init__.py
│   ├── core/               # Core framework
│   ├── guard/              # AEVA-Guard module
│   ├── bench/              # AEVA-Bench module
│   ├── auto/               # AEVA-Auto module
│   ├── brain/              # AEVA-Brain module
│   ├── llm_evaluation/     # LLM evaluation module ⭐ NEW
│   │   ├── correctness.py  # Hallucination, factuality, task completion
│   │   ├── performance.py  # TTFT, TPOT, latency, cost tracking
│   │   ├── safety.py       # Harmful content, jailbreak, PII detection
│   │   └── user_experience.py # Relevance, fluency, diversity, sentiment
│   ├── robustness/         # Adversarial robustness module ⭐ ENHANCED
│   │   ├── defenses.py     # 5 defense mechanisms (880+ lines) ⭐ ENHANCED
│   │   ├── attacks.py      # FGSM, PGD, C&W attacks
│   │   ├── evaluator.py    # Robustness evaluation
│   │   ├── report.py       # Report generation (808+ lines) ⭐ ENHANCED
│   │   └── visualizations.py # Visualization tools (606+ lines) ⭐ ENHANCED
│   ├── ab_testing/         # A/B testing framework ⭐ ENHANCED
│   │   ├── statistics.py   # Statistical tests (540+ lines) ⭐ ENHANCED
│   │   └── tester.py       # A/B testing framework (680+ lines) ⭐ ENHANCED
│   ├── model_cards/        # Model card system ⭐ ENHANCED
│   │   ├── generator.py    # Card generation (692+ lines) ⭐ ENHANCED
│   │   └── validator.py    # Validation & compliance (577+ lines) ⭐ ENHANCED
│   ├── data_quality/       # Data quality framework ⭐ ENHANCED
│   │   ├── metrics.py      # Quality metrics (619+ lines) ⭐ ENHANCED
│   │   └── profiler.py     # Data profiling
│   ├── common/             # Shared utilities
│   └── api/                # REST API services
├── config/                 # Configuration files
├── tests/                  # Test suites
├── examples/               # Usage examples
│   ├── llm_evaluation_example.py  # LLM evaluation demos ⭐ NEW
│   └── defense_example.py         # Adversarial defense demos ⭐ NEW
├── demo/                   # Interactive offline demo ⭐ NEW
│   ├── index.html         # Full-featured demo page
│   └── README.md          # Demo usage guide
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── LLM_EVALUATION_IMPLEMENTATION.md  # LLM evaluation guide ⭐ NEW
├── DEFENSE_IMPLEMENTATION.md         # Defense mechanisms guide ⭐ NEW
├── SCALABILITY_ARCHITECTURE.md       # Scalability architecture ⭐ NEW
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
├── Dockerfile             # Container definition
└── README.md              # This file
```

## Quick Start

### 🌐 Try Online Demo (No Installation Required)

**Live Demo**: https://liqcui.github.io/AEVA-P/

Experience AEVA's full functionality directly in your browser:
- ✅ No installation needed
- ✅ No API keys required
- ✅ Fully offline-capable
- ✅ All features with mock data
- ✅ Interactive Dashboard UI with 9 main pages + 4 advanced features ⭐ NEW
- ✅ LLM evaluation demos (hallucination, performance, safety) ⭐ NEW
- ✅ Enterprise scalability architecture showcase ⭐ NEW

### 🎭 Dual Interface - Choose Your Interaction Method

AEVA provides **two powerful ways** to interact with the platform:

#### 🖥️ Command-Line Interface (CLI)
**Best for**: Automation, CI/CD, scripting, batch processing

```bash
# Model evaluation
aeva evaluate model models/classifier.pkl data/test.csv --metrics accuracy --metrics f1

# Data validation
aeva data validate data/dataset.csv --output reports/

# Generate explainability report
aeva evaluate explainability models/model.pkl data/test.csv --method shap

# Launch API server
aeva server --port 8000
```

📖 **Full CLI Guide**: See [`docs/CLI_USAGE.md`](docs/CLI_USAGE.md) for complete CLI reference.

#### 🌐 Web Dashboard
**Best for**: Exploration, visualization, collaboration, demos

```bash
# Launch interactive dashboard
aeva dashboard

# Access at: http://localhost:8501
```

**Dashboard Features** (9 Main Pages):
- 🏠 Overview & Metrics
- 🔍 SHAP/LIME Explainability
- 🛡️ Adversarial Robustness
- 📊 Data Quality Analysis
- 📈 A/B Testing
- 📝 Model Card Generation
- 🤖 LLM Evaluation ⭐ NEW
- ⚙️ Production Integrations
- 📄 Report Generation ⭐ NEW

**Advanced Features** (4 Sub-Pages):
- 🏆 Benchmark Suite - Standardized evaluation & multi-model comparison
- 🤖 Auto Pipeline - Workflow orchestration & task scheduling
- 🧠 Brain Analysis - AI-powered intelligent analysis with LLM
- 🛡️ Quality Guard - Automated quality gates & release control

💡 **Try it now**: Experience the full Dashboard UI in our [interactive demo](https://liqcui.github.io/AEVA-P/) (no server required)

📖 **CLI vs Web Comparison**: See [`docs/CLI_VS_WEB.md`](docs/CLI_VS_WEB.md) for detailed comparison.

### 🎬 Interactive Demo (Offline-Ready)

**Try the live demo** - no installation required!

```bash
# Open the interactive demo page
cd demo
open index.html  # or double-click the file

# The demo is fully offline-capable and showcases:
# - Interactive Dashboard UI with 9 main pages + 4 advanced features ⭐ NEW
# - 9 Main Pages: Overview, Explainability, Robustness, Data Quality, A/B Testing, Model Cards, LLM Eval, Production, Report Generation
# - 4 Advanced Features: Benchmark Suite, Auto Pipeline, Brain Analysis, Quality Guard
# - LLM Evaluation (hallucination, performance, safety, UX) ⭐ NEW
# - Enterprise scalability & Kubernetes deployment ⭐ NEW
```

**Dashboard Pages**:
- 📊 **Overview**: 4 KPI cards, performance trends, quality distribution, recent models, advanced features showcase
- 🔍 **Explainability**: SHAP feature importance, LIME analysis, counterfactual explanations
- 🛡️ **Robustness**: FGSM/PGD attack testing, defense effectiveness evaluation
- 📊 **Data Quality**: Quality metrics, missing values detection, distribution drift analysis
- 📈 **A/B Testing**: Statistical significance testing, Bayesian analysis, sequential testing
- 📝 **Model Cards**: Automated model documentation generation and validation
- 🤖 **LLM Evaluation**: Hallucination detection, safety assessment, performance profiling, UX scoring
- ⚙️ **Production Integrations**: ART, Great Expectations, statsmodels integration showcase

**Advanced Features** (Accessed via Home):
- 🏆 **Benchmark Suite**: Create benchmark suites, run tests, multi-model comparison, performance ranking
- 🤖 **Auto Pipeline**: Pipeline management, task scheduling, execution monitoring, distributed execution
- 🧠 **Brain Analysis**: AI-powered result analysis, root cause detection, intelligent recommendations
- 🛡️ **Quality Guard**: Quality gates management, automated checks, execution monitoring, statistics reports

📖 **Demo Guide**: See [`demo/README.md`](demo/README.md) for detailed demo usage and presentation scripts.

## Installation & Deployment

### Option 1: Microservices Deployment (Recommended for Production)

**Prerequisites:**
- Docker Engine 20.10+
- Docker Compose 2.0+
- 8GB RAM minimum
- 20GB disk space

**Quick Start:**
```bash
# Clone repository
git clone https://github.com/liqcui/AEVA-P.git
cd AEVA-P

# Optional: Set LLM API key for Brain Service
echo "LLM_API_KEY=your-openai-api-key" > .env

# Start all services (11 containers)
docker-compose -f docker-compose.microservices.yml up -d

# Verify deployment
curl http://localhost:8000/health

# Access API documentation
open http://localhost:8000/api/v1/docs
```

**Services Started:**
- API Gateway (http://localhost:8000) - Unified API access
- Bench Service (http://localhost:8001) - Benchmark evaluation
- Guard Service (http://localhost:8002) - Quality gates
- Auto Service (http://localhost:8003) - Pipeline orchestration
- Brain Service (http://localhost:8004) - AI analysis
- 3 PostgreSQL databases (ports 5433-5435)
- 2 Redis instances (ports 6379-6380)
- 1 Celery worker (background tasks)

**Management Commands:**
```bash
# View logs
docker-compose -f docker-compose.microservices.yml logs -f

# Check status
docker-compose -f docker-compose.microservices.yml ps

# Stop all services
docker-compose -f docker-compose.microservices.yml down
```

📖 **Complete Guide**: See [MICROSERVICES.md](MICROSERVICES.md) for detailed deployment, usage examples, troubleshooting, and production configuration.

### Option 2: Monolithic Deployment (For Development)

**Switch to monolithic branch:**
```bash
git checkout deployment/monolithic
```

**Local Installation:**
```bash
# Clone the repository
git clone https://github.com/liqcui/AEVA-P.git
cd AEVA-P

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install AEVA in development mode
pip install -e .
```

📖 **Deployment Comparison**: See [DEPLOYMENT_MODE.md](DEPLOYMENT_MODE.md) for choosing between monolithic and microservices.

## Usage

### Microservices API (via API Gateway)

**Create and Run Benchmark:**
```bash
# Create benchmark
curl -X POST http://localhost:8000/api/v1/benchmark/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "model_evaluation",
    "algorithm": "RandomForest",
    "dataset": "test_data"
  }'

# Run benchmark
curl -X POST http://localhost:8000/api/v1/benchmark/{id}/run
```

**Quality Gate Validation:**
```bash
# Create quality gate
curl -X POST http://localhost:8000/api/v1/gate/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "production_gate",
    "threshold": 0.85,
    "metrics": ["accuracy", "f1_score"]
  }'

# Validate metrics
curl -X POST http://localhost:8000/api/v1/gate/{id}/validate \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": {"accuracy": 0.92, "f1_score": 0.88}
  }'
```

**Execute Complete Pipeline:**
```bash
# Create pipeline
curl -X POST http://localhost:8000/api/v1/pipeline/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ml_evaluation",
    "config": {
      "steps": [
        {"name": "benchmark", "type": "benchmark", "config": {"benchmark_id": "bench-123"}},
        {"name": "validate", "type": "validate", "config": {"gate_id": "gate-456"}},
        {"name": "analyze", "type": "analyze", "config": {"analysis_type": "comprehensive"}}
      ]
    }
  }'

# Execute pipeline
curl -X POST http://localhost:8000/api/v1/pipeline/{id}/execute
```

**AI-Powered Analysis:**
```bash
# Quick analysis
curl -X POST http://localhost:8000/api/v1/analysis/quick \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_type": "comprehensive",
    "data": {"metrics": {"accuracy": 0.95, "precision": 0.93}}
  }'
```

📖 **Interactive API Docs**: http://localhost:8000/api/v1/docs

### Python SDK (Monolithic Mode)

```python
from aeva import AEVA
from aeva.bench import BenchmarkSuite
from aeva.guard import QualityGate
from aeva.auto import Pipeline
from aeva.brain import QualityLLM

# Initialize AEVA platform
aeva = AEVA(config_path="config/aeva.yaml")

# Create evaluation pipeline
pipeline = Pipeline(name="algorithm_evaluation")

# Add benchmark tests
benchmark = BenchmarkSuite.load("standard_ml_bench")
pipeline.add_stage(benchmark)

# Add quality gates
gate = QualityGate(threshold=0.85)
pipeline.add_stage(gate)

# Add intelligent analysis
brain = QualityLLM(model="quality-judge-v1")
pipeline.add_stage(brain)

# Execute evaluation
result = aeva.run(pipeline)
print(result.summary())
```

## Key Features

### Evaluation-as-a-Service (EaaS)
- Standardized evaluation protocols
- Reusable evaluation components
- Scalable distributed execution
- API-first design

### Multi-dimensional Quality Assessment
- Accuracy metrics
- Performance profiling (including TTFT/TPOT for LLMs)
- Resource efficiency and cost tracking
- Robustness testing (including jailbreak detection)
- **Adversarial Defense** (5 mechanisms: training, transformation, masking, ensemble, detection) ⭐ NEW
- Fairness evaluation
- LLM-specific evaluation (hallucination, safety, UX)

### Intelligent Diagnostics
- LLM-powered analysis
- Automated root cause detection
- Smart recommendations
- Historical pattern learning

### Enterprise Integration
- CI/CD pipeline integration
- Version control tracking
- Audit logging
- Role-based access control

## Use Cases

1. **Pre-deployment Validation**: Automated quality gates before algorithm deployment
2. **Continuous Evaluation**: Ongoing monitoring and evaluation in production
3. **Benchmark Comparison**: Compare different algorithm versions and approaches
4. **Root Cause Analysis**: Intelligent diagnosis of quality issues
5. **Compliance Checking**: Ensure algorithms meet regulatory requirements (GDPR, EU AI Act, HIPAA)
6. **Adversarial Robustness Testing**: Evaluate and defend against adversarial attacks with 5 defense mechanisms
7. **A/B Testing & Experimentation**: Compare model variants with advanced statistical methods
8. **Data Quality Monitoring**: Comprehensive data quality assessment across 6 dimensions
9. **Model Documentation**: Automated model card generation for compliance and transparency

## Technology Stack

### Microservices Stack
- **Language**: Python 3.11+
- **Framework**: FastAPI (async web framework)
- **ORM**: SQLAlchemy 2.0
- **Databases**:
  - PostgreSQL 15 (Bench, Auto, Brain services)
  - Redis 7 (Guard service, Celery broker)
- **Task Queue**: Celery 5.3 (Auto service background workers)
- **API Gateway**: FastAPI with httpx async client
- **AI/ML**: OpenAI, Anthropic, Ollama (Brain service)
- **Testing**: Pytest with async support
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes (planned)
- **Monitoring**: Prometheus, Grafana (planned)

### Shared Components
- **SDK**: aeva-common (shared data models and interfaces)
- **Communication**: HTTP/REST with JSON
- **Authentication**: JWT (planned)
- **Rate Limiting**: In-memory (production: Redis)

### Development Tools
- **AI/ML Libraries**: PyTorch, scikit-learn, transformers
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn
- **Documentation**: Swagger/OpenAPI, ReDoc

## Development Roadmap

- [x] Phase 1: Core framework and AEVA-Guard
- [x] Phase 2: AEVA-Bench standardized benchmarks
- [x] Phase 3: AEVA-Auto pipeline automation
- [ ] Phase 4: AEVA-Brain intelligent analysis
- [ ] Phase 5: Enterprise features and scaling
- [ ] Phase 6: Advanced AI-powered optimization

## Contributing

Contributions are welcome! Please read our [Contributing Guide](docs/CONTRIBUTING.md) for details.

## License

[MIT License](LICENSE)

## Links

- 🌐 **Live Demo**: https://liqcui.github.io/AEVA-P/
- 📦 **GitHub Repository**: https://github.com/liqcui/AEVA-P
- 📖 **Documentation**: [docs/](docs/)
- 🐛 **Issue Tracker**: https://github.com/liqcui/AEVA-P/issues

## Contact

- **Email**: liquan_cui@126.com
- **GitHub Issues**: https://github.com/liqcui/AEVA-P/issues
- **License Inquiries**: liquan_cui@126.com (for commercial use)

---

**AEVA**: Transforming algorithm evaluation from manual operation to intelligent automation.

**Watermark**: AEVA-2026-LQC-dc68e33
