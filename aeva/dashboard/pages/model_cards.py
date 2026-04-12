"""
Model cards page

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
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
                from aeva.model_cards import ModelCardGenerator

                generator = ModelCardGenerator(model_name)

                card = generator.generate_card(
                    model_version=model_version,
                    model_type=model_type,
                    performance_metrics={
                        "accuracy": accuracy,
                        "precision": precision,
                        "recall": recall
                    },
                    intended_use=intended_use,
                    limitations=limitations
                )

                st.success("✅ 模型卡片生成成功!")

                # Display card
                st.markdown("### 生成的模型卡片")
                st.json(card)

                # Download
                card_json = json.dumps(card, indent=2, ensure_ascii=False)
                st.download_button(
                    label="📥 下载模型卡片 (JSON)",
                    data=card_json,
                    file_name="model_card.json",
                    mime="application/json"
                )

            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")


def render_validation_tab():
    st.markdown("## ✅ 验证模型卡片")

    uploaded_file = st.file_uploader("上传模型卡片 (JSON)", type=['json'])

    if uploaded_file is not None:
        try:
            from aeva.model_cards import ModelCardValidator

            card_data = json.load(uploaded_file)

            validator = ModelCardValidator()
            is_valid, errors = validator.validate(card_data)

            if is_valid:
                st.success("✅ 模型卡片验证通过!")
                st.json(card_data)
            else:
                st.error("❌ 验证失败")
                for error in errors:
                    st.warning(f"⚠️ {error}")

        except Exception as e:
            st.error(f"❌ 错误: {str(e)}")


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

    st.code("""
from aeva.model_cards import ModelCardGenerator, ModelCardValidator

# 生成模型卡片
generator = ModelCardGenerator("My Model")
card = generator.generate_card(
    model_version="1.0.0",
    model_type="classification",
    performance_metrics={
        "accuracy": 0.95,
        "precision": 0.94,
        "recall": 0.96
    },
    intended_use="医疗诊断辅助",
    limitations="仅供参考，需要医生确认"
)

# 保存卡片
generator.save_card(card, "model_card.json")

# 验证卡片
validator = ModelCardValidator()
is_valid, errors = validator.validate(card)
""", language="python")
