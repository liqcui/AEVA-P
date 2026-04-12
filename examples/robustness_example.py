"""
Robustness Analysis Examples

Demonstrates features of the Robustness framework including:
- Robustness report generation (text, HTML)
- Attack comparison and analysis
- Defense effectiveness evaluation
- Severity level assessment

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aeva.robustness.report import (
    RobustnessReportGenerator,
    AttackType,
    SeverityLevel,
    AttackResult,
    DefenseResult
)


def print_section(title: str):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def example_basic_attack_report():
    """Example 1: Basic Attack Report"""
    print_section("Example 1: Basic Attack Report Generation")

    generator = RobustnessReportGenerator()

    # Simulate attack results
    attack_results = [
        AttackResult(
            attack_type=AttackType.FGSM,
            success_rate=0.65,
            avg_perturbation=0.03,
            samples_tested=1000,
            samples_successful=650,
            epsilon=0.03,
            execution_time=5.2
        )
    ]

    print("\nScenario: Testing model against FGSM attack")
    print(f"  Attack Type: FGSM")
    print(f"  Samples Tested: 1000")
    print(f"  Success Rate: 65%")

    # Generate report
    report = generator.generate_report(
        model_name="Image Classifier v1.0",
        attack_results=attack_results,
        original_accuracy=0.95
    )

    print(f"\n✓ Robustness Report Generated!")
    print(f"  Model: {report.model_name}")
    print(f"  Original Accuracy: {report.original_accuracy:.2%}")
    print(f"  Robustness Score: {report.robustness_score:.1f}/100")
    print(f"  Severity Level: {report.severity_level.value}")

    # Save reports
    text_path = generator.save_report_text(report, "fgsm_attack_report.txt")
    html_path = generator.save_report_html(report, "fgsm_attack_report.html")
    print(f"\n✓ Reports saved:")
    print(f"  Text: {text_path}")
    print(f"  HTML: {html_path}")


def example_multi_attack_comparison():
    """Example 2: Multi-Attack Comparison"""
    print_section("Example 2: Multi-Attack Comparison Report")

    generator = RobustnessReportGenerator()

    # Simulate multiple attack results
    attack_results = [
        AttackResult(
            attack_type=AttackType.FGSM,
            success_rate=0.65,
            avg_perturbation=0.03,
            samples_tested=1000,
            samples_successful=650,
            epsilon=0.03,
            execution_time=5.2
        ),
        AttackResult(
            attack_type=AttackType.PGD,
            success_rate=0.82,
            avg_perturbation=0.05,
            samples_tested=1000,
            samples_successful=820,
            epsilon=0.05,
            execution_time=45.3
        ),
        AttackResult(
            attack_type=AttackType.CW,
            success_rate=0.91,
            avg_perturbation=0.02,
            samples_tested=1000,
            samples_successful=910,
            epsilon=0.0,
            execution_time=125.7
        )
    ]

    print("\nScenario: Testing model against multiple attack types")
    print(f"  Attacks: FGSM, PGD, C&W")
    print(f"  Samples per attack: 1000")

    # Generate comprehensive report
    report = generator.generate_report(
        model_name="ResNet-50 Classifier",
        attack_results=attack_results,
        original_accuracy=0.94
    )

    print(f"\n✓ Multi-Attack Report Generated!")
    print(f"\n📊 Attack Comparison:")

    for result in attack_results:
        print(f"\n  {result.attack_type.value}:")
        print(f"    Success Rate:      {result.success_rate:.1%}")
        print(f"    Avg Perturbation:  {result.avg_perturbation:.4f}")
        print(f"    Execution Time:    {result.execution_time:.1f}s")

    print(f"\n📈 Overall Assessment:")
    print(f"  Original Accuracy:   {report.original_accuracy:.2%}")
    print(f"  Robustness Score:    {report.robustness_score:.1f}/100")
    print(f"  Severity Level:      {report.severity_level.value}")

    if report.recommendations:
        print(f"\n💡 Top Recommendations:")
        for i, rec in enumerate(report.recommendations[:3], 1):
            print(f"    {i}. {rec}")

    # Save reports
    generator.save_report_text(report, "multi_attack_report.txt")
    generator.save_report_html(report, "multi_attack_report.html")
    print(f"\n✓ Reports saved (text and HTML)")


def example_defense_effectiveness():
    """Example 3: Defense Effectiveness Report"""
    print_section("Example 3: Defense Effectiveness Evaluation")

    generator = RobustnessReportGenerator()

    # Simulate attack results after defense
    attack_results = [
        AttackResult(
            attack_type=AttackType.PGD,
            success_rate=0.28,
            avg_perturbation=0.05,
            samples_tested=1000,
            samples_successful=280,
            epsilon=0.05,
            execution_time=45.3
        )
    ]

    # Defense result
    defense_results = [
        DefenseResult(
            defense_type="Adversarial Training",
            original_accuracy=0.94,
            defended_accuracy=0.92,
            attack_success_rate_before=0.85,
            attack_success_rate_after=0.28,
            defense_effectiveness=0.67,
            overhead_ms=5.2,
            robustness_gain=0.57
        )
    ]

    print("\nScenario: Evaluating adversarial training defense")
    print(f"  Defense: Adversarial Training")
    print(f"  Attack: PGD (epsilon=0.05)")

    print(f"\n📊 Before Defense:")
    print(f"  Accuracy:        94.0%")
    print(f"  Attack Success:  85.0%")

    print(f"\n📊 After Defense:")
    print(f"  Accuracy:        92.0% (-2.0%)")
    print(f"  Attack Success:  28.0% (-67.1%)")

    # Generate report
    report = generator.generate_report(
        model_name="Defended Classifier v2.0",
        attack_results=attack_results,
        original_accuracy=0.92,
        defense_results=defense_results
    )

    print(f"\n✓ Defense Effectiveness Report Generated!")
    print(f"  Defense Effectiveness: {defense_results[0].defense_effectiveness:.1%}")
    print(f"  Robustness Gain:       {defense_results[0].robustness_gain:.1%}")
    print(f"  Overhead:              {defense_results[0].overhead_ms:.1f}ms")

    generator.save_report_html(report, "defense_effectiveness_report.html")
    print(f"\n✓ Defense report saved (HTML)")


def example_severity_levels():
    """Example 4: Severity Level Classification"""
    print_section("Example 4: Severity Level Classification")

    generator = RobustnessReportGenerator()

    # Test different severity scenarios
    scenarios = [
        {"name": "Low Severity", "success_rate": 0.15},
        {"name": "Medium Severity", "success_rate": 0.45},
        {"name": "High Severity", "success_rate": 0.72},
        {"name": "Critical Severity", "success_rate": 0.95}
    ]

    print("\nScenario: Classifying attack severity levels")

    for scenario in scenarios:
        attack_results = [
            AttackResult(
                attack_type=AttackType.PGD,
                success_rate=scenario["success_rate"],
                avg_perturbation=0.05,
                samples_tested=1000,
                samples_successful=int(scenario["success_rate"] * 1000),
                epsilon=0.05,
                execution_time=45.0
            )
        ]

        report = generator.generate_report(
            model_name=f"Test Model - {scenario['name']}",
            attack_results=attack_results,
            original_accuracy=0.94
        )

        print(f"\n  {scenario['name']}:")
        print(f"    Success Rate:     {scenario['success_rate']:.1%}")
        print(f"    Severity:         {report.severity_level.value}")
        print(f"    Robustness Score: {report.robustness_score:.1f}/100")


def example_comprehensive_analysis():
    """Example 5: Comprehensive Robustness Analysis"""
    print_section("Example 5: Comprehensive Robustness Analysis")

    generator = RobustnessReportGenerator()

    # Comprehensive attack results
    attack_results = [
        AttackResult(AttackType.FGSM, 0.65, 0.03, 1000, 650, 0.03, 5.2),
        AttackResult(AttackType.PGD, 0.82, 0.05, 1000, 820, 0.05, 45.3),
        AttackResult(AttackType.CW, 0.91, 0.02, 1000, 910, 0.0, 125.7)
    ]

    # Defense results
    defense_results = [
        DefenseResult("Adversarial Training", 0.94, 0.92, 0.82, 0.35, 0.57, 5.2, 0.47),
        DefenseResult("Input Transformation", 0.94, 0.93, 0.82, 0.48, 0.41, 2.1, 0.34)
    ]

    print("\nScenario: Complete robustness analysis with attacks and defenses")

    # Generate report
    report = generator.generate_report(
        model_name="Production Classifier v3.0",
        attack_results=attack_results,
        original_accuracy=0.94,
        defense_results=defense_results
    )

    print(f"\n{'='*70}")
    print("  COMPREHENSIVE ROBUSTNESS ANALYSIS REPORT")
    print(f"{'='*70}")

    print(f"\n📋 Model Information:")
    print(f"  Name:              {report.model_name}")
    print(f"  Original Accuracy: {report.original_accuracy:.2%}")
    print(f"  Robustness Score:  {report.robustness_score:.1f}/100")
    print(f"  Severity Level:    {report.severity_level.value}")

    print(f"\n⚔️  Attack Results:")
    for result in attack_results:
        print(f"\n  {result.attack_type.value}:")
        print(f"    Success Rate:      {result.success_rate:.1%}")
        print(f"    Avg Perturbation:  {result.avg_perturbation:.4f}")
        print(f"    Samples Affected:  {result.samples_successful}/{result.samples_tested}")

    print(f"\n🛡️  Defense Results:")
    for defense in defense_results:
        print(f"\n  {defense.defense_type}:")
        print(f"    Effectiveness:     {defense.defense_effectiveness:.1%}")
        print(f"    Robustness Gain:   {defense.robustness_gain:.1%}")

    # Save reports
    generator.save_report_text(report, "comprehensive_analysis.txt")
    generator.save_report_html(report, "comprehensive_analysis.html")

    print(f"\n✓ Comprehensive analysis complete!")


def main():
    """Run all examples"""
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 12 + "AEVA Robustness Analysis Examples" + " " * 19 + "║")
    print("╚" + "=" * 68 + "╝")

    examples = [
        example_basic_attack_report,
        example_multi_attack_comparison,
        example_defense_effectiveness,
        example_severity_levels,
        example_comprehensive_analysis
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
    print("\nGenerated Files:")
    print("  • fgsm_attack_report.txt/html")
    print("  • multi_attack_report.txt/html")
    print("  • defense_effectiveness_report.html")
    print("  • comprehensive_analysis.txt/html")


if __name__ == "__main__":
    main()
