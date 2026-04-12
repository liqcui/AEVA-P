"""
AEVA Integrations Module

Provides production-grade library integrations while maintaining API compatibility.

Available integrations:
- ART (Adversarial Robustness Toolbox) for robustness testing
- Great Expectations for data quality
- statsmodels for advanced statistical testing
- SHAP optimizations for parallel computation
"""

from .robustness_art import ARTRobustnessTester
from .data_quality_ge import GreatExpectationsProfiler
from .statistics_sm import StatsModelsABTest

__all__ = [
    'ARTRobustnessTester',
    'GreatExpectationsProfiler',
    'StatsModelsABTest'
]
