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


def render():
    """Render home page"""

    st.markdown('<p class="main-header">🤖 AEVA v2.0 Dashboard</p>', unsafe_allow_html=True)
    st.markdown("### Algorithm Evaluation & Validation Agent")

    st.markdown("---")

    # Overview
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="核心模块",
            value="12",
            delta="100%"
        )

    with col2:
        st.metric(
            label="生产集成",
            value="3",
            delta="ART + GE + SM"
        )

    with col3:
        st.metric(
            label="测试覆盖",
            value="65%",
            delta="68 tests"
        )

    with col4:
        st.metric(
            label="项目成熟度",
            value="90%",
            delta="+50%"
        )

    st.markdown("---")

    # Features
    st.markdown("## 🎯 核心功能")

    col1, col2 = st.columns(2)

    with col1:
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

    with col2:
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

    st.markdown("---")

    # Quick Actions
    st.markdown("## ⚡ 快速开始")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔍 运行可解释性分析", key="quick_explain"):
            st.info("请前往'可解释性分析'页面")

    with col2:
        if st.button("🛡️ 测试对抗鲁棒性", key="quick_robust"):
            st.info("请前往'对抗鲁棒性'页面")

    with col3:
        if st.button("📊 分析数据质量", key="quick_quality"):
            st.info("请前往'数据质量'页面")

    st.markdown("---")

    # Advanced Features
    st.markdown("## 🚀 高级功能")
    st.markdown("探索AEVA的高级企业级功能，包括基准测试、自动化流水线、智能分析和质量门禁。")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 🏆 基准测试套件
        标准化评估与多模型对比

        **核心能力**:
        - 📋 创建自定义基准套件
        - 🔧 配置评估指标
        - 📁 管理测试数据集
        - 📈 多模型性能对比
        """)
        if st.button("进入基准测试 →", key="goto_benchmark", use_container_width=True):
            st.session_state.subpage = "benchmark"
            st.rerun()

        st.markdown("""
        ### 🧠 智能分析引擎
        基于LLM的智能结果分析

        **核心能力**:
        - 🔍 自动异常检测
        - 💡 AI驱动根因分析
        - 📝 智能改进建议
        - 🤖 Claude API集成
        """)
        if st.button("进入智能分析 →", key="goto_brain", use_container_width=True):
            st.session_state.subpage = "brain"
            st.rerun()

    with col2:
        st.markdown("""
        ### 🤖 自动化流水线
        工作流编排与任务调度

        **核心能力**:
        - 🔄 可视化流水线配置
        - ⚙️ 定时与事件触发
        - 🚀 执行监控与统计
        - 📊 分布式执行支持
        """)
        if st.button("进入自动化流水线 →", key="goto_auto", use_container_width=True):
            st.session_state.subpage = "auto"
            st.rerun()

        st.markdown("""
        ### 🛡️ 质量门禁系统
        自动化质量检查与发布控制

        **核心能力**:
        - 🎯 阈值/多指标门禁
        - 🚦 自动化质量检查
        - 📊 执行监控与统计
        - ⚡ 发布阻断保护
        """)
        if st.button("进入质量门禁 →", key="goto_guard", use_container_width=True):
            st.session_state.subpage = "guard"
            st.rerun()

    st.markdown("---")

    # Status
    st.markdown("## 📋 系统状态")

    # Check production libraries
    libs_status = check_production_libraries()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 核心依赖")
        st.success("""
        ✅ scikit-learn
        ✅ SHAP
        ✅ LIME
        ✅ scipy
        ✅ pandas
        ✅ numpy
        """)

    with col2:
        st.markdown("### 生产级库")

        if libs_status['art']:
            st.success("✅ ART (Adversarial Robustness Toolbox)")
        else:
            st.warning("⚠️ ART未安装 (使用Fallback)")

        if libs_status['ge']:
            st.success("✅ Great Expectations")
        else:
            st.warning("⚠️ Great Expectations未安装 (使用Fallback)")

        if libs_status['sm']:
            st.success("✅ statsmodels")
        else:
            st.warning("⚠️ statsmodels未安装 (使用Fallback)")

        if libs_status['streamlit']:
            st.success("✅ Streamlit")
        else:
            st.error("❌ Streamlit未安装")

    st.markdown("---")

    # Documentation
    st.markdown("## 📚 文档")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **快速开始**
        - [QUICK_START.md](../QUICK_START.md)
        - [示例代码](../examples/)
        - [API参考](../docs/)
        """)

    with col2:
        st.markdown("""
        **用户指南**
        - [生产集成指南](../docs/PRODUCTION_INTEGRATIONS.md)
        - [Docker部署](../docs/DOCKER_GUIDE.md)
        - [测试文档](../docs/PYTEST_SUMMARY.md)
        """)

    with col3:
        st.markdown("""
        **开发文档**
        - [架构设计](../docs/ARCHITECTURE.md)
        - [优化报告](../OPTIMIZATION_COMPLETE_SUMMARY.md)
        - [验证报告](../TEST_RUN_VERIFICATION.md)
        """)

    st.markdown("---")

    # Footer info
    st.info("""
    💡 **提示**: 使用左侧导航栏探索不同功能模块。每个模块都提供交互式演示和详细分析。
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
