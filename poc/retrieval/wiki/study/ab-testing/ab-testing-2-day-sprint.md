# 2-Day A/B Testing Sprint for Google Interview

Source: google/study/ab-testing/ab-testing-2-day-sprint.md

# 2-Day A/B Testing Sprint for Google Interview

## Goal

In 2 days, get interview-ready on A/B testing for Google, not textbook-complete.

Assumption: about 4 focused hours per day.

## Use These Files

- Main PDF: [ab_subset_single_260311_164041.pdf](/Users/oribecher/Projects/private/job_interview/positions/google/books/ab_subset_single_260311_164041.pdf)
- Practice pack: [ab_subset_practice.md](/Users/oribecher/Projects/private/job_interview/positions/google/study/ab-testing/ab_subset_practice.md)
- Quiz: [ab_subset_quiz.py](/Users/oribecher/Projects/private/job_interview/positions/google/study/ab-testing/ab_subset_quiz.py)
- Question bank: [ab-testing.md](/Users/oribecher/Projects/private/job_interview/positions/google/questions/ab-testing.md)

## End Deliverables

By the end of Day 2, you should be able to do all of these out loud:

1. Give a clean 5-minute answer to: "Design an A/B test for a Google product."
2. Explain `p-value`, `confidence interval`, `Type I`, `Type II`, and `power` in plain English.
3. Explain why correlation does not imply causality.
4. Explain how to choose a randomization unit and why user-level randomization is common.
5. Explain `A/A test`, `SRM`, guardrails, novelty effects, and ramping.
6. Handle at least 6 mock questions from [ab-testing.md](/Users/oribecher/Projects/private/job_interview/positions/google/questions/ab-testing.md) without freezing.

## Non-Negotiables

Do not try to read the whole PDF.

For every study block:

1. Read for 3 to 5 minutes only.
2. Close the material.
3. Recall out loud.
4. Do one mini-case.
5. Move on.

## Day 1: Foundations and Experiment Design

Total: about 4 hours

### Block 1: Causality and OEC

Time: 45 minutes

- Read from the PDF/practice pack:
  - Why experiments matter
  - Correlation vs causality
  - OEC
- Practice:
  - Explain why lower churn among adopters does not prove the feature works.
  - Define OEC in one sentence.

Deliverable:

- 60-second answer for `Why experiment instead of observational data?`

### Block 2: Experiment Design

Time: 60 minutes

- Study:
  - Hypothesis
  - Treatment and control
  - Target population
  - OEC and guardrails
  - Runtime and day-of-week effects
- Practice:
  - Answer: `Walk me through how you'd design an A/B test.`

Deliverable:

- 5-step answer framework for experiment design:
  - hypothesis
  - OEC and guardrails
  - randomization unit
  - runtime and power
  - launch decision

### Block 3: Randomization Unit

Time: 45 minutes

- Study:
  - User vs session vs pageview/query
  - Independence assumptions
  - Why analysis unit should usually match randomization unit
- Practice:
  - Explain why randomizing by user and analyzing pageviews naively can create false positives.

Deliverable:

- 90-second answer for `How do you choose a randomization unit?`

### Block 4: Ramping and Trust

Time: 45 minutes

- Study:
  - Pre-MPR
  - MPR
  - Why not ship to 100% immediately
  - Novelty and primacy
- Practice:
  - Explain a safe launch plan for a risky new feature.

Deliverable:

- 90-second answer for `How would you ramp an experiment?`

### Block 5: Day 1 Retrieval

Time: 45 minutes

- Run:
  - `uv run python /Users/oribecher/Projects/private/job_interview/positions/google/study/ab-testing/ab_subset_quiz.py --limit 12`
- Then answer 2 questions from [ab-testing.md](/Users/oribecher/Projects/private/job_interview/positions/google/questions/ab-testing.md) out loud.

Deliverable:

- You can answer `Q026` and one of `Q028/Q030/Q031` without notes.

## Day 2: Statistics, Sensitivity, and Interview Rehearsal

Total: about 4 hours

### Block 1: Core Stats

Time: 60 minutes

- Study:
  - t-test intuition
  - p-value
  - confidence interval
  - Type I and Type II
  - power
- Practice:
  - Explain what `p = 0.03` means.
  - Explain why non-significant does not mean no effect.

Deliverable:

- 2-minute plain-English explanation of significance and power.

### Block 2: Variance and Sensitivity

Time: 45 minutes

- Study:
  - Why variance matters
  - Ratio metrics
  - Outliers
  - Triggered analysis
  - CUPED at a high level
- Practice:
  - Answer: `My experiment is underpowered. What can I do besides waiting longer?`

Deliverable:

- List 4 levers for improving sensitivity.

### Block 3: A/A Tests and SRM

Time: 45 minutes

- Study:
  - Why A/A tests matter
  - What bad A/A results imply
  - Why SRM means results are not trustworthy
- Practice:
  - Explain what you would check if an experiment shows a huge win but has SRM.

Deliverable:

- 90-second answer for `What makes an experiment result untrustworthy?`

### Block 4: Google-Style Mock Round

Time: 60 minutes

Answer these out loud, timed:

1. `Walk me through how you'd design an A/B test.`
2. `You made a product change. How do you test whether a metric increased?`
3. `How would you remove bias in an A/B test?`
4. `Design an experiment for a YouTube feature.`

Deliverable:

- 4 spoken mock answers, each under 5 minutes and reasonably structured.

### Block 5: Final Review

Time: 30 minutes

- Run:
  - `uv run python /Users/oribecher/Projects/private/job_interview/positions/google/study/ab-testing/ab_subset_quiz.py --limit 15`
- Review only the questions you miss.

Deliverable:

- Final weak-topic list with at most 3 items.

## Interview Answer Skeleton

Use this for most A/B testing interview questions:

1. State the product goal and hypothesis.
2. Define primary metric or OEC.
3. Add guardrails.
4. Choose randomization unit and target population.
5. Describe control, treatment, and ramp.
6. Mention runtime, power, and sanity checks.
7. Interpret effect size and significance.
8. Decide launch, iterate, or stop.

## Must-Know Terms

You should be able to define each in one or two lines:

- OEC
- Guardrail metric
- Randomization unit
- Analysis unit
- p-value
- Confidence interval
- Type I error
- Type II error
- Power
- Novelty effect
- Primacy effect
- MPR
- A/A test
- SRM
- Triggered analysis
- CUPED

## Done Means Ready

You are ready enough for this topic if:

- You can answer the 4 mock questions without reading.
- You can explain stats without using formula-first language.
- You can catch obvious traps like:
  - `p-value = probability the null is true`
  - `not significant = no effect`
  - `SRM is fine if the lift is large`
  - `A/A tests are useless`
