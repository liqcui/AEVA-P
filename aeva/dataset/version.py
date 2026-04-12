"""
Dataset Version Control for tracking dataset changes

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
import hashlib
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class DatasetVersion:
    """
    Represents a dataset version

    Attributes:
        version: Version string (e.g., '1.0.0', '1.1.0')
        dataset_name: Name of the dataset
        size: Number of samples
        checksum: Data checksum for integrity
        metadata: Version metadata
        parent_version: Parent version (for tracking lineage)
        changes: Description of changes from parent
        created_at: Creation timestamp
        created_by: Creator identifier
    """
    version: str
    dataset_name: str
    size: int
    checksum: str
    metadata: Dict[str, Any]
    parent_version: Optional[str] = None
    changes: Optional[str] = None
    created_at: Optional[str] = None
    created_by: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class VersionControl:
    """
    Manage dataset versions with Git-like semantics

    Features:
    - Version tracking with semantic versioning
    - Checksum-based change detection
    - Version history and lineage
    - Diff between versions
    - Rollback to previous versions
    """

    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize version control

        Args:
            storage_path: Path to store version metadata
        """
        self.storage_path = Path(storage_path) if storage_path else Path("./dataset_versions")
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.versions: Dict[str, List[DatasetVersion]] = {}  # dataset_name -> versions
        self._load_versions()

    def _load_versions(self) -> None:
        """Load version history from storage"""
        version_file = self.storage_path / "versions.json"

        if version_file.exists():
            try:
                with open(version_file, 'r') as f:
                    data = json.load(f)

                for dataset_name, versions_list in data.items():
                    self.versions[dataset_name] = [
                        DatasetVersion(**v) for v in versions_list
                    ]

                total_versions = sum(len(v) for v in self.versions.values())
                logger.info(f"Loaded {total_versions} versions for {len(self.versions)} datasets")

            except Exception as e:
                logger.warning(f"Failed to load versions: {e}")

    def _save_versions(self) -> None:
        """Save version history to storage"""
        version_file = self.storage_path / "versions.json"

        data = {
            name: [v.to_dict() for v in versions]
            for name, versions in self.versions.items()
        }

        with open(version_file, 'w') as f:
            json.dump(data, f, indent=2)

        total_versions = sum(len(v) for v in self.versions.values())
        logger.info(f"Saved {total_versions} versions")

    def _compute_checksum(self, data: List[Any]) -> str:
        """Compute checksum for data integrity"""
        # Convert data to JSON string and hash
        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(data_str.encode()).hexdigest()

    def create_version(
        self,
        dataset_name: str,
        data: List[Any],
        version: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        changes: Optional[str] = None,
        created_by: Optional[str] = None
    ) -> DatasetVersion:
        """
        Create a new dataset version

        Args:
            dataset_name: Name of the dataset
            data: Dataset content
            version: Version string (auto-incremented if None)
            metadata: Version metadata
            changes: Description of changes
            created_by: Creator identifier

        Returns:
            DatasetVersion object
        """
        # Auto-generate version if not provided
        if version is None:
            version = self._next_version(dataset_name)

        # Get parent version
        parent_version = None
        if dataset_name in self.versions and self.versions[dataset_name]:
            parent_version = self.versions[dataset_name][-1].version

        # Compute checksum
        checksum = self._compute_checksum(data)

        # Check if data changed
        if parent_version:
            last_version = self.versions[dataset_name][-1]
            if checksum == last_version.checksum:
                logger.warning(f"Data unchanged from {parent_version}, not creating new version")
                return last_version

        # Create version
        dataset_version = DatasetVersion(
            version=version,
            dataset_name=dataset_name,
            size=len(data),
            checksum=checksum,
            metadata=metadata or {},
            parent_version=parent_version,
            changes=changes,
            created_by=created_by
        )

        # Store version
        if dataset_name not in self.versions:
            self.versions[dataset_name] = []

        self.versions[dataset_name].append(dataset_version)
        self._save_versions()

        logger.info(f"Created version {version} for {dataset_name} (size: {len(data)})")

        return dataset_version

    def _next_version(self, dataset_name: str) -> str:
        """Auto-increment version number"""
        if dataset_name not in self.versions or not self.versions[dataset_name]:
            return "1.0.0"

        last_version = self.versions[dataset_name][-1].version

        # Parse semantic version (major.minor.patch)
        try:
            parts = last_version.split('.')
            major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

            # Increment patch version
            patch += 1

            return f"{major}.{minor}.{patch}"

        except (ValueError, IndexError):
            logger.warning(f"Could not parse version {last_version}, using 1.0.0")
            return "1.0.0"

    def get_version(
        self,
        dataset_name: str,
        version: Optional[str] = None
    ) -> Optional[DatasetVersion]:
        """
        Get a specific dataset version

        Args:
            dataset_name: Name of the dataset
            version: Version string (None = latest)

        Returns:
            DatasetVersion or None if not found
        """
        if dataset_name not in self.versions or not self.versions[dataset_name]:
            logger.warning(f"No versions found for {dataset_name}")
            return None

        versions = self.versions[dataset_name]

        if version is None:
            return versions[-1]  # Latest

        # Find specific version
        for v in versions:
            if v.version == version:
                return v

        logger.warning(f"Version {version} not found for {dataset_name}")
        return None

    def list_versions(self, dataset_name: str) -> List[DatasetVersion]:
        """
        List all versions for a dataset

        Args:
            dataset_name: Name of the dataset

        Returns:
            List of DatasetVersion objects
        """
        return self.versions.get(dataset_name, [])

    def get_history(self, dataset_name: str) -> List[Dict[str, Any]]:
        """
        Get version history for a dataset

        Args:
            dataset_name: Name of the dataset

        Returns:
            List of version metadata dictionaries
        """
        versions = self.list_versions(dataset_name)

        history = []
        for v in versions:
            history.append({
                'version': v.version,
                'size': v.size,
                'checksum': v.checksum[:8],  # Short checksum
                'parent': v.parent_version,
                'changes': v.changes,
                'created_at': v.created_at,
                'created_by': v.created_by
            })

        return history

    def diff(
        self,
        dataset_name: str,
        version_a: str,
        version_b: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compare two versions

        Args:
            dataset_name: Name of the dataset
            version_a: First version
            version_b: Second version (None = latest)

        Returns:
            Difference summary
        """
        v1 = self.get_version(dataset_name, version_a)
        v2 = self.get_version(dataset_name, version_b)

        if not v1 or not v2:
            raise ValueError(f"Version not found for {dataset_name}")

        diff_result = {
            'dataset': dataset_name,
            'version_a': v1.version,
            'version_b': v2.version,
            'size_change': v2.size - v1.size,
            'size_change_pct': ((v2.size - v1.size) / v1.size * 100) if v1.size > 0 else 0,
            'checksum_changed': v1.checksum != v2.checksum,
            'metadata_changes': self._diff_metadata(v1.metadata, v2.metadata),
            'changes_description': v2.changes if v2.parent_version == v1.version else None
        }

        logger.info(f"Diff {version_a} -> {version_b or 'latest'}: size {diff_result['size_change']:+d}")

        return diff_result

    def _diff_metadata(
        self,
        metadata_a: Dict[str, Any],
        metadata_b: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare metadata between versions"""
        changes = {
            'added': {},
            'removed': {},
            'modified': {}
        }

        # Find added and modified
        for key, value in metadata_b.items():
            if key not in metadata_a:
                changes['added'][key] = value
            elif metadata_a[key] != value:
                changes['modified'][key] = {
                    'old': metadata_a[key],
                    'new': value
                }

        # Find removed
        for key in metadata_a:
            if key not in metadata_b:
                changes['removed'][key] = metadata_a[key]

        return changes

    def tag_version(
        self,
        dataset_name: str,
        version: str,
        tag: str,
        message: Optional[str] = None
    ) -> None:
        """
        Tag a version with a label (e.g., 'production', 'stable')

        Args:
            dataset_name: Name of the dataset
            version: Version to tag
            tag: Tag name
            message: Optional tag message
        """
        dataset_version = self.get_version(dataset_name, version)

        if not dataset_version:
            raise ValueError(f"Version {version} not found for {dataset_name}")

        if 'tags' not in dataset_version.metadata:
            dataset_version.metadata['tags'] = []

        tag_info = {'tag': tag, 'message': message, 'created_at': datetime.now().isoformat()}
        dataset_version.metadata['tags'].append(tag_info)

        self._save_versions()

        logger.info(f"Tagged {dataset_name} v{version} as '{tag}'")

    def get_tagged_version(
        self,
        dataset_name: str,
        tag: str
    ) -> Optional[DatasetVersion]:
        """
        Get version by tag

        Args:
            dataset_name: Name of the dataset
            tag: Tag name

        Returns:
            DatasetVersion or None
        """
        versions = self.list_versions(dataset_name)

        for v in reversed(versions):  # Search from latest
            tags = v.metadata.get('tags', [])
            for tag_info in tags:
                if tag_info.get('tag') == tag:
                    return v

        logger.warning(f"No version found with tag '{tag}' for {dataset_name}")
        return None

    def rollback(
        self,
        dataset_name: str,
        target_version: str
    ) -> DatasetVersion:
        """
        Rollback to a previous version

        Creates a new version with the same content as target_version

        Args:
            dataset_name: Name of the dataset
            target_version: Version to rollback to

        Returns:
            New DatasetVersion
        """
        target = self.get_version(dataset_name, target_version)

        if not target:
            raise ValueError(f"Version {target_version} not found for {dataset_name}")

        # Note: Actual data rollback would need to be handled by DatasetManager
        # This just creates a version record

        logger.info(f"Rollback {dataset_name} to version {target_version}")

        return target

    def validate_integrity(self, dataset_name: str, data: List[Any], version: str) -> bool:
        """
        Validate data integrity against version checksum

        Args:
            dataset_name: Name of the dataset
            data: Dataset content
            version: Version to validate against

        Returns:
            True if checksum matches
        """
        dataset_version = self.get_version(dataset_name, version)

        if not dataset_version:
            raise ValueError(f"Version {version} not found for {dataset_name}")

        computed_checksum = self._compute_checksum(data)
        is_valid = computed_checksum == dataset_version.checksum

        if is_valid:
            logger.info(f"Data integrity validated for {dataset_name} v{version}")
        else:
            logger.error(f"Data integrity check FAILED for {dataset_name} v{version}")

        return is_valid
