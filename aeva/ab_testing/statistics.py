"""
Statistical Tests

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""
from scipy import stats
import numpy as np

class StatisticalTest:
    """Statistical testing utilities"""
    
    @staticmethod
    def t_test(group_a: list, group_b: list) -> tuple:
        """Perform t-test"""
        return stats.ttest_ind(group_a, group_b)
    
    @staticmethod
    def chi_square(observed: list, expected: list) -> tuple:
        """Perform chi-square test"""
        return stats.chisquare(observed, expected)
    
    @staticmethod
    def effect_size(group_a: list, group_b: list) -> float:
        """Cohen's d effect size"""
        mean_diff = np.mean(group_a) - np.mean(group_b)
        pooled_std = np.sqrt((np.std(group_a)**2 + np.std(group_b)**2) / 2)
        return mean_diff / pooled_std if pooled_std > 0 else 0
