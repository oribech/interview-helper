# Probability: 5 Patterns for DS Interviews

Source: google/study/stats-probability/probability-patterns.md

# Probability: 5 Patterns for DS Interviews

## Pattern 1: Counting

P = favorable / total

**Step 1**: Define total outcomes.
- Independent choices → multiply: k^n (n people each pick from k options)
- **Permutations** (n!): Abstract question: *"How many ways to assign items to specific positions/slots?"* [^1]
- **Combinations** (C(n,k)): Abstract question: *"How many ways to select a subset of items from a group?"*

**Step 2**: Count favorable outcomes the same way. [^2]

## Pattern 2: Conditional Probability & Bayes

P(A|B) = P(A∩B) / P(B)

Bayes: P(A|B) = P(B|A) · P(A) / P(B)

**Independence**: P(A|B) = P(A). Each trial is fresh. Past outcomes don't change future probabilities.

**Information value**: A question is more useful if the answer changes your probability more. Splitting 50/50 is better than 1/52 vs 51/52.

## Pattern 3: Symmetry Trick

Find two events with **equal probability regardless of unknowns**, then condition on that subset.

Example: For any biased coin with P(H)=p:
- P(HT) = p(1-p)
- P(TH) = (1-p)p → same!

→ Condition on {HT, TH}, discard {HH, TT}. Now it's fair.

**When to use**: When a problem has an unknown parameter you can't compute. Look for events where the unknown cancels out.

## Pattern 4: Distributions

| Distribution | Use when | Parameters |
|---|---|---|
| Bernoulli | Single yes/no trial | p |
| Binomial | Count of successes in n trials | n, p |
| Poisson | Count of rare events in fixed time/space | λ (rate) |
| Exponential | Time between Poisson events | λ |
| Geometric | Trials until first success | p |
| Uniform | All outcomes equally likely | a, b |
| Normal | Sum of many independent things (CLT) | μ, σ |

**Key relationships**:
- Binomial → Poisson when n large, p small, np = λ
- Exponential is memoryless: P(X > s+t | X > s) = P(X > t)

## Pattern 5: Simulation / Inverse CDF

To generate samples from any distribution X using only Uniform(0,1):

1. Generate U ~ Uniform(0,1)
2. Return F⁻¹(U) where F is the CDF of X

**Why it works** (probability integral transform): If X ~ F, then F(X) ~ Uniform(0,1). So the reverse also works.

**For Normal**: Use Box-Muller: take U1, U2 ~ Uniform(0,1), compute Z = √(-2·ln(U1)) · cos(2π(U2)). Z ~ Normal(0,1). [^3]

---

## Universal Method: When Stuck

**Write out the full sample space.** List every outcome. Interview probability questions never have more than ~10-20 outcomes. The answer becomes obvious once you see them all.

---

## Appendix: Intuition Notes

[^1]: **Permutations**: Because order matters (e.g., ABC ≠ CBA), every time you place an item, the pool of remaining choices shrinks: n × (n-1) × ... × 1.

[^2]: **Count the same way**: Never mix methods! If your total count ignores order (combinations), your favorable count must also ignore order. If one uses permutations, both must.

[^3]: **Box-Muller**: We cannot simply use F⁻¹(U) because the Normal CDF lacks a closed-form math formula for its inverse. Box-Muller smartly bypasses this using 2D geometry to generate exact Normal values with basic math functions.
