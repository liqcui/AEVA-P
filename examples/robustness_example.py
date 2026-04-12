"""
Robustness Analysis Examples

Demonstrates all features of the enhanced Robustness framework including:
- Robustness report generation (text, HTML, PDF)
- 10+ visualization types
- Attack comparison and analysis
- Defense effectiveness evaluation
- Severity level assessment
- Executive summaries

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aeva.robustness import (
    RobustnessReportGenerator,
    RobustnessVisualizer,
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
            avg_confidence_drop=0.35,
            samples_tested=1000,
            samples_successful=650
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

    # Save text report
    text_path = generator.save_report_text(report, "fgsm_attack_report.txt")
    print(f"\n✓ Text report saved: {text_path}")

    # Save HTML report
    html_path = generator.save_report_html(report, "fgsm_attack_report.html")
    print(f"✓ HTML report saved: {html_path}")


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
            avg_confidence_drop=0.35,
            samples_tested=1000,
            samples_successful=650
        ),
        AttackResult(
            attack_type=AttackType.PGD,
            success_rate=0.82,
            avg_perturbation=0.05,
            avg_confidence_drop=0.48,
            samples_tested=1000,
            samples_successful=820
        ),
        AttackResult(
            attack_type=AttackType.CW,
            success_rate=0.91,
            avg_perturbation=0.02,
            avg_confidence_drop=0.62,
            samples_tested=1000,
            samples_successful=910
        ),
        AttackResult(
            attack_type=AttackType.DEEPFOOL,
            success_rate=0.74,
            avg_perturbation=0.04,
            avg_confidence_drop=0.41,
            samples_tested=1000,
            samples_successful=740
        )
    ]

    print("\nScenario: Testing model against 4 different attack types")
    print(f"  Attacks: FGSM, PGD, C&W, DeepFool")
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
        print(f"    Success Rate:        {result.success_rate:.1%}")
        print(f"    Avg Perturbation:    {result.avg_perturbation:.4f}")
        print(f"    Confidence Drop:     {result.avg_confidence_drop:.1%}")

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

    # Simulate attack results before defense
    attack_results_before = [
        AttackResult(
            attack_type=AttackType.PGD,
            success_rate=0.85,
            avg_perturbation=0.05,
            avg_confidence_drop=0.52,
            samples_tested=1000,
            samples_successful=850
        )
    ]

    # Simulate attack results after defense
    attack_results_after = [
        AttackResult(
            attack_type=AttackType.PGD,
            success_rate=0.28,
            avg_perturbation=0.05,
            avg_confidence_drop=0.18,
            samples_tested=1000,
            samples_successful=280
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
            defense_effectiveness=0.67,  # 67% reduction
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

    # Generate report with defense results
    report = generator.generate_report(
        model_name="Defended Classifier v2.0",
        attack_results=attack_results_after,
        original_accuracy=0.92,
        defense_results=defense_results
    )

    print(f"\n✓ Defense Effectiveness Report Generated!")
    print(f"  Defense Effectiveness: {defense_results[0].defense_effectiveness:.1%}")
    print(f"  Robustness Gain:       {defense_results[0].robustness_gain:.1%}")
    print(f"  Overhead:              {defense_results[0].overhead_ms:.1f}ms")

    print(f"\n🎯 Overall Assessment:")
    print(f"  Robustness Score: {report.robustness_score:.1f}/100")
    print(f"  Severity Level:   {report.severity_level.value}")

    # Save reports
    generator.save_report_html(report, "defense_effectiveness_report.html")
    print(f"\n✓ Defense report saved (HTML)")


def example_severity_levels():
    """Example 4: Severity Level Classification"""
    print_section("Example 4: Severity Level Classification")

    generator = RobustnessReportGenerator()

    # Test different severity scenarios
    scenarios = [
        {
            "name": "Low Severity",
            "success_rate": 0.15,
            "original_acc": 0.95
        },
        {
            "name": "Medium Severity",
            "success_rate": 0.45,
            "original_acc": 0.94
        },
        {
            "name": "High Severity",
            "success_rate": 0.72,
            "original_acc": 0.93
        },
        {
            "name": "Critical Severity",
            "success_rate": 0.95,
            "original_acc": 0.92
        }
    ]

    print("\nScenario: Classifying attack severity levels")

    for scenario in scenarios:
        attack_results = [
            AttackResult(
                attack_type=AttackType.PGD,
                success_rate=scenario["success_rate"],
                avg_perturbation=0.05,
                avg_confidence_drop=scenario["success_rate"] * 0.6,
                samples_tested=1000,
                samples_successful=int(scenario["success_rate"] * 1000)
            )
        ]

        report = generator.generate_report(
            model_name=f"Test Model - {scenario['name']}",
            attack_results=attack_results,
            original_accuracy=scenario["original_acc"]
        )

        print(f"\n  {scenario['name']}:")
        print(f"    Success Rate:     {scenario['success_rate']:.1%}")
        print(f"    Severity:         {report.severity_level.value}")
        print(f"    Robustness Score: {report.robustness_score:.1f}/100")


def example_visualizations():
    """Example 5: Robustness Visualizations"""
    print_section("Example 5: Robustness Visualizations")

    visualizer = RobustnessVisualizer()

    np.random.seed(42)

    print("\nScenario: Generating robustness visualizations")

    # 1. Adversarial examples visualization
    print("\n1️⃣ Adversarial Examples Comparison")
    original = np.random.rand(28, 28)
    adversarial = original + np.random.randn(28, 28) * 0.05
    perturbation = adversarial - original

    visualizer.plot_adversarial_examples(
        original, adversarial, perturbation,
        original_label="Cat (99.2%)",
        adversarial_label="Dog (87.3%)",
        save_path="adversarial_examples.png"
    )
    print("  ✓ Saved: adversarial_examples.png")

    # 2. Robustness curve
    print("\n2️⃣ Robustness Curve (Accuracy vs Epsilon)")
    epsilons = [0.0, 0.01, 0.03, 0.05, 0.1, 0.2, 0.3]
    accuracies = [0.95, 0.92, 0.85, 0.78, 0.62, 0.45, 0.32]

    visualizer.plot_robustness_curve(
        epsilons, accuracies,
        title="Model Robustness vs Attack Strength",
        save_path="robustness_curve.png"
    )
    print("  ✓ Saved: robustness_curve.png")

    # 3. Attack comparison
    print("\n3️⃣ Attack Success Rate Comparison")
    attack_names = ["FGSM", "PGD", "C&W", "DeepFool", "JSMA"]
    success_rates = [0.65, 0.82, 0.91, 0.74, 0.58]

    visualizer.plot_attack_comparison(
        attack_names, success_rates,
        title="Attack Success Rates",
        save_path="attack_comparison.png"
    )
    print("  ✓ Saved: attack_comparison.png")

    # 4. Defense effectiveness
    print("\n4️⃣ Defense Effectiveness Comparison")
    defense_names = ["No Defense", "Adv Training", "Input Transform", "Ensemble"]
    before_rates = [0.85, 0.85, 0.85, 0.85]
    after_rates = [0.85, 0.28, 0.52, 0.35]

    visualizer.plot_defense_effectiveness(
        defense_names, before_rates, after_rates,
        save_path="defense_effectiveness.png"
    )
    print("  ✓ Saved: defense_effectiveness.png")

    # 5. Confidence distribution
    print("\n5️⃣ Confidence Distribution Analysis")
    clean_confidences = np.random.beta(8, 2, 1000)  # High confidence
    adv_confidences = np.random.beta(2, 5, 1000)    # Low confidence

    visualizer.plot_confidence_distribution(
        clean_confidences, adv_confidences,
        save_path="confidence_distribution.png"
    )
    print("  ✓ Saved: confidence_distribution.png")

    # 6. Perturbation heatmap
    print("\n6️⃣ Perturbation Heatmap")
    perturbations = np.random.randn(28, 28) * 0.05

    visualizer.plot_perturbation_heatmap(
        perturbations,
        title="FGSM Perturbation Pattern",
        save_path="perturbation_heatmap.png"
    )
    print("  ✓ Saved: perturbation_heatmap.png")

    print("\n✓ All visualizations generated!")


def example_comprehensive_analysis():
    """Example 6: Comprehensive Robustness Analysis"""
    print_section("Example 6: Comprehensive Robustness Analysis")

    generator = RobustnessReportGenerator()
    visualizer = RobustnessVisualizer()

    # Comprehensive attack results
    attack_results = [
        AttackResult(AttackType.FGSM, 0.65, 0.03, 0.35, 1000, 650),
        AttackResult(AttackType.PGD, 0.82, 0.05, 0.48, 1000, 820),
        AttackResult(AttackType.CW, 0.91, 0.02, 0.62, 1000, 910),
        AttackResult(AttackType.DEEPFOOL, 0.74, 0.04, 0.41, 1000, 740),
        AttackResult(AttackType.JSMA, 0.58, 0.06, 0.29, 1000, 580)
    ]

    # Defense results
    defense_results = [
        DefenseResult("Adversarial Training", 0.94, 0.92, 0.82, 0.35, 0.57, 5.2, 0.47),
        DefenseResult("Input Transformation", 0.94, 0.93, 0.82, 0.48, 0.41, 2.1, 0.34),
        DefenseResult("Ensemble Defense", 0.94, 0.91, 0.82, 0.38, 0.54, 8.7, 0.44)
    ]

    print("\nScenario: Complete robustness analysis with multiple attacks and defenses")

    # Generate comprehensive report
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
    print(f"  Name:             {report.model_name}")
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
        print(f"    Overhead:          {defense.overhead_ms:.1f}ms")
        print(f"    Accuracy Impact:   {(defense.defended_accuracy - defense.original_accuracy):.2%}")

    print(f"\n💡 Key Recommendations:")
    if report.recommendations:
        for i, rec in enumerate(report.recommendations[:5], 1):
            print(f"  {i}. {rec}")

    # Generate visualizations
    print(f"\n📊 Generating Visualizations...")

    # Attack comparison
    attack_names = [r.attack_type.value for r in attack_results]
    success_rates = [r.success_rate for r in attack_results]
    visualizer.plot_attack_comparison(
        attack_names, success_rates,
        save_path="comprehensive_attack_comparison.png"
    )
    print("  ✓ Attack comparison chart")

    # Defense effectiveness
    defense_names = [d.defense_type for d in defense_results]
    before_rates = [d.attack_success_rate_before for d in defense_results]
    after_rates = [d.attack_success_rate_after for d in defense_results]
    visualizer.plot_defense_effectiveness(
        defense_names, before_rates, after_rates,
        save_path="comprehensive_defense_effectiveness.png"
    )
    print("  ✓ Defense effectiveness chart")

    # Save comprehensive reports
    generator.save_report_text(report, "comprehensive_analysis.txt")
    generator.save_report_html(report, "comprehensive_analysis.html")

    print(f"\n✓ Comprehensive analysis complete!")
    print(f"  Generated files:")
    print(f"    • comprehensive_analysis.txt")
    print(f"    • comprehensive_analysis.html")
    print(f"    • comprehensive_attack_comparison.png")
    print(f"    • comprehensive_defense_effectiveness.png")


def example_executive_summary():
    """Example 7: Executive Summary Generation"""
    print_section("Example 7: Executive Summary for Stakeholders")

    generator = RobustnessReportGenerator()

    attack_results = [
        AttackResult(AttackType.PGD, 0.75, 0.05, 0.45, 1000, 750),
        AttackResult(AttackType.CW, 0.88, 0.02, 0.58, 1000, 880)
    ]

    report = generator.generate_report(
        model_name="Customer Fraud Detector",
        attack_results=attack_results,
        original_accuracy=0.93
    )

    print("\nScenario: Creating executive summary for business stakeholders")

    print(f"\n{'='*70}")
    print("  EXECUTIVE SUMMARY - Robustness Assessment")
    print(f"{'='*70}")

    print(f"\n🎯 Key Findings:")
    print(f"  • Model: {report.model_name}")
    print(f"  • Overall Robustness: {report.robustness_score:.0f}/100")
    print(f"  • Risk Level: {report.severity_level.value.upper()}")

    print(f"\n📊 Business Impact:")
    if report.severity_level == SeverityLevel.CRITICAL:
        print(f"  ⚠️  CRITICAL: Model is highly vulnerable to attacks")
        print(f"  • Recommend immediate defensive measures")
        print(f"  • Consider delaying production deployment")
    elif report.severity_level == SeverityLevel.HIGH:
        print(f"  ⚠️  HIGH: Model shows significant vulnerabilities")
        print(f"  • Implement defenses before production use")
        print(f"  • Additional testing recommended")
    elif report.severity_level == SeverityLevel.MEDIUM:
        print(f"  ⚠️  MEDIUM: Model has moderate vulnerabilities")
        print(f"  • Deploy with monitoring and defenses")
        print(f"  • Plan for regular security audits")
    else:
        print(f"  ✓ LOW: Model shows good robustness")
        print(f"  • Suitable for production deployment")
        print(f"  • Maintain regular security reviews")

    print(f"\n💼 Recommended Actions:")
    if report.recommendations:
        for i, rec in enumerate(report.recommendations[:3], 1):
            print(f"  {i}. {rec}")

    print(f"\n📅 Next Steps:")
    print(f"  1. Review detailed technical report")
    print(f"  2. Implement recommended defenses")
    print(f"  3. Re-test after improvements")
    print(f"  4. Establish ongoing monitoring")


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
        example_visualizations,
        example_comprehensive_analysis,
        example_executive_summary
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
    print("  Reports:")
    print("    • fgsm_attack_report.txt/html")
    print("    • multi_attack_report.txt/html")
    print("    • defense_effectiveness_report.html")
    print("    • comprehensive_analysis.txt/html")
    print("\n  Visualizations:")
    print("    • adversarial_examples.png")
    print("    • robustness_curve.png")
    print("    • attack_comparison.png")
    print("    • defense_effectiveness.png")
    print("    • confidence_distribution.png")
    print("    • perturbation_heatmap.png")


if __name__ == "__main__":
    main()
