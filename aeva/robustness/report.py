"""
Robustness Reports

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any

@dataclass
class RobustnessReport:
    """Robustness report container"""
    model_name: str
    attack_type: str
    robustness_score: float
    timestamp: datetime = field(default_factory=datetime.now)

class RobustnessReportGenerator:
    """Generate robustness reports"""
    
    def generate_text_report(self, score) -> str:
        """Generate text report"""
        return f"Robustness Report\nAttack Success Rate: {score.attack_success_rate:.2%}\nSeverity: {score.severity.value}"
    
    def generate_html_report(self, score) -> str:
        """Generate HTML report"""
        return f"<html><body><h1>Robustness Report</h1><p>Success Rate: {score.attack_success_rate:.2%}</p></body></html>"
