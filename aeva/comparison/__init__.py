"""
AEVA Model Comparison Module

Provides multi-model comparison and A/B testing capabilities.
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
