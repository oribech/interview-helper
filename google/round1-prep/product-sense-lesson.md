# Product Sense -- Lesson Notes

Source: Ace the Data Science Interview, Ch 10-11

---

## The 4 Question Types You Will Get

| Type                   | What they ask                                 | Which framework          |
| ---------------------- | --------------------------------------------- | ------------------------ |
| **Define a metric**    | "How would you measure success of X?"         | 3-Step Metric Definition |
| **Diagnose a metric**  | "Metric X dropped 10%. Why?"                  | 4-Step Metric Diagnosis  |
| **Design an A/B test** | "How would you test this feature?"            | 4-Step Experiment Design |
| **Metric trade-off**   | "Revenue up 1%, engagement down 3%. Ship it?" | Trade-Off Approach       |

---

## The AARRR Pirate Funnel (quick ref)

Think of it as the user's journey through your product, top to bottom.

| Stage           | Question it answers                    | Example metrics                             |
| --------------- | -------------------------------------- | ------------------------------------------- |
| **A**cquisition | How do users find you?                 | New sign-ups, CAC (cost to get a customer)  |
| **A**ctivation  | Do they have a great first experience? | Profile completed, first order placed       |
| **R**etention   | Do they come back?                     | Monthly retention rate, churn rate          |
| **R**eferral    | Do they tell friends?                  | k-factor (referrals sent x conversion rate) |
| **R**evenue     | How do you make money?                 | LTV (lifetime value), ARPU                  |

**Key rule:** LTV should be higher than CAC, or the business loses money on each user.

---

## Good vs Bad Metrics

### Bad metrics (avoid these)

| Type            | What it means                   | Example                                      |
| --------------- | ------------------------------- | -------------------------------------------- |
| **Vanity**      | Sounds nice, means nothing      | "Profiles viewed" on a dating app            |
| **Irrelevant**  | Not tied to business goal       | "Time spent" on a dating app (not the point) |
| **Impractical** | Can't actually measure it       | "Number of 3rd dates that happened"          |
| **Complicated** | Hard to explain to stakeholders | Multi-component composite scores             |
| **Delayed**     | Takes too long to collect       | "Number of marriages from the app"           |

### Good metrics have 4 qualities (remember: MMUT)

1. **M**eaningful -- tied to business goals, can drive decisions
2. **M**easurable -- simple to consistently and reliably track
3. **U**nderstandable -- stakeholders know what it means by its name
4. **T**imely -- can be collected in a reasonable time frame

### North Star vs Guardrail Metrics

- **North Star** = the ONE main metric you care about most
- **Guardrail** = metrics that should NOT get worse while you optimize the north star
- Example: Removing harmful posts is the north star. Guardrails = posts viewed, likes, comments (don't nuke engagement)

---

## Framework 1: Defining a Metric (3 Steps)

1. **Clarify the product & its purpose**
   - Who uses it? What's the user flow? Why does the company care?
   - Ask clarifying questions! Don't assume.

2. **Explain the product & business goals**
   - Connect the product to the company's mission and revenue model
   - Bonus points for tying to company mission

3. **Define success metrics using AARRR**
   - Walk through the funnel: acquisition, activation, engagement, retention, revenue
   - Pick a north star + guardrails

### Worked Example: Facebook Dating

| Step          | What you say                                                                                                                                                                                                                          |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Clarify       | "Is this standalone or in-app? Casual or serious dating? What age group?"                                                                                                                                                             |
| Business goal | Drive engagement on Facebook overall; keep people in the FB ecosystem; tie to mission of meaningful relationships                                                                                                                     |
| Metrics       | **Acquisition:** sign-ups, profile completion. **Activation:** viewed 10 profiles, got first match. **Engagement:** matches/user, swipes/user. **Retention:** % active after 28 days. **Revenue:** paid memberships or ad impressions |

---

## Framework 2: Diagnosing a Metric Change (4 Steps)

1. **Scope the change**
   - What exactly does this metric mean? Is it a ratio (which part moved)?
   - How big is the change? Sudden or gradual? What time period?

2. **Hypothesize contributing factors** (4 buckets)
   - **Accidental:** Logging bug? Data pipeline broken?
   - **Natural:** Seasonality? Holiday? Day of week?
   - **Internal:** New feature launch? UI change? Bug fix?
   - **External:** Competitor launch? Pandemic? News event?

3. **Validate each factor**
   - Slice data by segment (age, country, device, platform)
   - Walk UP the product funnel to find where things broke
   - Check upstream metrics to pinpoint the issue

4. **Classify each factor**
   - **Root cause:** the actual reason
   - **Contributing factor:** helps the root cause but isn't THE cause
   - **Correlated result:** symptom, not cause
   - **Unrelated:** noise

### Worked Example: Instagram Comments Declining

| Step        | What happened                                                                                                                                          |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Scope       | Avg comments/post down 10% YoY, slow decline over 6 months, posts are still growing                                                                    |
| Hypothesize | UI change to comment composer? More ads crowding out comments? Reels cannibalizing comments? New moderation feature?                                   |
| Validate    | Slice by account age -- newer accounts have sharper decline. Run cohort analysis -- diverges for users who joined ~6 months ago                        |
| Root cause  | New interstitial on onboarding lets users turn off comments. Some posts get zero comments. Remove those posts from analysis and the decline disappears |

---

## Framework 3: Designing an A/B Test (4 Steps)

1. **Pick a metric to test**
   - Choose core metric + guardrails. Don't cherry-pick after the fact!

2. **Define thresholds**
   - Significance level (alpha): usually 0.05
   - Power (1 - beta): usually 0.8
   - Minimum detectable effect (MDE): smallest change worth caring about

3. **Decide sample size & experiment length**
   - Use MDE + power + variance to calculate sample size
   - Rule of thumb: run at least 2 weeks (captures day-of-week effects)

4. **Assign groups**
   - Randomize users into control & treatment
   - At big companies, the A/B testing platform handles this

---

## A/B Testing Pitfalls (know these cold)

| Pitfall              | What it means                                                     | How to handle it                                                       |
| -------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Non-normality**    | Your metric isn't normally distributed                            | Bootstrap, use Wilcoxon rank-sum test, or collect more data for CLT    |
| **Multiple testing** | Running 100 tests = some will be "significant" by chance          | Bonferroni correction, control FDR (false discovery rate), or FWER     |
| **Network effects**  | Users influence each other (social networks)                      | Cluster by sub-networks using graph partitioning; randomize by cluster |
| **Novelty effects**  | New feature causes temporary spike or dip                         | Compare new vs old users; wait for the spike to stabilize              |
| **Primacy effects**  | Users resist change because they like what's familiar             | Same as novelty -- check new users only                                |
| **Holdouts**         | Small group never gets the new feature, for long-term measurement | Keeps ~1-5% of users on old experience to track long-term impact       |

### When NOT to A/B Test

- **No infrastructure** -- small company, no testing platform
- **No impact** -- the change is too small to matter
- **No traffic** -- not enough users to reach significance
- **No isolation** -- can't create a proper control group (e.g., logo change)
- **No conviction** -- testing 60 random variants with no hypothesis

### When A/B testing isn't possible, use:

- Focus groups and surveys
- User activity log analysis
- Ship it, then do a retrospective analysis (before/after with historical data)

---

## Metric Trade-Off Approach

When asked "Revenue up 1% but engagement down 3% -- should we ship?"

1. **Clarify both metrics** -- what exactly do they measure?
2. **Understand the product & business** -- which metric matters more to the company right now?
3. **Ask clarifying questions** -- how hard/easy is each metric to move? Is the trade-off reversible?
4. **Recommend one of three options:**
   - **Revert** the change (trade-off is not acceptable)
   - **Mitigate** (brainstorm ways to keep the gain while reducing the loss)
   - **Accept** the trade-off (it's justified by the business context)

### Worked Example: LinkedIn Ads

- Feature shows more ads on LinkedIn. Revenue up 1%, engagement (time spent) down 3%.
- 1% revenue is easy to get through better ad targeting instead
- 3% engagement drop is HARD to recover and could unwind progress
- Recommendation: probably revert, or add "hide this ad" features to reduce engagement hit

---

## Interview Tips (keep in your pocket)

1. **Ask clarifying questions first** -- understand the product, user, business goal
2. **Talk out loud** -- interviewer wants to see your thought process
3. **Be conversational** -- talk WITH the interviewer, not AT them
4. **Keep business goals front and center** -- tie everything back to the company mission
5. **Mention guardrail metrics** after picking your north star
6. **Bring outside experience** -- reference your own domain knowledge tactfully
7. **Do your homework** -- research the company's product, business model, and competitors before the interview

---

## Case Study Tips (Ch 11)

- **Clarify, Clarify, Clarify** -- #1 mistake is jumping to a solution without understanding the problem
- **Be Coachable** -- when the interviewer hints at a direction, follow it
- **Stay Pragmatic** -- suggest realistic solutions, not moonshots
- **Mention Trade-offs** -- every approach has pros and cons, say them
- **Timebox Yourself** -- don't ramble; give a crisp answer, then ask if they want more detail
