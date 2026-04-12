# A/B Testing — Questions & Answers (Offline Reference)

## How to use this with me (Ori)

- I have ADHD — keep explanations complete but concise. No walls of text.
- I'm a data scientist, strong on coding/stats, weaker on the open-ended verbal A/B testing format.
- When quizzing me: give the question, wait for my answer, then give short targeted feedback.
- I know the concepts but freeze assembling them live. Help me practice the structure, not re-learn the theory.
- If I'm stuck: teach in 3-5 lines max, then re-quiz with a different question on the same concept.
- If I get frustrated: switch topics and come back later.
- My answer structure: Assumptions → Approach → Solution → Tradeoffs.
- For A/B testing specifically: I should always start by clarifying the question before answering.

---

## Must-Know Terms

**OEC (Overall Evaluation Criterion):** The single primary metric you use to decide ship/no-ship. Pick one metric, not five. "What user action, measurable in 2 weeks, best predicts long-term value?"

**Guardrail metric:** A metric that must NOT degrade. You don't optimize for it — you protect it. Examples: latency, crash rate, retention. If guardrail breaks, don't ship even if OEC improved.

**Randomization unit:** The entity you randomly assign to control/treatment. Usually user_id. Rule: "Does treating user A change user B's outcome?" No → user-level. Yes → cluster (e.g., geo region).

**Analysis unit:** The unit you measure. Should match randomization unit. If you randomize by user but analyze by pageview, you violate independence and get false positives.

**p-value:** Probability of seeing data this extreme IF the null hypothesis (no effect) were true. It is NOT "probability the null is true." p=0.03 means: if the feature truly had no effect, there's a 3% chance we'd see a result this large by luck.

**Confidence interval:** Range of plausible values for the true effect. 95% CI means: if we repeated this experiment many times, 95% of the intervals would contain the true effect. CI excluding 0 = statistically significant.

**Type I error (false positive):** Concluding the feature works when it doesn't. Controlled by significance level alpha (usually 0.05). "We shipped something useless."

**Type II error (false negative):** Concluding the feature doesn't work when it does. Controlled by power. "We killed a good feature."

**Power:** Probability of detecting a real effect when it exists. Power = 1 - P(Type II error). Standard target: 0.80 (80%). Low power = you'll miss real effects.

**MDE (Minimum Detectable Effect):** Smallest effect size you want your experiment to detect. This is a product decision, not a stats one: "What's the smallest improvement worth shipping?"

**Novelty effect:** Users try the new thing because it's new, not because it's better. Inflates short-term metrics. Fix: run longer (2+ weeks), look at new-vs-returning users separately.

**Primacy effect:** Opposite of novelty — users resist change because it's unfamiliar. Metrics look bad early but improve as users adapt. Fix: run longer.

**A/A test:** Run an experiment with no treatment — both groups get the same experience. Checks if your experimentation platform is working correctly. If A/A shows significant differences, your pipeline has a bug.

**SRM (Sample Ratio Mismatch):** Expected 50/50 split but got 48/52. Means something is biased in your assignment or measurement. SRM = results are untrustworthy. Do NOT interpret the experiment. Find the bug first.

**Triggered analysis:** Only analyze users who actually encountered the change. If you changed the checkout page but measure ALL users, most of your sample is noise (never saw checkout). Triggered = filter to exposed users.

**CUPED (Controlled Using Pre-Experiment Data):** Variance reduction technique. Uses pre-experiment metric values as a covariate to reduce noise. Like adjusting for a baseline. Doesn't change randomization — it's an analysis technique. Can dramatically increase sensitivity (detect smaller effects).

---

## Glassdoor Questions with Full Answers

### Q026: Walk me through how you'd design an A/B test.

**Answer (8-step skeleton):**

1. **Hypothesis:** State what you expect and why. "We believe [change] will [improve metric] because [reason]."

2. **OEC:** One primary metric. Use the hack: "What user action, measurable in 2 weeks, predicts long-term value?" Always per-user (normalizes for group size).

3. **Guardrails:** What must not break. Almost always include latency and retention. For revenue tests: refund rate. For engagement tests: spam rate.

4. **Randomization unit:** User-level unless spillover exists. Spillover test: "Does treating A change B's outcome?"

5. **Population:** Who's eligible? All users? Only mobile? Only new users? Narrower = less noise but less generalizable.

6. **Sample size:** n = 16sigma^2 / delta^2 per group (alpha=0.05, power=0.80). MDE (delta) comes from product: "smallest improvement worth shipping."

7. **Duration:** Minimum 2 weeks. Covers day-of-week effects, novelty/primacy, and gives enough data. Start with ramp: 1-5% → monitor for bugs → ramp to 50/50.

8. **Launch decision:** OEC is statistically significant AND guardrails are safe → ship. OEC significant but guardrail violated → investigate. OEC not significant → either underpowered (run longer) or no real effect.

---

### Q027: How could you do an A/B test if we see a 3% increase for the product?

**Answer:**

First clarify: 3% increase in what metric? Over what baseline? Is this from an existing experiment or an observation?

If from an experiment:
- Check if the 3% is statistically significant (CI doesn't include 0)
- Check practical significance: is 3% worth the engineering cost to maintain?
- Check guardrails: did anything break?
- Check for SRM: was the split balanced?
- Check segment effects: does it help everyone equally or just one group?

If you need to design an experiment to detect a 3% effect:
- MDE = 3%, use sample size formula to determine how many users you need
- Estimate variance from historical data
- n = 16 * sigma^2 / (0.03 * baseline_mean)^2
- This might require a large sample size — discuss tradeoffs between precision and speed

---

### Q028 / Q030: Design an experiment for a YouTube feature.

**Answer (example: YouTube adds a "save for later" button):**

**Clarify:** What's the feature? What's the business goal — engagement? retention? watch time?

**Hypothesis:** Adding a "save for later" button will increase return visits, as users build a personal queue they want to come back to.

**OEC:** Return visits per user within 7 days. This captures the core behavior we expect: users come back to watch saved content.

**Guardrails:** Watch time per session (don't cannibalize current viewing), ad revenue per user.

**Randomization:** User-level. No spillover — one user's saves don't affect another's experience.

**Population:** All YouTube logged-in users (need login to save).

**Sample size:** Estimate current return visit rate and variance, set MDE to smallest meaningful lift (e.g., 2% relative increase), compute n.

**Duration:** 3-4 weeks (novelty effect likely — new button will attract curiosity clicks that don't translate to long-term use).

**Launch decision:** If return visits per user increase significantly AND watch time doesn't drop, ship it.

---

### Q029: You have 2 groups and are testing 2 drugs. How would you design an experiment?

**Answer:**

This is a factorial design question.

**Option 1: Factorial design (preferred)**
- 4 groups: placebo-placebo, drug A only, drug B only, both A+B
- Tests main effects of each drug AND interaction between them
- More efficient than running two separate experiments
- Randomize patients to one of 4 groups

**Option 2: Sequential design**
- First test drug A vs placebo
- Then test drug B vs placebo
- Misses interaction effects

**Key considerations:**
- Block by relevant covariates: age, severity, gender (stratified randomization)
- Double-blind: neither patient nor doctor knows assignment
- Power: 4 groups means each group is smaller — need more total patients
- Interaction effect: does A+B together work differently than expected from A and B separately?
- Ethical guardrails: interim analysis with stopping rules if one group does significantly worse

---

### Q031: You have a Google app and make a change. How do you test if a metric increased?

**Answer:**

1. **If you can run an A/B test:** Split users into control (no change) and treatment (change). Compare the metric between groups. Use a two-sample t-test or bootstrap CI for the difference. This is the gold standard — causal inference.

2. **If you can't randomize (already shipped to everyone):** Use quasi-experimental methods:
   - **Before/after comparison:** Compare metric before and after the change. Problem: confounded by time trends, seasonality.
   - **Interrupted time series:** Model the pre-change trend, project forward, compare to actual post-change values.
   - **Diff-in-diff:** If change only affected some users/regions, compare the change in metric for affected vs unaffected groups.

3. **Statistical test:** Two-sample t-test (or Welch's if unequal variance). Check: is the difference statistically significant? Is the CI around the lift practically meaningful? Are guardrails stable?

---

### Q032: How would you remove bias in an A/B test, and how would you make inference from data about two ad campaigns?

**Answer:**

**Removing bias:**
- **Random assignment:** The primary tool. Random = no systematic differences between groups.
- **Stratified randomization:** Balance key covariates (geo, platform, user tenure) across groups.
- **A/A test:** Verify your platform isn't introducing bias before running the real test.
- **SRM check:** Monitor split ratios. Imbalance = bias.
- **Novelty/primacy:** Run long enough to wash out behavioral change artifacts.
- **Selection bias:** Don't let users self-select into groups (that's observational, not experimental).

**Inference on two ad campaigns:**
- Compare per-user metrics (CTR, conversion rate, revenue per user) between campaign groups.
- Use t-test or bootstrap CI for the difference.
- Check if differences are practically significant, not just statistically.
- Watch for confounders: were campaigns shown to different audiences? different times? different placements?

---

### Q033: Design a roadmap to test if features are good or not.

**Answer:**

This is a meta-question about experimentation culture:

1. **Establish an experimentation platform:** Consistent randomization, logging, metric computation.
2. **Define success metrics per product area:** Each team has an OEC + guardrails before building anything.
3. **Test everything:** Default to A/B test for any user-facing change. No shipping without data.
4. **Staged rollout process:** Idea → A/A validation → small ramp (1-5%) → bug check → full ramp (50/50) → analyze → ship/kill decision.
5. **Review cadence:** Weekly experiment review — interpret results, decide on next steps.
6. **Documentation:** Every experiment has a pre-registered hypothesis, OEC, guardrails, and expected MDE.

---

### Q034: A/B testing, selection bias, and ML.

**Answer:**

**Selection bias in A/B testing:**
- Occurs when assignment to groups is correlated with outcomes.
- Example: users who opt in to a beta feature are more engaged → comparing beta users to non-beta users is biased.
- Fix: random assignment, not self-selection.
- Check for it: compare pre-experiment covariates between groups. If they differ, you have bias.

**Selection bias in ML:**
- Training data doesn't represent production data.
- Example: model trained on users who clicked → biased toward clickers, can't predict non-clickers.
- Survivorship bias: only analyzing users who stayed, ignoring those who churned.
- Fix: use proper holdout, be aware of what your training data represents.

**Connection:** Both are about the same fundamental problem — your sample doesn't represent the population you're trying to draw conclusions about.

---

### Q035: Stats concepts + hypothetical experiment design walkthrough (PhD level).

**Answer:**

This is a combination question. The stats concepts portion tests:
- Can you explain p-value, CI, Type I/II correctly? (See definitions above)
- Can you derive or explain the sample size formula?
- Do you understand the relationship between alpha, power, MDE, variance, and sample size?

The experiment design portion tests:
- Can you walk through the 8-step skeleton fluently?
- Can you handle follow-ups: "What if the effect is heterogeneous?" → segment analysis. "What if you can't randomize?" → quasi-experimental methods. "What if your metric is a ratio?" → delta method for variance.

**Key PhD-level topics to be ready for:**
- Delta method for ratio metrics
- Multiple testing correction (Bonferroni, FDR)
- Sequential testing / always-valid p-values
- Heterogeneous treatment effects (CATE)
- Interference / network effects and cluster randomization

---

## Common Pitfalls (Quick Reference)

| Pitfall | What it is | How to catch/fix |
|---|---|---|
| Peeking | Checking results repeatedly, stopping when significant | Pre-commit to sample size. Or use sequential testing. |
| Multiple comparisons | Testing 20 metrics, one is p<0.05 by chance | Bonferroni correction or designate one OEC upfront |
| Novelty effect | New = exciting, inflates short-term metrics | Run 2+ weeks, split by new/returning users |
| SRM | Unequal group sizes | Chi-square test on counts. If SRM, results invalid. |
| Survivorship bias | Only measuring users who stayed | Intent-to-treat: analyze ALL randomized users |
| Simpson's paradox | Overall trend reverses within subgroups | Always check segment-level results |
| Low power | Can't detect real effects | Increase n, reduce variance (CUPED), increase MDE |

---

## The Google Play 10% Discount — Model Answer

**Question:** "We offered users 10% off at Google Play last weekend. How can we determine if this promotion was successful?"

**Step 1 — Clarify:**
"Did every user get the discount, or was there a holdout/control group? How were users selected?"

**If A/B test (control vs treatment):**
- OEC: Net revenue per user (after discount)
- Compare treatment vs control directly
- Break-even: need 11% more purchases to offset 10% price cut (1/0.9 - 1 = 0.111)

**If everyone got it:**
- Compare promo weekend to previous comparable weekends
- Harder — confounded by seasonality, trends
- Use diff-in-diff if some regions/segments didn't get the promo

**Guardrails:**
- Forward shifting: did users just move next week's purchases into promo weekend? Check post-promo revenue.
- Bargain hunters: did we attract low-quality users who never return at full price? Check 14/30-day retention of promo users.
- Refund rate (if measuring gross revenue)

**Launch decision:** Net revenue per user increased enough to cover the discount AND post-promo retention is stable → promo was successful. Consider repeating.

---

## 8-Step Skeleton (Copy-Paste for Practice)

1. Hypothesis
2. OEC
3. Guardrails
4. Randomization unit
5. Population
6. Sample size (n = 16sigma^2/delta^2)
7. Duration (2+ weeks)
8. Launch decision
