"""
数据质量模块单元测试
"""
import pytest
import numpy as np
import pandas as pd
from aeva.data_quality import DataProfiler, QualityMetrics


class TestDataProfiler:
    """数据画像器测试"""

    def test_initialization(self):
        """测试初始化"""
        profiler = DataProfiler()
        assert profiler is not None

    def test_profile_clean_data(self, sample_dataframe):
        """测试分析清洁数据"""
        profiler = DataProfiler()
        profile = profiler.profile(sample_dataframe)

        assert profile is not None
        assert profile.n_samples == len(sample_dataframe)
        assert profile.n_features == len(sample_dataframe.columns)
        assert profile.quality_score == 100.0  # 完美数据

    def test_profile_with_missing_data(self):
        """测试含缺失值的数据"""
        df = pd.DataFrame({
            'a': [1, 2, np.nan, 4],
            'b': [5, np.nan, 7, 8],
            'c': [9, 10, 11, 12]
        })

        profiler = DataProfiler()
        profile = profiler.profile(df)

        assert profile.n_samples == 4
        assert profile.n_features == 3
        assert profile.quality_score < 100.0  # 有缺失值

    def test_profile_with_duplicates(self):
        """测试含重复值的数据"""
        df = pd.DataFrame({
            'a': [1, 1, 2, 3],
            'b': [4, 4, 5, 6]
        })

        profiler = DataProfiler()
        profile = profiler.profile(df)

        assert profile.n_samples == 4
        assert profile.quality_score < 100.0  # 有重复

    def test_profile_numpy_array(self, sample_data):
        """测试分析numpy数组"""
        X, _, _ = sample_data

        profiler = DataProfiler()
        profile = profiler.profile(X)

        assert profile.n_samples == X.shape[0]
        assert profile.n_features == X.shape[1]

    def test_quality_score_range(self, sample_dataframe):
        """测试质量分数范围"""
        profiler = DataProfiler()
        profile = profiler.profile(sample_dataframe)

        assert 0 <= profile.quality_score <= 100


class TestQualityMetrics:
    """质量指标测试"""

    def test_initialization(self):
        """测试初始化"""
        metrics = QualityMetrics()
        assert metrics is not None

    def test_completeness_perfect(self, sample_dataframe):
        """测试完整性 - 完美数据"""
        metrics = QualityMetrics()
        completeness = metrics.completeness(sample_dataframe)

        assert completeness == 1.0  # 100%完整

    def test_completeness_with_missing(self):
        """测试完整性 - 缺失数据"""
        df = pd.DataFrame({
            'a': [1, 2, np.nan, 4],
            'b': [5, 6, 7, 8]
        })

        metrics = QualityMetrics()
        completeness = metrics.completeness(df)

        assert 0 < completeness < 1.0  # 有缺失但不是全空

    def test_uniqueness_all_unique(self):
        """测试唯一性 - 全唯一"""
        df = pd.DataFrame({
            'a': [1, 2, 3, 4],
            'b': [5, 6, 7, 8]
        })

        metrics = QualityMetrics()
        uniqueness = metrics.uniqueness(df)

        assert uniqueness == 1.0  # 100%唯一

    def test_uniqueness_with_duplicates(self):
        """测试唯一性 - 有重复"""
        df = pd.DataFrame({
            'a': [1, 1, 2, 2],
            'b': [3, 3, 4, 4]
        })

        metrics = QualityMetrics()
        uniqueness = metrics.uniqueness(df)

        assert 0 <= uniqueness < 1.0  # 有重复

    def test_validity_numeric(self):
        """测试有效性 - 数值数据"""
        df = pd.DataFrame({
            'a': [1.0, 2.0, 3.0, 4.0],
            'b': [5.0, 6.0, 7.0, 8.0]
        })

        def is_numeric(x):
            return isinstance(x, (int, float)) and not np.isnan(x)

        metrics = QualityMetrics()
        validity = metrics.validity(df, is_numeric)

        assert validity == 1.0  # 全部有效

    def test_consistency_consistent_data(self):
        """测试一致性 - 一致数据"""
        series = pd.Series([1.0, 1.5, 2.0, 2.5, 3.0])

        metrics = QualityMetrics()
        consistency = metrics.consistency(series)

        assert 0 <= consistency <= 1.0

    def test_consistency_inconsistent_data(self):
        """测试一致性 - 不一致数据"""
        series = pd.Series([1, 2, 100, 3, 4])  # 100是异常值

        metrics = QualityMetrics()
        consistency = metrics.consistency(series)

        assert 0 <= consistency <= 1.0


class TestDataQualityIntegration:
    """数据质量集成测试"""

    def test_complete_analysis(self, sample_dataframe):
        """测试完整分析流程"""
        profiler = DataProfiler()
        metrics = QualityMetrics()

        # 生成画像
        profile = profiler.profile(sample_dataframe)

        # 计算各项指标
        completeness = metrics.completeness(sample_dataframe)
        uniqueness = metrics.uniqueness(sample_dataframe)

        # 验证
        assert profile.quality_score >= 0
        assert 0 <= completeness <= 1
        assert 0 <= uniqueness <= 1

    def test_problematic_data_detection(self):
        """测试问题数据检测"""
        # 创建有问题的数据
        df = pd.DataFrame({
            'a': [1, 2, np.nan, 4, 5],
            'b': [1, 1, 1, 1, 1],  # 全部相同
            'c': [10, 20, 30, 1000, 50]  # 有异常值
        })

        profiler = DataProfiler()
        metrics = QualityMetrics()

        profile = profiler.profile(df)
        completeness = metrics.completeness(df)
        uniqueness = metrics.uniqueness(df)

        # 应该检测到质量问题
        assert profile.quality_score < 100.0
        assert completeness < 1.0  # 有缺失值
        assert uniqueness < 1.0  # 列b全部相同

    def test_empty_dataframe(self):
        """测试空DataFrame"""
        df = pd.DataFrame()

        profiler = DataProfiler()

        try:
            profile = profiler.profile(df)
            # 如果不报错，验证返回值
            assert profile.n_samples == 0 or profile.n_features == 0
        except ValueError:
            # 空DataFrame可能抛出异常，这也是合理的
            pass


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
