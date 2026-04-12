"""
Dataset Sampler for random and stratified sampling

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
import random
from typing import List, Any, Optional
from collections import Counter

logger = logging.getLogger(__name__)


class DatasetSampler:
    """
    Sample from datasets using various strategies

    Features:
    - Random sampling
    - Stratified sampling (maintains class distribution)
    - Balanced sampling (equal samples per class)
    - Weighted sampling
    - Reproducible sampling with random seed
    """

    def __init__(self, random_seed: int = 42):
        """
        Initialize dataset sampler

        Args:
            random_seed: Random seed for reproducibility
        """
        self.random_seed = random_seed
        random.seed(random_seed)

    def sample(
        self,
        data: List[Any],
        n_samples: int,
        strategy: str = 'random',
        stratify_key: str = 'label',
        replace: bool = False
    ) -> List[Any]:
        """
        Sample from dataset

        Args:
            data: Dataset to sample from
            n_samples: Number of samples to draw
            strategy: Sampling strategy ('random', 'stratified', 'balanced')
            stratify_key: Key for stratification (default: 'label')
            replace: Whether to sample with replacement

        Returns:
            Sampled dataset

        Raises:
            ValueError: If invalid strategy or n_samples > len(data) without replacement
        """
        if not data:
            raise ValueError("Cannot sample from empty dataset")

        if not replace and n_samples > len(data):
            raise ValueError(f"Cannot sample {n_samples} from {len(data)} without replacement")

        logger.info(f"Sampling {n_samples} from {len(data)} using strategy: {strategy}")

        if strategy == 'random':
            return self._random_sample(data, n_samples, replace)
        elif strategy == 'stratified':
            return self._stratified_sample(data, n_samples, stratify_key, replace)
        elif strategy == 'balanced':
            return self._balanced_sample(data, n_samples, stratify_key)
        else:
            raise ValueError(f"Unknown sampling strategy: {strategy}")

    def _random_sample(
        self,
        data: List[Any],
        n_samples: int,
        replace: bool
    ) -> List[Any]:
        """Perform random sampling"""
        if replace:
            sampled = random.choices(data, k=n_samples)
        else:
            sampled = random.sample(data, k=n_samples)

        logger.info(f"Random sampled {len(sampled)} samples")
        return sampled

    def _stratified_sample(
        self,
        data: List[Any],
        n_samples: int,
        stratify_key: str,
        replace: bool
    ) -> List[Any]:
        """
        Perform stratified sampling (maintains class distribution)

        Samples proportionally from each class
        """
        # Extract labels
        if isinstance(data[0], dict) and stratify_key in data[0]:
            labels = [sample[stratify_key] for sample in data]
        else:
            logger.warning(f"Stratify key '{stratify_key}' not found, falling back to random sampling")
            return self._random_sample(data, n_samples, replace)

        # Group by label
        label_groups = {}
        for sample, label in zip(data, labels):
            if label not in label_groups:
                label_groups[label] = []
            label_groups[label].append(sample)

        # Calculate samples per class
        label_counts = Counter(labels)
        total_count = len(labels)

        sampled = []
        remaining_samples = n_samples

        # Sort labels to ensure reproducibility
        sorted_labels = sorted(label_groups.keys(), key=str)

        for i, label in enumerate(sorted_labels):
            # Calculate proportion
            proportion = label_counts[label] / total_count

            if i == len(sorted_labels) - 1:
                # Last class gets remaining samples
                class_samples = remaining_samples
            else:
                class_samples = int(n_samples * proportion)

            # Sample from this class
            group = label_groups[label]

            if replace:
                class_sampled = random.choices(group, k=class_samples)
            else:
                # Handle case where we need more samples than available
                class_samples = min(class_samples, len(group))
                class_sampled = random.sample(group, k=class_samples)

            sampled.extend(class_sampled)
            remaining_samples -= len(class_sampled)

            logger.info(f"  {label}: {len(class_sampled)} samples ({proportion*100:.1f}%)")

        # Shuffle to mix classes
        random.shuffle(sampled)

        logger.info(f"Stratified sampled {len(sampled)} samples across {len(label_groups)} classes")
        return sampled

    def _balanced_sample(
        self,
        data: List[Any],
        n_samples: int,
        stratify_key: str
    ) -> List[Any]:
        """
        Perform balanced sampling (equal samples per class)

        Useful for handling imbalanced datasets
        """
        # Extract labels
        if isinstance(data[0], dict) and stratify_key in data[0]:
            labels = [sample[stratify_key] for sample in data]
        else:
            logger.warning(f"Stratify key '{stratify_key}' not found, falling back to random sampling")
            return self._random_sample(data, n_samples, replace=True)

        # Group by label
        label_groups = {}
        for sample, label in zip(data, labels):
            if label not in label_groups:
                label_groups[label] = []
            label_groups[label].append(sample)

        num_classes = len(label_groups)
        samples_per_class = n_samples // num_classes

        sampled = []

        for label, group in sorted(label_groups.items(), key=lambda x: str(x[0])):
            # Sample with replacement if needed
            if samples_per_class > len(group):
                logger.info(f"  {label}: sampling {samples_per_class} with replacement from {len(group)}")
                class_sampled = random.choices(group, k=samples_per_class)
            else:
                class_sampled = random.sample(group, k=samples_per_class)

            sampled.extend(class_sampled)
            logger.info(f"  {label}: {len(class_sampled)} samples")

        # Add remaining samples if needed
        remaining = n_samples - len(sampled)
        if remaining > 0:
            all_data = [item for group in label_groups.values() for item in group]
            sampled.extend(random.sample(all_data, k=remaining))
            logger.info(f"  Added {remaining} additional samples")

        # Shuffle to mix classes
        random.shuffle(sampled)

        logger.info(f"Balanced sampled {len(sampled)} samples ({samples_per_class} per class)")
        return sampled

    def weighted_sample(
        self,
        data: List[Any],
        n_samples: int,
        weights: List[float],
        replace: bool = True
    ) -> List[Any]:
        """
        Perform weighted sampling

        Args:
            data: Dataset to sample from
            n_samples: Number of samples
            weights: Weight for each sample
            replace: Whether to sample with replacement

        Returns:
            Sampled dataset
        """
        if len(weights) != len(data):
            raise ValueError(f"Length of weights ({len(weights)}) must match data ({len(data)})")

        logger.info(f"Weighted sampling {n_samples} samples")

        if replace:
            sampled = random.choices(data, weights=weights, k=n_samples)
        else:
            # For sampling without replacement with weights, use custom logic
            sampled = []
            available_indices = list(range(len(data)))
            available_weights = weights.copy()

            for _ in range(n_samples):
                # Normalize weights
                total_weight = sum(available_weights)
                probabilities = [w / total_weight for w in available_weights]

                # Sample one index
                idx = random.choices(available_indices, weights=probabilities, k=1)[0]
                sampled.append(data[idx])

                # Remove from available
                pos = available_indices.index(idx)
                available_indices.pop(pos)
                available_weights.pop(pos)

        logger.info(f"Weighted sampled {len(sampled)} samples")
        return sampled

    def bootstrap_sample(
        self,
        data: List[Any],
        n_bootstraps: int = 100,
        sample_size: Optional[int] = None
    ) -> List[List[Any]]:
        """
        Generate bootstrap samples

        Args:
            data: Dataset to sample from
            n_bootstraps: Number of bootstrap samples to generate
            sample_size: Size of each bootstrap sample (default: len(data))

        Returns:
            List of bootstrap samples
        """
        if sample_size is None:
            sample_size = len(data)

        logger.info(f"Generating {n_bootstraps} bootstrap samples of size {sample_size}")

        bootstraps = []
        for i in range(n_bootstraps):
            bootstrap = random.choices(data, k=sample_size)
            bootstraps.append(bootstrap)

        logger.info(f"Generated {len(bootstraps)} bootstrap samples")
        return bootstraps

    def reservoir_sample(
        self,
        data_stream,
        n_samples: int
    ) -> List[Any]:
        """
        Reservoir sampling for streaming data

        Efficiently samples from a data stream of unknown size

        Args:
            data_stream: Iterator/generator of data
            n_samples: Number of samples to keep

        Returns:
            Sampled dataset
        """
        logger.info(f"Reservoir sampling {n_samples} samples from stream")

        reservoir = []

        for i, item in enumerate(data_stream):
            if i < n_samples:
                reservoir.append(item)
            else:
                # Randomly replace elements with decreasing probability
                j = random.randint(0, i)
                if j < n_samples:
                    reservoir[j] = item

        logger.info(f"Reservoir sampled {len(reservoir)} samples from {i+1} total items")
        return reservoir

    def time_based_sample(
        self,
        data: List[Any],
        n_samples: int,
        time_key: str = 'timestamp',
        strategy: str = 'uniform'
    ) -> List[Any]:
        """
        Sample based on time distribution

        Args:
            data: Dataset to sample from
            n_samples: Number of samples
            time_key: Key for timestamp
            strategy: 'uniform' (evenly spaced) or 'recent' (bias toward recent)

        Returns:
            Sampled dataset
        """
        if not isinstance(data[0], dict) or time_key not in data[0]:
            logger.warning(f"Time key '{time_key}' not found, falling back to random sampling")
            return self._random_sample(data, n_samples, replace=False)

        # Sort by time
        sorted_data = sorted(data, key=lambda x: x[time_key])

        if strategy == 'uniform':
            # Sample evenly across time range
            indices = [int(i * len(sorted_data) / n_samples) for i in range(n_samples)]
            sampled = [sorted_data[idx] for idx in indices]
            logger.info(f"Uniformly sampled {len(sampled)} across time range")

        elif strategy == 'recent':
            # Bias toward recent data (exponential decay)
            weights = [2 ** i for i in range(len(sorted_data))]
            sampled = self.weighted_sample(sorted_data, n_samples, weights, replace=False)
            logger.info(f"Recent-biased sampled {len(sampled)} samples")

        else:
            raise ValueError(f"Unknown time-based strategy: {strategy}")

        return sampled
