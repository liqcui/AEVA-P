"""
Model Card Validator

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""
import logging

logger = logging.getLogger(__name__)

class ModelCardValidator:
    """Validate model card completeness"""
    
    REQUIRED_FIELDS = [
        "model_name",
        "model_version",
        "intended_use",
        "performance_metrics"
    ]
    
    def validate(self, card) -> tuple:
        """Validate model card"""
        issues = []
        
        for field in self.REQUIRED_FIELDS:
            if not getattr(card, field, None):
                issues.append(f"Missing required field: {field}")
        
        if not card.performance_metrics:
            issues.append("No performance metrics provided")
        
        is_valid = len(issues) == 0
        
        return is_valid, issues
