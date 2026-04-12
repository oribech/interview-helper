# Cheatsheet: Things I Learned During Prep

Source: google/study/stats-probability/CHEATSHEET.md

# Cheatsheet: Things I Learned During Prep

## Probability: Symmetry Hunting (universal method)

When stuck on any probability question:

1. **Define the sample space** — what are ALL possible outcomes? (e.g., n people choosing independently from k options → k^n, NOT n!)
2. **Find the symmetry** — which outcomes have equal probability by construction?
3. **Count or condition** — count favorable/total, or condition on the symmetric subset

When stuck: **write out the full sample space**. Interview questions never have more than a few lines. The answer jumps out.

### Example: Make an unfair coin fair (Von Neumann's trick)

Flip biased coin (P(H)=p) twice:
- HT has probability p(1-p)
- TH has probability (1-p)p — **same!**
- HT → "Heads", TH → "Tails", HH/TT → discard and repeat

## ML: Bagging vs Boosting

- **Bagging**: parallel, independent estimators, reduces **variance** (e.g., random forest)
- **Boosting**: sequential, each fixes previous errors, reduces **bias** (e.g., GBM)

## ML: Multicollinearity

- Coefficients become unstable (large, flip signs)
- CIs become very wide (SE explodes)
- **Prediction accuracy mostly unaffected** — hurts interpretability, not prediction

## ML: Evaluating Clustering with Known Labels

- **ARI (Adjusted Rand Index)** — pairwise agreement between true labels and clusters, adjusted for chance. Range -1 to 1.
- **NMI (Normalized Mutual Information)** — how much cluster assignment tells you about true label. Range 0 to 1.
- Interview one-liner: "ARI checks whether pairs that belong together are clustered together, adjusted for random chance."
