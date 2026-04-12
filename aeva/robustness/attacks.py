"""
Adversarial Attack Implementations

Provides common adversarial attacks:
- FGSM (Fast Gradient Sign Method)
- PGD (Projected Gradient Descent)
- BIM (Basic Iterative Method)

Note: This is a simplified implementation for demonstration.
For production use, consider using Adversarial Robustness Toolbox (ART).

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
from dataclasses import dataclass
from typing import Any, Callable, Optional
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class AttackResult:
    """Container for attack results"""
    original: np.ndarray
    adversarial: np.ndarray
    perturbation: np.ndarray
    original_pred: Any
    adversarial_pred: Any
    success: bool
    epsilon: float
    iterations: int = 1


class AdversarialAttack:
    """Base class for adversarial attacks"""

    def __init__(self, model: Any, loss_fn: Optional[Callable] = None):
        self.model = model
        self.loss_fn = loss_fn or self._default_loss

    def _default_loss(self, y_true, y_pred):
        """Default cross-entropy loss"""
        return -np.sum(y_true * np.log(y_pred + 1e-10))

    def attack(self, x: np.ndarray, y: np.ndarray, **kwargs) -> AttackResult:
        raise NotImplementedError


class FGSMAttack(AdversarialAttack):
    """
    Fast Gradient Sign Method (FGSM)

    Generates adversarial examples using sign of gradient.
    Fast but simple single-step attack.
    """

    def attack(self, x: np.ndarray, y: np.ndarray, epsilon: float = 0.1) -> AttackResult:
        """
        Generate FGSM adversarial example

        Args:
            x: Input sample
            y: True label
            epsilon: Perturbation magnitude

        Returns:
            Attack result
        """
        # Get original prediction
        orig_pred = self.model.predict(x.reshape(1, -1))[0]

        # Compute gradient (simplified - numerical approximation)
        grad = self._compute_gradient(x, y)

        # Create perturbation
        perturbation = epsilon * np.sign(grad)
        x_adv = x + perturbation

        # Clip to valid range
        x_adv = np.clip(x_adv, 0, 1)

        # Get adversarial prediction
        adv_pred = self.model.predict(x_adv.reshape(1, -1))[0]

        # Check success
        success = orig_pred != adv_pred if not hasattr(orig_pred, '__len__') else \
                  np.argmax(orig_pred) != np.argmax(adv_pred)

        return AttackResult(
            original=x,
            adversarial=x_adv,
            perturbation=perturbation,
            original_pred=orig_pred,
            adversarial_pred=adv_pred,
            success=success,
            epsilon=epsilon
        )

    def _compute_gradient(self, x: np.ndarray, y: np.ndarray, delta: float = 1e-4) -> np.ndarray:
        """Numerical gradient approximation"""
        grad = np.zeros_like(x)

        for i in range(len(x)):
            x_plus = x.copy()
            x_plus[i] += delta
            x_minus = x.copy()
            x_minus[i] -= delta

            pred_plus = self.model.predict_proba(x_plus.reshape(1, -1))[0] if hasattr(self.model, 'predict_proba') else self.model.predict(x_plus.reshape(1, -1))[0]
            pred_minus = self.model.predict_proba(x_minus.reshape(1, -1))[0] if hasattr(self.model, 'predict_proba') else self.model.predict(x_minus.reshape(1, -1))[0]

            grad[i] = (pred_plus[np.argmax(y)] - pred_minus[np.argmax(y)]) / (2 * delta)

        return grad


class PGDAttack(AdversarialAttack):
    """
    Projected Gradient Descent (PGD)

    Iterative attack with projection step.
    Stronger than FGSM.
    """

    def attack(
        self,
        x: np.ndarray,
        y: np.ndarray,
        epsilon: float = 0.1,
        alpha: float = 0.01,
        iterations: int = 10
    ) -> AttackResult:
        """
        Generate PGD adversarial example

        Args:
            x: Input sample
            y: True label
            epsilon: Maximum perturbation
            alpha: Step size
            iterations: Number of iterations

        Returns:
            Attack result
        """
        orig_pred = self.model.predict(x.reshape(1, -1))[0]

        # Initialize with small random perturbation
        x_adv = x + np.random.uniform(-epsilon, epsilon, x.shape)
        x_adv = np.clip(x_adv, 0, 1)

        # Iterative gradient steps
        for i in range(iterations):
            grad = self._compute_gradient(x_adv, y)
            x_adv = x_adv + alpha * np.sign(grad)

            # Project back to epsilon ball
            perturbation = x_adv - x
            perturbation = np.clip(perturbation, -epsilon, epsilon)
            x_adv = x + perturbation

            # Clip to valid range
            x_adv = np.clip(x_adv, 0, 1)

        adv_pred = self.model.predict(x_adv.reshape(1, -1))[0]

        success = orig_pred != adv_pred if not hasattr(orig_pred, '__len__') else \
                  np.argmax(orig_pred) != np.argmax(adv_pred)

        return AttackResult(
            original=x,
            adversarial=x_adv,
            perturbation=x_adv - x,
            original_pred=orig_pred,
            adversarial_pred=adv_pred,
            success=success,
            epsilon=epsilon,
            iterations=iterations
        )

    def _compute_gradient(self, x: np.ndarray, y: np.ndarray, delta: float = 1e-4) -> np.ndarray:
        """Numerical gradient approximation"""
        grad = np.zeros_like(x)

        for i in range(len(x)):
            x_plus = x.copy()
            x_plus[i] += delta
            x_minus = x.copy()
            x_minus[i] -= delta

            pred_plus = self.model.predict_proba(x_plus.reshape(1, -1))[0] if hasattr(self.model, 'predict_proba') else self.model.predict(x_plus.reshape(1, -1))[0]
            pred_minus = self.model.predict_proba(x_minus.reshape(1, -1))[0] if hasattr(self.model, 'predict_proba') else self.model.predict(x_minus.reshape(1, -1))[0]

            if hasattr(pred_plus, '__len__'):
                grad[i] = (pred_plus[np.argmax(y)] - pred_minus[np.argmax(y)]) / (2 * delta)
            else:
                grad[i] = (pred_plus - pred_minus) / (2 * delta)

        return grad


class BIMAttack(PGDAttack):
    """
    Basic Iterative Method (BIM)

    Special case of PGD without random initialization.
    """

    def attack(
        self,
        x: np.ndarray,
        y: np.ndarray,
        epsilon: float = 0.1,
        alpha: float = 0.01,
        iterations: int = 10
    ) -> AttackResult:
        """Generate BIM adversarial example"""
        orig_pred = self.model.predict(x.reshape(1, -1))[0]

        x_adv = x.copy()  # No random initialization (difference from PGD)

        for i in range(iterations):
            grad = self._compute_gradient(x_adv, y)
            x_adv = x_adv + alpha * np.sign(grad)

            perturbation = x_adv - x
            perturbation = np.clip(perturbation, -epsilon, epsilon)
            x_adv = x + perturbation
            x_adv = np.clip(x_adv, 0, 1)

        adv_pred = self.model.predict(x_adv.reshape(1, -1))[0]

        success = orig_pred != adv_pred if not hasattr(orig_pred, '__len__') else \
                  np.argmax(orig_pred) != np.argmax(adv_pred)

        return AttackResult(
            original=x,
            adversarial=x_adv,
            perturbation=x_adv - x,
            original_pred=orig_pred,
            adversarial_pred=adv_pred,
            success=success,
            epsilon=epsilon,
            iterations=iterations
        )


# Placeholder for C&W attack (complex, requires optimization)
class CWAttack(AdversarialAttack):
    """Carlini & Wagner Attack (Placeholder)"""

    def attack(self, x: np.ndarray, y: np.ndarray, **kwargs) -> AttackResult:
        logger.warning("C&W attack not fully implemented. Use ART library for production.")
        # Fallback to PGD
        pgd = PGDAttack(self.model, self.loss_fn)
        return pgd.attack(x, y, **kwargs)
