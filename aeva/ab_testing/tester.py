"""
A/B Testing Framework

Comprehensive A/B testing framework with advanced features for experimentation.

Features:
- Traditional frequentist A/B testing
- Sequential A/B testing with early stopping
- Bayesian A/B testing
- Multi-armed bandit algorithms
- Multi-variant testing (A/B/C/D...)
- Stratified testing
- Sample size and duration calculators
- Minimum detectable effect (MDE) calculator

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from enum import Enum
from scipy import stats
from .statistics import StatisticalTest

logger = logging.getLogger(__name__)


class TestStatus(Enum):
    """Status of an A/B test"""
    NOT_STARTED = "not_started"
    RUNNING = "running"
    STOPPED_EARLY = "stopped_early"
    COMPLETED = "completed"
    INCONCLUSIVE = "inconclusive"


class BanditAlgorithm(Enum):
    """Multi-armed bandit algorithms"""
    EPSILON_GREEDY = "epsilon_greedy"
    UCB = "ucb"  # Upper Confidence Bound
    THOMPSON_SAMPLING = "thompson_sampling"


@dataclass
class ABTestResult:
    """A/B test results"""
    variant_a_name: str
    variant_b_name: str
    variant_a_mean: float
    variant_b_mean: float
    variant_a_std: float
    variant_b_std: float
    variant_a_size: int
    variant_b_size: int
    p_value: float
    statistically_significant: bool
    improvement_pct: float
    winner: str
    effect_size: float
    confidence_interval: Tuple[float, float]
    power: Optional[float] = None
    test_duration_days: Optional[int] = None
    status: TestStatus = TestStatus.COMPLETED

    def __str__(self) -> str:
        result = [
            f"A/B Test Results: {self.variant_a_name} vs {self.variant_b_name}",
            f"Status: {self.status.value}",
            f"",
            f"Variant {self.variant_a_name}:",
            f"  Mean: {self.variant_a_mean:.4f}",
            f"  Std: {self.variant_a_std:.4f}",
            f"  Size: {self.variant_a_size}",
            f"",
            f"Variant {self.variant_b_name}:",
            f"  Mean: {self.variant_b_mean:.4f}",
            f"  Std: {self.variant_b_std:.4f}",
            f"  Size: {self.variant_b_size}",
            f"",
            f"Statistical Analysis:",
            f"  P-value: {self.p_value:.4f}",
            f"  Significant: {'Yes ✓' if self.statistically_significant else 'No ✗'}",
            f"  Improvement: {self.improvement_pct:+.2f}%",
            f"  Winner: {self.winner}",
            f"  Effect Size: {self.effect_size:.4f}",
            f"  95% CI: [{self.confidence_interval[0]:.4f}, {self.confidence_interval[1]:.4f}]"
        ]

        if self.power:
            result.append(f"  Power: {self.power:.2%}")
        if self.test_duration_days:
            result.append(f"  Duration: {self.test_duration_days} days")

        return "\n".join(result)


@dataclass
class BayesianResult:
    """Bayesian A/B test results"""
    variant_a_name: str
    variant_b_name: str
    prob_b_better: float  # P(B > A)
    expected_loss_a: float  # Expected loss if choosing A
    expected_loss_b: float  # Expected loss if choosing B
    credible_interval: Tuple[float, float]  # 95% credible interval for difference
    recommendation: str

    def __str__(self) -> str:
        return (
            f"Bayesian A/B Test Results:\n"
            f"  P({self.variant_b_name} > {self.variant_a_name}): {self.prob_b_better:.2%}\n"
            f"  Expected Loss (choose {self.variant_a_name}): {self.expected_loss_a:.4f}\n"
            f"  Expected Loss (choose {self.variant_b_name}): {self.expected_loss_b:.4f}\n"
            f"  95% Credible Interval: [{self.credible_interval[0]:.4f}, {self.credible_interval[1]:.4f}]\n"
            f"  Recommendation: {self.recommendation}"
        )


class ABTester:
    """
    Comprehensive A/B testing framework

    Supports traditional frequentist testing, sequential testing,
    and Bayesian methods.
    """

    def __init__(self, significance_level: float = 0.05, power: float = 0.8):
        """
        Initialize A/B tester.

        Args:
            significance_level: Alpha level for hypothesis testing (default: 0.05)
            power: Desired statistical power (default: 0.8)
        """
        self.significance_level = significance_level
        self.power = power
        self.stat_test = StatisticalTest(significance_level=significance_level)

    # ========== Traditional A/B Testing ==========

    def compare(
        self,
        variant_a_scores: List[float],
        variant_b_scores: List[float],
        variant_a_name: str = "A",
        variant_b_name: str = "B",
        test_type: str = "t_test"
    ) -> ABTestResult:
        """
        Compare two variants using frequentist approach.

        Args:
            variant_a_scores: Scores/metrics for variant A
            variant_b_scores: Scores/metrics for variant B
            variant_a_name: Name of variant A
            variant_b_name: Name of variant B
            test_type: Statistical test to use ("t_test", "mann_whitney")

        Returns:
            ABTestResult with comparison statistics
        """
        mean_a = np.mean(variant_a_scores)
        mean_b = np.mean(variant_b_scores)
        std_a = np.std(variant_a_scores, ddof=1)
        std_b = np.std(variant_b_scores, ddof=1)

        # Perform statistical test
        if test_type == "t_test":
            test_result = self.stat_test.t_test(variant_a_scores, variant_b_scores, equal_var=False)
        elif test_type == "mann_whitney":
            test_result = self.stat_test.mann_whitney_u(variant_a_scores, variant_b_scores)
        else:
            raise ValueError(f"Unknown test type: {test_type}")

        p_value = test_result.p_value
        is_significant = test_result.is_significant
        effect_size = test_result.effect_size
        ci = test_result.confidence_interval

        improvement = ((mean_b - mean_a) / mean_a * 100) if mean_a != 0 else 0
        winner = variant_b_name if mean_b > mean_a else variant_a_name

        # Calculate achieved power
        achieved_power = self.stat_test.power_analysis(
            effect_size=abs(effect_size),
            sample_size=len(variant_a_scores),
            alpha=self.significance_level
        )

        return ABTestResult(
            variant_a_name=variant_a_name,
            variant_b_name=variant_b_name,
            variant_a_mean=mean_a,
            variant_b_mean=mean_b,
            variant_a_std=std_a,
            variant_b_std=std_b,
            variant_a_size=len(variant_a_scores),
            variant_b_size=len(variant_b_scores),
            p_value=p_value,
            statistically_significant=is_significant,
            improvement_pct=improvement,
            winner=winner,
            effect_size=effect_size,
            confidence_interval=ci,
            power=achieved_power
        )

    # ========== Sequential A/B Testing ==========

    def sequential_test(
        self,
        variant_a_scores: List[float],
        variant_b_scores: List[float],
        variant_a_name: str = "A",
        variant_b_name: str = "B",
        check_interval: int = 100,
        min_samples: int = 100,
        max_samples: int = 10000
    ) -> ABTestResult:
        """
        Perform sequential A/B testing with early stopping.

        Uses alpha spending function to control Type I error across
        multiple looks at the data.

        Args:
            variant_a_scores: Scores for variant A
            variant_b_scores: Scores for variant B
            variant_a_name: Name of variant A
            variant_b_name: Name of variant B
            check_interval: How often to check for significance
            min_samples: Minimum samples before checking
            max_samples: Maximum samples before stopping

        Returns:
            ABTestResult with early stopping information
        """
        n = min(len(variant_a_scores), len(variant_b_scores))

        # O'Brien-Fleming alpha spending function
        def alpha_spending(t, alpha=0.05):
            """Calculate adjusted alpha for time t (0 to 1)"""
            if t <= 0:
                return 0
            z = stats.norm.ppf(1 - alpha/2)
            return 2 * (1 - stats.norm.cdf(z / np.sqrt(t)))

        status = TestStatus.RUNNING
        stopped_at = n

        for i in range(min_samples, min(n, max_samples), check_interval):
            # Cumulative data up to this point
            a_data = variant_a_scores[:i]
            b_data = variant_b_scores[:i]

            # Calculate current statistics
            mean_diff = np.mean(b_data) - np.mean(a_data)
            pooled_std = np.sqrt((np.var(a_data, ddof=1) + np.var(b_data, ddof=1)) / 2)
            se = pooled_std * np.sqrt(2/i)
            z_score = mean_diff / se if se > 0 else 0

            # Adjusted alpha for this look
            t = i / max_samples
            adjusted_alpha = alpha_spending(t, self.significance_level)
            critical_z = stats.norm.ppf(1 - adjusted_alpha/2)

            # Check for early stopping
            if abs(z_score) > critical_z:
                status = TestStatus.STOPPED_EARLY
                stopped_at = i
                logger.info(f"Early stopping at sample {i} (z={z_score:.2f}, critical={critical_z:.2f})")
                break

        # Use data up to stopping point
        result = self.compare(
            variant_a_scores[:stopped_at],
            variant_b_scores[:stopped_at],
            variant_a_name,
            variant_b_name
        )
        result.status = status

        return result

    # ========== Bayesian A/B Testing ==========

    def bayesian_test(
        self,
        variant_a_scores: List[float],
        variant_b_scores: List[float],
        variant_a_name: str = "A",
        variant_b_name: str = "B",
        prior_mean: float = 0.0,
        prior_std: float = 1.0,
        n_samples: int = 10000
    ) -> BayesianResult:
        """
        Perform Bayesian A/B testing.

        Uses Monte Carlo sampling to estimate posterior distributions
        and probability that B is better than A.

        Args:
            variant_a_scores: Scores for variant A
            variant_b_scores: Scores for variant B
            variant_a_name: Name of variant A
            variant_b_name: Name of variant B
            prior_mean: Prior mean for both variants
            prior_std: Prior standard deviation
            n_samples: Number of Monte Carlo samples

        Returns:
            BayesianResult with posterior analysis
        """
        # Compute sufficient statistics
        mean_a, std_a, n_a = np.mean(variant_a_scores), np.std(variant_a_scores, ddof=1), len(variant_a_scores)
        mean_b, std_b, n_b = np.mean(variant_b_scores), np.std(variant_b_scores, ddof=1), len(variant_b_scores)

        # Update posterior using conjugate prior (normal-normal model)
        # Posterior: N(posterior_mean, posterior_std)
        def posterior_params(data_mean, data_std, n, prior_mean, prior_std):
            prior_precision = 1 / (prior_std ** 2)
            data_precision = n / (data_std ** 2) if data_std > 0 else 0

            posterior_precision = prior_precision + data_precision
            posterior_mean = (prior_precision * prior_mean + data_precision * data_mean) / posterior_precision
            posterior_std = 1 / np.sqrt(posterior_precision)

            return posterior_mean, posterior_std

        post_mean_a, post_std_a = posterior_params(mean_a, std_a, n_a, prior_mean, prior_std)
        post_mean_b, post_std_b = posterior_params(mean_b, std_b, n_b, prior_mean, prior_std)

        # Sample from posteriors
        samples_a = np.random.normal(post_mean_a, post_std_a, n_samples)
        samples_b = np.random.normal(post_mean_b, post_std_b, n_samples)

        # Calculate P(B > A)
        prob_b_better = np.mean(samples_b > samples_a)

        # Calculate expected loss
        diff = samples_b - samples_a
        expected_loss_a = np.mean(np.maximum(diff, 0))  # Loss if we choose A
        expected_loss_b = np.mean(np.maximum(-diff, 0))  # Loss if we choose B

        # Credible interval for difference
        credible_interval = (
            np.percentile(diff, 2.5),
            np.percentile(diff, 97.5)
        )

        # Make recommendation
        if prob_b_better > 0.95:
            recommendation = f"Choose {variant_b_name} (high confidence)"
        elif prob_b_better < 0.05:
            recommendation = f"Choose {variant_a_name} (high confidence)"
        elif expected_loss_a < expected_loss_b:
            recommendation = f"Slight preference for {variant_a_name}"
        elif expected_loss_b < expected_loss_a:
            recommendation = f"Slight preference for {variant_b_name}"
        else:
            recommendation = "Inconclusive - collect more data"

        return BayesianResult(
            variant_a_name=variant_a_name,
            variant_b_name=variant_b_name,
            prob_b_better=prob_b_better,
            expected_loss_a=expected_loss_a,
            expected_loss_b=expected_loss_b,
            credible_interval=credible_interval,
            recommendation=recommendation
        )

    # ========== Multi-Variant Testing ==========

    def compare_multiple(
        self,
        variants: Dict[str, List[float]],
        control_name: str = "A"
    ) -> Dict[str, ABTestResult]:
        """
        Compare multiple variants against a control.

        Applies multiple comparison correction (Bonferroni).

        Args:
            variants: Dictionary mapping variant names to scores
            control_name: Name of control variant

        Returns:
            Dictionary of pairwise comparison results
        """
        if control_name not in variants:
            raise ValueError(f"Control variant '{control_name}' not found")

        control_scores = variants[control_name]
        variant_names = [name for name in variants.keys() if name != control_name]
        n_comparisons = len(variant_names)

        # Bonferroni-corrected alpha
        adjusted_alpha = self.significance_level / n_comparisons
        original_alpha = self.significance_level

        results = {}
        for variant_name in variant_names:
            # Temporarily adjust significance level
            self.significance_level = adjusted_alpha
            self.stat_test.significance_level = adjusted_alpha

            result = self.compare(
                control_scores,
                variants[variant_name],
                control_name,
                variant_name
            )
            results[f"{control_name}_vs_{variant_name}"] = result

        # Restore original significance level
        self.significance_level = original_alpha
        self.stat_test.significance_level = original_alpha

        return results

    # ========== Multi-Armed Bandit ==========

    class MultiArmedBandit:
        """
        Multi-armed bandit for dynamic allocation.

        Balances exploration vs exploitation to maximize cumulative reward.
        """

        def __init__(
            self,
            n_arms: int,
            algorithm: BanditAlgorithm = BanditAlgorithm.EPSILON_GREEDY,
            epsilon: float = 0.1,
            c: float = 2.0
        ):
            """
            Initialize multi-armed bandit.

            Args:
                n_arms: Number of arms (variants)
                algorithm: Bandit algorithm to use
                epsilon: Exploration rate for epsilon-greedy
                c: Exploration parameter for UCB
            """
            self.n_arms = n_arms
            self.algorithm = algorithm
            self.epsilon = epsilon
            self.c = c

            # Track statistics
            self.counts = np.zeros(n_arms)
            self.values = np.zeros(n_arms)
            self.total_count = 0

            # For Thompson Sampling (Beta distribution parameters)
            self.alpha = np.ones(n_arms)
            self.beta = np.ones(n_arms)

        def select_arm(self) -> int:
            """
            Select an arm to pull.

            Returns:
                Index of selected arm
            """
            if self.algorithm == BanditAlgorithm.EPSILON_GREEDY:
                if np.random.random() < self.epsilon:
                    return np.random.randint(self.n_arms)  # Explore
                else:
                    return np.argmax(self.values)  # Exploit

            elif self.algorithm == BanditAlgorithm.UCB:
                if self.total_count < self.n_arms:
                    # Pull each arm once initially
                    return self.total_count

                # UCB formula: mean + c * sqrt(log(t) / n_i)
                ucb_values = self.values + self.c * np.sqrt(
                    np.log(self.total_count + 1) / (self.counts + 1e-5)
                )
                return np.argmax(ucb_values)

            elif self.algorithm == BanditAlgorithm.THOMPSON_SAMPLING:
                # Sample from Beta distribution for each arm
                samples = np.random.beta(self.alpha, self.beta)
                return np.argmax(samples)

            else:
                raise ValueError(f"Unknown algorithm: {self.algorithm}")

        def update(self, arm: int, reward: float):
            """
            Update statistics after observing reward.

            Args:
                arm: Index of arm that was pulled
                reward: Observed reward (0-1 for Thompson Sampling)
            """
            self.counts[arm] += 1
            self.total_count += 1

            # Update running average
            n = self.counts[arm]
            value = self.values[arm]
            self.values[arm] = ((n - 1) / n) * value + (1 / n) * reward

            # Update Beta parameters for Thompson Sampling
            if self.algorithm == BanditAlgorithm.THOMPSON_SAMPLING:
                self.alpha[arm] += reward
                self.beta[arm] += 1 - reward

        def get_best_arm(self) -> int:
            """Get current best arm based on mean reward."""
            return np.argmax(self.values)

    # ========== Sample Size Calculation ==========

    def calculate_sample_size(
        self,
        baseline_rate: float,
        mde: float,
        power: Optional[float] = None,
        ratio: float = 1.0
    ) -> int:
        """
        Calculate required sample size per variant.

        Args:
            baseline_rate: Baseline conversion/success rate
            mde: Minimum detectable effect (relative, e.g., 0.05 for 5%)
            power: Desired statistical power (uses self.power if None)
            ratio: Allocation ratio (variant_b_size / variant_a_size)

        Returns:
            Required sample size per variant
        """
        power = power or self.power
        effect_size = mde * baseline_rate / np.sqrt(baseline_rate * (1 - baseline_rate))

        # Use the statistics module for sample size calculation
        n = self.stat_test.sample_size_calculation(
            effect_size=effect_size,
            power=power,
            alpha=self.significance_level
        )

        # Adjust for unequal allocation
        if ratio != 1.0:
            n = int(n * (1 + 1/ratio) / 2)

        return n

    def calculate_mde(
        self,
        baseline_rate: float,
        sample_size: int,
        power: Optional[float] = None
    ) -> float:
        """
        Calculate minimum detectable effect for given sample size.

        Args:
            baseline_rate: Baseline conversion/success rate
            sample_size: Available sample size per variant
            power: Desired statistical power (uses self.power if None)

        Returns:
            Minimum detectable effect (relative)
        """
        power = power or self.power

        # Binary search for MDE
        mde_low, mde_high = 0.001, 1.0

        while mde_high - mde_low > 0.001:
            mde_mid = (mde_low + mde_high) / 2
            required_n = self.calculate_sample_size(baseline_rate, mde_mid, power)

            if required_n > sample_size:
                mde_low = mde_mid
            else:
                mde_high = mde_mid

        return mde_high

    def estimate_duration(
        self,
        required_sample_size: int,
        daily_traffic: int,
        n_variants: int = 2
    ) -> int:
        """
        Estimate test duration in days.

        Args:
            required_sample_size: Required sample size per variant
            daily_traffic: Expected daily traffic
            n_variants: Number of variants (including control)

        Returns:
            Estimated duration in days
        """
        total_required = required_sample_size * n_variants
        days = int(np.ceil(total_required / daily_traffic))
        return days

    # ========== Stratified Testing ==========

    def stratified_test(
        self,
        variant_a_scores: List[float],
        variant_b_scores: List[float],
        strata_a: List[int],
        strata_b: List[int],
        variant_a_name: str = "A",
        variant_b_name: str = "B"
    ) -> ABTestResult:
        """
        Perform stratified A/B testing.

        Useful when you have segments with different baseline rates.

        Args:
            variant_a_scores: Scores for variant A
            variant_b_scores: Scores for variant B
            strata_a: Stratum labels for variant A
            strata_b: Stratum labels for variant B
            variant_a_name: Name of variant A
            variant_b_name: Name of variant B

        Returns:
            ABTestResult aggregated across strata
        """
        # Group by strata
        unique_strata = set(strata_a).union(set(strata_b))

        stratified_results = []
        weights = []

        for stratum in unique_strata:
            # Filter to this stratum
            a_mask = np.array(strata_a) == stratum
            b_mask = np.array(strata_b) == stratum

            a_stratum = np.array(variant_a_scores)[a_mask]
            b_stratum = np.array(variant_b_scores)[b_mask]

            if len(a_stratum) > 0 and len(b_stratum) > 0:
                # Test within stratum
                result = self.compare(
                    a_stratum.tolist(),
                    b_stratum.tolist(),
                    f"{variant_a_name}_stratum_{stratum}",
                    f"{variant_b_name}_stratum_{stratum}"
                )
                stratified_results.append(result)
                weights.append(len(a_stratum) + len(b_stratum))

        # Aggregate results (weighted by stratum size)
        weights = np.array(weights) / sum(weights)

        agg_mean_a = sum(r.variant_a_mean * w for r, w in zip(stratified_results, weights))
        agg_mean_b = sum(r.variant_b_mean * w for r, w in zip(stratified_results, weights))
        agg_effect = sum(r.effect_size * w for r, w in zip(stratified_results, weights))

        # Meta-analysis p-value (Fisher's method)
        p_values = [r.p_value for r in stratified_results]
        chi2_stat = -2 * sum(np.log(p) for p in p_values)
        combined_p = 1 - stats.chi2.cdf(chi2_stat, 2 * len(p_values))

        improvement = ((agg_mean_b - agg_mean_a) / agg_mean_a * 100) if agg_mean_a != 0 else 0

        return ABTestResult(
            variant_a_name=variant_a_name,
            variant_b_name=variant_b_name,
            variant_a_mean=agg_mean_a,
            variant_b_mean=agg_mean_b,
            variant_a_std=np.std(variant_a_scores, ddof=1),
            variant_b_std=np.std(variant_b_scores, ddof=1),
            variant_a_size=len(variant_a_scores),
            variant_b_size=len(variant_b_scores),
            p_value=combined_p,
            statistically_significant=combined_p < self.significance_level,
            improvement_pct=improvement,
            winner=variant_b_name if agg_mean_b > agg_mean_a else variant_a_name,
            effect_size=agg_effect,
            confidence_interval=(0, 0)  # Simplified for stratified
        )
