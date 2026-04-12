"""
Example: Dataset Management and Quality Analysis

Demonstrates how to use the dataset management module for:
- Dataset registration and loading
- Quality analysis
- Dataset splitting
- Dataset sampling
- Version control
"""

import random
from datetime import datetime, timedelta
from aeva.dataset import (
    DatasetManager,
    DataQualityAnalyzer,
    DatasetSplitter,
    DatasetSampler,
    VersionControl
)


def create_mock_classification_dataset(n_samples: int = 1000, imbalance_ratio: float = 1.0):
    """
    Create mock classification dataset

    Args:
        n_samples: Number of samples
        imbalance_ratio: Ratio of majority to minority class (1.0 = balanced)
    """
    data = []
    labels = ['positive', 'negative', 'neutral']

    # Create imbalanced distribution if requested
    if imbalance_ratio > 1.0:
        weights = [imbalance_ratio, 1.0, 1.0]
    else:
        weights = [1.0, 1.0, 1.0]

    for i in range(n_samples):
        label = random.choices(labels, weights=weights, k=1)[0]

        # Randomly introduce missing values
        text = f"Sample text {i}" if random.random() > 0.05 else ""  # 5% missing
        score = random.uniform(0, 1) if random.random() > 0.02 else None  # 2% missing

        data.append({
            'id': i,
            'text': text,
            'label': label,
            'score': score,
            'timestamp': (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat()
        })

    # Add some duplicates
    num_duplicates = int(n_samples * 0.03)  # 3% duplicates
    for _ in range(num_duplicates):
        data.append(random.choice(data).copy())

    random.shuffle(data)

    return data


def example_dataset_registration():
    """Example 1: Dataset registration and loading"""
    print("=" * 70)
    print("Example 1: Dataset Registration and Loading")
    print("=" * 70)

    # Create dataset manager
    manager = DatasetManager(storage_path="./example_datasets")

    # Create mock data
    data = create_mock_classification_dataset(n_samples=1000)

    # Register dataset
    dataset = manager.register_dataset(
        name="sentiment_dataset",
        data=data,
        version="1.0.0",
        metadata={
            'description': 'Sentiment classification dataset',
            'source': 'synthetic',
            'created_by': 'example_script'
        },
        save=True
    )

    print(f"\n✓ Registered dataset: {dataset.name}")
    print(f"  Version: {dataset.version}")
    print(f"  Size: {len(dataset)} samples")
    print(f"  Created: {dataset.created_at}")

    # List all datasets
    print("\nAll Datasets:")
    for ds_info in manager.list_datasets():
        print(f"  - {ds_info['name']} v{ds_info['version']} ({ds_info['size']} samples)")

    # Load dataset
    loaded_dataset = manager.load_dataset("sentiment_dataset")
    print(f"\n✓ Loaded dataset: {loaded_dataset.name} ({len(loaded_dataset)} samples)")

    return manager, dataset


def example_quality_analysis(manager, dataset):
    """Example 2: Dataset quality analysis"""
    print("\n" + "=" * 70)
    print("Example 2: Dataset Quality Analysis")
    print("=" * 70)

    # Analyze quality
    quality_report = manager.analyze_quality(dataset.name)

    print(f"\nQuality Analysis Report for {dataset.name}:")
    print(f"  Total Samples: {quality_report['total_samples']}")
    print(f"  Quality Score: {quality_report['quality_score']:.2f}/100")

    # Completeness
    completeness = quality_report['completeness']
    print(f"\n  Completeness:")
    print(f"    Complete: {completeness['complete']}")
    print(f"    Missing Fields: {completeness['missing_count']}")
    print(f"    Completeness Ratio: {completeness['completeness_ratio']:.2%}")

    # Balance
    balance = quality_report['balance']
    print(f"\n  Class Balance:")
    print(f"    Balanced: {balance['balanced']}")
    print(f"    Number of Classes: {balance['num_classes']}")
    if 'distribution' in balance:
        print(f"    Distribution:")
        for label, info in balance['distribution'].items():
            print(f"      {label}: {info['count']} ({info['percentage']:.1f}%)")

    # Duplicates
    duplicates = quality_report['duplicates']
    print(f"\n  Duplicates:")
    print(f"    Has Duplicates: {duplicates['has_duplicates']}")
    print(f"    Duplicate Count: {duplicates['duplicate_count']}")
    print(f"    Duplicate Ratio: {duplicates['duplicate_ratio']:.2%}")
    print(f"    Unique Samples: {duplicates['unique_count']}")

    # Recommendations
    if quality_report['recommendations']:
        print(f"\n  Recommendations ({len(quality_report['recommendations'])}):")
        for idx, rec in enumerate(quality_report['recommendations'], 1):
            print(f"    {idx}. {rec}")

    return quality_report


def example_dataset_splitting(manager, dataset):
    """Example 3: Dataset splitting"""
    print("\n" + "=" * 70)
    print("Example 3: Dataset Splitting")
    print("=" * 70)

    # Random split
    print("\n1. Random Split (70/15/15):")
    splits = manager.split_dataset(
        name=dataset.name,
        splits={'train': 0.7, 'val': 0.15, 'test': 0.15},
        stratify=False,
        random_seed=42
    )

    for split_name, split_dataset in splits.items():
        print(f"  {split_name}: {len(split_dataset)} samples")

    # Stratified split
    print("\n2. Stratified Split (70/15/15):")
    stratified_splits = manager.split_dataset(
        name=dataset.name,
        splits={'train': 0.7, 'val': 0.15, 'test': 0.15},
        stratify=True,
        random_seed=42
    )

    for split_name, split_dataset in stratified_splits.items():
        # Count labels
        labels = [s['label'] for s in split_dataset.data if isinstance(s, dict)]
        label_dist = {}
        for label in labels:
            label_dist[label] = label_dist.get(label, 0) + 1

        print(f"  {split_name}: {len(split_dataset)} samples")
        for label, count in sorted(label_dist.items()):
            print(f"    {label}: {count} ({count/len(labels)*100:.1f}%)")

    # K-fold split
    print("\n3. K-Fold Cross-Validation (k=5):")
    splitter = DatasetSplitter(random_seed=42)
    k_folds = splitter.k_fold_split(dataset.data, k=5, stratify=True)

    for i, fold in enumerate(k_folds[:3], 1):  # Show first 3 folds
        print(f"  Fold {i}: train={len(fold['train'])}, val={len(fold['val'])}")

    print(f"  ... ({len(k_folds)} total folds)")

    return splits


def example_dataset_sampling(manager, dataset):
    """Example 4: Dataset sampling"""
    print("\n" + "=" * 70)
    print("Example 4: Dataset Sampling")
    print("=" * 70)

    sampler = DatasetSampler(random_seed=42)

    # Random sampling
    print("\n1. Random Sampling (100 samples):")
    random_sample = sampler.sample(dataset.data, n_samples=100, strategy='random')
    print(f"  Sampled: {len(random_sample)} samples")

    # Stratified sampling
    print("\n2. Stratified Sampling (100 samples):")
    stratified_sample = sampler.sample(dataset.data, n_samples=100, strategy='stratified')

    labels = [s['label'] for s in stratified_sample if isinstance(s, dict)]
    label_dist = {}
    for label in labels:
        label_dist[label] = label_dist.get(label, 0) + 1

    print(f"  Sampled: {len(stratified_sample)} samples")
    for label, count in sorted(label_dist.items()):
        print(f"    {label}: {count} ({count/len(labels)*100:.1f}%)")

    # Balanced sampling
    print("\n3. Balanced Sampling (150 samples):")
    balanced_sample = sampler.sample(dataset.data, n_samples=150, strategy='balanced')

    labels = [s['label'] for s in balanced_sample if isinstance(s, dict)]
    label_dist = {}
    for label in labels:
        label_dist[label] = label_dist.get(label, 0) + 1

    print(f"  Sampled: {len(balanced_sample)} samples")
    for label, count in sorted(label_dist.items()):
        print(f"    {label}: {count} ({count/len(labels)*100:.1f}%)")

    # Use sampling through manager
    print("\n4. Manager Sampling:")
    sampled_dataset = manager.sample_dataset(
        name=dataset.name,
        n_samples=200,
        strategy='stratified',
        random_seed=42
    )

    print(f"  Created sampled dataset: {sampled_dataset.name}")
    print(f"  Size: {len(sampled_dataset)} samples")

    return sampled_dataset


def example_version_control():
    """Example 5: Dataset version control"""
    print("\n" + "=" * 70)
    print("Example 5: Dataset Version Control")
    print("=" * 70)

    # Create version control
    version_control = VersionControl(storage_path="./example_versions")

    # Create initial version
    data_v1 = create_mock_classification_dataset(n_samples=500)

    v1 = version_control.create_version(
        dataset_name="sentiment_v2",
        data=data_v1,
        version="1.0.0",
        metadata={'description': 'Initial release'},
        changes="Initial dataset creation",
        created_by="data_team"
    )

    print(f"\n✓ Created version: {v1.version}")
    print(f"  Dataset: {v1.dataset_name}")
    print(f"  Size: {v1.size} samples")
    print(f"  Checksum: {v1.checksum[:16]}...")

    # Create second version (with more data)
    data_v2 = create_mock_classification_dataset(n_samples=800)

    v2 = version_control.create_version(
        dataset_name="sentiment_v2",
        data=data_v2,
        metadata={'description': 'Expanded dataset'},
        changes="Added 300 new samples",
        created_by="data_team"
    )

    print(f"\n✓ Created version: {v2.version}")
    print(f"  Size: {v2.size} samples")
    print(f"  Parent: {v2.parent_version}")
    print(f"  Changes: {v2.changes}")

    # List version history
    print(f"\nVersion History for {v1.dataset_name}:")
    history = version_control.get_history("sentiment_v2")

    for entry in history:
        print(f"  v{entry['version']}")
        print(f"    Size: {entry['size']}")
        print(f"    Checksum: {entry['checksum']}")
        print(f"    Changes: {entry['changes']}")
        print(f"    Created: {entry['created_at']}")

    # Compare versions
    print(f"\nVersion Diff (v1.0.0 -> v1.0.1):")
    diff = version_control.diff("sentiment_v2", "1.0.0", "1.0.1")

    print(f"  Size change: {diff['size_change']:+d} ({diff['size_change_pct']:+.1f}%)")
    print(f"  Checksum changed: {diff['checksum_changed']}")
    print(f"  Changes: {diff['changes_description']}")

    # Tag a version
    version_control.tag_version(
        dataset_name="sentiment_v2",
        version="1.0.1",
        tag="production",
        message="Promoted to production"
    )

    print(f"\n✓ Tagged v1.0.1 as 'production'")

    # Get tagged version
    prod_version = version_control.get_tagged_version("sentiment_v2", "production")
    print(f"  Production version: {prod_version.version}")

    # Validate integrity
    print(f"\nIntegrity Check:")
    is_valid = version_control.validate_integrity("sentiment_v2", data_v2, "1.0.1")
    print(f"  Data integrity: {'✓ VALID' if is_valid else '✗ INVALID'}")

    return version_control


def example_comprehensive_workflow():
    """Example 6: Comprehensive dataset management workflow"""
    print("\n" + "=" * 70)
    print("Example 6: Comprehensive Workflow")
    print("=" * 70)

    print("\nScenario: Managing an evolving ML dataset")

    # Step 1: Create initial dataset
    print("\n📊 Step 1: Create initial dataset")
    manager = DatasetManager(storage_path="./workflow_datasets")
    data = create_mock_classification_dataset(n_samples=1000, imbalance_ratio=3.0)

    dataset = manager.register_dataset(
        name="production_dataset",
        data=data,
        version="1.0.0",
        metadata={'stage': 'development'},
        save=True
    )
    print(f"  ✓ Created dataset with {len(dataset)} samples")

    # Step 2: Analyze quality
    print("\n🔍 Step 2: Analyze quality")
    quality = manager.analyze_quality(dataset.name)
    print(f"  Quality Score: {quality['quality_score']:.2f}/100")

    if quality['recommendations']:
        print(f"  Issues found: {len(quality['recommendations'])}")
        for rec in quality['recommendations'][:2]:
            print(f"    - {rec}")

    # Step 3: Split dataset
    print("\n✂️ Step 3: Split into train/val/test")
    splits = manager.split_dataset(
        name=dataset.name,
        splits={'train': 0.7, 'val': 0.15, 'test': 0.15},
        stratify=True
    )

    for split_name, split_ds in splits.items():
        print(f"  {split_name}: {len(split_ds)} samples")

    # Step 4: Create balanced sample for experiments
    print("\n⚖️ Step 4: Create balanced sample for quick experiments")
    sampled = manager.sample_dataset(
        name=dataset.name,
        n_samples=300,
        strategy='balanced'
    )
    print(f"  ✓ Created balanced sample: {sampled.name} ({len(sampled)} samples)")

    # Step 5: Version control
    print("\n📝 Step 5: Track versions")
    vc = VersionControl(storage_path="./workflow_versions")

    v1 = vc.create_version(
        dataset_name="production_dataset",
        data=dataset.data,
        version="1.0.0",
        changes="Initial production dataset",
        created_by="ml_engineer"
    )

    vc.tag_version("production_dataset", "1.0.0", "baseline", "Baseline version for comparison")

    print(f"  ✓ Version {v1.version} created and tagged as 'baseline'")

    # Summary
    print("\n" + "=" * 70)
    print("Workflow Summary")
    print("=" * 70)
    print(f"✓ Dataset: {dataset.name} ({len(dataset)} samples)")
    print(f"✓ Quality Score: {quality['quality_score']:.2f}/100")
    print(f"✓ Splits: train={len(splits['train'])}, val={len(splits['val'])}, test={len(splits['test'])}")
    print(f"✓ Sample: {sampled.name} ({len(sampled)} samples)")
    print(f"✓ Version: {v1.version} (tagged: baseline)")


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("AEVA Dataset Management Examples")
    print("=" * 70)

    # Run examples
    manager, dataset = example_dataset_registration()
    quality_report = example_quality_analysis(manager, dataset)
    splits = example_dataset_splitting(manager, dataset)
    sampled = example_dataset_sampling(manager, dataset)
    version_control = example_version_control()
    example_comprehensive_workflow()

    print("\n" + "=" * 70)
    print("All Examples Completed!")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  ✓ Dataset registration and loading")
    print("  ✓ Quality analysis (completeness, balance, duplicates)")
    print("  ✓ Dataset splitting (random, stratified, k-fold)")
    print("  ✓ Dataset sampling (random, stratified, balanced)")
    print("  ✓ Version control (tracking, tagging, diff)")
    print("  ✓ Comprehensive workflow integration")


if __name__ == '__main__':
    main()
