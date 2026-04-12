# AEVA Quick Start Guide

Get started with AEVA in 5 minutes!

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AVEA-P
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your Claude API key:

```bash
AEVA_BRAIN_API_KEY=your_api_key_here
```

## Basic Usage

### Example 1: Simple Evaluation

```python
from aeva import AEVA
from aeva.core.pipeline import Pipeline, FunctionStage, StageType

# Initialize AEVA
aeva = AEVA(config_path="config/aeva.yaml")

# Create pipeline
pipeline = aeva.create_pipeline(name="my_evaluation")

# Add evaluation stage
def evaluate(context):
    # Your evaluation logic here
    return {"metrics": {"accuracy": 0.95}}

pipeline.add_function("eval", evaluate, StageType.BENCHMARK)

# Run evaluation
result = aeva.run(pipeline)
print(result.summary())
```

### Example 2: With Quality Gates

```python
from aeva import AEVA
from aeva.guard import ThresholdGate

aeva = AEVA(config_path="config/aeva.yaml")

# Add quality gate
gate = ThresholdGate(
    name="accuracy_gate",
    threshold=0.90,
    metric_name="accuracy"
)
aeva.guard.add_gate(gate)

# Run pipeline
result = aeva.run(pipeline)

# Check gate result
if result.gate_result.passed:
    print("✓ Quality gate passed!")
else:
    print("✗ Quality gate failed!")
```

### Example 3: Run Complete Examples

```bash
# Basic usage example
python examples/basic_usage.py

# Brain analysis example (requires Claude API key)
python examples/advanced_brain_analysis.py

# Benchmark suite example
python examples/benchmark_suite_example.py
```

## CLI Usage

```bash
# Show version
aeva version

# Initialize new project
aeva init

# Check status
aeva status

# Start API server
aeva server
```

## Docker Usage

```bash
# Build and start all services
docker-compose up -d

# Access API at http://localhost:8000
curl http://localhost:8000/status

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Next Steps

1. **Read the full README**: [README.md](README.md)
2. **Explore examples**: Check the `examples/` directory
3. **Configure AEVA**: Edit `config/aeva.yaml`
4. **Run tests**: `pytest tests/`
5. **Build custom pipelines**: See documentation

## Common Issues

### Issue: Import Error

```bash
pip install -e .
```

### Issue: API Key Not Found

Make sure your `.env` file contains:
```
AEVA_BRAIN_API_KEY=sk-ant-...
```

### Issue: Database Connection

For local development, you can disable database features in `config/aeva.yaml`.

## Support

- Issues: https://github.com/liqcui/AVEA-P/issues
- Documentation: See `docs/` directory

---

**Ready to evaluate algorithms intelligently!** 🚀
