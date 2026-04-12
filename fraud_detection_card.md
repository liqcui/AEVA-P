# Model Card: Fraud Detection System

**Version:** 5.1.0 | **Type:** classifier | **Generated:** 2026-04-12 23:10:53

## Model Details

- **Model Type:** classifier

## Intended Use

Real-time fraud detection for payment transactions

## Training Data

Transaction data with fraud labels

**Dataset Size:** 5,000,000 samples

## Performance Metrics

**Primary Metric:** precision

| Metric | Value |
|--------|-------|
| precision | 0.9300 |
| recall | 0.8900 |
| f1_score | 0.9100 |
| accuracy | 0.9800 |
| false_positive_rate | 0.0100 |

## Fairness Metrics

- **Demographic Parity:** 0.9400
- **Equal Opportunity:** 0.9600

**Protected Attributes:** merchant_category, geographic_region

## Limitations

May require additional rules for novel fraud patterns

## Ethical Considerations

Balance between fraud prevention and customer friction
