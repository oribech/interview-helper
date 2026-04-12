# A/B Testing

## Quick Reference
- **Null hypothesis (H₀)**: No difference between control and treatment
- **p-value**: Probability of observing data at least as extreme as results, assuming H₀ is true
- **Statistical significance**: Typically α = 0.05 (reject H₀ if p < α)
- **Power**: Probability of correctly rejecting H₀ when it's false (typically 0.8)

## Key Formulas
- **Sample size**: n = (Z_α/2 + Z_β)² × 2σ² / δ²
- **Minimum Detectable Effect (MDE)**: δ = Z_α/2 × √(2σ²/n)

## Common Pitfalls
- Peeking at results before reaching sample size (inflates false positive rate)
- Multiple comparisons without correction (Bonferroni, FDR)
- Network effects / interference between groups (use cluster randomization)
- Novelty/primacy effects (run test long enough)
- Simpson's paradox (check for confounders)

## Design Steps
1. Define hypothesis and metric (OEC — Overall Evaluation Criterion)
2. Choose randomization unit (user, session, page)
3. Calculate sample size for desired MDE and power
4. Set guardrail metrics (latency, crash rate, revenue)
5. Run test, wait for full duration
6. Analyze: check p-value, confidence interval, practical significance
