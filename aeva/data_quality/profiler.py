"""Data Profiler"""
import logging
import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, Any

logger = logging.getLogger(__name__)

@dataclass
class DataProfile:
    """Data profiling results"""
    n_samples: int
    n_features: int
    missing_pct: float
    duplicate_pct: float
    quality_score: float
    statistics: Dict[str, Any]

class DataProfiler:
    """Profile data quality"""
    
    def profile(self, data: np.ndarray) -> DataProfile:
        """Profile dataset"""
        if isinstance(data, np.ndarray):
            df = pd.DataFrame(data)
        else:
            df = data
        
        n_samples, n_features = df.shape
        missing_pct = df.isnull().sum().sum() / (n_samples * n_features) * 100
        duplicate_pct = df.duplicated().sum() / n_samples * 100
        
        # Simple quality score
        quality_score = 100 - missing_pct - duplicate_pct
        quality_score = max(0, min(100, quality_score))
        
        return DataProfile(
            n_samples=n_samples,
            n_features=n_features,
            missing_pct=missing_pct,
            duplicate_pct=duplicate_pct,
            quality_score=quality_score,
            statistics={
                "mean": df.mean().to_dict() if hasattr(df.mean(), 'to_dict') else {},
                "std": df.std().to_dict() if hasattr(df.std(), 'to_dict') else {}
            }
        )
