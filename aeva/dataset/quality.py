"""
Data Quality Analyzer

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
from typing import Dict, Any, List
from collections import Counter

logger = logging.getLogger(__name__)


class DataQualityAnalyzer:
    """
    Analyze dataset quality

    Features:
    - Completeness check
    - Balance analysis
    - Duplicate detection
    - Anomaly identification
    """

    def analyze(self, data: List[Any]) -> Dict[str, Any]:
        """
        Analyze dataset quality

        Args:
            data: Dataset to analyze

        Returns:
            Quality analysis report
        """
        logger.info(f"Analyzing quality of {len(data)} samples")

        report = {
            'total_samples': len(data),
            'completeness': self._check_completeness(data),
            'balance': self._analyze_balance(data),
            'duplicates': self._detect_duplicates(data),
            'statistics': self._compute_statistics(data),
            'quality_score': 0.0,
            'issues': [],
            'recommendations': []
        }

        # Calculate overall quality score
        report['quality_score'] = self._calculate_quality_score(report)

        # Generate recommendations
        report['recommendations'] = self._generate_recommendations(report)

        logger.info(f"Quality score: {report['quality_score']:.2f}/100")

        return report

    def _check_completeness(self, data: List[Any]) -> Dict[str, Any]:
        """Check data completeness"""
        if not data:
            return {'complete': False, 'missing_count': 0, 'completeness_ratio': 0.0}

        # Assuming data is list of dicts
        if isinstance(data[0], dict):
            total_fields = 0
            missing_fields = 0

            for sample in data:
                for key, value in sample.items():
                    total_fields += 1
                    if value is None or value == '':
                        missing_fields += 1

            completeness_ratio = (total_fields - missing_fields) / total_fields if total_fields > 0 else 0.0

            return {
                'complete': missing_fields == 0,
                'missing_count': missing_fields,
                'total_fields': total_fields,
                'completeness_ratio': completeness_ratio
            }

        return {'complete': True, 'missing_count': 0, 'completeness_ratio': 1.0}

    def _analyze_balance(self, data: List[Any]) -> Dict[str, Any]:
        """Analyze class balance (for classification datasets)"""
        if not data:
            return {'balanced': True}

        # Try to extract labels
        labels = []
        if isinstance(data[0], dict):
            if 'label' in data[0]:
                labels = [sample['label'] for sample in data]
            elif 'class' in data[0]:
                labels = [sample['class'] for sample in data]

        if not labels:
            return {'balanced': True, 'note': 'No labels found'}

        # Count label distribution
        label_counts = Counter(labels)
        total = len(labels)

        distribution = {
            label: {
                'count': count,
                'percentage': (count / total) * 100
            }
            for label, count in label_counts.items()
        }

        # Check balance (consider balanced if all classes within 30% of uniform)
        uniform_percentage = 100 / len(label_counts)
        balanced = all(
            abs(info['percentage'] - uniform_percentage) < 30
            for info in distribution.values()
        )

        return {
            'balanced': balanced,
            'num_classes': len(label_counts),
            'distribution': distribution,
            'most_common': label_counts.most_common(1)[0] if label_counts else None,
            'least_common': label_counts.most_common()[-1] if label_counts else None
        }

    def _detect_duplicates(self, data: List[Any]) -> Dict[str, Any]:
        """Detect duplicate samples"""
        if not data:
            return {'has_duplicates': False, 'duplicate_count': 0}

        # Convert to hashable format for duplicate detection
        hashable_data = []
        for sample in data:
            if isinstance(sample, dict):
                hashable_data.append(tuple(sorted(sample.items())))
            elif isinstance(sample, (list, tuple)):
                hashable_data.append(tuple(sample))
            else:
                hashable_data.append(sample)

        # Count occurrences
        counts = Counter(hashable_data)
        duplicates = {item: count for item, count in counts.items() if count > 1}

        duplicate_count = sum(count - 1 for count in duplicates.values())

        return {
            'has_duplicates': len(duplicates) > 0,
            'duplicate_count': duplicate_count,
            'duplicate_ratio': duplicate_count / len(data) if data else 0.0,
            'unique_count': len(counts)
        }

    def _compute_statistics(self, data: List[Any]) -> Dict[str, Any]:
        """Compute basic statistics"""
        stats = {
            'total_samples': len(data),
            'empty_samples': 0
        }

        # Count empty samples
        for sample in data:
            if not sample or (isinstance(sample, dict) and not any(sample.values())):
                stats['empty_samples'] += 1

        return stats

    def _calculate_quality_score(self, report: Dict[str, Any]) -> float:
        """Calculate overall quality score (0-100)"""
        score = 100.0

        # Completeness (40 points)
        completeness_ratio = report['completeness'].get('completeness_ratio', 1.0)
        score -= (1.0 - completeness_ratio) * 40

        # Balance (30 points)
        if not report['balance'].get('balanced', True):
            score -= 30

        # Duplicates (30 points)
        duplicate_ratio = report['duplicates'].get('duplicate_ratio', 0.0)
        score -= duplicate_ratio * 30

        return max(0.0, min(100.0, score))

    def _generate_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Generate quality improvement recommendations"""
        recommendations = []

        # Completeness issues
        if report['completeness']['completeness_ratio'] < 0.95:
            recommendations.append(
                f"Data has {report['completeness']['missing_count']} missing values. "
                "Consider data cleaning or imputation."
            )

        # Imbalance issues
        if not report['balance'].get('balanced', True):
            most_common = report['balance'].get('most_common')
            least_common = report['balance'].get('least_common')
            if most_common and least_common:
                ratio = most_common[1] / least_common[1]
                if ratio > 3:
                    recommendations.append(
                        f"Significant class imbalance detected (ratio: {ratio:.1f}:1). "
                        "Consider oversampling minority class or undersampling majority class."
                    )

        # Duplicate issues
        if report['duplicates']['duplicate_ratio'] > 0.05:  # 5%
            recommendations.append(
                f"High duplicate ratio ({report['duplicates']['duplicate_ratio']:.1%}). "
                "Consider removing duplicates to avoid overfitting."
            )

        # Empty samples
        if report['statistics']['empty_samples'] > 0:
            recommendations.append(
                f"Found {report['statistics']['empty_samples']} empty samples. "
                "Consider removing them."
            )

        return recommendations
