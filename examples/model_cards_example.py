"""
Model Cards System Examples

Demonstrates features of the Model Cards framework including:
- Model card generation
- Model card validation
- Multi-format export (JSON, Markdown, HTML)
- Fairness metrics

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aeva.model_cards import (
    ModelCardGenerator,
    ModelCardValidator,
    ModelType,
    TrainingDataInfo,
    PerformanceMetrics,
    FairnessMetrics
)


def print_section(title: str):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def example_basic_model_card():
    """Example 1: Basic Model Card Generation"""
    print_section("Example 1: Basic Model Card Generation")

    generator = ModelCardGenerator(model_name="Customer Churn Predictor")

    # Create training data info
    training_data = TrainingDataInfo(
        description="Historical customer purchase data from 2020-2025",
        size=100000,
        sources=["Internal database", "CRM system"],
        preprocessing=["Normalized numerical features", "One-hot encoded categories"]
    )

    # Create performance metrics
    performance = PerformanceMetrics(
        primary_metric="accuracy",
        metrics={
            "accuracy": 0.87,
            "precision": 0.85,
            "recall": 0.82,
            "f1_score": 0.835,
            "auc_roc": 0.91
        },
        test_set_size=10000
    )

    print("\nScenario: Creating model card for customer churn prediction model")

    card = generator.generate_card(
        model_version="1.0.0",
        model_type=ModelType.CLASSIFIER,
        intended_use="Binary classification model to predict customer churn risk",
        training_data=training_data,
        performance_metrics=performance
    )

    print(f"\n✓ Model Card Created!")
    print(f"  Model: {card.model_name}")
    print(f"  Version: {card.model_version}")
    print(f"  Type: {card.model_type}")
    print(f"  Primary Metric: {performance.primary_metric} = {performance.metrics.get('accuracy', 0):.2%}")

    # Export to JSON
    json_path = generator.export_json(card, "customer_churn_model_card.json")
    print(f"\n✓ Exported to JSON: {json_path}")

    # Export to Markdown
    md_path = generator.export_markdown(card, "customer_churn_model_card.md")
    print(f"✓ Exported to Markdown: {md_path}")


def example_fairness_metrics():
    """Example 2: Model Card with Fairness Metrics"""
    print_section("Example 2: Model Card with Fairness Metrics")

    generator = ModelCardGenerator(model_name="Loan Approval Model")

    # Create fairness metrics
    fairness = FairnessMetrics(
        demographic_parity=0.95,
        equal_opportunity=0.92,
        disparate_impact=0.88,
        protected_attributes=["age", "gender", "geographic_region"]
    )

    training_data = TrainingDataInfo(
        description="Loan application and repayment history",
        size=250000,
        sources=["Financial institution records"],
        preprocessing=["Feature engineering", "Bias mitigation applied"]
    )

    performance = PerformanceMetrics(
        primary_metric="f1_score",
        metrics={
            "accuracy": 0.85,
            "precision": 0.83,
            "recall": 0.80,
            "f1_score": 0.815
        },
        test_set_size=25000
    )

    print("\nScenario: Creating model card with fairness considerations")

    card = generator.generate_card(
        model_version="3.0.0",
        model_type=ModelType.CLASSIFIER,
        intended_use="Automated credit scoring for loan applications",
        training_data=training_data,
        performance_metrics=performance,
        fairness_metrics=fairness,
        limitations="Requires human review for applications outside normal parameters",
        ethical_considerations="Regular fairness audits recommended"
    )

    print(f"\n✓ Model Card with Fairness Metrics Created!")
    print(f"  Model: {card.model_name}")
    print(f"  Protected Attributes: {', '.join(fairness.protected_attributes)}")
    print(f"  Demographic Parity: {fairness.demographic_parity:.2%}")
    print(f"  Equal Opportunity: {fairness.equal_opportunity:.2%}")

    # Export
    generator.export_json(card, "loan_approval_model_card.json")
    generator.export_html(card, "loan_approval_model_card.html")
    print(f"\n✓ Exported to JSON and HTML")


def example_model_card_validation():
    """Example 3: Model Card Validation"""
    print_section("Example 3: Model Card Validation")

    generator = ModelCardGenerator(model_name="Test Model")
    validator = ModelCardValidator()

    print("\nScenario 1: Validating minimal model card")

    # Create a minimal card
    minimal_card = generator.generate_card(
        model_version="1.0",
        model_type=ModelType.CLASSIFIER
    )

    # Convert to dict for validation
    card_dict = {
        "model_name": minimal_card.model_name,
        "model_version": minimal_card.model_version,
        "model_type": minimal_card.model_type.value if hasattr(minimal_card.model_type, 'value') else str(minimal_card.model_type),
        "intended_use": minimal_card.intended_use
    }

    report = validator.validate(card_dict)

    print(f"\n✓ Validation Report:")
    print(f"  Valid: {report.is_valid}")
    print(f"  Completeness Score: {report.completeness_score:.1f}%")
    print(f"  Total Issues: {len(report.issues)}")

    if report.issues:
        print(f"\n  First 3 Issues:")
        for issue in report.issues[:3]:
            print(f"    [{issue.level.value}] {issue.message}")

    # Now validate a complete model card
    print("\n\nScenario 2: Validating complete model card")

    complete_card = generator.generate_card(
        model_version="2.0.0",
        model_type=ModelType.CLASSIFIER,
        intended_use="Production classification system",
        training_data=TrainingDataInfo(
            description="Comprehensive training dataset",
            size=100000,
            sources=["Public repository"]
        ),
        performance_metrics=PerformanceMetrics(
            primary_metric="accuracy",
            metrics={"accuracy": 0.90, "f1_score": 0.88},
            test_set_size=10000
        ),
        limitations="Performance may degrade on out-of-distribution data",
        ethical_considerations="Regular bias audits recommended"
    )

    complete_dict = {
        "model_name": complete_card.model_name,
        "model_version": complete_card.model_version,
        "model_type": complete_card.model_type.value if hasattr(complete_card.model_type, 'value') else str(complete_card.model_type),
        "intended_use": complete_card.intended_use,
        "limitations": complete_card.limitations,
        "ethical_considerations": complete_card.ethical_considerations
    }

    report2 = validator.validate(complete_dict)

    print(f"\n✓ Validation Report:")
    print(f"  Valid: {report2.is_valid}")
    print(f"  Completeness Score: {report2.completeness_score:.1f}%")
    print(f"  Total Issues: {len(report2.issues)}")


def example_html_export():
    """Example 4: HTML Export with Styling"""
    print_section("Example 4: Professional HTML Export")

    generator = ModelCardGenerator(model_name="Recommendation Engine")

    training_data = TrainingDataInfo(
        description="User-product interaction dataset with 5 years of history",
        size=10000000,
        sources=["E-commerce platform logs"],
        preprocessing=["Session aggregation", "Negative sampling", "Feature normalization"]
    )

    performance = PerformanceMetrics(
        primary_metric="ndcg@10",
        metrics={
            "ndcg@10": 0.75,
            "hit_rate@10": 0.68,
            "coverage": 0.45,
            "diversity": 0.62
        },
        test_set_size=500000
    )

    print("\nScenario: Generating professional HTML model card")

    card = generator.generate_card(
        model_version="4.2.0",
        model_type=ModelType.TRANSFORMER,
        intended_use="Real-time product recommendations on e-commerce platform",
        training_data=training_data,
        performance_metrics=performance,
        limitations="Cold start problem for new users and products",
        ethical_considerations="Diversity promotion implemented to avoid filter bubbles"
    )

    # Export to HTML with charts
    html_path = generator.export_html(card, "recommendation_engine_card.html", include_charts=True)

    print(f"\n✓ HTML Model Card Generated!")
    print(f"  Output: {html_path}")
    print(f"  Features:")
    print(f"    • Professional CSS styling")
    print(f"    • Responsive layout")
    print(f"    • Performance metrics display")
    print(f"\n  Open the HTML file in a browser to view the styled card!")


def example_multiple_exports():
    """Example 5: Exporting to Multiple Formats"""
    print_section("Example 5: Exporting to Multiple Formats")

    generator = ModelCardGenerator(model_name="Fraud Detection System")

    training_data = TrainingDataInfo(
        description="Transaction data with fraud labels",
        size=5000000,
        sources=["Payment processing system", "Fraud investigation database"],
        preprocessing=["Anonymization", "Feature engineering", "SMOTE for imbalance"]
    )

    performance = PerformanceMetrics(
        primary_metric="precision",
        metrics={
            "precision": 0.93,
            "recall": 0.89,
            "f1_score": 0.91,
            "accuracy": 0.98,
            "false_positive_rate": 0.01
        },
        test_set_size=500000
    )

    fairness = FairnessMetrics(
        demographic_parity=0.94,
        equal_opportunity=0.96,
        protected_attributes=["merchant_category", "geographic_region"]
    )

    print("\nScenario: Exporting model card in all formats")

    card = generator.generate_card(
        model_version="5.1.0",
        model_type=ModelType.CLASSIFIER,
        intended_use="Real-time fraud detection for payment transactions",
        training_data=training_data,
        performance_metrics=performance,
        fairness_metrics=fairness,
        limitations="May require additional rules for novel fraud patterns",
        ethical_considerations="Balance between fraud prevention and customer friction"
    )

    # Export to all formats
    json_path = generator.export_json(card, "fraud_detection_card.json")
    md_path = generator.export_markdown(card, "fraud_detection_card.md")
    html_path = generator.export_html(card, "fraud_detection_card.html")

    print(f"\n✓ Model Card Exported to All Formats!")
    print(f"  JSON:     {json_path}")
    print(f"  Markdown: {md_path}")
    print(f"  HTML:     {html_path}")


def main():
    """Run all examples"""
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "AEVA Model Cards System Examples" + " " * 20 + "║")
    print("╚" + "=" * 68 + "╝")

    examples = [
        example_basic_model_card,
        example_fairness_metrics,
        example_model_card_validation,
        example_html_export,
        example_multiple_exports
    ]

    for i, example in enumerate(examples, 1):
        try:
            example()
        except Exception as e:
            print(f"\n❌ Error in example {i}: {str(e)}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 70)
    print("All examples completed!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  • customer_churn_model_card.json/md")
    print("  • loan_approval_model_card.json/html")
    print("  • recommendation_engine_card.html")
    print("  • fraud_detection_card.json/md/html")


if __name__ == "__main__":
    main()
