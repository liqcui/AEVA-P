"""
Model Cards System Examples

Demonstrates all features of the enhanced Model Cards framework including:
- Model card generation with automated metrics
- Model card validation and compliance checking
- Template engine with HTML/CSS styling
- Compliance frameworks (GDPR, EU AI Act, HIPAA)
- Multi-format export (JSON, Markdown, HTML)
- Fairness and performance metrics

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aeva.model_cards import (
    ModelCardGenerator,
    ModelCardValidator,
    ModelType,
    ComplianceFramework,
    TrainingDataInfo,
    PerformanceMetrics,
    FairnessMetrics,
    ValidationLevel,
    ComplianceStandard
)


def print_section(title: str):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def example_basic_model_card():
    """Example 1: Basic Model Card Generation"""
    print_section("Example 1: Basic Model Card Generation")

    generator = ModelCardGenerator()

    # Create training data info
    training_data = TrainingDataInfo(
        name="Customer Purchase Dataset",
        description="Historical customer purchase data from 2020-2025",
        source="Internal database",
        size=100000,
        preprocessing="Normalized numerical features, one-hot encoded categories"
    )

    # Create performance metrics
    performance = PerformanceMetrics(
        accuracy=0.87,
        precision=0.85,
        recall=0.82,
        f1_score=0.835,
        additional_metrics={
            "auc_roc": 0.91,
            "avg_precision": 0.88
        }
    )

    print("\nScenario: Creating model card for customer churn prediction model")

    card = generator.create_model_card(
        model_name="Customer Churn Predictor v1.0",
        model_type=ModelType.CLASSIFICATION,
        description="Binary classification model to predict customer churn risk",
        version="1.0.0",
        authors=["Data Science Team"],
        training_data=training_data,
        performance=performance
    )

    print(f"\n✓ Model Card Created!")
    print(f"  Model: {card['model_name']}")
    print(f"  Version: {card['version']}")
    print(f"  Type: {card['model_type']}")
    print(f"  Accuracy: {card['performance']['accuracy']:.2%}")

    # Export to JSON
    json_path = generator.export_json(card, "customer_churn_model_card.json")
    print(f"\n✓ Exported to JSON: {json_path}")

    # Export to Markdown
    md_path = generator.export_markdown(card, "customer_churn_model_card.md")
    print(f"✓ Exported to Markdown: {md_path}")


def example_compliance_model_card():
    """Example 2: Model Card with Compliance Framework"""
    print_section("Example 2: Model Card with GDPR Compliance")

    generator = ModelCardGenerator()

    # Create comprehensive training data info
    training_data = TrainingDataInfo(
        name="Medical Diagnosis Dataset",
        description="De-identified patient records for disease prediction",
        source="Hospital partners (anonymized)",
        size=50000,
        preprocessing="PII removed, HIPAA-compliant anonymization",
        privacy_considerations="All patient data anonymized per GDPR Article 25"
    )

    # Create performance metrics with demographic breakdown
    performance = PerformanceMetrics(
        accuracy=0.92,
        precision=0.90,
        recall=0.88,
        f1_score=0.89,
        additional_metrics={
            "sensitivity": 0.88,
            "specificity": 0.94
        }
    )

    # Create fairness metrics
    fairness = FairnessMetrics(
        demographic_parity_diff=0.03,
        equal_opportunity_diff=0.04,
        groups_evaluated=["age", "gender", "ethnicity"],
        mitigation_strategies=["Re-weighting", "Threshold optimization"]
    )

    print("\nScenario: Healthcare AI model with GDPR compliance")

    card = generator.create_model_card(
        model_name="Disease Risk Predictor",
        model_type=ModelType.CLASSIFICATION,
        description="Predicts disease risk based on patient symptoms and history",
        version="2.1.0",
        authors=["Medical AI Team", "Clinical Partners"],
        training_data=training_data,
        performance=performance,
        fairness_metrics=fairness,
        intended_use="Clinical decision support tool for physicians",
        limitations="Not approved for autonomous diagnosis; requires physician oversight",
        ethical_considerations="Potential bias in training data from limited geographic regions"
    )

    # Add compliance template
    card_with_compliance = generator.add_compliance_template(
        card,
        ComplianceFramework.GDPR
    )

    print(f"\n✓ GDPR-Compliant Model Card Created!")
    print(f"  Model: {card_with_compliance['model_name']}")
    print(f"  Compliance Framework: GDPR")
    print(f"  Privacy Considerations: {card_with_compliance['training_data']['privacy_considerations']}")
    print(f"  Fairness Metrics:")
    print(f"    - Demographic Parity Diff: {fairness.demographic_parity_diff:.3f}")
    print(f"    - Equal Opportunity Diff: {fairness.equal_opportunity_diff:.3f}")

    # Export to HTML with styling
    html_path = generator.export_html(
        card_with_compliance,
        "disease_risk_model_card.html"
    )
    print(f"\n✓ Exported to HTML: {html_path}")


def example_eu_ai_act_compliance():
    """Example 3: EU AI Act High-Risk System"""
    print_section("Example 3: EU AI Act High-Risk System Compliance")

    generator = ModelCardGenerator()

    training_data = TrainingDataInfo(
        name="Loan Application Dataset",
        description="Historical loan application and repayment data",
        source="Financial institution records (2015-2024)",
        size=250000,
        preprocessing="Feature engineering, bias mitigation applied",
        privacy_considerations="GDPR-compliant data handling"
    )

    performance = PerformanceMetrics(
        accuracy=0.85,
        precision=0.83,
        recall=0.80,
        f1_score=0.815,
        additional_metrics={
            "approval_rate": 0.42,
            "default_rate": 0.08
        }
    )

    fairness = FairnessMetrics(
        demographic_parity_diff=0.05,
        equal_opportunity_diff=0.06,
        groups_evaluated=["gender", "age_group", "geographic_region"],
        mitigation_strategies=[
            "Adversarial debiasing",
            "Fairness constraints during training",
            "Post-processing calibration"
        ]
    )

    print("\nScenario: Credit scoring model (EU AI Act high-risk category)")

    card = generator.create_model_card(
        model_name="Credit Risk Assessment System",
        model_type=ModelType.CLASSIFICATION,
        description="Automated credit scoring for loan applications",
        version="3.0.0",
        authors=["Risk Analytics Team"],
        training_data=training_data,
        performance=performance,
        fairness_metrics=fairness,
        intended_use="Automated credit decisioning for consumer loans",
        limitations="Requires human review for applications outside normal parameters",
        ethical_considerations="High-risk AI system per EU AI Act Article 6",
        risk_assessment="Potential for discriminatory outcomes; fairness monitoring required"
    )

    # Add EU AI Act compliance template
    card_with_eu = generator.add_compliance_template(
        card,
        ComplianceFramework.EU_AI_ACT
    )

    print(f"\n✓ EU AI Act Compliant Model Card Created!")
    print(f"  Model: {card_with_eu['model_name']}")
    print(f"  Risk Category: High-Risk (Credit Scoring)")
    print(f"  Compliance Framework: EU AI Act")
    print(f"  Risk Assessment: {card_with_eu.get('risk_assessment', 'N/A')}")
    print(f"  Fairness Mitigation: {len(fairness.mitigation_strategies)} strategies applied")

    # Export all formats
    generator.export_json(card_with_eu, "credit_risk_model_card.json")
    generator.export_markdown(card_with_eu, "credit_risk_model_card.md")
    generator.export_html(card_with_eu, "credit_risk_model_card.html")

    print(f"\n✓ Exported in all formats (JSON, Markdown, HTML)")


def example_model_card_validation():
    """Example 4: Model Card Validation"""
    print_section("Example 4: Model Card Validation and Quality Scoring")

    generator = ModelCardGenerator()
    validator = ModelCardValidator()

    # Create a minimal model card (will have validation issues)
    print("\nScenario 1: Validating incomplete model card")

    incomplete_card = {
        "model_name": "Simple Classifier",
        "model_type": "classification",
        "version": "1.0"
        # Missing many required fields
    }

    report = validator.validate(incomplete_card)

    print(f"\n✓ Validation Report:")
    print(f"  Valid: {report.is_valid}")
    print(f"  Completeness Score: {report.completeness_score:.1f}%")
    print(f"  Total Issues: {len(report.issues)}")

    # Show issues by level
    errors = [i for i in report.issues if i.level == ValidationLevel.ERROR]
    warnings = [i for i in report.issues if i.level == ValidationLevel.WARNING]

    print(f"\n  Errors ({len(errors)}):")
    for issue in errors[:3]:  # Show first 3
        print(f"    - {issue.message}")

    print(f"\n  Warnings ({len(warnings)}):")
    for issue in warnings[:3]:  # Show first 3
        print(f"    - {issue.message}")

    if report.recommendations:
        print(f"\n  Top Recommendations:")
        for rec in report.recommendations[:3]:
            print(f"    • {rec}")

    # Now validate a complete model card
    print("\n\nScenario 2: Validating complete model card")

    complete_card = generator.create_model_card(
        model_name="Complete Classification Model",
        model_type=ModelType.CLASSIFICATION,
        description="A well-documented classification model with comprehensive metrics",
        version="1.0.0",
        authors=["ML Team"],
        training_data=TrainingDataInfo(
            name="Training Dataset",
            description="Comprehensive dataset with diverse samples",
            source="Public repository",
            size=100000,
            preprocessing="Standard normalization and feature engineering"
        ),
        performance=PerformanceMetrics(
            accuracy=0.90,
            precision=0.88,
            recall=0.87,
            f1_score=0.875
        ),
        intended_use="Production classification system",
        limitations="Performance may degrade on out-of-distribution data",
        ethical_considerations="Regular bias audits recommended"
    )

    report2 = validator.validate(complete_card)

    print(f"\n✓ Validation Report:")
    print(f"  Valid: {report2.is_valid}")
    print(f"  Completeness Score: {report2.completeness_score:.1f}%")
    print(f"  Total Issues: {len(report2.issues)}")

    if report2.is_valid:
        print(f"\n  ✓ Model card meets all validation requirements!")


def example_compliance_validation():
    """Example 5: Compliance-Specific Validation"""
    print_section("Example 5: Compliance-Specific Validation (GDPR)")

    generator = ModelCardGenerator()
    validator = ModelCardValidator()

    # Create model card with some compliance info
    card = generator.create_model_card(
        model_name="User Behavior Predictor",
        model_type=ModelType.CLASSIFICATION,
        description="Predicts user behavior patterns",
        version="1.5.0",
        authors=["Analytics Team"],
        training_data=TrainingDataInfo(
            name="User Interaction Data",
            description="Anonymized user interaction logs",
            source="Application database",
            size=500000,
            preprocessing="PII removal, aggregation",
            privacy_considerations="GDPR Article 25 - data minimization applied"
        ),
        performance=PerformanceMetrics(
            accuracy=0.82,
            precision=0.80,
            recall=0.78,
            f1_score=0.79
        )
    )

    print("\nScenario: Validating GDPR compliance for user data model")

    # Validate with GDPR standard
    report = validator.validate_compliance(card, ComplianceStandard.GDPR)

    print(f"\n✓ GDPR Compliance Validation:")
    print(f"  Compliant: {report.is_valid}")
    print(f"  Compliance Score: {report.completeness_score:.1f}%")

    # Check for specific GDPR issues
    gdpr_issues = [i for i in report.issues if "GDPR" in i.message or "privacy" in i.message.lower()]

    if gdpr_issues:
        print(f"\n  GDPR-Related Issues ({len(gdpr_issues)}):")
        for issue in gdpr_issues:
            print(f"    [{issue.level.value}] {issue.message}")

    if report.recommendations:
        print(f"\n  GDPR Recommendations:")
        for rec in report.recommendations[:5]:
            print(f"    • {rec}")


def example_quality_scoring():
    """Example 6: Quality Scoring and Improvement"""
    print_section("Example 6: Model Card Quality Scoring")

    validator = ModelCardValidator()

    # Create cards with different quality levels
    cards = {
        "Minimal": {
            "model_name": "Model A",
            "model_type": "classification",
            "version": "1.0"
        },
        "Basic": {
            "model_name": "Model B",
            "model_type": "classification",
            "version": "1.0",
            "description": "A basic classification model",
            "authors": ["Team A"],
            "performance": {
                "accuracy": 0.85
            }
        },
        "Complete": {
            "model_name": "Model C",
            "model_type": "classification",
            "version": "1.0",
            "description": "A comprehensive classification model with full documentation",
            "authors": ["Team C", "External Reviewers"],
            "training_data": {
                "name": "Dataset C",
                "description": "High-quality labeled dataset",
                "source": "Curated repository",
                "size": 100000,
                "preprocessing": "Advanced feature engineering"
            },
            "performance": {
                "accuracy": 0.90,
                "precision": 0.88,
                "recall": 0.87,
                "f1_score": 0.875
            },
            "fairness_metrics": {
                "demographic_parity_diff": 0.03,
                "equal_opportunity_diff": 0.04,
                "groups_evaluated": ["age", "gender"]
            },
            "intended_use": "Production deployment for classification tasks",
            "limitations": "May not generalize to unseen domains",
            "ethical_considerations": "Regular audits for bias recommended"
        }
    }

    print("\nScenario: Comparing quality scores of different model cards\n")

    results = []
    for name, card in cards.items():
        report = validator.validate(card)
        results.append((name, report.completeness_score, len(report.issues)))

        print(f"{name} Model Card:")
        print(f"  Completeness Score: {report.completeness_score:.1f}%")
        print(f"  Issues Found: {len(report.issues)}")
        print(f"  Valid: {'✓' if report.is_valid else '✗'}")
        print()

    # Show ranking
    results.sort(key=lambda x: x[1], reverse=True)
    print("\n📊 Quality Ranking:")
    for i, (name, score, issues) in enumerate(results, 1):
        print(f"  {i}. {name}: {score:.1f}% ({issues} issues)")


def example_template_engine():
    """Example 7: Template Engine and HTML Generation"""
    print_section("Example 7: Template Engine and Professional HTML Export")

    generator = ModelCardGenerator()

    # Create a feature-rich model card
    card = generator.create_model_card(
        model_name="Advanced Recommendation Engine",
        model_type=ModelType.RECOMMENDATION,
        description="Personalized product recommendation system using collaborative filtering and deep learning",
        version="4.2.0",
        authors=["ML Platform Team", "Personalization Team"],
        training_data=TrainingDataInfo(
            name="User-Product Interaction Dataset",
            description="5 years of user browsing and purchase history",
            source="E-commerce platform logs",
            size=10000000,
            preprocessing="Session aggregation, negative sampling, feature normalization"
        ),
        performance=PerformanceMetrics(
            accuracy=0.88,
            precision=0.85,
            recall=0.82,
            f1_score=0.835,
            additional_metrics={
                "ndcg@10": 0.75,
                "hit_rate@10": 0.68,
                "coverage": 0.45
            }
        ),
        fairness_metrics=FairnessMetrics(
            demographic_parity_diff=0.04,
            equal_opportunity_diff=0.05,
            groups_evaluated=["age_group", "region", "user_segment"]
        ),
        intended_use="Real-time product recommendations on e-commerce platform",
        limitations="Cold start problem for new users and products",
        ethical_considerations="Filter bubble concerns; diversity promotion implemented"
    )

    print("\nScenario: Generating professional HTML model card with styling")

    # Export to HTML
    html_path = generator.export_html(card, "recommendation_engine_card.html")

    print(f"\n✓ HTML Model Card Generated!")
    print(f"  Output: {html_path}")
    print(f"  Features:")
    print(f"    • Professional CSS styling")
    print(f"    • Responsive layout")
    print(f"    • Structured sections")
    print(f"    • Performance metrics table")
    print(f"    • Fairness metrics visualization")
    print(f"\n  Open the HTML file in a browser to view the styled card!")


def main():
    """Run all examples"""
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "AEVA Model Cards System Examples" + " " * 20 + "║")
    print("╚" + "=" * 68 + "╝")

    examples = [
        example_basic_model_card,
        example_compliance_model_card,
        example_eu_ai_act_compliance,
        example_model_card_validation,
        example_compliance_validation,
        example_quality_scoring,
        example_template_engine
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
    print("  • customer_churn_model_card.json")
    print("  • customer_churn_model_card.md")
    print("  • disease_risk_model_card.html")
    print("  • credit_risk_model_card.json/md/html")
    print("  • recommendation_engine_card.html")


if __name__ == "__main__":
    main()
