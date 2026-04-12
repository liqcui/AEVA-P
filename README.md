# AEVA - Algorithm Evaluation & Validation Agent
**算法评测与验证智能体**

[![License](https://img.shields.io/badge/License-Dual%20License-blue.svg)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Demo-Live-success)](https://liqcui.github.io/AEVA-P/)
[![GitHub](https://img.shields.io/badge/GitHub-AEVA--P-black)](https://github.com/liqcui/AEVA-P)

🌐 **[Live Demo](https://liqcui.github.io/AEVA-P/)** | 📖 **[Documentation](docs/)** | 📄 **[License](LICENSE)**

---

## Overview
AEVA is an intelligent platform for algorithm evaluation and validation, designed to transform algorithm testing from manual operations to AI-driven standardized processes. It implements "Evaluation-as-a-Service" (EaaS) philosophy.

## Architecture

```
┌─────────────────────────────────────────┐
│           AEVA Platform                 │
│  Algorithm Evaluation & Validation Agent│
├─────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │ AEVA-   │ │ AEVA-   │ │ AEVA-   │   │
│  │ Guard   │ │ Bench   │ │ Auto    │   │
│  │ 质量门禁 │ │ 标准基准 │ │ 自动化  │   │
│  └────┬────┘ └────┬────┘ └────┬────┘   │
│       └─────────────┼───────────┘       │
│                     ▼                   │
│              ┌─────────┐                │
│              │ AEVA-   │                │
│              │ Brain   │                │
│              │ 智能诊断 │                │
│              │ (Quality│                │
│              │  LLM)   │                │
│              └─────────┘                │
└─────────────────────────────────────────┘
```

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
│   ├── common/             # Shared utilities
│   └── api/                # REST API services
├── config/                 # Configuration files
├── tests/                  # Test suites
├── examples/               # Usage examples
│   └── llm_evaluation_example.py  # LLM evaluation demos ⭐ NEW
├── demo/                   # Interactive offline demo ⭐ NEW
│   ├── index.html         # Full-featured demo page
│   └── README.md          # Demo usage guide
├── docs/                   # Documentation
├── scripts/                # Utility scripts
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
- ✅ 8 interactive pages

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

**Dashboard Features**:
- 🏠 Overview & Metrics
- 🔍 SHAP/LIME Explainability
- 🛡️ Adversarial Robustness
- 📊 Data Quality Analysis
- 📈 A/B Testing & Deployment
- 📝 Model Card Generation
- ⚙️ Production Integrations

📖 **CLI vs Web Comparison**: See [`docs/CLI_VS_WEB.md`](docs/CLI_VS_WEB.md) for detailed comparison.

### 🎬 Interactive Demo (Offline-Ready)

**Try the live demo** - no installation required!

```bash
# Open the interactive demo page
cd demo
open index.html  # or double-click the file

# The demo is fully offline-capable and showcases:
# - Dashboard with key metrics
# - Guard quality gates
# - Bench standardized benchmarks
# - Auto pipeline visualization
# - Brain intelligent analysis (core innovation)
```

📖 **Demo Guide**: See [`demo/README.md`](demo/README.md) for detailed demo usage and presentation scripts.

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd AVEA-P

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install AEVA in development mode
pip install -e .
```

### Basic Usage

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
5. **Compliance Checking**: Ensure algorithms meet regulatory requirements

## Technology Stack

- **Language**: Python 3.8+
- **Framework**: FastAPI, SQLAlchemy
- **AI/ML**: PyTorch, scikit-learn, transformers
- **Database**: PostgreSQL, Redis
- **Message Queue**: RabbitMQ/Kafka
- **Monitoring**: Prometheus, Grafana
- **Containerization**: Docker, Kubernetes

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
