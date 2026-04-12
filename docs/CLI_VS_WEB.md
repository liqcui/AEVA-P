# CLI vs Web Interface Comparison

**Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.**
**Watermark**: AEVA-2026-LQC-dc68e33

---

## Overview

AEVA provides two powerful interaction methods:

| Method | Best For | Advantages |
|--------|----------|------------|
| **CLI** | Automation, CI/CD, scripting | Fast, scriptable, reproducible |
| **Web** | Exploration, visualization, demos | Interactive, visual, user-friendly |

---

## Quick Comparison

### Model Evaluation

**CLI**:
```bash
aeva evaluate model models/classifier.pkl data/test.csv \
  --metrics accuracy --metrics f1 \
  --format html \
  --output reports/
```

**Web**:
1. Open `http://localhost:8501`
2. Navigate to "🏠 主页"
3. Upload model and dataset
4. Click "Evaluate"
5. View interactive results

---

### Explainability Analysis

**CLI**:
```bash
aeva evaluate explainability models/model.pkl data/test.csv \
  --method shap \
  --samples 100 \
  --output explanations/
```

**Web**:
1. Navigate to "🔍 可解释性分析"
2. Upload model and data
3. Select SHAP or LIME
4. Configure samples
5. View interactive plots

---

### Data Quality Validation

**CLI**:
```bash
aeva data validate data/dataset.csv \
  --output reports/data_quality/
```

**Web**:
1. Navigate to "📊 数据质量"
2. Upload dataset
3. Click "Analyze Quality"
4. View quality dashboard with charts

---

### Fairness Evaluation

**CLI**:
```bash
aeva evaluate fairness models/model.pkl data/test.csv \
  --sensitive-features gender --sensitive-features race \
  --output fairness/
```

**Web**:
1. Navigate to "📊 数据质量" or custom fairness page
2. Upload model and data
3. Select sensitive attributes
4. View fairness metrics and visualizations

---

## Feature Matrix

| Feature | CLI | Web | Notes |
|---------|-----|-----|-------|
| **Model Evaluation** | ✅ | ✅ | Both fully supported |
| **Explainability (SHAP/LIME)** | ✅ | ✅ | Web has interactive plots |
| **Adversarial Robustness** | ⚠️ | ✅ | CLI: basic, Web: full |
| **Data Quality** | ✅ | ✅ | Web has visual dashboard |
| **A/B Testing** | ⚠️ | ✅ | Web more interactive |
| **Model Cards** | ⚠️ | ✅ | Web has template editor |
| **Batch Processing** | ✅ | ❌ | CLI only |
| **Interactive Visualization** | ❌ | ✅ | Web only |
| **CI/CD Integration** | ✅ | ❌ | CLI only |
| **Real-time Feedback** | ⚠️ | ✅ | Web superior |
| **Scriptability** | ✅ | ❌ | CLI only |
| **User-Friendly** | ⚠️ | ✅ | Web easier for beginners |

✅ = Fully supported | ⚠️ = Partial support | ❌ = Not supported

---

## Use Cases

### Use CLI When:

1. **Automation & CI/CD**
   ```bash
   # In CI/CD pipeline
   aeva evaluate model $MODEL_PATH $DATA_PATH --format json
   ```

2. **Batch Processing**
   ```bash
   for model in models/*.pkl; do
     aeva evaluate model "$model" data/test.csv --output "reports/$(basename $model)"
   done
   ```

3. **Scripting & Reproducibility**
   ```bash
   #!/bin/bash
   # evaluation_pipeline.sh
   aeva data validate data.csv
   aeva evaluate model model.pkl data.csv --metrics accuracy --metrics f1
   aeva evaluate explainability model.pkl data.csv --method shap
   ```

4. **Remote/Headless Servers**
   ```bash
   # SSH into server
   ssh server "cd /path/to/project && aeva evaluate model model.pkl data.csv"
   ```

5. **Quick One-off Tasks**
   ```bash
   aeva data profile data.csv --output profile.html
   ```

---

### Use Web When:

1. **Exploratory Analysis**
   - Upload different datasets
   - Try various methods interactively
   - Visualize results immediately

2. **Presentations & Demos**
   - Show live evaluation to stakeholders
   - Interactive parameter tuning
   - Real-time visualizations

3. **Model Debugging**
   - Inspect individual predictions
   - Explore SHAP/LIME explanations
   - Analyze failure cases

4. **Team Collaboration**
   - Share dashboard URL
   - Non-technical stakeholders can use
   - Visual feedback easier to discuss

5. **Learning & Training**
   - New users can explore features
   - Visual feedback aids understanding
   - No command-line knowledge needed

---

## Workflow Examples

### Development Workflow (Web)

1. **Explore** - Use Web dashboard to explore data and models
2. **Iterate** - Quickly try different configurations
3. **Debug** - Use interactive visualizations to understand issues
4. **Document** - Generate model cards via Web interface

### Production Workflow (CLI)

1. **Automate** - Script evaluation pipeline
2. **Integrate** - Add to CI/CD
3. **Monitor** - Schedule periodic evaluations
4. **Alert** - Trigger notifications on quality gate failures

---

## Combined Workflow

**Best Practice**: Use both!

```bash
# 1. Quick exploration (Web)
aeva dashboard

# 2. Finalize parameters and automate (CLI)
aeva evaluate model models/final.pkl data/test.csv \
  --metrics accuracy --metrics f1 \
  --format json \
  --output reports/

# 3. Schedule automated runs (CLI + cron)
0 2 * * * cd /path/to/project && aeva evaluate model model.pkl data.csv
```

---

## Performance Comparison

| Metric | CLI | Web |
|--------|-----|-----|
| **Startup Time** | <1s | ~5s (Streamlit) |
| **Evaluation Speed** | Fast | Same |
| **Memory Usage** | Low | Medium (browser) |
| **Scalability** | High (batch) | Medium |
| **Responsiveness** | Instant | ~1s delay |

---

## Access Methods

### CLI

```bash
# Local installation
pip install -e .
aeva --help

# Docker
docker run aeva:latest aeva --help

# Python
from aeva.cli_enhanced import cli
cli()
```

### Web

```bash
# Local
aeva dashboard

# Docker
docker run -p 8501:8501 aeva:latest aeva dashboard --host 0.0.0.0

# Docker Compose
docker-compose up dashboard

# Python
import streamlit.web.cli as stcli
import sys
sys.argv = ["streamlit", "run", "aeva/dashboard/app.py"]
stcli.main()
```

---

## Configuration

### CLI Configuration

```bash
# Use config file
aeva --config config/custom.yaml evaluate model model.pkl data.csv

# Environment variable
export AEVA_CONFIG=/path/to/config.yaml
aeva evaluate model model.pkl data.csv

# Command-line options (highest priority)
aeva --debug evaluate model model.pkl data.csv
```

### Web Configuration

```bash
# Port and host
aeva dashboard --port 8080 --host 0.0.0.0

# Environment variables
export STREAMLIT_SERVER_PORT=8080
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
aeva dashboard
```

---

## Output Formats

### CLI Outputs

- **JSON** - Machine-readable, perfect for automation
- **HTML** - Rich reports with charts
- **Markdown** - Documentation-friendly
- **Text** - Console output

### Web Outputs

- **Interactive Charts** - Plotly, Altair
- **Tables** - Sortable, filterable
- **Downloads** - Export to JSON, CSV, PDF
- **Screenshots** - Visual reports

---

## Example: Complete Evaluation

### CLI Approach

```bash
#!/bin/bash
# complete_evaluation.sh

set -e

MODEL="models/classifier.pkl"
DATA="data/test.csv"
OUTPUT="reports/$(date +%Y%m%d_%H%M%S)"

mkdir -p "$OUTPUT"

echo "1. Validating data..."
aeva data validate "$DATA" --output "$OUTPUT/data_quality/"

echo "2. Evaluating model..."
aeva evaluate model "$MODEL" "$DATA" \
  --metrics accuracy --metrics f1 --metrics precision --metrics recall \
  --format html \
  --output "$OUTPUT/metrics/"

echo "3. Generating explanations..."
aeva evaluate explainability "$MODEL" "$DATA" \
  --method shap \
  --samples 100 \
  --output "$OUTPUT/explanations/"

echo "4. Checking fairness..."
aeva evaluate fairness "$MODEL" "$DATA" \
  --sensitive-features gender --sensitive-features age \
  --output "$OUTPUT/fairness/"

echo "✅ Evaluation complete! Results in $OUTPUT"
```

### Web Approach

1. Launch dashboard: `aeva dashboard`
2. Navigate to "🏠 主页"
3. Upload model and dataset
4. Click through each analysis:
   - Model Evaluation
   - Explainability
   - Data Quality
   - Fairness
5. Download reports from each page

---

## Recommendation

### For Individual Developers

- **Use Web** for development and exploration
- **Use CLI** for automation and final pipelines
- **Combine** for best results

### For Teams

- **Web Dashboard** - Shared for collaboration
- **CLI Scripts** - Version-controlled pipelines
- **API Server** - Integration with other tools

### For Production

- **CLI** - Automated, scheduled evaluations
- **API** - Integration with ML platforms
- **Web** (optional) - Monitoring dashboard

---

## Summary

| Aspect | CLI | Web |
|--------|-----|-----|
| **Speed** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Ease of Use** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Automation** | ⭐⭐⭐⭐⭐ | ⭐ |
| **Visualization** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Scripting** | ⭐⭐⭐⭐⭐ | ⭐ |
| **Collaboration** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **CI/CD** | ⭐⭐⭐⭐⭐ | ⭐ |
| **Learning Curve** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**Recommendation**: Use both! They complement each other perfectly.

---

*AEVA v2.0 - Dual Interface for Maximum Flexibility*
*Copyright © 2024-2026 AEVA Development Team*
