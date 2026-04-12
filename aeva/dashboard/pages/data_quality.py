"""
Data quality analysis page

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
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

                metrics = QualityMetrics(df)
                completeness = metrics.completeness()
                uniqueness = metrics.uniqueness()

                st.success("✅ 质量指标计算完成!")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("完整性", f"{completeness:.1%}")
                with col2:
                    st.metric("唯一性", f"{uniqueness:.1%}")

                quality_score = (completeness + uniqueness) / 2 * 100
                st.metric("综合质量分", f"{quality_score:.1f}/100")

            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")


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

    st.code("""
from aeva.data_quality import DataProfiler, QualityMetrics

# 数据画像
profiler = DataProfiler()
profile = profiler.profile_dataframe(df)
print(profile)

# 质量指标
metrics = QualityMetrics(df)
completeness = metrics.completeness()
uniqueness = metrics.uniqueness()
validity = metrics.validity()
""", language="python")
