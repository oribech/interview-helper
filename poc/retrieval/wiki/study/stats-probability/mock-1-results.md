# Mock 1 Results

Source: google/study/stats-probability/mock-1-results.md

# Mock 1 Results

## Q1: What is a p-value?
**My answer:** Probability under H0 to see the results or more extreme one to the favor of H1.
**Verdict:** Correct

## Q2: When would you consider mean over median?
**My answer:** If the distribution is not skewed/there are outliers we usually use the mean. It has many advantages like normality from CLT, simple interpretability etc.
**Verdict:** Correct. Add: mean is preferred when you care about totals (mean * n = total).

## Q3: What is the standard error of the mean?
**My answer:** Gives you the square root of the variance estimation of the mean. Eventually tells you how the mean is estimated to move up and down from the true mean on average. Formula: s = sqrt(sum((x-bar(x))^2)/(n-1)), SE = s/sqrt(n).
**Verdict:** Correct

## Q4: For sample size n, margin of error is 3. How many more samples to make it 0.3?
**My answer:** MOE ~= c/sqrt(n), so you need about x100 obs more.
**Verdict:** Correct

## Q5: Is it good or bad to apply bootstrapping to increase sample size?
**My answer:** Bootstrapping is not increasing sample size but allowing to compute estimations from the same sample. The bootstrap estimate converges to the full sample estimate as number of bootstrap samples goes to inf.
**Verdict:** Correct

## Q6: 4 people in an elevator, 4 floors. Probability each gets off on a different floor?
**My answer:** There are factorial(4) options. 4 options to put 4 of them in the 4 floors. Probability is 4/factorial(4) = 1/6.
**Verdict:** Wrong. Total outcomes = 4^4 = 256 (independent choices), not 4!. Answer: 4!/4^4 = 24/256 = 3/32.

## Q7: Make an unfair coin fair.
**My answer:** I'm not sure. I guess you need to throw few times to make mechanism where some results over the multiple throws is 1/2. You can also make some condition, if H throw again or something conditional probability that cancels out p and gives half. Couldn't find the solution.
**Verdict:** Wrong. Von Neumann trick: flip twice, HT→Heads, TH→Tails, HH/TT→discard. Works because P(HT)=P(TH)=p(1-p).

## Q8: Difference between boosting and bagging?
**My answer:** In bagging we do independent estimators like trees and aggregate them (random forest for example). Boosting builds estimators on top of another like GBM where each estimator minimizes the error of the prev.
**Verdict:** Correct. Sharpen: bagging reduces variance, boosting reduces bias.

## Q9: Two highly correlated predictors — effect on logistic regression coefficients and CIs?
**My answer:** Predictor correlation creates multicollinearity, it can make one coef very very large and one very very small and even break the optimization algorithm leading to nulls. This makes CI impossible to calc as well.
**Verdict:** Mostly right. CIs become very wide (not impossible). Key point: hurts interpretability, not prediction.

## Q10: How does PCA work?
**My answer:** PCA takes a matrix and decomposes it to PDP^T. D has diagonal eigenvalues, P are eigenvectors. Gets orthogonal vectors ordered by variance explained. Helps with dim reduction, noise removal, and seeing clusters.
**Verdict:** Correct. Clarification: decomposition is on the covariance matrix, not the data matrix.

## Q11: Labels known in clustering — how to evaluate?
**My answer:** There is some metric that formulates how much of the true labels were indeed in the same bucket or scattered around. Don't remember it.
**Verdict:** Partial. Metrics: ARI (Adjusted Rand Index), NMI (Normalized Mutual Information).

## Q12: What is a Transformer? Explain it.
**My answer:** Architecture that helps with feature extraction from text. Works using the attention mechanism key value formulation. Measures correlations between words in the same doc and are foundation of modern LLMs.
**Verdict:** Partial. Missing: positional encoding, QKV mechanics (softmax(QK^T/√d)×V), multi-head attention, decoder-only vs encoder-decoder.

---

## Summary

| Subtopic | Score | Verdict |
|----------|-------|---------|
| Stats foundations | 4/4 | Strong |
| Bootstrap | 1/1 | Strong |
| Probability | 0/2 | Weak |
| ML fundamentals | 2/2 | Strong ?|
| ML applied | 1.5/2 | Needs review |
| Transformers/LLM | 0.5/1 | Needs review |

I dont understand deeply

1. how pca works. the difference to projection matrix
2.
