"""
Explanation Report Generator

Generates comprehensive explanation reports for regulatory compliance
and model documentation.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ExplanationReport:
    """
    Container for explanation report

    Attributes:
        title: Report title
        model_name: Name of the model
        timestamp: Report generation timestamp
        shap_results: SHAP explanation results
        lime_results: LIME explanation results
        importance_results: Feature importance results
        summary: Executive summary
        metadata: Additional metadata
    """
    title: str
    model_name: str
    timestamp: datetime = field(default_factory=datetime.now)
    shap_results: Optional[Dict[str, Any]] = None
    lime_results: Optional[Dict[str, Any]] = None
    importance_results: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ExplanationReportGenerator:
    """
    Generate explanation reports in multiple formats
    """

    def __init__(self, model_name: str = "Model"):
        """
        Initialize report generator

        Args:
            model_name: Name of the model
        """
        self.model_name = model_name

    def generate_text_report(
        self,
        shap_explanation: Optional[Any] = None,
        lime_explanation: Optional[Any] = None,
        feature_importance: Optional[Any] = None
    ) -> str:
        """
        Generate text-based explanation report

        Args:
            shap_explanation: SHAP explanation results
            lime_explanation: LIME explanation results
            feature_importance: Feature importance results

        Returns:
            Text report
        """
        report = []
        report.append("=" * 80)
        report.append(f"Model Explanation Report: {self.model_name}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)

        # SHAP results
        if shap_explanation:
            report.append("\n### SHAP Analysis ###\n")
            top_features = shap_explanation.get_top_features(10)
            report.append("Top 10 Most Important Features:")
            for i, (feature, value) in enumerate(top_features, 1):
                report.append(f"  {i}. {feature}: {value:.4f}")

        # LIME results
        if lime_explanation:
            report.append("\n### LIME Analysis ###\n")
            report.append(f"Local Model R² Score: {lime_explanation.score:.4f}")
            top_features = lime_explanation.get_top_features(10)
            report.append("\nTop 10 Feature Weights:")
            for i, (feature, weight) in enumerate(top_features, 1):
                direction = "↑" if weight > 0 else "↓"
                report.append(f"  {i}. {feature}: {weight:.4f} {direction}")

        # Feature Importance results
        if feature_importance:
            report.append(f"\n### Feature Importance ({feature_importance.method}) ###\n")
            top_features = feature_importance.get_top_features(10)
            report.append("Top 10 Important Features:")
            for i, (feature, score, rank) in enumerate(top_features, 1):
                report.append(f"  {i}. {feature}: {score:.4f} (Rank: {rank})")

        report.append("\n" + "=" * 80)
        report.append("End of Report")
        report.append("=" * 80)

        return "\n".join(report)

    def generate_html_report(
        self,
        shap_explanation: Optional[Any] = None,
        lime_explanation: Optional[Any] = None,
        feature_importance: Optional[Any] = None
    ) -> str:
        """
        Generate HTML explanation report

        Args:
            shap_explanation: SHAP explanation results
            lime_explanation: LIME explanation results
            feature_importance: Feature importance results

        Returns:
            HTML report
        """
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Explanation Report - {self.model_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
        .positive {{ color: green; }}
        .negative {{ color: red; }}
        .metric {{ font-weight: bold; color: #2980b9; }}
        .timestamp {{ color: #7f8c8d; font-size: 0.9em; }}
    </style>
</head>
<body>
    <h1>Model Explanation Report</h1>
    <p><strong>Model:</strong> {self.model_name}</p>
    <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
"""

        # SHAP section
        if shap_explanation:
            html += """
    <h2>SHAP Analysis</h2>
    <p>SHAP (SHapley Additive exPlanations) provides game theory-based feature importance.</p>
    <table>
        <tr><th>Rank</th><th>Feature</th><th>SHAP Value</th></tr>
"""
            top_features = shap_explanation.get_top_features(10)
            for i, (feature, value) in enumerate(top_features, 1):
                value_class = 'positive' if value > 0 else 'negative'
                html += f"        <tr><td>{i}</td><td>{feature}</td><td class='{value_class}'>{value:.4f}</td></tr>\n"
            html += "    </table>\n"

        # LIME section
        if lime_explanation:
            html += f"""
    <h2>LIME Analysis</h2>
    <p>LIME (Local Interpretable Model-agnostic Explanations) provides local approximations.</p>
    <p><span class="metric">Local Model R² Score:</span> {lime_explanation.score:.4f}</p>
    <table>
        <tr><th>Rank</th><th>Feature</th><th>Weight</th><th>Direction</th></tr>
"""
            top_features = lime_explanation.get_top_features(10)
            for i, (feature, weight) in enumerate(top_features, 1):
                direction = "Increases prediction" if weight > 0 else "Decreases prediction"
                weight_class = 'positive' if weight > 0 else 'negative'
                html += f"        <tr><td>{i}</td><td>{feature}</td><td class='{weight_class}'>{weight:.4f}</td><td>{direction}</td></tr>\n"
            html += "    </table>\n"

        # Feature Importance section
        if feature_importance:
            html += f"""
    <h2>Feature Importance ({feature_importance.method})</h2>
    <table>
        <tr><th>Rank</th><th>Feature</th><th>Importance Score</th></tr>
"""
            top_features = feature_importance.get_top_features(10)
            for i, (feature, score, rank) in enumerate(top_features, 1):
                html += f"        <tr><td>{rank}</td><td>{feature}</td><td>{score:.4f}</td></tr>\n"
            html += "    </table>\n"

        html += """
    <hr>
    <p style="text-align: center; color: #7f8c8d;">
        Generated by AEVA Explainability Module
    </p>
</body>
</html>
"""
        return html

    def save_report(
        self,
        filepath: str,
        format: str = 'html',
        **kwargs
    ) -> None:
        """
        Save explanation report to file

        Args:
            filepath: Path to save report
            format: Report format ('html' or 'text')
            **kwargs: Explanation results (shap_explanation, lime_explanation, etc.)
        """
        if format == 'html':
            content = self.generate_html_report(**kwargs)
        elif format == 'text':
            content = self.generate_text_report(**kwargs)
        else:
            raise ValueError(f"Unknown format: {format}")

        with open(filepath, 'w') as f:
            f.write(content)

        logger.info(f"Explanation report saved to {filepath}")
