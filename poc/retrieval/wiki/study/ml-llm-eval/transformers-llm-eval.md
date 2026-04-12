# Transformers + LLM Evaluation

Source: google/study/ml-llm-eval/transformers-llm-eval.md

# Transformers + LLM Evaluation

## Part 1: Transformer Architecture

### The Problem It Solved

Before Transformers: RNNs processed words one-by-one (sequential, slow, forgot long-range context).
Transformers: process all words at once (parallel, fast, see everything).

### The Architecture (6 key pieces)

**1. Input Embedding + Positional Encoding**
- Words → vectors (embeddings)
- Since all words processed in parallel, model has no sense of order
- Add positional encoding: a vector that tells the model "this word is at position 3"

**2. Self-Attention (the core idea)**
- Every word asks: "which other words in this sentence should I pay attention to?"
- Each word gets 3 vectors:
  - **Q (Query)**: "what am I looking for?"
  - **K (Key)**: "what do I contain?"
  - **V (Value)**: "what info do I give if selected?"
- Attention score: softmax(QK^T / sqrt(d_k)) x V
- sqrt(d_k) = scaling factor to prevent huge dot products

**In plain words**: multiply every word's Query by every word's Key → get a relevance score → use that score to weight each word's Value → output is a weighted mix of all words, weighted by relevance.

**3. Multi-Head Attention**
- Run self-attention multiple times in parallel with different learned Q/K/V projections
- Each "head" captures a different type of relationship (syntax, semantics, coreference, etc.)
- Concatenate all heads, project back to original dimension

**4. Feed-Forward Network**
- After attention, each token passes through a small 2-layer neural net
- Same network applied independently to each position

**5. Residual Connections + Layer Norm**
- Add the input back to the output of each sub-layer (residual connection)
- Then normalize. Helps with training stability and gradient flow.

**6. Stack N times**
- Repeat the attention + feed-forward block N times (e.g., 12 for BERT-base, 96 for GPT-4)

### Encoder vs Decoder

| | Encoder | Decoder |
|---|---|---|
| Sees | All tokens at once | Only previous tokens (masked) |
| Used for | Understanding (classification, NER) | Generation (text, translation) |
| Example | BERT | GPT |

**Original paper (2017)**: encoder-decoder for translation.
**Modern LLMs**: decoder-only (GPT, LLaMA, Gemini).

---

## Part 2: LLM Evaluation Metrics

### Automatic Metrics

| Metric | What it measures | How |
|---|---|---|
| **BLEU** | N-gram overlap with reference | Precision of n-grams (1-4) vs reference text. 0-1. |
| **ROUGE** | N-gram overlap (recall-oriented) | Recall of n-grams. ROUGE-L uses longest common subsequence. |
| **Perplexity** | How surprised the model is | 2^(cross-entropy). Lower = better. Only measures fluency, not correctness. |
| **BERTScore** | Semantic similarity | Cosine similarity of BERT embeddings. Catches paraphrases that BLEU misses. |
| **Exact Match / F1** | Factual accuracy | For QA tasks: does the answer match the gold answer? |

**Key limitation**: Automatic metrics measure surface similarity, not whether the answer is actually good, helpful, or safe. That's why human eval matters.

### When to use what

- **BLEU**: translation, summarization (when you have reference outputs)
- **ROUGE**: summarization
- **Perplexity**: comparing model versions on same data (lower = more fluent)
- **BERTScore**: when paraphrasing is OK (more flexible than BLEU)
- **Human eval**: always the gold standard, especially for open-ended generation

---

## Part 3: Human Evaluation & Rater Data

### Why it matters (directly from the job description)

The role involves "human evaluation data such as surveys and raters." This means designing eval tasks, managing rater quality, and interpreting results.

### Key Concepts

**Inter-Rater Reliability** — do raters agree with each other?
- **Cohen's Kappa**: agreement between 2 raters, adjusted for chance. κ > 0.8 = strong, 0.6-0.8 = moderate.
- **Krippendorff's Alpha**: generalization for multiple raters, any scale type. α > 0.8 = reliable.
- **Fleiss' Kappa**: like Cohen's but for 3+ raters.

**Rater Task Design**:
- Clear rubric with examples (anchor points)
- Calibration rounds before real rating
- Include gold questions (known correct answers) to catch low-quality raters
- Randomize order to prevent position bias

**Common rating scales**:
- Likert scale (1-5): "How helpful is this response?"
- Side-by-side (A vs B): "Which response is better?" ← used in RLHF
- Binary: "Is this response factually correct? Yes/No"

### Problems with human eval
- Expensive and slow
- Rater fatigue → quality drops
- Subjective tasks → low agreement
- Solution: clear rubrics + calibration + gold questions + measure IRR

---

## Part 4: RLHF (Reinforcement Learning from Human Feedback)

### The pipeline (3 steps)

**Step 1: Supervised Fine-Tuning (SFT)**
- Train base model on high-quality (prompt, response) pairs
- Result: model that follows instructions

**Step 2: Reward Model Training**
- Show raters pairs of responses, they pick the better one (side-by-side)
- Train a reward model to predict human preferences
- This is where rater data quality matters most

**Step 3: RL Optimization (PPO)**
- Model generates responses
- Reward model scores them
- Update model to maximize reward score
- KL penalty prevents model from drifting too far from SFT model

### Why this matters for the role
You'd be designing the evaluation frameworks that feed into step 2. Bad rater data = bad reward model = bad LLM.

---

## Part 5: Evaluating LLM Features in Production

### A/B testing LLM features
Same as regular A/B testing but with extra considerations:
- **Latency**: LLM responses are slower. Measure user patience / abandonment.
- **Quality metrics**: Need both automatic (BLEU/ROUGE) AND human eval
- **Safety**: Check for hallucinations, harmful content, bias before launch
- **User satisfaction**: Thumbs up/down, task completion rate, retention

### Evaluation framework for LLM features
1. Define task-specific metrics (not just generic quality)
2. Build evaluation dataset with gold-standard responses
3. Run automatic metrics for fast iteration
4. Use human raters for final quality assessment
5. A/B test with real users for product impact
6. Monitor post-launch for drift / degradation
