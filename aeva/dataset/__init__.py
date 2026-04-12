"""
AEVA Dataset Management Module

Provides dataset versioning, quality analysis, and augmentation capabilities.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
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
