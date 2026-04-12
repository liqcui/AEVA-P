# AEVA CLI Usage Guide

**Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.**
**Dual License**: Free for Personal/Academic, Commercial Requires Permission
**Watermark**: AEVA-2026-LQC-dc68e33
**GitHub**: https://github.com/liqcui/AEVA-P

---

## Overview

AEVA provides both CLI and Web interfaces for algorithm evaluation:

- **CLI** - Command-line interface for automation and scripting
- **Web** - Interactive Streamlit dashboard for visual exploration

---

## Installation

```bash
# Install from source
pip install -e .

# Or install with dependencies
pip install -e .[dev]
```

---

## CLI Commands

### 1. Model Evaluation

#### Evaluate a Model

```bash
aeva evaluate model MODEL_PATH DATA_PATH \
  --output results/ \
  --metrics accuracy --metrics f1 \
  --format json
```

**Options**:
- `--output`, `-o` - Output directory
- `--metrics`, `-m` - Metrics to compute (can specify multiple)
- `--format` - Output format: `json`, `html`, `markdown`

**Example**:
```bash
aeva evaluate model models/classifier.pkl data/test.csv \
  --metrics accuracy --metrics f1 --metrics precision \
  --format html \
  --output reports/
```

#### Generate Explainability Report

```bash
aeva evaluate explainability MODEL_PATH DATA_PATH \
  --method shap \
  --samples 100 \
  --output explanations/
```

**Options**:
- `--method` - Explanation method: `shap`, `lime`
- `--samples` - Number of samples to explain
- `--output`, `-o` - Output directory

#### Evaluate Fairness

```bash
aeva evaluate fairness MODEL_PATH DATA_PATH \
  --sensitive-features gender --sensitive-features race \
  --output fairness_report/
```

**Options**:
- `--sensitive-features` - Sensitive attribute names (can specify multiple)
- `--output`, `-o` - Output directory

---

### 2. Data Quality

#### Validate Dataset

```bash
aeva data validate DATA_PATH \
  --expectations expectations.json \
  --output validation_report/
```

**Options**:
- `--expectations` - Great Expectations suite file
- `--output`, `-o` - Output directory

**Example**:
```bash
aeva data validate data/training.csv \
  --output reports/data_quality/
```

#### Profile Dataset

```bash
aeva data profile DATA_PATH \
  --output profile.html
```

**Options**:
- `--output`, `-o` - Output HTML file path

---

### 3. Interactive Dashboard

#### Launch Web Dashboard

```bash
aeva dashboard
```

**Options**:
- `--port` - Port to run on (default: 8501)
- `--host` - Host to bind to (default: localhost)

**Example**:
```bash
# Launch on custom port
aeva dashboard --port 8080

# Launch on all interfaces
aeva dashboard --host 0.0.0.0 --port 8080
```

**Access**: Open browser to `http://localhost:8501`

---

### 4. API Server

#### Start REST API Server

```bash
aeva server
```

**Options**:
- `--port` - Port to run on (default: 8000)
- `--host` - Host to bind to (default: 0.0.0.0)
- `--reload` - Enable auto-reload for development

**Example**:
```bash
# Development mode with reload
aeva server --port 8000 --reload

# Production mode
aeva server --host 0.0.0.0 --port 8000
```

**API Docs**: Open browser to `http://localhost:8000/docs`

---

### 5. Project Management

#### Initialize New Project

```bash
aeva init PROJECT_NAME --template full
```

**Options**:
- `--template` - Project template: `basic`, `full`

**Example**:
```bash
aeva init my-ml-project --template full
cd my-ml-project
```

**Created Structure**:
```
my-ml-project/
├── data/
├── models/
├── results/
├── configs/
│   └── aeva.yaml
├── notebooks/      # (full template only)
├── tests/          # (full template only)
├── docs/           # (full template only)
└── README.md
```

---

### 6. System Information

#### Show AEVA Info

```bash
aeva info
```

**Output**:
- Version
- Author
- License
- Watermark ID
- GitHub URL
- Installed dependencies

---

## Global Options

All commands support these global options:

- `--debug` - Enable debug mode with verbose logging
- `--config PATH` - Path to custom config file
- `--quiet` - Suppress output except errors
- `--version` - Show version and exit
- `--help` - Show help message

**Example**:
```bash
# Run with debug logging
aeva --debug evaluate model model.pkl data.csv

# Use custom config
aeva --config custom_config.yaml evaluate model model.pkl data.csv

# Quiet mode
aeva --quiet data validate data.csv
```

---

## Web Dashboard

### Launch Dashboard

```bash
aeva dashboard
```

### Dashboard Pages

1. **🏠 主页** - Overview and system status
2. **🔍 可解释性分析** - SHAP/LIME explainability
3. **🛡️ 对抗鲁棒性** - Adversarial robustness testing
4. **📊 数据质量** - Data quality profiling
5. **📈 A/B 测试** - A/B testing and deployment
6. **📝 模型卡片** - Model card generation
7. **⚙️ 生产级集成** - Production integrations

### Features

- **Interactive Visualizations** - Charts, plots, and tables
- **File Upload** - Upload models and datasets
- **Real-time Results** - Instant feedback
- **Export Reports** - Download results in multiple formats
- **Responsive Design** - Works on desktop and mobile

---

## API Server

### Start Server

```bash
aeva server --port 8000
```

### API Endpoints

**Documentation**: `http://localhost:8000/docs`

**Key Endpoints**:
- `POST /api/v1/evaluate` - Evaluate model
- `POST /api/v1/explainability` - Generate explanations
- `POST /api/v1/fairness` - Evaluate fairness
- `GET /api/v1/status` - System status
- `GET /api/v1/health` - Health check

### Example API Call

```bash
curl -X POST "http://localhost:8000/api/v1/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "model_path": "models/classifier.pkl",
    "data_path": "data/test.csv",
    "metrics": ["accuracy", "f1"]
  }'
```

---

## Configuration

### Default Config Location

- `config/aeva.yaml` - Default configuration
- `~/.aeva/config.yaml` - User configuration
- Environment variable: `AEVA_CONFIG`

### Config File Format

```yaml
# AEVA Configuration
version: "2.0"

# Model evaluation settings
evaluation:
  metrics:
    - accuracy
    - f1_score
    - precision
    - recall

# Data quality settings
data_quality:
  check_missing: true
  check_duplicates: true

# API settings
api:
  host: "0.0.0.0"
  port: 8000

# Dashboard settings
dashboard:
  host: "localhost"
  port: 8501

# Watermark
watermark: AEVA-2026-LQC-dc68e33
```

---

## Examples

### Complete Workflow

```bash
# 1. Initialize project
aeva init my-evaluation --template full
cd my-evaluation

# 2. Validate data quality
aeva data validate data/dataset.csv --output reports/

# 3. Evaluate model
aeva evaluate model models/model.pkl data/test.csv \
  --metrics accuracy --metrics f1 \
  --format html \
  --output reports/

# 4. Generate explainability report
aeva evaluate explainability models/model.pkl data/test.csv \
  --method shap \
  --samples 100 \
  --output reports/explanations/

# 5. Check fairness
aeva evaluate fairness models/model.pkl data/test.csv \
  --sensitive-features gender \
  --output reports/fairness/

# 6. Launch dashboard to review results
aeva dashboard
```

### Automated Pipeline

```bash
#!/bin/bash
# automated_evaluation.sh

set -e

MODEL_PATH="models/production_model.pkl"
DATA_PATH="data/validation_set.csv"
OUTPUT_DIR="reports/$(date +%Y%m%d)"

mkdir -p "$OUTPUT_DIR"

# Validate data
aeva data validate "$DATA_PATH" --output "$OUTPUT_DIR/data_quality/"

# Evaluate model
aeva evaluate model "$MODEL_PATH" "$DATA_PATH" \
  --metrics accuracy --metrics f1 --metrics auc \
  --format json \
  --output "$OUTPUT_DIR/metrics/"

# Generate explanations
aeva evaluate explainability "$MODEL_PATH" "$DATA_PATH" \
  --method shap \
  --samples 50 \
  --output "$OUTPUT_DIR/explanations/"

# Check fairness
aeva evaluate fairness "$MODEL_PATH" "$DATA_PATH" \
  --sensitive-features gender --sensitive-features age \
  --output "$OUTPUT_DIR/fairness/"

echo "Evaluation complete! Results in $OUTPUT_DIR"
```

---

## Docker Usage

### Using Docker

```bash
# Build image
docker build -t aeva:latest .

# Run CLI command
docker run -v $(pwd)/data:/data aeva:latest \
  aeva evaluate model /data/model.pkl /data/test.csv

# Run dashboard
docker run -p 8501:8501 aeva:latest aeva dashboard --host 0.0.0.0

# Run API server
docker run -p 8000:8000 aeva:latest aeva server --host 0.0.0.0
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Services**:
- Dashboard: http://localhost:8501
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

## Troubleshooting

### Dashboard Won't Start

**Error**: `streamlit: command not found`

**Solution**:
```bash
pip install streamlit
```

### API Server Fails

**Error**: `fastapi: command not found`

**Solution**:
```bash
pip install fastapi uvicorn
```

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'aeva'`

**Solution**:
```bash
# Install in development mode
pip install -e .
```

### Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Use different port
aeva dashboard --port 8502
aeva server --port 8001
```

---

## Advanced Usage

### Custom Metrics

Create custom metric function:

```python
# custom_metrics.py
def custom_metric(y_true, y_pred):
    # Your custom logic
    return score

# Register with AEVA
from aeva.core.metrics import register_metric
register_metric('custom', custom_metric)
```

### Extending CLI

Add custom commands to `aeva/cli_enhanced.py`:

```python
@cli.command('custom')
@click.argument('input_path')
def custom_command(input_path):
    """Custom command description"""
    # Your logic here
    click.echo(f"Processing {input_path}...")
```

---

## Best Practices

1. **Use version control** - Track model and data versions
2. **Automate evaluation** - Create scripts for reproducibility
3. **Set quality gates** - Define acceptance criteria
4. **Monitor production** - Use continuous evaluation
5. **Document everything** - Use model cards
6. **Check fairness** - Test across demographic groups
7. **Test robustness** - Evaluate adversarial examples

---

## Support

- **GitHub**: https://github.com/liqcui/AEVA-P
- **Issues**: https://github.com/liqcui/AEVA-P/issues
- **Email**: liquan_cui@126.com

---

## License

**Dual License**:
- ✅ FREE for personal/academic use (with attribution)
- ⚠️ Commercial use requires explicit permission

**Watermark**: AEVA-2026-LQC-dc68e33

See [LICENSE](../LICENSE) for details.

---

*AEVA v2.0 - Algorithm Evaluation & Validation Agent*
*Copyright © 2024-2026 AEVA Development Team*
