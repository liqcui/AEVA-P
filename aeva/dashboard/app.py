"""
AEVA v2.0 Interactive Dashboard
Streamlit application for model evaluation and validation
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import pages
from aeva.dashboard.pages import (
    home,
    explainability,
    robustness,
    data_quality,
    ab_testing,
    model_cards,
    production_integrations
)

# Page configuration
st.set_page_config(
    page_title="AEVA v2.0 Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-org/AVEA-P',
        'Report a bug': "https://github.com/your-org/AVEA-P/issues",
        'About': "# AEVA v2.0\nAlgorithm Evaluation & Validation Agent"
    }
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        color: #155724;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 0.25rem;
        padding: 1rem;
        color: #856404;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        color: #721c24;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.markdown("# 🤖 AEVA v2.0")
st.sidebar.markdown("### Algorithm Evaluation & Validation Agent")
st.sidebar.markdown("---")

# Page selection
page = st.sidebar.radio(
    "导航",
    [
        "🏠 主页",
        "🔍 可解释性分析",
        "🛡️ 对抗鲁棒性",
        "📊 数据质量",
        "📈 A/B 测试",
        "📝 模型卡片",
        "⚙️ 生产级集成"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 系统信息")
st.sidebar.info(f"""
**版本**: v2.0.0
**状态**: ✅ Production Ready
**模块**: 12 核心 + 3 集成
**测试覆盖**: 65%
""")

# Page routing
if page == "🏠 主页":
    home.render()
elif page == "🔍 可解释性分析":
    explainability.render()
elif page == "🛡️ 对抗鲁棒性":
    robustness.render()
elif page == "📊 数据质量":
    data_quality.render()
elif page == "📈 A/B 测试":
    ab_testing.render()
elif page == "📝 模型卡片":
    model_cards.render()
elif page == "⚙️ 生产级集成":
    production_integrations.render()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; color: #666;">
    <small>AEVA v2.0 © 2026</small>
</div>
""", unsafe_allow_html=True)
