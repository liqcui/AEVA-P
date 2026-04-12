"""
AEVA Explainability Module

Provides model interpretability and explainability capabilities including:
- SHAP (SHapley Additive exPlanations) integration
- LIME (Local Interpretable Model-agnostic Explanations)
- Feature importance analysis
- Counterfactual explanations
- Explanation visualization and reporting

Compliance:
- EU AI Act (explainability for high-risk systems)
- FDA medical device requirements
- Financial services regulations
"""

from aeva.explainability.shap_explainer import (
    SHAPExplainer,
    SHAPExplanation,
    SHAPExplainerType
)
from aeva.explainability.lime_explainer import (
    LIMEExplainer,
    LIMEExplanation
)
from aeva.explainability.feature_importance import (
    FeatureImportanceAnalyzer,
    FeatureImportance
)
from aeva.explainability.visualizations import (
    ExplanationVisualizer,
    plot_shap_summary,
    plot_shap_waterfall,
    plot_lime_explanation,
    plot_feature_importance
)
from aeva.explainability.report_generator import (
    ExplanationReport,
    ExplanationReportGenerator
)

__all__ = [
    # SHAP
    'SHAPExplainer',
    'SHAPExplanation',
    'SHAPExplainerType',

    # LIME
    'LIMEExplainer',
    'LIMEExplanation',

    # Feature Importance
    'FeatureImportanceAnalyzer',
    'FeatureImportance',

    # Visualizations
    'ExplanationVisualizer',
    'plot_shap_summary',
    'plot_shap_waterfall',
    'plot_lime_explanation',
    'plot_feature_importance',

    # Reporting
    'ExplanationReport',
    'ExplanationReportGenerator',
]

__version__ = '1.0.0'
