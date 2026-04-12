"""
Internationalization (i18n) support for AEVA Dashboard
Supports Chinese and English with browser language auto-detection

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import streamlit as st
from typing import Dict, Any


# Translation dictionaries
TRANSLATIONS = {
    "zh": {
        # Navigation
        "nav_home": "🏠 主页",
        "nav_explainability": "🔍 可解释性分析",
        "nav_robustness": "🛡️ 对抗鲁棒性",
        "nav_data_quality": "📊 数据质量",
        "nav_ab_testing": "📈 A/B 测试",
        "nav_model_cards": "📝 模型卡片",
        "nav_llm_evaluation": "🤖 LLM 评测",
        "nav_production": "⚙️ 生产级集成",
        "nav_report_generation": "📄 报告生成",

        # System Info
        "system_info": "系统信息",
        "version": "版本",
        "status": "状态",
        "status_ready": "✅ Production Ready",
        "pages": "页面",
        "main_pages": "主页面",
        "advanced_features": "高级功能",
        "modules": "模块",
        "core": "核心",
        "integrations": "集成",
        "test_coverage": "测试覆盖",

        # Advanced Features
        "advanced_benchmark": "🏆 基准测试套件",
        "advanced_auto": "🤖 自动化流水线",
        "advanced_brain": "🧠 智能分析引擎",
        "advanced_guard": "🛡️ 质量门禁系统",

        # Benchmark
        "benchmark_title": "🏆 基准测试套件",
        "benchmark_subtitle": "多模型对比与性能基准",
        "benchmark_tab_suites": "📊 基准套件管理",
        "benchmark_tab_run": "🎯 运行测试",
        "benchmark_tab_compare": "📈 结果对比",
        "benchmark_tab_code": "💻 代码示例",
        "benchmark_registered": "已注册的基准套件",
        "benchmark_create": "创建新的基准测试",
        "benchmark_best_model": "最佳模型",
        "benchmark_accuracy": "Accuracy",
        "benchmark_precision": "Precision",
        "benchmark_recall": "Recall",
        "benchmark_f1": "F1 Score",
        "benchmark_overall": "综合得分",
        "benchmark_top3": "Top 3 模型",
        "benchmark_rank_first": "第一名",
        "benchmark_rank_second": "第二名",
        "benchmark_rank_third": "第三名",

        # Auto Pipeline
        "auto_title": "🤖 自动化评估流水线",
        "auto_subtitle": "工作流编排与任务调度",
        "auto_tab_pipeline": "🔄 流水线管理",
        "auto_tab_scheduling": "⚙️ 任务调度",
        "auto_tab_monitoring": "🚀 执行监控",
        "auto_tab_distributed": "📊 分布式执行",
        "auto_tab_code": "💻 代码示例",
        "auto_registered": "已注册的流水线",
        "auto_visualization": "📊 流水线可视化示例",
        "auto_create": "创建新的流水线",
        "auto_select_pipeline": "选择流水线查看结构",
        "auto_total_tasks": "总任务数",
        "auto_execution_mode": "执行方式",
        "auto_estimated_time": "预计耗时",
        "auto_failure_strategy": "失败策略",

        # Brain
        "brain_title": "🧠 智能分析引擎",
        "brain_subtitle": "基于LLM的智能结果分析与建议",
        "brain_tab_analysis": "🔍 结果分析",
        "brain_tab_root_cause": "💡 根因分析",
        "brain_tab_suggestions": "📝 改进建议",
        "brain_tab_llm": "🤖 LLM配置",
        "brain_tab_code": "💻 代码示例",
        "brain_anomaly": "异常检测",
        "brain_pattern": "模式识别",
        "brain_trend": "趋势分析",
        "brain_root_cause": "根本原因分析",
        "brain_high_priority": "高优先级",
        "brain_medium_priority": "中优先级",
        "brain_low_priority": "低优先级",

        # Guard
        "guard_title": "🛡️ 质量门禁系统",
        "guard_subtitle": "自动化质量检查与发布控制",
        "guard_tab_management": "🎯 门禁管理",
        "guard_tab_rules": "📊 规则配置",
        "guard_tab_monitoring": "🚦 执行监控",
        "guard_tab_statistics": "📈 统计报告",
        "guard_tab_code": "💻 代码示例",
        "guard_registered": "已注册的门禁",
        "guard_create": "创建新的质量门禁",
        "guard_current_execution": "运行中的任务",
        "guard_recent_history": "最近执行记录",
        "guard_detailed_info": "详细执行信息",

        # Common
        "back_to_home": "← 返回主页",
        "name": "名称",
        "description": "描述",
        "status": "状态",
        "active": "活跃",
        "paused": "暂停",
        "enabled": "启用",
        "disabled": "暂停",
        "create": "创建",
        "run": "运行",
        "view": "查看",
        "success": "成功",
        "failed": "失败",
        "running": "运行中",
        "model": "模型",
        "models": "模型",
        "result": "结果",
        "results": "结果",
        "time": "时间",
        "duration": "耗时",

        # Home Page
        "home_welcome": "欢迎使用 AEVA v2.0",
        "home_subtitle": "全面的算法评估与验证平台",
        "home_quick_start": "快速开始",
        "home_core_features": "核心功能",
        "home_advanced_features": "高级功能",
        "home_goto_benchmark": "进入基准测试 →",
        "home_goto_auto": "进入自动化流水线 →",
        "home_goto_brain": "进入智能分析 →",
        "home_goto_guard": "进入质量门禁 →",

        # Language
        "language": "语言",
        "lang_auto": "🌐 自动检测",
        "lang_zh": "🇨🇳 中文",
        "lang_en": "🇺🇸 English",
    },

    "en": {
        # Navigation
        "nav_home": "🏠 Home",
        "nav_explainability": "🔍 Explainability",
        "nav_robustness": "🛡️ Robustness",
        "nav_data_quality": "📊 Data Quality",
        "nav_ab_testing": "📈 A/B Testing",
        "nav_model_cards": "📝 Model Cards",
        "nav_llm_evaluation": "🤖 LLM Evaluation",
        "nav_production": "⚙️ Production Integration",
        "nav_report_generation": "📄 Report Generation",

        # System Info
        "system_info": "System Info",
        "version": "Version",
        "status": "Status",
        "status_ready": "✅ Production Ready",
        "pages": "Pages",
        "main_pages": "Main Pages",
        "advanced_features": "Advanced Features",
        "modules": "Modules",
        "core": "Core",
        "integrations": "Integrations",
        "test_coverage": "Test Coverage",

        # Advanced Features
        "advanced_benchmark": "🏆 Benchmark Suite",
        "advanced_auto": "🤖 Auto Pipeline",
        "advanced_brain": "🧠 Brain Analysis",
        "advanced_guard": "🛡️ Quality Guard",

        # Benchmark
        "benchmark_title": "🏆 Benchmark Suite",
        "benchmark_subtitle": "Multi-Model Comparison & Performance Benchmarking",
        "benchmark_tab_suites": "📊 Benchmark Suites",
        "benchmark_tab_run": "🎯 Run Tests",
        "benchmark_tab_compare": "📈 Compare Results",
        "benchmark_tab_code": "💻 Code Examples",
        "benchmark_registered": "Registered Benchmark Suites",
        "benchmark_create": "Create New Benchmark",
        "benchmark_best_model": "Best Model",
        "benchmark_accuracy": "Accuracy",
        "benchmark_precision": "Precision",
        "benchmark_recall": "Recall",
        "benchmark_f1": "F1 Score",
        "benchmark_overall": "Overall Score",
        "benchmark_top3": "Top 3 Models",
        "benchmark_rank_first": "1st Place",
        "benchmark_rank_second": "2nd Place",
        "benchmark_rank_third": "3rd Place",

        # Auto Pipeline
        "auto_title": "🤖 Automated Evaluation Pipeline",
        "auto_subtitle": "Workflow Orchestration & Task Scheduling",
        "auto_tab_pipeline": "🔄 Pipeline Management",
        "auto_tab_scheduling": "⚙️ Task Scheduling",
        "auto_tab_monitoring": "🚀 Execution Monitoring",
        "auto_tab_distributed": "📊 Distributed Execution",
        "auto_tab_code": "💻 Code Examples",
        "auto_registered": "Registered Pipelines",
        "auto_visualization": "📊 Pipeline Visualization",
        "auto_create": "Create New Pipeline",
        "auto_select_pipeline": "Select pipeline to view structure",
        "auto_total_tasks": "Total Tasks",
        "auto_execution_mode": "Execution Mode",
        "auto_estimated_time": "Estimated Time",
        "auto_failure_strategy": "Failure Strategy",

        # Brain
        "brain_title": "🧠 Intelligent Analysis Engine",
        "brain_subtitle": "LLM-Powered Result Analysis & Recommendations",
        "brain_tab_analysis": "🔍 Result Analysis",
        "brain_tab_root_cause": "💡 Root Cause Analysis",
        "brain_tab_suggestions": "📝 Improvement Suggestions",
        "brain_tab_llm": "🤖 LLM Configuration",
        "brain_tab_code": "💻 Code Examples",
        "brain_anomaly": "Anomaly Detection",
        "brain_pattern": "Pattern Recognition",
        "brain_trend": "Trend Analysis",
        "brain_root_cause": "Root Cause Analysis",
        "brain_high_priority": "High Priority",
        "brain_medium_priority": "Medium Priority",
        "brain_low_priority": "Low Priority",

        # Guard
        "guard_title": "🛡️ Quality Gate System",
        "guard_subtitle": "Automated Quality Checks & Release Control",
        "guard_tab_management": "🎯 Gate Management",
        "guard_tab_rules": "📊 Rule Configuration",
        "guard_tab_monitoring": "🚦 Execution Monitoring",
        "guard_tab_statistics": "📈 Statistics Report",
        "guard_tab_code": "💻 Code Examples",
        "guard_registered": "Registered Gates",
        "guard_create": "Create New Quality Gate",
        "guard_current_execution": "Running Tasks",
        "guard_recent_history": "Recent Execution History",
        "guard_detailed_info": "Detailed Execution Info",

        # Common
        "back_to_home": "← Back to Home",
        "name": "Name",
        "description": "Description",
        "status": "Status",
        "active": "Active",
        "paused": "Paused",
        "enabled": "Enabled",
        "disabled": "Disabled",
        "create": "Create",
        "run": "Run",
        "view": "View",
        "success": "Success",
        "failed": "Failed",
        "running": "Running",
        "model": "Model",
        "models": "Models",
        "result": "Result",
        "results": "Results",
        "time": "Time",
        "duration": "Duration",

        # Home Page
        "home_welcome": "Welcome to AEVA v2.0",
        "home_subtitle": "Comprehensive Algorithm Evaluation & Validation Platform",
        "home_quick_start": "Quick Start",
        "home_core_features": "Core Features",
        "home_advanced_features": "Advanced Features",
        "home_goto_benchmark": "Go to Benchmark →",
        "home_goto_auto": "Go to Auto Pipeline →",
        "home_goto_brain": "Go to Brain Analysis →",
        "home_goto_guard": "Go to Quality Guard →",

        # Language
        "language": "Language",
        "lang_auto": "🌐 Auto Detect",
        "lang_zh": "🇨🇳 中文",
        "lang_en": "🇺🇸 English",
    }
}


def get_browser_language() -> str:
    """
    Detect browser language from Streamlit session
    Returns 'zh' for Chinese, 'en' for English
    """
    try:
        # Try to get from query params first
        query_params = st.query_params
        if "lang" in query_params:
            lang = query_params["lang"]
            if lang in ["zh", "en"]:
                return lang

        # Try to detect from browser (via JavaScript)
        # Note: This is a fallback, Streamlit doesn't directly expose browser language
        # Default to English
        return "en"
    except:
        return "en"


def init_language():
    """Initialize language settings in session state"""
    if "language" not in st.session_state:
        # Check if user has manually set language
        if "lang_override" in st.session_state:
            st.session_state.language = st.session_state.lang_override
        else:
            # Auto-detect from browser or default to English
            st.session_state.language = get_browser_language()


def set_language(lang: str):
    """Set the current language"""
    if lang in ["zh", "en"]:
        st.session_state.language = lang
        st.session_state.lang_override = lang


def get_text(key: str, lang: str = None) -> str:
    """
    Get translated text for the given key

    Args:
        key: Translation key
        lang: Language code ('zh' or 'en'). If None, uses session state language

    Returns:
        Translated text, or the key itself if not found
    """
    if lang is None:
        if "language" not in st.session_state:
            init_language()
        lang = st.session_state.language

    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)


def t(key: str) -> str:
    """Shorthand for get_text"""
    return get_text(key)


def language_selector():
    """
    Render language selector in sidebar
    """
    init_language()

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### {t('language')}")

    # Language options
    lang_options = {
        "auto": t("lang_auto"),
        "zh": t("lang_zh"),
        "en": t("lang_en")
    }

    # Current selection
    if "lang_override" in st.session_state:
        current = st.session_state.lang_override
    else:
        current = "auto"

    # Radio buttons
    selected = st.sidebar.radio(
        label="选择语言 / Select Language",
        options=list(lang_options.keys()),
        format_func=lambda x: lang_options[x],
        index=list(lang_options.keys()).index(current),
        label_visibility="collapsed"
    )

    # Update language if changed
    if selected != current:
        if selected == "auto":
            if "lang_override" in st.session_state:
                del st.session_state.lang_override
            st.session_state.language = get_browser_language()
        else:
            set_language(selected)
        st.rerun()


def get_current_language() -> str:
    """Get the current language code"""
    if "language" not in st.session_state:
        init_language()
    return st.session_state.language


# Export commonly used functions
__all__ = [
    'init_language',
    'set_language',
    'get_text',
    't',
    'language_selector',
    'get_current_language',
    'TRANSLATIONS'
]
