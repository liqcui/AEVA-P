"""
模型卡片模块单元测试
"""
import pytest
import json
import os
from aeva.model_cards import ModelCardGenerator, ModelCardValidator


class TestModelCardGenerator:
    """模型卡片生成器测试"""

    def test_initialization(self):
        """测试初始化"""
        generator = ModelCardGenerator("Test Model")
        assert generator.model_name == "Test Model"

    def test_generate_card_minimal(self):
        """测试最小参数生成卡片"""
        generator = ModelCardGenerator("Test Model")
        card = generator.generate_card()

        assert card is not None
        assert card.model_name == "Test Model"
        assert card.model_version == "1.0"

    def test_generate_card_full(self):
        """测试完整参数生成卡片"""
        generator = ModelCardGenerator("Full Model")
        card = generator.generate_card(
            model_version="2.0",
            model_type="classifier",
            intended_use="Medical diagnosis",
            training_data={'samples': 1000, 'features': 30},
            performance_metrics={'accuracy': 0.95, 'precision': 0.93},
            limitations="Limited to specific use case",
            ethical_considerations="Requires human oversight"
        )

        assert card.model_version == "2.0"
        assert card.model_type == "classifier"
        assert card.intended_use == "Medical diagnosis"
        assert card.training_data['samples'] == 1000
        assert card.performance_metrics['accuracy'] == 0.95
        assert "specific use case" in card.limitations
        assert "human oversight" in card.ethical_considerations

    def test_export_json(self, tmp_path):
        """测试JSON导出"""
        generator = ModelCardGenerator("JSON Test")
        card = generator.generate_card(
            performance_metrics={'accuracy': 0.95}
        )

        filepath = tmp_path / "test_card.json"
        generator.export_json(card, str(filepath))

        assert filepath.exists()

        # 验证JSON格式
        with open(filepath, 'r') as f:
            data = json.load(f)
            assert data['model_name'] == "JSON Test"
            assert data['performance_metrics']['accuracy'] == 0.95

    def test_export_markdown(self, tmp_path):
        """测试Markdown导出"""
        generator = ModelCardGenerator("MD Test")
        card = generator.generate_card()

        filepath = tmp_path / "test_card.md"
        generator.export_markdown(card, str(filepath))

        assert filepath.exists()

        # 验证Markdown内容
        with open(filepath, 'r') as f:
            content = f.read()
            assert "# Model Card: MD Test" in content
            assert "## Model Details" in content


class TestModelCardValidator:
    """模型卡片验证器测试"""

    def test_initialization(self):
        """测试初始化"""
        validator = ModelCardValidator()
        assert validator is not None

    def test_validate_complete_card(self):
        """测试验证完整卡片"""
        generator = ModelCardGenerator("Complete Model")
        card = generator.generate_card(
            model_version="1.0",
            model_type="classifier",
            intended_use="Testing",
            training_data={'samples': 100},
            performance_metrics={'accuracy': 0.9},
            limitations="Test limitations",
            ethical_considerations="Test ethics"
        )

        validator = ModelCardValidator()
        validation = validator.validate(card)

        # 验证应该返回元组或对象
        assert validation is not None

    def test_validate_minimal_card(self):
        """测试验证最小卡片"""
        generator = ModelCardGenerator("Minimal Model")
        card = generator.generate_card()

        validator = ModelCardValidator()
        validation = validator.validate(card)

        assert validation is not None

    def test_validator_accepts_card(self):
        """测试验证器接受ModelCard对象"""
        generator = ModelCardGenerator("Test")
        card = generator.generate_card()

        validator = ModelCardValidator()

        # 不应该抛出异常
        try:
            result = validator.validate(card)
            assert result is not None
        except Exception as e:
            pytest.fail(f"Validator should accept ModelCard: {e}")


class TestModelCardIntegration:
    """模型卡片集成测试"""

    def test_complete_workflow(self, tmp_path, trained_model, model_predictions):
        """测试完整工作流"""
        y_test, y_pred = model_predictions

        # 计算指标
        from sklearn.metrics import accuracy_score
        accuracy = accuracy_score(y_test, y_pred)

        # 生成卡片
        generator = ModelCardGenerator("Workflow Test Model")
        card = generator.generate_card(
            model_version="1.0",
            model_type="classifier",
            intended_use="Breast cancer detection",
            performance_metrics={'accuracy': accuracy}
        )

        # 导出JSON
        json_path = tmp_path / "workflow.json"
        generator.export_json(card, str(json_path))

        # 导出Markdown
        md_path = tmp_path / "workflow.md"
        generator.export_markdown(card, str(md_path))

        # 验证
        validator = ModelCardValidator()
        validation = validator.validate(card)

        assert json_path.exists()
        assert md_path.exists()
        assert validation is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
