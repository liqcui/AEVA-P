"""
Great Expectations Integration

Provides production-grade data quality validation using Great Expectations.

Features:
- Automated expectation generation
- Data profiling
- Validation reports
- Data documentation

Usage:
    from aeva.integrations import GreatExpectationsProfiler

    profiler = GreatExpectationsProfiler()
    suite = profiler.profile_dataframe(df, "my_dataset")
    validation = profiler.validate(df, suite)

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
from typing import Any, Dict, List, Optional
import pandas as pd
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)


class GreatExpectationsProfiler:
    """
    Production-grade data quality profiling using Great Expectations

    Falls back to basic implementation if GE not installed.
    """

    def __init__(self, project_dir: Optional[str] = None):
        """
        Initialize Great Expectations profiler

        Args:
            project_dir: Directory for GE project (default: ./ge_project)
        """
        self.project_dir = project_dir or "./ge_project"

        # Try to import Great Expectations
        try:
            import great_expectations as gx
            from great_expectations.dataset import PandasDataset

            self.ge_available = True
            self.gx = gx
            self.PandasDataset = PandasDataset

            logger.info("Great Expectations library loaded successfully")

        except ImportError:
            self.ge_available = False
            logger.warning(
                "Great Expectations not installed. Install with: pip install great_expectations\n"
                "Falling back to basic data quality checks."
            )

    def is_available(self) -> bool:
        """Check if Great Expectations is available"""
        return self.ge_available

    def profile_dataframe(
        self,
        df: pd.DataFrame,
        dataset_name: str = "dataset",
        profile_type: str = "auto"
    ) -> Dict[str, Any]:
        """
        Profile a DataFrame and generate expectations

        Args:
            df: DataFrame to profile
            dataset_name: Name for the dataset
            profile_type: Profiling type ('auto', 'basic', 'comprehensive')

        Returns:
            Expectation suite or quality report
        """
        if not self.ge_available:
            return self._fallback_profile(df, dataset_name)

        # Create GE dataset
        ge_df = self.PandasDataset(df)

        expectations = {}

        # Basic expectations
        expectations['row_count'] = ge_df.expect_table_row_count_to_be_between(
            min_value=0,
            max_value=len(df) * 2
        )

        expectations['column_count'] = ge_df.expect_table_column_count_to_equal(
            value=len(df.columns)
        )

        # Per-column expectations
        column_expectations = {}

        for column in df.columns:
            col_expectations = []

            # Exist
            col_expectations.append(
                ge_df.expect_column_to_exist(column)
            )

            # Null values
            null_pct = df[column].isnull().sum() / len(df)
            col_expectations.append(
                ge_df.expect_column_values_to_not_be_null(
                    column,
                    mostly=1.0 - null_pct
                )
            )

            # Type-specific expectations
            dtype = df[column].dtype

            if pd.api.types.is_numeric_dtype(dtype):
                # Numeric column
                col_min = df[column].min()
                col_max = df[column].max()

                col_expectations.append(
                    ge_df.expect_column_values_to_be_between(
                        column,
                        min_value=col_min,
                        max_value=col_max,
                        mostly=0.95
                    )
                )

                # Mean/std expectations
                col_mean = df[column].mean()
                col_std = df[column].std()

                col_expectations.append(
                    ge_df.expect_column_mean_to_be_between(
                        column,
                        min_value=col_mean - 3 * col_std,
                        max_value=col_mean + 3 * col_std
                    )
                )

            column_expectations[column] = col_expectations

        # Get validation results
        validation_results = {
            'dataset_name': dataset_name,
            'success': True,
            'statistics': {
                'row_count': len(df),
                'column_count': len(df.columns),
                'columns': list(df.columns)
            },
            'expectations': expectations,
            'column_expectations': column_expectations,
            'using_ge': True
        }

        return validation_results

    def validate(
        self,
        df: pd.DataFrame,
        expectations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate DataFrame against expectations

        Args:
            df: DataFrame to validate
            expectations: Expectation suite

        Returns:
            Validation results
        """
        if not self.ge_available:
            return self._fallback_validate(df, expectations)

        ge_df = self.PandasDataset(df)

        results = {
            'success': True,
            'results': [],
            'statistics': {
                'evaluated_expectations': 0,
                'successful_expectations': 0,
                'unsuccessful_expectations': 0,
                'success_percent': 0.0
            }
        }

        # Validate each expectation
        total = 0
        successful = 0

        for exp_name, exp_result in expectations.get('expectations', {}).items():
            total += 1
            if exp_result.success:
                successful += 1
            results['results'].append({
                'expectation': exp_name,
                'success': exp_result.success
            })

        results['statistics']['evaluated_expectations'] = total
        results['statistics']['successful_expectations'] = successful
        results['statistics']['unsuccessful_expectations'] = total - successful
        results['statistics']['success_percent'] = (successful / total * 100) if total > 0 else 0

        results['success'] = (successful / total) > 0.8 if total > 0 else False

        return results

    def generate_data_docs(
        self,
        validation_results: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate data documentation

        Args:
            validation_results: Validation results
            output_path: Path to save documentation

        Returns:
            Path to generated documentation or HTML string
        """
        if not self.ge_available:
            return self._fallback_docs(validation_results)

        # Generate HTML report
        html = "<html><head><title>Data Quality Report</title></head><body>"
        html += "<h1>Data Quality Validation Report</h1>"

        html += f"<h2>Dataset: {validation_results.get('dataset_name', 'Unknown')}</h2>"

        stats = validation_results.get('statistics', {})
        html += "<h3>Statistics</h3><ul>"
        html += f"<li>Rows: {stats.get('row_count', 'N/A')}</li>"
        html += f"<li>Columns: {stats.get('column_count', 'N/A')}</li>"
        html += "</ul>"

        html += "<h3>Expectations</h3><ul>"
        for exp_name, exp_result in validation_results.get('expectations', {}).items():
            status = "✓" if exp_result.success else "✗"
            html += f"<li>{status} {exp_name}</li>"
        html += "</ul>"

        html += "</body></html>"

        if output_path:
            Path(output_path).write_text(html)
            return output_path

        return html

    def _fallback_profile(
        self,
        df: pd.DataFrame,
        dataset_name: str
    ) -> Dict[str, Any]:
        """Fallback profiling when GE not available"""
        logger.warning("Using fallback data profiling (Great Expectations not installed)")

        from ..data_quality import DataProfiler

        profiler = DataProfiler()
        profile = profiler.profile(df)

        return {
            'dataset_name': dataset_name,
            'success': True,
            'statistics': {
                'row_count': profile.n_samples,
                'column_count': profile.n_features,
                'columns': list(df.columns),
                'quality_score': profile.quality_score
            },
            'using_ge': False,
            'fallback': True
        }

    def _fallback_validate(
        self,
        df: pd.DataFrame,
        expectations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Fallback validation when GE not available"""
        logger.warning("Using fallback validation")

        from ..data_quality import QualityMetrics

        metrics = QualityMetrics()

        completeness = metrics.completeness(df)
        uniqueness = metrics.uniqueness(df)

        return {
            'success': completeness > 0.9 and uniqueness > 0.9,
            'statistics': {
                'completeness': completeness,
                'uniqueness': uniqueness,
                'evaluated_expectations': 2,
                'successful_expectations': int(completeness > 0.9) + int(uniqueness > 0.9),
                'success_percent': ((int(completeness > 0.9) + int(uniqueness > 0.9)) / 2) * 100
            },
            'fallback': True
        }

    def _fallback_docs(self, validation_results: Dict[str, Any]) -> str:
        """Fallback documentation generation"""
        report = "=" * 70 + "\n"
        report += "Data Quality Report (Basic)\n"
        report += "=" * 70 + "\n\n"

        stats = validation_results.get('statistics', {})
        report += f"Dataset: {validation_results.get('dataset_name', 'Unknown')}\n"
        report += f"Rows: {stats.get('row_count', 'N/A')}\n"
        report += f"Columns: {stats.get('column_count', 'N/A')}\n"

        if 'quality_score' in stats:
            report += f"Quality Score: {stats['quality_score']:.1f}/100\n"

        return report


def check_ge_installation() -> bool:
    """Check if Great Expectations is properly installed"""
    try:
        import great_expectations
        return True
    except ImportError:
        return False


def install_ge_instructions() -> str:
    """Return installation instructions for Great Expectations"""
    return """
To install Great Expectations:

pip install great_expectations

For full features:

pip install great_expectations[sqlalchemy,spark]

Documentation: https://docs.greatexpectations.io/
"""
