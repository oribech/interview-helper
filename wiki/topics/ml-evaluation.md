# ML & Model Evaluation

## Bias-Variance Tradeoff
- **High bias**: underfitting — model too simple
- **High variance**: overfitting — model too complex
- Goal: minimize total error = bias² + variance + irreducible noise

## Evaluation Metrics
- **Classification**: accuracy, precision, recall, F1, AUC-ROC, log loss
- **Regression**: MSE, RMSE, MAE, R²
- **Ranking**: NDCG, MAP, MRR

## When to Use What
- Imbalanced classes → precision/recall, F1, AUC (not accuracy)
- Cost-sensitive → weighted F1, custom loss
- Ranking → NDCG, MAP

## Cross-Validation
- k-fold: split data into k folds, train on k-1, test on 1
- Stratified k-fold: preserve class distribution
- Time series: walk-forward validation (no future leakage)

## Feature Engineering
- Missing values: imputation (mean/median/mode), indicator variable
- Categorical: one-hot, target encoding, ordinal
- Numerical: scaling, log transform, binning
- Feature selection: correlation, mutual information, L1 regularization

## Common Interview Questions
- "How do you handle overfitting?" → regularization, dropout, early stopping, more data
- "Explain precision vs recall" → precision = TP/(TP+FP), recall = TP/(TP+FN)
- "When would you use logistic regression over a tree model?" → interpretability, linear relationships, small data
