"""
A/B Testing Framework Examples

Demonstrates all features of the enhanced A/B testing framework including:
- Statistical tests (parametric and non-parametric)
- Traditional A/B testing
- Sequential A/B testing with early stopping
- Bayesian A/B testing
- Multi-variant testing
- Multi-armed bandit algorithms
- Sample size and MDE calculations

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aeva.ab_testing import ABTester, StatisticalTest, BanditAlgorithm


def print_section(title: str):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def example_statistical_tests():
    """Example 1: Statistical Tests"""
    print_section("Example 1: Statistical Tests")

    np.random.seed(42)

    # Generate sample data
    control = np.random.normal(100, 15, 200)
    treatment = np.random.normal(105, 15, 200)

    stat_test = StatisticalTest(significance_level=0.05)

    # 1. T-test (parametric)
    print("\n1. Student's t-test:")
    result = stat_test.t_test(control, treatment, equal_var=True)
    print(result)

    # 2. Mann-Whitney U test (non-parametric)
    print("\n2. Mann-Whitney U test (non-parametric):")
    result = stat_test.mann_whitney_u(control, treatment)
    print(result)

    # 3. Effect size
    print("\n3. Effect Sizes:")
    cohens_d = stat_test.cohens_d(control, treatment)
    hedges_g = stat_test.hedges_g(control, treatment)
    print(f"Cohen's d: {cohens_d:.4f}")
    print(f"Hedge's g: {hedges_g:.4f}")

    # 4. Power analysis
    print("\n4. Power Analysis:")
    power = stat_test.power_analysis(effect_size=0.3, sample_size=200)
    print(f"Statistical Power: {power:.2%}")

    required_n = stat_test.sample_size_calculation(effect_size=0.3, power=0.8)
    print(f"Required Sample Size: {required_n} per group")

    # 5. Multiple comparison correction
    print("\n5. Multiple Comparison Correction:")
    p_values = [0.01, 0.03, 0.05, 0.07, 0.10]
    corrected = stat_test.correct_pvalues(p_values, method=stat_test.CorrectionMethod.BONFERRONI)
    print(f"Original p-values: {p_values}")
    print(f"Bonferroni corrected: {[f'{p:.4f}' for p in corrected]}")


def example_traditional_ab_test():
    """Example 2: Traditional A/B Testing"""
    print_section("Example 2: Traditional A/B Testing")

    np.random.seed(42)

    # Simulate conversion rates
    control = np.random.binomial(1, 0.10, 1000)  # 10% conversion
    treatment = np.random.binomial(1, 0.12, 1000)  # 12% conversion

    tester = ABTester(significance_level=0.05, power=0.8)

    print("\nScenario: Testing new checkout flow")
    print(f"Control (old flow): {control.sum()} conversions from {len(control)} visitors")
    print(f"Treatment (new flow): {treatment.sum()} conversions from {len(treatment)} visitors")

    result = tester.compare(
        control.tolist(),
        treatment.tolist(),
        variant_a_name="Old Checkout",
        variant_b_name="New Checkout"
    )

    print(f"\n{result}")

    if result.statistically_significant:
        print(f"\n✓ Result is statistically significant!")
        print(f"  Recommend: Deploy the new checkout flow")
    else:
        print(f"\n✗ Result is NOT statistically significant")
        print(f"  Recommend: Continue testing or try a different variant")


def example_sequential_testing():
    """Example 3: Sequential A/B Testing"""
    print_section("Example 3: Sequential A/B Testing with Early Stopping")

    np.random.seed(42)

    # Generate data with clear difference
    control = np.random.normal(50, 10, 5000)
    treatment = np.random.normal(55, 10, 5000)  # 10% improvement

    tester = ABTester(significance_level=0.05, power=0.8)

    print("\nScenario: Testing new recommendation algorithm")
    print("Using sequential testing to potentially stop early")

    result = tester.sequential_test(
        control.tolist(),
        treatment.tolist(),
        variant_a_name="Old Algorithm",
        variant_b_name="New Algorithm",
        check_interval=200,
        min_samples=500,
        max_samples=5000
    )

    print(f"\n{result}")

    if result.status.value == "stopped_early":
        samples_saved = 5000 - result.variant_a_size
        print(f"\n✓ Test stopped early!")
        print(f"  Saved {samples_saved} samples (time/cost savings)")
        print(f"  Can deploy {result.winner} with confidence")


def example_bayesian_testing():
    """Example 4: Bayesian A/B Testing"""
    print_section("Example 4: Bayesian A/B Testing")

    np.random.seed(42)

    # Simulate click-through rates
    control = np.random.binomial(1, 0.05, 500)  # 5% CTR
    treatment = np.random.binomial(1, 0.06, 500)  # 6% CTR

    tester = ABTester()

    print("\nScenario: Testing new ad creative")
    print(f"Control: {control.sum()} clicks from {len(control)} impressions")
    print(f"Treatment: {treatment.sum()} clicks from {len(treatment)} impressions")

    result = tester.bayesian_test(
        control.tolist(),
        treatment.tolist(),
        variant_a_name="Old Creative",
        variant_b_name="New Creative",
        prior_mean=0.05,
        prior_std=0.02
    )

    print(f"\n{result}")

    if result.prob_b_better > 0.95:
        print(f"\n✓ High confidence that new creative is better!")
        print(f"  Expected lift: {(result.prob_b_better - 0.5) * 200:.1f}%")


def example_multivariant_testing():
    """Example 5: Multi-Variant Testing"""
    print_section("Example 5: Multi-Variant Testing (A/B/C/D)")

    np.random.seed(42)

    # Test 4 different variants
    variants = {
        "Control": np.random.normal(100, 15, 250).tolist(),
        "Variant_B": np.random.normal(105, 15, 250).tolist(),
        "Variant_C": np.random.normal(103, 15, 250).tolist(),
        "Variant_D": np.random.normal(107, 15, 250).tolist(),
    }

    tester = ABTester(significance_level=0.05)

    print("\nScenario: Testing 4 different landing page designs")
    print("Applying Bonferroni correction for multiple comparisons")

    results = tester.compare_multiple(variants, control_name="Control")

    print("\nResults:")
    for name, result in results.items():
        print(f"\n{name}:")
        print(f"  P-value: {result.p_value:.4f}")
        print(f"  Significant: {'Yes ✓' if result.statistically_significant else 'No ✗'}")
        print(f"  Improvement: {result.improvement_pct:+.2f}%")

    # Find best variant
    best_variant = max(results.items(), key=lambda x: x[1].improvement_pct)
    print(f"\n✓ Best Variant: {best_variant[0].split('_vs_')[1]}")
    print(f"  Improvement: {best_variant[1].improvement_pct:+.2f}%")


def example_multi_armed_bandit():
    """Example 6: Multi-Armed Bandit"""
    print_section("Example 6: Multi-Armed Bandit Algorithms")

    np.random.seed(42)

    # Simulate 3 ad variants with different true CTRs
    true_ctrs = [0.03, 0.05, 0.04]
    n_trials = 1000

    print("\nScenario: Dynamic ad allocation")
    print(f"True CTRs: {true_ctrs}")
    print(f"Running {n_trials} trials with Thompson Sampling")

    bandit = ABTester.MultiArmedBandit(
        n_arms=3,
        algorithm=BanditAlgorithm.THOMPSON_SAMPLING
    )

    # Simulate trials
    cumulative_reward = 0
    for trial in range(n_trials):
        # Select arm
        arm = bandit.select_arm()

        # Simulate reward (click or no click)
        reward = np.random.binomial(1, true_ctrs[arm])

        # Update bandit
        bandit.update(arm, reward)
        cumulative_reward += reward

    print(f"\nResults after {n_trials} trials:")
    print(f"Total clicks: {cumulative_reward}")
    print(f"Overall CTR: {cumulative_reward/n_trials:.2%}")
    print(f"\nArm Statistics:")
    for i in range(3):
        print(f"  Arm {i}: Selected {int(bandit.counts[i])} times, "
              f"Estimated CTR: {bandit.values[i]:.2%}")

    best_arm = bandit.get_best_arm()
    print(f"\n✓ Best Arm: {best_arm} (True CTR: {true_ctrs[best_arm]:.2%})")

    # Compare algorithms
    print("\n\nComparing Bandit Algorithms:")
    algorithms = [
        ("Epsilon-Greedy", BanditAlgorithm.EPSILON_GREEDY),
        ("UCB", BanditAlgorithm.UCB),
        ("Thompson Sampling", BanditAlgorithm.THOMPSON_SAMPLING)
    ]

    for name, algo in algorithms:
        bandit = ABTester.MultiArmedBandit(n_arms=3, algorithm=algo)
        total_reward = 0

        for _ in range(1000):
            arm = bandit.select_arm()
            reward = np.random.binomial(1, true_ctrs[arm])
            bandit.update(arm, reward)
            total_reward += reward

        print(f"  {name:20s}: {total_reward} clicks ({total_reward/1000:.2%} CTR)")


def example_sample_size_calculation():
    """Example 7: Sample Size and MDE Calculations"""
    print_section("Example 7: Sample Size & MDE Calculations")

    tester = ABTester(significance_level=0.05, power=0.8)

    # Scenario 1: Calculate required sample size
    print("\nScenario 1: How many users do I need?")
    baseline_rate = 0.10  # 10% conversion rate
    mde = 0.10  # Want to detect 10% relative improvement

    required_n = tester.calculate_sample_size(
        baseline_rate=baseline_rate,
        mde=mde
    )

    print(f"Baseline conversion rate: {baseline_rate:.1%}")
    print(f"Minimum detectable effect: {mde:.1%} (relative)")
    print(f"Required sample size: {required_n} per variant")
    print(f"Total users needed: {required_n * 2}")

    # Scenario 2: Calculate MDE for available sample
    print("\n\nScenario 2: What can I detect with my sample?")
    available_n = 1000

    mde_achievable = tester.calculate_mde(
        baseline_rate=baseline_rate,
        sample_size=available_n
    )

    print(f"Available sample size: {available_n} per variant")
    print(f"Baseline conversion rate: {baseline_rate:.1%}")
    print(f"Minimum detectable effect: {mde_achievable:.1%} (relative)")
    print(f"Can detect improvements of {mde_achievable*100:.1f}% or larger")

    # Scenario 3: Test duration estimation
    print("\n\nScenario 3: How long will the test take?")
    daily_traffic = 5000

    duration = tester.estimate_duration(
        required_sample_size=required_n,
        daily_traffic=daily_traffic,
        n_variants=2
    )

    print(f"Required sample size: {required_n} per variant")
    print(f"Daily traffic: {daily_traffic} users")
    print(f"Estimated duration: {duration} days")


def example_stratified_testing():
    """Example 8: Stratified Testing"""
    print_section("Example 8: Stratified A/B Testing")

    np.random.seed(42)

    # Simulate data for mobile and desktop users
    # Mobile users (stratum 0): lower conversion but more volume
    control_mobile = np.random.binomial(1, 0.05, 800)
    treatment_mobile = np.random.binomial(1, 0.06, 800)

    # Desktop users (stratum 1): higher conversion but less volume
    control_desktop = np.random.binomial(1, 0.12, 200)
    treatment_desktop = np.random.binomial(1, 0.14, 200)

    # Combine
    control_scores = np.concatenate([control_mobile, control_desktop]).tolist()
    treatment_scores = np.concatenate([treatment_mobile, treatment_desktop]).tolist()
    control_strata = [0]*800 + [1]*200
    treatment_strata = [0]*800 + [1]*200

    tester = ABTester()

    print("\nScenario: Testing checkout flow across device types")
    print(f"Mobile users: {800*2} total")
    print(f"Desktop users: {200*2} total")

    result = tester.stratified_test(
        control_scores,
        treatment_scores,
        control_strata,
        treatment_strata,
        "Control",
        "Treatment"
    )

    print(f"\n{result}")
    print(f"\nStratified analysis accounts for different baseline rates")
    print(f"between mobile and desktop users")


def main():
    """Run all examples"""
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "AEVA A/B Testing Framework Examples" + " " * 18 + "║")
    print("╚" + "=" * 68 + "╝")

    examples = [
        example_statistical_tests,
        example_traditional_ab_test,
        example_sequential_testing,
        example_bayesian_testing,
        example_multivariant_testing,
        example_multi_armed_bandit,
        example_sample_size_calculation,
        example_stratified_testing
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


if __name__ == "__main__":
    main()
