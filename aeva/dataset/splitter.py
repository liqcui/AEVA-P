"""
Dataset Splitter for train/val/test splits

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
import random
from typing import Dict, List, Any, Optional
from collections import Counter

logger = logging.getLogger(__name__)


class DatasetSplitter:
    """
    Split datasets into train/validation/test sets

    Features:
    - Random splitting
    - Stratified splitting (for classification)
    - Reproducible splits with random seed
    - Validation of split ratios
    """

    def __init__(self, random_seed: int = 42):
        """
        Initialize dataset splitter

        Args:
            random_seed: Random seed for reproducibility
        """
        self.random_seed = random_seed
        random.seed(random_seed)

    def split(
        self,
        data: List[Any],
        splits: Dict[str, float],
        stratify: bool = False,
        stratify_key: str = 'label'
    ) -> Dict[str, List[Any]]:
        """
        Split dataset into multiple sets

        Args:
            data: Dataset to split
            splits: Dictionary of split names and ratios (e.g., {'train': 0.7, 'val': 0.15, 'test': 0.15})
            stratify: Whether to stratify split (maintains class distribution)
            stratify_key: Key to use for stratification (default: 'label')

        Returns:
            Dictionary of split names to data lists

        Raises:
            ValueError: If split ratios don't sum to 1.0 or data is empty
        """
        if not data:
            raise ValueError("Cannot split empty dataset")

        # Validate split ratios
        total_ratio = sum(splits.values())
        if not (0.99 <= total_ratio <= 1.01):  # Allow small floating point errors
            raise ValueError(f"Split ratios must sum to 1.0, got {total_ratio}")

        logger.info(f"Splitting {len(data)} samples into {list(splits.keys())}")

        if stratify:
            return self._stratified_split(data, splits, stratify_key)
        else:
            return self._random_split(data, splits)

    def _random_split(
        self,
        data: List[Any],
        splits: Dict[str, float]
    ) -> Dict[str, List[Any]]:
        """Perform random split"""
        # Shuffle data
        shuffled_data = data.copy()
        random.shuffle(shuffled_data)

        # Calculate split sizes
        total_size = len(data)
        split_data = {}
        current_idx = 0

        split_names = list(splits.keys())
        for i, split_name in enumerate(split_names):
            if i == len(split_names) - 1:
                # Last split gets remaining data
                split_size = total_size - current_idx
            else:
                split_size = int(total_size * splits[split_name])

            split_data[split_name] = shuffled_data[current_idx:current_idx + split_size]
            current_idx += split_size

            logger.info(f"  {split_name}: {len(split_data[split_name])} samples ({splits[split_name]*100:.1f}%)")

        return split_data

    def _stratified_split(
        self,
        data: List[Any],
        splits: Dict[str, float],
        stratify_key: str
    ) -> Dict[str, List[Any]]:
        """Perform stratified split maintaining class distribution"""
        # Extract labels
        if isinstance(data[0], dict):
            if stratify_key not in data[0]:
                logger.warning(f"Stratify key '{stratify_key}' not found, falling back to random split")
                return self._random_split(data, splits)

            labels = [sample[stratify_key] for sample in data]
        else:
            logger.warning("Data is not dict format, falling back to random split")
            return self._random_split(data, splits)

        # Group data by label
        label_groups = {}
        for sample, label in zip(data, labels):
            if label not in label_groups:
                label_groups[label] = []
            label_groups[label].append(sample)

        # Shuffle each group
        for label in label_groups:
            random.shuffle(label_groups[label])

        logger.info(f"Stratifying across {len(label_groups)} classes")

        # Split each group according to ratios
        split_data = {name: [] for name in splits.keys()}

        for label, group in label_groups.items():
            group_size = len(group)
            current_idx = 0

            split_names = list(splits.keys())
            for i, split_name in enumerate(split_names):
                if i == len(split_names) - 1:
                    # Last split gets remaining data
                    split_size = group_size - current_idx
                else:
                    split_size = int(group_size * splits[split_name])

                split_data[split_name].extend(group[current_idx:current_idx + split_size])
                current_idx += split_size

        # Shuffle each split
        for split_name in split_data:
            random.shuffle(split_data[split_name])
            logger.info(f"  {split_name}: {len(split_data[split_name])} samples ({splits[split_name]*100:.1f}%)")

        # Verify stratification
        self._verify_stratification(split_data, stratify_key)

        return split_data

    def _verify_stratification(
        self,
        split_data: Dict[str, List[Any]],
        stratify_key: str
    ) -> None:
        """Verify that class distributions are maintained"""
        logger.info("Verifying stratification:")

        for split_name, data in split_data.items():
            if not data:
                continue

            labels = [sample[stratify_key] for sample in data if isinstance(sample, dict)]
            if labels:
                distribution = Counter(labels)
                total = len(labels)

                logger.info(f"  {split_name} class distribution:")
                for label, count in distribution.most_common():
                    percentage = (count / total) * 100
                    logger.info(f"    {label}: {count} ({percentage:.1f}%)")

    def k_fold_split(
        self,
        data: List[Any],
        k: int = 5,
        stratify: bool = False,
        stratify_key: str = 'label'
    ) -> List[Dict[str, List[Any]]]:
        """
        Perform k-fold cross-validation split

        Args:
            data: Dataset to split
            k: Number of folds
            stratify: Whether to stratify folds
            stratify_key: Key to use for stratification

        Returns:
            List of k dictionaries with 'train' and 'val' splits
        """
        if k < 2:
            raise ValueError("k must be at least 2")

        logger.info(f"Performing {k}-fold split on {len(data)} samples")

        if stratify:
            return self._stratified_k_fold(data, k, stratify_key)
        else:
            return self._random_k_fold(data, k)

    def _random_k_fold(self, data: List[Any], k: int) -> List[Dict[str, List[Any]]]:
        """Perform random k-fold split"""
        # Shuffle data
        shuffled_data = data.copy()
        random.shuffle(shuffled_data)

        # Calculate fold size
        fold_size = len(data) // k
        folds = []

        for i in range(k):
            # Validation set for this fold
            val_start = i * fold_size
            val_end = (i + 1) * fold_size if i < k - 1 else len(data)
            val_data = shuffled_data[val_start:val_end]

            # Training set is everything else
            train_data = shuffled_data[:val_start] + shuffled_data[val_end:]

            folds.append({
                'train': train_data,
                'val': val_data
            })

            logger.info(f"  Fold {i+1}: train={len(train_data)}, val={len(val_data)}")

        return folds

    def _stratified_k_fold(
        self,
        data: List[Any],
        k: int,
        stratify_key: str
    ) -> List[Dict[str, List[Any]]]:
        """Perform stratified k-fold split"""
        # Extract labels
        if isinstance(data[0], dict) and stratify_key in data[0]:
            labels = [sample[stratify_key] for sample in data]
        else:
            logger.warning(f"Stratify key '{stratify_key}' not found, falling back to random k-fold")
            return self._random_k_fold(data, k)

        # Group by label
        label_groups = {}
        for sample, label in zip(data, labels):
            if label not in label_groups:
                label_groups[label] = []
            label_groups[label].append(sample)

        # Shuffle each group
        for label in label_groups:
            random.shuffle(label_groups[label])

        # Create folds
        folds = [{'train': [], 'val': []} for _ in range(k)]

        # Distribute each class across folds
        for label, group in label_groups.items():
            fold_size = len(group) // k

            for i in range(k):
                val_start = i * fold_size
                val_end = (i + 1) * fold_size if i < k - 1 else len(group)

                # Add to validation set for fold i
                folds[i]['val'].extend(group[val_start:val_end])

                # Add to training set for all other folds
                for j in range(k):
                    if j != i:
                        folds[j]['train'].extend(group[val_start:val_end])

        # Shuffle each fold
        for i, fold in enumerate(folds):
            random.shuffle(fold['train'])
            random.shuffle(fold['val'])
            logger.info(f"  Fold {i+1}: train={len(fold['train'])}, val={len(fold['val'])}")

        return folds

    def temporal_split(
        self,
        data: List[Any],
        splits: Dict[str, float],
        time_key: str = 'timestamp'
    ) -> Dict[str, List[Any]]:
        """
        Perform temporal split (no shuffling, maintains time order)

        Useful for time-series data where temporal order matters

        Args:
            data: Dataset to split
            splits: Dictionary of split names and ratios
            time_key: Key to use for sorting (if data is dict)

        Returns:
            Dictionary of split names to data lists
        """
        logger.info(f"Performing temporal split on {len(data)} samples")

        # Sort by time if possible
        if isinstance(data[0], dict) and time_key in data[0]:
            sorted_data = sorted(data, key=lambda x: x[time_key])
            logger.info(f"Sorted by {time_key}")
        else:
            sorted_data = data
            logger.info("No sorting applied (data not dict or time key missing)")

        # Calculate split sizes
        total_size = len(data)
        split_data = {}
        current_idx = 0

        split_names = list(splits.keys())
        for i, split_name in enumerate(split_names):
            if i == len(split_names) - 1:
                split_size = total_size - current_idx
            else:
                split_size = int(total_size * splits[split_name])

            split_data[split_name] = sorted_data[current_idx:current_idx + split_size]
            current_idx += split_size

            logger.info(f"  {split_name}: {len(split_data[split_name])} samples ({splits[split_name]*100:.1f}%)")

        return split_data
