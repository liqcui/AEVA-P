"""
Data quality analysis page

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import numpy as np

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


def render():
    """Render data quality page"""

    st.markdown('<p class="main-header">📊 数据质量分析</p>', unsafe_allow_html=True)
    st.markdown("### 全面评估数据集质量")

    st.markdown("---")

    tabs = st.tabs(["📈 质量画像", "✅ 质量指标", "🔍 期望验证", "💻 代码示例"])

    with tabs[0]:
        render_profiling_tab()

    with tabs[1]:
        render_metrics_tab()

    with tabs[2]:
        render_expectations_tab()

    with tabs[3]:
        render_code_tab()


def render_profiling_tab():
    st.markdown("## 📈 数据画像分析")

    if st.button("🚀 运行数据画像", key="profiling"):
        with st.spinner("正在分析数据..."):
            try:
                from aeva.data_quality import DataProfiler
                from sklearn.datasets import load_breast_cancer

                data = load_breast_cancer()
                df = pd.DataFrame(data.data, columns=data.feature_names)

                profiler = DataProfiler()
                profile = profiler.profile_dataframe(df)

                st.success("✅ 数据画像完成!")

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("行数", profile.get('n_rows', 0))
                with col2:
                    st.metric("列数", profile.get('n_columns', 0))
                with col3:
                    st.metric("缺失值", profile.get('missing_cells', 0))
                with col4:
                    st.metric("重复行", profile.get('duplicate_rows', 0))

                st.markdown("### 列统计")
                if 'column_stats' in profile:
                    st.json(profile['column_stats'])

            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")


def render_metrics_tab():
    st.markdown("## ✅ 质量指标")

    if st.button("🚀 计算质量指标", key="metrics"):
        with st.spinner("正在计算..."):
            try:
                from aeva.data_quality import QualityMetrics
                from sklearn.datasets import load_breast_cancer

                data = load_breast_cancer()
                df = pd.DataFrame(data.data, columns=data.feature_names)

                # 使用静态方法计算整体指标
                completeness = QualityMetrics.completeness(df) / 100

                # 计算唯一性 (对第一列进行采样)
                uniqueness = QualityMetrics.uniqueness(df.iloc[:, 0]) / 100

                st.success("✅ 质量指标计算完成!")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("完整性", f"{completeness:.1%}")
                with col2:
                    st.metric("唯一性", f"{uniqueness:.1%}")
                with col3:
                    quality_score = (completeness + uniqueness) / 2 * 100
                    st.metric("综合质量分", f"{quality_score:.1f}/100")

                # 生成综合报告
                metrics_obj = QualityMetrics(df)
                report = metrics_obj.generate_quality_report()

                st.markdown("### 质量报告")
                st.metric("总体质量分", f"{report.overall_score:.1f}%")

                if report.dimension_scores:
                    st.markdown("#### 各维度评分")
                    for dim, score in report.dimension_scores.items():
                        st.write(f"- **{dim.value}**: {score.score:.1f}%")

            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")
                import traceback
                st.code(traceback.format_exc())


def render_expectations_tab():
    st.markdown("## 🔍 数据期望验证")

    st.markdown("""
    使用Great Expectations进行数据验证（需要安装great_expectations）

    **常用期望**:
    - ✅ 列存在性
    - ✅ 非空值
    - ✅ 值范围
    - ✅ 唯一性
    """)

    st.info("需要安装: pip install great_expectations")


def render_code_tab():
    st.markdown("## 💻 代码示例")

    st.markdown("### 数据画像")
    st.code("""
from aeva.data_quality import DataProfiler

# 数据画像
profiler = DataProfiler()
profile = profiler.profile_dataframe(df)
print(f"行数: {profile['n_rows']}")
print(f"列数: {profile['n_columns']}")
print(f"缺失值: {profile['missing_cells']}")
""", language="python")

    st.markdown("### 质量指标")
    st.code("""
from aeva.data_quality import QualityMetrics, OutlierMethod

# 静态方法 - 快速计算
completeness = QualityMetrics.completeness(df)  # 完整性
uniqueness = QualityMetrics.uniqueness(df['column_name'])  # 唯一性
validity = QualityMetrics.validity(df['age'], min_value=0, max_value=120)  # 有效性

# 创建实例 - 综合分析
metrics = QualityMetrics(df)

# 离群值检测
outliers = metrics.detect_outliers(method=OutlierMethod.IQR)
print(f"离群值数量: {outliers.outlier_count}")
print(f"离群值比例: {outliers.outlier_percentage:.2f}%")

# 分布分析
dist = metrics.analyze_distribution()
print(f"均值: {dist.mean:.2f}")
print(f"标准差: {dist.std:.2f}")
print(f"偏度: {dist.skewness:.2f}")

# 生成综合质量报告
report = metrics.generate_quality_report()
print(f"总体质量分: {report.overall_score:.2f}%")
for dim, score in report.dimension_scores.items():
    print(f"{dim.value}: {score.score:.2f}%")
""", language="python")
