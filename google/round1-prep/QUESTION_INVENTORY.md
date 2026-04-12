# Glassdoor Question Inventory

Status: ✅ = drilled, ⚠️ = partially covered, ❌ = not covered, 🔲 = skipped (low priority)

## Stats + Probability (Q001-Q025)

| Q    | Topic                                     | Status | Notes                                           |
| ---- | ----------------------------------------- | ------ | ----------------------------------------------- |
| Q001 | p-value explanation                       | ⚠️     | Covered in t-test drill, not drilled standalone |
| Q002 | Mean vs median                            | ❌     |                                                 |
| Q003 | Standard error of mean                    | ⚠️     | Used in t-test drill                            |
| Q004 | Sample size & margin of error             | ❌     |                                                 |
| Q005 | Assumptions of error in linear regression | ❌     |                                                 |
| Q006 | Card probability                          | ❌     | Prior study (strong)                            |
| Q007 | Coin toss independence                    | ❌     | Prior study (strong)                            |
| Q008 | P(2X > Y) uniform distributions           | ❌     | Prior study                                     |
| Q009 | Elevator probability                      | ❌     | Prior study                                     |
| Q010 | Make unfair coin fair                     | ❌     | Prior study                                     |
| Q011 | Random variable, distribution test        | ❌     |                                                 |
| Q012 | Non-normal distribution                   | ❌     |                                                 |
| Q013 | Test if coin is biased                    | ❌     |                                                 |
| Q014 | 1-point sample test                       | ❌     |                                                 |
| Q015 | Bootstrap — good or bad for sample size?  | ✅     | Block 2 drill 1                                 |
| Q016 | Implement bootstrap                       | ✅     | Block 2 drill 1                                 |
| Q017 | Probability integral transform            | ❌     |                                                 |
| Q018 | Generate iid draws from distribution      | ✅     | Block 2 drill 7 (Box-Muller)                    |
| Q019 | Generate N normal samples + plot          | ✅     | Block 2 drill 7                                 |
| Q020 | Confidence interval in Python             | ✅     | Block 2 drill 1 (bootstrap CI)                  |
| Q021 | Width of confidence interval              | ⚠️     | Related to CI drill                             |
| Q022 | p-values in high-dimensional regression   | ❌     |                                                 |
| Q023 | Simpson's paradox (pooled mean)           | ❌     |                                                 |
| Q024 | SE of mean vs SE of median                | ❌     |                                                 |
| Q025 | Bernoulli matrix, divide by column sums   | ✅     | Block 2 drill 8                                 |

## A/B Testing (Q026-Q035)

| Q    | Topic                                     | Status | Notes                     |
| ---- | ----------------------------------------- | ------ | ------------------------- |
| Q026 | Design an A/B test (walkthrough)          | ✅     | Block 5 drill 1           |
| Q027 | A/B test with 3% increase                 | ❌     |                           |
| Q028 | A/B test — new YouTube feature            | ❌     | Block 5 drill 3 (planned) |
| Q029 | Two-drug experiment design                | ❌     |                           |
| Q030 | YouTube product change experiment         | ❌     | Block 5 drill 3 (planned) |
| Q031 | Test if metric increased after app change | ❌     |                           |
| Q032 | Remove bias in A/B test, ad campaigns     | ❌     | Block 5 drill 4 (planned) |
| Q033 | Roadmap to test features                  | ❌     |                           |
| Q034 | A/B testing + selection bias + ML         | ❌     | Block 5 drill 4 (planned) |
| Q035 | Stats concepts + experiment design        | ❌     |                           |

## ML + LLM Eval (Q036-Q060)

| Q    | Topic                                    | Status | Notes                                         |
| ---- | ---------------------------------------- | ------ | --------------------------------------------- |
| Q036 | Bias in random forest                    | ❌     | Block 4 drill 1 (planned)                     |
| Q037 | Boosting vs bagging                      | ⚠️     | Covered in mock (swapped, corrected)          |
| Q038 | Feature selection in linear regression   | ❌     | Block 4 drill 1 (planned)                     |
| Q039 | Multicollinearity in logistic regression | ❌     | Block 4 drill 5 (planned)                     |
| Q040 | Multicollinearity — measure, effect      | ❌     | Block 4 drill 5 (planned)                     |
| Q041 | Omitted variable bias                    | ❌     |                                               |
| Q042 | MLE for logistic regression              | ⚠️     | Wrote logistic from scratch (Block 2 drill 3) |
| Q043 | Neural networks + sigmoid                | ✅     | Block 2 drill 3                               |
| Q044 | Transformers explanation                 | ❌     | Prior study (strong)                          |
| Q045 | Imbalanced datasets                      | ❌     |                                               |
| Q046 | Precision & Recall to non-technical      | ✅     | Drilled in metrics assignment                 |
| Q047 | Clustering evaluation with labels        | ❌     | Block 4 drill 2 (planned)                     |
| Q048 | K-means vs GMM, choose K                 | ❌     | Block 4 drill 2 (planned)                     |
| Q049 | PCA explanation                          | ❌     | Block 4 drill 4 (planned)                     |
| Q050 | Predictive model for YouTube Shorts      | ❌     |                                               |
| Q051 | Build predictive model end-to-end        | ❌     |                                               |
| Q052 | Forecast brand sales                     | ❌     |                                               |
| Q053 | Describe ML project you worked on        | ❌     | Behavioral — prep from experience             |
| Q054 | End-to-end ML project                    | ❌     | Behavioral — prep from experience             |
| Q055 | ML/DL experience                         | ❌     | Behavioral — prep from experience             |
| Q056 | LASSO, Ridge                             | ⚠️     | Covered in mock (L1/L2 strong)                |
| Q057 | Gaussian discrimination, Bayesian, RNN   | 🔲     | Very academic, low priority                   |
| Q058 | Why use feature selection?               | ❌     | Block 4 drill 1 (planned)                     |
| Q059 | Feature selection, overfitting           | ⚠️     | Covered in mock (overfitting strong)          |
| Q060 | Predict metrics using regression         | ✅     | Block 2 drill 2 (OLS)                         |

## Python + SQL (Q061-Q077)

| Q    | Topic                                    | Status | Notes                            |
| ---- | ---------------------------------------- | ------ | -------------------------------- |
| Q061 | IQR outlier detection (Python)           | ✅     | Block 2 drill 6                  |
| Q062 | SQL A/B testing case study               | ✅     | Block 1 drill 7                  |
| Q063 | Explain how SQL works                    | ⚠️     | Implicit in all SQL drills       |
| Q064 | SQL window function + GROUP BY           | ✅     | Block 1 drills 2, 5              |
| Q065 | Top-5 highest-selling items              | ✅     | Block 1 drill 3                  |
| Q066 | Compare first 3 cols to last 3           | ❌     |                                  |
| Q067 | Largest word by deleting chars           | 🔲     | Algorithms — low priority for DS |
| Q068 | Cluster separation + friends-of-friends  | 🔲     | Algorithms — low priority        |
| Q069 | Invert binary tree                       | 🔲     | Algorithms — low priority        |
| Q070 | Tree traversal                           | 🔲     | Algorithms — low priority        |
| Q071 | Rejection sampling                       | ❌     |                                  |
| Q072 | Data manipulation (groupby, merge, join) | ✅     | Block 2 drill 4                  |
| Q073 | Multiply matrix elements (R/Python)      | ✅     | Block 2 drill 8                  |
| Q074 | SQL joins                                | ✅     | Block 1 drill 4                  |
| Q075 | BFS                                      | 🔲     | Algorithms — low priority        |
| Q076 | Sum of squares                           | ✅     | Block 2 drill 9                  |
| Q077 | MapReduce design                         | ❌     |                                  |

## Product Sense (Q078-Q084, Q116)

| Q    | Topic                                   | Status | Notes                                         |
| ---- | --------------------------------------- | ------ | --------------------------------------------- |
| Q078 | Google Meet success metrics             | ⚠️     | Similar to Maps drill                         |
| Q079 | Google Chat low adoption — investigate  | ✅     | Similar to YouTube/Snapchat diagnostic drills |
| Q080 | YouTube success evaluation              | ⚠️     | Similar to Maps/Podcasts drills               |
| Q081 | Detect inappropriate content on YouTube | ✅     | Block 3 drill 5 (fake reviews variant)        |
| Q082 | YouTube abuse patterns                  | ⚠️     | Related to Q081                               |
| Q083 | Feature change — use DS to recommend    | ⚠️     | Covered in A/B framework                      |
| Q084 | Measure/value new product line          | ❌     | Business case type                            |
| Q116 | Improve a Google product                | ❌     |                                               |

## Time Series + Causal Inference (Q090-Q094)

| Q    | Topic                                  | Status | Notes |
| ---- | -------------------------------------- | ------ | ----- |
| Q090 | Compare 2 time series                  | ❌     |       |
| Q091 | Generatory component of time series    | ❌     |       |
| Q092 | Causal inference                       | ❌     |       |
| Q093 | Computational stats + causal inference | ❌     |       |
| Q094 | Historical analytics modeling          | ❌     |       |

## Misc (Q085, Q088-Q089)

| Q    | Topic                                | Status | Notes                 |
| ---- | ------------------------------------ | ------ | --------------------- |
| Q085 | Optimize DB query + evaluate ML algo | ❌     |                       |
| Q088 | Exploring a dataset                  | ❌     |                       |
| Q089 | Outlier detection                    | ✅     | Block 2 drill 6 (IQR) |

---

## Summary

| Category             | Total  | ✅ Done | ⚠️ Partial | ❌ Not done | 🔲 Skipped |
| -------------------- | ------ | ------- | ---------- | ----------- | ---------- |
| Stats + Probability  | 25     | 5       | 3          | 17          | 0          |
| A/B Testing          | 10     | 1       | 0          | 9           | 0          |
| ML + LLM Eval        | 25     | 3       | 4          | 16          | 2          |
| Python + SQL         | 17     | 10      | 1          | 2           | 4          |
| Product Sense        | 8      | 2       | 4          | 2           | 0          |
| Time Series + Causal | 5      | 0       | 0          | 5           | 0          |
| Misc                 | 3      | 1       | 0          | 2           | 0          |
| **Total**            | **93** | **22**  | **12**     | **53**      | **6**      |
