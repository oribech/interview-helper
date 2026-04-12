# Interaction Log

Source: google/round1-prep/INTERACTION_LOG.md

# Interaction Log

Each entry = one question/drill interaction. Updated by the agent after each exchange.

---

<!-- Template:
### [Block.Drill] Topic — YYYY-MM-DD HH:MM
- **Question:** ...
- **Your answer:** (brief summary)
- **Verdict:** strong / partial / miss
- **Gap:** (what was missing, if any)
- **Taught:** (what I explained, if any)
- **Re-quiz:** passed / pending / n/a
- **Action:** (cheatsheet added? weak spot logged?)
- **Q asked:** (timestamp when question was presented)
- **A received:** (timestamp when answer was evaluated)
-->

### [1.1] SQL: CTR Over Time — 2026-03-25
- **Question:** Table with Date, Impressions, Clicks — write a query to measure CTR over time.
- **Your answer:** Asked clarifying question about granularity (good). Stated assumptions (daily, 30 days, edge cases). Wrote correct GROUP BY Date query with SUM(Clicks)/SUM(Impressions), WHERE clause for last 30 days, ORDER BY Date. Discussed tradeoffs (group by week/month for sparse data).
- **Verdict:** strong
- **Gap:** Division by zero — mentioned zero impressions as edge case in assumptions but didn't protect against it in the query.
- **Taught:** NULLIF(SUM(Impressions), 0) pattern to prevent division by zero.
- **Re-quiz:** n/a
- **Action:** None — minor gap, pattern taught inline.
- **Timestamp:** 2026-03-25 ~14:30

### [1.2] SQL: YoY CTR Growth with LAG — 2026-03-25
- **Question:** Same table — measure how CTR has grown year over year.
- **Your answer:** Good clarifying questions (output shape, granularity, years available). Correct CTE approach with yearly aggregation + LAG. Used NULLIF (remembered pattern from drill 1).
- **Verdict:** strong (concept), partial (syntax)
- **Gap:** (1) NULLIF missing second arg, (2) LAG missing OVER (ORDER BY) clause, (3) growth formula was ratio not percentage (new/old vs (new-old)/old), (4) FRON typo, (5) unquoted alias with space.
- **Taught:** LAG always needs OVER(ORDER BY), growth% = (new-old)/NULLIF(old,0), EXTRACT(YEAR FROM date) over YEAR().
- **Re-quiz:** n/a — syntax errors, will reinforce in later drills
- **Action:** Added 4 patterns to CHEATSHEET.md (window func syntax, YoY growth, EXTRACT, CTE).
- **Timestamp:** 2026-03-25 ~14:45

### [1.3] SQL: Top-5 Highest-Selling Items — 2026-03-25
- **Question:** Sales table (item_id, item_name, quantity_sold, sale_date) — find top 5 by total quantity.
- **Your answer:** Good assumptions (all dates, name immutability). Used CTE to aggregate then ORDER+LIMIT. Correct GROUP BY 1,2.
- **Verdict:** strong (concept), partial (syntax)
- **Gap:** (1) Missing SELECT * — wrote `Select from`, (2) Wrote LIMIT 10 instead of 5, (3) Unsure if LIMIT applies after GROUP BY — it does (SQL execution order).
- **Taught:** SQL execution order: FROM→WHERE→GROUP BY→HAVING→SELECT→ORDER BY→LIMIT. Can ORDER BY aggregates directly. CTE unnecessary for simple cases.
- **Re-quiz:** n/a
- **Action:** Added execution order to CHEATSHEET.md.
- **Timestamp:** 2026-03-25 ~15:00

### [1.4] SQL: JOIN Types + Anti-Join — 2026-03-25
- **Question:** Users + Purchases tables — count users who never purchased. Explain JOIN types to a PM.
- **Your answer:** Excellent assumptions (completeness, no-signup purchases, duplications, cancellations). Two approaches: NOT IN subquery and LEFT JOIN WHERE NULL. Correct query using NOT IN. Good cross join PM explanation (days×hours example).
- **Verdict:** strong
- **Gap:** (1) Trailing comma syntax error, (2) NOT IN NULL gotcha — returns 0 rows if any NULL in subquery, (3) "elapsed" instead of "overlapping/matching", (4) Missing COUNT(*) — PM asked "how many" not "which ones", (5) LEFT/INNER join PM explanations too jargon-heavy.
- **Taught:** NOT IN breaks on NULLs → prefer LEFT JOIN WHERE NULL or NOT EXISTS. PM-friendly join explanation: Inner = only matches, Left = everyone + matches if they exist.
- **Re-quiz:** n/a
- **Action:** Added anti-join and NOT EXISTS patterns to CHEATSHEET.md. PM explanation: partial pass (cross join good, others need sharpening).
- **Timestamp:** 2026-03-25 ~15:10

### [1.5] SQL: Window Functions — ROW_NUMBER, RANK, DENSE_RANK — 2026-03-25
- **Question:** Employees table — rank by salary within department using all three ranking functions. Explain when to pick each.
- **Your answer:** Assumed no ties (question asked to handle ties). Used ROW_NUMBER with PARTITION BY — right instinct. Honest about not knowing RANK vs DENSE_RANK difference.
- **Verdict:** partial
- **Gap:** (1) PARTITION BY must come before ORDER BY (no comma between), (2) Only wrote ROW_NUMBER — didn't address RANK/DENSE_RANK as asked, (3) Assumed away ties when question explicitly asked about them.
- **Taught:** OVER clause order: PARTITION first, ORDER second. ROW_NUMBER=always unique (dedup). RANK=ties share, skip (1,2,2,4). DENSE_RANK=ties share, no skip (1,2,2,3).
- **Re-quiz:** passed (see 1.5R below)
- **Action:** Added OVER clause order + 3 ranking functions to CHEATSHEET.md. Weak spot: window function details.
- **Timestamp:** 2026-03-25 17:27

### [1.5R] SQL: Re-quiz — DENSE_RANK for Top-3 Revenue Tiers — 2026-03-25
- **Question:** Sales table — top 3 revenue tiers per region, ties share rank, still award #3. Which function + write query.
- **Your answer:** Correctly chose DENSE_RANK with clear reasoning (ROW_NUMBER arbitrary, RANK skips, DENSE_RANK = clean tiers). Correct PARTITION BY before ORDER BY (fixed from 1.5). CTE + WHERE rnk<=3 pattern. Filtered NULLs/zeros. Mentioned COALESCE for null-as-zero case.
- **Verdict:** strong
- **Gap:** Minor — used `rank` as alias (reserved word). Use `rnk` or `dense_rnk`.
- **Taught:** Avoid reserved words as aliases.
- **Re-quiz:** passed
- **Action:** Re-quiz closed. Ranking functions pattern locked in.
- **Timestamp:** 2026-03-25 17:49

### [1.6] SQL: Day-of-Week with Highest CTR — 2026-03-25
- **Question:** Date/Impressions/Clicks table — which day of week most often has the highest CTR?
- **Your answer:** Clear approach: per week find top-CTR day, then count which DOW wins most. Used max_by(dow, ctr) grouped by week, then COUNT+ORDER+LIMIT. Provided ROW_NUMBER fallback in gotchas unprompted. NULLIF applied correctly.
- **Verdict:** strong
- **Gap:** (1) Typo `From ct` → `FROM cte`, (2) Year-boundary bug — week_number alone collides across years, need EXTRACT(YEAR) or DATE_TRUNC('week'). (3) max_by not standard SQL (fine for BigQuery/Google).
- **Taught:** DATE_TRUNC('week', date) is unique across years. max_by is dialect-specific.
- **Re-quiz:** n/a
- **Action:** Added top-N-per-group, week grouping, reserved alias patterns to CHEATSHEET.md.
- **Timestamp:** 2026-03-25 19:09

### [1.7] SQL: A/B Test — Conversion Rate + Avg Purchase — 2026-03-26
- **Question:** Users (user_id, group) + Purchases (user_id, amount, date) — compare conversion rate and avg purchase between control/treatment.
- **Your answer:** Good clarifying question (what is conversion). Correct LEFT JOIN choice. Assumptions solid (Users superset). Mentioned GROUP BY in approach but omitted in query.
- **Verdict:** partial
- **Gap:** (1) Conversion rate formula wrong — wrote SUM(amount)/COUNT(id) instead of COUNT(DISTINCT purchasers)/COUNT(DISTINCT total), (2) Missing GROUP BY in query, (3) No DISTINCT after JOIN (1:many inflation), (4) Missing NULLIF on division, (5) `group` is reserved word.
- **Taught:** Conversion rate = distinct converters / distinct total. After LEFT JOIN use COUNT(DISTINCT) to avoid inflation. Reserved word `group` needs quoting.
- **Re-quiz:** passed (see 1.7R below)
- **Action:** Added conversion rate and JOIN duplicates patterns to CHEATSHEET.md. Weak spot: metric formulas in SQL.
- **Timestamp:** 2026-03-26 14:06

### [1.7R] SQL: Re-quiz — CTR per Campaign + Pct Above 2% — 2026-03-26
- **Question:** Ads table — CTR per campaign, percentage of campaigns with CTR > 2%.
- **Your answer:** CTE with GROUP BY, two queries. Correct concept: sum(boolean)/count(*) for percentage. Noted "no need for distinct" — correct.
- **Verdict:** partial (syntax), strong (concept)
- **Gap:** (1) Missing comma, (2) impressions not aggregated in SUM, (3) second query references alias from first SELECT not CTE, (4) SUM(boolean) not portable — use CASE WHEN.
- **Taught:** CASE WHEN for portable conditional aggregation. Alias scope — CTE columns vs SELECT aliases.
- **Re-quiz:** passed — conversion rate concept understood
- **Action:** None. Syntax errors are recurring theme — will improve with practice.
- **Timestamp:** 2026-03-26 14:18

### [2.1] Python: Bootstrap CI from Scratch — 2026-03-26
- **Question:** 1000 session durations, only random module — compute 95% bootstrap CI for mean.
- **Your answer:** Initially confused bootstrap with parametric CI — good question about why bootstrap. After teaching, wrote correct procedure: resample→mean→collect→percentiles. Wrote quantile function from scratch. Multiple syntax errors.
- **Verdict:** partial (concept understood after teaching, syntax needs work)
- **Gap:** (1) random.choice vs random.choices (singular=1, plural=k), (2) B=10,000 is tuple not int — use 10_000, (3) .sort() mutates — use sorted(), (4) case sensitivity Bootstrap_avgs vs bootstrap_avgs, (5) quantile index comparison wrong (q vs k), (6) import lst not valid.
- **Taught:** Bootstrap procedure (4 steps). random.choices(seq, k=N) for sampling with replacement. sorted() vs .sort(). 10_000 underscore separator.
- **Re-quiz:** passed (see 2.1R below)
- **Action:** Added Python patterns to CHEATSHEET.md.
- **Timestamp:** 2026-03-26 14:58

### [2.1R] Python: Re-quiz — Bootstrap CI for Difference in Means — 2026-03-26
- **Question:** Two groups (control_times, treatment_times) — bootstrap 95% CI for difference in means, only random module.
- **Your answer:** Clean structure with helper functions (quantile, sample, avg). Correct two-group bootstrap: resample each independently, diff means, collect, percentiles. Fixed 10_000 and sorted() from previous drill.
- **Verdict:** strong (concept), partial (syntax)
- **Gap:** (1) random.choices(lst, n) missing k= keyword — 2nd time, (2) quantile index is float not int, (3) hardcoded n from outer scope — should use len(lst) inside sample().
- **Taught:** k= is REQUIRED keyword arg in random.choices. Always int() index. Use len(lst) inside functions.
- **Re-quiz:** passed — bootstrap concept solid, k= recurring issue
- **Action:** None — patterns already in cheatsheet. k= needs muscle memory.
- **Timestamp:** 2026-03-26 17:12

### [2.2] Python: Linear Regression OLS from Scratch — 2026-03-26
- **Question:** Given x, y lists — compute slope and intercept using OLS. Explain slope in plain English.
- **Your answer:** Built helper functions (avg, ssq, corr). Used slope = r * σy/σx formula — correct. Intercept = ȳ - slope*x̄ — correct. Bessel's correction (n-1) applied. Generator expression in ssq.
- **Verdict:** strong
- **Gap:** (1) Variable names swapped in corr (den=numerator, numer=denominator), (2) No assumptions stated, (3) Slope explanation missing "per 1-unit increase" specificity.
- **Taught:** Direct OLS formula: slope = Σ(xi-x̄)(yi-ȳ)/SSx. Slope = "for every 1-unit increase in x, y changes by [slope] units."
- **Re-quiz:** n/a — math correct
- **Action:** None.
- **Timestamp:** 2026-03-26 17:46

### [2.3] Python: Logistic Regression / Sigmoid + Gradient Step — 2026-03-26
- **Question:** Implement sigmoid, then one gradient descent step for logistic regression. No numpy. Explain sigmoid.
- **Your answer:** Knew sigmoid immediately. Didn't know logistic gradient — taught in 4 lines. Then implemented correctly: dot, predict, grad, transpose, gradient_step. All helper functions clean with generators.
- **Verdict:** strong (after teaching)
- **Gap:** (1) `n_cols = X[0]` missing `len()`, (2) typo `erros`.
- **Taught:** Logistic gradient: predict→error→grad_j=(1/n)Σ(err*xij)→update. Same as linear regression but with sigmoid predictions.
- **Re-quiz:** n/a — implemented correctly after teach
- **Action:** PM explanation: passed. Cheatsheet updated with sigmoid, logistic gradient, dot, transpose.
- **Timestamp:** 2026-03-26 18:59

### [2.4] Python: Data Manipulation (no Pandas) — 2026-03-26
- **Question:** List of dicts — filter by event type, fill nulls, group by user_id and sum value.
- **Your answer:** List comprehension for filter, for-loop mutation for null fill, dict accumulation for groupby. Clean, readable approach.
- **Verdict:** strong (concept), partial (syntax)
- **Gap:** (1) `is "click"` — `is` checks identity not value, must use `==` for strings. `is` only for None/True/False. (2) `events['value']` plural instead of `event['value']` singular — TypeError.
- **Taught:** `is` vs `==` rule. `.get(key, default)` as cleaner alternative to if-not-in-dict pattern.
- **Re-quiz:** n/a — minor bugs
- **Action:** Add `is` vs `==` and `.get()` to cheatsheet.
- **Timestamp:** 2026-03-26 21:56

### [2.5] Python: Two-Sample T-Test from Scratch — 2026-03-27
- **Question:** Compute t-statistic and p-value for two-sample t-test. No scipy for t-stat.
- **Your answer:** Wrote variance, pooled_variance, t_statistic, t_test (normal approx), t_pval (scipy). Good structure. Asked smart follow-up questions (when pooled, cheatsheet for cases, bootstrap alternative).
- **Verdict:** partial
- **Gap:** (1) Pooled variance weights by n instead of n-1 (df), denominator n1+n2 instead of n1+n2-2, (2) t-statistic missing (1/n1 + 1/n2) factor — SE = sqrt(s²_p × (1/n1+1/n2)), not sqrt(s²_p).
- **Taught:** Pooled var formula with df weights. SE of difference needs (1/n1+1/n2). Welch's t as simpler alternative (no pooling). Bootstrap CI as non-parametric alternative.
- **Re-quiz:** pending — t-stat formula
- **Action:** Added pooled var, pooled t, Welch's t, quick sig check, p-value patterns to cheatsheet.
- **Timestamp:** 2026-03-27 14:12

### [2.6] Python: IQR Outlier Detection — 2026-03-27
- **Question:** Write function to find outliers using IQR method (< Q1-1.5×IQR or > Q3+1.5×IQR). No numpy.
- **Your answer:** Clean implementation with get_quantile, get_iqr, find_outliers. Correct formula and list comprehension filter.
- **Verdict:** strong
- **Gap:** get_quantile doesn't sort the data — returns wrong value on unsorted input. Need `sorted(data)`.
- **Taught:** Always sort before indexing for quantile.
- **Re-quiz:** n/a — minor bug
- **Action:** None.
- **Timestamp:** 2026-03-27 15:10

### [2.7] Python: Generate N Normal Samples — 2026-03-27
- **Question:** Generate N samples from normal distribution using only random module. Box-Muller.
- **Your answer:** Knew random.gauss(mean, std) — pragmatic. Attempted Box-Muller from scratch. Both approaches with list comprehension.
- **Verdict:** strong (gauss), partial (Box-Muller)
- **Gap:** Box-Muller formula: (1) missing sqrt, (2) + instead of *. Correct: sqrt(-2*ln(u1)) * cos(2π*u2).
- **Taught:** Box-Muller formula. Lead with random.gauss in interview.
- **Re-quiz:** n/a — random.gauss is the practical answer
- **Action:** None.
- **Timestamp:** 2026-03-27 15:27

### [2.8] Python: Bernoulli Matrix + Column Normalization — 2026-03-27
- **Question:** Generate m×n Bernoulli(p) matrix, divide each element by its column sum. No numpy.
- **Your answer:** Correct structure: generate→col sums→normalize. get_cols_sums clean. float(bool) trick for Bernoulli.
- **Verdict:** strong
- **Gap:** (1) Missing p parameter — hardcoded 0.5, (2) typo `appened`, (3) no division-by-zero guard for all-zero columns.
- **Taught:** random.random() < p for Bernoulli(p). Guard zero column sums.
- **Re-quiz:** n/a
- **Action:** None.
- **Timestamp:** 2026-03-27 15:41

### [2.9] Python: Sum of Two Squares — 2026-03-27
- **Question:** Count ways to express n as sum of two perfect squares (order matters).
- **Your answer:** Iterate i from 0 to sqrt(n), check if n-i² is perfect square. Correct logic, both orderings handled.
- **Verdict:** strong
- **Gap:** (1) is_square doesn't return False — returns None implicitly, (2) floating point risk on large numbers (use round+verify), (3) no edge case assumptions stated.
- **Taught:** Safer perfect square check: `r = int(n**0.5 + 0.5); return r*r == n`. Edge check habit.
- **Re-quiz:** n/a
- **Action:** None.
- **Timestamp:** 2026-03-27 16:10

### [3.1] A/B Testing: Experiment Design Framework — 2026-03-27
- **Question:** Walk through how you'd design an A/B test (Maps "save parking spot" feature).
- **Your answer:** Named all key steps. Hypothesis + OEC + guardrails correct. Duration reasoning good. Got confused on randomization: mixed up CUPED (analysis), propensity score (observational), and stratified randomization (what they actually wanted). Sample size formula roughly remembered. Missing ramp plan and launch decision.
- **Verdict:** partial
- **Gap:** (1) CUPED is analysis not randomization, (2) propensity score is for observational not experiments, (3) user-level randomization is fine when no spillover, (4) missing ramp plan + launch decision steps, (5) gave a list not a fleshed-out answer.
- **Taught:** When to use user vs cluster randomization (spillover test). CUPED vs propensity vs stratified. 8-step skeleton. n=16σ²/δ² formula.
- **Re-quiz:** pending — full verbal walkthrough
- **Action:** Added 8-step skeleton and tool clarifications to CHEATSHEET.md. Weak spot: randomization strategy selection.
- **Q asked:** 2026-03-27 ~17:00
- **A received:** 2026-03-27 17:20

### [3.2] A/B Testing: Google Play 10% Discount — 2026-03-28
- **Question:** "We offered users 10% off at Google Play last weekend. Was it successful?"
- **Your answer:** OEC: revenue per user. Guardrails: uncertain. Randomization: user-level. Duration: 2 weeks. MDE: tried to tie to break-even but math off (used 5% instead of 11%).
- **Verdict:** partial
- **Gap:** (1) Didn't clarify if A/B test vs everyone got it (critical first question), (2) discount guardrails: forward shifting + bargain hunters, (3) MDE break-even: 1/0.9-1=11% not 5%.
- **Taught:** First clarify A/B vs universal. Discount guardrails. MDE tied to business break-even.
- **Re-quiz:** deferred — switching to Block 3 (Applied Analysis) after frustration
- **Action:** Reordered plan: Applied Analysis + Quick Fills first, A/B testing moved to Block 5.
- **Q asked:** 2026-03-27 ~17:30
- **A received:** 2026-03-28 19:27

### [3.1] Applied Analysis: Measure Success of Google Maps — 2026-03-29
- **Question:** "How would you measure success of Google Maps?"
- **Your answer:** Clarified scope (navigation). OEC: routes completed/user. Secondary: time to start route. Quality: rerouting/user. After coaching: refined rerouting to ETA accuracy, added retention (WAU/MAU) and guardrails (latency, battery).
- **Verdict:** partial → strong after coaching
- **Gap:** (1) Initial answer missing retention/satisfaction, (2) rerouting is ambiguous — split user-initiated vs Maps-suggested or use ETA accuracy instead.
- **Taught:** ETA accuracy as quality metric. WAU/MAU for retention. Think across user journey stages not just engagement.
- **Re-quiz:** n/a
- **Action:** None.
- **Q asked:** 2026-03-28 23:16
- **A received:** 2026-03-29 13:20

### [3.2] Applied Analysis: Snapchat DAU Drop — 2026-03-29
- **Question:** "Snapchat saw 5% DAU drop over past week. Investigate."
- **Your answer:** Ran 4 checks correctly when prompted. Identified iOS camera redesign as cause after interviewer revealed data. Needed coaching on the overlap/match concept.
- **Verdict:** partial (needed help phrasing questions + understanding match concept)
- **Taught:** WHERE/WHAT/MATCH framework. Compare affected vs unaffected group.
- **Q asked:** 2026-03-29 17:43
- **A received:** 2026-03-29 ~18:00

### [3.2b] Applied Analysis: YouTube Watch Time Drop — 2026-03-29
- **Question:** "YouTube watch time dropped 8% this month. Investigate."
- **Your answer:** Stated framework correctly but couldn't generate questions. Teaching moment.
- **Verdict:** partial (knew steps, couldn't execute as questions)
- **Taught:** Compare to same period last year to distinguish seasonal vs new cause.
- **Q asked:** 2026-03-29 18:05
- **A received:** 2026-03-29 ~18:15

### [3.2c] Applied Analysis: Gmail Open Rate Drop — 2026-03-29
- **Question:** "Gmail open rate dropped 10% this month. Investigate."
- **Your answer:** Asked all 5 questions. Correctly identified spam filter as stronger hypothesis over tax season. Proposed validation: compare spam rate before/after filter change.
- **Verdict:** strong
- **Q asked:** 2026-03-29 19:33
- **A received:** 2026-03-29 ~19:40

### [3.2d] Applied Analysis: Google Maps Trip Duration Increase — 2026-03-29
- **Question:** "Google Maps trip duration increased 12%. Investigate."
- **Your answer:** All 5 checks unprompted with product-specific reasoning (two data sources, construction hypothesis). Correctly identified need to match algorithm rollout cities with duration increase.
- **Verdict:** strong
- **Q asked:** 2026-03-29 19:42
- **A received:** 2026-03-29 19:48

### [3.4] Applied Analysis: Google Podcasts Metrics — 2026-03-30
- **Question:** "Google launches Podcasts. What metrics to track?"
- **Your answer:** Filled full AARRR funnel: signups/week, % first episode in 7 days, listening hrs/user/week, WAU/MAU, revenue/user. Needed coaching on activation (had engagement first) and retain.
- **Verdict:** partial → strong after coaching
- **Taught:** Activation = first aha moment, not ongoing usage. Retain = WAU/MAU. Always use rates not totals.
- **Q asked:** 2026-03-29 20:43
- **A received:** 2026-03-30 ~13:55

### [3.5] Applied Analysis: Google Maps Fake Reviews — 2026-03-30
- **Question:** "Google Maps has fake reviews. How to detect?"
- **Your answer:** Good clarification (what counts as fake). Features: reviewer metadata, history, business data. Model: classification (logistic/RF + CV). Metric: identified precision/recall tradeoff, chose recall for trust.
- **Verdict:** strong
- **Taught:** Human review queue for borderline cases. Interview tip: acknowledge both sides of tradeoff.
- **Q asked:** 2026-03-30 13:49
- **A received:** 2026-03-30 14:05

### [3.6] Applied Analysis: Clarifying Questions Practice — 2026-03-30
- **Question:** 3 vague prompts — write clarifying questions for each.
- **Your answer:** By prompt 3, generated 4 checks (data, segment, internal, external) unprompted.
- **Verdict:** strong
- **Q asked:** 2026-03-30 ~14:08
- **A received:** 2026-03-30 ~14:11

### [3.G1] Gate Test: Google Fit Metrics — 2026-03-30
- **Question:** "Google launches fitness tracker. What metrics?"
- **Your answer:** Full AARRR but swapped activate/engage, missed retain.
- **Verdict:** partial
- **Q asked:** 2026-03-30 14:11
- **A received:** 2026-03-30 ~14:20

### [3.G2] Gate Test: Google Translate Accuracy Drop — 2026-03-30
- **Question:** "Translate accuracy dropped 15%. Investigate."
- **Your answer:** All 4 checks, identified model update matching 12 languages. No help.
- **Verdict:** strong
- **Q asked:** 2026-03-30 ~14:20
- **A received:** 2026-03-30 ~14:25

### [3.G3] Gate Test: Gmail Auto-Categorize — 2026-03-30
- **Question:** "Build email auto-categorization. How?"
- **Your answer:** Got structure but needed nudges on features, metric, tradeoff.
- **Verdict:** partial
- **Q asked:** 2026-03-30 ~14:25
- **A received:** 2026-03-30 ~14:33

### [3.R1] Re-drill: Language Learning App Metrics — 2026-03-30
- **Question:** "Google launches language learning app. Metrics?"
- **Your answer:** Full AARRR, all stages correct, activate = real action, retain included.
- **Verdict:** strong
- **Q asked:** 2026-03-30 14:35
- **A received:** 2026-03-30 ~14:40

### [3.R2] Re-drill: Google Photos Face Clustering — 2026-03-30
- **Question:** "Auto-detect and group photos by people. How?"
- **Your answer:** All 5 stages: clarify (foreground/background), features (images), model (neural net), metric (accuracy), tradeoff (recall vs precision).
- **Verdict:** strong
- **Q asked:** 2026-03-30 ~14:40
- **A received:** 2026-03-30 ~14:45

### [3.R3] Gate Re-test: Carpooling Metrics — 2026-03-30
- **Question:** "Google Maps carpooling feature. Metrics?"
- **Your answer:** All stages, creative acquire (feature discovery), specific actions per stage.
- **Verdict:** strong
- **Q asked:** 2026-03-30 ~14:45
- **A received:** 2026-03-30 ~14:48

### [3.R4] Gate Re-test: Phishing Detection — 2026-03-30
- **Question:** "Auto-detect phishing emails. How?"
- **Your answer:** Full framework: clarify, features, model, metric (precision > recall with reasoning), tradeoff.
- **Verdict:** strong
- **Q asked:** 2026-03-30 ~14:48
- **A received:** 2026-03-30 14:52

---

## MOCK TEST 1 — 2026-03-30

### [M1.1] Mock — Coding: SQL (Zero-Click Searches) — 2026-03-30
- **Question:** SearchQueries + Clicks tables — find percentage of searches with zero clicks by month.
- **Your answer:** Correct LEFT JOIN + NULL approach. Gave count instead of percentage. Used SUM(IS NULL) which is dialect-dependent.
- **Verdict:** partial
- **Gap:** (1) Gave count not percentage — need COUNT(CASE)/COUNT(*), (2) SUM(boolean) not portable.
- **Q asked:** 2026-03-30 ~15:00
- **A received:** 2026-03-30 ~15:10

### [M1.2] Mock — Coding: Python (Session Stats) — 2026-03-30
- **Question:** Function returning mean, median, std from list of session lengths. No libraries.
- **Your answer:** Right structure with dict. Mean correct. Median missing sort. Std had undefined variables (x instead of arr, avg not stored).
- **Verdict:** partial
- **Gap:** (1) Median needs sorted(), (2) undefined variables in std formula, (3) missing storing avg before reuse.
- **Q asked:** 2026-03-30 ~15:00
- **A received:** 2026-03-30 ~15:10

### [M1.3] Mock — Applied Analysis: YouTube Music Bundle — 2026-03-30
- **Question:** "YouTube Premium offered free 3-month YouTube Music trial. Should we make bundle permanent?"
- **Your answer:** Jumped to OEC (conversion rate) and guardrails without clarifying. Froze when question didn't fit a clean framework. Didn't ask if holdout group existed. Didn't frame as business case (does revenue exceed cost).
- **Verdict:** weak
- **Gap:** (1) No clarification first, (2) didn't identify this as A/B + business case hybrid, (3) conversion rate not specified (of what?), (4) froze.
- **Q asked:** 2026-03-30 ~15:10
- **A received:** 2026-03-30 ~15:20

### [M1.4] Mock — Measurement: Bias-Variance Tradeoff — 2026-03-30
- **Question:** "Explain bias-variance tradeoff. Example of high-bias and high-variance model."
- **Your answer:** Good dart analogy. Named boosting/bagging but swapped them (corrected when pointed out).
- **Verdict:** strong
- **Gap:** Swapped boosting (reduces bias) and bagging (reduces variance).
- **Q asked:** 2026-03-30 ~15:20
- **A received:** 2026-03-30 ~15:30

### [M1.5] Mock — Measurement: Overfitting — 2026-03-30
- **Question:** "Model good on train, bad on test. What's happening, what to do?"
- **Your answer:** Overfitting. Check data leakage, add regularization, better CV.
- **Verdict:** strong
- **Q asked:** 2026-03-30 ~15:30
- **A received:** 2026-03-30 ~15:33

### [M1.6] Mock — Measurement: L1 vs L2 Regularization — 2026-03-30
- **Question:** "Difference between L1 and L2. When to use each?"
- **Your answer:** L1 = abs penalty, zeros out coefficients (feature selection). L2 = square penalty, shrinks but keeps all.
- **Verdict:** strong
- **Q asked:** 2026-03-30 ~15:33
- **A received:** 2026-03-30 ~15:38

### Mock 1 Summary

| Section | Verdict |
|---|---|
| Coding — SQL | Partial |
| Coding — Python | Partial |
| Applied Analysis & Experiments | Weak |
| Measurement & Modeling (3 Qs) | Strong |

**Key gaps to address:**
1. Applied Analysis: hybrid business case + experiment questions (not clean single-framework)
2. Coding: percentage calculations, variable scoping in Python
3. Boosting vs bagging direction

- **Q asked:** 2026-03-30 ~15:00
- **A received:** 2026-03-30 15:43

### [5.3] A/B Test Design: YouTube AI Chapter Markers — 2026-03-30
- **Question:** "YouTube tests AI-generated chapter markers. Design an A/B test."
- **Your answer:** Hit all 8 steps. Hypothesis: chapters increase session watch time for long videos. OEC: watch time per user per session. Guardrails: ad revenue, creator satisfaction. Randomization: user-level (no network effects). Sample size: 16σ²/δ². Duration: initially said 1 week, should be 2. Launch: OEC sig + guardrails safe.
- **Verdict:** strong
- **Gap:** (1) Population too broad ("YouTube users" — should be users who watch long videos), (2) Talked self out of 2 weeks into 1 week, (3) Needed help resolving watch-time paradox (per-session not per-video).
- **Taught:** Measure at session level to resolve per-video paradox. Population = narrow to relevant users. Stick with 2 weeks for novelty/primacy.
- **Re-quiz:** n/a
- **Action:** None.
- **Q asked:** 2026-03-30 18:13
- **A received:** 2026-03-30 18:38

### [5.4] A/B Testing Pitfalls: Should We Ship? — 2026-03-30
- **Question:** "A/B test shows 5% lift in signups, p=0.03. Manager wants to ship. What concerns?"
- **Your answer:** (1) Check statistical assumptions (normality), (2) Experiment validity: novelty, primacy, seasonality, network effects, selection bias, randomization, (3) Practical significance — does 5% justify shipping cost.
- **Verdict:** strong
- **Gap:** Could also mention guardrails (counter-metrics) and multiple testing correction.
- **Taught:** Guardrails check + multiple testing as additional concerns.
- **Re-quiz:** n/a
- **Action:** None.
- **Q asked:** 2026-03-30 ~18:40
- **A received:** 2026-03-30 18:47

### [5.5] Sample Size + MDE: Google Store Checkout — 2026-03-30
- **Question:** "New checkout flow, CVR=3%. How many users for the test?"
- **Your answer:** Correctly asked PM for MDE first. Used n=16σ²/δ². Computed σ²=p(1-p)=0.0291, δ=0.005, n≈18,600 per group. Initially confused σ² with σ²/n (variance of mean vs population variance) — clarified.
- **Verdict:** strong
- **Gap:** σ² in the formula is population variance, not standard error.
- **Taught:** For binary metric σ²=p(1-p). The formula already divides by n — don't double-divide.
- **Re-quiz:** n/a
- **Action:** None.
- **Q asked:** 2026-03-30 ~18:48
- **A received:** 2026-03-30 19:23

### [5.6] Business Case: Promo Evaluation — 2026-04-12
- **Question:** "YouTube Premium ran 3-month free trial promo (vs standard 1-month) for all Q1 signups. No holdout. Should we make it permanent?"
- **Your answer:** Good clarifying Q (was A/B test done?). Identified DiD as causal method but didn't know it — taught. Correctly identified "no clean control" problem. Sharp question about PSM/matching/meta-learners. Chose revenue as primary metric with cannibalization reasoning. Identified need for stat + practical significance. LTV-CAC framing (wrong — should be incremental value vs cost). Couldn't deliver structured pitch.
- **Verdict:** partial
- **Gap:** (1) Didn't know DiD, (2) needed heavy prompting throughout — couldn't drive the analysis independently, (3) LTV-CAC vs incremental framing, (4) missed observation window truncation + zero-inflated revenue + sample size, (5) couldn't deliver Assumptions→Approach→Recommendation pitch
- **Taught:** DiD (5-line teach), selection bias / post-treatment conditioning, incremental value vs cost framing, full funnel evaluation (acquisition + conversion + retention + LTV), ship/no-ship rule (practical sig + stat sig + guardrails), Assumptions→Approach→Recommendation structure with worked example
- **Re-quiz:** pending — DiD design (iOS onboarding scenario) + structured pitch delivery
- **Action:** Weak spot: structured verbal delivery. Weak spot: quasi-experimental methods (DiD, PSM, ITS).
- **Q asked:** 2026-04-11 22:38
- **A received:** 2026-04-12 14:10
