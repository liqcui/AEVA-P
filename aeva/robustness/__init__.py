"""
AEVA Adversarial Robustness Module

Provides adversarial robustness testing and evaluation including:
- Attack generation (FGSM, PGD, BIM, C&W)
- Defense evaluation
- Robustness scoring
- Attack success rate measurement
- Perturbation visualization

Use Cases:
- Financial services security
- Medical AI safety
- Autonomous vehicle testing
- Security-critical systems
"""

from aeva.robustness.attacks import (
    AdversarialAttack,
    FGSMAttack,
    PGDAttack,
    BIMAttack,
    CWAttack,
    AttackResult
)
from aeva.robustness.evaluator import (
    RobustnessEvaluator,
    RobustnessScore,
    RobustnessSeverity
)
from aeva.robustness.defenses import (
    AdversarialDefense,
    AdversarialTraining,
    InputTransformation,
    DefenseEvaluator
)
from aeva.robustness.visualizations import (
    plot_adversarial_examples,
    plot_perturbation,
    plot_robustness_curve
)
from aeva.robustness.report import (
    RobustnessReport,
    RobustnessReportGenerator
)

__all__ = [
    # Attacks
    'AdversarialAttack',
    'FGSMAttack',
    'PGDAttack',
    'BIMAttack',
    'CWAttack',
    'AttackResult',

    # Evaluation
    'RobustnessEvaluator',
    'RobustnessScore',
    'RobustnessSeverity',

    # Defenses
    'AdversarialDefense',
    'AdversarialTraining',
    'InputTransformation',
    'DefenseEvaluator',

    # Visualization
    'plot_adversarial_examples',
    'plot_perturbation',
    'plot_robustness_curve',

    # Reporting
    'RobustnessReport',
    'RobustnessReportGenerator',
]

__version__ = '1.0.0'
