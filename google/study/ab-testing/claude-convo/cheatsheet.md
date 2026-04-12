# A/B Cheatsheet

## Roadmap

|     | Topic                                     |
| --- | ----------------------------------------- |
| ✅  | Design components                         |
| ✅  | Power formula                             |
| ✅  | p-value / practical significance          |
| ✅  | SRM                                       |
| ✅  | Multiple testing                          |
| ✅  | Experiment designs (multi-arm, crossover) |
| ✅  | Novelty/primacy effects                   |
| ✅  | Network interference                      |
| ✅  | Bias / selection bias                     |
| 🔲  | Mock end-to-end                           |

---

## Components

|            |                                                        |
| ---------- | ------------------------------------------------------ |
| Hypothesis | "[Change] increases [OEC] without harming [guardrail]" |
| OEC        | metric/user (revenue-per-user, sessions-per-user)      |
| Guardrails | metrics that must not move (latency, CTR, crash rate)  |
| Rand. unit | user (cookie or login ID)                              |
| Population | triggered users only (affected by change)              |
| Duration   | ≥ 1 week (day-of-week) + 2–4 weeks if novelty effects  |
| Size       | n ≈ 16σ²/δ² per variant                                |

---

## Experiment Designs

| Design          | Description                                        | Pro                              | Con                                  |
| --------------- | -------------------------------------------------- | -------------------------------- | ------------------------------------ |
| **A/B (2-arm)** | Control vs 1 Treatment                             | Simple                           | Tests one thing                      |
| **Multi-arm**   | Control vs Treatment1 vs Treatment2                | Tests multiple variants at once  | Needs more traffic; multiple testing |
| **Crossover**   | Group A gets drug1→drug2, Group B gets drug2→drug1 | Removes between-subject variance | Needs washout period; carryover risk |
| **Factorial**   | Test combinations (A on/off × B on/off)            | Tests interactions               | Complex; needs large n               |

**2-drug question:** use **3-arm parallel** (Control, Drug1, Drug2) or **crossover with washout** if within-subject comparison needed.

---

## Power

$$n \approx \frac{16\sigma^2}{\delta^2} \quad \text{per variant}$$

- 16 = 2(1.96 + 0.84)² ← α=0.05, power=80%
- More variants → adjust α for multiple testing

## Key Numbers

|         |                          |
| ------- | ------------------------ |
| α       | 0.05                     |
| Power   | 0.80                     |
| z(α/2)  | 1.96                     |
| z(β)    | 0.84                     |
| CI      | δ̂ ± 1.96·SE              |
| Type I  | false positive (α)       |
| Type II | false negative (1−power) |

---

## SRM

- Configured vs actual group sizes don't match → **results untrustworthy**
- Detect: chi-square on actual vs expected sizes
- Causes: bot filtering, redirect bugs, logging bugs, cache
- Action: do not launch, investigate, rerun

---

## Multiple Testing

| Tier            | Threshold |
| --------------- | --------- |
| Primary OEC     | p < 0.05  |
| Guardrails      | p < 0.01  |
| Everything else | p < 0.001 |

100 metrics → expect ~5 spurious at p<0.05.

---

## Practical vs Statistical Significance

| Result           | Action                          |
| ---------------- | ------------------------------- |
| Both significant | Launch                          |
| Stat only        | Don't launch (effect too small) |
| Practical only   | Rerun with more power           |
| Neither          | Abandon                         |
| CI very wide     | Rerun with more power           |

---

## Novelty & Primacy Effects

| Effect      | Description                                  | Metric pattern             |
| ----------- | -------------------------------------------- | -------------------------- |
| **Novelty** | Users excited by change, engagement inflated | High → decreases over time |
| **Primacy** | Users resist change, engagement suppressed   | Low → increases over time  |

**Fix:** plot metric daily, wait for stabilization (~2 weeks). Use **new users** as clean signal (no prior exposure).

---

## Google Product Metrics

| Product       | OEC                                  | Guardrails                                 |
| ------------- | ------------------------------------ | ------------------------------------------ |
| YouTube       | watch-time-per-user                  | ad-revenue-per-user, video completion rate |
| Google Search | queries-per-user, time-to-click      | ad-CTR, revenue-per-query                  |
| Gmail         | emails-sent-per-user                 | latency, spam rate                         |
| Google Maps   | sessions-per-user, route completions | crash rate, latency                        |
| Google Ads    | ad-revenue-per-user                  | CTR, advertiser spend                      |
| Google Play   | installs-per-user                    | uninstall rate, revenue                    |

---

## Practical Significance

Always state before running: **"We only care if δ ≥ X%"**

- Sets your δ for power analysis
- Drives launch/no-launch decision
- X depends on engineering cost — bigger cost → higher bar

---

## Think-Out-Loud Template

| Step       | Say                                                                    |
| ---------- | ---------------------------------------------------------------------- |
| Goal       | "The business goal here is..."                                         |
| OEC        | "I'd measure X because Y"                                              |
| Guardrail  | "I'd protect Z because this feature could harm it by..."               |
| Population | "Only users who could be affected, specifically..."                    |
| Size       | "I'd run power analysis with δ = our practical significance threshold" |
| Risk       | "Main risk here is... so I'd add..."                                   |

---

## Gotchas / Edge Cases

| Gotcha                 | Question to ask yourself                                     |
| ---------------------- | ------------------------------------------------------------ |
| Network effects        | Do Treatment users affect Control users? → cluster randomize |
| Selection bias         | Did users self-select into Treatment? → must randomize       |
| SRM                    | Are group sizes as configured? → chi-square check            |
| Novelty/primacy        | Is metric stable over time? → plot daily, wait 2-4 weeks     |
| Multiple testing       | How many metrics am I testing? → tiered thresholds           |
| Triggered analysis     | Are all users actually affected? → restrict population       |
| Carryover              | Crossover design? → need washout period                      |
| Bot traffic            | Outliers inflating variance? → cap metrics                   |
| Practical significance | Did I define δ before running? → always state the bar        |
| Cannibalization        | Does feature steal from another metric? → add as guardrail   |
