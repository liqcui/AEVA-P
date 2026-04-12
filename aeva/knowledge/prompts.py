"""
Prompt Engineering and Management

Build and optimize prompts for model evaluation

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
import re
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class PromptTemplate:
    """Prompt template with variables"""
    template_id: str
    name: str
    template: str
    variables: List[str]
    category: str
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def render(self, **kwargs) -> str:
        """
        Render template with variables

        Args:
            **kwargs: Variable values

        Returns:
            Rendered prompt
        """
        prompt = self.template

        for var in self.variables:
            if var not in kwargs:
                logger.warning(f"Variable '{var}' not provided for template '{self.template_id}'")
                continue

            placeholder = "{" + var + "}"
            value = str(kwargs[var])
            prompt = prompt.replace(placeholder, value)

        return prompt

    def to_dict(self) -> Dict[str, Any]:
        return {
            'template_id': self.template_id,
            'name': self.name,
            'template': self.template,
            'variables': self.variables,
            'category': self.category,
            'description': self.description,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat()
        }


class PromptBuilder:
    """
    Build prompts for various evaluation tasks

    Features:
    - Template management
    - Variable substitution
    - Multi-part prompt construction
    - Prompt validation
    """

    def __init__(self):
        """Initialize prompt builder"""
        self.templates: Dict[str, PromptTemplate] = {}
        self._load_default_templates()

        logger.info("Prompt builder initialized")

    def _load_default_templates(self) -> None:
        """Load default prompt templates"""
        # Classification template
        self.add_template(PromptTemplate(
            template_id="classification",
            name="Classification Prompt",
            template="""Classify the following text into one of these categories: {categories}

Text: {text}

Classification:""",
            variables=["categories", "text"],
            category="classification",
            description="Basic classification prompt"
        ))

        # Sentiment analysis template
        self.add_template(PromptTemplate(
            template_id="sentiment",
            name="Sentiment Analysis",
            template="""Analyze the sentiment of the following text.

Text: "{text}"

Sentiment (positive/negative/neutral):""",
            variables=["text"],
            category="sentiment",
            description="Sentiment analysis prompt"
        ))

        # NER template
        self.add_template(PromptTemplate(
            template_id="ner",
            name="Named Entity Recognition",
            template="""Extract named entities from the following text.

Text: "{text}"

Entity types to extract: {entity_types}

Entities (format: entity [type]):""",
            variables=["text", "entity_types"],
            category="ner",
            description="Named entity recognition prompt"
        ))

        # QA template
        self.add_template(PromptTemplate(
            template_id="qa",
            name="Question Answering",
            template="""Answer the following question based on the given context.

Context: {context}

Question: {question}

Answer:""",
            variables=["context", "question"],
            category="qa",
            description="Question answering prompt"
        ))

        # Evaluation template
        self.add_template(PromptTemplate(
            template_id="evaluation",
            name="Model Evaluation",
            template="""Evaluate the following model output.

Task: {task}
Input: {input}
Model Output: {output}
Evaluation Criteria: {criteria}

Evaluation (score and explanation):""",
            variables=["task", "input", "output", "criteria"],
            category="evaluation",
            description="Model output evaluation prompt"
        ))

    def add_template(self, template: PromptTemplate) -> None:
        """Add a prompt template"""
        self.templates[template.template_id] = template
        logger.info(f"Added template: {template.template_id}")

    def get_template(self, template_id: str) -> Optional[PromptTemplate]:
        """Get template by ID"""
        return self.templates.get(template_id)

    def build_prompt(
        self,
        template_id: str,
        **kwargs
    ) -> str:
        """
        Build prompt from template

        Args:
            template_id: Template ID
            **kwargs: Variable values

        Returns:
            Rendered prompt
        """
        template = self.templates.get(template_id)

        if not template:
            raise ValueError(f"Template not found: {template_id}")

        return template.render(**kwargs)

    def build_chain_of_thought_prompt(
        self,
        task: str,
        input_text: str,
        n_steps: int = 3
    ) -> str:
        """
        Build chain-of-thought prompt

        Args:
            task: Task description
            input_text: Input text
            n_steps: Number of reasoning steps

        Returns:
            Chain-of-thought prompt
        """
        prompt = f"""Task: {task}

Input: {input_text}

Let's solve this step by step:
"""

        for i in range(1, n_steps + 1):
            prompt += f"\nStep {i}:"

        prompt += "\n\nFinal Answer:"

        return prompt

    def build_zero_shot_prompt(
        self,
        task_description: str,
        input_text: str,
        output_format: Optional[str] = None
    ) -> str:
        """
        Build zero-shot prompt

        Args:
            task_description: Description of the task
            input_text: Input to process
            output_format: Optional output format description

        Returns:
            Zero-shot prompt
        """
        prompt = f"""{task_description}

Input: {input_text}
"""

        if output_format:
            prompt += f"\n{output_format}\n"

        prompt += "\nOutput:"

        return prompt

    def build_few_shot_prompt(
        self,
        task_description: str,
        examples: List[Dict[str, Any]],
        test_input: str
    ) -> str:
        """
        Build few-shot prompt

        Args:
            task_description: Task description
            examples: List of examples with 'input' and 'output'
            test_input: Test input

        Returns:
            Few-shot prompt
        """
        prompt = f"""{task_description}

Examples:
"""

        for i, example in enumerate(examples, 1):
            prompt += f"\nExample {i}:\n"
            prompt += f"Input: {example['input']}\n"
            prompt += f"Output: {example['output']}\n"

        prompt += f"\nNow solve this:\nInput: {test_input}\nOutput:"

        return prompt

    def build_evaluation_prompt(
        self,
        model_output: str,
        expected_output: Optional[str] = None,
        criteria: Optional[List[str]] = None
    ) -> str:
        """
        Build prompt for evaluating model output

        Args:
            model_output: Model's output
            expected_output: Expected/reference output
            criteria: Evaluation criteria

        Returns:
            Evaluation prompt
        """
        prompt = "Evaluate the following model output:\n\n"
        prompt += f"Model Output: {model_output}\n"

        if expected_output:
            prompt += f"Expected Output: {expected_output}\n"

        if criteria:
            prompt += "\nEvaluation Criteria:\n"
            for criterion in criteria:
                prompt += f"- {criterion}\n"

        prompt += "\nProvide a score (0-10) and explanation:"

        return prompt

    def validate_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Validate prompt quality

        Args:
            prompt: Prompt to validate

        Returns:
            Validation result
        """
        issues = []
        suggestions = []

        # Check length
        if len(prompt) < 10:
            issues.append("Prompt is too short")
        elif len(prompt) > 2000:
            issues.append("Prompt is very long, may be truncated")

        # Check for placeholders
        unresolved = re.findall(r'\{(\w+)\}', prompt)
        if unresolved:
            issues.append(f"Unresolved placeholders: {', '.join(unresolved)}")

        # Check for clear instructions
        if '?' not in prompt and ':' not in prompt:
            suggestions.append("Consider adding clearer instructions or questions")

        # Check for examples
        if 'example' not in prompt.lower() and 'e.g.' not in prompt.lower():
            suggestions.append("Consider adding examples to clarify the task")

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'suggestions': suggestions,
            'length': len(prompt),
            'word_count': len(prompt.split())
        }


class PromptOptimizer:
    """
    Optimize prompts for better performance

    Features:
    - A/B testing of prompt variants
    - Performance tracking
    - Automatic optimization suggestions
    """

    def __init__(self):
        """Initialize prompt optimizer"""
        self.prompt_performance: Dict[str, List[float]] = {}

        logger.info("Prompt optimizer initialized")

    def track_performance(
        self,
        prompt_id: str,
        score: float
    ) -> None:
        """
        Track prompt performance

        Args:
            prompt_id: Prompt identifier
            score: Performance score
        """
        if prompt_id not in self.prompt_performance:
            self.prompt_performance[prompt_id] = []

        self.prompt_performance[prompt_id].append(score)

        logger.debug(f"Tracked performance for {prompt_id}: {score:.4f}")

    def compare_prompts(
        self,
        prompt_a_id: str,
        prompt_b_id: str
    ) -> Dict[str, Any]:
        """
        Compare two prompts

        Args:
            prompt_a_id: First prompt ID
            prompt_b_id: Second prompt ID

        Returns:
            Comparison result
        """
        scores_a = self.prompt_performance.get(prompt_a_id, [])
        scores_b = self.prompt_performance.get(prompt_b_id, [])

        if not scores_a or not scores_b:
            logger.warning("Insufficient data for comparison")
            return {
                'error': 'Insufficient data'
            }

        avg_a = sum(scores_a) / len(scores_a)
        avg_b = sum(scores_b) / len(scores_b)

        improvement = ((avg_b - avg_a) / avg_a * 100) if avg_a > 0 else 0

        return {
            'prompt_a': {
                'id': prompt_a_id,
                'avg_score': avg_a,
                'n_samples': len(scores_a)
            },
            'prompt_b': {
                'id': prompt_b_id,
                'avg_score': avg_b,
                'n_samples': len(scores_b)
            },
            'winner': prompt_a_id if avg_a > avg_b else prompt_b_id,
            'improvement_pct': abs(improvement),
            'statistically_significant': len(scores_a) >= 30 and len(scores_b) >= 30
        }

    def suggest_improvements(self, prompt: str) -> List[str]:
        """
        Suggest prompt improvements

        Args:
            prompt: Prompt to analyze

        Returns:
            List of suggestions
        """
        suggestions = []

        # Check for specificity
        if 'specific' not in prompt.lower() and 'detailed' not in prompt.lower():
            suggestions.append("Add 'specific' or 'detailed' to encourage precise responses")

        # Check for output format
        if 'format' not in prompt.lower() and 'structure' not in prompt.lower():
            suggestions.append("Specify the desired output format")

        # Check for constraints
        if 'must' not in prompt.lower() and 'should' not in prompt.lower():
            suggestions.append("Add explicit constraints or requirements")

        # Check for examples
        if 'example' not in prompt.lower():
            suggestions.append("Include examples to clarify expectations")

        # Check for role/persona
        if 'you are' not in prompt.lower() and 'act as' not in prompt.lower():
            suggestions.append("Consider defining a role or persona for the model")

        # Check for step-by-step
        if 'step' not in prompt.lower() and len(prompt.split()) > 50:
            suggestions.append("For complex tasks, request step-by-step reasoning")

        return suggestions

    def optimize_prompt_length(
        self,
        prompt: str,
        max_length: int = 500
    ) -> str:
        """
        Optimize prompt length

        Args:
            prompt: Original prompt
            max_length: Maximum character length

        Returns:
            Optimized prompt
        """
        if len(prompt) <= max_length:
            return prompt

        # Simple truncation with ellipsis
        # In practice, use more sophisticated summarization

        truncated = prompt[:max_length - 3] + "..."

        logger.info(f"Truncated prompt: {len(prompt)} -> {len(truncated)} characters")

        return truncated

    def get_best_prompt(self, min_samples: int = 10) -> Optional[str]:
        """
        Get best performing prompt

        Args:
            min_samples: Minimum samples required

        Returns:
            Best prompt ID or None
        """
        valid_prompts = {
            prompt_id: scores
            for prompt_id, scores in self.prompt_performance.items()
            if len(scores) >= min_samples
        }

        if not valid_prompts:
            return None

        best_prompt = max(
            valid_prompts.items(),
            key=lambda x: sum(x[1]) / len(x[1])
        )

        return best_prompt[0]

    def get_statistics(self) -> Dict[str, Any]:
        """Get optimization statistics"""
        total_prompts = len(self.prompt_performance)
        total_evaluations = sum(len(scores) for scores in self.prompt_performance.values())

        if self.prompt_performance:
            all_scores = [score for scores in self.prompt_performance.values() for score in scores]
            avg_score = sum(all_scores) / len(all_scores)
        else:
            avg_score = 0.0

        return {
            'total_prompts_tracked': total_prompts,
            'total_evaluations': total_evaluations,
            'avg_score': avg_score,
            'best_prompt': self.get_best_prompt(min_samples=5)
        }
