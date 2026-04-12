"""
Dataset Manager for AEVA evaluation datasets

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class Dataset:
    """
    Represents an evaluation dataset

    Attributes:
        name: Dataset name
        version: Dataset version
        data: Actual dataset content
        metadata: Dataset metadata
        created_at: Creation timestamp
    """

    def __init__(
        self,
        name: str,
        data: List[Any],
        version: str = "1.0.0",
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.name = name
        self.version = version
        self.data = data
        self.metadata = metadata or {}
        self.created_at = datetime.now()

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'version': self.version,
            'size': len(self.data),
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat()
        }


class DatasetManager:
    """
    Manage evaluation datasets

    Features:
    - Dataset registration and loading
    - Version control
    - Quality analysis integration
    - Splitting and sampling
    """

    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize dataset manager

        Args:
            storage_path: Path to store datasets
        """
        self.storage_path = Path(storage_path) if storage_path else Path("./datasets")
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.datasets: Dict[str, Dataset] = {}
        self._load_registry()

    def _load_registry(self) -> None:
        """Load dataset registry from storage"""
        registry_path = self.storage_path / "registry.json"

        if registry_path.exists():
            try:
                with open(registry_path, 'r') as f:
                    registry = json.load(f)
                    logger.info(f"Loaded registry with {len(registry)} datasets")
            except Exception as e:
                logger.warning(f"Failed to load registry: {e}")

    def _save_registry(self) -> None:
        """Save dataset registry to storage"""
        registry_path = self.storage_path / "registry.json"

        registry = {
            name: dataset.to_dict()
            for name, dataset in self.datasets.items()
        }

        with open(registry_path, 'w') as f:
            json.dump(registry, f, indent=2)

        logger.info(f"Saved registry with {len(registry)} datasets")

    def register_dataset(
        self,
        name: str,
        data: List[Any],
        version: str = "1.0.0",
        metadata: Optional[Dict[str, Any]] = None,
        save: bool = True
    ) -> Dataset:
        """
        Register a new dataset

        Args:
            name: Dataset name
            data: Dataset content
            version: Version string
            metadata: Additional metadata
            save: Whether to save to disk

        Returns:
            Dataset object
        """
        logger.info(f"Registering dataset: {name} v{version} ({len(data)} samples)")

        dataset = Dataset(
            name=name,
            data=data,
            version=version,
            metadata=metadata
        )

        self.datasets[name] = dataset

        if save:
            self._save_dataset(dataset)
            self._save_registry()

        return dataset

    def _save_dataset(self, dataset: Dataset) -> None:
        """Save dataset to disk"""
        dataset_path = self.storage_path / f"{dataset.name}_v{dataset.version}.json"

        data_to_save = {
            'name': dataset.name,
            'version': dataset.version,
            'data': dataset.data,
            'metadata': dataset.metadata,
            'created_at': dataset.created_at.isoformat()
        }

        with open(dataset_path, 'w') as f:
            json.dump(data_to_save, f, indent=2)

        logger.info(f"Dataset saved to {dataset_path}")

    def load_dataset(self, name: str, version: Optional[str] = None) -> Dataset:
        """
        Load dataset from registry or disk

        Args:
            name: Dataset name
            version: Specific version (None = latest)

        Returns:
            Dataset object
        """
        # Check if already loaded
        if name in self.datasets:
            return self.datasets[name]

        # Load from disk
        if version:
            dataset_path = self.storage_path / f"{name}_v{version}.json"
        else:
            # Find latest version
            dataset_files = list(self.storage_path.glob(f"{name}_v*.json"))
            if not dataset_files:
                raise ValueError(f"Dataset {name} not found")
            dataset_path = sorted(dataset_files)[-1]

        with open(dataset_path, 'r') as f:
            data_dict = json.load(f)

        dataset = Dataset(
            name=data_dict['name'],
            data=data_dict['data'],
            version=data_dict['version'],
            metadata=data_dict.get('metadata', {})
        )

        self.datasets[name] = dataset
        logger.info(f"Loaded dataset: {name} v{dataset.version}")

        return dataset

    def list_datasets(self) -> List[Dict[str, Any]]:
        """List all registered datasets"""
        return [dataset.to_dict() for dataset in self.datasets.values()]

    def get_dataset_info(self, name: str) -> Dict[str, Any]:
        """Get dataset information"""
        if name not in self.datasets:
            raise ValueError(f"Dataset {name} not found")

        dataset = self.datasets[name]
        return {
            'name': dataset.name,
            'version': dataset.version,
            'size': len(dataset),
            'metadata': dataset.metadata,
            'created_at': dataset.created_at.isoformat()
        }

    def split_dataset(
        self,
        name: str,
        splits: Dict[str, float],
        stratify: bool = False,
        random_seed: int = 42
    ) -> Dict[str, Dataset]:
        """
        Split dataset into train/val/test

        Args:
            name: Dataset name
            splits: Dictionary of split names and ratios (e.g., {'train': 0.7, 'val': 0.15, 'test': 0.15})
            stratify: Whether to stratify split (for classification)
            random_seed: Random seed for reproducibility

        Returns:
            Dictionary of split datasets
        """
        from aeva.dataset.splitter import DatasetSplitter

        dataset = self.datasets[name]
        splitter = DatasetSplitter(random_seed=random_seed)

        split_data = splitter.split(
            data=dataset.data,
            splits=splits,
            stratify=stratify
        )

        # Create dataset objects for each split
        split_datasets = {}
        for split_name, data in split_data.items():
            split_dataset = Dataset(
                name=f"{name}_{split_name}",
                data=data,
                version=dataset.version,
                metadata={
                    **dataset.metadata,
                    'split': split_name,
                    'parent_dataset': name
                }
            )
            split_datasets[split_name] = split_dataset
            self.datasets[split_dataset.name] = split_dataset

        logger.info(f"Split dataset {name} into {list(split_datasets.keys())}")

        return split_datasets

    def sample_dataset(
        self,
        name: str,
        n_samples: int,
        strategy: str = 'random',
        random_seed: int = 42
    ) -> Dataset:
        """
        Sample from dataset

        Args:
            name: Dataset name
            n_samples: Number of samples
            strategy: Sampling strategy ('random', 'stratified')
            random_seed: Random seed

        Returns:
            Sampled dataset
        """
        from aeva.dataset.sampler import DatasetSampler

        dataset = self.datasets[name]
        sampler = DatasetSampler(random_seed=random_seed)

        sampled_data = sampler.sample(
            data=dataset.data,
            n_samples=n_samples,
            strategy=strategy
        )

        sampled_dataset = Dataset(
            name=f"{name}_sampled_{n_samples}",
            data=sampled_data,
            version=dataset.version,
            metadata={
                **dataset.metadata,
                'sampled_from': name,
                'sample_size': n_samples,
                'sample_strategy': strategy
            }
        )

        self.datasets[sampled_dataset.name] = sampled_dataset
        logger.info(f"Sampled {n_samples} from {name}")

        return sampled_dataset

    def analyze_quality(self, name: str) -> Dict[str, Any]:
        """
        Analyze dataset quality

        Args:
            name: Dataset name

        Returns:
            Quality analysis results
        """
        from aeva.dataset.quality import DataQualityAnalyzer

        dataset = self.datasets[name]
        analyzer = DataQualityAnalyzer()

        quality_report = analyzer.analyze(dataset.data)

        logger.info(f"Quality analysis completed for {name}")

        return quality_report
