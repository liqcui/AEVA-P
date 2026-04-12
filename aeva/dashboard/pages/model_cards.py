"""
Model cards page

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import streamlit as st
import sys
from pathlib import Path
import json

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


def render():
    """Render model cards page"""

    st.markdown('<p class="main-header">📝 模型卡片生成</p>', unsafe_allow_html=True)
    st.markdown("### 自动化模型文档与合规")

    st.markdown("---")

    tabs = st.tabs(["📄 生成卡片", "✅ 验证卡片", "📋 模板", "💻 代码示例"])

    with tabs[0]:
        render_generation_tab()

    with tabs[1]:
        render_validation_tab()

    with tabs[2]:
        render_templates_tab()

    with tabs[3]:
        render_code_tab()


def render_generation_tab():
    st.markdown("## 📄 生成模型卡片")

    with st.form("model_card_form"):
        st.markdown("### 基本信息")

        model_name = st.text_input("模型名称", "Breast Cancer Classifier")
        model_version = st.text_input("版本", "1.0.0")
        model_type = st.selectbox("模型类型", ["分类", "回归", "聚类", "其他"])

        st.markdown("### 性能指标")

        accuracy = st.number_input("准确率", value=0.95, min_value=0.0, max_value=1.0)
        precision = st.number_input("精确率", value=0.94, min_value=0.0, max_value=1.0)
        recall = st.number_input("召回率", value=0.96, min_value=0.0, max_value=1.0)

        st.markdown("### 用途与限制")

        intended_use = st.text_area("预期用途", "用于乳腺癌早期筛查辅助诊断")
        limitations = st.text_area("已知限制", "仅供辅助参考，最终诊断需要医生判断")

        submitted = st.form_submit_button("🚀 生成模型卡片")

        if submitted:
            try:
                from aeva.model_cards import ModelCardGenerator, ModelType, PerformanceMetrics

                # 创建性能指标对象
                perf_metrics = PerformanceMetrics(
                    primary_metric="accuracy",
                    metrics={
                        "accuracy": accuracy,
                        "precision": precision,
                        "recall": recall,
                        "f1_score": 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
                    }
                )

                # 映射模型类型
                type_map = {
                    "分类": ModelType.CLASSIFIER,
                    "回归": ModelType.REGRESSOR,
                    "聚类": ModelType.CLUSTERING,
                    "其他": ModelType.CLASSIFIER
                }

                generator = ModelCardGenerator(model_name=model_name)

                card = generator.generate_card(
                    model_version=model_version,
                    model_type=type_map.get(model_type, ModelType.CLASSIFIER),
                    performance_metrics=perf_metrics,
                    intended_use=intended_use,
                    limitations=limitations
                )

                st.success("✅ 模型卡片生成成功!")

                # Display card - convert to dict for JSON display
                from dataclasses import asdict
                try:
                    card_dict = asdict(card)
                    # Convert enums to strings
                    if 'model_type' in card_dict and hasattr(card_dict['model_type'], 'value'):
                        card_dict['model_type'] = card_dict['model_type'].value
                except:
                    card_dict = {
                        "model_name": card.model_name,
                        "model_version": card.model_version,
                        "model_type": card.model_type.value if hasattr(card.model_type, 'value') else str(card.model_type),
                        "intended_use": card.intended_use,
                        "limitations": card.limitations
                    }

                st.markdown("### 生成的模型卡片")
                st.json(card_dict)

                # Download
                card_json = json.dumps(card_dict, indent=2, ensure_ascii=False, default=str)
                st.download_button(
                    label="📥 下载模型卡片 (JSON)",
                    data=card_json,
                    file_name="model_card.json",
                    mime="application/json"
                )

                # Export to HTML
                html_path = generator.export_html(card, "/tmp/model_card.html")
                st.info(f"HTML导出至: {html_path}")

            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")
                import traceback
                st.code(traceback.format_exc())


def render_validation_tab():
    st.markdown("## ✅ 验证模型卡片")

    uploaded_file = st.file_uploader("上传模型卡片 (JSON)", type=['json'])

    if uploaded_file is not None:
        try:
            from aeva.model_cards import ModelCardValidator

            card_data = json.load(uploaded_file)

            validator = ModelCardValidator()
            report = validator.validate(card_data)

            if report.is_valid:
                st.success("✅ 模型卡片验证通过!")
                st.metric("完整性评分", f"{report.completeness_score:.1f}%")
                st.json(card_data)
            else:
                st.error(f"❌ 验证失败 - 完整性: {report.completeness_score:.1f}%")

                st.markdown("### 验证问题")
                for issue in report.issues:
                    if issue.level.value == "error":
                        st.error(f"❌ {issue.message}")
                    elif issue.level.value == "warning":
                        st.warning(f"⚠️ {issue.message}")
                    else:
                        st.info(f"ℹ️ {issue.message}")

        except Exception as e:
            st.error(f"❌ 错误: {str(e)}")
            import traceback
            st.code(traceback.format_exc())


def render_templates_tab():
    st.markdown("## 📋 模型卡片模板")

    st.markdown("""
    模型卡片包含以下标准字段:

    ### 基本信息
    - 模型名称
    - 版本号
    - 模型类型
    - 创建日期

    ### 性能指标
    - 准确率
    - 精确率
    - 召回率
    - F1分数
    - AUC-ROC

    ### 用途
    - 预期用途
    - 应用场景
    - 目标用户

    ### 限制
    - 已知限制
    - 不适用场景
    - 伦理考虑

    ### 合规性
    - EU AI Act
    - FDA要求
    - 数据隐私
    """)


def render_code_tab():
    st.markdown("## 💻 代码示例")

    st.markdown("### 生成模型卡片")
    st.code("""
from aeva.model_cards import (
    ModelCardGenerator,
    ModelType,
    PerformanceMetrics,
    FairnessMetrics
)

# 创建性能指标
perf_metrics = PerformanceMetrics(
    primary_metric="accuracy",
    metrics={
        "accuracy": 0.95,
        "precision": 0.94,
        "recall": 0.96,
        "f1_score": 0.95
    },
    test_set_size=10000
)

# 创建公平性指标
fairness = FairnessMetrics(
    demographic_parity=0.95,
    equal_opportunity=0.92,
    protected_attributes=["age", "gender"]
)

# 生成模型卡片
generator = ModelCardGenerator(model_name="Medical Diagnosis Model")
card = generator.generate_card(
    model_version="1.0.0",
    model_type=ModelType.CLASSIFIER,
    performance_metrics=perf_metrics,
    fairness_metrics=fairness,
    intended_use="医疗诊断辅助",
    limitations="仅供参考，需要医生确认",
    ethical_considerations="已考虑公平性和隐私保护"
)

# 导出多种格式
generator.export_json(card, "model_card.json")
generator.export_markdown(card, "model_card.md")
generator.export_html(card, "model_card.html")
""", language="python")

    st.markdown("### 验证模型卡片")
    st.code("""
from aeva.model_cards import ModelCardValidator

# 验证模型卡片
validator = ModelCardValidator()
card_dict = {...}  # 从JSON加载的模型卡片

report = validator.validate(card_dict)

if report.is_valid:
    print("✓ 验证通过!")
    print(f"完整性评分: {report.completeness_score:.1f}%")
else:
    print("✗ 验证失败")
    for issue in report.issues:
        print(f"[{issue.level.value}] {issue.message}")
""", language="python")
