"""
Quick Model Cards Test - Model Documentation Demo
快速验证模型卡片模块的核心功能
"""
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import sys
sys.path.insert(0, '.')

from aeva.model_cards import ModelCardGenerator, ModelCardValidator

print("=" * 70)
print("AEVA Model Cards Module - Quick Test")
print("=" * 70)

# Load and train model
print("\n1. Training model...")
data = load_breast_cancer()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(f"   ✓ Model trained on {len(X_train)} samples")

# Calculate metrics
metrics = {
    'accuracy': accuracy_score(y_test, y_pred),
    'precision': precision_score(y_test, y_pred),
    'recall': recall_score(y_test, y_pred),
    'f1': f1_score(y_test, y_pred)
}
print(f"   ✓ Accuracy: {metrics['accuracy']:.3f}")

# Test Model Card Generator
print("\n2. Testing Model Card Generator...")
try:
    generator = ModelCardGenerator("Breast Cancer Classifier")

    card = generator.generate_card(
        model_version="1.0",
        model_type="classifier",
        intended_use="Medical diagnosis support - breast cancer detection",
        training_data={
            'dataset': 'Breast Cancer Wisconsin',
            'n_samples': len(X_train),
            'n_features': X_train.shape[1]
        },
        performance_metrics=metrics,
        ethical_considerations=[
            "Model should not be used as sole diagnostic tool",
            "Requires medical professional oversight"
        ],
        limitations=[
            "Limited to specific cancer types",
            "Trained on historical data"
        ]
    )

    print(f"   ✓ Model card generated")
    print(f"   ✓ Model: {card.model_name} v{card.model_version}")
    print(f"   ✓ Type: {card.model_type}")
    print(f"   ✓ Metrics: {len(card.performance_metrics)} recorded")
except Exception as e:
    print(f"   ✗ Generator test failed: {e}")

# Test JSON Export
print("\n3. Testing JSON Export...")
try:
    json_output = generator.export_json(card)
    print(f"   ✓ JSON export successful ({len(json_output)} characters)")

    # Save to file
    with open('/tmp/model_card.json', 'w') as f:
        f.write(json_output)
    print(f"   ✓ Saved to /tmp/model_card.json")
except Exception as e:
    print(f"   ✗ JSON export failed: {e}")

# Test Markdown Export
print("\n4. Testing Markdown Export...")
try:
    md_output = generator.export_markdown(card)
    print(f"   ✓ Markdown export successful ({len(md_output)} characters)")

    # Save to file
    with open('/tmp/model_card.md', 'w') as f:
        f.write(md_output)
    print(f"   ✓ Saved to /tmp/model_card.md")
except Exception as e:
    print(f"   ✗ Markdown export failed: {e}")

# Test Model Card Validator
print("\n5. Testing Model Card Validator...")
try:
    validator = ModelCardValidator()

    validation = validator.validate(card)

    print(f"   ✓ Validation complete")
    print(f"   ✓ Valid: {validation.is_valid}")
    print(f"   ✓ Completeness: {validation.completeness_score:.1%}")
    print(f"   ✓ Warnings: {len(validation.warnings)}")
    print(f"   ✓ Errors: {len(validation.errors)}")

    if validation.missing_fields:
        print(f"   ℹ Missing fields: {', '.join(validation.missing_fields)}")
except Exception as e:
    print(f"   ✗ Validator test failed: {e}")

print("\n" + "=" * 70)
print("✅ Model Cards Module Test Complete!")
print("=" * 70)
