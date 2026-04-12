# Round 1 Study Plan

## Table of Contents

- [Round 1 Study Plan](#round-1-study-plan)
  - [Table of Contents](#table-of-contents)
  - [Context](#context)
    - [Block 1: SQL Drills (2 hrs)](#block-1-sql-drills-2-hrs)
    - [Block 2: Python Coding From Scratch (2 hrs)](#block-2-python-coding-from-scratch-2-hrs)
    - [Block 3: Applied Analysis + Ambiguity Training (1.5 hrs)](#block-3-applied-analysis--ambiguity-training-15-hrs)
    - [Block 4: Measurement \& Modeling Concepts (1.5 hrs)](#block-4-measurement--modeling-concepts-15-hrs)
    - [Block 5: Experimentation \& Business Cases (2.5 hrs)](#block-5-experimentation--business-cases-25-hrs)
    - [Block 6: Cheatsheet Review (45 min)](#block-6-cheatsheet-review-45-min)
    - [Block 7: Full Mock — Round 1 Format (1 hr)](#block-7-full-mock--round-1-format-1-hr)
    - [Block 8: Weak Spot Patch (30 min)](#block-8-weak-spot-patch-30-min)
  - [Key Files](#key-files)

---

## Context

Google DS interview Round 1 — rescheduled to **~April 14**. Round 1 covers:

- **Coding** (SQL + Python — from scratch on shared doc, no IDE/libraries guaranteed)
- **Applied Analysis & Experiments** (open-ended, ambiguity-heavy, clarify-first format)
- **Measurement & Modeling Concepts** (stats, ML, metrics definition, supervised/unsupervised)

**Already completed** (from prior sessions):

- Stats/Probability: strong (mock + 13 Glassdoor drills + symmetry/Bayes patterns)
- Transformers/LLM eval: strong (12-Q quiz, cheatsheet, eval metrics doc)
- Diagnostic mock: done (weak areas identified: probability edge cases, clustering metrics)

**Process:** Drill protocol, communication training, gate tests, and statefulness rules are in the [skill file](../../.claude/skills/round1-drill/SKILL.md). This file is the **what** (blocks, drills, schedule). The skill is the **how** (protocols, frameworks, tone).

---

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

**Key patterns:** GROUP BY + HAVING, window functions (LAG, LEAD, ROW_NUMBER, RANK), CTEs, CASE WHEN, date extraction.

### Block 2: Python Coding From Scratch (2 hrs)

No pandas/sklearn guaranteed. Practice writing on shared doc. Use Glassdoor Q061, Q066-Q073, Q076.

| Drill                                                      | Time   | Source                |
| ---------------------------------------------------------- | ------ | --------------------- |
| Bootstrap CI & Compute p-value from scratch (math/code)    | 25 min | Q015-Q016, Guide      |
| Linear regression (OLS) from scratch — fit + predict       | 20 min | Q060                  |
| Logistic regression / sigmoid from scratch — fit + predict | 15 min | Guide (stat modeling) |
| Data manipulation: combine, groupby, filter, handle nulls  | 20 min | Q072, Guide example   |
| Two-sample t-test from scratch (test statistic + p-value)  | 10 min | Guide (stat coding)   |
| IQR outlier detection function                             | 15 min | Q061                  |
| Generate N samples from normal distribution + plot         | 15 min | Q019                  |
| Bernoulli matrix, divide by column sums                    | 10 min | Q025                  |
| Sum of squares, basic algorithms                           | 10 min | Q076                  |

**Key patterns:** `random` module (no numpy), manual mean/std/median, dictionary-based groupby, list comprehensions, f-strings for output.

---

### Block 3: Applied Analysis + Ambiguity Training (1.5 hrs)

Practice the Google format: vague question → clarify → assume → analyze → recommend.

| Drill                                                   | Time   | Focus                                      |
| ------------------------------------------------------- | ------ | ------------------------------------------ |
| "How would you measure success of Google Maps?"         | 15 min | Metric definition, user-centric thinking   |
| "YouTube adoption is low, investigate cause"            | 15 min | Q079 — diagnostic framework                |
| "What model would you fit to this dataset to answer X?" | 20 min | Official Guide — Model selection/tradeoffs |
| "Product X launch — what metrics to track?"             | 15 min | Recruiter example, Q078                    |
| "How to detect inappropriate content on YouTube?"       | 15 min | Q081 — ML + product sense                  |
| Practice clarifying questions (write 5 per scenario)    | 10 min | Muscle memory                              |

### Block 4: Measurement & Modeling Concepts (1.5 hrs)

Covers topics from official Google guide + Glassdoor question bank.

| Drill | Topic                                                       | Time   | Source                |
| ----- | ----------------------------------------------------------- | ------ | --------------------- |
| 1     | Bias-variance tradeoff, overfitting, regularization (L1/L2) | 15 min | Q036-Q041, Q056, Q058 |
| 2     | Clustering: K-means vs GMM, how to pick K                   | 10 min | Q047-Q048             |
| 3     | Decision trees → Random Forest → Boosting (differences)     | 10 min | Q036-Q037             |
| 4     | PCA — when and why                                          | 5 min  | Q049                  |
| 5     | Multicollinearity — detect, effect, fix                     | 5 min  | Q039-Q040             |
| 6     | Survival analysis — when to use, 1-sentence explanation     | 5 min  | Official guide        |
| 7     | Convex optimization — gradient descent intuition            | 5 min  | Official guide        |
| G1-G3 | Gate test (3 unseen, pass 2/3)                              | —      |                       |

**Already covered in earlier blocks:** Probability, hypothesis testing, regression (linear/logistic), bootstrap, cross-validation, Monte Carlo (via bootstrap).

### Block 5: Experimentation & Business Cases (2.5 hrs)

Covers the full "Experimentation & Applied Analysis" interview section: A/B test design + hybrid business case questions. Drills 1-2 done (framework + Google Play discount).

**Part A — A/B Test Design (remaining drills)**

| Drill | Topic                                                  | Time   | Source      |
| ----- | ------------------------------------------------------ | ------ | ----------- |
| ~~1~~ | ~~Experiment design framework (8-step skeleton)~~      | done   | Sprint plan |
| ~~2~~ | ~~10% Google Play discount — full walkthrough~~        | done   | Recruiter   |
| 3     | YouTube new feature — full A/B test design             | 20 min | Q028, Q030  |
| 4     | Common pitfalls: novelty, selection bias, SRM, network | 15 min | Q032, Q034  |
| 5     | Sample size + MDE tied to business logic               | 15 min | Sprint plan |

**Part B — Business Case Hybrids (the gap from mock)**

| Drill | Topic                                                                 | Time   | Source             |
| ----- | --------------------------------------------------------------------- | ------ | ------------------ |
| 6     | "We ran a promo/trial. Should we make it permanent?" (evaluate)       | 20 min | Mock gap           |
| 7     | "A/B test shows X improved but Y dropped. Should we ship?" (tradeoff) | 15 min | Ch 10 (10.5, 10.6) |
| 8     | "Build a recommendation system for product X" (end-to-end case)       | 20 min | Ch 11 (Amazon)     |
| G1-G3 | Gate test (3 unseen, pass 2/3)                                        | —      |                    |

**Must-know terms:** OEC, guardrail metrics, randomization unit, p-value, CI, Type I/II errors, power, novelty effect, primacy effect, MDE, A/A test, SRM, triggered analysis, CUPED.

---

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

| File                                               | Purpose                              |
| -------------------------------------------------- | ------------------------------------ |
| `questions/python-sql.md`                          | Q061-Q077 coding questions           |
| `questions/ab-testing.md`                          | Q026-Q035 experiment questions       |
| `questions/ml-llm-eval.md`                         | Q036-Q060 modeling questions         |
| `questions/product-sense.md`                       | Q078-Q084 applied analysis           |
| `study/ab-testing/ab-testing-2-day-sprint.md`      | A/B testing framework & skeleton     |
| `study/ml-llm-eval/CHEATSHEET.md`                  | ML/LLM eval quick reference          |
| `study/stats-probability/CHEATSHEET.md`            | Stats quick reference                |
| `study/ml-llm-eval/eval-metrics.md`                | Detailed eval metrics                |
| `research/provided-materials/materials-website.md` | Official Google prep guide           |
| `books/ace-ds-interivew.md`                        | Ch 8 SQL, Ch 10 Product, Ch 11 Cases |
| `round1-prep/CHEATSHEET.md`                        | Patterns learned during drills       |
| `round1-prep/product-sense-lesson.md`              | Frameworks + worked examples         |
| `round1-prep/product-sense-qa.md`                  | 26 Q&As flashcard style              |
| `round1-prep/QUESTION_INVENTORY.md`                | 93 Glassdoor Qs with status          |
