# AEVA Dashboard Internationalization (i18n)

## 📚 Overview

AEVA Dashboard now supports **bilingual interface** with automatic browser language detection:
- 🇨🇳 **Chinese (中文)** - Default for Chinese browsers
- 🇺🇸 **English** - Default for English browsers
- 🌐 **Auto-detection** - Automatically detects browser language

## 🎯 Features

### Automatic Language Detection
The dashboard automatically detects your browser language and displays the appropriate interface.

### Manual Language Selection
Users can manually override the language setting using the language selector in the sidebar:
- 🌐 Auto Detect (自动检测)
- 🇨🇳 中文 (Chinese)
- 🇺🇸 English

### Supported Pages
All pages support bilingual interface:

**Main Pages (8)**:
1. 🏠 Home / 主页
2. 🔍 Explainability / 可解释性分析
3. 🛡️ Robustness / 对抗鲁棒性
4. 📊 Data Quality / 数据质量
5. 📈 A/B Testing / A/B 测试
6. 📝 Model Cards / 模型卡片
7. 🤖 LLM Evaluation / LLM 评测
8. ⚙️ Production Integration / 生产级集成

**Advanced Features (4)**:
1. 🏆 Benchmark Suite / 基准测试套件
2. 🤖 Auto Pipeline / 自动化流水线
3. 🧠 Brain Analysis / 智能分析引擎
4. 🛡️ Quality Guard / 质量门禁系统

## 🔧 Implementation

### Using the i18n Module

```python
from aeva.dashboard.i18n import t, get_current_language, init_language

# Initialize language (call once at the beginning)
init_language()

# Get translated text
title = t("nav_home")  # Returns "🏠 主页" or "🏠 Home"

# Get current language
lang = get_current_language()  # Returns "zh" or "en"

# Use in conditions
if lang == "zh":
    st.markdown("欢迎")
else:
    st.markdown("Welcome")
```

### Adding New Translations

Edit `aeva/dashboard/i18n.py` and add your translations to the `TRANSLATIONS` dictionary:

```python
TRANSLATIONS = {
    "zh": {
        "your_key": "你的中文翻译",
        # ...
    },
    "en": {
        "your_key": "Your English Translation",
        # ...
    }
}
```

Then use it in your code:

```python
st.markdown(t("your_key"))
```

### Language Selector

The language selector is automatically rendered in the sidebar by `language_selector()` function in `app.py`.

## 🌐 URL-based Language Selection

You can also set the language via URL query parameter:

```
http://localhost:8501/?lang=zh   # Force Chinese
http://localhost:8501/?lang=en   # Force English
```

## 📝 Translation Keys Reference

### Navigation
- `nav_home` - Home navigation item
- `nav_explainability` - Explainability navigation item
- `nav_robustness` - Robustness navigation item
- `nav_data_quality` - Data Quality navigation item
- `nav_ab_testing` - A/B Testing navigation item
- `nav_model_cards` - Model Cards navigation item
- `nav_llm_evaluation` - LLM Evaluation navigation item
- `nav_production` - Production Integration navigation item

### System Info
- `system_info` - System Information title
- `version` - Version label
- `status` - Status label
- `pages` - Pages label
- `main_pages` - Main Pages label
- `advanced_features` - Advanced Features label

### Benchmark
- `benchmark_title` - Benchmark page title
- `benchmark_subtitle` - Benchmark page subtitle
- `benchmark_tab_suites` - Suite Management tab
- `benchmark_tab_run` - Run Tests tab
- `benchmark_tab_compare` - Compare Results tab
- `benchmark_tab_code` - Code Examples tab

### Auto Pipeline
- `auto_title` - Auto Pipeline page title
- `auto_subtitle` - Auto Pipeline page subtitle
- `auto_tab_pipeline` - Pipeline Management tab
- `auto_tab_scheduling` - Task Scheduling tab
- `auto_tab_monitoring` - Execution Monitoring tab
- `auto_tab_distributed` - Distributed Execution tab
- `auto_tab_code` - Code Examples tab

### Brain
- `brain_title` - Brain page title
- `brain_subtitle` - Brain page subtitle
- `brain_tab_analysis` - Result Analysis tab
- `brain_tab_root_cause` - Root Cause Analysis tab
- `brain_tab_suggestions` - Improvement Suggestions tab
- `brain_tab_llm` - LLM Configuration tab
- `brain_tab_code` - Code Examples tab

### Guard
- `guard_title` - Guard page title
- `guard_subtitle` - Guard page subtitle
- `guard_tab_management` - Gate Management tab
- `guard_tab_rules` - Rule Configuration tab
- `guard_tab_monitoring` - Execution Monitoring tab
- `guard_tab_statistics` - Statistics Report tab
- `guard_tab_code` - Code Examples tab

### Common
- `back_to_home` - Back to home button text
- `name` - Name label
- `description` - Description label
- `status` - Status label
- `create` - Create button text
- `run` - Run button text
- `view` - View button text

### Home Page
- `home_welcome` - Welcome message
- `home_subtitle` - Page subtitle
- `home_quick_start` - Quick Start section title
- `home_core_features` - Core Features section title
- `home_advanced_features` - Advanced Features section title
- `home_goto_benchmark` - Go to Benchmark button
- `home_goto_auto` - Go to Auto Pipeline button
- `home_goto_brain` - Go to Brain Analysis button
- `home_goto_guard` - Go to Quality Guard button

### Language
- `language` - Language selector title
- `lang_auto` - Auto Detect option
- `lang_zh` - Chinese option
- `lang_en` - English option

## 🎨 Best Practices

### 1. Always Use Translation Keys
```python
# ✅ Good
st.markdown(f"## {t('benchmark_title')}")

# ❌ Bad
st.markdown("## 🏆 基准测试套件")
```

### 2. Keep Keys Organized
Use prefixes to group related translations:
- `nav_*` - Navigation items
- `benchmark_*` - Benchmark page items
- `auto_*` - Auto Pipeline page items
- `brain_*` - Brain page items
- `guard_*` - Guard page items

### 3. Use Conditional Rendering for Complex Content
For long text blocks with different formatting:
```python
lang = get_current_language()
if lang == "zh":
    st.markdown("""
    ### 中文内容
    详细的中文描述...
    """)
else:
    st.markdown("""
    ### English Content
    Detailed English description...
    """)
```

### 4. Maintain Consistency
- Use same emoji for both languages
- Keep formatting consistent
- Align feature names across languages

## 🔄 Migration Guide

### Migrating Existing Pages

1. Import i18n module:
```python
from aeva.dashboard.i18n import t, get_current_language
```

2. Replace hardcoded text with translation keys:
```python
# Before
st.markdown("## 📊 基准套件")

# After
st.markdown(f"## {t('benchmark_tab_suites')}")
```

3. For complex bilingual content, use conditional rendering:
```python
lang = get_current_language()
if lang == "zh":
    # Chinese content
else:
    # English content
```

## 📊 Current Coverage

### Fully Translated
- ✅ Main navigation (8 pages)
- ✅ System information sidebar
- ✅ Language selector
- ✅ Home page structure
- ✅ Advanced features navigation buttons
- ✅ All advanced feature page titles and tabs

### Partially Translated
- 🟡 Home page content (uses conditional rendering)
- 🟡 Advanced feature page content (titles and tabs only)

### To Be Translated
- ⬜ Detailed content within advanced feature pages
- ⬜ Form labels and buttons
- ⬜ Code examples and documentation links

## 🚀 Future Enhancements

1. **More Languages**: Add support for additional languages (Spanish, French, Japanese, etc.)
2. **Dynamic Content**: Translate dynamically generated content
3. **User Preferences**: Remember user's language preference across sessions
4. **Translation Management**: Use JSON files for easier translation management
5. **RTL Support**: Add right-to-left language support (Arabic, Hebrew)

## 📞 Support

For questions or issues related to internationalization, please:
1. Check the translation keys in `aeva/dashboard/i18n.py`
2. Review examples in updated pages (home.py, benchmark.py, etc.)
3. Open an issue on GitHub with the `i18n` label

## 📝 License

Copyright © 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
