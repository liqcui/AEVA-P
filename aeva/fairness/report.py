"""
Fairness Report Generation

Generate comprehensive fairness assessment reports

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

from aeva.fairness.detector import BiasDetectionResult

logger = logging.getLogger(__name__)


@dataclass
class FairnessReport:
    """Comprehensive fairness report"""
    model_name: str
    timestamp: datetime
    overall_biased: bool
    overall_severity: str
    attribute_results: Dict[str, BiasDetectionResult]
    summary: Dict[str, Any]
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'model_name': self.model_name,
            'timestamp': self.timestamp.isoformat(),
            'overall_biased': self.overall_biased,
            'overall_severity': self.overall_severity,
            'attribute_results': {
                name: result.to_dict()
                for name, result in self.attribute_results.items()
            },
            'summary': self.summary,
            'recommendations': self.recommendations
        }


class FairnessReportGenerator:
    """
    Generate fairness assessment reports

    Features:
    - Multi-attribute summaries
    - Visual-friendly formatting
    - Actionable recommendations
    - Export to various formats
    """

    def __init__(self):
        """Initialize report generator"""
        pass

    def generate_report(
        self,
        model_name: str,
        attribute_results: Dict[str, BiasDetectionResult]
    ) -> FairnessReport:
        """
        Generate comprehensive fairness report

        Args:
            model_name: Name of the model
            attribute_results: Bias detection results per attribute

        Returns:
            FairnessReport
        """
        logger.info(f"Generating fairness report for {model_name}")

        # Determine overall status
        overall_biased = any(r.biased for r in attribute_results.values())

        # Determine overall severity
        severities = [r.severity for r in attribute_results.values()]
        severity_order = {'none': 0, 'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
        overall_severity = max(severities, key=lambda s: severity_order.get(s, 0))

        # Generate summary
        summary = self._generate_summary(attribute_results)

        # Aggregate recommendations
        recommendations = self._aggregate_recommendations(attribute_results)

        report = FairnessReport(
            model_name=model_name,
            timestamp=datetime.now(),
            overall_biased=overall_biased,
            overall_severity=overall_severity,
            attribute_results=attribute_results,
            summary=summary,
            recommendations=recommendations
        )

        logger.info(f"Fairness report generated: biased={overall_biased}, severity={overall_severity}")

        return report

    def _generate_summary(
        self,
        attribute_results: Dict[str, BiasDetectionResult]
    ) -> Dict[str, Any]:
        """Generate summary statistics"""
        total_attributes = len(attribute_results)
        biased_attributes = sum(1 for r in attribute_results.values() if r.biased)

        violation_counts = {}
        for result in attribute_results.values():
            for violation in result.violations:
                metric = violation['metric']
                violation_counts[metric] = violation_counts.get(metric, 0) + 1

        return {
            'total_attributes_analyzed': total_attributes,
            'biased_attributes': biased_attributes,
            'fair_attributes': total_attributes - biased_attributes,
            'violation_counts': violation_counts,
            'most_common_violation': max(violation_counts.items(), key=lambda x: x[1])[0] if violation_counts else None
        }

    def _aggregate_recommendations(
        self,
        attribute_results: Dict[str, BiasDetectionResult]
    ) -> List[str]:
        """Aggregate and deduplicate recommendations"""
        all_recs = []

        for attr_name, result in attribute_results.items():
            if result.biased:
                all_recs.append(f"\n{attr_name.upper()}:")
                all_recs.extend(result.recommendations[:5])  # Top 5 per attribute

        # Add overall recommendations
        if all_recs:
            overall = [
                "",
                "OVERALL RECOMMENDATIONS:",
                "• Conduct comprehensive fairness audit",
                "• Implement fairness monitoring in production",
                "• Document fairness considerations for stakeholders",
                "• Consider regulatory compliance requirements"
            ]
            all_recs.extend(overall)

        return all_recs

    def generate_text_report(self, report: FairnessReport) -> str:
        """
        Generate human-readable text report

        Args:
            report: FairnessReport object

        Returns:
            Formatted text report
        """
        lines = []
        lines.append("=" * 80)
        lines.append(f"FAIRNESS ASSESSMENT REPORT")
        lines.append("=" * 80)
        lines.append(f"\nModel: {report.model_name}")
        lines.append(f"Date: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"\nOverall Status: {'⚠️ BIASED' if report.overall_biased else '✓ FAIR'}")
        lines.append(f"Severity: {report.overall_severity.upper()}")

        # Summary
        lines.append(f"\n{'=' * 80}")
        lines.append("SUMMARY")
        lines.append(f"{'=' * 80}")
        lines.append(f"\nAttributes Analyzed: {report.summary['total_attributes_analyzed']}")
        lines.append(f"Biased Attributes: {report.summary['biased_attributes']}")
        lines.append(f"Fair Attributes: {report.summary['fair_attributes']}")

        if report.summary['violation_counts']:
            lines.append(f"\nViolations by Metric:")
            for metric, count in sorted(report.summary['violation_counts'].items(), key=lambda x: x[1], reverse=True):
                lines.append(f"  • {metric}: {count}")

        # Per-attribute results
        lines.append(f"\n{'=' * 80}")
        lines.append("DETAILED RESULTS BY ATTRIBUTE")
        lines.append(f"{'=' * 80}")

        for attr_name, result in report.attribute_results.items():
            lines.append(f"\n{attr_name.upper()}")
            lines.append(f"{'-' * 80}")
            lines.append(f"Status: {'⚠️ Biased' if result.biased else '✓ Fair'}")
            lines.append(f"Severity: {result.severity}")
            lines.append(f"Privileged Group: {result.privileged_group}")
            lines.append(f"Unprivileged Groups: {', '.join(str(g) for g in result.unprivileged_groups)}")

            # Metrics
            lines.append(f"\nFairness Metrics:")
            metrics_dict = result.metrics.to_dict()
            for metric_name, value in metrics_dict.items():
                lines.append(f"  • {metric_name}: {value:.4f}")

            # Violations
            if result.violations:
                lines.append(f"\nViolations ({len(result.violations)}):")
                for v in result.violations:
                    lines.append(f"  ⚠️ {v['description']}")
                    lines.append(f"     Value: {v['value']:.4f}, Threshold: {v['threshold']}")

            # Group metrics
            lines.append(f"\nPerformance by Group:")
            for group, metrics in result.group_metrics.items():
                lines.append(f"  {group}:")
                lines.append(f"    Size: {metrics['size']}")
                lines.append(f"    Accuracy: {metrics['accuracy']:.4f}")
                lines.append(f"    Precision: {metrics['precision']:.4f}")
                lines.append(f"    Recall: {metrics['recall']:.4f}")
                lines.append(f"    F1: {metrics['f1']:.4f}")

        # Recommendations
        if report.recommendations:
            lines.append(f"\n{'=' * 80}")
            lines.append("RECOMMENDATIONS")
            lines.append(f"{'=' * 80}")
            lines.append("")
            for rec in report.recommendations:
                lines.append(rec)

        lines.append(f"\n{'=' * 80}")

        return "\n".join(lines)

    def generate_html_report(self, report: FairnessReport) -> str:
        """
        Generate HTML fairness report

        Args:
            report: FairnessReport object

        Returns:
            HTML string
        """
        status_color = "#e74c3c" if report.overall_biased else "#27ae60"
        status_text = "BIASED" if report.overall_biased else "FAIR"

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Fairness Report - {report.model_name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #2c3e50;
            color: white;
            padding: 30px;
            border-radius: 5px;
        }}
        .status {{
            background-color: {status_color};
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }}
        .section {{
            background-color: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metric {{
            display: flex;
            justify-content: space-between;
            padding: 10px;
            border-bottom: 1px solid #eee;
        }}
        .violation {{
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 10px;
            margin: 10px 0;
        }}
        .group-metrics {{
            margin: 10px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #34495e;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Fairness Assessment Report</h1>
        <p>Model: {report.model_name}</p>
        <p>Date: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <div class="status">
        {status_text} (Severity: {report.overall_severity.upper()})
    </div>

    <div class="section">
        <h2>Summary</h2>
        <div class="metric">
            <span>Attributes Analyzed:</span>
            <strong>{report.summary['total_attributes_analyzed']}</strong>
        </div>
        <div class="metric">
            <span>Biased Attributes:</span>
            <strong>{report.summary['biased_attributes']}</strong>
        </div>
        <div class="metric">
            <span>Fair Attributes:</span>
            <strong>{report.summary['fair_attributes']}</strong>
        </div>
    </div>
"""

        # Per-attribute results
        for attr_name, result in report.attribute_results.items():
            attr_status = "BIASED" if result.biased else "FAIR"
            attr_color = "#e74c3c" if result.biased else "#27ae60"

            html += f"""
    <div class="section">
        <h2>{attr_name}</h2>
        <p style="color: {attr_color}; font-weight: bold;">Status: {attr_status} (Severity: {result.severity})</p>
        <p>Privileged Group: <strong>{result.privileged_group}</strong></p>

        <h3>Fairness Metrics</h3>
        <table>
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
"""
            for metric_name, value in result.metrics.to_dict().items():
                html += f"""
            <tr>
                <td>{metric_name}</td>
                <td>{value:.4f}</td>
            </tr>
"""

            html += """
        </table>
"""

            if result.violations:
                html += """
        <h3>Violations</h3>
"""
                for v in result.violations:
                    html += f"""
        <div class="violation">
            <strong>{v['description']}</strong><br>
            Value: {v['value']:.4f}, Threshold: {v['threshold']}
        </div>
"""

            html += """
    </div>
"""

        # Recommendations
        if report.recommendations:
            html += """
    <div class="section">
        <h2>Recommendations</h2>
        <ul>
"""
            for rec in report.recommendations:
                if rec.strip():
                    html += f"            <li>{rec}</li>\n"

            html += """
        </ul>
    </div>
"""

        html += """
</body>
</html>
"""

        return html
