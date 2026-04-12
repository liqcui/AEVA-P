"""
LLM User Experience Evaluation Module

Evaluates user-facing quality metrics:
- Relevance scoring
- Fluency assessment
- Diversity analysis
- Sentiment analysis

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Watermark: AEVA-2026-LQC-dc68e33
"""

from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
import re
import math
from collections import Counter
import logging

logger = logging.getLogger(__name__)


@dataclass
class RelevanceResult:
    """Relevance scoring result"""
    relevance_score: float  # 0-1
    semantic_similarity: float
    context_match: float
    intent_alignment: float
    details: Dict[str, Any]


@dataclass
class FluencyResult:
    """Fluency evaluation result"""
    fluency_score: float  # 0-1
    readability_score: float
    coherence_score: float
    grammar_score: float
    naturalness_score: float
    issues: List[str]


@dataclass
class DiversityResult:
    """Diversity analysis result"""
    diversity_score: float  # 0-1
    vocabulary_richness: float
    unique_words_ratio: float
    repetition_score: float
    creativity_score: float
    statistics: Dict[str, Any]


@dataclass
class SentimentResult:
    """Sentiment analysis result"""
    sentiment: str  # 'positive', 'negative', 'neutral'
    polarity_score: float  # -1 to 1
    subjectivity_score: float  # 0 to 1
    emotion: str  # dominant emotion
    tone: str  # 'formal', 'casual', 'friendly', etc.


class RelevanceScorer:
    """
    Scores relevance of LLM output to input

    Features:
    - Semantic similarity
    - Context matching
    - Intent alignment
    """

    def __init__(self):
        """Initialize relevance scorer"""
        pass

    def score(
        self,
        output: str,
        input_text: str,
        context: Optional[str] = None,
        **kwargs
    ) -> RelevanceResult:
        """
        Score output relevance

        Args:
            output: LLM output to score
            input_text: Original input/query
            context: Additional context

        Returns:
            RelevanceResult with relevance scores
        """
        # Semantic similarity (word overlap based)
        semantic_similarity = self._calculate_semantic_similarity(
            output, input_text
        )

        # Context match
        context_match = 1.0
        if context:
            context_match = self._calculate_context_match(output, context)

        # Intent alignment (keyword matching)
        intent_alignment = self._calculate_intent_alignment(
            output, input_text
        )

        # Overall relevance score
        relevance_score = (
            semantic_similarity * 0.4 +
            context_match * 0.3 +
            intent_alignment * 0.3
        )

        return RelevanceResult(
            relevance_score=relevance_score,
            semantic_similarity=semantic_similarity,
            context_match=context_match,
            intent_alignment=intent_alignment,
            details={
                'output_length': len(output.split()),
                'input_length': len(input_text.split()),
                'overlap_ratio': semantic_similarity
            }
        )

    def _calculate_semantic_similarity(
        self,
        text1: str,
        text2: str
    ) -> float:
        """Calculate word-based semantic similarity"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        # Jaccard similarity
        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0.0

    def _calculate_context_match(self, output: str, context: str) -> float:
        """Calculate context matching score"""
        context_words = set(context.lower().split())
        output_words = set(output.lower().split())

        if not context_words:
            return 1.0

        # What percentage of context is covered in output
        coverage = len(context_words & output_words) / len(context_words)
        return min(1.0, coverage * 1.5)  # Scale up

    def _calculate_intent_alignment(
        self,
        output: str,
        input_text: str
    ) -> float:
        """Calculate intent alignment score"""
        # Extract question words/intent markers
        intent_markers = [
            'what', 'why', 'how', 'when', 'where', 'who',
            'explain', 'describe', 'list', 'analyze'
        ]

        input_lower = input_text.lower()
        output_lower = output.lower()

        # Check if output addresses the intent
        intent_found = False
        for marker in intent_markers:
            if marker in input_lower:
                intent_found = True
                # Output should have related content
                if len(output_lower) > 20:  # Non-trivial response
                    return 0.9
                else:
                    return 0.5

        return 0.7 if len(output_lower) > 0 else 0.0


class FluencyEvaluator:
    """
    Evaluates language fluency

    Features:
    - Readability
    - Coherence
    - Grammar checking (basic)
    - Naturalness
    """

    def __init__(self):
        """Initialize fluency evaluator"""
        # Common grammar issues patterns
        self.grammar_patterns = [
            (r'\b(a)\s+[aeiou]', 'Article error (a before vowel)'),
            (r'\b(an)\s+[^aeiou]', 'Article error (an before consonant)'),
            (r'(\w+)\s+\1', 'Word repetition'),
        ]

    def evaluate(self, text: str, **kwargs) -> FluencyResult:
        """
        Evaluate text fluency

        Args:
            text: Text to evaluate

        Returns:
            FluencyResult with fluency scores
        """
        # Readability (Flesch reading ease approximation)
        readability_score = self._calculate_readability(text)

        # Coherence (sentence transition smoothness)
        coherence_score = self._calculate_coherence(text)

        # Grammar (basic error detection)
        grammar_score, grammar_issues = self._check_grammar(text)

        # Naturalness (based on sentence structure variety)
        naturalness_score = self._calculate_naturalness(text)

        # Overall fluency score
        fluency_score = (
            readability_score * 0.25 +
            coherence_score * 0.25 +
            grammar_score * 0.3 +
            naturalness_score * 0.2
        )

        return FluencyResult(
            fluency_score=fluency_score,
            readability_score=readability_score,
            coherence_score=coherence_score,
            grammar_score=grammar_score,
            naturalness_score=naturalness_score,
            issues=grammar_issues
        )

    def _calculate_readability(self, text: str) -> float:
        """Calculate readability score (simplified Flesch)"""
        words = text.split()
        sentences = text.split('.')

        if not words or not sentences:
            return 0.5

        avg_word_length = sum(len(w) for w in words) / len(words)
        avg_sentence_length = len(words) / len(sentences)

        # Ideal: 5 letter words, 15-20 words per sentence
        word_score = 1.0 - abs(avg_word_length - 5) / 10
        sentence_score = 1.0 - abs(avg_sentence_length - 17) / 30

        readability = (word_score + sentence_score) / 2
        return max(0.0, min(1.0, readability))

    def _calculate_coherence(self, text: str) -> float:
        """Calculate coherence score"""
        sentences = [s.strip() for s in text.split('.') if s.strip()]

        if len(sentences) < 2:
            return 1.0

        # Check for transition words
        transition_words = [
            'however', 'therefore', 'furthermore', 'additionally',
            'moreover', 'consequently', 'thus', 'hence'
        ]

        transition_count = 0
        for sentence in sentences[1:]:  # Skip first sentence
            if any(word in sentence.lower() for word in transition_words):
                transition_count += 1

        # Score based on transition usage
        coherence = transition_count / (len(sentences) - 1)
        return min(1.0, coherence + 0.5)  # Add base score

    def _check_grammar(self, text: str) -> tuple:
        """Basic grammar checking"""
        issues = []
        error_count = 0

        for pattern, description in self.grammar_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                issues.append(f"{description} ({len(matches)} occurrences)")
                error_count += len(matches)

        # Grammar score (inversely proportional to errors)
        words_count = len(text.split())
        if words_count == 0:
            return 1.0, issues

        error_ratio = error_count / words_count
        grammar_score = max(0.0, 1.0 - error_ratio * 5)

        return grammar_score, issues

    def _calculate_naturalness(self, text: str) -> float:
        """Calculate naturalness score"""
        sentences = [s.strip() for s in text.split('.') if s.strip()]

        if not sentences:
            return 0.5

        # Check sentence length variety
        lengths = [len(s.split()) for s in sentences]
        if not lengths:
            return 0.5

        avg_length = sum(lengths) / len(lengths)
        variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)

        # Higher variance = more natural (variety)
        naturalness = min(1.0, math.sqrt(variance) / 10)
        return max(0.5, naturalness)


class DiversityAnalyzer:
    """
    Analyzes output diversity

    Features:
    - Vocabulary richness
    - Unique word ratio
    - Repetition detection
    - Creativity scoring
    """

    def __init__(self):
        """Initialize diversity analyzer"""
        pass

    def analyze(self, text: str, **kwargs) -> DiversityResult:
        """
        Analyze text diversity

        Args:
            text: Text to analyze

        Returns:
            DiversityResult with diversity metrics
        """
        words = text.lower().split()

        if not words:
            return DiversityResult(
                diversity_score=0.0,
                vocabulary_richness=0.0,
                unique_words_ratio=0.0,
                repetition_score=1.0,
                creativity_score=0.0,
                statistics={}
            )

        # Vocabulary richness (Type-Token Ratio)
        vocabulary_richness = len(set(words)) / len(words)

        # Unique words ratio
        unique_words_ratio = len(set(words)) / len(words)

        # Repetition detection (inverse of repetition)
        repetition_score = self._calculate_repetition(words)

        # Creativity (based on rare word usage)
        creativity_score = self._calculate_creativity(words)

        # Overall diversity score
        diversity_score = (
            vocabulary_richness * 0.3 +
            unique_words_ratio * 0.2 +
            repetition_score * 0.3 +
            creativity_score * 0.2
        )

        statistics = {
            'total_words': len(words),
            'unique_words': len(set(words)),
            'most_common': Counter(words).most_common(5),
            'type_token_ratio': vocabulary_richness
        }

        return DiversityResult(
            diversity_score=diversity_score,
            vocabulary_richness=vocabulary_richness,
            unique_words_ratio=unique_words_ratio,
            repetition_score=repetition_score,
            creativity_score=creativity_score,
            statistics=statistics
        )

    def _calculate_repetition(self, words: List[str]) -> float:
        """Calculate repetition score (lower repetition = higher score)"""
        if not words:
            return 1.0

        word_counts = Counter(words)
        max_repetition = max(word_counts.values())

        # Score inversely proportional to max repetition
        repetition_score = 1.0 / max_repetition if max_repetition > 0 else 1.0
        return min(1.0, repetition_score)

    def _calculate_creativity(self, words: List[str]) -> float:
        """Calculate creativity score (usage of less common words)"""
        # Common English words (partial list)
        common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
            'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are',
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had'
        }

        if not words:
            return 0.0

        # Ratio of uncommon words
        uncommon_count = sum(1 for w in words if w not in common_words)
        creativity_score = uncommon_count / len(words)

        return min(1.0, creativity_score)


class SentimentAnalyzer:
    """
    Analyzes sentiment and tone

    Features:
    - Polarity detection (positive/negative/neutral)
    - Subjectivity scoring
    - Emotion detection
    - Tone classification
    """

    def __init__(self):
        """Initialize sentiment analyzer"""
        # Sentiment lexicons (simplified)
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful',
            'fantastic', 'awesome', 'love', 'happy', 'joy', 'best'
        }
        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'worst',
            'hate', 'sad', 'angry', 'poor', 'disappointing'
        }

        # Emotion keywords
        self.emotions = {
            'joy': ['happy', 'joy', 'delighted', 'cheerful'],
            'sadness': ['sad', 'unhappy', 'depressed', 'sorrowful'],
            'anger': ['angry', 'furious', 'mad', 'irritated'],
            'fear': ['afraid', 'scared', 'fearful', 'anxious'],
            'surprise': ['surprised', 'amazed', 'astonished']
        }

    def analyze(self, text: str, **kwargs) -> SentimentResult:
        """
        Analyze sentiment

        Args:
            text: Text to analyze

        Returns:
            SentimentResult with sentiment analysis
        """
        words = text.lower().split()

        # Polarity score
        polarity_score, sentiment = self._calculate_polarity(words)

        # Subjectivity score
        subjectivity_score = self._calculate_subjectivity(words)

        # Emotion detection
        emotion = self._detect_emotion(words)

        # Tone classification
        tone = self._classify_tone(text, polarity_score)

        return SentimentResult(
            sentiment=sentiment,
            polarity_score=polarity_score,
            subjectivity_score=subjectivity_score,
            emotion=emotion,
            tone=tone
        )

    def _calculate_polarity(self, words: List[str]) -> tuple:
        """Calculate polarity score"""
        positive_count = sum(1 for w in words if w in self.positive_words)
        negative_count = sum(1 for w in words if w in self.negative_words)

        total_sentiment_words = positive_count + negative_count

        if total_sentiment_words == 0:
            return 0.0, 'neutral'

        # Polarity: -1 (negative) to +1 (positive)
        polarity = (positive_count - negative_count) / total_sentiment_words

        # Classify sentiment
        if polarity > 0.2:
            sentiment = 'positive'
        elif polarity < -0.2:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        return polarity, sentiment

    def _calculate_subjectivity(self, words: List[str]) -> float:
        """Calculate subjectivity score (0=objective, 1=subjective)"""
        # Subjective indicators
        subjective_words = {
            'i', 'me', 'my', 'think', 'believe', 'feel',
            'opinion', 'seems', 'appears', 'probably'
        }

        if not words:
            return 0.0

        subjective_count = sum(1 for w in words if w in subjective_words)
        subjectivity = subjective_count / len(words)

        return min(1.0, subjectivity * 5)  # Scale up

    def _detect_emotion(self, words: List[str]) -> str:
        """Detect dominant emotion"""
        emotion_scores = {}

        for emotion, keywords in self.emotions.items():
            count = sum(1 for w in words if w in keywords)
            emotion_scores[emotion] = count

        if not any(emotion_scores.values()):
            return 'neutral'

        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        return dominant_emotion

    def _classify_tone(self, text: str, polarity: float) -> str:
        """Classify tone of text"""
        # Simple heuristics
        has_questions = '?' in text
        has_exclamations = '!' in text
        is_short = len(text.split()) < 10

        if has_exclamations and polarity > 0:
            return 'enthusiastic'
        elif has_exclamations and polarity < 0:
            return 'aggressive'
        elif has_questions:
            return 'inquisitive'
        elif polarity > 0.5:
            return 'friendly'
        elif polarity < -0.5:
            return 'hostile'
        elif is_short:
            return 'direct'
        else:
            return 'neutral'
