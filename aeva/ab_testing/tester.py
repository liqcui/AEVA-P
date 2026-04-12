"""
A/B Tester

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""
import logging
import numpy as np
from dataclasses import dataclass
from typing import List, Optional

logger = logging.getLogger(__name__)

@dataclass
class ABTestResult:
    """A/B test results"""
    variant_a_mean: float
    variant_b_mean: float
    p_value: float
    statistically_significant: bool
    improvement_pct: float
    winner: str

class ABTester:
    """A/B testing framework"""
    
    def __init__(self, significance_level: float = 0.05):
        self.significance_level = significance_level
    
    def compare(
        self,
        variant_a_scores: List[float],
        variant_b_scores: List[float],
        variant_a_name: str = "A",
        variant_b_name: str = "B"
    ) -> ABTestResult:
        """Compare two variants"""
        from scipy import stats
        
        mean_a = np.mean(variant_a_scores)
        mean_b = np.mean(variant_b_scores)
        
        # T-test
        t_stat, p_value = stats.ttest_ind(variant_a_scores, variant_b_scores)
        
        is_significant = p_value < self.significance_level
        improvement = ((mean_b - mean_a) / mean_a * 100) if mean_a != 0 else 0
        
        winner = variant_b_name if mean_b > mean_a else variant_a_name
        
        return ABTestResult(
            variant_a_mean=mean_a,
            variant_b_mean=mean_b,
            p_value=p_value,
            statistically_significant=is_significant,
            improvement_pct=improvement,
            winner=winner
        )
