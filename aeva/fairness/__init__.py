"""
AEVA Fairness and Bias Detection Module

Provides fairness metrics, bias detection, and mitigation recommendations for ML models.
"""

from aeva.fairness.metrics import FairnessMetrics, BiasMetrics
from aeva.fairness.detector import BiasDetector, FairnessAnalyzer
from aeva.fairness.report import FairnessReport, FairnessReportGenerator
from aeva.fairness.mitigation import BiasMitigation, FairnessOptimizer

__all__ = [
    'FairnessMetrics',
    'BiasMetrics',
    'BiasDetector',
    'FairnessAnalyzer',
    'FairnessReport',
    'FairnessReportGenerator',
    'BiasMitigation',
    'FairnessOptimizer',
]
