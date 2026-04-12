"""
Knowledge Base Management

Store and manage evaluation knowledge, test cases, and examples
"""

import logging
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class KnowledgeEntry:
    """
    Single knowledge base entry

    Represents a test case, example, or evaluation pattern
    """
    entry_id: str
    category: str  # 'test_case', 'example', 'pattern', 'best_practice'
    title: str
    content: Dict[str, Any]
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    usage_count: int = 0
    success_rate: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KnowledgeEntry':
        """Create from dictionary"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return cls(**data)


class KnowledgeBase:
    """
    Knowledge base for storing evaluation knowledge

    Features:
    - Entry management (CRUD)
    - Category organization
    - Tag-based search
    - Usage tracking
    - Export/import
    """

    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize knowledge base

        Args:
            storage_path: Path to store knowledge base
        """
        self.storage_path = Path(storage_path) if storage_path else Path("./knowledge_base")
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.entries: Dict[str, KnowledgeEntry] = {}
        self.category_index: Dict[str, List[str]] = defaultdict(list)
        self.tag_index: Dict[str, List[str]] = defaultdict(list)

        self._load_knowledge_base()

        logger.info(f"Knowledge base initialized at {self.storage_path}")

    def _load_knowledge_base(self) -> None:
        """Load knowledge base from storage"""
        kb_file = self.storage_path / "knowledge_base.json"

        if kb_file.exists():
            try:
                with open(kb_file, 'r') as f:
                    data = json.load(f)

                for entry_data in data.get('entries', []):
                    entry = KnowledgeEntry.from_dict(entry_data)
                    self.entries[entry.entry_id] = entry

                    # Rebuild indices
                    self.category_index[entry.category].append(entry.entry_id)
                    for tag in entry.tags:
                        self.tag_index[tag].append(entry.entry_id)

                logger.info(f"Loaded {len(self.entries)} knowledge entries")

            except Exception as e:
                logger.error(f"Failed to load knowledge base: {e}")

    def _save_knowledge_base(self) -> None:
        """Save knowledge base to storage"""
        kb_file = self.storage_path / "knowledge_base.json"

        data = {
            'entries': [entry.to_dict() for entry in self.entries.values()],
            'metadata': {
                'total_entries': len(self.entries),
                'last_updated': datetime.now().isoformat()
            }
        }

        with open(kb_file, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved {len(self.entries)} knowledge entries")

    def add_entry(
        self,
        entry_id: str,
        category: str,
        title: str,
        content: Dict[str, Any],
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> KnowledgeEntry:
        """
        Add a new knowledge entry

        Args:
            entry_id: Unique entry ID
            category: Entry category
            title: Entry title
            content: Entry content
            tags: Optional tags
            metadata: Optional metadata

        Returns:
            KnowledgeEntry
        """
        entry = KnowledgeEntry(
            entry_id=entry_id,
            category=category,
            title=title,
            content=content,
            tags=tags or [],
            metadata=metadata or {}
        )

        self.entries[entry_id] = entry

        # Update indices
        self.category_index[category].append(entry_id)
        for tag in entry.tags:
            self.tag_index[tag].append(entry_id)

        self._save_knowledge_base()

        logger.info(f"Added knowledge entry: {entry_id} ({category})")

        return entry

    def get_entry(self, entry_id: str) -> Optional[KnowledgeEntry]:
        """Get entry by ID"""
        return self.entries.get(entry_id)

    def update_entry(
        self,
        entry_id: str,
        content: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[KnowledgeEntry]:
        """
        Update an existing entry

        Args:
            entry_id: Entry ID
            content: Updated content
            tags: Updated tags
            metadata: Updated metadata

        Returns:
            Updated KnowledgeEntry or None
        """
        entry = self.entries.get(entry_id)

        if not entry:
            logger.warning(f"Entry not found: {entry_id}")
            return None

        # Remove from old tag indices
        for tag in entry.tags:
            if entry_id in self.tag_index[tag]:
                self.tag_index[tag].remove(entry_id)

        # Update entry
        if content is not None:
            entry.content = content

        if tags is not None:
            entry.tags = tags
            # Add to new tag indices
            for tag in tags:
                self.tag_index[tag].append(entry_id)

        if metadata is not None:
            entry.metadata.update(metadata)

        entry.updated_at = datetime.now()

        self._save_knowledge_base()

        logger.info(f"Updated knowledge entry: {entry_id}")

        return entry

    def delete_entry(self, entry_id: str) -> bool:
        """
        Delete an entry

        Args:
            entry_id: Entry ID

        Returns:
            True if deleted, False if not found
        """
        entry = self.entries.get(entry_id)

        if not entry:
            return False

        # Remove from indices
        self.category_index[entry.category].remove(entry_id)
        for tag in entry.tags:
            self.tag_index[tag].remove(entry_id)

        # Remove entry
        del self.entries[entry_id]

        self._save_knowledge_base()

        logger.info(f"Deleted knowledge entry: {entry_id}")

        return True

    def search_by_category(self, category: str) -> List[KnowledgeEntry]:
        """
        Search entries by category

        Args:
            category: Category name

        Returns:
            List of matching entries
        """
        entry_ids = self.category_index.get(category, [])
        return [self.entries[eid] for eid in entry_ids]

    def search_by_tags(self, tags: List[str], match_all: bool = True) -> List[KnowledgeEntry]:
        """
        Search entries by tags

        Args:
            tags: List of tags to search
            match_all: If True, entry must have all tags; if False, any tag

        Returns:
            List of matching entries
        """
        if match_all:
            # Entry must have all tags
            entry_sets = [set(self.tag_index.get(tag, [])) for tag in tags]
            if entry_sets:
                matching_ids = set.intersection(*entry_sets)
            else:
                matching_ids = set()
        else:
            # Entry can have any tag
            matching_ids = set()
            for tag in tags:
                matching_ids.update(self.tag_index.get(tag, []))

        return [self.entries[eid] for eid in matching_ids]

    def search_by_text(self, query: str) -> List[KnowledgeEntry]:
        """
        Simple text search in title and content

        Args:
            query: Search query

        Returns:
            List of matching entries
        """
        query_lower = query.lower()
        matching = []

        for entry in self.entries.values():
            # Search in title
            if query_lower in entry.title.lower():
                matching.append(entry)
                continue

            # Search in content (convert to string)
            content_str = json.dumps(entry.content).lower()
            if query_lower in content_str:
                matching.append(entry)

        logger.info(f"Text search for '{query}': {len(matching)} results")

        return matching

    def get_most_used(self, limit: int = 10) -> List[KnowledgeEntry]:
        """
        Get most frequently used entries

        Args:
            limit: Maximum number of entries

        Returns:
            List of most used entries
        """
        sorted_entries = sorted(
            self.entries.values(),
            key=lambda e: e.usage_count,
            reverse=True
        )

        return sorted_entries[:limit]

    def get_best_performing(self, limit: int = 10) -> List[KnowledgeEntry]:
        """
        Get entries with highest success rate

        Args:
            limit: Maximum number of entries

        Returns:
            List of best performing entries
        """
        # Filter entries with at least some usage
        used_entries = [e for e in self.entries.values() if e.usage_count > 0]

        sorted_entries = sorted(
            used_entries,
            key=lambda e: e.success_rate,
            reverse=True
        )

        return sorted_entries[:limit]

    def record_usage(
        self,
        entry_id: str,
        success: bool
    ) -> None:
        """
        Record usage of an entry

        Args:
            entry_id: Entry ID
            success: Whether the usage was successful
        """
        entry = self.entries.get(entry_id)

        if not entry:
            return

        # Update usage count
        entry.usage_count += 1

        # Update success rate
        if entry.usage_count == 1:
            entry.success_rate = 1.0 if success else 0.0
        else:
            # Incremental average
            old_count = entry.usage_count - 1
            entry.success_rate = (entry.success_rate * old_count + (1.0 if success else 0.0)) / entry.usage_count

        self._save_knowledge_base()

        logger.debug(f"Recorded usage for {entry_id}: success={success}, total={entry.usage_count}")

    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        total_entries = len(self.entries)

        category_counts = {
            category: len(entry_ids)
            for category, entry_ids in self.category_index.items()
        }

        total_usage = sum(e.usage_count for e in self.entries.values())

        avg_success_rate = 0.0
        if self.entries:
            used_entries = [e for e in self.entries.values() if e.usage_count > 0]
            if used_entries:
                avg_success_rate = sum(e.success_rate for e in used_entries) / len(used_entries)

        return {
            'total_entries': total_entries,
            'categories': category_counts,
            'total_tags': len(self.tag_index),
            'total_usage': total_usage,
            'avg_success_rate': avg_success_rate,
            'most_used_category': max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else None
        }

    def export_entries(self, file_path: str, category: Optional[str] = None) -> None:
        """
        Export entries to JSON file

        Args:
            file_path: Export file path
            category: Optional category filter
        """
        if category:
            entries_to_export = self.search_by_category(category)
        else:
            entries_to_export = list(self.entries.values())

        data = {
            'entries': [entry.to_dict() for entry in entries_to_export],
            'exported_at': datetime.now().isoformat(),
            'total_entries': len(entries_to_export)
        }

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"Exported {len(entries_to_export)} entries to {file_path}")

    def import_entries(self, file_path: str, overwrite: bool = False) -> int:
        """
        Import entries from JSON file

        Args:
            file_path: Import file path
            overwrite: Whether to overwrite existing entries

        Returns:
            Number of entries imported
        """
        with open(file_path, 'r') as f:
            data = json.load(f)

        imported_count = 0

        for entry_data in data.get('entries', []):
            entry = KnowledgeEntry.from_dict(entry_data)

            if entry.entry_id in self.entries and not overwrite:
                logger.warning(f"Entry {entry.entry_id} already exists, skipping")
                continue

            self.entries[entry.entry_id] = entry

            # Update indices
            self.category_index[entry.category].append(entry.entry_id)
            for tag in entry.tags:
                self.tag_index[tag].append(entry.entry_id)

            imported_count += 1

        self._save_knowledge_base()

        logger.info(f"Imported {imported_count} entries from {file_path}")

        return imported_count
