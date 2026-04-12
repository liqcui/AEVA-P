"""
Data Quality Framework Examples

Demonstrates all features of the enhanced Data Quality framework including:
- 6 quality dimensions (Completeness, Uniqueness, Validity, Accuracy, Consistency, Timeliness)
- Outlier detection (IQR, Z-score, Modified Z-score)
- Distribution analysis and normality testing
- Comprehensive quality reporting
- Pandas DataFrame and NumPy array support

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import numpy as np
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aeva.data_quality import QualityMetrics, QualityDimension, OutlierMethod


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

    metrics = QualityMetrics()

    print("\nScenario: Analyzing customer data completeness")
    print(f"\nDataset shape: {df.shape}")
    print(f"\nMissing values per column:")
    print(df.isnull().sum())

    # Check completeness for each column
    print("\n📊 Completeness Scores:")
    for col in df.columns:
        score = metrics.check_completeness(df[col])
        print(f"  {col:20s}: {score.score:.1f}% ({score.details.get('missing_count', 0)} missing)")

    # Overall completeness
    overall_missing = df.isnull().sum().sum()
    total_cells = df.shape[0] * df.shape[1]
    overall_completeness = ((total_cells - overall_missing) / total_cells) * 100

    print(f"\n✓ Overall Dataset Completeness: {overall_completeness:.1f}%")


def example_uniqueness():
    """Example 2: Uniqueness and Duplicate Detection"""
    print_section("Example 2: Uniqueness and Duplicate Detection")

    # Create dataset with duplicates
    data = {
        'transaction_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'user_id': [101, 102, 103, 101, 105, 102, 107, 108, 103, 101],  # Duplicates
        'product_code': ['A1', 'B2', 'C3', 'A1', 'E5', 'B2', 'G7', 'H8', 'C3', 'J10'],
        'amount': [50, 75, 100, 50, 125, 75, 150, 175, 100, 200]
    }
    df = pd.DataFrame(data)

    metrics = QualityMetrics()

    print("\nScenario: Detecting duplicate transactions")
    print(f"\nDataset: {len(df)} transactions")

    # Check uniqueness for each column
    print("\n📊 Uniqueness Scores:")
    for col in df.columns:
        score = metrics.check_uniqueness(df[col])
        print(f"  {col:20s}: {score.score:.1f}% ({score.details.get('duplicate_count', 0)} duplicates)")

    # Show duplicate user_ids
    print("\n🔍 Duplicate Analysis for user_id:")
    duplicates = df[df.duplicated(subset=['user_id'], keep=False)]
    print(f"  Duplicate user_ids found: {duplicates['user_id'].nunique()}")
    print(f"  Rows with duplicates: {len(duplicates)}")
    print(f"\n  Duplicate user_ids: {sorted(duplicates['user_id'].unique().tolist())}")


def example_validity():
    """Example 3: Validity Checks"""
    print_section("Example 3: Validity Checks")

    # Create dataset with invalid values
    data = {
        'age': [25, 30, -5, 150, 35, 28, 200, 40, 22, 27],  # Invalid: negative and >120
        'score': [85, 92, 78, 105, 88, 95, -10, 91, 87, 82],  # Invalid: >100 and <0
        'email': ['valid@test.com', 'invalid.email', 'another@valid.com', 'bad@',
                  'good@domain.org', 'notanemail', 'ok@test.co', '@nodomain.com',
                  'fine@example.com', 'wrong@.com']
    }
    df = pd.DataFrame(data)

    metrics = QualityMetrics()

    print("\nScenario: Validating user data ranges and formats")

    # Check age validity (0-120)
    print("\n📊 Age Validity (valid range: 0-120):")
    age_score = metrics.check_validity(df['age'], min_value=0, max_value=120)
    print(f"  Validity Score: {age_score.score:.1f}%")
    print(f"  Invalid values: {age_score.details.get('invalid_count', 0)}")

    invalid_ages = df[(df['age'] < 0) | (df['age'] > 120)]['age'].tolist()
    if invalid_ages:
        print(f"  Invalid ages found: {invalid_ages}")

    # Check score validity (0-100)
    print("\n📊 Score Validity (valid range: 0-100):")
    score_score = metrics.check_validity(df['score'], min_value=0, max_value=100)
    print(f"  Validity Score: {score_score.score:.1f}%")
    print(f"  Invalid values: {score_score.details.get('invalid_count', 0)}")

    invalid_scores = df[(df['score'] < 0) | (df['score'] > 100)]['score'].tolist()
    if invalid_scores:
        print(f"  Invalid scores found: {invalid_scores}")

    # Check email validity (pattern)
    print("\n📊 Email Validity (pattern: xxx@yyy.zzz):")
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    email_score = metrics.check_validity(df['email'], pattern=email_pattern)
    print(f"  Validity Score: {email_score.score:.1f}%")
    print(f"  Invalid emails: {email_score.details.get('invalid_count', 0)}")


def example_outlier_detection():
    """Example 4: Outlier Detection Methods"""
    print_section("Example 4: Outlier Detection Methods")

    np.random.seed(42)

    # Generate data with outliers
    normal_data = np.random.normal(100, 15, 95)
    outliers = np.array([200, 250, -50, 280, 300])  # Clear outliers
    data = np.concatenate([normal_data, outliers])
    np.random.shuffle(data)

    metrics = QualityMetrics()

    print("\nScenario: Detecting outliers in sales data")
    print(f"\nDataset: {len(data)} samples")
    print(f"Mean: {data.mean():.2f}, Std: {data.std():.2f}")

    # Method 1: IQR Method
    print("\n1️⃣ IQR Method:")
    result_iqr = metrics.detect_outliers(data, method=OutlierMethod.IQR)
    print(f"  Outliers detected: {result_iqr.outlier_count}")
    print(f"  Outlier percentage: {result_iqr.outlier_percentage:.1f}%")
    print(f"  Outlier indices: {result_iqr.outlier_indices[:5]}...")  # Show first 5

    # Method 2: Z-Score
    print("\n2️⃣ Z-Score Method:")
    result_z = metrics.detect_outliers(data, method=OutlierMethod.ZSCORE, threshold=3.0)
    print(f"  Outliers detected: {result_z.outlier_count}")
    print(f"  Outlier percentage: {result_z.outlier_percentage:.1f}%")

    # Method 3: Modified Z-Score (MAD)
    print("\n3️⃣ Modified Z-Score (MAD) Method:")
    result_mad = metrics.detect_outliers(data, method=OutlierMethod.MODIFIED_ZSCORE, threshold=3.5)
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
        "Uniform": np.random.uniform(0, 100, 1000),
        "Bimodal": np.concatenate([
            np.random.normal(50, 10, 500),
            np.random.normal(150, 10, 500)
        ])
    }

    metrics = QualityMetrics()

    print("\nScenario: Analyzing different data distributions")

    for name, data in distributions.items():
        print(f"\n📊 {name} Distribution:")

        analysis = metrics.analyze_distribution(data)

        print(f"  Mean:     {analysis.mean:.2f}")
        print(f"  Median:   {analysis.median:.2f}")
        print(f"  Std Dev:  {analysis.std:.2f}")
        print(f"  Skewness: {analysis.skewness:.2f}")
        print(f"  Kurtosis: {analysis.kurtosis:.2f}")
        print(f"  Min:      {analysis.min:.2f}")
        print(f"  Max:      {analysis.max:.2f}")
        print(f"  Range:    {analysis.range:.2f}")

        # Normality test
        if analysis.is_normal:
            print(f"  ✓ Passes normality test (p={analysis.normality_p_value:.4f})")
        else:
            print(f"  ✗ Fails normality test (p={analysis.normality_p_value:.4f})")

        print(f"  Distribution type: {analysis.distribution_type}")


def example_consistency_checks():
    """Example 6: Consistency Checks"""
    print_section("Example 6: Consistency Checks")

    # Create dataset with consistency issues
    data = {
        'order_date': pd.date_range('2024-01-01', periods=10, freq='D'),
        'ship_date': pd.date_range('2024-01-03', periods=10, freq='D'),
        'min_age': [18, 21, 25, 30, 18, 21, 25, 30, 18, 21],
        'max_age': [65, 70, 55, 75, 65, 70, 75, 80, 65, 70],
        'country': ['USA', 'USA', 'UK', 'UK', 'USA', 'Canada', 'USA', 'UK', 'Canada', 'USA'],
        'currency': ['USD', 'USD', 'GBP', 'GBP', 'EUR', 'CAD', 'USD', 'EUR', 'CAD', 'USD']
    }
    df = pd.DataFrame(data)

    metrics = QualityMetrics()

    print("\nScenario: Checking data consistency rules")

    # Check if ship_date >= order_date
    print("\n1️⃣ Temporal Consistency (ship_date >= order_date):")
    valid_dates = (df['ship_date'] >= df['order_date']).all()
    consistency_pct = (df['ship_date'] >= df['order_date']).mean() * 100
    print(f"  Consistency Score: {consistency_pct:.1f}%")

    if not valid_dates:
        violations = df[df['ship_date'] < df['order_date']]
        print(f"  ✗ Found {len(violations)} violations")
    else:
        print(f"  ✓ All dates are consistent")

    # Check if max_age > min_age
    print("\n2️⃣ Logical Consistency (max_age > min_age):")
    valid_ages = (df['max_age'] > df['min_age']).all()
    age_consistency_pct = (df['max_age'] > df['min_age']).mean() * 100
    print(f"  Consistency Score: {age_consistency_pct:.1f}%")

    if not valid_ages:
        violations = df[df['max_age'] <= df['min_age']]
        print(f"  ✗ Found {len(violations)} violations")
    else:
        print(f"  ✓ All age ranges are valid")

    # Check country-currency mapping consistency
    print("\n3️⃣ Cross-Field Consistency (country-currency mapping):")
    expected_mapping = {'USA': 'USD', 'UK': 'GBP', 'Canada': 'CAD'}

    consistent = []
    for _, row in df.iterrows():
        if row['country'] in expected_mapping:
            consistent.append(row['currency'] == expected_mapping[row['country']])
        else:
            consistent.append(True)  # Unknown country, can't validate

    consistency_score = (sum(consistent) / len(consistent)) * 100
    print(f"  Consistency Score: {consistency_score:.1f}%")

    inconsistent_rows = df[[not c for c in consistent]]
    if len(inconsistent_rows) > 0:
        print(f"  ✗ Found {len(inconsistent_rows)} inconsistent mappings")
        print(f"  Inconsistencies: {list(zip(inconsistent_rows['country'], inconsistent_rows['currency']))}")


def example_comprehensive_report():
    """Example 7: Comprehensive Quality Report"""
    print_section("Example 7: Comprehensive Data Quality Report")

    np.random.seed(42)

    # Create realistic dataset
    n_samples = 200
    data = {
        'user_id': range(1, n_samples + 1),
        'age': np.random.randint(18, 80, n_samples),
        'income': np.random.normal(50000, 15000, n_samples),
        'credit_score': np.random.normal(700, 100, n_samples),
        'account_balance': np.random.normal(5000, 2000, n_samples)
    }

    # Add some quality issues
    df = pd.DataFrame(data)

    # Add missing values
    df.loc[np.random.choice(df.index, 10), 'age'] = np.nan
    df.loc[np.random.choice(df.index, 5), 'income'] = np.nan

    # Add duplicates
    df = pd.concat([df, df.iloc[:5]], ignore_index=True)

    # Add outliers
    df.loc[df.index[-3:], 'income'] = [200000, 250000, 300000]

    metrics = QualityMetrics()

    print("\nScenario: Generating comprehensive quality report for financial dataset")
    print(f"\nDataset: {len(df)} records, {len(df.columns)} columns")

    # Generate comprehensive report
    report = metrics.generate_quality_report(df)

    print("\n" + "=" * 70)
    print("  COMPREHENSIVE DATA QUALITY REPORT")
    print("=" * 70)

    print(f"\n📊 Overall Quality Score: {report.overall_score:.1f}%\n")

    # Dimension scores
    print("Quality Dimensions:")
    for dim, score in report.dimension_scores.items():
        stars = "★" * int(score / 20) + "☆" * (5 - int(score / 20))
        print(f"  {dim.value:15s}: {score:.1f}% {stars}")

    # Column-level metrics
    print(f"\n📋 Column-Level Metrics:")
    print(f"  {'Column':<20} {'Completeness':<15} {'Uniqueness':<15} {'Outliers':<15}")
    print(f"  {'-'*20} {'-'*15} {'-'*15} {'-'*15}")

    for col in df.select_dtypes(include=[np.number]).columns:
        completeness = metrics.check_completeness(df[col])
        uniqueness = metrics.check_uniqueness(df[col])
        outliers = metrics.detect_outliers(df[col].dropna())

        print(f"  {col:<20} {completeness.score:>6.1f}%        "
              f"{uniqueness.score:>6.1f}%        "
              f"{outliers.outlier_count:>3} ({outliers.outlier_percentage:.1f}%)")

    # Summary statistics
    print(f"\n📈 Summary Statistics:")
    print(f"  Total Records:    {len(df)}")
    print(f"  Total Columns:    {len(df.columns)}")
    print(f"  Missing Values:   {df.isnull().sum().sum()}")
    print(f"  Duplicate Rows:   {df.duplicated().sum()}")

    # Recommendations
    print(f"\n💡 Recommendations:")
    recommendations = []

    # Check completeness
    missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    if missing_pct > 5:
        recommendations.append(f"Address {missing_pct:.1f}% missing values")

    # Check duplicates
    dup_pct = (df.duplicated().sum() / len(df)) * 100
    if dup_pct > 0:
        recommendations.append(f"Remove {df.duplicated().sum()} duplicate records ({dup_pct:.1f}%)")

    # Check outliers
    for col in df.select_dtypes(include=[np.number]).columns:
        outliers = metrics.detect_outliers(df[col].dropna())
        if outliers.outlier_percentage > 5:
            recommendations.append(f"Investigate {outliers.outlier_count} outliers in '{col}'")

    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")

    if not recommendations:
        print(f"  ✓ Data quality is good! No major issues detected.")


def example_timeliness_analysis():
    """Example 8: Timeliness Analysis"""
    print_section("Example 8: Timeliness Analysis")

    # Create time-series data
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    data = {
        'date': dates,
        'value': np.random.normal(100, 15, 100),
        'updated_at': dates + pd.Timedelta(days=1)
    }
    df = pd.DataFrame(data)

    # Add some old records
    df.loc[df.index[-10:], 'updated_at'] = pd.Timestamp('2023-01-01')

    metrics = QualityMetrics()

    print("\nScenario: Analyzing data timeliness")

    # Check recency
    current_date = pd.Timestamp.now()
    days_old = (current_date - df['updated_at']).dt.days

    print(f"\n📅 Timeliness Metrics:")
    print(f"  Most recent update:  {df['updated_at'].max()}")
    print(f"  Oldest update:       {df['updated_at'].min()}")
    print(f"  Average age (days):  {days_old.mean():.1f}")

    # Calculate timeliness score (fresh data = 100%, old data = lower score)
    threshold_days = 30
    timely_records = (days_old <= threshold_days).sum()
    timeliness_score = (timely_records / len(df)) * 100

    print(f"\n  Timeliness Score (< {threshold_days} days): {timeliness_score:.1f}%")
    print(f"  Fresh records:  {timely_records}")
    print(f"  Stale records:  {len(df) - timely_records}")

    if timeliness_score < 90:
        print(f"\n  ⚠️  Warning: {len(df) - timely_records} records are older than {threshold_days} days")


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
        example_consistency_checks,
        example_comprehensive_report,
        example_timeliness_analysis
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
    print("  ✓ 6 Quality Dimensions")
    print("  ✓ 3 Outlier Detection Methods")
    print("  ✓ Distribution Analysis")
    print("  ✓ Consistency Checks")
    print("  ✓ Timeliness Metrics")
    print("  ✓ Comprehensive Reporting")


if __name__ == "__main__":
    main()
