"""
Pytest配置和共享fixtures
"""
import pytest
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


@pytest.fixture(scope="session")
def sample_data():
    """加载示例数据集"""
    data = load_breast_cancer()
    X, y = data.data, data.target
    feature_names = data.feature_names.tolist()
    return X, y, feature_names


@pytest.fixture(scope="session")
def train_test_data(sample_data):
    """分割训练测试数据"""
    X, y, feature_names = sample_data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test, feature_names


@pytest.fixture(scope="session")
def trained_model(train_test_data):
    """训练一个测试模型"""
    X_train, X_test, y_train, y_test, _ = train_test_data
    model = RandomForestClassifier(n_estimators=30, random_state=42, max_depth=5)
    model.fit(X_train, y_train)
    return model


@pytest.fixture
def sample_dataframe(sample_data):
    """创建pandas DataFrame"""
    X, y, feature_names = sample_data
    df = pd.DataFrame(X, columns=feature_names)
    return df


@pytest.fixture
def sample_instance(train_test_data):
    """单个测试实例"""
    _, X_test, _, y_test, _ = train_test_data
    return X_test[0], y_test[0]


@pytest.fixture
def model_predictions(trained_model, train_test_data):
    """模型预测结果"""
    _, X_test, _, y_test, _ = train_test_data
    y_pred = trained_model.predict(X_test)
    return y_test, y_pred
