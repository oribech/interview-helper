# A/B Testing Interview Prep — Complete Notes

Source: google/study/ab-testing/ab_testing_complete_notes.md

# A/B Testing Interview Prep — Complete Notes

Source: "Trustworthy Online Controlled Experiments" (Chapters 1-3, 5-6, 14-15, 17-19)
Compiled from Claude Code conversation (2026-03-15)

---

## Table of Contents

1. [Why A/B Test at All](#block-1-why-ab-test-at-all)
2. [Designing an Experiment](#block-2-designing-an-experiment)
3. [Interpreting Results](#block-3-interpreting-results)
4. [Metrics](#block-4-metrics)
5. [Randomization Unit](#block-5-randomization-unit)
6. [Ramping / Launching](#block-6-ramping--launching)
7. [Statistics Core](#block-7-statistics-core)
8. [Variance and Sensitivity](#block-8-variance-and-sensitivity)
9. [A/A Tests](#block-9-aa-tests)
10. [Key Explanations from Q&A](#key-explanations-from-qa)
11. [Mock Interview Questions](#mock-interview-questions)
12. [Common Traps](#common-traps)
13. [Hands-On Lab Summary](#hands-on-lab-notebook)

---

## Block 1: Why A/B Test at All

### The core insight

Netflix sees X% churn. They add a feature. Users of that feature churn at X/2%. Does the feature reduce churn?

**NO.** Heavy users both use features more AND churn less. The feature didn't cause anything — the usage pattern did.

This is called **confounding**: a hidden variable (user engagement) affects both the thing you're measuring (churn) and the thing you changed (feature adoption).

**The ONLY way to prove causation:** randomly assign users to Treatment (sees feature) and Control (doesn't). Then compare. That's an A/B test.

### Key term — OEC (Overall Evaluation Criterion)

The ONE metric you care about most.

- Not "profit" — too slow to measure, gameable with price hikes
- Something measurable in 1-2 weeks that predicts long-term success
- Example: revenue-per-user (not total revenue, because group sizes vary by chance)

### Hierarchy of evidence (strongest → weakest)

1. Meta-analysis of multiple experiments
2. Randomized controlled experiments (A/B tests)
3. Non-randomized experiments
4. Observational studies
5. Expert opinion (HiPPO — Highest Paid Person's Opinion)

### Drill

> "If I see users of feature X churn less, I still can't say the feature reduces churn. Why? Because adoption wasn't random. Engaged users self-select into the feature AND churn less. I need a randomized experiment to separate the two."

### Q&A

- **Q: PM says "users who use our new search filter buy 2x more, let's invest more in it." What's wrong?**
  A: Selection bias. Users who use search filter are probably already high-intent buyers. You'd need to randomly show/hide the filter to prove it causes more purchases.

- **Q: What is an OEC? Why not just use "profit"?**
  A: OEC = the primary metric for your experiment. Profit is bad because (a) too slow to measure in a 2-week test, (b) short-term profit tricks like raising prices can hurt long-term. Use something like revenue-per-user.

- **Q: Why is an A/B test better than looking at before/after data?**
  A: Before/after has no control group. Seasonality, other launches, external events all change metrics over time. An A/B test runs Treatment and Control simultaneously, so these effects cancel out.

---

## Block 2: Designing an Experiment

### Real example

An e-commerce site wants to add a coupon code field to checkout.

**The problem:** You're buying shoes. About to pay. Then you see a box that says "Enter Coupon Code." Now you think: "Wait, there's a coupon I'm missing?" You leave checkout to Google for a coupon. Many people never come back to finish buying. **The coupon box itself — even with zero coupons existing — costs you sales just by being there.**

That's why they A/B tested it before building a real coupon system.

### The 5-step design process

| Step | What | Example |
|------|------|---------|
| 1. Hypothesis | What you think will happen | "Adding coupon field will decrease revenue" |
| 2. Metrics | OEC + guardrails | OEC: revenue-per-user. Guardrails: latency, crash rate |
| 3. Randomization unit | What gets randomly assigned | Users (not pages, not sessions) |
| 4. Population | Who's included in analysis | Users who START checkout (not all visitors) |
| 5. Size & duration | How long, how many | Enough power to detect 1% change; min 1 week |

### Why "users who start checkout" as population?

- All visitors: too noisy, most never reach checkout
- Only purchasers: **WRONG!** If coupon field PREVENTS purchases, those users vanish from your denominator
- Users who start checkout: includes everyone potentially affected, excludes noise

### Duration rules of thumb

- Minimum 1 week (captures weekday/weekend differences)
- Longer if you suspect novelty or primacy effects
- Consider seasonality (holidays, back-to-school)

### Guardrails explained

**Guardrails = "don't break stuff while you test."**

You're testing if the coupon field hurts revenue. But what if your new code also makes the page load 5 seconds slower, or crashes for 10% of users? You'd lose money for a reason that has nothing to do with the coupon.

So you watch guardrails like page speed and crash rate. If those move, your test is broken — fix that first before judging the coupon.

### Drill

> "To design an A/B test I need: hypothesis, metrics with an OEC and guardrails, randomization unit, target population, and power analysis for size and duration. I always run at least one full week."

### Q&A

- **Q: Walk through designing an A/B test for adding "recommended for you" on homepage.**
  A: (1) Hypothesis: adding recs increases engagement and purchase rate. (2) OEC: clicks-per-user or revenue-per-user; guardrails: page load time, other-section CTR. (3) Randomization: user-level. (4) Population: all homepage visitors. (5) Power analysis for 1% detectable change, run 1-2 weeks.

- **Q: Why run for at least 1 full week?**
  A: User behavior differs on weekdays vs weekends. If you only run Mon-Wed, you miss weekend patterns. A full week captures the weekly cycle.

- **Q: Testing a checkout change — OEC denominator: all site visitors or users who reach checkout?**
  A: Users who reach checkout. All visitors adds noise from people who never interact with the change. But NOT only purchasers — that would exclude people the change scared away.

---

## Block 3: Interpreting Results

### Real results from the book (coupon field experiment)

| Variant | Rev/user (Treatment) | Rev/user (Control) | Diff | p-value | 95% CI |
|---------|---------------------|--------------------|----- |---------|--------|
| Treatment 1 vs Control | $3.12 | $3.21 | -2.8% | 0.0003 | [-4.3%, -1.3%] |
| Treatment 2 vs Control | $2.96 | $3.21 | -7.8% | 1.5e-23 | [-9.3%, -6.3%] |

### How to read this

- **p-value < 0.05** = statistically significant = unlikely to be random noise
- **p-value IS NOT** "probability the null is true." It's "probability of seeing this data IF there were no real difference"
- **Confidence interval** [-4.3%, -1.3%] = we're 95% sure the true effect is somewhere in this range. Zero is NOT in the range, so it's significant.
- **Practical significance**: Is the effect big enough to matter? A 0.01% change might be statistically significant with millions of users but not worth acting on. For Google/Bing, even 0.2% matters (billions in revenue). For a startup, maybe 10%+ is the bar.

### The 6 decision scenarios (comes up in interviews)

| # | Stat sig? | Practically sig? | Decision |
|---|-----------|-----------------|----------|
| 1 | No | No | Easy: no effect. Iterate or drop. |
| 2 | Yes | Yes | Easy: launch! |
| 3 | Yes | No | Effect is real but tiny. Probably not worth the cost. |
| 4 | No | No (wide CI) | Underpowered. Can't conclude anything. Run bigger test. |
| 5 | No | Probably yes | Promising but noisy. Rerun with more power. |
| 6 | Yes | Probably yes | Likely worth it but CI is wide. Consider rerunning or just launch. |

### Guardrail metrics / invariants

Before trusting results, check things that SHOULD NOT change:

- Sample sizes should match the configured split (e.g., 50/50)
- Latency shouldn't change if your change is UI-only
- If these invariants move, your experiment has a bug. **Don't trust the results.**

### Twyman's Law

> "Any figure that looks interesting or different is usually wrong."

If results look too good, check for bugs first.

### Q&A

- **Q: p-value is 0.03 and effect is +0.5% revenue. Launch?**
  A: Depends on practical significance. Is 0.5% revenue meaningful for this business? For Google, yes (millions of dollars). For a small app, maybe not worth the engineering maintenance cost. Also check guardrails.

- **Q: You see a +15% lift. First reaction?**
  A: Twyman's Law — be suspicious. +15% is unusually large. Check for bugs: SRM, logging errors, bot traffic, data pipeline issues. If it checks out, great — but verify first.

- **Q: Treatment has 48% users, Control 52%, but you configured 50/50. What do you do?**
  A: This is a **Sample Ratio Mismatch (SRM)**. Something is wrong with randomization or data collection. DO NOT trust the experiment results. Investigate the cause before drawing any conclusions.

---

## Block 4: Metrics

### Three types of metrics

| Type | What | Example | Moves fast? |
|------|------|---------|-------------|
| **Goal metric** | Ultimate success measure | Monthly active users, long-term revenue | No, slow |
| **Driver metric** | Leading indicator of goal | Session length, CTR, 7-day retention | Yes |
| **Guardrail metric** | "Don't break this" | Page load time, crash rate, error rate | Should not move |

### Good OEC characteristics

- Measurable in short time (1-2 weeks)
- Sensitive enough to detect real changes
- Hard to game
- Predictive of long-term goal

### Bad OEC examples

- "Profit" — too slow, gameable (raise prices)
- "Clicks" alone — gameable (clickbait)
- CTR sometimes bad because you can increase it by removing good results

### Metric frameworks

- **HEART**: Happiness, Engagement, Adoption, Retention, Task success
- **AARRR (Pirate)**: Acquisition, Activation, Retention, Referral, Revenue

### Speed matters (real examples)

- **Amazon**: 100ms slowdown = 1% decrease in sales
- **Bing**: every 10ms improvement paid for an engineer's salary for a year
- Always have page load time as a guardrail metric

### Q&A

- **Q: New recommendation engine — what's your OEC and guardrails?**
  A: OEC: CTR on recommendations, or revenue-per-user from recommended items. Guardrails: page load time (recs can slow pages), overall CTR (make sure recs don't cannibalize organic results), error rate.

- **Q: "Number of searches per user" as OEC for a search engine. Good or bad?**
  A: Bad. More searches might mean users CAN'T FIND what they want. A user who searches once and finds the answer is happier than one who searches 5 times. Better OEC: sessions with successful click, time-to-success, or absence of query reformulation.

- **Q: Difference between goal and driver metric?**
  A: Goal metric = the ultimate thing you care about (e.g., long-term revenue). Moves slowly, hard to measure in 2 weeks. Driver metric = a shorter-term proxy that predicts the goal (e.g., weekly retention rate). You use driver metrics as your OEC because they're measurable in experiment timeframes.

---

## Block 5: Randomization Unit

### Three granularity levels

| Unit | What it means | Pro | Con |
|------|--------------|-----|-----|
| **Page-level** | Each pageview randomly assigned | Huge sample size, more power | Same user sees different variants! Bad UX. |
| **Session-level** | All pages in one visit get same variant | Better than page-level | User returns next day, might get different variant |
| **User-level** | A user always sees same variant | Consistent experience, can measure retention | Need more users for same power |

### User-level is the default. Why?

- Consistent experience (user doesn't see feature appear/disappear)
- Can measure long-term metrics (retention, lifetime value)
- Satisfies SUTVA (Stable Unit Treatment Value Assumption): units don't interfere with each other

### User ID options

- Signed-in user ID: best, works cross-device
- Cookie: common, but lost on browser clear / incognito
- Device ID: stable longitudinally but different per device

### Critical rule: randomization unit >= analysis unit

- Randomize by user, analyze by user = **fine**
- Randomize by user, analyze by pageview = **DANGEROUS**
  - Pageviews from same user are correlated
  - Variance formula assumes independence
  - You'll underestimate variance → too many false positives
  - Your A/A tests will fail

### Q&A

- **Q: Why is user-level randomization the most common choice?**
  A: Consistent user experience (no flickering between variants), ability to measure user-level metrics like retention, satisfies independence assumption when analyzing per-user metrics.

- **Q: You randomize by user but compute CTR per page. Why is this a problem?**
  A: Pages from the same user are correlated (not independent). Standard variance formula assumes i.i.d. samples. Using it on correlated page-level data underestimates variance → confidence intervals too narrow, p-values too small → false positives. Use the delta method or bootstrap instead.

- **Q: When might you NOT use user-level randomization?**
  A: Infrastructure changes (e.g., comparing hosting providers — randomize by IP or data center). Or when you specifically want sub-user metrics. Also: ad auctions might randomize by advertiser cluster.

---

## Block 6: Ramping / Launching

### SQR Framework

When ramping an experiment, balance:

- **Speed** — how fast you iterate
- **Quality** — how precise your measurement is
- **Risk** — how much damage a bad variant can do

### Four ramp phases

| Phase | Traffic | Purpose |
|-------|---------|---------|
| **Pre-MPR** | 0.5%-5% | Catch bugs. Use internal "rings": team → employees → beta → small % of real users |
| **MPR** (Maximum Power Ramp) | ~50% Treatment | Precise measurement. Run ~1 week min. This is where you measure the real effect. |
| **Post-MPR** | 75%-100% | Operational readiness. Can system handle full load? |
| **Long-term holdout** | 95-100% + 5-10% holdout | Keep small group on control for months to measure long-term effects |

### Why not 100% on day one?

- Healthcare.gov launched to 100%, site collapsed
- Bad feature with 1% exposure hurts few users; at 100% it's a disaster
- You can't measure anything if the system is down

### MPR = 50/50 for one Treatment. Why?

- Variance of t-test is proportional to 1/(q(1-q)) where q = treatment fraction
- Minimized at q=0.5, so 50/50 gives maximum statistical power

### Q&A

- **Q: Launching a new ML ranking model. Describe your ramp plan.**
  A: (1) Pre-MPR: ship to team internally, then 1% of users. Monitor guardrails (latency, errors, crashes). (2) MPR: ramp to 50/50, run for 1 week+, measure OEC. (3) Post-MPR: if positive, ramp to 100% while monitoring operational metrics. (4) Optional: keep 5% holdout for 2 months.

- **Q: Why is 50/50 the maximum power ramp?**
  A: Variance of the treatment effect estimate is proportional to 1/(q*(1-q)). Minimized when q=0.5, giving most statistical power to detect a real effect.

- **Q: What is a long-term holdout and why use one?**
  A: Keeps small % of users (5-10%) on Control for months after launch. Purpose: check if the positive effect from MPR is sustained long-term, or was a novelty effect that wears off.

---

## Block 7: Statistics Core

### Two-sample t-test

Treatment mean vs Control mean — is the difference real or noise?

- T-statistic = (Treatment mean - Control mean) / sqrt(var of difference)
- Bigger T = more likely the difference is real
- T maps to a p-value

### p-value (say this 3 times)

> The probability of seeing data this extreme IF the null hypothesis (no difference) is true.

**Common wrong interpretation:** "p-value = probability that the null is true."
That requires Bayes' rule and a prior on how likely your treatment is to work.

### Confidence interval

- 95% CI = the range that covers the true difference 95% of the time
- If CI doesn't contain zero → statistically significant
- CI = observed delta ± 1.96 × standard error
- Equivalent to p-value < 0.05

### Type I and Type II errors

| | You say "effect!" | You say "no effect" |
|---|---|---|
| **Real effect exists** | Correct | **Type II error** (miss) |
| **No real effect** | **Type I error** (false alarm) | Correct |

- Type I rate = alpha = 0.05 (you set this)
- Type II rate = beta (typically 0.20)
- **Power = 1 - beta = 0.80** = probability of catching a real effect

### Power formula (approx)

```
n ≈ 16 × σ² / δ²
```

- Want to detect smaller δ? Need **way** more users (quadratic!)
- Want higher power? Need more users

### Multiple testing problem

If you test 100 metrics at alpha=0.05, you expect ~5 false positives even with no real effect.

Solutions:
- **Bonferroni**: use alpha/number_of_tests (simple but conservative)
- **Benjamini-Hochberg**: controls false discovery rate (better)
- **Tier your metrics**: expected-to-move (0.05), might-move (0.01), shouldn't-move (0.001)

### Q&A

- **Q: Explain p-value to a PM who thinks "p=0.03 means 97% chance the treatment works."**
  A: "Not quite. p=0.03 means: IF the treatment actually did nothing, there's only a 3% chance we'd see results this extreme by random chance. To know the probability the treatment works, we'd also need to know how likely it was to work before we ran the test (the prior). What p=0.03 does tell us: this result is unlikely to be pure noise."

- **Q: Experiment has power of 60%. Enough?**
  A: 60% power means 40% chance of MISSING a real effect. Industry standard is 80%. With 60%, you might conclude "no effect" when there actually is one. Either run longer, get more traffic, or accept you can only detect larger effects.

- **Q: 200 metrics tested, 12 significant at p<0.05. Concerning?**
  A: At alpha=0.05 with 200 independent metrics and no real effect, you'd expect 10 false positives. 12 is barely above that. (1) Separate metrics into tiers by likelihood of impact. (2) Apply stricter thresholds to unexpected metrics. (3) Check if significant metrics tell a coherent story or seem random.

---

## Block 8: Variance and Sensitivity

### Why variance matters

High variance = noisy experiment = need more users = longer to run = harder to detect effects.
Lower variance = same experiment finds smaller effects = faster decisions.

### Delta vs Delta %

- Delta = Treatment mean - Control mean (absolute)
- Delta% = Delta / Control mean (relative, what people usually report)
- To compute CI for Delta%: do NOT just divide var(Delta) by Control_mean²
  - Control mean is also a random variable!
  - Use the **delta method**: var(Delta%) = (1/Yc²)×var(Yt) + (Yt²/Yc⁴)×var(Yc)

### Outliers destroy your experiment

A single bot with 10,000 pageviews can flip your t-test from significant to not.
Fix: cap values at a reasonable threshold (e.g., max 500 searches/day per user).

### Ways to reduce variance (improve sensitivity)

1. **Better metric**: conversion rate (binary) has lower variance than revenue (continuous)
2. **Cap/transform**: cap outliers, or use log(revenue+1)
3. **Triggered analysis**: only analyze users who actually SAW the change (exclude users who never reached the changed page)
4. **CUPED**: use pre-experiment data as a covariate to reduce variance (like a "before" measurement)
5. **Stratification**: analyze by strata (desktop vs mobile, country) then combine
6. **More granular unit**: randomize by page instead of user (but careful about consistency!)

### CUPED formula

```
Y_adjusted = Y - θ × (X - mean(X))
where θ = cov(Y, X) / var(X)
X = pre_experiment_revenue, Y = revenue_per_user
```

### Q&A

- **Q: Revenue-per-user is very noisy (some $0, one $10,000). What do you do?**
  A: (1) Cap revenue at a reasonable max (e.g., $500/user/day). (2) Consider using purchase indicator (yes/no) instead — lower variance. (3) Try log transform. (4) Apply CUPED using pre-experiment revenue as covariate.

- **Q: What is CUPED in one sentence?**
  A: CUPED uses each user's pre-experiment metric value as a control variate to reduce the variance of the treatment effect estimate, making the experiment more sensitive.

- **Q: What is triggered analysis?**
  A: Only include users who were actually exposed to the change. If your change is on the checkout page, exclude users who never visited checkout. Removes noise from users who couldn't possibly be affected.

---

## Block 9: A/A Tests

### What is an A/A test?

Split users into two groups. Give them the EXACT SAME experience. Analyze as if one group is Treatment.

### Why?

If your platform is correct, ~5% of metrics should show p<0.05 by chance. If you see way more than 5%, something is BROKEN:

- Randomization is biased
- Variance calculation is wrong
- Data pipeline has a bug
- Logging differs between variants

### What A/A tests catch (real examples from the book)

1. **Wrong variance formula**: randomize by user, compute CTR per pageview, use standard variance formula → assumes independence that doesn't exist → A/A tests show way too many false positives

2. **Peeking / early stopping**: if you check results daily and stop as soon as p<0.05, you'll get many false positives. Optimizely had this bug. A/A tests exposed it.

3. **Browser redirects**: if Treatment redirects to a new URL, the redirect itself causes performance differences, bots crawl differently, bookmarks break. A/A tests with redirects consistently fail.

4. **Unequal splits with caching**: 90/10 splits can cause false positives because the larger group gets more LRU cache hits.

### Q&A

- **Q: A/A test shows 15% of metrics significant at p<0.05. What do you do?**
  A: Something is wrong. (1) Check if randomization unit matches analysis unit. (2) Check for SRM. (3) Check data pipeline for duplication/loss. (4) Check variance calculation for correlation. Do NOT run real experiments until A/A passes.

- **Q: Name two things A/A tests can detect.**
  A: (1) Incorrect variance estimation (e.g., from unit mismatch). (2) Biased randomization. (3) Data pipeline bugs. (4) Platform bugs creating systematic differences.

- **Q: Team says "A/A tests are a waste of traffic." How do you respond?**
  A: "A/A tests are cheap insurance. They validate that our platform produces trustworthy results. Multiple companies found critical bugs through A/A tests. Running one A/A test could save us from wrong launch decisions on every future experiment."

---

## Key Explanations from Q&A

### Coupon field example (full walkthrough)

You're buying shoes. You're about to pay. Then you see a box that says "Enter Coupon Code." Now you think: "Wait, there's a coupon I'm missing?" You leave the checkout page to Google for a coupon. Maybe you find one, maybe you don't. Either way, many people **never come back to finish buying**. The coupon box itself — even with zero coupons existing — **costs you sales** just by being there. That's why they A/B tested it before building a real coupon system.

### Guardrails (ELI5)

**Guardrails = "don't break stuff while you test."** You're testing if the coupon field hurts revenue. But what if your new code also makes the page load 5 seconds slower, or crashes for 10% of users? You'd lose money for a reason that has nothing to do with the coupon. So you watch guardrails like page speed and crash rate. If those move, your test is broken — fix that first.

---

## Mock Interview Questions

Answer these without looking. 2 minutes each.

1. **"Walk me through how you'd design an A/B test."** (5 steps: hypothesis → metrics → randomization unit → population → size/duration)
2. **"Your experiment shows p=0.04 and +0.3% revenue lift. Launch or not?"** (Depends on practical significance for the business + check guardrails)
3. **"You see a +20% lift. What do you do?"** (Twyman's Law — be suspicious, check for bugs first)
4. **"Explain p-value to a non-technical PM."** (NOT probability null is true; it's probability of this data if null were true)
5. **"Your A/A test is failing. What could be wrong?"** (Variance formula, randomization bias, data pipeline, logging)
6. **"How would you reduce the variance of your experiment?"** (CUPED, capping outliers, triggered analysis, better metric, stratification)
7. **"What's the difference between statistical and practical significance?"** (Stat sig = unlikely noise; practical sig = big enough to matter for the business)
8. **"Why not just compare before and after instead of running an A/B test?"** (No control group — seasonality, other launches, external events all confound)

---

## Common Traps

These are WRONG — know why:

| Trap | Why it's wrong |
|------|----------------|
| "p-value = probability the null is true" | p-value is P(data \| null), not P(null \| data) |
| "Not significant = no effect" | Could be underpowered — absence of evidence ≠ evidence of absence |
| "Big lift is fine even with SRM" | SRM means the experiment is broken. Results can't be trusted at all. |
| "A/A tests are useless" | They catch platform bugs that invalidate all your experiments |
| "If I randomized by user, pageviews are independent too" | Pageviews from same user are correlated → broken variance estimate |

---

## Hands-On Lab Notebook

Location: `ab-testing/ab_testing_practice.ipynb`
Support package: `ab-testing/ab_lab/`

### Lab structure

| Lab | What you DO | Concept tested |
|-----|------------|----------------|
| 1 — First Experiment | Design experiment, compute means/t-test/CI, make launch decision | Full lifecycle |
| 2 — Catch the Bug | Detect a rigged 50/50 split | SRM |
| 3 — Outliers | See outliers break a t-test, fix with capping | Outliers & variance |
| 4 — A/A Test | Simulate 200 A/A tests, check false positive rate | A/A tests |
| 5 — CUPED | Apply CUPED formula to detect a tiny 1% effect | Variance reduction |
| 6 — Power Analysis | Implement power formula, see how sample size scales | Power analysis |
| 7 — Multiple Scenarios | Pick scenarios, design + analyze + decide | End-to-end practice |

### Available scenarios (in `ab_lab/scenarios.py`)

| Scenario | Description | True effect | N per group |
|----------|-------------|-------------|-------------|
| `coupon_field` | Coupon code field on checkout | -2.8% | 5,000 |
| `new_ranking` | New ML ranking model | +1.5% | 8,000 |
| `homepage_recs` | Recommended For You on homepage | +0.8% | 10,000 |
| `button_color` | Green vs Blue buy button | +0.1% (tiny) | 50,000 |

### Key formulas used in labs

```python
# Two-sample t-test
from scipy import stats
t_stat, p_value = stats.ttest_ind(control_values, treatment_values)

# Confidence interval
se = sqrt(var_control/n_control + var_treatment/n_treatment)
ci_lower = diff - 1.96 * se
ci_upper = diff + 1.96 * se

# CUPED
theta = cov(Y, X) / var(X)
Y_adjusted = Y - theta * (X - mean(X))

# Power / sample size
n = 16 * variance / delta**2

# SRM check (chi-squared)
from scipy.stats import chi2
chi2_stat = (n_ctrl - expected_ctrl)**2/expected_ctrl + (n_trt - expected_trt)**2/expected_trt
p_value = 1 - chi2.cdf(chi2_stat, df=1)
```

---

## If Brain Is Cooked

Do only Block 1 + Block 2 + the Mock Interview Questions out loud.
That's ~45 min and covers 80% of what you'll be asked.

---

## Day-by-Day Checklist

### Day 1 — Can you answer these without looking?

- [ ] Why can't you prove causation from observational data?
- [ ] What are the 5 steps to design an A/B test?
- [ ] What does p-value actually mean (and what it does NOT mean)?
- [ ] What's the difference between statistical and practical significance?
- [ ] Name the 3 types of metrics

### Day 2 — Can you answer these without looking?

- [ ] Why is user-level randomization the default?
- [ ] What happens if you randomize by user but analyze by pageview?
- [ ] Describe the 4 ramp phases
- [ ] Type I vs Type II error
- [ ] Power = ? How do you get more of it?
- [ ] What is CUPED in one sentence?
- [ ] What's the point of A/A tests?
