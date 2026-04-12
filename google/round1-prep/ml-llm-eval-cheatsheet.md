# LLM + Transformers Cheatsheet

## Transformer types

| Type | Sees | Good at | Example |
|------|------|---------|---------|
| Encoder-only | All tokens (bidirectional) | Understanding, classification | BERT |
| Decoder-only | Only previous tokens (left→right) | Generation | GPT, LLaMA, Gemini |
| Encoder-decoder | Encoder reads input, decoder generates | Seq-to-seq (translation) | T5, original Transformer |

Modern LLMs are all **decoder-only**.

## BLEU — n-gram **precision**

How many n-grams in my output match the reference?

Ref: `the cat sat on the mat` → bigrams: {the cat, cat sat, sat on, on the, the mat}
Gen: `the cat on the mat` → bigrams: {the cat, cat on, on the, the mat}
Matches: 3/4 → **BLEU-2 = 0.75**

## ROUGE — n-gram **recall**

How many n-grams in the reference appear in my output?

Ref: `the big cat sat on the mat` (7 words)
Gen: `the cat`
**ROUGE-1 = 2/7 = 0.29**

Variants: ROUGE-1 (unigram), ROUGE-2 (bigram), ROUGE-L (longest common subsequence)

## BLEU vs ROUGE

```
Ref: "the big cat sat on the mat"   Gen: "the cat"
BLEU:  2/2 = 1.0   ← "everything I said was correct"
ROUGE: 2/7 = 0.29  ← "but you missed most of it"
```

## Perplexity — model confidence

PPL = 2^(-avg log₂ P(token))

P("the")=0.5, P("cat")=0.25, P("sat")=0.125
avg log₂ = (-1 + -2 + -3)/3 = -2 → **PPL = 4** ("choosing between ~4 options per token")

Lower = better. PPL=1 perfect, PPL=50k random guessing.

## BERTScore — semantic similarity

Embed tokens with BERT, cosine-similarity match each generated token to best reference token. "feline" ≈ "cat" → high score even when BLEU = 0.

## When to use / pros & cons

| Metric | Use for | Pro | Con |
|--------|---------|-----|-----|
| BLEU | Translation | Fast, standard | No semantics, no recall |
| ROUGE | Summarization | Catches missing content | No semantics |
| Perplexity | Model comparison | No reference needed | Doesn't measure quality |
| BERTScore | Open-ended gen | Captures meaning | Slow, needs model |
| Human eval | Chatbot/creative | Gold standard | Expensive, slow |

## LLM Eval Framework (3 layers)

1. **Automated metrics** (BLEU, ROUGE, NLI for hallucination) — cheap, fast, every change
2. **Human eval** — raters score accuracy/completeness/helpfulness. Check inter-rater agreement (Cohen's κ for 2 raters, Krippendorff's α for 3+)
3. **Online A/B test** — real user engagement + guardrails

**Key insight**: Automated metrics can improve while user experience degrades. Never trust metrics alone.

## RLHF (3 steps)

1. **SFT** — supervised fine-tune on (prompt, good_response) pairs
2. **Reward model** — train separate model on human preference rankings (which response is better?)
3. **PPO** — model generates, reward model scores, model updates to maximize reward + KL penalty (stay close to SFT model)

## Hallucination Detection

- **NLI model** (BERT-based, encoder-only, fast) — classifies each claim as supported/not supported by source
- **Self-consistency** — ask same question multiple times, contradictions = hallucination
- **Human eval** — raters flag unfaithful statements
