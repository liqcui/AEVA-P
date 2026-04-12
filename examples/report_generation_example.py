"""
Example: Generate Evaluation Reports

Demonstrates how to generate HTML/PDF/Markdown reports from evaluation results.
"""

from aeva.core.result import EvaluationResult
from aeva.report import ReportGenerator, HTMLTemplate, MarkdownTemplate
from aeva.report.exporters import HTMLExporter, PDFExporter, MarkdownExporter
from datetime import datetime


def create_sample_result() -> EvaluationResult:
    """Create a sample evaluation result for demonstration"""
    result = EvaluationResult(
        model_name="bert-base-chinese",
        status="success"
    )

    # Add metadata
    result.model_version = "v2.1.0"
    result.evaluation_id = "eval_20260411_001"
    result.benchmark = "text_classification_benchmark"
    result.dataset = "CLUE-10K"
    result.timestamp = datetime.now()

    # Add metrics
    result.metrics = {
        'accuracy': 0.942,
        'precision': 0.935,
        'recall': 0.948,
        'f1_score': 0.941,
        'inference_time_ms': 85,
        'throughput': 235.3,
        'latency_p50': 78,
        'latency_p95': 112,
        'latency_p99': 145,
        'memory_mb': 1536,
        'gpu_utilization': 0.65,
        'cpu_utilization': 0.42
    }

    # Add gate result
    result.gate_result = {
        'passed': True,
        'gates': [
            {
                'name': 'Accuracy Gate',
                'passed': True,
                'threshold': 0.90,
                'actual': 0.942
            },
            {
                'name': 'Performance Gate',
                'passed': True,
                'threshold': 100,
                'actual': 85
            },
            {
                'name': 'F1 Score Gate',
                'passed': True,
                'threshold': 0.88,
                'actual': 0.941
            }
        ],
        'blocking_failures': []
    }

    # Add analysis
    result.analysis = {
        'summary': (
            'Model bert-base-chinese v2.1.0 demonstrates excellent performance '
            'with 94.2% accuracy, exceeding the threshold by 4.2 percentage points. '
            'Inference time of 85ms meets real-time requirements. '
            'Minor improvement opportunity identified in intent recognition scenarios.'
        ),
        'root_causes': [
            {
                'category': 'Training Data Quality',
                'status': 'excellent',
                'details': 'Well-balanced training data with high quality samples across multiple domains'
            },
            {
                'category': 'Model Architecture',
                'status': 'appropriate',
                'details': 'BERT-base architecture is well-suited for the task complexity'
            },
            {
                'category': 'Hyperparameters',
                'status': 'optimizable',
                'details': 'Learning rate and batch size are reasonable, but longer training epochs could improve performance'
            }
        ],
        'severity': 'success',
        'confidence': 0.87
    }

    # Add recommendations
    result.recommendations = [
        {
            'priority': 'high',
            'title': 'Enhance Intent Recognition Scenarios',
            'description': 'Intent recognition task shows slightly lower accuracy (88.9%). Recommend targeted improvement.',
            'actions': [
                'Augment training data with 1000+ intent recognition samples',
                'Apply data augmentation techniques',
                'Consider contrastive learning for better discrimination'
            ],
            'expected_improvement': '+3-5% accuracy improvement'
        },
        {
            'priority': 'medium',
            'title': 'Further Performance Optimization',
            'description': 'Current inference speed of 85ms is good, but can be further optimized.',
            'actions': [
                'Explore model distillation to reduce parameters',
                'Enable TensorRT for inference acceleration',
                'Use dynamic batching to improve throughput'
            ],
            'expected_improvement': '20-30% latency reduction'
        },
        {
            'priority': 'medium',
            'title': 'Continuous Monitoring',
            'description': 'Establish continuous evaluation mechanism post-deployment.',
            'actions': [
                'Sample 100 production data points daily for evaluation',
                'Set alert threshold at 92% accuracy',
                'Generate weekly performance trend reports'
            ]
        }
    ]

    result.gate_passed = True
    result.confidence = 0.87

    return result


def generate_html_report():
    """Generate HTML report"""
    print("="*60)
    print("Generating HTML Report")
    print("="*60)

    # Create sample result
    result = create_sample_result()

    # Create generator with custom brand
    generator = ReportGenerator(
        template=HTMLTemplate(),
        language='zh',
        brand_config={
            'name': 'AEVA Platform',
            'primary_color': '#2563eb',
            'secondary_color': '#10b981',
            'footer': 'Generated by AEVA - Algorithm Evaluation & Validation Agent'
        }
    )

    # Generate report
    html_content = generator.generate(
        result=result,
        include_charts=True,
        include_details=True
    )

    # Export to file
    exporter = HTMLExporter()
    output_path = 'reports/bert-base-chinese_evaluation_report.html'
    exporter.export(html_content, output_path)

    print(f"✓ HTML report generated: {output_path}")
    print(f"  Size: {len(html_content)} characters")
    print()


def generate_markdown_report():
    """Generate Markdown report"""
    print("="*60)
    print("Generating Markdown Report")
    print("="*60)

    result = create_sample_result()

    generator = ReportGenerator(
        template=MarkdownTemplate(),
        language='en'
    )

    md_content = generator.generate(result)

    exporter = MarkdownExporter()
    output_path = 'reports/bert-base-chinese_evaluation_report.md'
    exporter.export(md_content, output_path)

    print(f"✓ Markdown report generated: {output_path}")
    print(f"  Size: {len(md_content)} characters")
    print()


def generate_pdf_report():
    """Generate PDF report"""
    print("="*60)
    print("Generating PDF Report")
    print("="*60)

    result = create_sample_result()

    generator = ReportGenerator(
        template=HTMLTemplate(),
        language='zh'
    )

    html_content = generator.generate(result)

    exporter = PDFExporter()
    output_path = 'reports/bert-base-chinese_evaluation_report.pdf'
    exporter.export(html_content, output_path)

    print(f"✓ PDF report generated (or HTML fallback): {output_path}")
    print("  Note: PDF generation requires 'weasyprint' package")
    print("  Install with: pip install weasyprint")
    print()


def generate_comparison_report():
    """Generate comparison report for multiple models"""
    print("="*60)
    print("Generating Model Comparison Report")
    print("="*60)

    # Create results for multiple models
    results = []

    # Model 1: BERT
    bert_result = create_sample_result()
    results.append(bert_result)

    # Model 2: RoBERTa (lower performance)
    roberta_result = EvaluationResult(
        model_name="roberta-large",
        status="warning"
    )
    roberta_result.model_version = "v2.0.0"
    roberta_result.metrics = {
        'accuracy': 0.823,
        'precision': 0.815,
        'recall': 0.831,
        'f1_score': 0.823,
        'inference_time_ms': 250,
        'memory_mb': 2048
    }
    results.append(roberta_result)

    # Model 3: GPT
    gpt_result = EvaluationResult(
        model_name="gpt-sentiment",
        status="success"
    )
    gpt_result.model_version = "v1.5.2"
    gpt_result.metrics = {
        'accuracy': 0.897,
        'precision': 0.892,
        'recall': 0.903,
        'f1_score': 0.897,
        'inference_time_ms': 120,
        'memory_mb': 1800
    }
    results.append(gpt_result)

    # Generate comparison report
    generator = ReportGenerator(language='zh')
    comparison_html = generator.generate_comparison_report(
        results=results,
        output_path='reports/model_comparison_report.html'
    )

    print(f"✓ Comparison report generated: reports/model_comparison_report.html")
    print(f"  Compared {len(results)} models")
    print(f"  Size: {len(comparison_html)} characters")
    print()


def main():
    """Main function"""
    print("\n" + "="*60)
    print("AEVA Report Generation Examples")
    print("="*60 + "\n")

    # Generate different types of reports
    generate_html_report()
    generate_markdown_report()
    generate_pdf_report()
    generate_comparison_report()

    print("="*60)
    print("All Reports Generated Successfully!")
    print("="*60)
    print("\nCheck the 'reports/' directory for generated files.")
    print("\nReport Types:")
    print("  ✓ HTML Report (single model)")
    print("  ✓ Markdown Report (single model)")
    print("  ✓ PDF Report (single model, may fallback to HTML)")
    print("  ✓ Comparison Report (multiple models)")


if __name__ == '__main__':
    main()
