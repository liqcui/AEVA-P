"""
Robustness Evaluator

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
from dataclasses import dataclass
from enum import Enum
import numpy as np

logger = logging.getLogger(__name__)


class RobustnessSeverity(Enum):
    """Robustness severity levels"""
    ROBUST = "robust"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RobustnessScore:
    """Robustness evaluation results"""
    attack_success_rate: float
    average_perturbation: float
    severity: RobustnessSeverity
    total_samples: int
    successful_attacks: int


class RobustnessEvaluator:
    """Evaluate model robustness against adversarial attacks"""

    def evaluate(self, attack_results: list) -> RobustnessScore:
        """Evaluate robustness from attack results"""
        total = len(attack_results)
        successful = sum(1 for r in attack_results if r.success)

        attack_success_rate = successful / total if total > 0 else 0
        avg_perturbation = np.mean([np.linalg.norm(r.perturbation) for r in attack_results])

        # Determine severity
        if attack_success_rate < 0.1:
            severity = RobustnessSeverity.ROBUST
        elif attack_success_rate < 0.3:
            severity = RobustnessSeverity.LOW
        elif attack_success_rate < 0.6:
            severity = RobustnessSeverity.MEDIUM
        elif attack_success_rate < 0.8:
            severity = RobustnessSeverity.HIGH
        else:
            severity = RobustnessSeverity.CRITICAL

        return RobustnessScore(
            attack_success_rate=attack_success_rate,
            average_perturbation=float(avg_perturbation),
            severity=severity,
            total_samples=total,
            successful_attacks=successful
        )
