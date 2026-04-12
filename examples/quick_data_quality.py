"""
Quick Data Quality Test - Data Profiling Demo
快速验证数据质量模块的核心功能
"""
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
import sys
sys.path.insert(0, '.')

from aeva.data_quality import DataProfiler, QualityMetrics

print("=" * 70)
print("AEVA Data Quality Module - Quick Test")
print("=" * 70)

# Load data
print("\n1. Loading data...")
data = load_breast_cancer()
X = data.data
feature_names = data.feature_names.tolist()
df = pd.DataFrame(X, columns=feature_names)
print(f"   ✓ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# Test DataProfiler
print("\n2. Testing Data Profiler...")
try:
    profiler = DataProfiler()
    profile = profiler.profile(df)

    print(f"   ✓ Profile generated")
    print(f"   ✓ Samples: {profile.n_samples}")
    print(f"   ✓ Features: {profile.n_features}")
    print(f"   ✓ Quality Score: {profile.quality_score:.1f}/100")
    print(f"   ✓ Missing %: {profile.missing_percentage:.2f}%")
    print(f"   ✓ Duplicate %: {profile.duplicate_percentage:.2f}%")
except Exception as e:
    print(f"   ✗ Profiler test failed: {e}")

# Test with problematic data
print("\n3. Testing with problematic data...")
try:
    # Create dataset with issues
    df_dirty = df.copy()

    # Add missing values
    df_dirty.iloc[0:10, 0] = np.nan

    # Add duplicates
    df_dirty = pd.concat([df_dirty, df_dirty.iloc[0:5]], ignore_index=True)

    profile_dirty = profiler.profile(df_dirty)

    print(f"   ✓ Dirty data profile generated")
    print(f"   ✓ Quality Score: {profile_dirty.quality_score:.1f}/100")
    print(f"   ✓ Missing %: {profile_dirty.missing_percentage:.2f}%")
    print(f"   ✓ Duplicate %: {profile_dirty.duplicate_percentage:.2f}%")
except Exception as e:
    print(f"   ✗ Dirty data test failed: {e}")

# Test QualityMetrics
print("\n4. Testing Quality Metrics...")
try:
    metrics = QualityMetrics()

    # Completeness
    completeness = metrics.completeness(df)
    print(f"   ✓ Completeness: {completeness:.2%}")

    # Uniqueness
    uniqueness = metrics.uniqueness(df)
    print(f"   ✓ Uniqueness: {uniqueness:.2%}")

    # Validity (all numeric, should be 100%)
    def is_numeric(x):
        return isinstance(x, (int, float)) and not np.isnan(x)

    validity = metrics.validity(df, is_numeric)
    print(f"   ✓ Validity: {validity:.2%}")

    # Consistency
    consistency = metrics.consistency(df.iloc[:, 0])  # Check first column
    print(f"   ✓ Consistency: {consistency:.2%}")
except Exception as e:
    print(f"   ✗ Metrics test failed: {e}")

# Test Feature Quality
print("\n5. Testing Feature-level Quality...")
try:
    feature_profile = profiler.profile_features(df.iloc[:, :5])  # First 5 features

    print(f"   ✓ Feature profiles generated: {len(feature_profile)}")

    for fname, fprofile in list(feature_profile.items())[:3]:
        print(f"   ✓ {fname}: missing={fprofile['missing_count']}, "
              f"unique={fprofile['unique_count']}")
except Exception as e:
    print(f"   ✗ Feature quality test failed: {e}")

# Test Quality Report
print("\n6. Testing Quality Report Generation...")
try:
    report = profiler.generate_report(df)

    print(f"   ✓ Report generated ({len(report)} characters)")

    # Save to file
    with open('/tmp/data_quality_report.txt', 'w') as f:
        f.write(report)
    print(f"   ✓ Saved to /tmp/data_quality_report.txt")
except Exception as e:
    print(f"   ✗ Report generation failed: {e}")

print("\n" + "=" * 70)
print("✅ Data Quality Module Test Complete!")
print("=" * 70)
