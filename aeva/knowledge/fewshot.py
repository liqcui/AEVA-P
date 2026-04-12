"""
Few-shot Learning Support

Select and manage few-shot examples for model evaluation
"""

import logging
import random
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from collections import Counter

from aeva.knowledge.base import KnowledgeBase, KnowledgeEntry
from aeva.knowledge.retriever import KnowledgeRetriever

logger = logging.getLogger(__name__)


@dataclass
class FewShotExample:
    """Few-shot learning example"""
    input: Any
    output: Any
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'input': self.input,
            'output': self.output,
            'metadata': self.metadata
        }


class FewShotSelector:
    """
    Select few-shot examples from knowledge base

    Selection strategies:
    - Random selection
    - Diversity-based selection
    - Similarity-based selection
    - Performance-based selection
    """

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        retriever: Optional[KnowledgeRetriever] = None
    ):
        """
        Initialize few-shot selector

        Args:
            knowledge_base: KnowledgeBase instance
            retriever: Optional KnowledgeRetriever
        """
        self.kb = knowledge_base
        self.retriever = retriever or KnowledgeRetriever(knowledge_base)

    def select_random(
        self,
        n_examples: int,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        random_seed: int = 42
    ) -> List[FewShotExample]:
        """
        Random few-shot example selection

        Args:
            n_examples: Number of examples
            category: Optional category filter
            tags: Optional tag filter
            random_seed: Random seed

        Returns:
            List of FewShotExample
        """
        random.seed(random_seed)

        logger.info(f"Selecting {n_examples} random examples")

        # Get candidates
        candidates = list(self.kb.entries.values())

        if category:
            candidates = [e for e in candidates if e.category == category]

        if tags:
            candidates = [
                e for e in candidates
                if any(tag in e.tags for tag in tags)
            ]

        # Random sample
        n_examples = min(n_examples, len(candidates))
        selected_entries = random.sample(candidates, n_examples)

        # Convert to FewShotExample
        examples = []
        for entry in selected_entries:
            example = self._entry_to_example(entry)
            if example:
                examples.append(example)

        logger.info(f"Selected {len(examples)} random examples")

        return examples

    def select_diverse(
        self,
        n_examples: int,
        category: Optional[str] = None,
        diversity_key: str = 'label'
    ) -> List[FewShotExample]:
        """
        Select diverse examples (balanced across classes/types)

        Args:
            n_examples: Number of examples
            category: Optional category filter
            diversity_key: Key in content to use for diversity

        Returns:
            List of FewShotExample
        """
        logger.info(f"Selecting {n_examples} diverse examples")

        # Get candidates
        candidates = list(self.kb.entries.values())

        if category:
            candidates = [e for e in candidates if e.category == category]

        # Group by diversity key
        groups = {}
        for entry in candidates:
            if diversity_key in entry.content:
                group_value = entry.content[diversity_key]
                if group_value not in groups:
                    groups[group_value] = []
                groups[group_value].append(entry)

        if not groups:
            logger.warning(f"No entries with diversity key '{diversity_key}'")
            return self.select_random(n_examples, category=category)

        # Sample evenly from each group
        examples = []
        examples_per_group = max(1, n_examples // len(groups))

        for group_value, group_entries in groups.items():
            n_from_group = min(examples_per_group, len(group_entries))
            sampled = random.sample(group_entries, n_from_group)

            for entry in sampled:
                example = self._entry_to_example(entry)
                if example:
                    examples.append(example)

        # If we need more examples, add randomly
        if len(examples) < n_examples:
            remaining = n_examples - len(examples)
            all_entries = [e for group in groups.values() for e in group]
            used_ids = {e.metadata['entry_id'] for e in examples}

            available = [e for e in all_entries if e.entry_id not in used_ids]

            if available:
                additional = random.sample(available, min(remaining, len(available)))
                for entry in additional:
                    example = self._entry_to_example(entry)
                    if example:
                        examples.append(example)

        logger.info(f"Selected {len(examples)} diverse examples from {len(groups)} groups")

        return examples[:n_examples]

    def select_similar(
        self,
        query: str,
        n_examples: int,
        category: Optional[str] = None
    ) -> List[FewShotExample]:
        """
        Select examples similar to query

        Args:
            query: Query text
            n_examples: Number of examples
            category: Optional category filter

        Returns:
            List of FewShotExample
        """
        logger.info(f"Selecting {n_examples} similar examples for query: '{query}'")

        # Use retriever
        results = self.retriever.retrieve(
            query=query,
            top_k=n_examples,
            category=category
        )

        examples = []
        for result in results:
            example = self._entry_to_example(result.entry)
            if example:
                example.metadata['relevance_score'] = result.score
                examples.append(example)

        logger.info(f"Selected {len(examples)} similar examples")

        return examples

    def select_best_performing(
        self,
        n_examples: int,
        category: Optional[str] = None,
        min_usage: int = 1
    ) -> List[FewShotExample]:
        """
        Select best performing examples based on success rate

        Args:
            n_examples: Number of examples
            category: Optional category filter
            min_usage: Minimum usage count

        Returns:
            List of FewShotExample
        """
        logger.info(f"Selecting {n_examples} best performing examples")

        # Get candidates with sufficient usage
        candidates = [
            e for e in self.kb.entries.values()
            if e.usage_count >= min_usage
        ]

        if category:
            candidates = [e for e in candidates if e.category == category]

        # Sort by success rate
        candidates.sort(key=lambda e: e.success_rate, reverse=True)

        # Select top n
        selected = candidates[:n_examples]

        examples = []
        for entry in selected:
            example = self._entry_to_example(entry)
            if example:
                example.metadata['success_rate'] = entry.success_rate
                examples.append(example)

        logger.info(f"Selected {len(examples)} best performing examples")

        return examples

    def _entry_to_example(self, entry: KnowledgeEntry) -> Optional[FewShotExample]:
        """Convert knowledge entry to few-shot example"""
        # Extract input and output from content
        content = entry.content

        if 'input' not in content or 'output' not in content:
            logger.warning(f"Entry {entry.entry_id} missing input/output")
            return None

        return FewShotExample(
            input=content['input'],
            output=content['output'],
            metadata={
                'entry_id': entry.entry_id,
                'title': entry.title,
                'category': entry.category,
                'tags': entry.tags
            }
        )


class FewShotLearner:
    """
    Few-shot learning coordinator

    Features:
    - Example selection
    - Prompt construction
    - Performance tracking
    - Example optimization
    """

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        selector: Optional[FewShotSelector] = None
    ):
        """
        Initialize few-shot learner

        Args:
            knowledge_base: KnowledgeBase instance
            selector: Optional FewShotSelector
        """
        self.kb = knowledge_base
        self.selector = selector or FewShotSelector(knowledge_base)

    def create_few_shot_prompt(
        self,
        task_description: str,
        examples: List[FewShotExample],
        test_input: Any,
        format_fn: Optional[Callable] = None
    ) -> str:
        """
        Create few-shot prompt

        Args:
            task_description: Description of the task
            examples: Few-shot examples
            test_input: Test input to evaluate
            format_fn: Optional formatting function

        Returns:
            Formatted prompt
        """
        if format_fn:
            return format_fn(task_description, examples, test_input)

        # Default formatting
        prompt_parts = [task_description, ""]

        # Add examples
        for i, example in enumerate(examples, 1):
            prompt_parts.append(f"Example {i}:")
            prompt_parts.append(f"Input: {example.input}")
            prompt_parts.append(f"Output: {example.output}")
            prompt_parts.append("")

        # Add test input
        prompt_parts.append("Now, evaluate this:")
        prompt_parts.append(f"Input: {test_input}")
        prompt_parts.append("Output:")

        return "\n".join(prompt_parts)

    def evaluate_with_few_shot(
        self,
        test_input: Any,
        n_examples: int = 3,
        selection_strategy: str = 'similar',
        category: Optional[str] = None,
        query: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform few-shot evaluation

        Args:
            test_input: Input to evaluate
            n_examples: Number of examples
            selection_strategy: 'random', 'diverse', 'similar', 'best'
            category: Optional category filter
            query: Query for similarity-based selection

        Returns:
            Evaluation result with prompt and examples
        """
        logger.info(f"Few-shot evaluation with {n_examples} examples ({selection_strategy})")

        # Select examples
        if selection_strategy == 'random':
            examples = self.selector.select_random(n_examples, category=category)
        elif selection_strategy == 'diverse':
            examples = self.selector.select_diverse(n_examples, category=category)
        elif selection_strategy == 'similar':
            query_text = query or str(test_input)
            examples = self.selector.select_similar(query_text, n_examples, category=category)
        elif selection_strategy == 'best':
            examples = self.selector.select_best_performing(n_examples, category=category)
        else:
            raise ValueError(f"Unknown selection strategy: {selection_strategy}")

        # Create prompt
        task_description = "Evaluate the following input based on the examples:"

        prompt = self.create_few_shot_prompt(
            task_description=task_description,
            examples=examples,
            test_input=test_input
        )

        return {
            'prompt': prompt,
            'examples': [ex.to_dict() for ex in examples],
            'n_examples': len(examples),
            'selection_strategy': selection_strategy
        }

    def optimize_n_examples(
        self,
        test_cases: List[Dict[str, Any]],
        max_examples: int = 10,
        metric_fn: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Find optimal number of few-shot examples

        Args:
            test_cases: List of test cases with 'input' and 'expected_output'
            max_examples: Maximum number of examples to try
            metric_fn: Function to compute performance metric

        Returns:
            Optimization result
        """
        logger.info(f"Optimizing n_examples (max: {max_examples})")

        results = []

        for n in range(1, max_examples + 1):
            # Evaluate with n examples
            scores = []

            for test_case in test_cases:
                eval_result = self.evaluate_with_few_shot(
                    test_input=test_case['input'],
                    n_examples=n,
                    selection_strategy='similar'
                )

                # Compute score (simplified - in practice, run model and evaluate)
                if metric_fn:
                    score = metric_fn(eval_result, test_case['expected_output'])
                else:
                    score = 1.0  # Placeholder

                scores.append(score)

            avg_score = sum(scores) / len(scores) if scores else 0

            results.append({
                'n_examples': n,
                'avg_score': avg_score
            })

            logger.info(f"  n={n}: avg_score={avg_score:.4f}")

        # Find best n
        best = max(results, key=lambda x: x['avg_score'])

        logger.info(f"Optimal n_examples: {best['n_examples']} (score: {best['avg_score']:.4f})")

        return {
            'optimal_n': best['n_examples'],
            'optimal_score': best['avg_score'],
            'all_results': results
        }

    def track_example_performance(
        self,
        entry_id: str,
        success: bool
    ) -> None:
        """
        Track performance of a used example

        Args:
            entry_id: Entry ID
            success: Whether usage was successful
        """
        self.kb.record_usage(entry_id, success)

        logger.debug(f"Tracked example performance: {entry_id} (success={success})")
