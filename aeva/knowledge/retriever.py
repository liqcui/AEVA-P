"""
Knowledge Retrieval

Retrieve relevant knowledge entries based on query

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
import math

from aeva.knowledge.base import KnowledgeBase, KnowledgeEntry

logger = logging.getLogger(__name__)


@dataclass
class RetrievalResult:
    """Result of knowledge retrieval"""
    entry: KnowledgeEntry
    score: float
    relevance: str  # 'high', 'medium', 'low'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'entry': self.entry.to_dict(),
            'score': self.score,
            'relevance': self.relevance
        }


class KnowledgeRetriever:
    """
    Retrieve relevant knowledge entries

    Features:
    - Keyword-based retrieval
    - TF-IDF scoring
    - Relevance ranking
    - Filtering by category/tags
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initialize retriever

        Args:
            knowledge_base: KnowledgeBase instance
        """
        self.kb = knowledge_base

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_score: float = 0.0
    ) -> List[RetrievalResult]:
        """
        Retrieve relevant entries

        Args:
            query: Search query
            top_k: Number of results to return
            category: Optional category filter
            tags: Optional tag filter
            min_score: Minimum relevance score

        Returns:
            List of RetrievalResult
        """
        logger.info(f"Retrieving knowledge for query: '{query}'")

        # Get candidate entries
        candidates = self._get_candidates(category, tags)

        if not candidates:
            logger.warning("No candidate entries found")
            return []

        # Score each candidate
        scored_results = []

        for entry in candidates:
            score = self._calculate_score(query, entry)

            if score >= min_score:
                relevance = self._determine_relevance(score)

                scored_results.append(RetrievalResult(
                    entry=entry,
                    score=score,
                    relevance=relevance
                ))

        # Sort by score descending
        scored_results.sort(key=lambda x: x.score, reverse=True)

        # Return top k
        results = scored_results[:top_k]

        logger.info(f"Retrieved {len(results)} relevant entries")

        return results

    def _get_candidates(
        self,
        category: Optional[str],
        tags: Optional[List[str]]
    ) -> List[KnowledgeEntry]:
        """Get candidate entries based on filters"""
        candidates = list(self.kb.entries.values())

        if category:
            candidates = [e for e in candidates if e.category == category]

        if tags:
            # Entry must have at least one tag
            candidates = [
                e for e in candidates
                if any(tag in e.tags for tag in tags)
            ]

        return candidates

    def _calculate_score(self, query: str, entry: KnowledgeEntry) -> float:
        """
        Calculate relevance score

        Simple scoring based on:
        - Title match
        - Tag match
        - Content match
        - Usage statistics
        """
        score = 0.0

        query_lower = query.lower()
        query_tokens = set(query_lower.split())

        # Title match (weight: 0.4)
        title_lower = entry.title.lower()
        title_tokens = set(title_lower.split())

        title_overlap = len(query_tokens & title_tokens)
        if title_overlap > 0:
            title_score = title_overlap / len(query_tokens) if query_tokens else 0
            score += title_score * 0.4

        # Tag match (weight: 0.3)
        entry_tags_lower = [tag.lower() for tag in entry.tags]
        tag_overlap = sum(1 for token in query_tokens if token in entry_tags_lower)

        if tag_overlap > 0:
            tag_score = tag_overlap / len(query_tokens) if query_tokens else 0
            score += tag_score * 0.3

        # Content match (weight: 0.2)
        import json
        content_str = json.dumps(entry.content).lower()

        content_overlap = sum(1 for token in query_tokens if token in content_str)
        if content_overlap > 0:
            content_score = content_overlap / len(query_tokens) if query_tokens else 0
            score += content_score * 0.2

        # Success rate bonus (weight: 0.1)
        if entry.usage_count > 0:
            score += entry.success_rate * 0.1

        return score

    def _determine_relevance(self, score: float) -> str:
        """Determine relevance level from score"""
        if score >= 0.7:
            return 'high'
        elif score >= 0.4:
            return 'medium'
        else:
            return 'low'

    def retrieve_similar(
        self,
        entry_id: str,
        top_k: int = 5
    ) -> List[RetrievalResult]:
        """
        Retrieve entries similar to a given entry

        Args:
            entry_id: Reference entry ID
            top_k: Number of results

        Returns:
            List of similar entries
        """
        reference = self.kb.get_entry(entry_id)

        if not reference:
            logger.warning(f"Entry not found: {entry_id}")
            return []

        # Use title and tags as query
        query = reference.title + " " + " ".join(reference.tags)

        results = self.retrieve(
            query=query,
            top_k=top_k + 1,  # +1 because reference will be in results
            category=reference.category
        )

        # Remove reference entry from results
        results = [r for r in results if r.entry.entry_id != entry_id]

        return results[:top_k]


class SemanticRetriever(KnowledgeRetriever):
    """
    Semantic retrieval using embeddings

    Note: This is a simplified version. In production, use proper embedding models.
    """

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        embedding_fn: Optional[Callable[[str], List[float]]] = None
    ):
        """
        Initialize semantic retriever

        Args:
            knowledge_base: KnowledgeBase instance
            embedding_fn: Function to compute embeddings
        """
        super().__init__(knowledge_base)

        self.embedding_fn = embedding_fn or self._simple_embedding

        # Cache embeddings
        self.entry_embeddings: Dict[str, List[float]] = {}

        logger.info("Semantic retriever initialized")

    def _simple_embedding(self, text: str) -> List[float]:
        """
        Simple embedding based on character frequencies

        In production, use proper embedding models (e.g., sentence-transformers)
        """
        # Character frequency-based embedding (simplified)
        text_lower = text.lower()

        # Simple features: letter frequencies
        embedding = [0.0] * 26

        for char in text_lower:
            if 'a' <= char <= 'z':
                idx = ord(char) - ord('a')
                embedding[idx] += 1

        # Normalize
        total = sum(embedding)
        if total > 0:
            embedding = [x / total for x in embedding]

        return embedding

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between vectors"""
        if len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)

    def _get_entry_embedding(self, entry: KnowledgeEntry) -> List[float]:
        """Get or compute embedding for entry"""
        if entry.entry_id in self.entry_embeddings:
            return self.entry_embeddings[entry.entry_id]

        # Combine title and content for embedding
        import json
        text = entry.title + " " + json.dumps(entry.content)

        embedding = self.embedding_fn(text)
        self.entry_embeddings[entry.entry_id] = embedding

        return embedding

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_score: float = 0.0
    ) -> List[RetrievalResult]:
        """
        Retrieve using semantic similarity

        Args:
            query: Search query
            top_k: Number of results
            category: Optional category filter
            tags: Optional tag filter
            min_score: Minimum similarity score

        Returns:
            List of RetrievalResult
        """
        logger.info(f"Semantic retrieval for query: '{query}'")

        # Compute query embedding
        query_embedding = self.embedding_fn(query)

        # Get candidates
        candidates = self._get_candidates(category, tags)

        if not candidates:
            return []

        # Calculate semantic similarity
        scored_results = []

        for entry in candidates:
            entry_embedding = self._get_entry_embedding(entry)
            similarity = self._cosine_similarity(query_embedding, entry_embedding)

            if similarity >= min_score:
                relevance = self._determine_relevance(similarity)

                scored_results.append(RetrievalResult(
                    entry=entry,
                    score=similarity,
                    relevance=relevance
                ))

        # Sort by similarity
        scored_results.sort(key=lambda x: x.score, reverse=True)

        results = scored_results[:top_k]

        logger.info(f"Retrieved {len(results)} semantically similar entries")

        return results

    def precompute_embeddings(self) -> None:
        """Precompute embeddings for all entries"""
        logger.info(f"Precomputing embeddings for {len(self.kb.entries)} entries")

        for entry in self.kb.entries.values():
            self._get_entry_embedding(entry)

        logger.info("Embedding precomputation complete")
