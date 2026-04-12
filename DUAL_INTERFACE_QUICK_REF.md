# 🚀 AEVA Dual Interface - Quick Reference Card

**Watermark**: AEVA-2026-LQC-dc68e33 | **Copyright**: © 2024-2026 AEVA Development Team

---

## ⚡ Quick Start

### CLI
```bash
pip install -e .
aeva --help
```

### Web
```bash
aeva dashboard
# Open: http://localhost:8501
```

---

## 📋 Command Cheat Sheet

### Model Evaluation
```bash
# CLI
aeva evaluate model MODEL.pkl DATA.csv --metrics accuracy --metrics f1

# Web
Navigate to 🏠 主页 → Upload files → Click "Evaluate"
```

### Explainability
```bash
# CLI
aeva evaluate explainability MODEL.pkl DATA.csv --method shap --samples 100

# Web
Navigate to 🔍 可解释性分析 → Select SHAP/LIME → Analyze
```

### Data Quality
```bash
# CLI
aeva data validate DATA.csv --output reports/
aeva data profile DATA.csv --output profile.html

# Web
Navigate to 📊 数据质量 → Upload data → View dashboard
```

### Fairness
```bash
# CLI
aeva evaluate fairness MODEL.pkl DATA.csv --sensitive-features gender

# Web
Navigate to 📊 数据质量 or custom page → Select features → Evaluate
```

---

## 🎯 Quick Decision Guide

**Need automation?** → Use CLI
**Need visualization?** → Use Web
**Need both?** → Use both! They work together.

---

## 🔧 Service Launchers

### Dashboard
```bash
aeva dashboard [--port PORT] [--host HOST]
```

### API Server
```bash
aeva server [--port PORT] [--host HOST] [--reload]
```

### Project Init
```bash
aeva init PROJECT_NAME [--template basic|full]
```

---

## 🐳 Docker Quick Commands

```bash
# Build
docker build -t aeva:latest .

# Run CLI
docker run aeva:latest aeva --help

# Run Dashboard
docker run -p 8501:8501 aeva:latest aeva dashboard --host 0.0.0.0

# Run API
docker run -p 8000:8000 aeva:latest aeva server --host 0.0.0.0

# Docker Compose
docker-compose up -d
```

---

## 📖 Documentation Links

- **Complete CLI Guide**: [`docs/CLI_USAGE.md`](docs/CLI_USAGE.md)
- **CLI vs Web**: [`docs/CLI_VS_WEB.md`](docs/CLI_VS_WEB.md)
- **Implementation Details**: [`docs/DUAL_INTERFACE_IMPLEMENTATION.md`](docs/DUAL_INTERFACE_IMPLEMENTATION.md)
- **Examples**: [`examples/cli_usage_example.py`](examples/cli_usage_example.py)

---

## 🎭 Interface Features

| Feature | CLI | Web |
|---------|:---:|:---:|
| Model Eval | ✅ | ✅ |
| SHAP/LIME | ✅ | ✅ |
| Data Quality | ✅ | ✅ |
| Batch Mode | ✅ | ❌ |
| Interactive | ❌ | ✅ |
| Automation | ✅ | ❌ |
| Visualization | ⚠️ | ✅ |

✅ Full support | ⚠️ Partial | ❌ Not available

---

## 💡 Pro Tips

1. **Explore with Web, automate with CLI**
   ```bash
   # First: aeva dashboard (find best params)
   # Then: aeva evaluate model ... (automate it)
   ```

2. **Use config files for consistency**
   ```bash
   aeva --config config/prod.yaml evaluate model ...
   ```

3. **Chain commands with &&**
   ```bash
   aeva data validate data.csv && aeva evaluate model model.pkl data.csv
   ```

4. **Debug with --debug**
   ```bash
   aeva --debug evaluate model model.pkl data.csv
   ```

---

## 🚨 Common Issues

**Dashboard won't start?**
```bash
pip install streamlit
```

**API server fails?**
```bash
pip install fastapi uvicorn
```

**Import errors?**
```bash
pip install -e .
```

**Port in use?**
```bash
aeva dashboard --port 8502
```

---

## 📞 Support

- **GitHub**: https://github.com/liqcui/AEVA-P
- **Email**: liquan_cui@126.com
- **Issues**: https://github.com/liqcui/AEVA-P/issues

---

**Print this page and keep it handy! 📄**

*AEVA v2.0 - Choose your interface, own your evaluation*
