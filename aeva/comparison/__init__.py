"""
AEVA Model Comparison Module

Provides multi-model comparison and A/B testing capabilities.

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from aeva.comparison.comparator import ModelComparator
from aeva.comparison.ab_test import ABTester
from aeva.comparison.regression import RegressionDetector
from aeva.comparison.champion import ChampionChallengerManager

__all__ = [
    'ModelComparator',
    'ABTester',
    'RegressionDetector',
    'ChampionChallengerManager',
]
