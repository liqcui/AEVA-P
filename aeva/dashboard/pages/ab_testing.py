"""
A/B testing page

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
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

            tester = ABTester(significance_level=0.05)
            result = tester.compare(
                scores_a.tolist(),
                scores_b.tolist(),
                variant_a_name="模型A",
                variant_b_name="模型B"
            )

            st.success("✅ 对比完成!")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("P值", f"{result.p_value:.4f}")
            with col2:
                st.metric("效应量", f"{result.effect_size:.4f}")
            with col3:
                st.metric("显著性", "显著 ✓" if result.statistically_significant else "不显著 ✗")
            with col4:
                st.metric("提升", f"{result.improvement_pct:+.2f}%")

        except Exception as e:
            st.error(f"❌ 错误: {str(e)}")
            import traceback
            st.code(traceback.format_exc())


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

    st.markdown("### 基本 A/B 测试")
    st.code("""
from aeva.ab_testing import ABTester

# 创建测试器
tester = ABTester(significance_level=0.05, power=0.8)

# 对比两组模型性能
result = tester.compare(
    scores_a.tolist(),
    scores_b.tolist(),
    variant_a_name="模型A",
    variant_b_name="模型B"
)

print(f"P值: {result.p_value:.4f}")
print(f"显著性: {result.statistically_significant}")
print(f"效应量: {result.effect_size:.4f}")
print(f"提升: {result.improvement_pct:+.2f}%")
print(f"胜者: {result.winner}")
""", language="python")

    st.markdown("### 统计检验")
    st.code("""
from aeva.ab_testing import StatisticalTest

# 创建统计检验对象
stat_test = StatisticalTest(significance_level=0.05)

# t检验
result = stat_test.t_test(group_a, group_b)
print(f"t统计量: {result.statistic:.4f}")
print(f"p值: {result.p_value:.4f}")
print(f"显著: {result.significant}")

# Mann-Whitney U检验 (非参数)
result = stat_test.mann_whitney_u(group_a, group_b)

# 效应量
cohens_d = stat_test.cohens_d(group_a, group_b)
print(f"Cohen's d: {cohens_d:.4f}")
""", language="python")

    st.markdown("### 序贯测试 (提前停止)")
    st.code("""
# 序贯A/B测试 - 可以提前停止以节省样本
result = tester.sequential_test(
    control_scores,
    treatment_scores,
    check_interval=200,
    min_samples=500,
    max_samples=5000
)

if result.status.value == "stopped_early":
    print(f"✓ 测试提前停止!")
    print(f"  节省样本: {5000 - result.variant_a_size}")
""", language="python")

    st.markdown("### 贝叶斯A/B测试")
    st.code("""
# 贝叶斯方法
result = tester.bayesian_test(
    control_data,
    treatment_data,
    prior_mean=0.05,
    prior_std=0.02
)

print(f"P(B优于A): {result.prob_b_better:.2%}")
print(f"期望损失: {result.expected_loss_a:.4f}")
""", language="python")
