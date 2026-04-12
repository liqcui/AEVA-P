"""
LLM Correctness Evaluation Module

Evaluates LLM output correctness including:
- Accuracy and factuality checking
- Hallucination detection
- Logical reasoning validation
- Task completion scoring

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Watermark: AEVA-2026-LQC-dc68e33
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import re
import logging

logger = logging.getLogger(__name__)


@dataclass
class HallucinationResult:
    """Hallucination detection result"""
    is_hallucinated: bool
    confidence_score: float
    hallucination_type: str  # 'factual', 'logical', 'contextual'
    evidence: str
    details: Dict[str, Any]


@dataclass
class FactualityResult:
    """Factuality checking result"""
    is_factual: bool
    accuracy_score: float
    verified_claims: int
    total_claims: int
    false_claims: List[str]
    sources: List[str]


@dataclass
class TaskCompletionResult:
    """Task completion evaluation result"""
    completion_score: float
    instruction_followed: bool
    output_format_correct: bool
    completeness_score: float
    missing_elements: List[str]


class HallucinationDetector:
    """
    Detects hallucinations in LLM outputs

    Methods:
    - Self-consistency checking
    - External knowledge verification
    - Confidence scoring
    """

    def __init__(
        self,
        threshold: float = 0.7,
        use_external_kb: bool = False
    ):
        """
        Initialize hallucination detector

        Args:
            threshold: Confidence threshold for hallucination detection
            use_external_kb: Whether to use external knowledge base
        """
        self.threshold = threshold
        self.use_external_kb = use_external_kb

    def detect(
        self,
        output: str,
        context: Optional[str] = None,
        reference: Optional[str] = None,
        **kwargs
    ) -> HallucinationResult:
        """
        Detect hallucinations in output

        Args:
            output: LLM generated output
            context: Input context/prompt
            reference: Reference text or ground truth

        Returns:
            HallucinationResult with detection results
        """
        # Self-consistency check
        consistency_score = self._check_self_consistency(output)

        # Context alignment check
        context_score = 1.0
        if context:
            context_score = self._check_context_alignment(output, context)

        # Reference comparison
        reference_score = 1.0
        if reference:
            reference_score = self._check_reference_alignment(output, reference)

        # Aggregate scores
        confidence = (consistency_score + context_score + reference_score) / 3
        is_hallucinated = confidence < self.threshold

        # Determine hallucination type
        hallucination_type = self._determine_hallucination_type(
            consistency_score, context_score, reference_score
        )

        return HallucinationResult(
            is_hallucinated=is_hallucinated,
            confidence_score=confidence,
            hallucination_type=hallucination_type,
            evidence=f"Consistency: {consistency_score:.2f}, Context: {context_score:.2f}",
            details={
                'consistency_score': consistency_score,
                'context_alignment': context_score,
                'reference_alignment': reference_score
            }
        )

    def _check_self_consistency(self, output: str) -> float:
        """Check internal consistency of output"""
        # Simple heuristic: check for contradictions
        sentences = output.split('.')

        # Look for negation patterns
        negation_patterns = [
            (r'is\s+(\w+)', r'is\s+not\s+\1'),
            (r'can\s+(\w+)', r'cannot\s+\1'),
            (r'will\s+(\w+)', r'will\s+not\s+\1'),
        ]

        contradictions = 0
        for i, sent1 in enumerate(sentences):
            for sent2 in sentences[i+1:]:
                for pos_pattern, neg_pattern in negation_patterns:
                    if re.search(pos_pattern, sent1) and re.search(neg_pattern, sent2):
                        contradictions += 1

        # Score based on contradictions
        if len(sentences) == 0:
            return 1.0
        consistency_score = max(0.0, 1.0 - (contradictions / len(sentences)))
        return consistency_score

    def _check_context_alignment(self, output: str, context: str) -> float:
        """Check alignment with input context"""
        # Simple word overlap metric
        output_words = set(output.lower().split())
        context_words = set(context.lower().split())

        if len(context_words) == 0:
            return 1.0

        overlap = len(output_words & context_words)
        alignment_score = min(1.0, overlap / max(len(context_words) * 0.3, 1))
        return alignment_score

    def _check_reference_alignment(self, output: str, reference: str) -> float:
        """Check alignment with reference text"""
        # Token-level similarity
        output_tokens = set(output.lower().split())
        reference_tokens = set(reference.lower().split())

        if len(reference_tokens) == 0:
            return 1.0

        overlap = len(output_tokens & reference_tokens)
        similarity = overlap / len(reference_tokens)
        return min(1.0, similarity * 2)  # Scale up

    def _determine_hallucination_type(
        self,
        consistency: float,
        context: float,
        reference: float
    ) -> str:
        """Determine type of hallucination"""
        if consistency < 0.5:
            return 'logical'
        elif context < 0.5:
            return 'contextual'
        elif reference < 0.5:
            return 'factual'
        else:
            return 'none'


class FactualityChecker:
    """
    Checks factual accuracy of LLM outputs

    Features:
    - Claim extraction
    - Fact verification
    - Knowledge base lookup
    """

    def __init__(self, knowledge_base: Optional[Dict] = None):
        """
        Initialize factuality checker

        Args:
            knowledge_base: External knowledge base for verification
        """
        self.knowledge_base = knowledge_base or {}

    def check(
        self,
        output: str,
        ground_truth: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> FactualityResult:
        """
        Check factual accuracy

        Args:
            output: LLM output to check
            ground_truth: Known facts for verification

        Returns:
            FactualityResult with verification results
        """
        # Extract claims from output
        claims = self._extract_claims(output)

        # Verify each claim
        verified = 0
        false_claims = []
        sources = []

        for claim in claims:
            is_verified, source = self._verify_claim(claim, ground_truth)
            if is_verified:
                verified += 1
                if source:
                    sources.append(source)
            else:
                false_claims.append(claim)

        total_claims = len(claims)
        accuracy_score = verified / total_claims if total_claims > 0 else 1.0

        return FactualityResult(
            is_factual=accuracy_score > 0.8,
            accuracy_score=accuracy_score,
            verified_claims=verified,
            total_claims=total_claims,
            false_claims=false_claims,
            sources=sources
        )

    def _extract_claims(self, text: str) -> List[str]:
        """Extract factual claims from text"""
        # Simple sentence splitting as claims
        claims = [s.strip() for s in text.split('.') if s.strip()]
        return claims

    def _verify_claim(
        self,
        claim: str,
        ground_truth: Optional[Dict] = None
    ) -> Tuple[bool, Optional[str]]:
        """Verify a single claim"""
        # Simple keyword matching for demo
        if not ground_truth:
            # Without ground truth, assume verified
            return True, None

        # Check against ground truth
        for key, value in ground_truth.items():
            if key.lower() in claim.lower():
                if str(value).lower() in claim.lower():
                    return True, f"ground_truth[{key}]"

        return False, None


class TaskCompletionScorer:
    """
    Scores task completion quality

    Evaluates:
    - Instruction following
    - Output format correctness
    - Completeness
    """

    def __init__(self):
        """Initialize task completion scorer"""
        pass

    def score(
        self,
        output: str,
        instructions: str,
        expected_format: Optional[str] = None,
        required_elements: Optional[List[str]] = None,
        **kwargs
    ) -> TaskCompletionResult:
        """
        Score task completion

        Args:
            output: LLM output
            instructions: Original instructions
            expected_format: Expected output format
            required_elements: Required content elements

        Returns:
            TaskCompletionResult with completion scores
        """
        # Check instruction following
        instruction_followed = self._check_instruction_following(
            output, instructions
        )

        # Check output format
        format_correct = True
        if expected_format:
            format_correct = self._check_format(output, expected_format)

        # Check completeness
        completeness_score = 1.0
        missing_elements = []
        if required_elements:
            completeness_score, missing_elements = self._check_completeness(
                output, required_elements
            )

        # Calculate overall completion score
        completion_score = (
            (1.0 if instruction_followed else 0.0) +
            (1.0 if format_correct else 0.0) +
            completeness_score
        ) / 3

        return TaskCompletionResult(
            completion_score=completion_score,
            instruction_followed=instruction_followed,
            output_format_correct=format_correct,
            completeness_score=completeness_score,
            missing_elements=missing_elements
        )

    def _check_instruction_following(
        self,
        output: str,
        instructions: str
    ) -> bool:
        """Check if output follows instructions"""
        # Extract key verbs from instructions
        instruction_verbs = re.findall(
            r'\b(list|explain|describe|analyze|summarize|generate|create)\b',
            instructions.lower()
        )

        # Simple heuristic: check if output has reasonable length
        # for the instruction type
        if 'list' in instruction_verbs:
            # Expect bullet points or numbered list
            has_list = bool(re.search(r'[-*•\d+\.]\s', output))
            return has_list

        # General case: assume followed if output is non-empty
        return len(output.strip()) > 0

    def _check_format(self, output: str, expected_format: str) -> bool:
        """Check output format correctness"""
        format_checks = {
            'json': lambda x: x.strip().startswith('{') and x.strip().endswith('}'),
            'markdown': lambda x: bool(re.search(r'#+\s', x)),
            'list': lambda x: bool(re.search(r'[-*•\d+\.]\s', x)),
            'paragraph': lambda x: len(x.split('.')) > 2,
        }

        check_func = format_checks.get(expected_format.lower())
        if check_func:
            return check_func(output)

        return True  # Unknown format, assume correct

    def _check_completeness(
        self,
        output: str,
        required_elements: List[str]
    ) -> Tuple[float, List[str]]:
        """Check output completeness"""
        missing = []
        found = 0

        for element in required_elements:
            if element.lower() in output.lower():
                found += 1
            else:
                missing.append(element)

        completeness = found / len(required_elements) if required_elements else 1.0
        return completeness, missing


class CorrectnessEvaluator:
    """
    Comprehensive correctness evaluator

    Combines hallucination detection, factuality checking,
    and task completion scoring
    """

    def __init__(self, **kwargs):
        """Initialize correctness evaluator"""
        self.hallucination_detector = HallucinationDetector(**kwargs)
        self.factuality_checker = FactualityChecker()
        self.task_completion_scorer = TaskCompletionScorer()

    def evaluate(
        self,
        output: str,
        context: Optional[str] = None,
        reference: Optional[str] = None,
        instructions: Optional[str] = None,
        ground_truth: Optional[Dict] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Comprehensive correctness evaluation

        Args:
            output: LLM output
            context: Input context
            reference: Reference text
            instructions: Task instructions
            ground_truth: Known facts

        Returns:
            Complete evaluation results
        """
        results = {}

        # Hallucination detection
        results['hallucination'] = self.hallucination_detector.detect(
            output, context, reference
        )

        # Factuality checking
        if ground_truth:
            results['factuality'] = self.factuality_checker.check(
                output, ground_truth
            )

        # Task completion
        if instructions:
            results['task_completion'] = self.task_completion_scorer.score(
                output, instructions, **kwargs
            )

        # Overall correctness score
        scores = []
        if 'hallucination' in results:
            scores.append(results['hallucination'].confidence_score)
        if 'factuality' in results:
            scores.append(results['factuality'].accuracy_score)
        if 'task_completion' in results:
            scores.append(results['task_completion'].completion_score)

        results['overall_correctness'] = sum(scores) / len(scores) if scores else 0.0

        return results
