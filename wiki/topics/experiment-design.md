# Experiment Design

## Step-by-Step Framework
1. **Hypothesis**: clear, testable statement
2. **Randomization unit**: user, cookie, device, session, cluster
3. **Metric**: OEC + guardrails
4. **Sample size**: power analysis (MDE, α, β, baseline rate)
5. **Duration**: account for day-of-week effects (minimum 1-2 weeks)
6. **Analysis**: intention-to-treat, check for SRM (sample ratio mismatch)

## Power Analysis
- n = (Z_α/2 + Z_β)² × (p₁(1-p₁) + p₂(1-p₂)) / (p₁ - p₂)²
- Rules of thumb: smaller MDE → need more users
- For proportions: n ≈ 16σ²/δ² (at 80% power, α=0.05)

## Interference / Network Effects
- Problem: treatment affects control (social networks, marketplaces)
- Solutions: cluster randomization, geo-based experiments, switchback designs

## Multiple Testing
- Bonferroni correction: α_adjusted = α / m (too conservative)
- Benjamini-Hochberg (FDR): controls false discovery rate
- Pre-registration: specify primary metric upfront

## Guardrail Metrics
- Revenue, latency, crash rate, customer complaints
- Set thresholds before experiment starts
- If guardrail violated → pause experiment
