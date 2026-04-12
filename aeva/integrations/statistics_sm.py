"""
statsmodels Integration

Provides advanced statistical testing using statsmodels library.

Features:
- Comprehensive statistical tests
- Bayesian A/B testing
- Time series analysis
- Effect size calculations
- Power analysis

Usage:
    from aeva.integrations import StatsModelsABTest

    tester = StatsModelsABTest()
    result = tester.advanced_ab_test(scores_a, scores_b)
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class AdvancedABResult:
    """Results from advanced A/B testing"""
    test_name: str
    variant_a_mean: float
    variant_b_mean: float
    variant_a_std: float
    variant_b_std: float
    difference: float
    effect_size: float
    t_statistic: float
    p_value: float
    confidence_interval: Tuple[float, float]
    power: float
    is_significant: bool
    winner: Optional[str]
    recommendation: str
    metadata: Dict[str, Any]


class StatsModelsABTest:
    """
    Advanced A/B testing using statsmodels

    Falls back to scipy-based testing if statsmodels not installed.
    """

    def __init__(self, significance_level: float = 0.05):
        """
        Initialize statsmodels A/B tester

        Args:
            significance_level: Significance threshold (default 0.05)
        """
        self.significance_level = significance_level

        # Try to import statsmodels
        try:
            import statsmodels.api as sm
            import statsmodels.stats.api as sms
            from statsmodels.stats.power import tt_ind_solve_power

            self.sm_available = True
            self.sm = sm
            self.sms = sms
            self.tt_ind_solve_power = tt_ind_solve_power

            logger.info("statsmodels library loaded successfully")

        except ImportError:
            self.sm_available = False
            logger.warning(
                "statsmodels not installed. Install with: pip install statsmodels\n"
                "Falling back to scipy-based testing."
            )

    def is_available(self) -> bool:
        """Check if statsmodels is available"""
        return self.sm_available

    def advanced_ab_test(
        self,
        variant_a: List[float],
        variant_b: List[float],
        test_type: str = "welch"
    ) -> AdvancedABResult:
        """
        Perform advanced A/B test with comprehensive statistics

        Args:
            variant_a: Scores for variant A
            variant_b: Scores for variant B
            test_type: Type of test ('welch', 'student', 'mann_whitney')

        Returns:
            Comprehensive A/B test results
        """
        a = np.array(variant_a)
        b = np.array(variant_b)

        # Basic statistics
        mean_a = np.mean(a)
        mean_b = np.mean(b)
        std_a = np.std(a, ddof=1)
        std_b = np.std(b, ddof=1)
        n_a = len(a)
        n_b = len(b)

        # Calculate effect size (Cohen's d)
        pooled_std = np.sqrt(((n_a - 1) * std_a**2 + (n_b - 1) * std_b**2) / (n_a + n_b - 2))
        effect_size = (mean_b - mean_a) / pooled_std if pooled_std > 0 else 0

        if self.sm_available:
            # Use statsmodels for advanced testing
            from statsmodels.stats.weightstats import ttest_ind

            # Welch's t-test (unequal variances)
            t_stat, p_value, df = ttest_ind(a, b, usevar='unequal')

            # Confidence interval using statsmodels
            from statsmodels.stats.weightstats import DescrStatsW
            diff = mean_b - mean_a
            desc_a = DescrStatsW(a)
            desc_b = DescrStatsW(b)

            # Calculate pooled SE
            se_diff = np.sqrt(desc_a.std_mean**2 + desc_b.std_mean**2)
            margin = 1.96 * se_diff  # 95% CI
            ci = (diff - margin, diff + margin)

            # Statistical power
            try:
                power = self.tt_ind_solve_power(
                    effect_size=abs(effect_size),
                    nobs1=n_a,
                    alpha=self.significance_level,
                    ratio=n_b / n_a,
                    alternative='two-sided'
                )
            except:
                power = 0.0

        else:
            # Fallback to scipy
            from scipy import stats

            if test_type == 'mann_whitney':
                statistic, p_value = stats.mannwhitneyu(a, b, alternative='two-sided')
                t_stat = statistic
            else:
                t_stat, p_value = stats.ttest_ind(a, b, equal_var=(test_type == 'student'))

            # Confidence interval (manual calculation)
            diff = mean_b - mean_a
            se_diff = np.sqrt(std_a**2 / n_a + std_b**2 / n_b)
            margin = 1.96 * se_diff
            ci = (diff - margin, diff + margin)

            # Approximate power
            power = 0.0

        # Determine significance
        is_significant = p_value < self.significance_level

        # Determine winner
        winner = None
        if is_significant:
            winner = "Variant B" if mean_b > mean_a else "Variant A"

        # Generate recommendation
        recommendation = self._generate_recommendation(
            mean_a, mean_b, p_value, effect_size, power, is_significant
        )

        return AdvancedABResult(
            test_name=test_type,
            variant_a_mean=mean_a,
            variant_b_mean=mean_b,
            variant_a_std=std_a,
            variant_b_std=std_b,
            difference=mean_b - mean_a,
            effect_size=effect_size,
            t_statistic=t_stat,
            p_value=p_value,
            confidence_interval=ci,
            power=power,
            is_significant=is_significant,
            winner=winner,
            recommendation=recommendation,
            metadata={
                'n_a': n_a,
                'n_b': n_b,
                'using_statsmodels': self.sm_available
            }
        )

    def bayesian_ab_test(
        self,
        variant_a: List[float],
        variant_b: List[float],
        prior_mean: float = 0.5,
        prior_std: float = 0.1
    ) -> Dict[str, Any]:
        """
        Bayesian A/B test (if statsmodels available)

        Args:
            variant_a: Scores for variant A
            variant_b: Scores for variant B
            prior_mean: Prior mean for conversion rate
            prior_std: Prior std for conversion rate

        Returns:
            Bayesian test results
        """
        if not self.sm_available:
            logger.warning("Bayesian A/B test requires statsmodels")
            return {'available': False, 'message': 'statsmodels required'}

        # Simplified Bayesian approach
        a = np.array(variant_a)
        b = np.array(variant_b)

        # Calculate posterior distributions (assuming normal)
        mean_a = np.mean(a)
        mean_b = np.mean(b)
        std_a = np.std(a)
        std_b = np.std(b)

        # Probability B > A (Monte Carlo approximation)
        n_samples = 10000
        samples_a = np.random.normal(mean_a, std_a / np.sqrt(len(a)), n_samples)
        samples_b = np.random.normal(mean_b, std_b / np.sqrt(len(b)), n_samples)

        prob_b_better = np.mean(samples_b > samples_a)

        return {
            'available': True,
            'prob_b_better_than_a': prob_b_better,
            'prob_a_better_than_b': 1 - prob_b_better,
            'posterior_mean_a': mean_a,
            'posterior_mean_b': mean_b,
            'recommendation': 'Choose B' if prob_b_better > 0.95 else 'Continue testing' if prob_b_better > 0.75 else 'Choose A' if prob_b_better < 0.05 else 'No clear winner'
        }

    def sequential_testing(
        self,
        variant_a: List[float],
        variant_b: List[float],
        alpha: float = 0.05,
        beta: float = 0.2
    ) -> Dict[str, Any]:
        """
        Sequential probability ratio test

        Args:
            variant_a: Current scores for A
            variant_b: Current scores for B
            alpha: Type I error rate
            beta: Type II error rate

        Returns:
            Sequential test results with decision
        """
        result = self.advanced_ab_test(variant_a, variant_b)

        # Calculate boundaries (simplified)
        A = np.log((1 - beta) / alpha)
        B = np.log(beta / (1 - alpha))

        # Log likelihood ratio (simplified)
        llr = result.t_statistic

        decision = "continue"
        if llr >= A:
            decision = "stop_b_better"
        elif llr <= B:
            decision = "stop_a_better"

        return {
            'decision': decision,
            'llr': llr,
            'upper_boundary': A,
            'lower_boundary': B,
            'current_p_value': result.p_value,
            'samples_a': len(variant_a),
            'samples_b': len(variant_b),
            'recommendation': self._sequential_recommendation(decision)
        }

    def power_analysis(
        self,
        effect_size: float,
        alpha: float = 0.05,
        power: float = 0.8,
        ratio: float = 1.0
    ) -> Dict[str, Any]:
        """
        Calculate required sample size for desired power

        Args:
            effect_size: Expected Cohen's d
            alpha: Significance level
            power: Desired statistical power
            ratio: Ratio of sample sizes (n2/n1)

        Returns:
            Sample size requirements
        """
        if not self.sm_available:
            # Approximation without statsmodels
            z_alpha = 1.96  # For alpha=0.05
            z_beta = 0.84   # For power=0.8

            n1 = ((z_alpha + z_beta) / effect_size) ** 2 * (1 + ratio) / ratio
            n2 = n1 * ratio

            return {
                'n1_required': int(np.ceil(n1)),
                'n2_required': int(np.ceil(n2)),
                'total_required': int(np.ceil(n1 + n2)),
                'using_statsmodels': False
            }

        # Use statsmodels
        n1 = self.tt_ind_solve_power(
            effect_size=effect_size,
            alpha=alpha,
            power=power,
            ratio=ratio,
            alternative='two-sided'
        )

        n2 = n1 * ratio

        return {
            'n1_required': int(np.ceil(n1)),
            'n2_required': int(np.ceil(n2)),
            'total_required': int(np.ceil(n1 + n2)),
            'effect_size': effect_size,
            'alpha': alpha,
            'power': power,
            'using_statsmodels': True
        }

    def _generate_recommendation(
        self,
        mean_a: float,
        mean_b: float,
        p_value: float,
        effect_size: float,
        power: float,
        is_significant: bool
    ) -> str:
        """Generate actionable recommendation"""
        if not is_significant:
            if abs(effect_size) < 0.2:
                return "No meaningful difference detected. Either variant is acceptable."
            else:
                return "Difference detected but not statistically significant. Consider collecting more data."

        # Significant difference
        winner = "B" if mean_b > mean_a else "A"
        improvement = abs((mean_b - mean_a) / mean_a * 100)

        if abs(effect_size) > 0.8:
            magnitude = "large"
        elif abs(effect_size) > 0.5:
            magnitude = "medium"
        else:
            magnitude = "small"

        recommendation = f"Choose Variant {winner}. "
        recommendation += f"Shows {magnitude} effect size ({abs(effect_size):.2f}) "
        recommendation += f"with {improvement:.1f}% improvement. "

        if power > 0 and power < 0.8:
            recommendation += "Note: Statistical power is low - results may not be reliable."

        return recommendation

    def _sequential_recommendation(self, decision: str) -> str:
        """Generate recommendation for sequential testing"""
        if decision == "stop_b_better":
            return "Stop test and deploy Variant B"
        elif decision == "stop_a_better":
            return "Stop test and keep Variant A"
        else:
            return "Continue collecting data - no conclusive result yet"

    def generate_report(self, result: AdvancedABResult) -> str:
        """Generate comprehensive report"""
        report = "=" * 70 + "\n"
        report += "Advanced A/B Test Report\n"
        report += "=" * 70 + "\n\n"

        if not result.metadata.get('using_statsmodels'):
            report += "⚠️  Using scipy fallback (statsmodels not installed)\n\n"

        report += f"Test Type: {result.test_name}\n"
        report += f"Significance Level: {self.significance_level}\n\n"

        report += "-" * 70 + "\n"
        report += "Results:\n"
        report += "-" * 70 + "\n\n"

        report += f"Variant A: {result.variant_a_mean:.4f} ± {result.variant_a_std:.4f} (n={result.metadata['n_a']})\n"
        report += f"Variant B: {result.variant_b_mean:.4f} ± {result.variant_b_std:.4f} (n={result.metadata['n_b']})\n\n"

        report += f"Difference: {result.difference:.4f}\n"
        report += f"Effect Size (Cohen's d): {result.effect_size:.4f}\n"
        report += f"95% Confidence Interval: ({result.confidence_interval[0]:.4f}, {result.confidence_interval[1]:.4f})\n\n"

        report += f"t-statistic: {result.t_statistic:.4f}\n"
        report += f"p-value: {result.p_value:.6f}\n"

        if result.power > 0:
            report += f"Statistical Power: {result.power:.2%}\n"

        report += f"\nStatistically Significant: {'Yes' if result.is_significant else 'No'}\n"

        if result.winner:
            report += f"Winner: {result.winner}\n"

        report += "\n" + "-" * 70 + "\n"
        report += "Recommendation:\n"
        report += "-" * 70 + "\n\n"

        report += result.recommendation + "\n"

        report += "\n" + "=" * 70 + "\n"

        return report


def check_statsmodels_installation() -> bool:
    """Check if statsmodels is properly installed"""
    try:
        import statsmodels
        return True
    except ImportError:
        return False


def install_statsmodels_instructions() -> str:
    """Return installation instructions for statsmodels"""
    return """
To install statsmodels:

pip install statsmodels

For full features:

pip install statsmodels[build]

Documentation: https://www.statsmodels.org/
"""
