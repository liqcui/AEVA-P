"""
Model Card Generator

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""
import logging
import json
import base64
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

logger = logging.getLogger(__name__)


class ModelType(Enum):
    """Supported model types"""
    CLASSIFIER = "classifier"
    REGRESSOR = "regressor"
    CLUSTERING = "clustering"
    GENERATIVE = "generative"
    REINFORCEMENT = "reinforcement"
    ENSEMBLE = "ensemble"
    TRANSFORMER = "transformer"
    CNN = "cnn"
    RNN = "rnn"
    OTHER = "other"


class ComplianceFramework(Enum):
    """Regulatory compliance frameworks"""
    GDPR = "gdpr"
    EU_AI_ACT = "eu_ai_act"
    CCPA = "ccpa"
    HIPAA = "hipaa"
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    NIST = "nist"
    NONE = "none"


@dataclass
class TrainingDataInfo:
    """Training data information"""
    description: str = ""
    size: int = 0
    sources: List[str] = field(default_factory=list)
    preprocessing: List[str] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    temporal_coverage: str = ""
    geographical_coverage: str = ""
    demographic_info: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceMetrics:
    """Performance metrics container"""
    primary_metric: str = ""
    metrics: Dict[str, float] = field(default_factory=dict)
    test_set_size: int = 0
    cross_validation: Optional[Dict[str, Any]] = None
    confidence_intervals: Dict[str, Tuple[float, float]] = field(default_factory=dict)


@dataclass
class FairnessMetrics:
    """Fairness metrics and analysis"""
    demographic_parity: Optional[float] = None
    equal_opportunity: Optional[float] = None
    disparate_impact: Optional[float] = None
    protected_attributes: List[str] = field(default_factory=list)
    bias_analysis: str = ""


@dataclass
class ModelCard:
    """Model card data structure"""
    model_name: str
    model_version: str
    model_type: ModelType
    intended_use: str
    training_data: TrainingDataInfo
    performance_metrics: PerformanceMetrics
    limitations: str
    ethical_considerations: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Enhanced fields
    model_architecture: str = ""
    hyperparameters: Dict[str, Any] = field(default_factory=dict)
    training_procedure: str = ""
    out_of_scope_uses: List[str] = field(default_factory=list)
    fairness_metrics: Optional[FairnessMetrics] = None
    environmental_impact: Dict[str, Any] = field(default_factory=dict)
    compliance_frameworks: List[ComplianceFramework] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    authors: List[str] = field(default_factory=list)
    license_info: str = ""


class TemplateEngine:
    """Template engine for model cards"""

    @staticmethod
    def get_html_template() -> str:
        """Get HTML template with styling"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Model Card: {model_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
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
        .header h1 {{
            margin: 0 0 10px 0;
        }}
        .section {{
            background: white;
            padding: 30px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-top: 0;
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
        .badge {{
            display: inline-block;
            padding: 5px 12px;
            background: #667eea;
            color: white;
            border-radius: 15px;
            font-size: 0.9em;
            margin: 5px 5px 5px 0;
        }}
        .warning {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
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
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #555;
        }}
        .footer {{
            text-align: center;
            color: #666;
            padding: 20px;
            font-size: 0.9em;
        }}
        pre {{
            background: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        code {{
            font-family: 'Courier New', monospace;
            color: #c7254e;
            background: #f9f2f4;
            padding: 2px 6px;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
    {content}
    <div class="footer">
        Generated on {timestamp} | AEVA Model Card Generator
    </div>
</body>
</html>
"""

    @staticmethod
    def get_compliance_template(framework: ComplianceFramework) -> str:
        """Get compliance-specific template sections"""
        templates = {
            ComplianceFramework.GDPR: """
## GDPR Compliance

- **Data Protection**: {data_protection}
- **Right to Explanation**: {explainability}
- **Data Retention**: {retention_policy}
- **Cross-border Transfer**: {transfer_mechanism}
""",
            ComplianceFramework.EU_AI_ACT: """
## EU AI Act Compliance

- **Risk Category**: {risk_category}
- **Conformity Assessment**: {conformity_status}
- **Human Oversight**: {oversight_mechanism}
- **Transparency Requirements**: {transparency_measures}
""",
            ComplianceFramework.HIPAA: """
## HIPAA Compliance

- **PHI Handling**: {phi_handling}
- **Access Controls**: {access_controls}
- **Audit Logging**: {audit_mechanism}
- **Encryption**: {encryption_status}
""",
        }
        return templates.get(framework, "")


class ModelCardGenerator:
    """Generate model cards for compliance"""

    def __init__(self, model_name: str = "Model"):
        """Initialize generator

        Args:
            model_name: Name of the model
        """
        self.model_name = model_name
        self.template_engine = TemplateEngine()

    def generate_card(
        self,
        model_version: str = "1.0",
        model_type: ModelType = ModelType.CLASSIFIER,
        intended_use: str = "",
        training_data: Optional[TrainingDataInfo] = None,
        performance_metrics: Optional[PerformanceMetrics] = None,
        limitations: str = "",
        ethical_considerations: str = "",
        **kwargs
    ) -> ModelCard:
        """Generate a model card

        Args:
            model_version: Version of the model
            model_type: Type of model
            intended_use: Intended use description
            training_data: Training data information
            performance_metrics: Performance metrics
            limitations: Known limitations
            ethical_considerations: Ethical considerations
            **kwargs: Additional fields for ModelCard

        Returns:
            ModelCard instance
        """
        return ModelCard(
            model_name=self.model_name,
            model_version=model_version,
            model_type=model_type,
            intended_use=intended_use or "General purpose classification",
            training_data=training_data or TrainingDataInfo(),
            performance_metrics=performance_metrics or PerformanceMetrics(),
            limitations=limitations or "See documentation",
            ethical_considerations=ethical_considerations or "Standard considerations apply",
            **kwargs
        )

    def extract_metrics_from_results(
        self,
        results: Dict[str, Any],
        primary_metric: str = "accuracy"
    ) -> PerformanceMetrics:
        """Automatically extract metrics from evaluation results

        Args:
            results: Dictionary of evaluation results
            primary_metric: Primary metric name

        Returns:
            PerformanceMetrics instance
        """
        metrics = {}
        confidence_intervals = {}

        for key, value in results.items():
            if isinstance(value, (int, float)):
                metrics[key] = float(value)
            elif isinstance(value, dict) and 'mean' in value:
                metrics[key] = value['mean']
                if 'ci' in value:
                    confidence_intervals[key] = value['ci']

        return PerformanceMetrics(
            primary_metric=primary_metric,
            metrics=metrics,
            confidence_intervals=confidence_intervals
        )

    def generate_visualizations(self, card: ModelCard) -> Dict[str, str]:
        """Generate visualization charts as base64 encoded images

        Args:
            card: ModelCard instance

        Returns:
            Dictionary mapping chart names to base64 encoded images
        """
        charts = {}

        # Performance metrics bar chart
        if card.performance_metrics.metrics:
            fig, ax = plt.subplots(figsize=(10, 6))
            metrics = card.performance_metrics.metrics
            names = list(metrics.keys())
            values = list(metrics.values())

            bars = ax.bar(names, values, color='#667eea', alpha=0.8)
            ax.set_ylabel('Score', fontsize=12)
            ax.set_title('Performance Metrics', fontsize=14, fontweight='bold')
            ax.set_ylim(0, 1)
            ax.grid(axis='y', alpha=0.3)

            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom', fontsize=10)

            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            charts['performance_metrics'] = base64.b64encode(buffer.read()).decode()
            plt.close(fig)

        # Fairness metrics radar chart
        if card.fairness_metrics:
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))

            fairness_data = []
            labels = []

            if card.fairness_metrics.demographic_parity is not None:
                fairness_data.append(card.fairness_metrics.demographic_parity)
                labels.append('Demographic Parity')
            if card.fairness_metrics.equal_opportunity is not None:
                fairness_data.append(card.fairness_metrics.equal_opportunity)
                labels.append('Equal Opportunity')
            if card.fairness_metrics.disparate_impact is not None:
                fairness_data.append(min(card.fairness_metrics.disparate_impact, 1.0))
                labels.append('Disparate Impact')

            if fairness_data:
                angles = np.linspace(0, 2 * np.pi, len(fairness_data), endpoint=False).tolist()
                fairness_data += fairness_data[:1]
                angles += angles[:1]

                ax.plot(angles, fairness_data, 'o-', linewidth=2, color='#764ba2')
                ax.fill(angles, fairness_data, alpha=0.25, color='#764ba2')
                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(labels)
                ax.set_ylim(0, 1)
                ax.set_title('Fairness Metrics', fontsize=14, fontweight='bold', pad=20)
                ax.grid(True)

                buffer = BytesIO()
                plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
                buffer.seek(0)
                charts['fairness_metrics'] = base64.b64encode(buffer.read()).decode()
                plt.close(fig)

        return charts

    def export_json(self, card: ModelCard, filepath: str):
        """Export model card to JSON

        Args:
            card: ModelCard instance
            filepath: Output file path
        """
        def default_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, Enum):
                return obj.value
            elif hasattr(obj, '__dict__'):
                return obj.__dict__
            return str(obj)

        with open(filepath, 'w') as f:
            json.dump(asdict(card), f, indent=2, default=default_serializer)
        logger.info(f"Model card exported to {filepath}")

    def export_markdown(self, card: ModelCard, filepath: str):
        """Export model card to Markdown

        Args:
            card: ModelCard instance
            filepath: Output file path
        """
        sections = []

        # Header
        sections.append(f"# Model Card: {card.model_name}\n")
        sections.append(f"**Version:** {card.model_version} | **Type:** {card.model_type.value} | **Generated:** {card.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Model Details
        sections.append("## Model Details\n")
        sections.append(f"- **Model Type:** {card.model_type.value}")
        if card.model_architecture:
            sections.append(f"- **Architecture:** {card.model_architecture}")
        if card.authors:
            sections.append(f"- **Authors:** {', '.join(card.authors)}")
        if card.license_info:
            sections.append(f"- **License:** {card.license_info}")
        sections.append("")

        # Intended Use
        sections.append("## Intended Use\n")
        sections.append(card.intended_use)
        sections.append("")

        if card.out_of_scope_uses:
            sections.append("### Out-of-Scope Uses\n")
            for use in card.out_of_scope_uses:
                sections.append(f"- {use}")
            sections.append("")

        # Training Data
        sections.append("## Training Data\n")
        if card.training_data.description:
            sections.append(card.training_data.description)
        if card.training_data.size > 0:
            sections.append(f"\n**Dataset Size:** {card.training_data.size:,} samples")
        if card.training_data.features:
            sections.append(f"\n**Features:** {', '.join(card.training_data.features)}")
        sections.append("")

        # Performance Metrics
        sections.append("## Performance Metrics\n")
        if card.performance_metrics.primary_metric:
            sections.append(f"**Primary Metric:** {card.performance_metrics.primary_metric}\n")

        sections.append("| Metric | Value |")
        sections.append("|--------|-------|")
        for metric, value in card.performance_metrics.metrics.items():
            sections.append(f"| {metric} | {value:.4f} |")
        sections.append("")

        # Fairness Metrics
        if card.fairness_metrics:
            sections.append("## Fairness Metrics\n")
            if card.fairness_metrics.demographic_parity is not None:
                sections.append(f"- **Demographic Parity:** {card.fairness_metrics.demographic_parity:.4f}")
            if card.fairness_metrics.equal_opportunity is not None:
                sections.append(f"- **Equal Opportunity:** {card.fairness_metrics.equal_opportunity:.4f}")
            if card.fairness_metrics.disparate_impact is not None:
                sections.append(f"- **Disparate Impact:** {card.fairness_metrics.disparate_impact:.4f}")
            if card.fairness_metrics.protected_attributes:
                sections.append(f"\n**Protected Attributes:** {', '.join(card.fairness_metrics.protected_attributes)}")
            sections.append("")

        # Limitations
        sections.append("## Limitations\n")
        sections.append(card.limitations)
        sections.append("")

        # Ethical Considerations
        sections.append("## Ethical Considerations\n")
        sections.append(card.ethical_considerations)
        sections.append("")

        # Environmental Impact
        if card.environmental_impact:
            sections.append("## Environmental Impact\n")
            for key, value in card.environmental_impact.items():
                sections.append(f"- **{key.replace('_', ' ').title()}:** {value}")
            sections.append("")

        # Compliance
        if card.compliance_frameworks:
            sections.append("## Compliance Frameworks\n")
            for framework in card.compliance_frameworks:
                sections.append(f"- {framework.value.upper()}")
            sections.append("")

        # References
        if card.references:
            sections.append("## References\n")
            for i, ref in enumerate(card.references, 1):
                sections.append(f"{i}. {ref}")
            sections.append("")

        md_content = "\n".join(sections)

        with open(filepath, 'w') as f:
            f.write(md_content)
        logger.info(f"Model card exported to {filepath}")

    def export_html(self, card: ModelCard, filepath: str, include_charts: bool = True):
        """Export model card to styled HTML

        Args:
            card: ModelCard instance
            filepath: Output file path
            include_charts: Whether to include visualization charts
        """
        charts = self.generate_visualizations(card) if include_charts else {}

        sections = []

        # Header
        sections.append(f"""
<div class="header">
    <h1>{card.model_name}</h1>
    <p>Version {card.model_version} | {card.model_type.value.title()} Model</p>
</div>
""")

        # Model Details
        sections.append("""
<div class="section">
    <h2>Model Details</h2>
""")
        if card.model_architecture:
            sections.append(f"<p><strong>Architecture:</strong> {card.model_architecture}</p>")
        if card.authors:
            sections.append(f"<p><strong>Authors:</strong> {', '.join(card.authors)}</p>")
        if card.license_info:
            sections.append(f"<p><strong>License:</strong> {card.license_info}</p>")
        if card.compliance_frameworks:
            sections.append("<p><strong>Compliance:</strong> ")
            for framework in card.compliance_frameworks:
                sections.append(f'<span class="badge">{framework.value.upper()}</span>')
            sections.append("</p>")
        sections.append("</div>")

        # Intended Use
        sections.append(f"""
<div class="section">
    <h2>Intended Use</h2>
    <p>{card.intended_use}</p>
""")
        if card.out_of_scope_uses:
            sections.append('<div class="warning"><strong>Out-of-Scope Uses:</strong><ul>')
            for use in card.out_of_scope_uses:
                sections.append(f"<li>{use}</li>")
            sections.append("</ul></div>")
        sections.append("</div>")

        # Performance Metrics
        sections.append("""
<div class="section">
    <h2>Performance Metrics</h2>
""")
        if card.performance_metrics.primary_metric:
            sections.append(f"<p><strong>Primary Metric:</strong> {card.performance_metrics.primary_metric}</p>")

        for metric, value in card.performance_metrics.metrics.items():
            sections.append(f"""
    <div class="metric">
        <span class="metric-name">{metric}:</span>
        <span class="metric-value">{value:.4f}</span>
    </div>
""")

        if 'performance_metrics' in charts:
            sections.append(f"""
    <div class="chart">
        <img src="data:image/png;base64,{charts['performance_metrics']}" alt="Performance Metrics">
    </div>
""")
        sections.append("</div>")

        # Fairness Metrics
        if card.fairness_metrics:
            sections.append("""
<div class="section">
    <h2>Fairness Metrics</h2>
""")
            if card.fairness_metrics.demographic_parity is not None:
                sections.append(f"<p><strong>Demographic Parity:</strong> {card.fairness_metrics.demographic_parity:.4f}</p>")
            if card.fairness_metrics.equal_opportunity is not None:
                sections.append(f"<p><strong>Equal Opportunity:</strong> {card.fairness_metrics.equal_opportunity:.4f}</p>")
            if card.fairness_metrics.disparate_impact is not None:
                sections.append(f"<p><strong>Disparate Impact:</strong> {card.fairness_metrics.disparate_impact:.4f}</p>")

            if 'fairness_metrics' in charts:
                sections.append(f"""
    <div class="chart">
        <img src="data:image/png;base64,{charts['fairness_metrics']}" alt="Fairness Metrics">
    </div>
""")
            sections.append("</div>")

        # Training Data
        sections.append("""
<div class="section">
    <h2>Training Data</h2>
""")
        if card.training_data.description:
            sections.append(f"<p>{card.training_data.description}</p>")
        if card.training_data.size > 0:
            sections.append(f"<p><strong>Dataset Size:</strong> {card.training_data.size:,} samples</p>")
        if card.training_data.features:
            sections.append(f"<p><strong>Features:</strong> {', '.join(card.training_data.features)}</p>")
        sections.append("</div>")

        # Limitations
        sections.append(f"""
<div class="section">
    <h2>Limitations</h2>
    <p>{card.limitations}</p>
</div>
""")

        # Ethical Considerations
        sections.append(f"""
<div class="section">
    <h2>Ethical Considerations</h2>
    <p>{card.ethical_considerations}</p>
</div>
""")

        content = "\n".join(sections)
        html = self.template_engine.get_html_template().format(
            model_name=card.model_name,
            content=content,
            timestamp=card.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        )

        with open(filepath, 'w') as f:
            f.write(html)
        logger.info(f"Model card HTML exported to {filepath}")
