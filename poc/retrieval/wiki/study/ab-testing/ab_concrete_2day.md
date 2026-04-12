# A/B Testing: 2-Day Concrete Plan

Source: google/study/ab-testing/ab_concrete_2day.md

# A/B Testing: 2-Day Concrete Plan

Source: ab_subset_single (chapters 1-3, 5-6, 14-15, 17-19)

## How This Works

- Each block = 1 concept + the knowledge you need + a drill
- You do NOT need to read the PDF first. The content is here.
- PDF pages are listed IF you want to go deeper. Skip them if brain says no.
- Speak answers out loud. That's the practice.
- Check the box when done.

---

## DAY 1 (4 blocks, ~2 hours total)

---

### Block 1: Why A/B Test at All (20 min)

**The knowledge:**

Netflix sees X% churn. They add a feature. Users of that feature churn at X/2%.
Does the feature reduce churn? **NO.** You can't tell. Heavy users both use features
more AND churn less. The feature didn't cause anything - usage pattern did.

This is called **confounding**: a hidden variable (user engagement) affects both
the thing you're measuring (churn) and the thing you changed (feature adoption).

The ONLY way to prove causation: **randomly assign** users to Treatment (sees feature)
and Control (doesn't). Then compare. That's an A/B test.

**Key term - OEC (Overall Evaluation Criterion):**
The ONE metric you care about most. Not "profit" (too slow to measure, gameable
with price hikes). Something measurable in 1-2 weeks that predicts long-term success.
Example: revenue-per-user, not total revenue (because group sizes vary by chance).

**Hierarchy of evidence (top = strongest):**
1. Meta-analysis of multiple experiments
2. Randomized controlled experiments (A/B tests)
3. Non-randomized experiments
4. Observational studies
5. Expert opinion (HiPPO - Highest Paid Person's Opinion)

**Drill - say out loud:**

> "If I see users of feature X churn less, I still can't say the feature reduces churn.
> Why? Because adoption wasn't random. Engaged users self-select into the feature
> AND churn less. I need a randomized experiment to separate the two."

**Now answer these (out loud, ~1 min each):**

- [ ] Q1: Your PM says "users who use our new search filter buy 2x more, let's invest more in it." What's wrong with this claim?
- [ ] Q2: What is an OEC? Why not just use "profit"?
- [ ] Q3: Why is an A/B test better than looking at before/after data?

<details>
<summary>Answers</summary>

Q1: Selection bias. Users who use search filter are probably already high-intent buyers. You'd need to randomly show/hide the filter to prove it causes more purchases.

Q2: OEC = the primary metric for your experiment. Profit is bad because: (a) too slow to measure in a 2-week test, (b) short-term profit tricks like raising prices can hurt long-term. Use something like revenue-per-user.

Q3: Before/after has no control group. Seasonality, other launches, external events all change metrics over time. An A/B test runs Treatment and Control simultaneously, so these effects cancel out.
</details>

*Want more depth? PDF pages 1-7 (book pages 8-14)*

---

### Block 2: Designing an Experiment (25 min)

**The knowledge:**

The book walks through a real example: an e-commerce site wants to add a coupon
code field to checkout. Concern: even an empty coupon field might make users
abandon checkout to go hunt for codes.

**The 5-step design process:**

| Step | What | Example |
|------|------|---------|
| 1. Hypothesis | What you think will happen | "Adding coupon field will decrease revenue" |
| 2. Metrics | OEC + guardrails | OEC: revenue-per-user. Guardrails: latency, crash rate |
| 3. Randomization unit | What gets randomly assigned | Users (not pages, not sessions) |
| 4. Population | Who's included in analysis | Users who START checkout (not all visitors) |
| 5. Size & duration | How long, how many | Enough power to detect 1% change; min 1 week |

**Why "users who start checkout" as population?**
- All visitors: too noisy, most never reach checkout
- Only purchasers: wrong! If coupon field PREVENTS purchases, those users vanish from your denominator
- Users who start checkout: includes everyone potentially affected, excludes noise

**Duration rules of thumb:**
- Minimum 1 week (captures weekday/weekend differences)
- Longer if you suspect novelty or primacy effects
- Consider seasonality (holidays, back-to-school)

**Drill - say out loud:**

> "To design an A/B test I need: hypothesis, metrics with an OEC and guardrails,
> randomization unit, target population, and power analysis for size and duration.
> I always run at least one full week."

**Now answer these (out loud):**

- [ ] Q4: Walk me through designing an A/B test for adding a "recommended for you" section to a homepage. (Say the 5 steps)
- [ ] Q5: Why run for at least 1 full week?
- [ ] Q6: You're testing a checkout change. Should your OEC denominator be all site visitors or only users who reach checkout?

<details>
<summary>Answers</summary>

Q4: (1) Hypothesis: adding recs increases engagement and purchase rate. (2) OEC: clicks-per-user or revenue-per-user; guardrails: page load time, other-section CTR. (3) Randomization: user-level. (4) Population: all homepage visitors. (5) Power analysis for 1% detectable change, run 1-2 weeks.

Q5: User behavior differs on weekdays vs weekends. If you only run Mon-Wed, you miss weekend patterns. A full week captures the weekly cycle.

Q6: Users who reach checkout. All visitors adds noise from people who never interact with the change. But NOT only purchasers - that would exclude people the change scared away.
</details>

*Want more depth? PDF pages 19-27 (book pages 26-34)*

---

### Block 3: Interpreting Results (25 min)

**The knowledge:**

You ran the coupon experiment. Here are real results from the book:

| Variant | Rev/user (Treatment) | Rev/user (Control) | Diff | p-value | 95% CI |
|---------|---------------------|--------------------|----- |---------|--------|
| Treatment 1 vs Control | $3.12 | $3.21 | -2.8% | 0.0003 | [-4.3%, -1.3%] |
| Treatment 2 vs Control | $2.96 | $3.21 | -7.8% | 1.5e-23 | [-9.3%, -6.3%] |

**How to read this:**

- **p-value < 0.05** = statistically significant = unlikely to be random noise
- **p-value IS NOT** "probability the null is true." It's "probability of seeing this data IF there were no real difference"
- **Confidence interval** [-4.3%, -1.3%] = we're 95% sure the true effect is somewhere in this range. Zero is NOT in the range, so it's significant.
- **Practical significance**: Is the effect big enough to matter? A 0.01% change might be statistically significant with millions of users but not worth acting on. For Google/Bing, even 0.2% matters (billions in revenue). For a startup, maybe 10%+ is the bar.

**The 6 scenarios (this comes up in interviews):**

| # | Stat sig? | Practically sig? | Decision |
|---|-----------|-----------------|----------|
| 1 | No | No | Easy: no effect. Iterate or drop. |
| 2 | Yes | Yes | Easy: launch! |
| 3 | Yes | No | Effect is real but tiny. Probably not worth the cost. |
| 4 | No | No (wide CI) | Underpowered. Can't conclude anything. Run bigger test. |
| 5 | No | Probably yes | Promising but noisy. Rerun with more power. |
| 6 | Yes | Probably yes | Likely worth it but CI is wide. Consider rerunning or just launch. |

**Guardrail metrics / invariants:**
Before trusting results, check things that SHOULD NOT change:
- Sample sizes should match the configured split (e.g., 50/50)
- Latency shouldn't change if your change is UI-only
- If these invariants move, your experiment has a bug. **Don't trust the results.**

**Twyman's Law:** "Any figure that looks interesting or different is usually wrong."
If results look too good, check for bugs first.

**Drill - say out loud:**

> "p-value 0.03 means: IF there were no real effect, there's only a 3% chance
> I'd see data this extreme. It does NOT mean there's a 3% chance the treatment
> has no effect."

**Now answer these:**

- [ ] Q7: p-value is 0.03 and the effect is +0.5% revenue. Your PM asks "should we launch?" What's your answer?
- [ ] Q8: You see a +15% lift in your experiment. What should your first reaction be?
- [ ] Q9: Treatment has 48% of users and Control has 52%, but you configured 50/50. What do you do?

<details>
<summary>Answers</summary>

Q7: Depends on practical significance. Is 0.5% revenue meaningful for this business? For Google, yes (millions of dollars). For a small app, maybe not worth the engineering maintenance cost. Also check guardrails (latency, errors).

Q8: Twyman's Law - be suspicious. A +15% lift is unusually large. Check for bugs: sample ratio mismatch, logging errors, bot traffic, data pipeline issues. If it checks out, great - but verify first.

Q9: This is a Sample Ratio Mismatch (SRM). Something is wrong with randomization or data collection. DO NOT trust the experiment results. Investigate the cause before drawing any conclusions.
</details>

*Want more depth? PDF pages 28-32 (book pages 35-39)*

---

### Block 4: Metrics (25 min)

**The knowledge:**

**Three types of metrics:**

| Type | What | Example | Moves fast? |
|------|------|---------|-------------|
| **Goal metric** | Ultimate success measure | Monthly active users, long-term revenue | No, slow |
| **Driver metric** | Leading indicator of goal | Session length, click-through rate, 7-day retention | Yes |
| **Guardrail metric** | "Don't break this" | Page load time, crash rate, error rate | Should not move |

**Good OEC characteristics:**
- Measurable in short time (1-2 weeks)
- Sensitive enough to detect real changes
- Hard to game
- Predictive of long-term goal

**Bad OEC examples:**
- "Profit" - too slow, gameable (raise prices)
- "Clicks" alone - gameable (clickbait)
- CTR sometimes bad because you can increase it by removing good results

**Frameworks for choosing metrics:**
- HEART: Happiness, Engagement, Adoption, Retention, Task success
- AARRR (Pirate): Acquisition, Activation, Retention, Referral, Revenue

**Speed matters (real examples from book):**
- Amazon: 100ms slowdown = 1% decrease in sales
- Bing: every 10ms improvement paid for an engineer's salary for a year
- Always have page load time as a guardrail metric

**Drill:**

- [ ] Q10: Your team launches a new recommendation engine. What's your OEC? What are your guardrails?
- [ ] Q11: Someone proposes "number of searches per user" as OEC for a search engine. Why might this be bad?
- [ ] Q12: What's the difference between a goal metric and a driver metric?

<details>
<summary>Answers</summary>

Q10: OEC could be: click-through rate on recommendations, or revenue-per-user from recommended items. Guardrails: page load time (recs can slow pages), overall CTR (make sure recs don't cannibalize organic results), error rate.

Q11: More searches might mean users CAN'T FIND what they want. A user who searches once and finds the answer is happier than one who searches 5 times. Better OEC: sessions with successful click (time-to-success, or absence of query reformulation).

Q12: Goal metric = the ultimate thing you care about (e.g., long-term revenue). It moves slowly and is hard to measure in a 2-week experiment. Driver metric = a shorter-term proxy that predicts the goal (e.g., weekly retention rate). You use driver metrics as your OEC because they're measurable in experiment timeframes.
</details>

*Want more depth? PDF pages 35-38 (book pages 90-93)*

---

### Day 1 Checkpoint

If you can answer these without looking up, you're good:

- [ ] Why can't you prove causation from observational data?
- [ ] What are the 5 steps to design an A/B test?
- [ ] What does p-value actually mean (and what it does NOT mean)?
- [ ] What's the difference between statistical and practical significance?
- [ ] Name the 3 types of metrics

---

## DAY 2 (5 blocks, ~2.5 hours total)

---

### Block 5: Randomization Unit (20 min)

**The knowledge:**

**Three granularity levels:**

| Unit | What it means | Pro | Con |
|------|--------------|-----|-----|
| **Page-level** | Each pageview is randomly assigned | Huge sample size, more power | Same user sees different variants! Bad UX. |
| **Session-level** | All pages in one visit get same variant | Better than page-level | User returns next day, might get different variant |
| **User-level** | A user always sees same variant | Consistent experience, can measure retention | Need more users for same power |

**User-level is the default.** Why?
- Consistent experience (user doesn't see feature appear/disappear)
- Can measure long-term metrics (retention, lifetime value)
- Satisfies SUTVA (Stable Unit Treatment Value Assumption): units don't interfere with each other

**User ID options:**
- Signed-in user ID: best, works cross-device
- Cookie: common, but lost on browser clear / incognito
- Device ID: stable longitudinally but different per device

**Critical rule: randomization unit >= analysis unit**
- Randomize by user, analyze by user = fine
- Randomize by user, analyze by pageview = DANGEROUS
  - Pageviews from same user are correlated
  - Variance formula assumes independence
  - You'll underestimate variance = too many false positives
  - Your A/A tests will fail

**Drill:**

- [ ] Q13: Why is user-level randomization the most common choice?
- [ ] Q14: You randomize by user but compute click-through rate per page. Why is this a problem?
- [ ] Q15: When might you NOT use user-level randomization?

<details>
<summary>Answers</summary>

Q13: Consistent user experience (no flickering between variants), ability to measure user-level metrics like retention, and satisfies independence assumption when analyzing per-user metrics.

Q14: Pages from the same user are correlated (not independent). The standard variance formula assumes i.i.d. samples. Using it on correlated page-level data underestimates variance, making confidence intervals too narrow and p-values too small. You'll see false positives. Use the delta method or bootstrap instead.

Q15: Infrastructure changes where user-level isn't possible (e.g., comparing hosting providers - randomize by IP or data center). Or when you specifically want sub-user metrics and don't care about cross-session consistency. Also: ad auctions might randomize by advertiser cluster.
</details>

*Want more depth? PDF pages 42-46 (book pages 167-171)*

---

### Block 6: Ramping / Launching (20 min)

**The knowledge:**

**SQR Framework:** When ramping an experiment, balance:
- **Speed** - how fast you iterate
- **Quality** - how precise your measurement is
- **Risk** - how much damage a bad variant can do

**Four ramp phases:**

| Phase | Traffic | Purpose |
|-------|---------|---------|
| **Pre-MPR** | Small (0.5%-5%) | Catch bugs. Use internal "rings": team -> company employees -> beta users -> small % of real users |
| **MPR** (Maximum Power Ramp) | ~50% Treatment | Get precise measurement. Run ~1 week minimum. This is where you measure the real effect. |
| **Post-MPR** | 75%-100% | Operational readiness. Can the system handle full load? |
| **Long-term holdout** | 95-100% + small holdout (5-10%) | Keep a small group on control for months to measure long-term effects |

**Why not 100% on day one?**
- Healthcare.gov launched to 100%, site collapsed
- Bad feature with 1% exposure hurts few users; at 100% it's a disaster
- You can't measure anything if the system is down

**MPR = 50/50 for one Treatment.** Why?
- Variance of t-test is proportional to 1/(q(1-q)) where q = treatment fraction
- Minimized at q=0.5, so 50/50 gives maximum statistical power

**Drill:**

- [ ] Q16: You're launching a new ML ranking model. Describe your ramp plan.
- [ ] Q17: Why is 50/50 the maximum power ramp?
- [ ] Q18: What is a long-term holdout and why would you use one?

<details>
<summary>Answers</summary>

Q16: (1) Pre-MPR: ship to team internally, then 1% of users. Monitor guardrails (latency, errors, crashes) in near-real-time. (2) MPR: ramp to 50/50, run for 1 week+, measure OEC. (3) Post-MPR: if positive, ramp to 100% while monitoring operational metrics. (4) Optional: keep 5% holdout for 2 months to check for long-term decay.

Q17: The variance of the treatment effect estimate is proportional to 1/(q*(1-q)) where q is the treatment fraction. This is minimized when q=0.5 (50/50 split), giving you the most statistical power to detect a real effect.

Q18: A long-term holdout keeps a small % of users (5-10%) on Control for months after launch. Purpose: check if the positive effect measured during MPR is sustained long-term, or if it was novelty effect that wears off.
</details>

*Want more depth? PDF pages 46-50 (book pages 171-175)*

---

### Block 7: Statistics Core (30 min)

**The knowledge:**

**Two-sample t-test:**
You have Treatment mean and Control mean. Is the difference real or just noise?

- T-statistic = (Treatment mean - Control mean) / sqrt(var of difference)
- Bigger T = more likely the difference is real
- T maps to a p-value

**p-value (say this 3 times):**
> The probability of seeing data this extreme IF the null hypothesis (no difference) is true.

**Common wrong interpretation:** "p-value = probability that the null is true."
That requires Bayes' rule and a prior on how likely your treatment is to work. The p-value alone doesn't give you this.

**Confidence interval:**
- 95% CI = the range that covers the true difference 95% of the time
- If CI doesn't contain zero -> statistically significant
- CI = observed delta +/- 1.96 * standard error
- Equivalent to p-value < 0.05

**Type I and Type II errors:**

| | You say "effect!" | You say "no effect" |
|---|---|---|
| **Real effect exists** | Correct | **Type II error** (miss) |
| **No real effect** | **Type I error** (false alarm) | Correct |

- Type I rate = alpha = 0.05 (you set this)
- Type II rate = beta (typically 0.20)
- **Power = 1 - beta = 0.80** = probability of catching a real effect

**Power formula (approx):**
- n = 16 * variance / delta^2
- Want to detect smaller delta? Need way more users (quadratic!)
- Want higher power? Need more users

**Multiple testing problem:**
If you test 100 metrics at alpha=0.05, you expect ~5 false positives even with no real effect.
Solutions:
- Bonferroni: use alpha/number_of_tests (simple but conservative)
- Benjamini-Hochberg: controls false discovery rate (better)
- Tier your metrics: expected-to-move (0.05), might-move (0.01), shouldn't-move (0.001)

**Drill:**

- [ ] Q19: Explain p-value to a PM who thinks "p=0.03 means 97% chance the treatment works."
- [ ] Q20: Your experiment has power of 60%. Is that enough? What happens?
- [ ] Q21: You ran an experiment with 200 metrics. 12 are significant at p<0.05. Is this concerning?

<details>
<summary>Answers</summary>

Q19: "Not quite. p=0.03 means: IF the treatment actually did nothing, there's only a 3% chance we'd see results this extreme by random chance. To know the probability the treatment works, we'd also need to know how likely it was to work before we ran the test (the prior). What p=0.03 does tell us: this result is unlikely to be pure noise."

Q20: 60% power means 40% chance of MISSING a real effect. Industry standard is 80%. With 60% power, you might conclude "no effect" when there actually is one. Either run longer, get more traffic, or accept you can only detect larger effects.

Q21: At alpha=0.05 with 200 independent metrics and no real effect, you'd expect 10 false positives. Seeing 12 is barely above that. You should (1) separate metrics into tiers by how likely they are to be impacted, (2) apply stricter thresholds to unexpected metrics, (3) check if the significant metrics tell a coherent story or seem random.
</details>

*Want more depth? PDF pages 52-59 (book pages 185-192)*

---

### Block 8: Variance and Sensitivity (20 min)

**The knowledge:**

**Why variance matters:**
High variance = noisy experiment = need more users = longer to run = harder to detect effects.
Lower variance = same experiment finds smaller effects = faster decisions.

**Delta vs Delta %:**
- Delta = Treatment mean - Control mean (absolute)
- Delta% = Delta / Control mean (relative, what people usually report)
- To compute CI for Delta%: do NOT just divide var(Delta) by Control_mean^2
  - Control mean is also a random variable!
  - Use the delta method: var(Delta%) = (1/Yc^2)*var(Yt) + (Yt^2/Yc^4)*var(Yc)

**Outliers destroy your experiment:**
A single bot with 10,000 pageviews can make your t-test go from significant to not.
Fix: cap values at a reasonable threshold (e.g., max 500 searches/day per user).

**Ways to reduce variance (improve sensitivity):**
1. **Better metric**: conversion rate (binary) has lower variance than revenue (continuous)
2. **Cap/transform**: cap outliers, or use log(revenue+1)
3. **Triggered analysis**: only analyze users who actually SAW the change (exclude users who never reached the changed page)
4. **CUPED**: use pre-experiment data as a covariate to reduce variance (like a "before" measurement)
5. **Stratification**: analyze by strata (desktop vs mobile, country) then combine
6. **More granular unit**: randomize by page instead of user (but careful about consistency!)

**Drill:**

- [ ] Q22: Your experiment measures revenue-per-user but revenue is very noisy (some users spend $0, one spent $10,000). What do you do?
- [ ] Q23: What is CUPED in one sentence?
- [ ] Q24: What is triggered analysis?

<details>
<summary>Answers</summary>

Q22: (1) Cap revenue at a reasonable max (e.g., $500/user/day) to limit outlier impact. (2) Consider using purchase indicator (did they buy: yes/no) instead, which has lower variance. (3) Could also try log transform. (4) Apply CUPED using pre-experiment revenue as covariate.

Q23: CUPED uses each user's pre-experiment metric value (e.g., last week's revenue) as a control variate to reduce the variance of the treatment effect estimate, making the experiment more sensitive.

Q24: Only include users who were actually exposed to (triggered by) the change in your analysis. If your change is on the checkout page, exclude users who never visited checkout. This removes noise from users who couldn't possibly be affected, giving a more precise estimate.
</details>

*Want more depth? PDF pages 60-65 (book pages 193-198)*

---

### Block 9: A/A Tests (20 min)

**The knowledge:**

**What is an A/A test?**
Split users into two groups. Give them the EXACT SAME experience. Analyze as if one group is Treatment.

**Why?**
If your platform is correct, ~5% of metrics should show p<0.05 by chance.
If you see way more than 5%, something is BROKEN:
- Randomization is biased
- Variance calculation is wrong
- Data pipeline has a bug
- Logging differs between variants

**What A/A tests catch (real examples from the book):**

1. **Wrong variance formula**: randomize by user, compute CTR per pageview, use standard variance formula -> assumes independence that doesn't exist -> A/A tests show way too many false positives

2. **Peeking / early stopping**: if you check results daily and stop as soon as p<0.05, you'll get many false positives. Optimizely had this bug. A/A tests exposed it.

3. **Browser redirects**: if Treatment redirects to a new URL, the redirect itself causes performance differences, bots crawl differently, bookmarks break. A/A tests with redirects consistently fail.

4. **Unequal splits with caching**: 90/10 splits can cause false positives because the larger group gets more LRU cache hits.

**Drill:**

- [ ] Q25: What would you do if your A/A test shows 15% of metrics significant at p<0.05?
- [ ] Q26: Name two things A/A tests can detect.
- [ ] Q27: Your team says "A/A tests are a waste of traffic." How do you respond?

<details>
<summary>Answers</summary>

Q25: Something is wrong. Investigate: (1) Check if randomization unit matches analysis unit (if not, variance is underestimated). (2) Check for sample ratio mismatch. (3) Check data pipeline for duplication or loss. (4) Check if variance calculation accounts for correlation. Do NOT run real experiments until A/A passes.

Q26: (1) Incorrect variance estimation (e.g., from unit mismatch). (2) Biased randomization. (3) Data pipeline bugs (logging differences). (4) Platform bugs that create systematic differences.

Q27: "A/A tests are cheap insurance. They validate that our platform produces trustworthy results. Multiple companies have found critical bugs through A/A tests - wrong variance formulas, biased randomization, logging bugs. Running one A/A test could save us from making wrong launch decisions on every future experiment. The cost of one A/A test is tiny compared to the cost of untrustworthy experimentation."
</details>

*Want more depth? PDF pages 67-71 (book pages 200-204)*

---

### Day 2 Checkpoint

- [ ] Why is user-level randomization the default?
- [ ] What happens if you randomize by user but analyze by pageview?
- [ ] Describe the 4 ramp phases
- [ ] What does p-value actually mean?
- [ ] Type I vs Type II error
- [ ] Power = ? How do you get more of it?
- [ ] What is CUPED in one sentence?
- [ ] What's the point of A/A tests?

---

## Final Boss: Mock Interview Questions

After finishing both days, answer these without looking. Time yourself: 2 min each.

- [ ] "Walk me through how you'd design an A/B test." (5 steps)
- [ ] "Your experiment shows p=0.04 and +0.3% revenue lift. Launch or not?"
- [ ] "You see a +20% lift. What do you do?"
- [ ] "Explain p-value to a non-technical PM."
- [ ] "Your A/A test is failing. What could be wrong?"
- [ ] "How would you reduce the variance of your experiment?"
- [ ] "What's the difference between statistical and practical significance?"
- [ ] "Why not just compare before and after instead of running an A/B test?"

---

## If Brain Is Cooked

Do only Block 1 + Block 2 + the Final Boss questions out loud.
That's 45 min and covers 80% of what you'll be asked.
