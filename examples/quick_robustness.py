"""
Quick Robustness Test - Adversarial Attack Demo
快速验证对抗鲁棒性模块的核心功能
"""
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import sys
sys.path.insert(0, '.')

from aeva.robustness import FGSMAttack, PGDAttack, RobustnessEvaluator

print("=" * 70)
print("AEVA Robustness Module - Quick Test")
print("=" * 70)

# Load data
print("\n1. Loading data...")
data = load_breast_cancer()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
print(f"   ✓ Training: {len(X_train)}, Test: {len(X_test)}")

# Train model
print("\n2. Training model...")
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
print(f"   ✓ Model accuracy: {accuracy:.3f}")

# Test FGSM Attack
print("\n3. Testing FGSM Attack...")
try:
    fgsm = FGSMAttack(model)
    instance = X_test[0]
    label = y_test[0]

    result = fgsm.attack(instance, label, epsilon=0.1)

    print(f"   ✓ Original prediction: {result.original_pred}")
    print(f"   ✓ Adversarial prediction: {result.adversarial_pred}")
    print(f"   ✓ Attack success: {result.success}")
    print(f"   ✓ Perturbation norm: {np.linalg.norm(result.perturbation):.4f}")
except Exception as e:
    print(f"   ✗ FGSM test failed: {e}")

# Test PGD Attack
print("\n4. Testing PGD Attack...")
try:
    pgd = PGDAttack(model)
    result = pgd.attack(instance, label, epsilon=0.1, iterations=10)

    print(f"   ✓ Original prediction: {result.original_pred}")
    print(f"   ✓ Adversarial prediction: {result.adversarial_pred}")
    print(f"   ✓ Attack success: {result.success}")
    print(f"   ✓ Iterations: {result.iterations}")
except Exception as e:
    print(f"   ✗ PGD test failed: {e}")

# Test Robustness Evaluator
print("\n5. Testing Robustness Evaluator...")
try:
    evaluator = RobustnessEvaluator()

    # Run multiple attacks
    attack_results = []
    for i in range(min(20, len(X_test))):
        result = fgsm.attack(X_test[i], y_test[i], epsilon=0.1)
        attack_results.append(result)

    # Evaluate
    score = evaluator.evaluate(attack_results)

    print(f"   ✓ Samples evaluated: {score.total_samples}")
    print(f"   ✓ Successful attacks: {score.successful_attacks}")
    print(f"   ✓ Attack success rate: {score.attack_success_rate:.2%}")
    print(f"   ✓ Severity: {score.severity.value}")
except Exception as e:
    print(f"   ✗ Evaluator test failed: {e}")

print("\n" + "=" * 70)
print("✅ Robustness Module Test Complete!")
print("=" * 70)
