"""
Statistical Tests for A/B Testing

Comprehensive statistical testing framework for A/B testing and experimentation.

Features:
- Parametric tests (t-test, z-test, ANOVA)
- Non-parametric tests (Mann-Whitney U, Wilcoxon, Kruskal-Wallis)
- Multiple comparison correction (Bonferroni, FDR, Holm)
- Effect size calculations (Cohen's d, Hedge's g, Glass's delta)
- Bootstrap confidence intervals
- Power analysis and sample size calculation
- Normality and variance tests

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from scipy import stats
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
from enum import Enum
import warnings


class TestType(Enum):
    """Types of statistical tests"""
    T_TEST = "t_test"
    Z_TEST = "z_test"
    MANN_WHITNEY = "mann_whitney_u"
    WILCOXON = "wilcoxon"
    CHI_SQUARE = "chi_square"
    ANOVA = "anova"
    KRUSKAL_WALLIS = "kruskal_wallis"


class CorrectionMethod(Enum):
    """Multiple comparison correction methods"""
    BONFERRONI = "bonferroni"
    FDR_BH = "fdr_bh"  # Benjamini-Hochberg
    FDR_BY = "fdr_by"  # Benjamini-Yekutieli
    HOLM = "holm"
    SIDAK = "sidak"


@dataclass
class TestResult:
    """Statistical test result"""
    test_type: str
    statistic: float
    p_value: float
    df: Optional[float] = None
    is_significant: bool = False
    significance_level: float = 0.05
    effect_size: Optional[float] = None
    confidence_interval: Optional[Tuple[float, float]] = None
    power: Optional[float] = None

    def __str__(self) -> str:
        result = [
            f"Test: {self.test_type}",
            f"Statistic: {self.statistic:.4f}",
            f"P-value: {self.p_value:.4f}",
            f"Significant: {'Yes' if self.is_significant else 'No'} (α={self.significance_level})"
        ]
        if self.df is not None:
            result.insert(3, f"DF: {self.df:.0f}")
        if self.effect_size is not None:
            result.append(f"Effect Size: {self.effect_size:.4f}")
        if self.confidence_interval is not None:
            result.append(f"95% CI: [{self.confidence_interval[0]:.4f}, {self.confidence_interval[1]:.4f}]")
        if self.power is not None:
            result.append(f"Power: {self.power:.4f}")
        return "\n".join(result)


class StatisticalTest:
    """Comprehensive statistical testing utilities for A/B testing"""

    def __init__(self, significance_level: float = 0.05):
        """
        Initialize statistical test framework.

        Args:
            significance_level: Alpha level for hypothesis testing (default: 0.05)
        """
        self.significance_level = significance_level

    # ========== Parametric Tests ==========

    def t_test(
        self,
        group_a: List[float],
        group_b: List[float],
        equal_var: bool = True,
        paired: bool = False
    ) -> TestResult:
        """
        Perform t-test (Student's or Welch's).

        Args:
            group_a: First group data
            group_b: Second group data
            equal_var: Assume equal variance (True=Student's, False=Welch's)
            paired: Paired t-test if True

        Returns:
            TestResult with test statistics
        """
        if paired:
            statistic, p_value = stats.ttest_rel(group_a, group_b)
            df = len(group_a) - 1
        else:
            statistic, p_value = stats.ttest_ind(group_a, group_b, equal_var=equal_var)
            if equal_var:
                df = len(group_a) + len(group_b) - 2
            else:
                # Welch's degrees of freedom
                var_a, var_b = np.var(group_a, ddof=1), np.var(group_b, ddof=1)
                n_a, n_b = len(group_a), len(group_b)
                df = (var_a/n_a + var_b/n_b)**2 / (
                    (var_a/n_a)**2/(n_a-1) + (var_b/n_b)**2/(n_b-1)
                )

        effect_size = self.cohens_d(group_a, group_b)
        ci = self._bootstrap_ci_diff(group_a, group_b)

        return TestResult(
            test_type="Paired t-test" if paired else ("Student's t-test" if equal_var else "Welch's t-test"),
            statistic=statistic,
            p_value=p_value,
            df=df,
            is_significant=p_value < self.significance_level,
            significance_level=self.significance_level,
            effect_size=effect_size,
            confidence_interval=ci
        )

    def z_test(
        self,
        group_a: List[float],
        group_b: List[float],
        pooled: bool = True
    ) -> TestResult:
        """
        Perform two-sample z-test (for large samples).

        Args:
            group_a: First group data
            group_b: Second group data
            pooled: Use pooled variance estimate

        Returns:
            TestResult with test statistics
        """
        mean_a, mean_b = np.mean(group_a), np.mean(group_b)
        var_a, var_b = np.var(group_a, ddof=1), np.var(group_b, ddof=1)
        n_a, n_b = len(group_a), len(group_b)

        if pooled:
            pooled_var = ((n_a - 1) * var_a + (n_b - 1) * var_b) / (n_a + n_b - 2)
            se = np.sqrt(pooled_var * (1/n_a + 1/n_b))
        else:
            se = np.sqrt(var_a/n_a + var_b/n_b)

        z_stat = (mean_a - mean_b) / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

        effect_size = self.cohens_d(group_a, group_b)
        ci = self._bootstrap_ci_diff(group_a, group_b)

        return TestResult(
            test_type="Two-sample z-test",
            statistic=z_stat,
            p_value=p_value,
            is_significant=p_value < self.significance_level,
            significance_level=self.significance_level,
            effect_size=effect_size,
            confidence_interval=ci
        )

    def anova(self, *groups: List[float]) -> TestResult:
        """
        Perform one-way ANOVA.

        Args:
            *groups: Variable number of groups to compare

        Returns:
            TestResult with F-statistic
        """
        f_stat, p_value = stats.f_oneway(*groups)

        # Calculate degrees of freedom
        k = len(groups)  # number of groups
        n = sum(len(g) for g in groups)  # total samples
        df_between = k - 1
        df_within = n - k

        # Effect size (eta-squared)
        grand_mean = np.mean(np.concatenate(groups))
        ss_between = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in groups)
        ss_total = sum((x - grand_mean)**2 for g in groups for x in g)
        eta_squared = ss_between / ss_total if ss_total > 0 else 0

        return TestResult(
            test_type="One-way ANOVA",
            statistic=f_stat,
            p_value=p_value,
            df=df_between,
            is_significant=p_value < self.significance_level,
            significance_level=self.significance_level,
            effect_size=eta_squared
        )

    # ========== Non-Parametric Tests ==========

    def mann_whitney_u(
        self,
        group_a: List[float],
        group_b: List[float],
        alternative: str = "two-sided"
    ) -> TestResult:
        """
        Perform Mann-Whitney U test (non-parametric alternative to t-test).

        Args:
            group_a: First group data
            group_b: Second group data
            alternative: "two-sided", "less", or "greater"

        Returns:
            TestResult with U statistic
        """
        u_stat, p_value = stats.mannwhitneyu(
            group_a, group_b, alternative=alternative
        )

        # Calculate rank-biserial correlation as effect size
        n_a, n_b = len(group_a), len(group_b)
        r = 1 - (2*u_stat) / (n_a * n_b)  # Rank-biserial correlation

        return TestResult(
            test_type="Mann-Whitney U test",
            statistic=u_stat,
            p_value=p_value,
            is_significant=p_value < self.significance_level,
            significance_level=self.significance_level,
            effect_size=r
        )

    def wilcoxon(
        self,
        group_a: List[float],
        group_b: List[float],
        alternative: str = "two-sided"
    ) -> TestResult:
        """
        Perform Wilcoxon signed-rank test (non-parametric paired test).

        Args:
            group_a: First group data
            group_b: Second group data
            alternative: "two-sided", "less", or "greater"

        Returns:
            TestResult with W statistic
        """
        w_stat, p_value = stats.wilcoxon(
            group_a, group_b, alternative=alternative
        )

        # Calculate effect size (r = Z / sqrt(N))
        n = len(group_a)
        z = stats.norm.ppf(1 - p_value/2)  # Approximate Z-score
        r = abs(z) / np.sqrt(n)

        return TestResult(
            test_type="Wilcoxon signed-rank test",
            statistic=w_stat,
            p_value=p_value,
            is_significant=p_value < self.significance_level,
            significance_level=self.significance_level,
            effect_size=r
        )

    def kruskal_wallis(self, *groups: List[float]) -> TestResult:
        """
        Perform Kruskal-Wallis H test (non-parametric alternative to ANOVA).

        Args:
            *groups: Variable number of groups to compare

        Returns:
            TestResult with H statistic
        """
        h_stat, p_value = stats.kruskal(*groups)

        # Calculate epsilon-squared as effect size
        n = sum(len(g) for g in groups)
        k = len(groups)
        epsilon_squared = (h_stat - k + 1) / (n - k)

        return TestResult(
            test_type="Kruskal-Wallis H test",
            statistic=h_stat,
            p_value=p_value,
            df=k-1,
            is_significant=p_value < self.significance_level,
            significance_level=self.significance_level,
            effect_size=epsilon_squared
        )

    def chi_square(
        self,
        observed: List[float],
        expected: Optional[List[float]] = None
    ) -> TestResult:
        """
        Perform chi-square goodness-of-fit test.

        Args:
            observed: Observed frequencies
            expected: Expected frequencies (uniform if None)

        Returns:
            TestResult with chi-square statistic
        """
        chi2_stat, p_value = stats.chisquare(observed, expected)
        df = len(observed) - 1

        # Cramér's V as effect size
        n = sum(observed)
        cramers_v = np.sqrt(chi2_stat / (n * (min(len(observed), 2) - 1)))

        return TestResult(
            test_type="Chi-square test",
            statistic=chi2_stat,
            p_value=p_value,
            df=df,
            is_significant=p_value < self.significance_level,
            significance_level=self.significance_level,
            effect_size=cramers_v
        )

    # ========== Effect Size Calculations ==========

    def cohens_d(
        self,
        group_a: List[float],
        group_b: List[float],
        pooled: bool = True
    ) -> float:
        """
        Calculate Cohen's d effect size.

        Args:
            group_a: First group data
            group_b: Second group data
            pooled: Use pooled standard deviation

        Returns:
            Cohen's d value
        """
        mean_a, mean_b = np.mean(group_a), np.mean(group_b)

        if pooled:
            n_a, n_b = len(group_a), len(group_b)
            var_a, var_b = np.var(group_a, ddof=1), np.var(group_b, ddof=1)
            pooled_std = np.sqrt(((n_a - 1) * var_a + (n_b - 1) * var_b) / (n_a + n_b - 2))
            return (mean_a - mean_b) / pooled_std if pooled_std > 0 else 0
        else:
            # Glass's delta (use control group std)
            std_b = np.std(group_b, ddof=1)
            return (mean_a - mean_b) / std_b if std_b > 0 else 0

    def hedges_g(self, group_a: List[float], group_b: List[float]) -> float:
        """
        Calculate Hedge's g (bias-corrected Cohen's d for small samples).

        Args:
            group_a: First group data
            group_b: Second group data

        Returns:
            Hedge's g value
        """
        d = self.cohens_d(group_a, group_b, pooled=True)
        n = len(group_a) + len(group_b)
        correction = 1 - (3 / (4 * n - 9))
        return d * correction

    def glass_delta(self, group_a: List[float], group_b: List[float]) -> float:
        """
        Calculate Glass's delta (uses control group std only).

        Args:
            group_a: Treatment group data
            group_b: Control group data

        Returns:
            Glass's delta value
        """
        return self.cohens_d(group_a, group_b, pooled=False)

    # ========== Multiple Comparison Correction ==========

    def correct_pvalues(
        self,
        p_values: List[float],
        method: CorrectionMethod = CorrectionMethod.BONFERRONI
    ) -> List[float]:
        """
        Apply multiple comparison correction to p-values.

        Args:
            p_values: List of p-values to correct
            method: Correction method to use

        Returns:
            Corrected p-values
        """
        p_values = np.array(p_values)
        n = len(p_values)

        if method == CorrectionMethod.BONFERRONI:
            return np.minimum(p_values * n, 1.0).tolist()

        elif method == CorrectionMethod.SIDAK:
            return (1 - (1 - p_values) ** n).tolist()

        elif method == CorrectionMethod.HOLM:
            # Holm-Bonferroni method
            sorted_indices = np.argsort(p_values)
            sorted_p = p_values[sorted_indices]
            corrected = np.zeros(n)

            for i, p in enumerate(sorted_p):
                corrected[sorted_indices[i]] = min(p * (n - i), 1.0)

            # Make monotonic
            for i in range(1, n):
                if corrected[i] < corrected[i-1]:
                    corrected[i] = corrected[i-1]

            return corrected.tolist()

        elif method in [CorrectionMethod.FDR_BH, CorrectionMethod.FDR_BY]:
            # Benjamini-Hochberg or Benjamini-Yekutieli FDR control
            sorted_indices = np.argsort(p_values)
            sorted_p = p_values[sorted_indices]
            corrected = np.zeros(n)

            if method == CorrectionMethod.FDR_BH:
                c = 1.0
            else:  # FDR_BY
                c = np.sum(1.0 / np.arange(1, n + 1))

            for i in range(n-1, -1, -1):
                corrected[sorted_indices[i]] = min(
                    sorted_p[i] * n / ((i + 1) * c), 1.0
                )

            # Make monotonic
            for i in range(n-2, -1, -1):
                if corrected[i] > corrected[i+1]:
                    corrected[i] = corrected[i+1]

            return corrected.tolist()

        else:
            raise ValueError(f"Unknown correction method: {method}")

    # ========== Bootstrap Methods ==========

    def _bootstrap_ci_diff(
        self,
        group_a: List[float],
        group_b: List[float],
        n_bootstrap: int = 1000,
        ci_level: float = 0.95
    ) -> Tuple[float, float]:
        """
        Calculate bootstrap confidence interval for mean difference.

        Args:
            group_a: First group data
            group_b: Second group data
            n_bootstrap: Number of bootstrap samples
            ci_level: Confidence level (default: 0.95 for 95% CI)

        Returns:
            Tuple of (lower_bound, upper_bound)
        """
        group_a = np.array(group_a)
        group_b = np.array(group_b)

        diffs = []
        for _ in range(n_bootstrap):
            sample_a = np.random.choice(group_a, size=len(group_a), replace=True)
            sample_b = np.random.choice(group_b, size=len(group_b), replace=True)
            diffs.append(np.mean(sample_a) - np.mean(sample_b))

        alpha = 1 - ci_level
        lower = np.percentile(diffs, alpha/2 * 100)
        upper = np.percentile(diffs, (1 - alpha/2) * 100)

        return (lower, upper)

    # ========== Power Analysis ==========

    def power_analysis(
        self,
        effect_size: float,
        sample_size: int,
        alpha: float = 0.05,
        alternative: str = "two-sided"
    ) -> float:
        """
        Calculate statistical power for t-test.

        Args:
            effect_size: Expected effect size (Cohen's d)
            sample_size: Sample size per group
            alpha: Significance level
            alternative: "two-sided" or "one-sided"

        Returns:
            Statistical power (0-1)
        """
        from scipy.stats import nct, t

        df = 2 * sample_size - 2
        ncp = effect_size * np.sqrt(sample_size / 2)  # Non-centrality parameter

        if alternative == "two-sided":
            t_crit = t.ppf(1 - alpha/2, df)
            power = 1 - nct.cdf(t_crit, df, ncp) + nct.cdf(-t_crit, df, ncp)
        else:
            t_crit = t.ppf(1 - alpha, df)
            power = 1 - nct.cdf(t_crit, df, ncp)

        return power

    def sample_size_calculation(
        self,
        effect_size: float,
        power: float = 0.8,
        alpha: float = 0.05,
        alternative: str = "two-sided"
    ) -> int:
        """
        Calculate required sample size per group for desired power.

        Args:
            effect_size: Expected effect size (Cohen's d)
            power: Desired statistical power (default: 0.8)
            alpha: Significance level
            alternative: "two-sided" or "one-sided"

        Returns:
            Required sample size per group
        """
        # Binary search for sample size
        n_low, n_high = 2, 10000

        while n_high - n_low > 1:
            n_mid = (n_low + n_high) // 2
            current_power = self.power_analysis(effect_size, n_mid, alpha, alternative)

            if current_power < power:
                n_low = n_mid
            else:
                n_high = n_mid

        return n_high

    # ========== Assumption Tests ==========

    def normality_test(
        self,
        data: List[float],
        method: str = "shapiro"
    ) -> TestResult:
        """
        Test for normality of data distribution.

        Args:
            data: Data to test
            method: "shapiro" (Shapiro-Wilk) or "anderson" (Anderson-Darling)

        Returns:
            TestResult with normality test statistics
        """
        if method == "shapiro":
            statistic, p_value = stats.shapiro(data)
            test_name = "Shapiro-Wilk test"
        elif method == "anderson":
            result = stats.anderson(data, dist='norm')
            # Use 5% significance level
            statistic = result.statistic
            p_value = 0.05 if statistic > result.critical_values[2] else 0.10
            test_name = "Anderson-Darling test"
        else:
            raise ValueError(f"Unknown method: {method}")

        return TestResult(
            test_type=test_name,
            statistic=statistic,
            p_value=p_value,
            is_significant=p_value < self.significance_level,
            significance_level=self.significance_level
        )

    def variance_test(
        self,
        group_a: List[float],
        group_b: List[float]
    ) -> TestResult:
        """
        Test for equal variances (Levene's test).

        Args:
            group_a: First group data
            group_b: Second group data

        Returns:
            TestResult with Levene's test statistics
        """
        statistic, p_value = stats.levene(group_a, group_b)

        return TestResult(
            test_type="Levene's test (equal variances)",
            statistic=statistic,
            p_value=p_value,
            is_significant=p_value < self.significance_level,
            significance_level=self.significance_level
        )
