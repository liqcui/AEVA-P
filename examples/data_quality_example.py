"""
Data Quality Framework Examples

Demonstrates features of the Data Quality framework including:
- Quality dimensions (Completeness, Uniqueness, Validity, etc.)
- Outlier detection methods
- Distribution analysis
- Comprehensive quality reporting

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import numpy as np
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aeva.data_quality import QualityMetrics, OutlierMethod


def print_section(title: str):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def example_completeness():
    """Example 1: Completeness Analysis"""
    print_section("Example 1: Completeness Analysis")

    # Create sample DataFrame with missing values
    data = {
        'customer_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'name': ['Alice', 'Bob', None, 'David', 'Eve', 'Frank', None, 'Hannah', 'Ivan', 'Jane'],
        'email': ['a@ex.com', 'b@ex.com', 'c@ex.com', None, 'e@ex.com', None, 'g@ex.com', None, 'i@ex.com', 'j@ex.com'],
        'age': [25, 30, None, 35, 28, None, 42, 31, None, 27],
        'purchase_amount': [100, 200, 150, None, 300, 250, 180, None, 220, 190]
    }
    df = pd.DataFrame(data)

    print("\nScenario: Analyzing customer data completeness")
    print(f"\nDataset shape: {df.shape}")
    print(f"\nMissing values per column:")
    print(df.isnull().sum())

    # Check completeness using static method
    print("\n📊 Completeness Scores:")
    for col in df.columns:
        completeness_pct = QualityMetrics.completeness(df[col])
        missing_count = df[col].isnull().sum()
        print(f"  {col:20s}: {completeness_pct:.1f}% ({missing_count} missing)")

    # Overall completeness
    overall_missing = df.isnull().sum().sum()
    total_cells = df.shape[0] * df.shape[1]
    overall_completeness = ((total_cells - overall_missing) / total_cells) * 100

    print(f"\n✓ Overall Dataset Completeness: {overall_completeness:.1f}%")


def example_uniqueness():
    """Example 2: Uniqueness and Duplicate Detection"""
    print_section("Example 2: Uniqueness and Duplicate Detection")

    # Create dataset with duplicates
    user_ids = pd.Series([101, 102, 103, 101, 105, 102, 107, 108, 103, 101])
    product_codes = pd.Series(['A1', 'B2', 'C3', 'A1', 'E5', 'B2', 'G7', 'H8', 'C3', 'J10'])

    print("\nScenario: Detecting duplicate transactions")
    print(f"\nDataset: {len(user_ids)} transactions")

    # Check uniqueness
    print("\n📊 Uniqueness Scores:")

    user_uniqueness = QualityMetrics.uniqueness(user_ids)
    user_duplicates = len(user_ids) - user_ids.nunique()
    print(f"  user_id:      {user_uniqueness:.1f}% ({user_duplicates} duplicates)")

    product_uniqueness = QualityMetrics.uniqueness(product_codes)
    product_duplicates = len(product_codes) - product_codes.nunique()
    print(f"  product_code: {product_uniqueness:.1f}% ({product_duplicates} duplicates)")

    # Show duplicate user_ids
    print("\n🔍 Duplicate Analysis for user_id:")
    duplicates_mask = user_ids.duplicated(keep=False)
    duplicate_values = user_ids[duplicates_mask].unique()
    print(f"  Duplicate user_ids: {sorted(duplicate_values.tolist())}")
    print(f"  Rows with duplicates: {duplicates_mask.sum()}")


def example_validity():
    """Example 3: Validity Checks"""
    print_section("Example 3: Validity Checks")

    # Create dataset with invalid values
    ages = np.array([25, 30, -5, 150, 35, 28, 200, 40, 22, 27])
    scores = np.array([85, 92, 78, 105, 88, 95, -10, 91, 87, 82])

    print("\nScenario: Validating user data ranges")

    # Check age validity (0-120)
    print("\n📊 Age Validity (valid range: 0-120):")
    age_validity = QualityMetrics.validity(ages, min_value=0, max_value=120)
    invalid_ages = ages[(ages < 0) | (ages > 120)]
    print(f"  Validity Score: {age_validity:.1f}%")
    print(f"  Invalid count: {len(invalid_ages)}")
    if len(invalid_ages) > 0:
        print(f"  Invalid ages: {invalid_ages.tolist()}")

    # Check score validity (0-100)
    print("\n📊 Score Validity (valid range: 0-100):")
    score_validity = QualityMetrics.validity(scores, min_value=0, max_value=100)
    invalid_scores = scores[(scores < 0) | (scores > 100)]
    print(f"  Validity Score: {score_validity:.1f}%")
    print(f"  Invalid count: {len(invalid_scores)}")
    if len(invalid_scores) > 0:
        print(f"  Invalid scores: {invalid_scores.tolist()}")


def example_outlier_detection():
    """Example 4: Outlier Detection Methods"""
    print_section("Example 4: Outlier Detection Methods")

    np.random.seed(42)

    # Generate data with outliers
    normal_data = np.random.normal(100, 15, 95)
    outliers = np.array([200, 250, -50, 280, 300])
    data = np.concatenate([normal_data, outliers])
    np.random.shuffle(data)

    # Create QualityMetrics instance
    metrics = QualityMetrics(data)

    print("\nScenario: Detecting outliers in sales data")
    print(f"\nDataset: {len(data)} samples")
    print(f"Mean: {data.mean():.2f}, Std: {data.std():.2f}")

    # Method 1: IQR Method
    print("\n1️⃣ IQR Method:")
    result_iqr = metrics.detect_outliers(method=OutlierMethod.IQR)
    print(f"  Outliers detected: {result_iqr.outlier_count}")
    print(f"  Outlier percentage: {result_iqr.outlier_percentage:.1f}%")

    # Method 2: Z-Score
    print("\n2️⃣ Z-Score Method:")
    result_z = metrics.detect_outliers(method=OutlierMethod.Z_SCORE, threshold=3.0)
    print(f"  Outliers detected: {result_z.outlier_count}")
    print(f"  Outlier percentage: {result_z.outlier_percentage:.1f}%")

    # Method 3: Modified Z-Score
    print("\n3️⃣ Modified Z-Score (MAD) Method:")
    result_mad = metrics.detect_outliers(method=OutlierMethod.MODIFIED_Z_SCORE, threshold=3.5)
    print(f"  Outliers detected: {result_mad.outlier_count}")
    print(f"  Outlier percentage: {result_mad.outlier_percentage:.1f}%")

    # Show comparison
    print("\n📊 Method Comparison:")
    print(f"  IQR:            {result_iqr.outlier_count} outliers")
    print(f"  Z-Score:        {result_z.outlier_count} outliers")
    print(f"  Modified Z:     {result_mad.outlier_count} outliers")


def example_distribution_analysis():
    """Example 5: Distribution Analysis"""
    print_section("Example 5: Distribution Analysis")

    np.random.seed(42)

    # Create different distributions
    distributions = {
        "Normal": np.random.normal(100, 15, 1000),
        "Skewed": np.random.exponential(2, 1000),
        "Uniform": np.random.uniform(0, 100, 1000)
    }

    print("\nScenario: Analyzing different data distributions")

    for name, data in distributions.items():
        print(f"\n📊 {name} Distribution:")

        metrics = QualityMetrics(data)
        analysis = metrics.analyze_distribution()

        print(f"  Mean:     {analysis.mean:.2f}")
        print(f"  Median:   {analysis.median:.2f}")
        print(f"  Std Dev:  {analysis.std:.2f}")
        print(f"  Skewness: {analysis.skewness:.2f}")
        print(f"  Kurtosis: {analysis.kurtosis:.2f}")
        print(f"  Min:      {analysis.min:.2f}")
        print(f"  Max:      {analysis.max:.2f}")

        # Normality test
        if analysis.normality_test_p_value:
            is_normal = analysis.normality_test_p_value > 0.05
            if is_normal:
                print(f"  ✓ Passes normality test (p={analysis.normality_test_p_value:.4f})")
            else:
                print(f"  ✗ Fails normality test (p={analysis.normality_test_p_value:.4f})")


def example_comprehensive_report():
    """Example 6: Comprehensive Quality Report"""
    print_section("Example 6: Comprehensive Data Quality Report")

    np.random.seed(42)

    # Create realistic dataset
    n_samples = 200
    data = {
        'user_id': range(1, n_samples + 1),
        'age': np.random.randint(18, 80, n_samples),
        'income': np.random.normal(50000, 15000, n_samples),
        'credit_score': np.random.normal(700, 100, n_samples)
    }

    df = pd.DataFrame(data)

    # Add some quality issues
    # Missing values
    df.loc[np.random.choice(df.index, 10, replace=False), 'age'] = np.nan
    df.loc[np.random.choice(df.index, 5, replace=False), 'income'] = np.nan

    # Outliers
    df.loc[df.index[-3:], 'income'] = [200000, 250000, 300000]

    print("\nScenario: Generating comprehensive quality report for financial dataset")
    print(f"\nDataset: {len(df)} records, {len(df.columns)} columns")

    # Create quality metrics instance
    metrics = QualityMetrics(df)

    # Generate report
    report = metrics.generate_quality_report()

    print("\n" + "=" * 70)
    print("  COMPREHENSIVE DATA QUALITY REPORT")
    print("=" * 70)

    print(f"\n📊 Overall Quality Score: {report.overall_score:.1f}%\n")

    # Dimension scores
    if report.dimension_scores:
        print("Quality Dimensions:")
        for dim, score in report.dimension_scores.items():
            stars = "★" * int(score.score / 20) + "☆" * (5 - int(score.score / 20))
            print(f"  {dim.value:15s}: {score.score:.1f}% {stars}")

    # Summary statistics
    print(f"\n📈 Summary Statistics:")
    print(f"  Total Records:    {len(df)}")
    print(f"  Total Columns:    {len(df.columns)}")
    print(f"  Missing Values:   {df.isnull().sum().sum()}")

    # Distribution analysis
    if report.distribution_analysis:
        print(f"\n📊 Distribution Analysis (income column):")
        dist = report.distribution_analysis
        print(f"  Mean:   {dist.mean:.2f}")
        print(f"  Median: {dist.median:.2f}")
        print(f"  Std:    {dist.std:.2f}")

    # Outlier analysis
    if report.outlier_analysis:
        print(f"\n🔍 Outlier Analysis:")
        out = report.outlier_analysis
        print(f"  Method:     {out.method.value}")
        print(f"  Count:      {out.outlier_count}")
        print(f"  Percentage: {out.outlier_percentage:.1f}%")

    print(f"\n✓ Quality report generated successfully!")


def main():
    """Run all examples"""
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 12 + "AEVA Data Quality Framework Examples" + " " * 17 + "║")
    print("╚" + "=" * 68 + "╝")

    examples = [
        example_completeness,
        example_uniqueness,
        example_validity,
        example_outlier_detection,
        example_distribution_analysis,
        example_comprehensive_report
    ]

    for i, example in enumerate(examples, 1):
        try:
            example()
        except Exception as e:
            print(f"\n❌ Error in example {i}: {str(e)}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 70)
    print("All examples completed!")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  ✓ Completeness Analysis")
    print("  ✓ Uniqueness Detection")
    print("  ✓ Validity Checks")
    print("  ✓ Outlier Detection (3 methods)")
    print("  ✓ Distribution Analysis")
    print("  ✓ Comprehensive Reporting")


if __name__ == "__main__":
    main()
