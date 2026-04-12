"""
Example: Knowledge Base and Few-shot Learning

Demonstrates how to use the knowledge module for:
- Knowledge base management
- Knowledge retrieval
- Few-shot example selection
- Prompt engineering and optimization
"""

import random
from aeva.knowledge import (
    KnowledgeBase,
    KnowledgeEntry,
    KnowledgeRetriever,
    SemanticRetriever,
    FewShotLearner,
    FewShotSelector,
    PromptBuilder,
    PromptTemplate,
    PromptOptimizer
)


def create_sample_knowledge_entries():
    """Create sample knowledge entries for demonstration"""
    entries = [
        {
            'entry_id': 'example_001',
            'category': 'test_case',
            'title': 'Sentiment Analysis - Positive Example',
            'content': {
                'input': 'This movie was absolutely fantastic! I loved every minute of it.',
                'output': 'positive',
                'label': 'positive'
            },
            'tags': ['sentiment', 'positive', 'movie']
        },
        {
            'entry_id': 'example_002',
            'category': 'test_case',
            'title': 'Sentiment Analysis - Negative Example',
            'content': {
                'input': 'Terrible experience. Would not recommend to anyone.',
                'output': 'negative',
                'label': 'negative'
            },
            'tags': ['sentiment', 'negative', 'review']
        },
        {
            'entry_id': 'example_003',
            'category': 'test_case',
            'title': 'Sentiment Analysis - Neutral Example',
            'content': {
                'input': 'The product arrived on time and matches the description.',
                'output': 'neutral',
                'label': 'neutral'
            },
            'tags': ['sentiment', 'neutral', 'product']
        },
        {
            'entry_id': 'example_004',
            'category': 'test_case',
            'title': 'NER - Person and Location',
            'content': {
                'input': 'John Smith visited Paris last summer.',
                'output': 'Person: John Smith, Location: Paris',
                'label': 'ner'
            },
            'tags': ['ner', 'person', 'location']
        },
        {
            'entry_id': 'example_005',
            'category': 'test_case',
            'title': 'NER - Organization',
            'content': {
                'input': 'Apple Inc. announced new products at their headquarters.',
                'output': 'Organization: Apple Inc.',
                'label': 'ner'
            },
            'tags': ['ner', 'organization']
        },
        {
            'entry_id': 'example_006',
            'category': 'best_practice',
            'title': 'Clear Task Description',
            'content': {
                'description': 'Always provide clear and specific task descriptions',
                'example': 'Instead of "Classify this", use "Classify the sentiment as positive, negative, or neutral"'
            },
            'tags': ['prompt', 'clarity']
        },
        {
            'entry_id': 'example_007',
            'category': 'best_practice',
            'title': 'Include Examples',
            'content': {
                'description': 'Few-shot examples significantly improve performance',
                'guideline': 'Include 3-5 diverse examples for best results'
            },
            'tags': ['few-shot', 'examples']
        },
        {
            'entry_id': 'example_008',
            'category': 'test_case',
            'title': 'QA - Simple Fact',
            'content': {
                'input': 'What is the capital of France?',
                'output': 'Paris',
                'label': 'qa'
            },
            'tags': ['qa', 'factual']
        }
    ]

    return entries


def example_knowledge_base_management():
    """Example 1: Basic knowledge base operations"""
    print("=" * 70)
    print("Example 1: Knowledge Base Management")
    print("=" * 70)

    # Create knowledge base
    kb = KnowledgeBase(storage_path="./example_kb")

    print(f"\n✓ Knowledge base initialized")

    # Add entries
    print("\n📝 Adding Knowledge Entries:")
    sample_entries = create_sample_knowledge_entries()

    for entry_data in sample_entries:
        kb.add_entry(**entry_data)
        print(f"  Added: {entry_data['title']}")

    # Get statistics
    print("\n📊 Knowledge Base Statistics:")
    stats = kb.get_statistics()
    print(f"  Total Entries: {stats['total_entries']}")
    print(f"  Categories: {stats['categories']}")
    print(f"  Total Tags: {stats['total_tags']}")

    # Search by category
    print("\n🔍 Search by Category (test_case):")
    test_cases = kb.search_by_category('test_case')
    print(f"  Found {len(test_cases)} test cases")
    for tc in test_cases[:3]:
        print(f"    - {tc.title}")

    # Search by tags
    print("\n🏷️ Search by Tags (sentiment):")
    sentiment_entries = kb.search_by_tags(['sentiment'])
    print(f"  Found {len(sentiment_entries)} sentiment-related entries")

    # Text search
    print("\n🔎 Text Search ('Paris'):")
    results = kb.search_by_text('Paris')
    print(f"  Found {len(results)} matching entries")
    for result in results:
        print(f"    - {result.title}")

    return kb


def example_knowledge_retrieval(kb):
    """Example 2: Knowledge retrieval"""
    print("\n" + "=" * 70)
    print("Example 2: Knowledge Retrieval")
    print("=" * 70)

    # Create retriever
    retriever = KnowledgeRetriever(kb)

    # Retrieve relevant knowledge
    print("\n🔍 Query: 'sentiment analysis positive'")
    results = retriever.retrieve(
        query='sentiment analysis positive',
        top_k=3
    )

    print(f"\nRetrieved {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.entry.title}")
        print(f"   Score: {result.score:.4f}")
        print(f"   Relevance: {result.relevance}")
        print(f"   Category: {result.entry.category}")

    # Retrieve similar entries
    print("\n🔗 Finding Similar Entries to 'example_001':")
    similar = retriever.retrieve_similar('example_001', top_k=3)

    print(f"\nFound {len(similar)} similar entries:")
    for result in similar:
        print(f"  - {result.entry.title} (score: {result.score:.4f})")

    return retriever


def example_semantic_retrieval(kb):
    """Example 3: Semantic retrieval"""
    print("\n" + "=" * 70)
    print("Example 3: Semantic Retrieval")
    print("=" * 70)

    # Create semantic retriever
    semantic_retriever = SemanticRetriever(kb)

    # Precompute embeddings
    print("\n🧮 Precomputing embeddings...")
    semantic_retriever.precompute_embeddings()
    print(f"  ✓ Computed embeddings for {len(kb.entries)} entries")

    # Semantic search
    print("\n🔍 Semantic Query: 'finding named entities'")
    results = semantic_retriever.retrieve(
        query='finding named entities',
        top_k=3
    )

    print(f"\nSemanticly similar results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.entry.title}")
        print(f"   Similarity: {result.score:.4f}")
        print(f"   Tags: {', '.join(result.entry.tags)}")

    return semantic_retriever


def example_few_shot_selection(kb):
    """Example 4: Few-shot example selection"""
    print("\n" + "=" * 70)
    print("Example 4: Few-shot Example Selection")
    print("=" * 70)

    # Create selector
    selector = FewShotSelector(kb)

    # 1. Random selection
    print("\n1️⃣ Random Selection (3 examples):")
    random_examples = selector.select_random(
        n_examples=3,
        category='test_case',
        random_seed=42
    )

    for i, example in enumerate(random_examples, 1):
        print(f"  {i}. {example.metadata['title']}")

    # 2. Diverse selection
    print("\n2️⃣ Diverse Selection (3 examples, balanced by label):")
    diverse_examples = selector.select_diverse(
        n_examples=3,
        category='test_case',
        diversity_key='label'
    )

    for i, example in enumerate(diverse_examples, 1):
        label = example.input if isinstance(example.input, str) else 'N/A'
        print(f"  {i}. {example.metadata['title']}")

    # 3. Similar selection
    print("\n3️⃣ Similar Selection (query: 'sentiment positive'):")
    similar_examples = selector.select_similar(
        query='sentiment positive',
        n_examples=3,
        category='test_case'
    )

    for i, example in enumerate(similar_examples, 1):
        score = example.metadata.get('relevance_score', 0)
        print(f"  {i}. {example.metadata['title']} (score: {score:.4f})")

    # Record usage
    print("\n📊 Recording Example Usage:")
    for example in random_examples:
        success = random.choice([True, True, True, False])  # 75% success rate
        kb.record_usage(example.metadata['entry_id'], success)

    # 4. Best performing selection
    print("\n4️⃣ Best Performing Selection:")
    best_examples = selector.select_best_performing(
        n_examples=3,
        category='test_case'
    )

    for i, example in enumerate(best_examples, 1):
        success_rate = example.metadata.get('success_rate', 0)
        print(f"  {i}. {example.metadata['title']} (success: {success_rate:.2%})")

    return selector


def example_few_shot_learning(kb):
    """Example 5: Few-shot learning"""
    print("\n" + "=" * 70)
    print("Example 5: Few-shot Learning")
    print("=" * 70)

    # Create learner
    learner = FewShotLearner(kb)

    # Test input
    test_input = "This restaurant serves amazing food with great service!"

    # Create few-shot evaluation
    print("\n🎯 Few-shot Evaluation:")
    print(f"Test Input: '{test_input}'")

    result = learner.evaluate_with_few_shot(
        test_input=test_input,
        n_examples=3,
        selection_strategy='similar',
        category='test_case',
        query='sentiment'
    )

    print(f"\n✓ Generated Few-shot Prompt:")
    print(f"  Strategy: {result['selection_strategy']}")
    print(f"  Examples Used: {result['n_examples']}")

    print(f"\n📝 Prompt Preview:")
    print("-" * 70)
    print(result['prompt'][:500])
    print("... (truncated)")
    print("-" * 70)

    # Track performance
    print("\n📈 Tracking Performance:")
    for example_dict in result['examples']:
        entry_id = example_dict['metadata']['entry_id']
        success = random.choice([True, True, True, False])
        learner.track_example_performance(entry_id, success)
        print(f"  Tracked: {entry_id} (success={success})")

    return learner


def example_prompt_engineering():
    """Example 6: Prompt engineering"""
    print("\n" + "=" * 70)
    print("Example 6: Prompt Engineering")
    print("=" * 70)

    # Create builder
    builder = PromptBuilder()

    # 1. Use template
    print("\n1️⃣ Using Prompt Template:")
    prompt = builder.build_prompt(
        template_id='sentiment',
        text='This product exceeded my expectations!'
    )

    print(prompt)

    # 2. Zero-shot prompt
    print("\n2️⃣ Zero-shot Prompt:")
    zero_shot = builder.build_zero_shot_prompt(
        task_description='Classify the sentiment of the text as positive, negative, or neutral.',
        input_text='The service was okay, nothing special.',
        output_format='Format: sentiment (confidence: 0-1)'
    )

    print(zero_shot)

    # 3. Few-shot prompt
    print("\n3️⃣ Few-shot Prompt:")
    examples = [
        {'input': 'Excellent quality!', 'output': 'positive'},
        {'input': 'Very disappointed.', 'output': 'negative'},
        {'input': 'It works as described.', 'output': 'neutral'}
    ]

    few_shot = builder.build_few_shot_prompt(
        task_description='Classify sentiment:',
        examples=examples,
        test_input='Amazing customer support!'
    )

    print(few_shot)

    # 4. Chain-of-thought
    print("\n4️⃣ Chain-of-thought Prompt:")
    cot = builder.build_chain_of_thought_prompt(
        task='Determine if the review is positive or negative',
        input_text='The food was great but the service was slow.',
        n_steps=3
    )

    print(cot)

    # 5. Validate prompt
    print("\n5️⃣ Prompt Validation:")
    validation = builder.validate_prompt(prompt)

    print(f"  Valid: {validation['valid']}")
    print(f"  Length: {validation['length']} chars, {validation['word_count']} words")
    if validation['issues']:
        print(f"  Issues: {validation['issues']}")
    if validation['suggestions']:
        print(f"  Suggestions:")
        for suggestion in validation['suggestions'][:3]:
            print(f"    - {suggestion}")

    return builder


def example_prompt_optimization():
    """Example 7: Prompt optimization"""
    print("\n" + "=" * 70)
    print("Example 7: Prompt Optimization")
    print("=" * 70)

    # Create optimizer
    optimizer = PromptOptimizer()

    # Simulate performance tracking
    print("\n📊 Tracking Prompt Performance:")

    prompt_variants = {
        'prompt_v1': [0.75, 0.78, 0.76, 0.80, 0.77],
        'prompt_v2': [0.82, 0.85, 0.83, 0.87, 0.84],
        'prompt_v3': [0.70, 0.72, 0.71, 0.73, 0.69]
    }

    for prompt_id, scores in prompt_variants.items():
        for score in scores:
            optimizer.track_performance(prompt_id, score)
        avg = sum(scores) / len(scores)
        print(f"  {prompt_id}: avg={avg:.4f} ({len(scores)} samples)")

    # Compare prompts
    print("\n⚖️ Comparing Prompts:")
    comparison = optimizer.compare_prompts('prompt_v1', 'prompt_v2')

    print(f"\n  Prompt A (v1): {comparison['prompt_a']['avg_score']:.4f}")
    print(f"  Prompt B (v2): {comparison['prompt_b']['avg_score']:.4f}")
    print(f"  Winner: {comparison['winner']}")
    print(f"  Improvement: {comparison['improvement_pct']:.2f}%")

    # Get best prompt
    print("\n🏆 Best Performing Prompt:")
    best = optimizer.get_best_prompt(min_samples=3)
    print(f"  {best}")

    # Suggest improvements
    print("\n💡 Improvement Suggestions:")
    sample_prompt = "Classify this text"
    suggestions = optimizer.suggest_improvements(sample_prompt)

    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. {suggestion}")

    # Statistics
    print("\n📈 Optimization Statistics:")
    stats = optimizer.get_statistics()
    print(f"  Total Prompts Tracked: {stats['total_prompts_tracked']}")
    print(f"  Total Evaluations: {stats['total_evaluations']}")
    print(f"  Average Score: {stats['avg_score']:.4f}")

    return optimizer


def example_integrated_workflow(kb):
    """Example 8: Integrated workflow"""
    print("\n" + "=" * 70)
    print("Example 8: Integrated Knowledge-based Evaluation")
    print("=" * 70)

    print("\nScenario: Evaluate sentiment classification with knowledge base")

    # 1. Query knowledge base
    print("\n📚 Step 1: Query Knowledge Base")
    retriever = KnowledgeRetriever(kb)

    results = retriever.retrieve(
        query='sentiment classification',
        top_k=5,
        category='test_case'
    )
    print(f"  Retrieved {len(results)} relevant examples")

    # 2. Select few-shot examples
    print("\n🎯 Step 2: Select Few-shot Examples")
    selector = FewShotSelector(kb, retriever)

    examples = selector.select_similar(
        query='positive sentiment',
        n_examples=3,
        category='test_case'
    )
    print(f"  Selected {len(examples)} examples")

    # 3. Build prompt
    print("\n✍️ Step 3: Build Evaluation Prompt")
    builder = PromptBuilder()

    test_input = "The product quality is outstanding!"

    prompt = builder.build_few_shot_prompt(
        task_description='Classify the sentiment as positive, negative, or neutral:',
        examples=[
            {'input': ex.input, 'output': ex.output}
            for ex in examples
        ],
        test_input=test_input
    )

    print(f"  ✓ Prompt created ({len(prompt)} characters)")

    # 4. Validate prompt
    print("\n✅ Step 4: Validate Prompt")
    validation = builder.validate_prompt(prompt)
    print(f"  Valid: {validation['valid']}")
    print(f"  Length: {validation['length']} chars")

    # 5. Track performance
    print("\n📊 Step 5: Track Performance")
    for example in examples:
        kb.record_usage(example.metadata['entry_id'], success=True)
    print(f"  ✓ Recorded usage for {len(examples)} examples")

    # 6. Summary
    print("\n" + "=" * 70)
    print("Workflow Complete!")
    print("=" * 70)
    print(f"✓ Retrieved {len(results)} relevant knowledge entries")
    print(f"✓ Selected {len(examples)} few-shot examples")
    print(f"✓ Generated prompt ({len(prompt)} chars)")
    print(f"✓ Validated and ready for evaluation")


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("AEVA Knowledge Base and Few-shot Learning Examples")
    print("=" * 70)

    # Run examples
    kb = example_knowledge_base_management()
    retriever = example_knowledge_retrieval(kb)
    semantic = example_semantic_retrieval(kb)
    selector = example_few_shot_selection(kb)
    learner = example_few_shot_learning(kb)
    builder = example_prompt_engineering()
    optimizer = example_prompt_optimization()
    example_integrated_workflow(kb)

    print("\n" + "=" * 70)
    print("All Examples Completed!")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  ✓ Knowledge base CRUD operations")
    print("  ✓ Multi-strategy knowledge retrieval")
    print("  ✓ Semantic similarity search")
    print("  ✓ Few-shot example selection (4 strategies)")
    print("  ✓ Few-shot prompt generation")
    print("  ✓ Prompt engineering (5 types)")
    print("  ✓ Prompt optimization and A/B testing")
    print("  ✓ Integrated evaluation workflow")


if __name__ == '__main__':
    main()
