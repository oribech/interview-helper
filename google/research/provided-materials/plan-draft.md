# Round 1 Study Plan — 3 Days (March 25-27)

## Context

Google DS interview Round 1 is **March 27**. Round 1 covers:

- **Coding** (SQL + Python — from scratch on shared doc, no IDE/libraries guaranteed)
- **Applied Analysis & Experiments** (open-ended, ambiguity-heavy, clarify-first format)
- **Measurement & Modeling Concepts** (stats, ML, metrics definition, supervised/unsupervised)

**Already completed** (from prior sessions):

- Stats/Probability: strong (mock + 13 Glassdoor drills + symmetry/Bayes patterns)
- Transformers/LLM eval: strong (12-Q quiz, cheatsheet, eval metrics doc)
- Diagnostic mock: done (weak areas identified: probability edge cases, clustering metrics)

**Gaps (all untouched):** SQL, Python from scratch, A/B testing drills, applied analysis framework, survival analysis/convex optimization/Monte Carlo

**Budget:** 3 days × 4 hrs = **12 hours**

---

## Day 1 — Tuesday March 25: **Coding** (4 hrs)

### Block 1: SQL Drills (2 hrs)

Practice on shared-doc style (no IDE autocomplete). Use Glassdoor questions Q062-Q065, Q074.

| Drill                                                     | Time   | Source                                   |
| --------------------------------------------------------- | ------ | ---------------------------------------- |
| CTR over time (DATE, Impressions, Clicks table)           | 20 min | Recruiter example (materials-website.md) |
| YoY growth with window functions (LAG)                    | 20 min | Glassdoor Q064                           |
| Top-5 highest-selling items (GROUP BY + ORDER BY + LIMIT) | 15 min | Glassdoor Q065                           |
| JOIN types drill — LEFT/INNER/CROSS, explain when each    | 15 min | Glassdoor Q074                           |
| Window functions: ROW_NUMBER, RANK, DENSE_RANK, NTILE     | 20 min | Practice                                 |
| Day-of-week with highest CTR (EXTRACT + GROUP BY)         | 15 min | Recruiter example                        |
| A/B test SQL case study: compare control vs treatment     | 15 min | Glassdoor Q062                           |

**Key patterns to nail:** GROUP BY + HAVING, window functions (LAG, LEAD, ROW_NUMBER, RANK), CTEs for readability, CASE WHEN for conditional aggregation, date extraction.

**SQL interview tip (Ace the DS Interview, Ch 8):** "Work backwards — imagine you had all the info in a single ideal table so your query is just a SELECT. Then work backwards one SQL statement at a time to the original tables." Don't jump in without understanding the problem first.

### Block 2: Python Coding From Scratch (2 hrs)

No pandas/sklearn guaranteed. Practice writing on shared doc. Use Glassdoor Q061, Q066-Q073, Q076.

| Drill                                                       | Time   | Source                   |
| ----------------------------------------------------------- | ------ | ------------------------ |
| Bootstrap CI & Compute p-value from scratch (math/code)     | 25 min | Q015-Q016, Guide         |
| Linear regression (OLS) from scratch — fit + predict        | 25 min | Q060                     |
| Data manipulation: Combine 2 datasets (lists/dicts)         | 20 min | Q072, Guide example      |
| IQR outlier detection function                              | 15 min | Q061                     |
| Generate N samples from normal distribution + plot          | 15 min | Q019                     |
| Bernoulli matrix, divide by column sums                     | 10 min | Q025                     |
| Sum of squares, basic algorithms                            | 10 min | Q076                     |

**Key patterns:** `random` module (no numpy), manual mean/std/median, dictionary-based groupby, list comprehensions, f-strings for output.

---

## Day 2 — Wednesday March 26: **Experiments + Applied Analysis** (4 hrs)

### Block 3: A/B Testing & Experiment Design (2 hrs)

Use Glassdoor Q026-Q035 + recruiter's 10% discount example.

| Drill                                                           | Time   | Source                     |
| --------------------------------------------------------------- | ------ | -------------------------- |
| Walk through experiment design framework (8-step skeleton)      | 15 min | ab-testing-2-day-sprint.md |
| 10% Google Play discount — full walkthrough with clarifications | 25 min | Recruiter example          |
| YouTube new feature experiment design                           | 20 min | Q028, Q030                 |
| Hypothesis framing: OEC + guardrail metrics                     | 15 min | Q026                       |
| Sample size calculation (power, MDE, significance)              | 15 min | Sprint plan                |
| Two-drug experiment design (randomization, blocking)            | 15 min | Q029                       |
| Common pitfalls: novelty effect, selection bias, SRM            | 15 min | Q032, Q034                 |

**Must-know terms:** OEC, guardrail metrics, randomization unit, p-value, CI, Type I/II errors, power, novelty effect, primacy effect, MDE, A/A test, SRM, triggered analysis, CUPED.

**8-step answer skeleton:** Hypothesis → OEC + guardrails → Randomization unit → Sample size → Duration → Ramp plan → Analysis (statistical test) → Launch decision.

### Block 4: Applied Analysis + Ambiguity Training (1.5 hrs)

Practice the Google format: vague question → clarify → assume → analyze → recommend.

| Drill                                                      | Time   | Focus                                      |
| ---------------------------------------------------------- | ------ | ------------------------------------------ |
| "How would you measure success of Google Maps?"            | 15 min | Metric definition, user-centric thinking   |
| "YouTube adoption is low, investigate cause"               | 15 min | Q079 — diagnostic framework                |
| "What model would you fit to this dataset to answer X?"    | 20 min | Official Guide — Model selection/tradeoffs |
| "Product X launch — what metrics to track?"                | 15 min | Recruiter example, Q078                    |
| "How to detect inappropriate content on YouTube?"          | 15 min | Q081 — ML + product sense                  |
| Practice clarifying questions (write 5 per scenario)       | 10 min | Muscle memory                              |

**Framework:** (1) Clarify scope & stakeholders, (2) State assumptions, (3) Define metrics (primary + guardrail), (4) Propose analysis approach, (5) Discuss tradeoffs, (6) Recommend with caveats.

**Product metrics framework (Ace the DS Interview, Ch 10):** Use AARRR pirate metrics as your mental model for metric definition questions: **A**cquisition → **A**ctivation → Engagement → **R**etention → **R**eferral → **R**evenue. A good metric is: Meaningful (tied to business goals, actionable), Measurable (simple to track), not Vanity (looks nice but drives no decisions), not Delayed (marriage count vs. match count), not Irrelevant (time-spent on a dating app ≠ success).

**Case study approach (Ace the DS Interview, Ch 11):** The Citadel (revenue estimation), Amazon (recommendation), and Airbnb (listing revenue) cases are excellent practice — they follow exactly the Applied Analysis format: Clarify business goal → Scope down → State assumptions → Propose model/analysis → Discuss tradeoffs & counter metrics → Address limitations. Key tip: "Pretend you've already been hired — you're just having a meeting with a co-worker about the problem."

### Block 5: Measurement and modeling concepts - Quick Fills (30 min)

| Topic                                                  | Time   | Source               |
| ------------------------------------------------------ | ------ | -------------------- |
| Survival analysis — 5-line teach + when to use         | 10 min | Q109 topic list      |
| Convex optimization — intuition + gradient descent     | 10 min | Materials-website.md |
| Monte Carlo methods — bootstrap connection, simulation | 10 min | Q017-Q018            |

---

## Day 3 — Thursday March 27 (Interview Day): **Review + Mock** (2-3 hrs morning)

### Block 6: Cheatsheet Review (45 min)

- Stats/Probability CHEATSHEET.md (15 min)
- ML/LLM eval CHEATSHEET.md + eval-metrics.md (15 min)
- A/B testing must-know terms (15 min)

### Block 7: Full Mock — Round 1 Format (1 hr)

Timed simulation of actual Round 1:

- Coding segment (20 min): 1 SQL + 1 Python question, shared-doc style
- Applied Analysis & Experiments (20 min): Open-ended scenario with clarification
- Measurement & Modeling (20 min): Metric definition + statistical modeling question

Score and identify last-minute gaps.

### Block 8: Weak Spot Patch (30 min)

Address anything flagged in mock. Re-read key formulas. Mental warm-up.

---

## Key Files

| File                                               | Purpose                          |
| -------------------------------------------------- | -------------------------------- |
| `questions/python-sql.md`                          | Q061-Q077 coding questions       |
| `questions/ab-testing.md`                          | Q026-Q035 experiment questions   |
| `questions/ml-llm-eval.md`                         | Q036-Q060 modeling questions     |
| `questions/product-sense.md`                       | Q078-Q084 applied analysis       |
| `study/ab-testing/ab-testing-2-day-sprint.md`      | A/B testing framework & skeleton |
| `study/ml-llm-eval/CHEATSHEET.md`                  | ML/LLM eval quick reference      |
| `study/stats-probability/CHEATSHEET.md`            | Stats quick reference            |
| `study/ml-llm-eval/eval-metrics.md`                | Detailed eval metrics            |
| `research/provided-materials/materials-website.md` | Official Google prep guide       |
| `books/ace-ds-interivew.md`                        | Ch 8 SQL, Ch 10 Product, Ch 11 Cases |

## How We'll Work Together

For each drill block, I'll:

1. Present a question (Glassdoor or recruiter-style)
2. You answer as if in the interview (shared doc, think out loud)
3. I give immediate feedback + correct solution if needed
4. We iterate until the pattern is locked in

For applied analysis drills, I'll play the interviewer — giving vague prompts and waiting for your clarifying questions before revealing more info.

### When you're stuck or wrong

**Don't know at all:**
1. Teach in 3-5 lines max (no lecture)
2. Re-quiz with a **different question** testing the same concept (prevent overfit — test the skill, not the answer)
3. If must-know: add to cheatsheet
4. Log as weak spot → revisit in Day 3 Block 8

**Partially know:**
1. Sharpen the gap (1-2 lines)
2. Re-quiz targeting **only the gap**, with a different question

**No idea + not critical for Round 1:**
1. Give a 1-line "interview survival answer" (enough to not blank)
2. Move on to higher-priority drills

## Verification

- After each block: quick self-check on key patterns
- Day 3 mock: timed, scored, realistic format
- If any block runs over, steal time from Block 5 (quick fills) first
