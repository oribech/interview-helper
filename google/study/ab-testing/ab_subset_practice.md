# A/B Testing Practice Pack

## Read This First

Use the **PDF page numbers** below.

That means:

- open the PDF
- jump to page `1`, `25`, `42`, and so on
- ignore the printed book page number on the page itself

Main PDF:

- [ab_subset_single_260311_164041.pdf](/Users/oribecher/Projects/private/job_interview/positions/google/books/ab_subset_single_260311_164041.pdf)

Quiz:

- [ab_subset_quiz.py](/Users/oribecher/Projects/private/job_interview/positions/google/study/ab-testing/ab_subset_quiz.py)

Question bank:

- [ab-testing.md](/Users/oribecher/Projects/private/job_interview/positions/google/questions/ab-testing.md)

## Rules

- Read small.
- Speak out loud.
- No long notes.
- No trying to finish the book.
- If a page becomes too mathy, skim it and move on.

## Start Now: First 90 Minutes

Do this exact order.

### Step 1

Read **PDF pages 1-3**.

Time: 12 minutes

Focus on:

- why experiments matter
- correlation is not causation
- OEC

After reading, say this out loud:

- `Correlation is not causation.`
- `Experiment is how I get closer to causal truth.`
- `OEC is the main metric I care about.`

Then answer:

- `Why is lower churn among feature users not enough to prove the feature works?`

Good answer:

- feature use was not randomized
- heavy users may both use the feature more and churn less
- that is confounding

### Step 2

Read **PDF pages 25-27**.

Time: 15 minutes

Focus on:

- how to design an experiment
- randomization unit
- power
- run long enough to cover day-of-week

After reading, say this out loud:

- `First I define hypothesis and metrics.`
- `Then I choose randomization unit.`
- `Then I make sure runtime and power are enough.`

Then answer:

- `Walk me through how you would design an A/B test.`

Good answer skeleton:

1. hypothesis
2. OEC plus guardrails
3. randomization unit
4. runtime and power
5. decision rule

### Step 3

Read **PDF pages 42-44**.

Time: 15 minutes

Focus on:

- choosing randomization unit
- why user-level randomization is common
- why analysis unit and randomization unit should usually match

After reading, say this out loud:

- `User is usually the safest default randomization unit.`
- `If I randomize by user, I should be careful not to treat pageviews as independent.`
- `Wrong unit choice can break trust in the result.`

Then answer:

- `Why can randomizing by user and analyzing pageviews create false positives?`

Good answer:

- pageviews from the same user are correlated
- independence assumption breaks
- variance can be underestimated

### Step 4

Read **PDF pages 46-48**.

Time: 15 minutes

Focus on:

- ramping
- risk
- MPR
- why not ship to 100% at once

After reading, say this out loud:

- `Ramping is for safety, not just measurement.`
- `Pre-MPR is for catching bad problems early.`
- `MPR is where I measure well.`

Then answer:

- `Why not launch a risky feature to 100% on day one?`

Good answer:

- blast radius is too large
- ramping controls risk
- MPR gives cleaner measurement later

### Step 5

Time: 20 to 30 minutes

Do one:

- run `uv run python /Users/oribecher/Projects/private/job_interview/positions/google/study/ab-testing/ab_subset_quiz.py --limit 10`
- answer `Q026` and `Q030` from [ab-testing.md](/Users/oribecher/Projects/private/job_interview/positions/google/questions/ab-testing.md) out loud

If you do only these 5 steps, that is already a good start.

## Day 1 Exact Pages

Read these exact PDF pages today:

1. **1-3**: causality, OEC, why experiments
2. **25-27**: experiment design
3. **42-44**: randomization unit
4. **46-48**: ramping

If you still have energy, add:

5. **29-31**: how to interpret results and practical vs statistical significance

## Day 2 Exact Pages

Read these exact PDF pages tomorrow:

1. **52-54**: t-test, p-value, confidence interval
2. **56-58**: Type I, Type II, power, multiple testing
3. **60-62**: variance basics and common pitfall
4. **64-65**: how to improve sensitivity
5. **67-68**: what A/A tests are and why they matter
6. **69-70**: skim the CTR example, just get the idea

Optional:

7. **71**: redirect example

## What To Say After Each Topic

Keep it baby-simple.

### Causality

- `Observational pattern is not proof.`
- `Users are different from each other.`
- `Experiment helps separate treatment from confounding.`

### Experiment Design

- `I start with hypothesis.`
- `I choose one main metric and some guardrails.`
- `I decide unit, runtime, and power.`

### Randomization Unit

- `User-level is common because product impact is often at user level.`
- `Smaller units can increase power but can also break assumptions.`

### Ramping

- `Go small first.`
- `Catch bugs early.`
- `Measure well before full launch.`

### Stats

- `p-value is not the probability the null is true.`
- `Confidence interval shows plausible effect range.`
- `Power is chance to detect a real effect of the size I care about.`

### Variance

- `High variance makes experiments noisy.`
- `Lower variance means easier detection.`
- `Triggered analysis and CUPED can help.`

### A/A Tests

- `A/A means both sides are the same.`
- `If A/A shows many wins, something is wrong.`
- `A/A is for trust.`

## Traps To Kill Fast

- `p-value = probability the null is true`
- `not significant = no effect`
- `big lift is fine even with SRM`
- `A/A tests are useless`
- `if I randomized by user, pageviews are independent too`

## Bare Minimum If You Are Tired

Do only this:

1. read **PDF 1-3**
2. read **PDF 25-27**
3. answer `Walk me through how you'd design an A/B test`
4. run `uv run python /Users/oribecher/Projects/private/job_interview/positions/google/study/ab-testing/ab_subset_quiz.py --limit 5`

That is enough for today if your brain is cooked.
