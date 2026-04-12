"""
Quality Metrics

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""
import numpy as np

class QualityMetrics:
    """Data quality metrics"""
    
    @staticmethod
    def completeness(data: np.ndarray) -> float:
        """Calculate completeness"""
        if isinstance(data, np.ndarray):
            return 1.0 - np.isnan(data).sum() / data.size
        return 1.0
    
    @staticmethod
    def uniqueness(data: np.ndarray) -> float:
        """Calculate uniqueness"""
        if len(data.shape) == 1:
            return len(np.unique(data)) / len(data)
        return 1.0
    
    @staticmethod
    def validity(data: np.ndarray, min_val: float = 0, max_val: float = 1) -> float:
        """Calculate validity (values in range)"""
        valid = np.logical_and(data >= min_val, data <= max_val)
        return valid.sum() / data.size
