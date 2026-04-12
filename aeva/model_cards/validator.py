"""
Model Card Validator

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""
import logging
import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class ValidationLevel(Enum):
    """Validation severity levels"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ComplianceStandard(Enum):
    """Compliance standards for validation"""
    BASIC = "basic"
    GDPR = "gdpr"
    EU_AI_ACT = "eu_ai_act"
    HIPAA = "hipaa"
    ENTERPRISE = "enterprise"


@dataclass
class ValidationIssue:
    """Validation issue container"""
    level: ValidationLevel
    field: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class ValidationReport:
    """Comprehensive validation report"""
    is_valid: bool
    completeness_score: float
    quality_score: float
    issues: List[ValidationIssue] = field(default_factory=list)
    passed_checks: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    compliance_status: Dict[str, bool] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_errors(self) -> List[ValidationIssue]:
        """Get only error-level issues"""
        return [issue for issue in self.issues if issue.level == ValidationLevel.ERROR]

    def get_warnings(self) -> List[ValidationIssue]:
        """Get only warning-level issues"""
        return [issue for issue in self.issues if issue.level == ValidationLevel.WARNING]

    def get_summary(self) -> str:
        """Get validation summary"""
        errors = len(self.get_errors())
        warnings = len(self.get_warnings())
        status = "VALID" if self.is_valid else "INVALID"

        return f"""Validation Summary:
Status: {status}
Completeness: {self.completeness_score:.1%}
Quality Score: {self.quality_score:.1%}
Errors: {errors}
Warnings: {warnings}
Passed Checks: {len(self.passed_checks)}
"""


class ModelCardValidator:
    """Validate model card completeness and quality"""

    REQUIRED_FIELDS = {
        "basic": [
            "model_name",
            "model_version",
            "model_type",
            "intended_use",
            "performance_metrics",
            "limitations",
            "ethical_considerations",
        ],
        "enterprise": [
            "model_name",
            "model_version",
            "model_type",
            "model_architecture",
            "intended_use",
            "training_data",
            "performance_metrics",
            "limitations",
            "ethical_considerations",
            "authors",
            "timestamp",
        ],
        "gdpr": [
            "model_name",
            "model_version",
            "intended_use",
            "training_data",
            "performance_metrics",
            "limitations",
            "ethical_considerations",
            "fairness_metrics",
        ],
        "eu_ai_act": [
            "model_name",
            "model_version",
            "model_type",
            "intended_use",
            "training_data",
            "performance_metrics",
            "fairness_metrics",
            "limitations",
            "ethical_considerations",
            "compliance_frameworks",
        ],
        "hipaa": [
            "model_name",
            "model_version",
            "intended_use",
            "training_data",
            "performance_metrics",
            "limitations",
            "ethical_considerations",
            "metadata",
        ]
    }

    QUALITY_THRESHOLDS = {
        "min_description_length": 50,
        "min_limitations_length": 30,
        "min_ethics_length": 30,
        "min_metrics_count": 1,
        "min_training_data_fields": 2,
    }

    def __init__(self, standard: ComplianceStandard = ComplianceStandard.BASIC):
        """Initialize validator

        Args:
            standard: Compliance standard to validate against
        """
        self.standard = standard
        self.required_fields = self.REQUIRED_FIELDS.get(standard.value, self.REQUIRED_FIELDS["basic"])

    def validate(self, card) -> ValidationReport:
        """Validate model card

        Args:
            card: ModelCard instance to validate

        Returns:
            ValidationReport with detailed validation results
        """
        report = ValidationReport(
            is_valid=True,
            completeness_score=0.0,
            quality_score=0.0
        )

        # Run all validation checks
        self._check_required_fields(card, report)
        self._check_field_quality(card, report)
        self._check_performance_metrics(card, report)
        self._check_training_data(card, report)
        self._check_fairness_metrics(card, report)
        self._check_compliance_requirements(card, report)

        # Calculate scores
        report.completeness_score = self._calculate_completeness(card)
        report.quality_score = self._calculate_quality_score(card, report)

        # Final validation status
        report.is_valid = len(report.get_errors()) == 0

        logger.info(f"Validation completed: {report.is_valid}, "
                   f"Completeness: {report.completeness_score:.1%}, "
                   f"Quality: {report.quality_score:.1%}")

        return report

    def _check_required_fields(self, card, report: ValidationReport):
        """Check if all required fields are present"""
        for field in self.required_fields:
            value = getattr(card, field, None)

            if value is None or value == "" or (isinstance(value, (list, dict)) and not value):
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    field=field,
                    message=f"Required field '{field}' is missing or empty",
                    suggestion=f"Please provide a value for '{field}'"
                ))
            else:
                report.passed_checks.append(f"Field '{field}' present")

    def _check_field_quality(self, card, report: ValidationReport):
        """Check the quality of field contents"""

        # Check intended use description
        if hasattr(card, 'intended_use') and card.intended_use:
            if len(card.intended_use) < self.QUALITY_THRESHOLDS["min_description_length"]:
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    field="intended_use",
                    message=f"Intended use description is too brief ({len(card.intended_use)} chars)",
                    suggestion=f"Provide at least {self.QUALITY_THRESHOLDS['min_description_length']} characters"
                ))
            else:
                report.passed_checks.append("Intended use description is adequate")

            # Check for vague language
            vague_terms = ["general", "various", "etc", "stuff", "things"]
            if any(term in card.intended_use.lower() for term in vague_terms):
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    field="intended_use",
                    message="Intended use contains vague terminology",
                    suggestion="Be more specific about intended use cases"
                ))

        # Check limitations
        if hasattr(card, 'limitations') and card.limitations:
            if len(card.limitations) < self.QUALITY_THRESHOLDS["min_limitations_length"]:
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    field="limitations",
                    message=f"Limitations description is too brief ({len(card.limitations)} chars)",
                    suggestion="Provide detailed information about model limitations"
                ))
            else:
                report.passed_checks.append("Limitations adequately documented")

        # Check ethical considerations
        if hasattr(card, 'ethical_considerations') and card.ethical_considerations:
            if len(card.ethical_considerations) < self.QUALITY_THRESHOLDS["min_ethics_length"]:
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    field="ethical_considerations",
                    message=f"Ethical considerations too brief ({len(card.ethical_considerations)} chars)",
                    suggestion="Provide comprehensive ethical analysis"
                ))
            else:
                report.passed_checks.append("Ethical considerations adequately documented")

        # Check model version format
        if hasattr(card, 'model_version') and card.model_version:
            version_pattern = r'^\d+\.\d+(\.\d+)?'
            if not re.match(version_pattern, card.model_version):
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    field="model_version",
                    message="Model version does not follow semantic versioning",
                    suggestion="Use format: MAJOR.MINOR.PATCH (e.g., 1.0.0)"
                ))

    def _check_performance_metrics(self, card, report: ValidationReport):
        """Validate performance metrics"""
        if not hasattr(card, 'performance_metrics'):
            return

        metrics = card.performance_metrics

        # Check if metrics exist
        if hasattr(metrics, 'metrics') and isinstance(metrics.metrics, dict):
            if not metrics.metrics:
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    field="performance_metrics",
                    message="No performance metrics provided",
                    suggestion="Add at least one performance metric"
                ))
            elif len(metrics.metrics) < self.QUALITY_THRESHOLDS["min_metrics_count"]:
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    field="performance_metrics",
                    message=f"Only {len(metrics.metrics)} metric(s) provided",
                    suggestion="Consider adding multiple metrics for comprehensive evaluation"
                ))
            else:
                report.passed_checks.append(f"Performance metrics present ({len(metrics.metrics)} metrics)")

            # Check metric values are in valid range
            for metric_name, value in metrics.metrics.items():
                if not isinstance(value, (int, float)):
                    report.issues.append(ValidationIssue(
                        level=ValidationLevel.ERROR,
                        field=f"performance_metrics.{metric_name}",
                        message=f"Metric '{metric_name}' has invalid value type",
                        suggestion="Metric values should be numeric"
                    ))
                elif value < 0 or value > 1:
                    # Many metrics are in [0, 1] range
                    report.issues.append(ValidationIssue(
                        level=ValidationLevel.INFO,
                        field=f"performance_metrics.{metric_name}",
                        message=f"Metric '{metric_name}' value {value} is outside typical [0, 1] range",
                        suggestion="Verify this is the correct scale for this metric"
                    ))

        # Check for primary metric
        if hasattr(metrics, 'primary_metric'):
            if not metrics.primary_metric:
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    field="performance_metrics.primary_metric",
                    message="Primary metric not specified",
                    suggestion="Specify which metric is the primary evaluation metric"
                ))
            else:
                report.passed_checks.append(f"Primary metric specified: {metrics.primary_metric}")

        # Check for test set information
        if hasattr(metrics, 'test_set_size'):
            if not metrics.test_set_size or metrics.test_set_size == 0:
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    field="performance_metrics.test_set_size",
                    message="Test set size not specified",
                    suggestion="Document the size of the test set"
                ))
            else:
                report.passed_checks.append(f"Test set size documented: {metrics.test_set_size}")

    def _check_training_data(self, card, report: ValidationReport):
        """Validate training data information"""
        if not hasattr(card, 'training_data'):
            return

        training_data = card.training_data
        filled_fields = 0

        # Check key training data fields
        if hasattr(training_data, 'description') and training_data.description:
            filled_fields += 1
            if len(training_data.description) < 50:
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    field="training_data.description",
                    message="Training data description is too brief",
                    suggestion="Provide detailed description of training data"
                ))
            else:
                report.passed_checks.append("Training data description present")

        if hasattr(training_data, 'size') and training_data.size > 0:
            filled_fields += 1
            report.passed_checks.append(f"Training data size documented: {training_data.size}")
        else:
            report.issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                field="training_data.size",
                message="Training data size not specified",
                suggestion="Document the number of training samples"
            ))

        if hasattr(training_data, 'sources') and training_data.sources:
            filled_fields += 1
            report.passed_checks.append("Training data sources documented")

        if hasattr(training_data, 'features') and training_data.features:
            filled_fields += 1
            report.passed_checks.append(f"Features documented ({len(training_data.features)} features)")

        # Overall training data completeness
        if filled_fields < self.QUALITY_THRESHOLDS["min_training_data_fields"]:
            report.issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                field="training_data",
                message=f"Training data information incomplete ({filled_fields} fields filled)",
                suggestion="Provide comprehensive training data information"
            ))

    def _check_fairness_metrics(self, card, report: ValidationReport):
        """Validate fairness metrics"""
        if not hasattr(card, 'fairness_metrics') or card.fairness_metrics is None:
            if self.standard in [ComplianceStandard.GDPR, ComplianceStandard.EU_AI_ACT, ComplianceStandard.ENTERPRISE]:
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    field="fairness_metrics",
                    message="Fairness metrics required for this compliance standard",
                    suggestion="Add fairness metrics analysis"
                ))
            else:
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.INFO,
                    field="fairness_metrics",
                    message="Fairness metrics not provided",
                    suggestion="Consider adding fairness analysis for comprehensive evaluation"
                ))
            return

        fairness = card.fairness_metrics
        metrics_present = 0

        if hasattr(fairness, 'demographic_parity') and fairness.demographic_parity is not None:
            metrics_present += 1
            report.passed_checks.append("Demographic parity metric present")

        if hasattr(fairness, 'equal_opportunity') and fairness.equal_opportunity is not None:
            metrics_present += 1
            report.passed_checks.append("Equal opportunity metric present")

        if hasattr(fairness, 'disparate_impact') and fairness.disparate_impact is not None:
            metrics_present += 1
            report.passed_checks.append("Disparate impact metric present")

        if metrics_present == 0:
            report.issues.append(ValidationIssue(
                level=ValidationLevel.ERROR,
                field="fairness_metrics",
                message="Fairness metrics object present but no metrics calculated",
                suggestion="Calculate at least one fairness metric"
            ))

        # Check protected attributes
        if hasattr(fairness, 'protected_attributes'):
            if not fairness.protected_attributes:
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    field="fairness_metrics.protected_attributes",
                    message="Protected attributes not specified",
                    suggestion="Document which attributes were evaluated for fairness"
                ))
            else:
                report.passed_checks.append(f"Protected attributes documented: {len(fairness.protected_attributes)}")

    def _check_compliance_requirements(self, card, report: ValidationReport):
        """Check compliance-specific requirements"""
        compliance_checks = {
            ComplianceStandard.GDPR: self._check_gdpr_compliance,
            ComplianceStandard.EU_AI_ACT: self._check_eu_ai_act_compliance,
            ComplianceStandard.HIPAA: self._check_hipaa_compliance,
        }

        check_func = compliance_checks.get(self.standard)
        if check_func:
            check_func(card, report)

    def _check_gdpr_compliance(self, card, report: ValidationReport):
        """Check GDPR-specific requirements"""
        # Check for data protection information
        if hasattr(card, 'metadata'):
            if 'data_protection' not in card.metadata:
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    field="metadata.data_protection",
                    message="GDPR requires data protection information",
                    suggestion="Add data protection measures to metadata"
                ))
            else:
                report.passed_checks.append("Data protection documented")

        # Check for explainability
        if hasattr(card, 'metadata'):
            if 'explainability' not in card.metadata:
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    field="metadata.explainability",
                    message="GDPR recommends explainability documentation",
                    suggestion="Document model explainability capabilities"
                ))

        report.compliance_status['gdpr'] = len([i for i in report.issues if 'gdpr' in i.message.lower()]) == 0

    def _check_eu_ai_act_compliance(self, card, report: ValidationReport):
        """Check EU AI Act requirements"""
        # Check risk category
        if hasattr(card, 'metadata'):
            if 'risk_category' not in card.metadata:
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    field="metadata.risk_category",
                    message="EU AI Act requires risk categorization",
                    suggestion="Add risk_category to metadata (minimal/limited/high/unacceptable)"
                ))
            else:
                report.passed_checks.append("Risk category documented")

        # Check human oversight
        if hasattr(card, 'metadata'):
            if 'human_oversight' not in card.metadata:
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    field="metadata.human_oversight",
                    message="EU AI Act requires human oversight documentation",
                    suggestion="Document human oversight mechanisms"
                ))

        report.compliance_status['eu_ai_act'] = len([i for i in report.issues if 'eu ai act' in i.message.lower()]) == 0

    def _check_hipaa_compliance(self, card, report: ValidationReport):
        """Check HIPAA requirements"""
        # Check PHI handling
        if hasattr(card, 'metadata'):
            if 'phi_handling' not in card.metadata:
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    field="metadata.phi_handling",
                    message="HIPAA requires PHI handling documentation",
                    suggestion="Document how Protected Health Information is handled"
                ))

        # Check encryption
        if hasattr(card, 'metadata'):
            if 'encryption' not in card.metadata:
                report.issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    field="metadata.encryption",
                    message="HIPAA requires encryption documentation",
                    suggestion="Document encryption measures for data at rest and in transit"
                ))

        report.compliance_status['hipaa'] = len([i for i in report.issues if 'hipaa' in i.message.lower()]) == 0

    def _calculate_completeness(self, card) -> float:
        """Calculate completeness percentage

        Args:
            card: ModelCard instance

        Returns:
            Completeness score from 0.0 to 1.0
        """
        total_fields = len(self.required_fields)
        filled_fields = 0

        for field in self.required_fields:
            value = getattr(card, field, None)
            if value is not None and value != "" and (not isinstance(value, (list, dict)) or value):
                filled_fields += 1

        return filled_fields / total_fields if total_fields > 0 else 0.0

    def _calculate_quality_score(self, card, report: ValidationReport) -> float:
        """Calculate overall quality score

        Args:
            card: ModelCard instance
            report: Validation report

        Returns:
            Quality score from 0.0 to 1.0
        """
        # Start with completeness as base
        score = report.completeness_score

        # Deduct points for issues
        errors = len(report.get_errors())
        warnings = len(report.get_warnings())

        # Each error reduces score by 10%, warnings by 5%
        score -= (errors * 0.10)
        score -= (warnings * 0.05)

        # Bonus for having fairness metrics
        if hasattr(card, 'fairness_metrics') and card.fairness_metrics is not None:
            score += 0.05

        # Bonus for environmental impact
        if hasattr(card, 'environmental_impact') and card.environmental_impact:
            score += 0.03

        # Bonus for references
        if hasattr(card, 'references') and card.references:
            score += 0.02

        return max(0.0, min(1.0, score))
