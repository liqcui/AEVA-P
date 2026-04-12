"""
Report Templates for AEVA

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Dict, Any
from abc import ABC, abstractmethod


class ReportTemplate(ABC):
    """Base class for report templates"""

    @abstractmethod
    def render(self, context: Dict[str, Any]) -> str:
        """Render report from context"""
        pass

    @abstractmethod
    def render_comparison(self, context: Dict[str, Any]) -> str:
        """Render comparison report"""
        pass


class HTMLTemplate(ReportTemplate):
    """HTML report template"""

    def render(self, context: Dict[str, Any]) -> str:
        """Render single model report in HTML"""
        metadata = context['metadata']
        summary = context['summary']
        metrics = context['metrics']
        gates = context['gates']
        analysis = context['analysis']
        recommendations = context['recommendations']
        brand = context['brand']

        html = f"""
<!DOCTYPE html>
<html lang="{context['language']}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AEVA Evaluation Report - {metadata['model_name']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        .header {{
            border-bottom: 3px solid {brand['primary_color']};
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}

        .header h1 {{
            color: {brand['primary_color']};
            font-size: 2rem;
            margin-bottom: 10px;
        }}

        .metadata {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
        }}

        .metadata-item {{
            padding: 10px;
        }}

        .metadata-label {{
            font-weight: 600;
            color: #666;
            font-size: 0.9rem;
        }}

        .metadata-value {{
            font-size: 1.1rem;
            color: #333;
            margin-top: 5px;
        }}

        .section {{
            margin-bottom: 40px;
        }}

        .section-title {{
            font-size: 1.5rem;
            color: {brand['primary_color']};
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid {brand['primary_color']};
        }}

        .status {{
            display: inline-block;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 1.1rem;
        }}

        .status-success {{
            background: #10b981;
            color: white;
        }}

        .status-warning {{
            background: #f59e0b;
            color: white;
        }}

        .status-error {{
            background: #ef4444;
            color: white;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}

        .metric-card {{
            background: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}

        .metric-value {{
            font-size: 2.5rem;
            font-weight: 700;
            color: {brand['primary_color']};
        }}

        .metric-label {{
            font-size: 0.9rem;
            color: #666;
            margin-top: 5px;
        }}

        .gate {{
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 4px solid #ddd;
        }}

        .gate-passed {{
            background: #ecfdf5;
            border-color: #10b981;
        }}

        .gate-failed {{
            background: #fef2f2;
            border-color: #ef4444;
        }}

        .recommendation {{
            background: #f0f9ff;
            border-left: 4px solid {brand['primary_color']};
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
        }}

        .recommendation-title {{
            font-weight: 600;
            color: {brand['primary_color']};
            margin-bottom: 10px;
        }}

        .recommendation-actions {{
            margin-top: 10px;
            padding-left: 20px;
        }}

        .recommendation-actions li {{
            margin: 5px 0;
        }}

        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
            font-size: 0.9rem;
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
            background: {brand['primary_color']};
            color: white;
            font-weight: 600;
        }}

        tr:hover {{
            background: #f9f9f9;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{brand['name']} - Evaluation Report</h1>
            <p>Generated: {context['generated_at']}</p>
        </div>

        <!-- Metadata -->
        <div class="metadata">
            <div class="metadata-item">
                <div class="metadata-label">Model Name</div>
                <div class="metadata-value">{metadata['model_name']}</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">Version</div>
                <div class="metadata-value">{metadata['model_version']}</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">Benchmark</div>
                <div class="metadata-value">{metadata['benchmark']}</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">Dataset</div>
                <div class="metadata-value">{metadata['dataset']}</div>
            </div>
        </div>

        <!-- Summary -->
        <div class="section">
            <h2 class="section-title">Executive Summary</h2>
            <p><strong>Overall Status:</strong>
                <span class="status status-{self._get_status_class(summary['overall_status'])}">
                    {summary['overall_status'].upper()}
                </span>
            </p>
            <p style="margin-top: 15px;">
                <strong>Quality Gate:</strong>
                {"✓ PASSED" if summary.get('gate_passed', False) else "✗ FAILED"}
            </p>
        </div>

        <!-- Key Metrics -->
        <div class="section">
            <h2 class="section-title">Key Metrics</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">{summary['key_metrics']['accuracy']:.2%}</div>
                    <div class="metric-label">Accuracy</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{summary['key_metrics']['precision']:.2%}</div>
                    <div class="metric-label">Precision</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{summary['key_metrics']['recall']:.2%}</div>
                    <div class="metric-label">Recall</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{summary['key_metrics']['f1_score']:.2%}</div>
                    <div class="metric-label">F1 Score</div>
                </div>
            </div>
        </div>

        <!-- Performance -->
        <div class="section">
            <h2 class="section-title">Performance</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">{summary['performance']['inference_time']}</div>
                    <div class="metric-label">Inference Time (ms)</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{summary['performance']['throughput']:.1f}</div>
                    <div class="metric-label">Throughput (QPS)</div>
                </div>
            </div>
        </div>

        <!-- Quality Gates -->
        {self._render_gates_section(gates)}

        <!-- Analysis -->
        {self._render_analysis_section(analysis)}

        <!-- Recommendations -->
        {self._render_recommendations_section(recommendations)}

        <div class="footer">
            <p>{brand['footer']}</p>
        </div>
    </div>
</body>
</html>
"""
        return html

    def render_comparison(self, context: Dict[str, Any]) -> str:
        """Render comparison report in HTML"""
        models = context['models']
        comparison = context['comparison']
        brand = context['brand']

        html = f"""
<!DOCTYPE html>
<html lang="{context['language']}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AEVA Model Comparison Report</title>
    <style>
        /* Reuse styles from single report */
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ border-bottom: 3px solid {brand['primary_color']}; padding-bottom: 20px; margin-bottom: 30px; }}
        .header h1 {{ color: {brand['primary_color']}; font-size: 2rem; margin-bottom: 10px; }}
        .section-title {{ font-size: 1.5rem; color: {brand['primary_color']}; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid {brand['primary_color']}; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: {brand['primary_color']}; color: white; font-weight: 600; }}
        tr:hover {{ background: #f9f9f9; }}
        .best {{ background: #10b981; color: white; font-weight: 600; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{brand['name']} - Model Comparison Report</h1>
            <p>Generated: {context['generated_at']}</p>
            <p>Comparing {len(models)} models</p>
        </div>

        <div class="section">
            <h2 class="section-title">Metrics Comparison</h2>
            <table>
                <thead>
                    <tr>
                        <th>Model</th>
                        <th>Accuracy</th>
                        <th>Precision</th>
                        <th>Recall</th>
                        <th>F1 Score</th>
                        <th>Inference Time (ms)</th>
                        <th>Memory (MB)</th>
                        <th>Rank</th>
                    </tr>
                </thead>
                <tbody>
                    {self._render_comparison_rows(comparison)}
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>{brand['footer']}</p>
        </div>
    </div>
</body>
</html>
"""
        return html

    def _get_status_class(self, status: str) -> str:
        """Get CSS class for status"""
        status_lower = status.lower()
        if status_lower in ['success', 'passed']:
            return 'success'
        elif status_lower in ['warning']:
            return 'warning'
        else:
            return 'error'

    def _render_gates_section(self, gates: Dict[str, Any]) -> str:
        """Render quality gates section"""
        if not gates.get('enabled'):
            return ""

        gates_html = '<div class="section"><h2 class="section-title">Quality Gates</h2>'

        for gate in gates.get('gates', []):
            gate_class = 'gate-passed' if gate.get('passed') else 'gate-failed'
            gates_html += f"""
            <div class="gate {gate_class}">
                <strong>{gate.get('name', 'Unknown')}</strong>:
                {"✓ PASSED" if gate.get('passed') else "✗ FAILED"}
                <br>
                <small>Threshold: {gate.get('threshold', 'N/A')} |
                Actual: {gate.get('actual', 'N/A')}</small>
            </div>
            """

        gates_html += '</div>'
        return gates_html

    def _render_analysis_section(self, analysis: Dict[str, Any]) -> str:
        """Render analysis section"""
        if not analysis.get('enabled'):
            return ""

        return f"""
        <div class="section">
            <h2 class="section-title">Intelligent Analysis</h2>
            <p><strong>Summary:</strong> {analysis.get('summary', 'N/A')}</p>
            <p><strong>Confidence:</strong> {analysis.get('confidence', 0):.0%}</p>

            <h3 style="margin-top: 20px; margin-bottom: 10px;">Root Causes</h3>
            <ul>
                {"".join([f"<li><strong>{rc.get('category', 'N/A')}</strong>: {rc.get('details', 'N/A')}</li>" for rc in analysis.get('root_causes', [])])}
            </ul>
        </div>
        """

    def _render_recommendations_section(self, recommendations: list) -> str:
        """Render recommendations section"""
        if not recommendations:
            return ""

        recs_html = '<div class="section"><h2 class="section-title">Recommendations</h2>'

        for idx, rec in enumerate(recommendations, 1):
            recs_html += f"""
            <div class="recommendation">
                <div class="recommendation-title">
                    {idx}. {rec.get('title', 'N/A')}
                    <span style="color: #666; font-size: 0.9rem;">(Priority: {rec.get('priority', 'medium')})</span>
                </div>
                <p>{rec.get('description', '')}</p>
                <ul class="recommendation-actions">
                    {"".join([f"<li>{action}</li>" for action in rec.get('actions', [])])}
                </ul>
                {f"<p style='margin-top: 10px;'><strong>Expected Improvement:</strong> {rec.get('expected_improvement', 'N/A')}</p>" if rec.get('expected_improvement') else ''}
            </div>
            """

        recs_html += '</div>'
        return recs_html

    def _render_comparison_rows(self, comparison: Dict[str, Any]) -> str:
        """Render comparison table rows"""
        metrics = comparison['metrics']
        best = comparison['best_model']
        rankings = comparison['rankings']

        rows = ""
        for model, model_metrics in metrics.items():
            rows += f"""
            <tr>
                <td><strong>{model}</strong></td>
                <td class="{'best' if best.get('accuracy') == model else ''}">{model_metrics['accuracy']:.2%}</td>
                <td class="{'best' if best.get('precision') == model else ''}">{model_metrics['precision']:.2%}</td>
                <td class="{'best' if best.get('recall') == model else ''}">{model_metrics['recall']:.2%}</td>
                <td class="{'best' if best.get('f1_score') == model else ''}">{model_metrics['f1_score']:.2%}</td>
                <td class="{'best' if best.get('inference_time') == model else ''}">{model_metrics['inference_time']:.0f}</td>
                <td class="{'best' if best.get('memory') == model else ''}">{model_metrics['memory']:.0f}</td>
                <td>{rankings.get(model, 'N/A')}</td>
            </tr>
            """

        return rows


class MarkdownTemplate(ReportTemplate):
    """Markdown report template"""

    def render(self, context: Dict[str, Any]) -> str:
        """Render single model report in Markdown"""
        metadata = context['metadata']
        summary = context['summary']
        metrics = context['metrics']

        md = f"""# AEVA Evaluation Report

## Model Information

- **Model Name**: {metadata['model_name']}
- **Version**: {metadata['model_version']}
- **Benchmark**: {metadata['benchmark']}
- **Dataset**: {metadata['dataset']}
- **Generated**: {context['generated_at']}

## Executive Summary

- **Overall Status**: {summary['overall_status'].upper()}
- **Quality Gate**: {"✓ PASSED" if summary.get('gate_passed', False) else "✗ FAILED"}

## Key Metrics

| Metric | Value |
|--------|-------|
| Accuracy | {summary['key_metrics']['accuracy']:.2%} |
| Precision | {summary['key_metrics']['precision']:.2%} |
| Recall | {summary['key_metrics']['recall']:.2%} |
| F1 Score | {summary['key_metrics']['f1_score']:.2%} |

## Performance

| Metric | Value |
|--------|-------|
| Inference Time | {summary['performance']['inference_time']} ms |
| Throughput | {summary['performance']['throughput']:.1f} QPS |

---

*Generated by {context['brand']['footer']}*
"""
        return md

    def render_comparison(self, context: Dict[str, Any]) -> str:
        """Render comparison report in Markdown"""
        comparison = context['comparison']
        metrics = comparison['metrics']

        md = f"""# AEVA Model Comparison Report

Generated: {context['generated_at']}

## Metrics Comparison

| Model | Accuracy | Precision | Recall | F1 Score | Inference Time (ms) | Rank |
|-------|----------|-----------|--------|----------|---------------------|------|
"""

        for model, model_metrics in metrics.items():
            rank = comparison['rankings'].get(model, 'N/A')
            md += f"| {model} | {model_metrics['accuracy']:.2%} | {model_metrics['precision']:.2%} | {model_metrics['recall']:.2%} | {model_metrics['f1_score']:.2%} | {model_metrics['inference_time']:.0f} | {rank} |\n"

        md += f"\n---\n\n*Generated by {context['brand']['footer']}*\n"

        return md
