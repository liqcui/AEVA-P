"""
A/B testing page

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import streamlit as st
import sys
from pathlib import Path
import numpy as np
import pandas as pd

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


def render():
    """Render A/B testing page"""

    st.markdown('<p class="main-header">📈 A/B 测试</p>', unsafe_allow_html=True)
    st.markdown("### 统计检验与模型比较")

    st.markdown("---")

    tabs = st.tabs(["📊 模型对比", "🎯 统计检验", "📉 功效分析", "💻 代码示例"])

    with tabs[0]:
        render_comparison_tab()

    with tabs[1]:
        render_statistical_tab()

    with tabs[2]:
        render_power_tab()

    with tabs[3]:
        render_code_tab()


def render_comparison_tab():
    st.markdown("## 📊 模型性能对比")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 模型A")
        n_a = st.number_input("样本量", value=100, key="n_a")
        mean_a = st.number_input("平均准确率", value=0.85, key="mean_a")

    with col2:
        st.markdown("### 模型B")
        n_b = st.number_input("样本量", value=100, key="n_b")
        mean_b = st.number_input("平均准确率", value=0.88, key="mean_b")

    if st.button("🚀 运行对比测试", key="compare"):
        st.info(f"对比模型A ({mean_a:.1%}) vs 模型B ({mean_b:.1%})")

        # Simulate comparison
        scores_a = np.random.normal(mean_a, 0.05, n_a)
        scores_b = np.random.normal(mean_b, 0.05, n_b)

        try:
            from aeva.ab_testing import ABTester

            tester = ABTester()
            result = tester.compare(scores_a, scores_b)

            st.success("✅ 对比完成!")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("P值", f"{result.get('p_value', 0):.4f}")
            with col2:
                st.metric("效应量", f"{result.get('effect_size', 0):.4f}")
            with col3:
                significant = result.get('p_value', 1) < 0.05
                st.metric("显著性", "显著" if significant else "不显著")

        except Exception as e:
            st.error(f"❌ 错误: {str(e)}")


def render_statistical_tab():
    st.markdown("## 🎯 统计检验")

    st.markdown("""
    **支持的检验方法**:
    - t检验 (独立样本)
    - Welch t检验 (方差不等)
    - Mann-Whitney U检验 (非参数)
    - Wilcoxon检验 (配对样本)
    """)

    test_type = st.selectbox("选择检验方法", ["t-test", "welch", "mann-whitney", "wilcoxon"])

    st.info(f"选择的检验方法: {test_type}")


def render_power_tab():
    st.markdown("## 📉 统计功效分析")

    st.markdown("""
    计算达到期望统计功效所需的样本量。

    **需要安装**: `pip install statsmodels`
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        effect_size = st.number_input("效应量", value=0.5, min_value=0.1, max_value=2.0)

    with col2:
        alpha = st.number_input("显著性水平 (α)", value=0.05, min_value=0.01, max_value=0.1)

    with col3:
        power = st.number_input("统计功效 (1-β)", value=0.8, min_value=0.5, max_value=0.99)

    if st.button("🚀 计算样本量", key="power"):
        # Simple estimation (not actual statsmodels calculation)
        from scipy import stats
        estimated_n = int(16 * (power / (1 - alpha)) ** 2 / effect_size ** 2)

        st.success(f"✅ 估算每组需要样本量: **{estimated_n}**")
        st.info("精确计算需要安装statsmodels")


def render_code_tab():
    st.markdown("## 💻 代码示例")

    st.code("""
from aeva.ab_testing import ABTester, StatisticalTests

# 创建测试器
tester = ABTester()

# 对比两组
result = tester.compare(scores_a, scores_b)
print(f"P值: {result['p_value']}")
print(f"显著性: {result['significant']}")

# 统计检验
stats = StatisticalTests()
result = stats.t_test(group_a, group_b)
result = stats.mann_whitney_test(group_a, group_b)
""", language="python")
