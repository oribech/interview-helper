# LLM Evaluation Metrics — From Zero to Interview Ready

## BLEU — "Did I use the right words?"

**Idea**: Count how many chunks (n-grams) in my output also appear in the reference.

**Calculate BLEU-1 (unigrams) by hand**:

Reference: `the cat sat on the mat`
Generated: `the the the the`

Step 1: Count unigram matches. "the" appears in reference? Yes.
Step 2: Raw precision = 4/4 = 1.0. But that's cheating — I just repeated "the".
Step 3: Clipped precision = min(count in generated, count in reference) / count in generated = 2/4 = 0.5
Step 4: Brevity penalty — generated is shorter than reference → penalty < 1

**Full BLEU** = brevity_penalty × exp(avg of log precisions for n=1,2,3,4)

**Calcualtion example (BLEU-2)**:

Reference: `the cat sat on the mat` → bigrams: {the cat, cat sat, sat on, on the, the mat}
Generated: `the cat on the mat` → bigrams: {the cat, cat on, on the, the mat}
Matches: {the cat, on the, the mat} → 3 out of 4
BLEU-2 precision = 3/4 = 0.75

---

## ROUGE — "Did I cover what matters?"

**Idea**: Of the words/chunks in the **reference**, how many appear in my output? (Recall, not precision)

**Calculate ROUGE-1 by hand**:

Reference: `the big cat sat on the mat` (7 tokens)
Generated: `the cat`

ROUGE-1 = matched unigrams / total unigrams in reference = 2/7 = 0.29

**Variants**:
- **ROUGE-1**: unigram recall
- **ROUGE-2**: bigram recall
- **ROUGE-L**: length of Longest Common Subsequence / reference length

**ROUGE-L example**:

Reference: `the cat is on the mat`
Generated: `the cat the mat`
LCS: `the cat` ... `the mat` → length 4
ROUGE-L = 4/6 = 0.67

---

## BLEU vs ROUGE — The key distinction

```
Reference:  "the big cat sat on the mat"
Generated:  "the cat"

BLEU:  2/2 = 1.0 precision  ← "everything I said was correct!"
ROUGE: 2/7 = 0.29 recall   ← "but you missed most of it"
```

**BLEU** punishes wrong words. **ROUGE** punishes missing words.

---

## Perplexity — "How confident is the model?"

**Idea**: If the model assigns high probability to each actual next token, perplexity is low.

**Formula**: PPL = 2^(-1/N × Σ log₂ P(token_i))

**Calculate by hand** (3 tokens):

Model predicts: P("the")=0.5, P("cat")=0.25, P("sat")=0.125
avg log₂ prob = (log₂0.5 + log₂0.25 + log₂0.125) / 3 = (-1 + -2 + -3) / 3 = -2
PPL = 2^(-(-2)) = 2^2 = 4

**Intuition**: PPL=4 means "at each token, the model was ~equally confused between 4 options"

- PPL = 1 → perfect prediction (knew every token)
- PPL = 50,000 → random guessing over 50k vocab

---

## BERTScore — "Do they mean the same thing?"

**Idea**: Embed each token with BERT, compute cosine similarity between generated and reference token embeddings.

**Steps**:
1. Embed reference tokens → vectors r₁, r₂, ...
2. Embed generated tokens → vectors g₁, g₂, ...
3. For each generated token, find its best-matching reference token (max cosine similarity)
4. Average those max similarities → BERTScore precision
5. Do reverse for recall. F1 = harmonic mean.

**Why it works**: "feline" and "cat" have similar BERT embeddings → high score even though BLEU gives 0.

No hand calculation needed — just know the intuition.

---

## When to use which

| Scenario | Use | Why |
|----------|-----|-----|
| Translation (one correct answer) | **BLEU** | Exact wording matters |
| Summarization (cover key points) | **ROUGE** | Recall matters — did you capture the content? |
| Comparing two LLMs | **Perplexity** | Lower PPL = better language model |
| Open-ended generation (many valid answers) | **BERTScore** | Captures meaning, not exact words |
| Chatbot/creative tasks | **Human eval** | No metric captures helpfulness well |

## Pros & Cons at a glance

| Metric | Pro | Con |
|--------|-----|-----|
| BLEU | Fast, no model needed, standard for translation | No semantics, ignores recall, needs reference |
| ROUGE | Catches missing content, good for summaries | No semantics, needs reference |
| Perplexity | No reference needed, just test set | Doesn't measure output quality directly |
| BERTScore | Captures semantic similarity | Slow, needs BERT model, less interpretable |
