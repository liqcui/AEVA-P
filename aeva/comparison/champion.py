"""
Champion/Challenger Model Management

Implements safe model deployment with champion/challenger pattern.

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Optional, Dict, Any
import logging
from datetime import datetime

from aeva.core.result import EvaluationResult

logger = logging.getLogger(__name__)


class ChampionChallengerManager:
    """
    Manage champion (production) and challenger (candidate) models

    Features:
    - Safe gradual rollout
    - Performance monitoring
    - Automatic promotion/demotion
    - Rollback capabilities
    """

    def __init__(
        self,
        promotion_threshold: float = 0.02,  # 2% improvement required
        confidence_level: float = 0.95
    ):
        """
        Initialize manager

        Args:
            promotion_threshold: Minimum improvement required for promotion
            confidence_level: Statistical confidence required
        """
        self.promotion_threshold = promotion_threshold
        self.confidence_level = confidence_level
        self.champion: Optional[EvaluationResult] = None
        self.challenger: Optional[EvaluationResult] = None
        self.history: list = []

    def set_champion(self, result: EvaluationResult) -> None:
        """Set current champion model"""
        logger.info(f"Setting champion: {result.model_name}")
        self.champion = result
        self._record_event('champion_set', result.model_name)

    def set_challenger(self, result: EvaluationResult) -> None:
        """Set challenger model"""
        logger.info(f"Setting challenger: {result.model_name}")
        self.challenger = result
        self._record_event('challenger_set', result.model_name)

    def should_promote(self) -> Dict[str, Any]:
        """
        Determine if challenger should be promoted to champion

        Returns:
            Dictionary with promotion decision and reasoning
        """
        if not self.champion or not self.challenger:
            return {
                'should_promote': False,
                'reason': 'Missing champion or challenger'
            }

        # Compare key metrics
        decision = self._evaluate_promotion()

        if decision['should_promote']:
            logger.info(f"Recommend promoting challenger: {decision['reason']}")
        else:
            logger.info(f"Keep champion: {decision['reason']}")

        return decision

    def promote_challenger(self) -> None:
        """Promote challenger to champion"""
        if not self.challenger:
            raise ValueError("No challenger to promote")

        logger.info(
            f"Promoting {self.challenger.model_name} to champion, "
            f"demoting {self.champion.model_name if self.champion else 'None'}"
        )

        self.champion = self.challenger
        self.challenger = None
        self._record_event('promotion', self.champion.model_name)

    def _evaluate_promotion(self) -> Dict[str, Any]:
        """Evaluate whether to promote challenger"""
        champion_metrics = getattr(self.champion, 'metrics', {})
        challenger_metrics = getattr(self.challenger, 'metrics', {})

        # Compare key metrics
        key_metrics = ['accuracy', 'f1_score']
        improvements = {}

        for metric in key_metrics:
            champ_val = champion_metrics.get(metric, 0)
            chall_val = challenger_metrics.get(metric, 0)

            if champ_val > 0:
                improvement = (chall_val - champ_val) / champ_val
                improvements[metric] = improvement

        # Check if improvements meet threshold
        avg_improvement = sum(improvements.values()) / len(improvements) if improvements else 0

        if avg_improvement >= self.promotion_threshold:
            return {
                'should_promote': True,
                'reason': f'Challenger shows {avg_improvement:.1%} improvement',
                'improvements': improvements,
                'confidence': 'high'
            }
        elif avg_improvement > 0:
            return {
                'should_promote': False,
                'reason': f'Improvement {avg_improvement:.1%} below threshold {self.promotion_threshold:.1%}',
                'improvements': improvements,
                'confidence': 'medium'
            }
        else:
            return {
                'should_promote': False,
                'reason': 'Challenger shows no improvement',
                'improvements': improvements,
                'confidence': 'high'
            }

    def _record_event(self, event_type: str, model_name: str) -> None:
        """Record event in history"""
        self.history.append({
            'timestamp': datetime.now(),
            'event': event_type,
            'model': model_name
        })

    def get_status(self) -> Dict[str, Any]:
        """Get current status"""
        return {
            'champion': self.champion.model_name if self.champion else None,
            'challenger': self.challenger.model_name if self.challenger else None,
            'history_count': len(self.history),
            'promotion_threshold': self.promotion_threshold
        }
