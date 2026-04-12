"""
AEVA Dataset Management Module

Provides dataset versioning, quality analysis, and augmentation capabilities.
"""

from aeva.dataset.manager import DatasetManager
from aeva.dataset.version import DatasetVersion, VersionControl
from aeva.dataset.quality import DataQualityAnalyzer
from aeva.dataset.splitter import DatasetSplitter
from aeva.dataset.sampler import DatasetSampler

__all__ = [
    'DatasetManager',
    'DatasetVersion',
    'VersionControl',
    'DataQualityAnalyzer',
    'DatasetSplitter',
    'DatasetSampler',
]
