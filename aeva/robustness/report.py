"""
Robustness Reports

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""
import logging
import json
import base64
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from pathlib import Path
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

logger = logging.getLogger(__name__)


class AttackType(Enum):
    """Types of adversarial attacks"""
    FGSM = "fgsm"
    PGD = "pgd"
    CARLINI_WAGNER = "carlini_wagner"
    DEEPFOOL = "deepfool"
    BOUNDARY = "boundary"
    NOISE = "noise"
    CUSTOM = "custom"


class SeverityLevel(Enum):
    """Severity levels for robustness issues"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AttackResult:
    """Results from a specific attack"""
    attack_type: AttackType
    success_rate: float
    avg_perturbation: float
    samples_tested: int
    samples_successful: int
    epsilon: float
    execution_time: float
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DefenseResult:
    """Results from defense mechanism evaluation"""
    defense_name: str
    effectiveness: float
    performance_impact: float
    robustness_improvement: float
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RobustnessReport:
    """Comprehensive robustness report container"""
    model_name: str
    attack_results: List[AttackResult] = field(default_factory=list)
    defense_results: List[DefenseResult] = field(default_factory=list)
    overall_robustness_score: float = 0.0
    severity_level: SeverityLevel = SeverityLevel.LOW
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    comparative_analysis: Optional[Dict[str, Any]] = None


class RobustnessReportGenerator:
    """Generate comprehensive robustness reports"""

    def __init__(self, model_name: str = "Model"):
        """Initialize report generator

        Args:
            model_name: Name of the model being evaluated
        """
        self.model_name = model_name

    def create_report(
        self,
        attack_results: Optional[List[AttackResult]] = None,
        defense_results: Optional[List[DefenseResult]] = None,
        **kwargs
    ) -> RobustnessReport:
        """Create a robustness report

        Args:
            attack_results: List of attack evaluation results
            defense_results: List of defense evaluation results
            **kwargs: Additional metadata

        Returns:
            RobustnessReport instance
        """
        report = RobustnessReport(
            model_name=self.model_name,
            attack_results=attack_results or [],
            defense_results=defense_results or [],
            metadata=kwargs
        )

        # Calculate overall metrics
        report.overall_robustness_score = self._calculate_robustness_score(report)
        report.severity_level = self._determine_severity(report)
        report.recommendations = self._generate_recommendations(report)

        return report

    def _calculate_robustness_score(self, report: RobustnessReport) -> float:
        """Calculate overall robustness score

        Args:
            report: RobustnessReport instance

        Returns:
            Score from 0.0 to 1.0 (higher is more robust)
        """
        if not report.attack_results:
            return 0.0

        # Robustness = 1 - average attack success rate
        success_rates = [result.success_rate for result in report.attack_results]
        avg_success_rate = np.mean(success_rates)

        # Factor in defense effectiveness if available
        if report.defense_results:
            defense_bonus = np.mean([d.effectiveness for d in report.defense_results]) * 0.2
            robustness = (1.0 - avg_success_rate) + defense_bonus
        else:
            robustness = 1.0 - avg_success_rate

        return min(1.0, max(0.0, robustness))

    def _determine_severity(self, report: RobustnessReport) -> SeverityLevel:
        """Determine severity level based on robustness score

        Args:
            report: RobustnessReport instance

        Returns:
            SeverityLevel
        """
        score = report.overall_robustness_score

        if score >= 0.8:
            return SeverityLevel.LOW
        elif score >= 0.6:
            return SeverityLevel.MEDIUM
        elif score >= 0.4:
            return SeverityLevel.HIGH
        else:
            return SeverityLevel.CRITICAL

    def _generate_recommendations(self, report: RobustnessReport) -> List[str]:
        """Generate recommendations based on results

        Args:
            report: RobustnessReport instance

        Returns:
            List of recommendations
        """
        recommendations = []

        # Analyze attack results
        if report.attack_results:
            max_success = max(r.success_rate for r in report.attack_results)

            if max_success > 0.7:
                recommendations.append("CRITICAL: Implement adversarial training to improve robustness")
                recommendations.append("Consider ensemble methods for improved defense")

            if max_success > 0.5:
                recommendations.append("Add input validation and sanitization")
                recommendations.append("Implement detection mechanisms for adversarial examples")

            # Check for specific attack vulnerabilities
            for result in report.attack_results:
                if result.success_rate > 0.6:
                    recommendations.append(
                        f"High vulnerability to {result.attack_type.value} attacks - "
                        f"consider specific defenses"
                    )

        # Analyze defense results
        if report.defense_results:
            weak_defenses = [d for d in report.defense_results if d.effectiveness < 0.5]
            if weak_defenses:
                recommendations.append(
                    f"Review and strengthen defenses: {', '.join(d.defense_name for d in weak_defenses)}"
                )

        if report.severity_level == SeverityLevel.CRITICAL:
            recommendations.append("URGENT: Model requires immediate security review before deployment")

        if not recommendations:
            recommendations.append("Model shows good robustness - maintain current security practices")

        return recommendations

    def generate_text_report(self, report: RobustnessReport) -> str:
        """Generate plain text report

        Args:
            report: RobustnessReport instance

        Returns:
            Formatted text report
        """
        lines = []
        lines.append("=" * 80)
        lines.append(f"ROBUSTNESS EVALUATION REPORT")
        lines.append("=" * 80)
        lines.append(f"Model: {report.model_name}")
        lines.append(f"Generated: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Overall Robustness Score: {report.overall_robustness_score:.2%}")
        lines.append(f"Severity Level: {report.severity_level.value.upper()}")
        lines.append("")

        # Attack Results Section
        if report.attack_results:
            lines.append("-" * 80)
            lines.append("ATTACK EVALUATION RESULTS")
            lines.append("-" * 80)
            for result in report.attack_results:
                lines.append(f"\n{result.attack_type.value.upper()} Attack:")
                lines.append(f"  Success Rate: {result.success_rate:.2%}")
                lines.append(f"  Average Perturbation: {result.avg_perturbation:.6f}")
                lines.append(f"  Samples Tested: {result.samples_tested}")
                lines.append(f"  Successful Attacks: {result.samples_successful}")
                lines.append(f"  Epsilon: {result.epsilon}")
                lines.append(f"  Execution Time: {result.execution_time:.2f}s")

        # Defense Results Section
        if report.defense_results:
            lines.append("\n" + "-" * 80)
            lines.append("DEFENSE EVALUATION RESULTS")
            lines.append("-" * 80)
            for result in report.defense_results:
                lines.append(f"\n{result.defense_name}:")
                lines.append(f"  Effectiveness: {result.effectiveness:.2%}")
                lines.append(f"  Performance Impact: {result.performance_impact:.2%}")
                lines.append(f"  Robustness Improvement: {result.robustness_improvement:.2%}")

        # Recommendations
        if report.recommendations:
            lines.append("\n" + "-" * 80)
            lines.append("RECOMMENDATIONS")
            lines.append("-" * 80)
            for i, rec in enumerate(report.recommendations, 1):
                lines.append(f"{i}. {rec}")

        # Executive Summary
        lines.append("\n" + "=" * 80)
        lines.append("EXECUTIVE SUMMARY")
        lines.append("=" * 80)
        lines.append(self._generate_executive_summary(report))

        lines.append("\n" + "=" * 80)

        return "\n".join(lines)

    def generate_html_report(self, report: RobustnessReport, include_charts: bool = True) -> str:
        """Generate HTML report with styling

        Args:
            report: RobustnessReport instance
            include_charts: Whether to include visualization charts

        Returns:
            HTML formatted report
        """
        # Generate charts if requested
        charts = {}
        if include_charts:
            charts = self._generate_charts(report)

        html_parts = []
        html_parts.append("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Robustness Report: {model_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .severity-{severity} {{
            background: {severity_color};
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            display: inline-block;
            font-weight: bold;
        }}
        .section {{
            background: white;
            padding: 30px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metric {{
            display: inline-block;
            margin: 10px 20px 10px 0;
            padding: 15px 20px;
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }}
        .metric-name {{
            font-weight: bold;
            color: #555;
        }}
        .metric-value {{
            font-size: 1.5em;
            color: #667eea;
            margin-left: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #667eea;
            color: white;
            font-weight: 600;
        }}
        .chart {{
            margin: 20px 0;
            text-align: center;
        }}
        .chart img {{
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .recommendation {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        .critical {{
            background: #f8d7da;
            border-left-color: #dc3545;
        }}
        .footer {{
            text-align: center;
            color: #666;
            padding: 20px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
""".format(
            model_name=report.model_name,
            severity=report.severity_level.value,
            severity_color=self._get_severity_color(report.severity_level)
        ))

        # Header
        html_parts.append(f"""
    <div class="header">
        <h1>Robustness Evaluation Report</h1>
        <p>{report.model_name}</p>
        <p>Generated: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
""")

        # Summary Section
        html_parts.append(f"""
    <div class="section">
        <h2>Overall Assessment</h2>
        <div class="metric">
            <span class="metric-name">Robustness Score:</span>
            <span class="metric-value">{report.overall_robustness_score:.2%}</span>
        </div>
        <div class="metric">
            <span class="metric-name">Severity Level:</span>
            <span class="severity-{report.severity_level.value}">{report.severity_level.value.upper()}</span>
        </div>
    </div>
""")

        # Attack Results
        if report.attack_results:
            html_parts.append("""
    <div class="section">
        <h2>Attack Evaluation Results</h2>
        <table>
            <tr>
                <th>Attack Type</th>
                <th>Success Rate</th>
                <th>Avg Perturbation</th>
                <th>Samples Tested</th>
                <th>Epsilon</th>
            </tr>
""")
            for result in report.attack_results:
                html_parts.append(f"""
            <tr>
                <td>{result.attack_type.value.upper()}</td>
                <td>{result.success_rate:.2%}</td>
                <td>{result.avg_perturbation:.6f}</td>
                <td>{result.samples_tested}</td>
                <td>{result.epsilon}</td>
            </tr>
""")
            html_parts.append("        </table>")

            # Add chart if available
            if 'attack_comparison' in charts:
                html_parts.append(f"""
        <div class="chart">
            <h3>Attack Success Rates</h3>
            <img src="data:image/png;base64,{charts['attack_comparison']}" alt="Attack Comparison">
        </div>
""")
            html_parts.append("    </div>")

        # Defense Results
        if report.defense_results:
            html_parts.append("""
    <div class="section">
        <h2>Defense Evaluation Results</h2>
        <table>
            <tr>
                <th>Defense Mechanism</th>
                <th>Effectiveness</th>
                <th>Performance Impact</th>
                <th>Robustness Improvement</th>
            </tr>
""")
            for result in report.defense_results:
                html_parts.append(f"""
            <tr>
                <td>{result.defense_name}</td>
                <td>{result.effectiveness:.2%}</td>
                <td>{result.performance_impact:.2%}</td>
                <td>{result.robustness_improvement:.2%}</td>
            </tr>
""")
            html_parts.append("        </table>")

            # Add chart if available
            if 'defense_effectiveness' in charts:
                html_parts.append(f"""
        <div class="chart">
            <h3>Defense Effectiveness</h3>
            <img src="data:image/png;base64,{charts['defense_effectiveness']}" alt="Defense Effectiveness">
        </div>
""")
            html_parts.append("    </div>")

        # Recommendations
        if report.recommendations:
            html_parts.append("""
    <div class="section">
        <h2>Recommendations</h2>
""")
            for i, rec in enumerate(report.recommendations, 1):
                css_class = "critical" if "CRITICAL" in rec or "URGENT" in rec else ""
                html_parts.append(f"""
        <div class="recommendation {css_class}">
            <strong>{i}.</strong> {rec}
        </div>
""")
            html_parts.append("    </div>")

        # Executive Summary
        html_parts.append(f"""
    <div class="section">
        <h2>Executive Summary</h2>
        <p>{self._generate_executive_summary(report)}</p>
    </div>
""")

        # Footer
        html_parts.append(f"""
    <div class="footer">
        Generated by AEVA Robustness Report Generator | {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
    </div>
</body>
</html>
""")

        return "".join(html_parts)

    def generate_pdf_report(self, report: RobustnessReport, filepath: str):
        """Generate PDF report

        Args:
            report: RobustnessReport instance
            filepath: Output PDF file path
        """
        if not REPORTLAB_AVAILABLE:
            logger.error("ReportLab not installed. Install with: pip install reportlab")
            raise ImportError("ReportLab is required for PDF generation")

        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
        )
        story.append(Paragraph("Robustness Evaluation Report", title_style))
        story.append(Paragraph(f"Model: {report.model_name}", styles['Heading2']))
        story.append(Paragraph(
            f"Generated: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            styles['Normal']
        ))
        story.append(Spacer(1, 0.3 * inch))

        # Overall Assessment
        story.append(Paragraph("Overall Assessment", styles['Heading2']))
        story.append(Paragraph(
            f"Robustness Score: {report.overall_robustness_score:.2%}",
            styles['Normal']
        ))
        story.append(Paragraph(
            f"Severity Level: {report.severity_level.value.upper()}",
            styles['Normal']
        ))
        story.append(Spacer(1, 0.2 * inch))

        # Attack Results
        if report.attack_results:
            story.append(Paragraph("Attack Evaluation Results", styles['Heading2']))

            data = [['Attack Type', 'Success Rate', 'Avg Perturbation', 'Samples']]
            for result in report.attack_results:
                data.append([
                    result.attack_type.value.upper(),
                    f"{result.success_rate:.2%}",
                    f"{result.avg_perturbation:.6f}",
                    str(result.samples_tested)
                ])

            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)
            story.append(Spacer(1, 0.3 * inch))

        # Recommendations
        if report.recommendations:
            story.append(Paragraph("Recommendations", styles['Heading2']))
            for i, rec in enumerate(report.recommendations, 1):
                story.append(Paragraph(f"{i}. {rec}", styles['Normal']))
                story.append(Spacer(1, 0.1 * inch))

        # Executive Summary
        story.append(PageBreak())
        story.append(Paragraph("Executive Summary", styles['Heading2']))
        story.append(Paragraph(self._generate_executive_summary(report), styles['Normal']))

        # Build PDF
        doc.build(story)
        logger.info(f"PDF report generated: {filepath}")

    def generate_comparison_report(
        self,
        reports: Dict[str, RobustnessReport],
        output_format: str = "html"
    ) -> str:
        """Generate comparison report for multiple models

        Args:
            reports: Dictionary mapping model names to their reports
            output_format: Output format ('html' or 'text')

        Returns:
            Formatted comparison report
        """
        if output_format == "html":
            return self._generate_html_comparison(reports)
        else:
            return self._generate_text_comparison(reports)

    def _generate_html_comparison(self, reports: Dict[str, RobustnessReport]) -> str:
        """Generate HTML comparison report"""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Model Robustness Comparison</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: center; }
        th { background: #667eea; color: white; }
        .best { background: #d4edda; }
        .worst { background: #f8d7da; }
    </style>
</head>
<body>
    <h1>Model Robustness Comparison</h1>
    <table>
        <tr>
            <th>Model</th>
            <th>Robustness Score</th>
            <th>Severity</th>
            <th>Avg Attack Success Rate</th>
        </tr>
"""

        # Find best and worst
        scores = {name: r.overall_robustness_score for name, r in reports.items()}
        best_model = max(scores, key=scores.get)
        worst_model = min(scores, key=scores.get)

        for name, report in reports.items():
            avg_success = np.mean([r.success_rate for r in report.attack_results]) if report.attack_results else 0
            css_class = "best" if name == best_model else ("worst" if name == worst_model else "")

            html += f"""
        <tr class="{css_class}">
            <td>{name}</td>
            <td>{report.overall_robustness_score:.2%}</td>
            <td>{report.severity_level.value}</td>
            <td>{avg_success:.2%}</td>
        </tr>
"""

        html += """
    </table>
</body>
</html>
"""
        return html

    def _generate_text_comparison(self, reports: Dict[str, RobustnessReport]) -> str:
        """Generate text comparison report"""
        lines = ["Model Robustness Comparison", "=" * 80]

        for name, report in reports.items():
            avg_success = np.mean([r.success_rate for r in report.attack_results]) if report.attack_results else 0
            lines.append(f"\n{name}:")
            lines.append(f"  Robustness Score: {report.overall_robustness_score:.2%}")
            lines.append(f"  Severity: {report.severity_level.value}")
            lines.append(f"  Avg Attack Success: {avg_success:.2%}")

        return "\n".join(lines)

    def _generate_executive_summary(self, report: RobustnessReport) -> str:
        """Generate executive summary"""
        summary_parts = []

        summary_parts.append(
            f"The model '{report.model_name}' achieved an overall robustness score of "
            f"{report.overall_robustness_score:.1%} with a {report.severity_level.value} severity rating."
        )

        if report.attack_results:
            avg_success = np.mean([r.success_rate for r in report.attack_results])
            summary_parts.append(
                f" Across {len(report.attack_results)} attack type(s), "
                f"the average success rate was {avg_success:.1%}."
            )

        if report.defense_results:
            avg_effectiveness = np.mean([d.effectiveness for d in report.defense_results])
            summary_parts.append(
                f" Defense mechanisms showed an average effectiveness of {avg_effectiveness:.1%}."
            )

        if report.severity_level in [SeverityLevel.HIGH, SeverityLevel.CRITICAL]:
            summary_parts.append(
                " RECOMMENDATION: Immediate action is required to improve model security before production deployment."
            )
        else:
            summary_parts.append(
                " The model demonstrates acceptable robustness for its intended use case."
            )

        return "".join(summary_parts)

    def _generate_charts(self, report: RobustnessReport) -> Dict[str, str]:
        """Generate visualization charts

        Returns:
            Dictionary mapping chart names to base64 encoded images
        """
        charts = {}

        # Attack comparison chart
        if report.attack_results:
            fig, ax = plt.subplots(figsize=(10, 6))
            attack_names = [r.attack_type.value.upper() for r in report.attack_results]
            success_rates = [r.success_rate for r in report.attack_results]

            bars = ax.bar(attack_names, success_rates, color='#dc3545', alpha=0.7)
            ax.set_ylabel('Success Rate', fontsize=12)
            ax.set_title('Attack Success Rates', fontsize=14, fontweight='bold')
            ax.set_ylim(0, 1)
            ax.grid(axis='y', alpha=0.3)

            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1%}',
                       ha='center', va='bottom')

            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150)
            buffer.seek(0)
            charts['attack_comparison'] = base64.b64encode(buffer.read()).decode()
            plt.close(fig)

        # Defense effectiveness chart
        if report.defense_results:
            fig, ax = plt.subplots(figsize=(10, 6))
            defense_names = [d.defense_name for d in report.defense_results]
            effectiveness = [d.effectiveness for d in report.defense_results]

            bars = ax.bar(defense_names, effectiveness, color='#28a745', alpha=0.7)
            ax.set_ylabel('Effectiveness', fontsize=12)
            ax.set_title('Defense Mechanism Effectiveness', fontsize=14, fontweight='bold')
            ax.set_ylim(0, 1)
            ax.grid(axis='y', alpha=0.3)

            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1%}',
                       ha='center', va='bottom')

            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150)
            buffer.seek(0)
            charts['defense_effectiveness'] = base64.b64encode(buffer.read()).decode()
            plt.close(fig)

        return charts

    def _get_severity_color(self, severity: SeverityLevel) -> str:
        """Get color for severity level"""
        colors_map = {
            SeverityLevel.LOW: "#28a745",
            SeverityLevel.MEDIUM: "#ffc107",
            SeverityLevel.HIGH: "#fd7e14",
            SeverityLevel.CRITICAL: "#dc3545"
        }
        return colors_map.get(severity, "#6c757d")
