"""
Quality Metrics

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""
import logging
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Union, Tuple
from enum import Enum
from datetime import datetime, timedelta
from scipy import stats

logger = logging.getLogger(__name__)


class QualityDimension(Enum):
    """Data quality dimensions"""
    COMPLETENESS = "completeness"
    UNIQUENESS = "uniqueness"
    VALIDITY = "validity"
    ACCURACY = "accuracy"
    CONSISTENCY = "consistency"
    TIMELINESS = "timeliness"


class OutlierMethod(Enum):
    """Outlier detection methods"""
    IQR = "iqr"
    Z_SCORE = "z_score"
    ISOLATION_FOREST = "isolation_forest"
    MODIFIED_Z_SCORE = "modified_z_score"


@dataclass
class QualityScore:
    """Quality score for a dimension"""
    dimension: QualityDimension
    score: float
    details: Dict[str, Any] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class OutlierAnalysis:
    """Outlier detection results"""
    outlier_indices: np.ndarray
    outlier_count: int
    outlier_percentage: float
    method: OutlierMethod
    threshold: float
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DistributionAnalysis:
    """Statistical distribution analysis"""
    mean: float
    median: float
    std: float
    min: float
    max: float
    quartiles: Tuple[float, float, float]
    skewness: float
    kurtosis: float
    distribution_type: str = "unknown"
    normality_test_p_value: Optional[float] = None


@dataclass
class QualityReport:
    """Comprehensive data quality report"""
    overall_score: float
    dimension_scores: Dict[QualityDimension, QualityScore] = field(default_factory=dict)
    distribution_analysis: Optional[DistributionAnalysis] = None
    outlier_analysis: Optional[OutlierAnalysis] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_summary(self) -> str:
        """Get quality report summary"""
        summary = [f"Data Quality Report - Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"]
        summary.append(f"Overall Quality Score: {self.overall_score:.2%}")
        summary.append("\nDimension Scores:")
        for dim, score in self.dimension_scores.items():
            summary.append(f"  - {dim.value.title()}: {score.score:.2%}")
        return "\n".join(summary)


class QualityMetrics:
    """Comprehensive data quality metrics"""

    def __init__(self, data: Union[np.ndarray, pd.DataFrame, pd.Series]):
        """Initialize quality metrics calculator

        Args:
            data: Input data (numpy array, pandas DataFrame or Series)
        """
        if isinstance(data, pd.DataFrame):
            self.data = data
            self.is_dataframe = True
        elif isinstance(data, pd.Series):
            self.data = data.to_frame()
            self.is_dataframe = True
        else:
            self.data = np.asarray(data)
            self.is_dataframe = False

    @staticmethod
    def completeness(data: Union[np.ndarray, pd.DataFrame, pd.Series]) -> float:
        """Calculate completeness (non-missing data ratio)

        Args:
            data: Input data

        Returns:
            Completeness score from 0.0 to 1.0
        """
        if isinstance(data, pd.DataFrame):
            total = data.size
            non_null = data.count().sum()
            return non_null / total if total > 0 else 0.0
        elif isinstance(data, pd.Series):
            return data.count() / len(data) if len(data) > 0 else 0.0
        elif isinstance(data, np.ndarray):
            if data.dtype.kind in ['O', 'U', 'S']:  # Object or string types
                non_null = np.sum(pd.notna(data))
            else:
                non_null = np.sum(~np.isnan(data))
            return non_null / data.size if data.size > 0 else 0.0
        return 1.0

    @staticmethod
    def uniqueness(data: Union[np.ndarray, pd.Series]) -> float:
        """Calculate uniqueness (ratio of unique values)

        Args:
            data: Input data

        Returns:
            Uniqueness score from 0.0 to 1.0
        """
        if isinstance(data, pd.Series):
            total = len(data)
            unique = data.nunique()
        elif isinstance(data, np.ndarray):
            if len(data.shape) == 1:
                total = len(data)
                unique = len(np.unique(data))
            else:
                # For multidimensional arrays, flatten first
                flat = data.flatten()
                total = len(flat)
                unique = len(np.unique(flat))
        else:
            return 1.0

        return unique / total if total > 0 else 0.0

    @staticmethod
    def validity(
        data: Union[np.ndarray, pd.Series],
        min_val: Optional[float] = None,
        max_val: Optional[float] = None,
        allowed_values: Optional[List[Any]] = None,
        pattern: Optional[str] = None
    ) -> float:
        """Calculate validity (values meeting specified constraints)

        Args:
            data: Input data
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            allowed_values: List of allowed categorical values
            pattern: Regex pattern for string validation

        Returns:
            Validity score from 0.0 to 1.0
        """
        if isinstance(data, pd.Series):
            arr = data.values
        else:
            arr = np.asarray(data)

        total = len(arr)
        if total == 0:
            return 1.0

        valid_count = total

        # Range validation
        if min_val is not None:
            valid_count = np.sum(arr >= min_val)

        if max_val is not None:
            if min_val is not None:
                valid_count = np.sum((arr >= min_val) & (arr <= max_val))
            else:
                valid_count = np.sum(arr <= max_val)

        # Categorical validation
        if allowed_values is not None:
            valid_count = np.sum(np.isin(arr, allowed_values))

        # Pattern validation
        if pattern is not None and isinstance(data, pd.Series):
            import re
            valid_count = data.astype(str).str.match(pattern).sum()

        return valid_count / total

    def accuracy(
        self,
        reference_data: Union[np.ndarray, pd.Series],
        tolerance: float = 0.01
    ) -> float:
        """Calculate accuracy against reference data

        Args:
            reference_data: Ground truth or reference values
            tolerance: Acceptable relative difference for continuous values

        Returns:
            Accuracy score from 0.0 to 1.0
        """
        if isinstance(self.data, pd.DataFrame):
            data = self.data.iloc[:, 0].values
        else:
            data = self.data.flatten()

        if isinstance(reference_data, pd.Series):
            reference = reference_data.values
        else:
            reference = np.asarray(reference_data).flatten()

        # Ensure same length
        min_len = min(len(data), len(reference))
        data = data[:min_len]
        reference = reference[:min_len]

        if len(data) == 0:
            return 0.0

        # Check data type
        if np.issubdtype(data.dtype, np.number) and np.issubdtype(reference.dtype, np.number):
            # Numerical accuracy
            diff = np.abs(data - reference)
            max_val = np.maximum(np.abs(data), np.abs(reference))
            relative_diff = np.divide(diff, max_val, where=max_val != 0, out=np.zeros_like(diff))
            accurate = np.sum(relative_diff <= tolerance)
        else:
            # Categorical accuracy
            accurate = np.sum(data == reference)

        return accurate / len(data)

    def consistency(self, column_pairs: Optional[List[Tuple[str, str]]] = None) -> float:
        """Calculate consistency across related fields

        Args:
            column_pairs: List of column pairs to check for consistency

        Returns:
            Consistency score from 0.0 to 1.0
        """
        if not self.is_dataframe:
            logger.warning("Consistency check requires DataFrame input")
            return 1.0

        if column_pairs is None:
            # Auto-detect numerical columns for basic consistency check
            num_cols = self.data.select_dtypes(include=[np.number]).columns
            if len(num_cols) < 2:
                return 1.0
            column_pairs = [(num_cols[0], num_cols[1])]

        consistency_scores = []

        for col1, col2 in column_pairs:
            if col1 not in self.data.columns or col2 not in self.data.columns:
                continue

            # Check for logical consistency
            data1 = self.data[col1].dropna()
            data2 = self.data[col2].dropna()

            # Simple correlation-based consistency for numeric data
            if np.issubdtype(data1.dtype, np.number) and np.issubdtype(data2.dtype, np.number):
                common_idx = data1.index.intersection(data2.index)
                if len(common_idx) > 1:
                    corr = np.corrcoef(data1.loc[common_idx], data2.loc[common_idx])[0, 1]
                    consistency_scores.append(abs(corr))
            else:
                # Categorical consistency (matching values)
                common_idx = data1.index.intersection(data2.index)
                if len(common_idx) > 0:
                    matches = (data1.loc[common_idx] == data2.loc[common_idx]).sum()
                    consistency_scores.append(matches / len(common_idx))

        return np.mean(consistency_scores) if consistency_scores else 1.0

    def timeliness(
        self,
        timestamp_column: Optional[str] = None,
        max_age_days: int = 30,
        timestamp_data: Optional[Union[pd.Series, List[datetime]]] = None
    ) -> float:
        """Calculate timeliness of data

        Args:
            timestamp_column: Name of timestamp column in DataFrame
            max_age_days: Maximum acceptable age in days
            timestamp_data: Explicit timestamp data if not using column

        Returns:
            Timeliness score from 0.0 to 1.0
        """
        if timestamp_data is not None:
            timestamps = pd.to_datetime(timestamp_data)
        elif self.is_dataframe and timestamp_column and timestamp_column in self.data.columns:
            timestamps = pd.to_datetime(self.data[timestamp_column])
        else:
            logger.warning("No timestamp data provided for timeliness check")
            return 1.0

        now = pd.Timestamp.now()
        max_age = pd.Timedelta(days=max_age_days)

        # Calculate age of each record
        ages = now - timestamps
        timely = (ages <= max_age).sum()

        return timely / len(timestamps) if len(timestamps) > 0 else 0.0

    def detect_outliers(
        self,
        method: OutlierMethod = OutlierMethod.IQR,
        threshold: float = 1.5,
        column: Optional[str] = None
    ) -> OutlierAnalysis:
        """Detect outliers in data

        Args:
            method: Outlier detection method
            threshold: Threshold parameter (meaning depends on method)
            column: Specific column for DataFrame (uses first numeric column if None)

        Returns:
            OutlierAnalysis results
        """
        # Get data to analyze
        if self.is_dataframe:
            if column:
                data = self.data[column].values
            else:
                # Use first numeric column
                num_cols = self.data.select_dtypes(include=[np.number]).columns
                if len(num_cols) == 0:
                    return OutlierAnalysis(
                        outlier_indices=np.array([]),
                        outlier_count=0,
                        outlier_percentage=0.0,
                        method=method,
                        threshold=threshold
                    )
                data = self.data[num_cols[0]].values
        else:
            data = self.data.flatten()

        # Remove NaN values
        clean_data = data[~np.isnan(data)]

        if len(clean_data) == 0:
            return OutlierAnalysis(
                outlier_indices=np.array([]),
                outlier_count=0,
                outlier_percentage=0.0,
                method=method,
                threshold=threshold
            )

        # Apply detection method
        if method == OutlierMethod.IQR:
            outlier_mask = self._outliers_iqr(clean_data, threshold)
            details = {"method_description": "Interquartile Range (IQR) method"}

        elif method == OutlierMethod.Z_SCORE:
            outlier_mask = self._outliers_zscore(clean_data, threshold)
            details = {"method_description": "Z-score method"}

        elif method == OutlierMethod.MODIFIED_Z_SCORE:
            outlier_mask = self._outliers_modified_zscore(clean_data, threshold)
            details = {"method_description": "Modified Z-score (MAD) method"}

        else:
            # Default to IQR
            outlier_mask = self._outliers_iqr(clean_data, threshold)
            details = {"method_description": "Interquartile Range (IQR) method"}

        outlier_indices = np.where(outlier_mask)[0]
        outlier_count = len(outlier_indices)
        outlier_percentage = outlier_count / len(clean_data) if len(clean_data) > 0 else 0.0

        return OutlierAnalysis(
            outlier_indices=outlier_indices,
            outlier_count=outlier_count,
            outlier_percentage=outlier_percentage,
            method=method,
            threshold=threshold,
            details=details
        )

    def _outliers_iqr(self, data: np.ndarray, multiplier: float = 1.5) -> np.ndarray:
        """Detect outliers using IQR method"""
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        lower_bound = q1 - multiplier * iqr
        upper_bound = q3 + multiplier * iqr
        return (data < lower_bound) | (data > upper_bound)

    def _outliers_zscore(self, data: np.ndarray, threshold: float = 3.0) -> np.ndarray:
        """Detect outliers using Z-score method"""
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return np.zeros(len(data), dtype=bool)
        z_scores = np.abs((data - mean) / std)
        return z_scores > threshold

    def _outliers_modified_zscore(self, data: np.ndarray, threshold: float = 3.5) -> np.ndarray:
        """Detect outliers using Modified Z-score (MAD) method"""
        median = np.median(data)
        mad = np.median(np.abs(data - median))
        if mad == 0:
            return np.zeros(len(data), dtype=bool)
        modified_z_scores = 0.6745 * (data - median) / mad
        return np.abs(modified_z_scores) > threshold

    def analyze_distribution(self, column: Optional[str] = None) -> DistributionAnalysis:
        """Analyze statistical distribution of data

        Args:
            column: Specific column for DataFrame

        Returns:
            DistributionAnalysis results
        """
        # Get data to analyze
        if self.is_dataframe:
            if column:
                data = self.data[column].values
            else:
                num_cols = self.data.select_dtypes(include=[np.number]).columns
                if len(num_cols) == 0:
                    raise ValueError("No numeric columns found")
                data = self.data[num_cols[0]].values
        else:
            data = self.data.flatten()

        # Remove NaN values
        clean_data = data[~np.isnan(data)]

        if len(clean_data) == 0:
            raise ValueError("No valid data for distribution analysis")

        # Calculate statistics
        mean_val = np.mean(clean_data)
        median_val = np.median(clean_data)
        std_val = np.std(clean_data)
        min_val = np.min(clean_data)
        max_val = np.max(clean_data)
        q1, q2, q3 = np.percentile(clean_data, [25, 50, 75])
        skewness = stats.skew(clean_data)
        kurtosis = stats.kurtosis(clean_data)

        # Test for normality
        if len(clean_data) >= 3:
            _, p_value = stats.shapiro(clean_data[:5000])  # Limit for performance
        else:
            p_value = None

        # Determine distribution type
        distribution_type = "unknown"
        if p_value is not None and p_value > 0.05:
            distribution_type = "normal"
        elif abs(skewness) < 0.5:
            distribution_type = "approximately_normal"
        elif skewness > 1:
            distribution_type = "right_skewed"
        elif skewness < -1:
            distribution_type = "left_skewed"

        return DistributionAnalysis(
            mean=mean_val,
            median=median_val,
            std=std_val,
            min=min_val,
            max=max_val,
            quartiles=(q1, q2, q3),
            skewness=skewness,
            kurtosis=kurtosis,
            distribution_type=distribution_type,
            normality_test_p_value=p_value
        )

    def generate_quality_report(
        self,
        check_timeliness: bool = False,
        timestamp_column: Optional[str] = None,
        detect_outliers: bool = True,
        analyze_distribution: bool = True
    ) -> QualityReport:
        """Generate comprehensive quality report

        Args:
            check_timeliness: Whether to check data timeliness
            timestamp_column: Column name for timeliness check
            detect_outliers: Whether to perform outlier detection
            analyze_distribution: Whether to analyze distribution

        Returns:
            Comprehensive QualityReport
        """
        dimension_scores = {}

        # Completeness
        completeness_score = self.completeness(self.data)
        dimension_scores[QualityDimension.COMPLETENESS] = QualityScore(
            dimension=QualityDimension.COMPLETENESS,
            score=completeness_score,
            details={"missing_percentage": 1.0 - completeness_score}
        )

        # Uniqueness
        if self.is_dataframe:
            # Average uniqueness across columns
            uniqueness_scores = []
            for col in self.data.columns:
                uniqueness_scores.append(self.uniqueness(self.data[col]))
            uniqueness_score = np.mean(uniqueness_scores)
        else:
            uniqueness_score = self.uniqueness(self.data)

        dimension_scores[QualityDimension.UNIQUENESS] = QualityScore(
            dimension=QualityDimension.UNIQUENESS,
            score=uniqueness_score,
            details={"duplicate_ratio": 1.0 - uniqueness_score}
        )

        # Validity (default range 0-1 for numeric data)
        try:
            if self.is_dataframe:
                num_cols = self.data.select_dtypes(include=[np.number]).columns
                if len(num_cols) > 0:
                    validity_scores = []
                    for col in num_cols:
                        validity_scores.append(self.validity(self.data[col], min_val=0, max_val=1))
                    validity_score = np.mean(validity_scores)
                else:
                    validity_score = 1.0
            else:
                validity_score = self.validity(self.data, min_val=0, max_val=1)
        except:
            validity_score = 1.0

        dimension_scores[QualityDimension.VALIDITY] = QualityScore(
            dimension=QualityDimension.VALIDITY,
            score=validity_score
        )

        # Timeliness
        if check_timeliness:
            timeliness_score = self.timeliness(timestamp_column=timestamp_column)
            dimension_scores[QualityDimension.TIMELINESS] = QualityScore(
                dimension=QualityDimension.TIMELINESS,
                score=timeliness_score
            )

        # Calculate overall score (weighted average)
        weights = {
            QualityDimension.COMPLETENESS: 0.3,
            QualityDimension.UNIQUENESS: 0.2,
            QualityDimension.VALIDITY: 0.25,
            QualityDimension.ACCURACY: 0.15,
            QualityDimension.TIMELINESS: 0.1
        }

        total_weight = sum(weights[dim] for dim in dimension_scores.keys() if dim in weights)
        overall_score = sum(
            score.score * weights.get(dim, 0)
            for dim, score in dimension_scores.items()
        ) / total_weight if total_weight > 0 else 0.0

        # Optional analyses
        outlier_analysis = None
        if detect_outliers:
            try:
                outlier_analysis = self.detect_outliers()
            except Exception as e:
                logger.warning(f"Outlier detection failed: {e}")

        distribution_analysis = None
        if analyze_distribution:
            try:
                distribution_analysis = self.analyze_distribution()
            except Exception as e:
                logger.warning(f"Distribution analysis failed: {e}")

        return QualityReport(
            overall_score=overall_score,
            dimension_scores=dimension_scores,
            distribution_analysis=distribution_analysis,
            outlier_analysis=outlier_analysis
        )
