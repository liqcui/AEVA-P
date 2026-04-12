"""
AEVA v2.0 Interactive Dashboard
Streamlit application for model evaluation and validation

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
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
    llm_evaluation,
    production_integrations,
    report_generation
)

# Import advanced feature pages
from aeva.dashboard.pages.advanced import benchmark, auto_pipeline, brain, guard

# Import i18n support
from aeva.dashboard.i18n import init_language, t, language_selector

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

# Initialize language
init_language()

# Sidebar navigation
st.sidebar.markdown("# 🤖 AEVA v2.0")
st.sidebar.markdown("### Algorithm Evaluation & Validation Agent")
st.sidebar.markdown("---")

# Page selection
page = st.sidebar.radio(
    "Navigation / 导航",
    [
        t("nav_home"),
        t("nav_explainability"),
        t("nav_robustness"),
        t("nav_data_quality"),
        t("nav_ab_testing"),
        t("nav_model_cards"),
        t("nav_llm_evaluation"),
        t("nav_production"),
        t("nav_report_generation")
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"### {t('system_info')}")
st.sidebar.info(f"""
**{t('version')}**: v2.0.0
**{t('status')}**: {t('status_ready')}
**{t('pages')}**: 9 {t('main_pages')} + 4 {t('advanced_features')}
**{t('modules')}**: 12 {t('core')} + 3 {t('integrations')}
**{t('test_coverage')}**: 65%
""")

# Check for sub-page navigation
if 'subpage' in st.session_state and st.session_state.subpage:
    # Render advanced feature sub-pages
    if st.session_state.subpage == "benchmark":
        benchmark.render()
    elif st.session_state.subpage == "auto":
        auto_pipeline.render()
    elif st.session_state.subpage == "brain":
        brain.render()
    elif st.session_state.subpage == "guard":
        guard.render()
else:
    # Normal page routing
    if page == t("nav_home"):
        home.render()
    elif page == t("nav_explainability"):
        explainability.render()
    elif page == t("nav_robustness"):
        robustness.render()
    elif page == t("nav_data_quality"):
        data_quality.render()
    elif page == t("nav_ab_testing"):
        ab_testing.render()
    elif page == t("nav_model_cards"):
        model_cards.render()
    elif page == t("nav_llm_evaluation"):
        llm_evaluation.render()
    elif page == t("nav_production"):
        production_integrations.render()
    elif page == t("nav_report_generation"):
        report_generation.render()

# Language selector
language_selector()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; color: #666;">
    <small>AEVA v2.0 © 2026</small>
</div>
""", unsafe_allow_html=True)


def main():
    """Main entry point for CLI"""
    import sys
    import os

    # This is called when running: aeva-dashboard or streamlit run app.py
    # Streamlit will handle the app automatically
    pass


if __name__ == "__main__":
    main()
