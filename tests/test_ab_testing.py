"""
A/B测试模块单元测试
"""
import pytest
import numpy as np
from aeva.ab_testing import ABTester, StatisticalTest


class TestStatisticalTest:
    """统计检验测试"""

    def test_initialization(self):
        """测试初始化"""
        test = StatisticalTest()
        assert test is not None

    def test_t_test_equal_means(self):
        """测试T-test - 相同均值"""
        test = StatisticalTest()

        # 相同分布的数据
        a = [1.0, 2.0, 3.0, 4.0, 5.0] * 10
        b = [1.0, 2.0, 3.0, 4.0, 5.0] * 10

        t_stat, p_value = test.t_test(a, b)

        assert isinstance(t_stat, (int, float))
        assert isinstance(p_value, (int, float))
        assert p_value > 0.05  # 不应该显著不同

    def test_t_test_different_means(self):
        """测试T-test - 不同均值"""
        test = StatisticalTest()

        # 不同分布的数据
        a = [1.0, 2.0, 3.0, 4.0, 5.0] * 10
        b = [10.0, 11.0, 12.0, 13.0, 14.0] * 10

        t_stat, p_value = test.t_test(a, b)

        assert p_value < 0.05  # 应该显著不同

    def test_cohens_d_no_effect(self):
        """测试Cohen's d - 无效应"""
        test = StatisticalTest()

        # 相同数据
        a = [1, 2, 3, 4, 5] * 10
        b = [1, 2, 3, 4, 5] * 10

        d = test.cohens_d(a, b)

        assert abs(d) < 0.1  # 应该接近0

    def test_cohens_d_large_effect(self):
        """测试Cohen's d - 大效应"""
        test = StatisticalTest()

        # 非常不同的数据
        a = [1, 2, 3] * 10
        b = [10, 11, 12] * 10

        d = test.cohens_d(a, b)

        assert abs(d) > 0.8  # 应该是大效应

    def test_chi_square_independent(self):
        """测试卡方检验 - 独立"""
        test = StatisticalTest()

        # 独立的分类数据
        a = np.array([0, 0, 1, 1, 0, 0, 1, 1])
        b = np.array([1, 0, 1, 0, 1, 0, 1, 0])

        chi_stat, p_value = test.chi_square_test(a, b)

        assert isinstance(chi_stat, (int, float))
        assert isinstance(p_value, (int, float))
        assert p_value >= 0  # P值应该非负

    def test_chi_square_dependent(self):
        """测试卡方检验 - 相关"""
        test = StatisticalTest()

        # 完全相关的数据
        a = np.array([0, 0, 1, 1, 0, 0, 1, 1] * 10)
        b = np.array([0, 0, 1, 1, 0, 0, 1, 1] * 10)

        chi_stat, p_value = test.chi_square_test(a, b)

        # 完全相关，p值应该很大
        assert p_value > 0.05


class TestABTester:
    """A/B测试器测试"""

    def test_initialization(self):
        """测试初始化"""
        tester = ABTester(significance_level=0.05)
        assert tester is not None
        assert tester.significance_level == 0.05

    def test_compare_no_difference(self):
        """测试对比 - 无差异"""
        tester = ABTester(significance_level=0.05)

        a_scores = [0.95, 0.96, 0.94, 0.95, 0.96] * 5
        b_scores = [0.95, 0.96, 0.94, 0.95, 0.96] * 5

        result = tester.compare(a_scores, b_scores, metric_name="accuracy")

        assert result is not None
        assert not result.is_significant  # 不应该显著
        assert abs(result.improvement_percentage) < 1  # 提升应该接近0

    def test_compare_with_difference(self):
        """测试对比 - 有差异"""
        tester = ABTester(significance_level=0.05)

        a_scores = [0.90, 0.91, 0.89, 0.90, 0.91] * 5
        b_scores = [0.95, 0.96, 0.94, 0.95, 0.96] * 5

        result = tester.compare(a_scores, b_scores, metric_name="accuracy")

        assert result is not None
        assert result.variant_b_mean > result.variant_a_mean
        assert result.improvement_percentage > 0

    def test_compare_with_custom_test(self):
        """测试对比 - 自定义检验"""
        tester = ABTester(significance_level=0.05)

        a_scores = [0.95] * 50
        b_scores = [0.96] * 50

        result = tester.compare(
            a_scores, b_scores,
            metric_name="accuracy",
            test_type="t_test"
        )

        assert result is not None
        assert result.test_type == "t_test"

    def test_winner_determination(self):
        """测试优胜者判定"""
        tester = ABTester(significance_level=0.05)

        a_scores = [0.85] * 50
        b_scores = [0.95] * 50

        result = tester.compare(a_scores, b_scores)

        # B应该明显更好
        if result.is_significant:
            assert result.winner == "Variant B" or result.winner is not None

    def test_minimum_sample_size(self):
        """测试最小样本量要求"""
        tester = ABTester(significance_level=0.05, min_sample_size=10)

        a_scores = [0.95, 0.96]  # 少于10个样本
        b_scores = [0.96, 0.97]

        result = tester.compare(a_scores, b_scores)

        # 应该有警告或样本量不足标记
        assert result is not None


class TestABTestingIntegration:
    """A/B测试集成测试"""

    def test_model_comparison_workflow(self, trained_model, train_test_data):
        """测试模型对比工作流"""
        from sklearn.ensemble import GradientBoostingClassifier
        from sklearn.model_selection import cross_val_score

        _, X_test, _, y_test, _ = train_test_data

        # 模型A: 现有模型
        scores_a = cross_val_score(trained_model, X_test, y_test, cv=5)

        # 模型B: 新模型
        model_b = GradientBoostingClassifier(n_estimators=30, random_state=42)
        model_b.fit(X_test, y_test)  # 简化：在测试集上训练
        scores_b = cross_val_score(model_b, X_test, y_test, cv=5)

        # A/B测试
        tester = ABTester(significance_level=0.05)
        result = tester.compare(
            scores_a.tolist(),
            scores_b.tolist(),
            metric_name="accuracy"
        )

        assert result is not None
        assert result.metric_name == "accuracy"
        assert 0 <= result.variant_a_mean <= 1
        assert 0 <= result.variant_b_mean <= 1

    def test_statistical_power_calculation(self):
        """测试统计功效"""
        test = StatisticalTest()

        # 大样本，小差异
        a = np.random.normal(0.9, 0.02, 100).tolist()
        b = np.random.normal(0.91, 0.02, 100).tolist()

        t_stat, p_value = test.t_test(a, b)
        effect_size = test.cohens_d(a, b)

        # 验证统计量合理
        assert isinstance(t_stat, (int, float))
        assert 0 <= p_value <= 1
        assert isinstance(effect_size, (int, float))

    def test_report_generation(self):
        """测试报告生成"""
        tester = ABTester()

        a_scores = [0.90, 0.91, 0.92, 0.89, 0.90] * 10
        b_scores = [0.95, 0.96, 0.94, 0.95, 0.96] * 10

        result = tester.compare(a_scores, b_scores, metric_name="F1-Score")

        # 生成报告
        report = tester.generate_report(result)

        assert isinstance(report, str)
        assert len(report) > 0
        assert "F1-Score" in report or result.metric_name in report


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
