"""
AEVA Fairness and Bias Detection Module

Provides fairness metrics, bias detection, and mitigation recommendations for ML models.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
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
