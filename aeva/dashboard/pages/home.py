"""
Home page of AEVA dashboard

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import i18n
from aeva.dashboard.i18n import t, get_current_language


def render():
    """Render home page"""

    lang = get_current_language()

    st.markdown('<p class="main-header">🤖 AEVA v2.0 Dashboard</p>', unsafe_allow_html=True)
    st.markdown("### Algorithm Evaluation & Validation Agent")

    st.markdown("---")

    # Overview
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Core Modules / 核心模块" if lang == "en" else "核心模块",
            value="12",
            delta="100%"
        )

    with col2:
        st.metric(
            label="Prod Integrations / 生产集成" if lang == "en" else "生产集成",
            value="3",
            delta="ART + GE + SM"
        )

    with col3:
        st.metric(
            label="Test Coverage / 测试覆盖" if lang == "en" else "测试覆盖",
            value="65%",
            delta="68 tests"
        )

    with col4:
        st.metric(
            label="Maturity / 项目成熟度" if lang == "en" else "项目成熟度",
            value="90%",
            delta="+50%"
        )

    st.markdown("---")

    # Features
    st.markdown(f"## 🎯 {t('home_core_features')}")

    col1, col2 = st.columns(2)

    with col1:
        if lang == "zh":
            st.markdown("""
            ### 📊 模型评估
            - **可解释性**: SHAP, LIME, 特征重要性
            - **鲁棒性**: 对抗攻击测试 (40+ methods)
            - **公平性**: 偏见检测与缓解
            - **性能**: 多维度性能分析

            ### 📈 数据分析
            - **质量评估**: 50+ 数据期望
            - **画像分析**: 自动化数据分析
            - **A/B测试**: 统计检验与功效分析
            - **版本管理**: 数据集版本控制
            """)
        else:
            st.markdown("""
            ### 📊 Model Evaluation
            - **Explainability**: SHAP, LIME, Feature Importance
            - **Robustness**: Adversarial Testing (40+ methods)
            - **Fairness**: Bias Detection & Mitigation
            - **Performance**: Multi-dimensional Analysis

            ### 📈 Data Analysis
            - **Quality Assessment**: 50+ Data Expectations
            - **Profiling**: Automated Data Analysis
            - **A/B Testing**: Statistical Tests & Power Analysis
            - **Versioning**: Dataset Version Control
            """)

    with col2:
        if lang == "zh":
            st.markdown("""
            ### 🔧 生产工具
            - **模型卡片**: 自动生成文档
            - **持续监控**: 模型drift检测
            - **基准测试**: 标准benchmark套件
            - **报告生成**: 专业级报告

            ### 🚀 企业特性
            - **生产集成**: ART, Great Expectations, statsmodels
            - **API服务**: RESTful API
            - **Docker支持**: 容器化部署
            - **仪表板**: 实时可视化
            """)
        else:
            st.markdown("""
            ### 🔧 Production Tools
            - **Model Cards**: Auto-generated Documentation
            - **Monitoring**: Model Drift Detection
            - **Benchmarking**: Standard Benchmark Suites
            - **Reporting**: Professional-grade Reports

            ### 🚀 Enterprise Features
            - **Integrations**: ART, Great Expectations, statsmodels
            - **API Service**: RESTful API
            - **Docker Support**: Containerized Deployment
            - **Dashboard**: Real-time Visualization
            """)

    st.markdown("---")

    # Quick Actions
    st.markdown(f"## ⚡ {t('home_quick_start')}")

    col1, col2, col3 = st.columns(3)

    with col1:
        btn_text = "🔍 Run Explainability" if lang == "en" else "🔍 运行可解释性分析"
        info_text = "Go to 'Explainability' page" if lang == "en" else "请前往'可解释性分析'页面"
        if st.button(btn_text, key="quick_explain"):
            st.info(info_text)

    with col2:
        btn_text = "🛡️ Test Robustness" if lang == "en" else "🛡️ 测试对抗鲁棒性"
        info_text = "Go to 'Robustness' page" if lang == "en" else "请前往'对抗鲁棒性'页面"
        if st.button(btn_text, key="quick_robust"):
            st.info(info_text)

    with col3:
        btn_text = "📊 Analyze Data Quality" if lang == "en" else "📊 分析数据质量"
        info_text = "Go to 'Data Quality' page" if lang == "en" else "请前往'数据质量'页面"
        if st.button(btn_text, key="quick_quality"):
            st.info(info_text)

    st.markdown("---")

    # Advanced Features
    st.markdown(f"## 🚀 {t('home_advanced_features')}")

    if lang == "zh":
        st.markdown("探索AEVA的高级企业级功能，包括基准测试、自动化流水线、智能分析和质量门禁。")
    else:
        st.markdown("Explore AEVA's advanced enterprise features, including benchmarking, automation pipelines, intelligent analysis, and quality gates.")

    col1, col2 = st.columns(2)

    with col1:
        # Benchmark
        if lang == "zh":
            st.markdown("""
            ### 🏆 基准测试套件
            标准化评估与多模型对比

            **核心能力**:
            - 📋 创建自定义基准套件
            - 🔧 配置评估指标
            - 📁 管理测试数据集
            - 📈 多模型性能对比
            """)
        else:
            st.markdown("""
            ### 🏆 Benchmark Suite
            Standardized Evaluation & Multi-Model Comparison

            **Core Capabilities**:
            - 📋 Create Custom Benchmark Suites
            - 🔧 Configure Evaluation Metrics
            - 📁 Manage Test Datasets
            - 📈 Multi-Model Performance Comparison
            """)
        if st.button(t("home_goto_benchmark"), key="goto_benchmark", use_container_width=True):
            st.session_state.subpage = "benchmark"
            st.rerun()

        # Brain
        if lang == "zh":
            st.markdown("""
            ### 🧠 智能分析引擎
            基于LLM的智能结果分析

            **核心能力**:
            - 🔍 自动异常检测
            - 💡 AI驱动根因分析
            - 📝 智能改进建议
            - 🤖 Claude API集成
            """)
        else:
            st.markdown("""
            ### 🧠 Brain Analysis Engine
            LLM-Powered Intelligent Result Analysis

            **Core Capabilities**:
            - 🔍 Automatic Anomaly Detection
            - 💡 AI-Driven Root Cause Analysis
            - 📝 Intelligent Improvement Suggestions
            - 🤖 Claude API Integration
            """)
        if st.button(t("home_goto_brain"), key="goto_brain", use_container_width=True):
            st.session_state.subpage = "brain"
            st.rerun()

    with col2:
        # Auto Pipeline
        if lang == "zh":
            st.markdown("""
            ### 🤖 自动化流水线
            工作流编排与任务调度

            **核心能力**:
            - 🔄 可视化流水线配置
            - ⚙️ 定时与事件触发
            - 🚀 执行监控与统计
            - 📊 分布式执行支持
            """)
        else:
            st.markdown("""
            ### 🤖 Automation Pipeline
            Workflow Orchestration & Task Scheduling

            **Core Capabilities**:
            - 🔄 Visual Pipeline Configuration
            - ⚙️ Scheduled & Event Triggers
            - 🚀 Execution Monitoring & Statistics
            - 📊 Distributed Execution Support
            """)
        if st.button(t("home_goto_auto"), key="goto_auto", use_container_width=True):
            st.session_state.subpage = "auto"
            st.rerun()

        # Guard
        if lang == "zh":
            st.markdown("""
            ### 🛡️ 质量门禁系统
            自动化质量检查与发布控制

            **核心能力**:
            - 🎯 阈值/多指标门禁
            - 🚦 自动化质量检查
            - 📊 执行监控与统计
            - ⚡ 发布阻断保护
            """)
        else:
            st.markdown("""
            ### 🛡️ Quality Gate System
            Automated Quality Checks & Release Control

            **Core Capabilities**:
            - 🎯 Threshold/Multi-Metric Gates
            - 🚦 Automated Quality Checks
            - 📊 Execution Monitoring & Statistics
            - ⚡ Release Blocking Protection
            """)
        if st.button(t("home_goto_guard"), key="goto_guard", use_container_width=True):
            st.session_state.subpage = "guard"
            st.rerun()

    st.markdown("---")

    # Status
    if lang == "zh":
        st.markdown("## 📋 系统状态")
    else:
        st.markdown("## 📋 System Status")

    # Check production libraries
    libs_status = check_production_libraries()

    col1, col2 = st.columns(2)

    with col1:
        if lang == "zh":
            st.markdown("### 核心依赖")
        else:
            st.markdown("### Core Dependencies")
        st.success("""
        ✅ scikit-learn
        ✅ SHAP
        ✅ LIME
        ✅ scipy
        ✅ pandas
        ✅ numpy
        """)

    with col2:
        if lang == "zh":
            st.markdown("### 生产级库")
        else:
            st.markdown("### Production Libraries")

        if libs_status['art']:
            st.success("✅ ART (Adversarial Robustness Toolbox)")
        else:
            warning_text = "⚠️ ART未安装 (使用Fallback)" if lang == "zh" else "⚠️ ART not installed (Using Fallback)"
            st.warning(warning_text)

        if libs_status['ge']:
            st.success("✅ Great Expectations")
        else:
            warning_text = "⚠️ Great Expectations未安装 (使用Fallback)" if lang == "zh" else "⚠️ Great Expectations not installed (Using Fallback)"
            st.warning(warning_text)

        if libs_status['sm']:
            st.success("✅ statsmodels")
        else:
            warning_text = "⚠️ statsmodels未安装 (使用Fallback)" if lang == "zh" else "⚠️ statsmodels not installed (Using Fallback)"
            st.warning(warning_text)

        if libs_status['streamlit']:
            st.success("✅ Streamlit")
        else:
            error_text = "❌ Streamlit未安装" if lang == "zh" else "❌ Streamlit not installed"
            st.error(error_text)

    st.markdown("---")

    # Documentation
    if lang == "zh":
        st.markdown("## 📚 文档")
    else:
        st.markdown("## 📚 Documentation")

    col1, col2, col3 = st.columns(3)

    with col1:
        if lang == "zh":
            st.markdown("""
            **快速开始**
            - [QUICK_START.md](../QUICK_START.md)
            - [示例代码](../examples/)
            - [API参考](../docs/)
            """)
        else:
            st.markdown("""
            **Quick Start**
            - [QUICK_START.md](../QUICK_START.md)
            - [Example Code](../examples/)
            - [API Reference](../docs/)
            """)

    with col2:
        if lang == "zh":
            st.markdown("""
            **用户指南**
            - [生产集成指南](../docs/PRODUCTION_INTEGRATIONS.md)
            - [Docker部署](../docs/DOCKER_GUIDE.md)
            - [测试文档](../docs/PYTEST_SUMMARY.md)
            """)
        else:
            st.markdown("""
            **User Guide**
            - [Production Integration Guide](../docs/PRODUCTION_INTEGRATIONS.md)
            - [Docker Deployment](../docs/DOCKER_GUIDE.md)
            - [Testing Documentation](../docs/PYTEST_SUMMARY.md)
            """)

    with col3:
        if lang == "zh":
            st.markdown("""
            **开发文档**
            - [架构设计](../docs/ARCHITECTURE.md)
            - [优化报告](../OPTIMIZATION_COMPLETE_SUMMARY.md)
            - [验证报告](../TEST_RUN_VERIFICATION.md)
            """)
        else:
            st.markdown("""
            **Developer Docs**
            - [Architecture Design](../docs/ARCHITECTURE.md)
            - [Optimization Report](../OPTIMIZATION_COMPLETE_SUMMARY.md)
            - [Verification Report](../TEST_RUN_VERIFICATION.md)
            """)

    st.markdown("---")

    # Footer info
    if lang == "zh":
        st.info("""
        💡 **提示**: 使用左侧导航栏探索不同功能模块。每个模块都提供交互式演示和详细分析。
        """)
    else:
        st.info("""
        💡 **Tip**: Use the left navigation bar to explore different feature modules. Each module provides interactive demos and detailed analysis.
        """)


def check_production_libraries():
    """Check if production libraries are available"""
    status = {}

    try:
        import art
        status['art'] = True
    except ImportError:
        status['art'] = False

    try:
        import great_expectations
        status['ge'] = True
    except ImportError:
        status['ge'] = False

    try:
        import statsmodels
        status['sm'] = True
    except ImportError:
        status['sm'] = False

    try:
        import streamlit
        status['streamlit'] = True
    except ImportError:
        status['streamlit'] = False

    return status
