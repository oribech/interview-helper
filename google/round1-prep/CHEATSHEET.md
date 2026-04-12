# Round 1 Drill Cheatsheet

Patterns learned during drill practice. Scan before interview.

---

## SQL

| Pattern | Syntax | When |
|---------|--------|------|
| Safe division | `SUM(x) / NULLIF(SUM(y), 0)` | Any division — prevents divide-by-zero |
| Window func syntax | `LAG(col, 1) OVER (ORDER BY col)` | OVER clause is mandatory for all window funcs |
| YoY growth % | `(new - old) / NULLIF(old, 0)` | Growth = (new-old)/old, NOT new/old |
| Extract year | `EXTRACT(YEAR FROM date)` | More portable than `YEAR(date)` |
| CTE for readability | `WITH name AS (...)` | Use CTEs to break complex queries into steps |
| Execution order | `FROM→WHERE→GROUP BY→HAVING→SELECT→ORDER BY→LIMIT` | LIMIT is last; ORDER BY agg works |
| Anti-join (not in B) | `LEFT JOIN b ON ... WHERE b.key IS NULL` | Prefer over NOT IN — NOT IN breaks on NULLs |
| NOT EXISTS | `WHERE NOT EXISTS (SELECT 1 FROM b WHERE ...)` | Also NULL-safe; use for "not in" checks |
| OVER clause order | `OVER (PARTITION BY x ORDER BY y)` | PARTITION first, ORDER second, no comma |
| ROW_NUMBER | `ROW_NUMBER() OVER (...)` | Always unique — use for dedup |
| RANK | `RANK() OVER (...)` | Ties share rank, skips next (1,2,2,**4**) |
| DENSE_RANK | `DENSE_RANK() OVER (...)` | Ties share rank, no skip (1,2,2,**3**) |
| Top-N per group | CTE with `RANK/DENSE_RANK ... WHERE rnk <= N` | Standard pattern for "top N per partition" |
| Week grouping | `DATE_TRUNC('week', date)` | Unique across years — safer than `week_number()` |
| Avoid reserved aliases | Use `rnk`, `dense_rnk` | `rank` is reserved in most dialects |
| Conversion rate | `COUNT(DISTINCT p.id) / NULLIF(COUNT(DISTINCT u.id), 0)` | Users who did X / total users |
| JOIN duplicates | Use `COUNT(DISTINCT ...)` after JOINs | LEFT JOIN inflates rows when 1:many |
| Conditional agg | `SUM(CASE WHEN x THEN 1 ELSE 0 END)` | Portable boolean counting — don't SUM(boolean) |

## Python

| Pattern | Syntax | When |
|---------|--------|------|
| Sample with replacement | `random.choices(seq, k=N)` | Bootstrap. `choice()` (singular) = 1 draw |
| Large int literal | `10_000` not `10,000` | Comma creates tuple in Python |
| Non-mutating sort | `sorted(lst)` not `lst.sort()` | When you don't own the data |
| Manual mean | `sum(lst) / len(lst)` | No numpy available |
| Bootstrap CI | resample→stat→collect→percentiles | `sorted(means)[int(q * len(means))]` |
| OLS slope (direct) | `Σ(xi-x̄)(yi-ȳ) / Σ(xi-x̄)²` | Simpler than r*σy/σx — fewer moving parts |
| OLS slope (via corr) | `r * σy / σx` | Also correct — shows corr↔regression link |
| OLS intercept | `ȳ - slope * x̄` | Regression line passes through (x̄, ȳ) |
| Sum of squares | `sum((xi - avg) ** 2 for xi in lst)` | Use generator expression — memory efficient |
| Slope in English | "For every 1-unit increase in x, y changes by [slope] units" | Must include "1-unit" |
| Sigmoid | `1 / (1 + math.exp(-z))` | Maps ℝ → (0,1) — turns linear combo into probability |
| Logistic gradient | `grad_j = (1/n) * Σ(ŷᵢ-yᵢ)*xᵢⱼ` | Same as linear reg but ŷ = sigmoid(wᵀx) |
| Dot product | `sum(a*b for a,b in zip(x1,x2))` | No numpy — use generator + zip |
| Transpose (no numpy) | `[[row[j] for row in X] for j in range(len(X[0]))]` | List-of-lists column access |
| `is` vs `==` | `is` for None/True/False only; `==` for values | `is "click"` is WRONG — use `== "click"` |
| Dict default get | `d.get(key, 0)` | Cleaner than `if key not in d: d[key] = 0` |
| Dict groupby | `d[k] = d.get(k, 0) + val` | Manual groupby+sum without pandas |
## T-Tests — Which Test + Formulas

| Scenario | Statistic | df |
|----------|-----------|-----|
| 1 sample, σ known | z = (x̄ - μ) / (σ/√n) | — |
| 1 sample, σ unknown | t = (x̄ - μ) / (s/√n) | n-1 |
| 2 sample, equal var | pooled t (below) | n₁+n₂-2 |
| 2 sample, unequal var | Welch's t (below) | Welch-Satterthwaite (below) |

**Pooled variance:** `s²_p = ((n₁-1)s₁² + (n₂-1)s₂²) / (n₁+n₂-2)`
**Pooled t:** `t = (x̄₁-x̄₂) / sqrt(s²_p × (1/n₁ + 1/n₂))`

**Welch's t:** `t = (x̄₁-x̄₂) / sqrt(s₁²/n₁ + s₂²/n₂)`
**Welch's df:** `df = (s₁²/n₁ + s₂²/n₂)² / ((s₁²/n₁)²/(n₁-1) + (s₂²/n₂)²/(n₂-1))`

**P-value:** `2 * scipy.stats.t.sf(abs(t), df)` — sf = 1-CDF
**Quick check:** |t| > 1.96 → p < 0.05 (normal approx, n>30)
**Non-parametric alternatives (no distributional assumptions):**
- **Bootstrap CI:** Resample within each group → diff of means → CI excludes 0 → significant
- **Permutation test:** Pool both groups → shuffle into n₁,n₂ → diff of means → repeat B times → p = fraction ≥ |observed|. Directly simulates H₀.

## A/B Testing

**8-step skeleton:**
1. **Hypothesis** — testable, specific
2. **OEC** — one primary metric
3. **Guardrails** — don't break these
4. **Randomization unit** — user unless spillover ("does treating A change B's outcome?")
5. **Population** — who's eligible
6. **Sample size** — `n = 16σ²/δ²` per group (α=.05, power=.80). MDE = product decision
7. **Duration** — 2+ weeks (DOW, novelty, primacy)
8. **Launch decision** — OEC sig + guardrails safe → ship

**Ramp plan:** 1-5% → monitor → 50/50

**OEC selection hack:** "What single user action, measurable in 2 weeks, best predicts long-term value?"

| Product Type | OEC | Trap |
|---|---|---|
| Search | Successful click rate | "Searches/user" (more = struggling) |
| E-commerce | Revenue per user | Total revenue (traffic-confounded) |
| Social/content | DAU/MAU, time/session | Raw impressions (vanity) |
| Subscription | Trial→paid, weekly retention | Total signups (ignores quality) |
| Ads | Revenue/search + UX penalty | Revenue alone (incentivizes spam) |
| Recs | CTR on recs per user | Impression count |

**Good OEC passes 5 tests:** measurable in 1-4wk, sensitive, directional, hard to game, predicts long-term goal

**Metric tiers in interview:**
1. **OEC** — ship if this improves
2. **Diagnostic** — explains WHY OEC moved (don't decide on these)
3. **Guardrails** — must NOT degrade (latency, crash rate, retention)

**Clarify your tools:**
- **CUPED** = variance reduction in analysis (not randomization)
- **Propensity score** = observational studies (not experiments)
- **Stratified randomization** = balance covariates (e.g., geo) across groups

## Applied Analysis

**3 question types — identify then grab framework:**

| Question sounds like... | Type | Framework |
|---|---|---|
| "What metrics for product X?" | Metric definition | Acquire→Activate→Engage→Retain→Revenue |
| "Metric X dropped, why?" | Diagnostic | WHERE / WHAT / MATCH |
| "Should we launch feature X?" | A/B test design | 8-step skeleton |

**Metric definition — fill in per stage:**

| Stage | What to measure | Example (Podcasts) |
|---|---|---|
| Acquire | New users finding the product | Signups per week |
| Activate | First "aha moment" | % who listen to first episode within 7 days |
| Engage | Regular usage | Listening hours per user per week |
| Retain | Coming back | WAU/MAU, % active after 30 days |
| Revenue | Making money | Premium subs, ad revenue per user |

**Rules:** Always use rates (per time/per user), never raw totals. Pick 1 metric per stage, not 5.

**ML metric selection:**

| Situation | Metric |
|---|---|
| False positives costly (spam, kids content) | Precision |
| Missing positives costly (fraud, cancer) | Recall |
| Balanced | F1 |
| Ranking, no fixed threshold | AUC |
| Top-K results matter (search, recs) | Precision@K, NDCG |
| Need calibrated probabilities | Log loss |

## Modeling & Stats

_(empty — filling during Block 5)_
