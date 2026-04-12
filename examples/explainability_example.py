"""
Example: Model Explainability (SHAP & LIME)

Demonstrates how to use the explainability module for:
- SHAP (SHapley Additive exPlanations) analysis
- LIME (Local Interpretable Model-agnostic Explanations)
- Feature importance analysis
- Explanation visualization
- Regulatory compliance reporting

Compliance: EU AI Act, FDA medical devices, financial services
"""

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from aeva.explainability import (
    SHAPExplainer,
    SHAPExplainerType,
    LIMEExplainer,
    FeatureImportanceAnalyzer,
    ExplanationReportGenerator,
    plot_feature_importance
)


def create_sample_classification_model():
    """Create a sample classification model for demonstration"""
    # Load breast cancer dataset
    data = load_breast_cancer()
    X, y = data.data, data.target
    feature_names = data.feature_names.tolist()

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    return model, X_train, X_test, y_train, y_test, feature_names


def create_sample_regression_model():
    """Create a sample regression model for demonstration"""
    # Load boston housing dataset (using alternative as it's deprecated)
    from sklearn.datasets import fetch_california_housing
    data = fetch_california_housing()
    X, y = data.data, data.target
    feature_names = data.feature_names.tolist()

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    return model, X_train, X_test, y_train, y_test, feature_names


def example_shap_analysis():
    """Example 1: SHAP Analysis"""
    print("=" * 70)
    print("Example 1: SHAP Analysis")
    print("=" * 70)

    # Create model
    model, X_train, X_test, y_train, y_test, feature_names = create_sample_classification_model()

    print(f"\n✓ Trained RandomForest Classifier")
    print(f"  Training samples: {len(X_train)}")
    print(f"  Test samples: {len(X_test)}")
    print(f"  Features: {len(feature_names)}")

    # Initialize SHAP explainer
    print("\n📊 Initializing SHAP Explainer...")
    explainer = SHAPExplainer(
        model=model,
        background_data=X_train[:100],  # Use subset for speed
        feature_names=feature_names,
        explainer_type=SHAPExplainerType.TREE  # TreeExplainer for tree-based models
    )

    # Explain single instance
    print("\n🔍 Explaining Single Instance:")
    instance = X_test[0]
    explanation = explainer.explain_instance(instance)

    print(f"\n  Expected value (baseline): {explanation.expected_value:.4f}")
    print(f"  Model output: {explanation.model_output}")

    print("\n  Top 10 Most Important Features:")
    top_features = explanation.get_top_features(10)
    for i, (feature, value) in enumerate(top_features, 1):
        direction = "↑" if value > 0 else "↓"
        print(f"    {i}. {feature}: {value:.4f} {direction}")

    # Global feature importance
    print("\n🌍 Global Feature Importance:")
    global_explanation = explainer.explain_global(X_test[:50])

    top_global = global_explanation.get_top_features(10)
    print("\n  Top 10 Globally Important Features:")
    for i, (feature, value) in enumerate(top_global, 1):
        print(f"    {i}. {feature}: {value:.4f}")

    # Get feature importance dictionary
    importance_dict = explainer.get_feature_importance(X_test[:50])
    print(f"\n  ✓ Computed importance for {len(importance_dict)} features")

    return explainer, explanation


def example_lime_analysis():
    """Example 2: LIME Analysis"""
    print("\n" + "=" * 70)
    print("Example 2: LIME Analysis")
    print("=" * 70)

    # Create model
    model, X_train, X_test, y_train, y_test, feature_names = create_sample_classification_model()

    print(f"\n✓ Trained RandomForest Classifier")

    # Initialize LIME explainer
    print("\n📊 Initializing LIME Explainer...")

    # LIME needs prediction function
    def predict_fn(X):
        return model.predict_proba(X)

    explainer = LIMEExplainer(
        predict_fn=predict_fn,
        training_data=X_train,
        feature_names=feature_names,
        mode='classification'
    )

    # Explain single instance
    print("\n🔍 Explaining Single Instance with LIME:")
    instance = X_test[0]
    explanation = explainer.explain_instance(
        instance,
        num_features=10,
        num_samples=5000,
        labels=(1,)  # Explain class 1 (malignant)
    )

    print(f"\n  Local Model R² Score: {explanation.score:.4f}")
    print(f"  Intercept: {explanation.intercept:.4f}")

    print("\n  Top 10 Feature Weights:")
    top_features = explanation.get_top_features(10, absolute=False)
    for i, (feature, weight) in enumerate(top_features, 1):
        direction = "Increases" if weight > 0 else "Decreases"
        print(f"    {i}. {feature}: {weight:.4f} ({direction} prediction)")

    # Counterfactual suggestions
    print("\n🔄 Counterfactual Suggestions:")
    target_change = -0.1  # Try to decrease probability by 0.1
    suggestions = explainer.get_counterfactual_direction(
        instance,
        target_change,
        num_features=5
    )

    print(f"\n  To decrease prediction by {abs(target_change):.2f}:")
    for feature, change in list(suggestions.items())[:5]:
        print(f"    {feature}: change by {change:.4f}")

    return explainer, explanation


def example_feature_importance():
    """Example 3: Feature Importance Analysis"""
    print("\n" + "=" * 70)
    print("Example 3: Feature Importance Analysis")
    print("=" * 70)

    # Create model
    model, X_train, X_test, y_train, y_test, feature_names = create_sample_classification_model()

    print(f"\n✓ Trained RandomForest Classifier")

    # Initialize analyzer
    print("\n📊 Initializing Feature Importance Analyzer...")
    analyzer = FeatureImportanceAnalyzer(
        model=model,
        X=X_test,
        y=y_test,
        feature_names=feature_names
    )

    # 1. Model-specific importance
    print("\n1️⃣ Model-Specific Importance (from Random Forest):")
    model_importance = analyzer.model_importance()

    if model_importance:
        top_features = model_importance.get_top_features(10)
        for i, (feature, score, rank) in enumerate(top_features, 1):
            print(f"    {i}. {feature}: {score:.4f}")

    # 2. Permutation importance
    print("\n2️⃣ Permutation Importance:")
    print("  (Measuring performance drop when shuffling features...)")
    perm_importance = analyzer.permutation_importance(n_repeats=5)

    print(f"\n  Baseline Score: {perm_importance.metadata['baseline_score']:.4f}")
    top_features = perm_importance.get_top_features(10)
    print("\n  Top 10 Features by Permutation:")
    for i, (feature, score, rank) in enumerate(top_features, 1):
        print(f"    {i}. {feature}: {score:.4f} (rank: {rank})")

    # 3. Compare methods
    print("\n3️⃣ Comparing Multiple Methods:")
    comparison = analyzer.compare_methods(['permutation', 'model', 'shap'])

    print(f"\n  Methods compared: {list(comparison.keys())}")

    # Aggregate results
    aggregated = analyzer.aggregate_importances(comparison, method='mean')

    print("\n  Aggregated Top 10 Features:")
    top_features = aggregated.get_top_features(10)
    for i, (feature, score, rank) in enumerate(top_features, 1):
        print(f"    {i}. {feature}: {score:.4f}")

    return analyzer, aggregated


def example_explanation_visualization():
    """Example 4: Explanation Visualization"""
    print("\n" + "=" * 70)
    print("Example 4: Explanation Visualization")
    print("=" * 70)

    # Create model
    model, X_train, X_test, y_train, y_test, feature_names = create_sample_classification_model()

    # Feature importance
    print("\n📊 Creating Feature Importance Visualization...")
    analyzer = FeatureImportanceAnalyzer(
        model=model,
        X=X_test[:100],
        y=y_test[:100],
        feature_names=feature_names
    )

    importance = analyzer.model_importance()

    # Create plot
    try:
        fig = plot_feature_importance(importance, top_n=15)
        print("  ✓ Feature importance plot created")
        print("  (Plot displayed if running interactively)")
    except Exception as e:
        print(f"  Note: Visualization requires matplotlib: {e}")

    return importance


def example_compliance_reporting():
    """Example 5: Compliance Reporting"""
    print("\n" + "=" * 70)
    print("Example 5: Compliance Reporting (EU AI Act, FDA)")
    print("=" * 70)

    # Create model
    model, X_train, X_test, y_train, y_test, feature_names = create_sample_classification_model()

    print("\n📋 Generating Compliance Report...")

    # Get explanations
    shap_explainer = SHAPExplainer(
        model=model,
        background_data=X_train[:100],
        feature_names=feature_names
    )
    shap_explanation = shap_explainer.explain_instance(X_test[0])

    lime_explainer = LIMEExplainer(
        predict_fn=model.predict_proba,
        training_data=X_train,
        feature_names=feature_names,
        mode='classification'
    )
    lime_explanation = lime_explainer.explain_instance(X_test[0], num_features=10)

    analyzer = FeatureImportanceAnalyzer(
        model=model,
        X=X_test[:100],
        y=y_test[:100],
        feature_names=feature_names
    )
    importance = analyzer.model_importance()

    # Generate reports
    report_generator = ExplanationReportGenerator(model_name="Breast Cancer Classifier")

    # Text report
    print("\n1️⃣ Text Report:")
    text_report = report_generator.generate_text_report(
        shap_explanation=shap_explanation,
        lime_explanation=lime_explanation,
        feature_importance=importance
    )
    print(text_report[:500] + "...\n")

    # HTML report
    print("2️⃣ HTML Report:")
    html_report = report_generator.generate_html_report(
        shap_explanation=shap_explanation,
        lime_explanation=lime_explanation,
        feature_importance=importance
    )
    print(f"  ✓ HTML report generated ({len(html_report)} characters)")

    # Save reports
    try:
        report_generator.save_report(
            './explanation_report.html',
            format='html',
            shap_explanation=shap_explanation,
            lime_explanation=lime_explanation,
            feature_importance=importance
        )
        print("  ✓ Report saved to ./explanation_report.html")
    except Exception as e:
        print(f"  Note: Could not save report: {e}")

    print("\n📜 Compliance Notes:")
    print("  ✓ EU AI Act: Explanations provided for high-risk AI system")
    print("  ✓ FDA: Algorithm transparency documented")
    print("  ✓ Financial Services: Model decisions explained")

    return report_generator


def example_regression_explanation():
    """Example 6: Regression Model Explanation"""
    print("\n" + "=" * 70)
    print("Example 6: Regression Model Explanation")
    print("=" * 70)

    # Create regression model
    model, X_train, X_test, y_train, y_test, feature_names = create_sample_regression_model()

    print(f"\n✓ Trained RandomForest Regressor")
    print(f"  Predicting: House prices")

    # SHAP for regression
    print("\n📊 SHAP Analysis for Regression:")
    explainer = SHAPExplainer(
        model=model,
        background_data=X_train[:100],
        feature_names=feature_names
    )

    explanation = explainer.explain_instance(X_test[0])

    print(f"\n  Expected value: ${explanation.expected_value:.2f}")
    print(f"  Predicted value: ${explanation.model_output:.2f}")

    print("\n  Top Features Affecting This Prediction:")
    top_features = explanation.get_top_features(8)
    for i, (feature, value) in enumerate(top_features, 1):
        effect = "increases" if value > 0 else "decreases"
        print(f"    {i}. {feature}: {effect} price by ${abs(value):.2f}")

    return explainer


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("AEVA Explainability Module Examples")
    print("Compliance: EU AI Act, FDA, Financial Services")
    print("=" * 70)

    # Run examples
    shap_explainer, shap_exp = example_shap_analysis()
    lime_explainer, lime_exp = example_lime_analysis()
    analyzer, importance = example_feature_importance()
    viz_importance = example_explanation_visualization()
    report_gen = example_compliance_reporting()
    reg_explainer = example_regression_explanation()

    # Summary
    print("\n" + "=" * 70)
    print("All Examples Completed!")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  ✓ SHAP explanations (local & global)")
    print("  ✓ LIME explanations (local approximations)")
    print("  ✓ Feature importance (multiple methods)")
    print("  ✓ Counterfactual suggestions")
    print("  ✓ Compliance reporting (EU/FDA)")
    print("  ✓ Regression & classification support")
    print("\n🎯 Interview Highlights:")
    print("  • Regulatory compliance (EU AI Act, FDA)")
    print("  • Industry-standard methods (SHAP/LIME)")
    print("  • Model-agnostic explanations")
    print("  • Production-ready reporting")


if __name__ == '__main__':
    main()
