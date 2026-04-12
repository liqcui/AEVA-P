"""Production integrations page"""

import streamlit as st
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


def render():
    """Render production integrations page"""

    st.markdown('<p class="main-header">⚙️ 生产级集成</p>', unsafe_allow_html=True)
    st.markdown("### ART, Great Expectations, statsmodels")

    st.markdown("---")

    # Check library availability
    libs_status = check_libraries()

    # Display status
    st.markdown("## 📦 库状态")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### ART")
        if libs_status['art']:
            st.success("✅ 已安装")
            st.info("40+ 攻击方法可用")
        else:
            st.warning("⚠️ 未安装")
            st.code("pip install adversarial-robustness-toolbox")

    with col2:
        st.markdown("### Great Expectations")
        if libs_status['ge']:
            st.success("✅ 已安装")
            st.info("50+ 数据期望可用")
        else:
            st.warning("⚠️ 未安装")
            st.code("pip install great_expectations")

    with col3:
        st.markdown("### statsmodels")
        if libs_status['sm']:
            st.success("✅ 已安装")
            st.info("贝叶斯检验可用")
        else:
            st.warning("⚠️ 未安装")
            st.code("pip install statsmodels")

    st.markdown("---")

    # Tabs for each integration
    tabs = st.tabs(["🛡️ ART集成", "📊 GE集成", "📈 statsmodels集成", "💻 代码示例"])

    with tabs[0]:
        render_art_tab(libs_status['art'])

    with tabs[1]:
        render_ge_tab(libs_status['ge'])

    with tabs[2]:
        render_sm_tab(libs_status['sm'])

    with tabs[3]:
        render_code_tab()


def check_libraries():
    """Check if production libraries are installed"""
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

    return status


def render_art_tab(is_available):
    st.markdown("## 🛡️ ART (Adversarial Robustness Toolbox)")

    st.markdown("""
    IBM Research开发的对抗鲁棒性工具包。

    **功能提升**:
    - 攻击方法: 3 → 40+ (13x)
    - 性能: 2-3x 提升
    - GPU加速: 支持
    - 防御方法: 10+ 可用

    **主要攻击**:
    - FGSM, PGD, BIM (基础)
    - Carlini & Wagner L2 (强力)
    - DeepFool (最小扰动)
    - Boundary Attack (黑盒)
    """)

    if is_available:
        if st.button("🚀 运行ART演示", key="art_demo"):
            st.info("ART集成演示")
            st.code("""
from aeva.integrations import ARTRobustnessTester

tester = ARTRobustnessTester(model, input_shape, num_classes)
results = tester.comprehensive_test(X_test, y_test)
report = tester.generate_robustness_report(results)
""", language="python")
    else:
        st.warning("请先安装ART以使用完整功能")


def render_ge_tab(is_available):
    st.markdown("## 📊 Great Expectations")

    st.markdown("""
    企业级数据验证与文档工具。

    **功能提升**:
    - 期望类型: 5 → 50+ (10x)
    - 报告: 文本 → 专业HTML
    - 自动化: 支持完整pipeline
    - 集成: Airflow, dbt等

    **常用期望**:
    - expect_column_values_to_not_be_null
    - expect_column_values_to_be_between
    - expect_column_mean_to_be_between
    - expect_table_row_count_to_be_between
    """)

    if is_available:
        if st.button("🚀 运行GE演示", key="ge_demo"):
            st.info("Great Expectations集成演示")
            st.code("""
from aeva.integrations import GreatExpectationsProfiler

profiler = GreatExpectationsProfiler()
profile = profiler.profile_dataframe(df)
validation = profiler.validate(df, profile)
docs = profiler.generate_data_docs(profile)
""", language="python")
    else:
        st.warning("请先安装Great Expectations以使用完整功能")


def render_sm_tab(is_available):
    st.markdown("## 📈 statsmodels")

    st.markdown("""
    Python统计建模库，提供高级统计分析。

    **功能提升**:
    - 统计方法: 20+ → 100+ (5x)
    - 贝叶斯A/B测试: 新增
    - 功效分析: 新增
    - 序贯检验: 新增

    **主要功能**:
    - 精确统计检验
    - 贝叶斯推断
    - 样本量计算
    - 置信区间计算
    """)

    if is_available:
        if st.button("🚀 运行statsmodels演示", key="sm_demo"):
            st.info("statsmodels集成演示")
            st.code("""
from aeva.integrations import StatsModelsABTest

tester = StatsModelsABTest()

# 高级A/B测试
result = tester.advanced_ab_test(scores_a, scores_b)

# 贝叶斯A/B测试
bayesian = tester.bayesian_ab_test(scores_a, scores_b)

# 功效分析
power = tester.power_analysis(effect_size=0.5, alpha=0.05, power=0.8)
""", language="python")
    else:
        st.warning("请先安装statsmodels以使用完整功能")


def render_code_tab():
    st.markdown("## 💻 安装与使用")

    st.markdown("### 安装生产级库")

    st.code("""
# 安装所有库
pip install adversarial-robustness-toolbox great_expectations statsmodels

# 或单独安装
pip install adversarial-robustness-toolbox  # ART
pip install great_expectations              # GE
pip install statsmodels                      # statsmodels
""", language="bash")

    st.markdown("---")

    st.markdown("### 使用示例")

    st.code("""
# 1. ART集成
from aeva.integrations import ARTRobustnessTester

tester = ARTRobustnessTester(model, input_shape=(30,), num_classes=2)

# 多种攻击测试
results = tester.comprehensive_test(
    X_test, y_test,
    attacks=['fgsm', 'pgd', 'carlini'],
    epsilon_values=[0.05, 0.1, 0.2]
)

# 生成报告
report = tester.generate_robustness_report(results)

# ---

# 2. Great Expectations集成
from aeva.integrations import GreatExpectationsProfiler

profiler = GreatExpectationsProfiler()

# 自动分析
profile = profiler.profile_dataframe(df, dataset_name="my_data")

# 验证数据
validation = profiler.validate(df, profile)

# 生成HTML文档
docs_path = profiler.generate_data_docs(profile, "./report.html")

# ---

# 3. statsmodels集成
from aeva.integrations import StatsModelsABTest

tester = StatsModelsABTest()

# 高级A/B测试（含效应量和CI）
result = tester.advanced_ab_test(scores_a, scores_b)
print(f"Effect size: {result['effect_size']}")
print(f"95% CI: {result['confidence_interval']}")

# 贝叶斯A/B测试
bayesian = tester.bayesian_ab_test(scores_a, scores_b)
print(f"P(B > A) = {bayesian['prob_b_better_than_a']:.2%}")

# 功效分析（样本量计算）
power = tester.power_analysis(
    effect_size=0.5,  # Cohen's d
    alpha=0.05,       # 显著性水平
    power=0.8         # 统计功效
)
print(f"Required sample size: {power['n1_required']} per group")

# 序贯检验（可提前停止）
sequential = tester.sequential_testing(scores_a, scores_b)
if sequential['decision'] == 'stop':
    print("Can stop testing early!")
""", language="python")

    st.markdown("---")

    st.markdown("### Fallback机制")

    st.info("""
    **智能回退**: 当生产级库未安装时，AEVA会自动使用基础实现。

    - ✅ 100% API兼容
    - ✅ 无需修改代码
    - ✅ 清晰的日志提示
    - ✅ 渐进式升级路径

    **开发环境**: 使用Fallback即可快速开发
    **生产环境**: 强烈推荐安装所有生产级库
    """)
