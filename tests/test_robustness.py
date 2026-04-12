"""
对抗鲁棒性模块单元测试
"""
import pytest
import numpy as np
from sklearn.preprocessing import StandardScaler
from aeva.robustness import (
    FGSMAttack,
    PGDAttack,
    BIMAttack,
    RobustnessEvaluator,
    RobustnessSeverity
)


@pytest.fixture
def scaled_data(train_test_data):
    """标准化数据"""
    X_train, X_test, y_train, y_test, feature_names = train_test_data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, y_train, y_test, feature_names


class TestFGSMAttack:
    """FGSM攻击测试"""

    def test_initialization(self, trained_model):
        """测试初始化"""
        attack = FGSMAttack(trained_model)
        assert attack.model is not None

    def test_attack_generation(self, trained_model, scaled_data):
        """测试攻击生成"""
        _, X_test_scaled, _, y_test, _ = scaled_data

        attack = FGSMAttack(trained_model)
        result = attack.attack(X_test_scaled[0], y_test[0], epsilon=0.1)

        assert result is not None
        assert result.original is not None
        assert result.adversarial is not None
        assert result.perturbation is not None
        assert isinstance(result.success, bool)
        assert result.epsilon == 0.1

    def test_perturbation_bounds(self, trained_model, scaled_data):
        """测试扰动在有效范围内"""
        _, X_test_scaled, _, y_test, _ = scaled_data

        attack = FGSMAttack(trained_model)
        result = attack.attack(X_test_scaled[0], y_test[0], epsilon=0.1)

        # 扰动应该不超过epsilon
        perturbation_norm = np.linalg.norm(result.perturbation, ord=np.inf)
        assert perturbation_norm <= 0.1 + 1e-6  # 允许小误差

    def test_different_epsilon(self, trained_model, scaled_data):
        """测试不同epsilon值"""
        _, X_test_scaled, _, y_test, _ = scaled_data

        attack = FGSMAttack(trained_model)

        for epsilon in [0.01, 0.05, 0.1, 0.2]:
            result = attack.attack(X_test_scaled[0], y_test[0], epsilon=epsilon)
            assert result.epsilon == epsilon


class TestPGDAttack:
    """PGD攻击测试"""

    def test_initialization(self, trained_model):
        """测试初始化"""
        attack = PGDAttack(trained_model)
        assert attack.model is not None

    def test_attack_generation(self, trained_model, scaled_data):
        """测试攻击生成"""
        _, X_test_scaled, _, y_test, _ = scaled_data

        attack = PGDAttack(trained_model)
        result = attack.attack(X_test_scaled[0], y_test[0], epsilon=0.1, iterations=5)

        assert result is not None
        assert result.iterations == 5

    def test_iterations(self, trained_model, scaled_data):
        """测试迭代次数"""
        _, X_test_scaled, _, y_test, _ = scaled_data

        attack = PGDAttack(trained_model)

        for num_iter in [1, 5, 10]:
            result = attack.attack(
                X_test_scaled[0], y_test[0],
                epsilon=0.1, iterations=num_iter
            )
            assert result.iterations == num_iter


class TestBIMAttack:
    """BIM攻击测试"""

    def test_initialization(self, trained_model):
        """测试初始化"""
        attack = BIMAttack(trained_model)
        assert attack.model is not None

    def test_attack_generation(self, trained_model, scaled_data):
        """测试攻击生成"""
        _, X_test_scaled, _, y_test, _ = scaled_data

        attack = BIMAttack(trained_model)
        result = attack.attack(X_test_scaled[0], y_test[0], epsilon=0.1, iterations=5)

        assert result is not None
        assert result.adversarial is not None


class TestRobustnessEvaluator:
    """鲁棒性评估器测试"""

    def test_initialization(self):
        """测试初始化"""
        evaluator = RobustnessEvaluator()
        assert evaluator is not None

    def test_evaluate_single_attack(self, trained_model, scaled_data):
        """测试评估单个攻击"""
        _, X_test_scaled, _, y_test, _ = scaled_data

        attack = FGSMAttack(trained_model)
        results = []

        for i in range(10):
            result = attack.attack(X_test_scaled[i], y_test[i], epsilon=0.1)
            results.append(result)

        evaluator = RobustnessEvaluator()
        score = evaluator.evaluate(results)

        assert score is not None
        assert 0 <= score.attack_success_rate <= 1
        assert score.total_samples == 10
        assert isinstance(score.severity, RobustnessSeverity)

    def test_severity_levels(self, trained_model, scaled_data):
        """测试严重性等级"""
        _, X_test_scaled, _, y_test, _ = scaled_data

        attack = FGSMAttack(trained_model)
        results = []

        for i in range(20):
            result = attack.attack(X_test_scaled[i], y_test[i], epsilon=0.1)
            results.append(result)

        evaluator = RobustnessEvaluator()
        score = evaluator.evaluate(results)

        # 验证严重性等级
        severity_values = [s.value for s in RobustnessSeverity]
        assert score.severity.value in severity_values

    def test_empty_results(self):
        """测试空结果"""
        evaluator = RobustnessEvaluator()

        # 空结果列表应该不崩溃
        score = evaluator.evaluate([])
        assert score.total_samples == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
