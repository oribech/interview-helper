# 🎯 Google DS — Identity Personalization Interview Deep Research

Source: google/research/deep_research_interview_intel.md

# 🎯 Google DS — Identity Personalization Interview Deep Research

> **Role:** Data Scientist, Product, Identity Personalization · Google Tel Aviv  
> **Status:** Phone screen passed — 5 onsite interviews scheduled (2 rounds: tech + non-tech each, + 1 more)  
> **Last updated:** March 2026 · Sourced from: Reddit, Glassdoor, onsites.fyi, InterviewQuery, Kaggle, Medium, unofficial Google DS blog

---

## 📋 Interview Structure (Your Specific Setup)

Based on recruiter info: **5 interviews**, split into **2 rounds** (each with a tech + non-tech interview), plus **1 additional interview**.

### Most likely mapping:

| #   | Round      | Type               | Focus                          |
| --- | ---------- | ------------------ | ------------------------------ |
| 1   | Round 1    | Technical          | Coding (SQL/Python)            |
| 2   | Round 1    | Non-Technical      | Behavioral / Googleyness       |
| 3   | Round 2    | Technical          | Stats + ML + Experimentation   |
| 4   | Round 2    | Non-Technical      | Product Sense + Case Study     |
| 5   | Additional | Technical or Mixed | ML System Design or more Stats |

> ⚠️ **Order may vary** — confirmed by multiple candidates. Some had product sense before stats. All are 45 min each.

### Google's 4 Scoring Dimensions (for Hiring Committee):

- **GCA** — General Cognitive Ability (structured thinking, problem decomposition)
- **RRK** — Role-Related Knowledge (tech depth: stats, ML, SQL, Python)
- **Leadership** — Emergent leadership, influence without authority
- **Googleyness** — Cultural fit, humility, bias-to-action, comfort with ambiguity

**Scores:** 1 (Strong No Hire), 2 (Lean No Hire), 3 (Lean Hire), 4 (Strong Hire)  
A single "1" is typically disqualifying. Aim for all 3s/4s.

---

## 🔧 Round Type 1: Coding (SQL / Python)

### SQL — What to expect

Medium-to-hard complexity. Emphasis on **window functions, CTEs, ranking, aggregation**.

**Verbatim questions from candidates (onsites.fyi / InterviewQuery / Reddit):**

- "Find the top 3 highest-paid employees per department. If fewer than 3, return all. Sort by department (asc), salary (desc)."
  - Use: `DENSE_RANK()` or `RANK()` partitioned by dept, ordered by salary DESC
- "Find customers who placed orders in both 2023 and 2024."
  - Use: Conditional grouping / self-join / INTERSECT
- "Write a query to calculate 7-day rolling retention."
- "Measure CTR over time, year-over-year growth, and identify the day with highest CTR from a table with (Date, Impressions, Clicks)."
- "Find the marketing channel responsible for a user's first conversion (from user_sessions + user_channels tables)."
- "Calculate the median in SQL."
- "Find top 5 highest-selling items from order history."
- "How would you find users who frequently search for 'ML' but rarely click sponsored ads?"

**Key SQL skills to drill:**

- `DENSE_RANK() / ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)`
- CTEs with `WITH` statements
- Self-joins, lateral joins
- `HAVING` with aggregates
- Handling NULLs, deduplication

### Python / Pandas — What to expect

Not LeetCode-heavy. Focus on **data manipulation + statistical computation**.

**Verbatim questions:**

- "Write a function that draws N samples from N(0,1) and plots the histogram."
- "Write a function that returns a given percentile. Input format: `a1,b1,c1_a2,b2,c2_...` (tricky string parsing!)"
- "Given a list of numbers, calculate the sum of odd-indexed elements in a sequence of 100."
- "Filter rows where favorite_color ∈ {green, red} AND grade > 90."
- "Find the mean and median from a numerical dataset with unusual string formatting (extract numbers from strings)."
- "Write code for binary search / reverse a linked list" (less common, more SWE-adjacent)
- "Implement a function to detect anomalies in time series data."

**Key pandas skills:**

- `groupby`, `agg`, `transform`
- `pivot_table` vs `pivot`
- Handling missing data (dropna, fillna, interpolate)
- Merging / joining DataFrames
- String operations on columns
- `apply()` with custom functions
- `pd.cut`, `pd.qcut` (for percentiles/bins)

**Recommended practice:** LeetCode "30 Days of Pandas", StrataScratch (Google filter), InterviewQuery

---

## 📊 Round Type 2: Statistics, ML & Experimentation

This is the **most important round for this specific role** — Identity Personalization is heavily experimentation-driven.

### A/B Testing & Experimentation (HIGH PRIORITY)

**Core concepts to master:**

- Sample size calculation: `n = (Z_α/2 + Z_β)² · 2σ² / δ²`
- Type I error (α, false positive), Type II error (β, false negative), Power (1-β)
- MDE (Minimum Detectable Effect)
- Two-tailed vs one-tailed tests
- Multiple testing problem (Bonferroni correction, BH procedure)
- Randomization unit (user, session, device, cookie)

**Role-specific topic: USER LEARNING EFFECTS** (literally in the job description)

- **Definition:** Users' behavior changes over time as they learn to use a new feature — short-term test results may NOT predict long-term impact
- **Google's approach:** Long-duration experiments with lagged-start control groups; cookie-cookie day randomization; models using short-term satisfaction as proxies for long-term value
- **Interview question pattern:** "You ran an A/B test for 2 weeks with positive lift. PM is worried about user learning. How do you validate long-term impact?"
  - **Answer:** Lagged holdout groups, cohort analysis over time, use satisfaction metrics as proxies, model short→long-term mapping

**Novelty Effect vs Primacy Effect:**

- **Novelty:** Initial spike in engagement due to curiosity (fades). More common with new users
- **Primacy / Change Aversion:** Initial DROP due to resistance to change. More common with long-term users
- How to detect: Segment by new vs existing users; monitor trend over 3-6 weeks
- Classic interview scenario: "Feature launched well in A/B test but engagement dropped back after full rollout" → Novelty effect

**Verbatim statistical questions:**

- "Your A/B test shows lift but p=0.08. What do you do?" (Can you launch? What factors matter?)
- "Measuring time spent in Google Search per day per user. The average is going down. Initial analysis?"
- "Average searches/user goes down but each country's average goes up. Explain this." → **Simpson's Paradox**
- "How would you design an experiment to test the effectiveness of two drugs with two groups?"
- "How would you study YouTube hours watched vs age, accounting for confounds like ZIP code?"
- "What's the probability of a Type I error? What happens if you filter out all values below the mean?"
- "What's the probability of observing 1000 given μ=0, σ=1?" (essentially P(X=1000) for continuous → 0)
- "For sample size n, margin of error = 3. How many more samples to get margin of error = 0.3?" → 100x more (MOE ∝ 1/√n, so need 100n total, 99n more)
- "In what situation would you prefer mean over median?"
- "What is the degree of freedom for LASSO?"

**Probability brainteasers (verbatim, from Kaggle/onsites.fyi):**

- "You're at a Casino. You win $10 every time you roll a 5. If you play until you win and stop, what's the expected payout?" → Expected payout = $10; E[rolls] = 6 (geometric dist, p=1/6)
- "You call 3 friends about rain in London. Each friend tells truth with prob 2/3. All 3 say it's raining. P(actually raining)?" → Bayes: P(rain|all say rain)
- "40 cards: 10 each of 4 colors, numbered 1-10. Two random cards. P(not same number AND not same color)?"
- "Box A: 100R+100B. Box B: 50R+50B. Drawing 2 cards. Which box has higher P(same color)?" → Box B (slightly, hypergeometric)
- "Box with 20 pink + 20 white vs box with 40 pink + 40 white. Pick 2 at random. Which has higher P(both same color)?" → Same box, smaller box is slightly higher

### Statistics Traps to Know (Google Loves These)

- **Simpson's Paradox:** Aggregate trend reverses when groups are separated. Classic avg-searches example above
- **Berkson's Paradox (Collider Bias):** Selection on a collider creates artificial correlation between otherwise independent variables
- **Survivorship Bias:** Only analyzing winners — e.g., successful products without considering failed ones
- **Novelty/Primacy Effects** (see above)

### ML Concepts

- "Explain bias-variance tradeoff"
- "When would you use L1 (LASSO) vs L2 (Ridge) regularization?"
- "How do you handle class imbalance?" (SMOTE, reweighting, threshold tuning, etc.)
- "Explain logistic regression coefficients interpretation + confidence intervals"
- "How would you prevent overfitting?"
- "What is cross-validation and why is it important?"
- "Difference between bagged (Random Forest) vs boosted (XGBoost) models"
- "What methods would you use for anomaly detection?"
- "Steps to apply Gaussian Mixture Model — how to test applicability?"
- "How would you simulate a bivariate normal?"
- "What are dimensionality reduction techniques?"
- "Explain transfer learning advantages"

---

## 🤖 Role-Specific: LLM Evaluation (This Role's Secret Sauce)

The job description explicitly mentions **LLM eval techniques** and **human evaluation data (surveys and raters)**. This is rare in DS JDs. Expect questions.

### LLM Evaluation Metrics to Know

| Metric             | What it measures                         | Best for                 |
| ------------------ | ---------------------------------------- | ------------------------ |
| BLEU               | Precision of n-gram overlap              | Machine translation      |
| ROUGE              | Recall-based n-gram overlap              | Summarization            |
| METEOR             | Precision + recall + synonyms            | Nuanced matching         |
| BERTScore          | Semantic similarity via BERT embeddings  | Deep semantic comparison |
| Perplexity         | How well model predicts sample           | Language model quality   |
| LLM-as-a-Judge     | Uses GPT-4/Gemini to score outputs       | Nuanced quality          |
| Faithfulness       | Are facts grounded in retrieved context? | RAG systems              |
| Answer Relevancy   | Does answer address the question?        | QA systems               |
| Hallucination rate | Fabricated information                   | Safety/reliability       |

> **Why combine multiple metrics?** No single metric covers all LLM output dimensions (accuracy, tone, coherence, safety).

### RLHF (Reinforcement Learning from Human Feedback)

Know the 3 stages:

1. **SFT (Supervised Fine-Tuning):** Fine-tune base model on high-quality human demos
2. **Reward Model Training:** Human raters compare & rank model outputs → train a reward model
3. **RL Optimization (PPO):** Use reward model to further fine-tune LLM via RL

**Challenges with human raters:**

- Bias amplification from subjective judgments
- Low inter-rater agreement on subjective tasks
- Slow, expensive, not scalable
- Expert domain knowledge lacking in general rater pools

**Potential interview questions:**

- "How would you design a human evaluation framework for an LLM used in Google Identity/personalization?"
- "How would you measure the quality of a fine-tuning dataset for an LLM?"
- "What metrics would you use to evaluate an LLM's personalization of user responses?"
- "How do you handle noisy labels from human raters?"
- "What are the limitations of using BLEU for evaluating conversational AI?"

---

## 📦 Round Type 3: Product Sense / Case Study ("Non-Tech")

### Metric Design Framework (MEMORIZE THIS)

1. **Clarify** the product/feature/goal (5 mins!)
2. **User journey:** who uses it, how, why
3. **North Star metric** (core value being delivered)
4. **Supporting metrics:** AARRR → Acquisition, Activation, Engagement, Retention, Revenue
5. **Guardrail metrics** (what must NOT go down)
6. **Trade-offs** between metrics
7. **Experimentation plan** (A/B test setup)

### Root Cause Analysis Framework

When a metric drops:

1. Is it real or a tracking issue?
2. When did it start? Correlate with launches
3. Which segment? (Geography, platform, user type, device)
4. Which funnel stage? (Acquisition, activation, engagement, retention)
5. External factors? (Seasonality, competitor, news)
6. Propose fix + experiment to validate

### Verbatim Product Sense Questions (onsites.fyi / Reddit)

- "Gmail adoption has slipped 5% over 6 months. What would you do?"
- "Average searches per day per user going down. Walk me through your analysis."
- "How would you detect inappropriate content on YouTube?"
- "How would you measure success of YouTube Shorts?"
- "If you were PM for Google Maps, what would your success metrics be?"
- "How would you measure time spent in Google Search per day per user?"
- "You're creating a report on content uploads and see a spike in January image uploads. What caused it?"
- "How would you test a new Search feature to determine if the change is positive?"
- "What kind of product do you want to build at Google?" (especially relevant for Identity/Personalization!)
- "Cars implanted with speed trackers → insurance companies. What business questions can be answered?"
- "Two Surge Pricing Algorithms for an airline — how do you decide which is better?"
- "How do you measure the success of [promotion: 10% off]? Was it successful?"

### Identity/Personalization Specific System Design

Likely scenario: **"Design a personalization system for Google Account identity features"**

Framework:

1. Clarify: What do we personalize? (Account recommendations, sign-in experience, security suggestions, profile completion)
2. Objectives: Reduce friction, increase security compliance, improve user satisfaction
3. Features: User history, device, location, account age, activity patterns, demographic signals
4. Model: Two-tower retrieval + ranking; real-time + batch scoring
5. Evaluation: CTR, task completion rate, user satisfaction (CSAT), security incident rate
6. A/B testing: Holdout groups, novelty effect monitoring, long-term cohort tracking
7. Data quality: Missing features, cold start for new users, privacy/anonymization

---

## 🧠 Round Type 4: Behavioral / Googleyness ("Non-Tech")

### What "Googleyness" Actually Means

- **Humble:** Admits mistakes, gives credit, asks for help
- **Bias to action:** Doesn't wait for perfect info
- **Comfortable with ambiguity:** Can define the problem, not just solve it
- **Courageous:** Disagrees respectfully, speaks up
- **Conscientious:** Thinks about user impact
- **Enjoys fun:** Not too serious

### Most Common Questions (verbatim from Reddit/Glassdoor)

- "Tell me about yourself" (keep to 90 seconds: background → key achievement → why Google)
- "Why Google specifically?" (NOT "it's a great company")
- "Tell me about a time you had to influence without authority"
- "Describe a project that failed. What did you learn?"
- "Tell me about a time you disagreed with your manager. What happened?"
- "How do you handle ambiguous requirements?"
- "Tell me about your most impactful project" (quantify impact!)
- "Tell me about a time you had to deliver complex findings to non-technical stakeholders"
- "How do you prioritize when you have multiple competing deadlines?"
- "Tell me about a time when you failed to meet a deadline"
- "How do you push back when you disagree with a manager?"
- "Describe a situation where colleagues weren't convinced by your approach. How did you change their minds?"
- "How do you sort priorities when multitasking?"
- "What are the top competencies you're bringing to Google?"
- "How do you keep up with new technology?"
- "Do you prefer small or large teams?"
- "Where do you see your career in 10 years?"
- "Why Google over [competitor]?"

### STAR Method Template

- **S**ituation: Brief context (1-2 sentences)
- **T**ask: Your specific responsibility
- **A**ction: What YOU did (not "we") — be specific and technical where relevant
- **R**esult: Quantified impact ("increased retention by 12%", "saved $2.3M")

> Prepare 8-10 specific stories adaptable to different question types.

---

## 🏗️ Round Type 5: ML System Design (Advanced)

### Likely Questions for Identity Personalization DS

- "Design an identity verification system that uses ML"
- "Design a personalized sign-in experience (e.g., suggest passkeys, 2FA methods) based on user behavior"
- "Design a recommendation system for Google account security features"
- "Design a fraud detection system for Google accounts"
- "Design an LLM evaluation pipeline with human raters at scale"

### General System Design Framework for DS

1. **Clarify requirements** (business + technical constraints)
2. **Define success metrics** (online + offline)
3. **Data**: sources, features, quality, privacy
4. **Modeling**: training approach, architecture choice
5. **Serving**: latency requirements, batch vs real-time
6. **Evaluation**: A/B testing plan, shadow mode
7. **Monitoring**: drift detection, retraining triggers
8. **Scale considerations**: billions of users at Google

### Personalization System Design Key Concepts

- **Two-tower model**: Separate user and item encoders → dot product for retrieval
- **Feature store**: Consistent features between training and serving
- **Cold start problem**: New users with no history → use demographic/device signals
- **Exploration vs exploitation**: ε-greedy, UCB, Thompson sampling
- **Long-term vs short-term objectives**: Immediate satisfaction vs retention

---

## 💡 Role-Specific Intelligence

### What the Identity Personalization Team Actually Does

- **Statistical modeling of user journeys** across Google (Search, Gmail, YouTube, Account, etc.)
- **LLM fine-tuning datasets**: Creating and evaluating data for personalized LLM responses
- **A/B experimentation with user learning effects** (literally in the JD — prepare this deeply!)
- **Data quality frameworks + automated dashboards** at scale
- **Cross-functional collaboration**: Engineering, Product, UX, Research
- **Human evaluation** pipelines: Designing rater guidelines, inter-rater reliability, label quality

### Buzzwords from the JD → Map to Interview Topics

| JD phrase                                          | Interview topic                                      |
| -------------------------------------------------- | ---------------------------------------------------- |
| "user-journey analysis"                            | Product sense, funnel analysis, cohort analysis      |
| "quantify impact on KPIs"                          | Metric design, A/B testing, causal inference         |
| "validation methodologies for LLMs"                | LLM eval (BLEU, BERTScore, human eval)               |
| "evaluation metrics for LLMs"                      | All LLM metrics, RLHF                                |
| "fine-tuning datasets"                             | Data quality, annotation, label noise                |
| "data quality frameworks"                          | Data pipeline, monitoring, missing data              |
| "advanced experimentation (user learning effects)" | **KEY: novelty/primacy effects, long-term holdouts** |
| "cross-functional stakeholders"                    | Behavioral: influence without authority              |
| "unstructured business problems"                   | Product sense, case studies                          |

---

## 📚 Preparation Resources (Prioritized)

### Highest Priority

- 📖 **"Trustworthy Online Controlled Experiments"** (Kohavi et al.) — Google interviewers explicitly reference this
- 🎥 **Emma Ding YouTube channel** — Product sense + DS interview prep, Google-specific
- 🧑‍💻 **InterviewQuery.com** — Filter by Google, DS role
- 🧑‍💻 **StrataScratch** — Google DS SQL questions (filter by company)

### Practice Platforms

- **LeetCode**: "30 Days of Pandas" + Google-tagged SQL questions
- **onsites.fyi**: Real interview reports from Google DS candidates
- **Glassdoor**: Google Data Scientist interview reviews (filter by 2023-2025)
- **Kaggle**: "100 Pandas Quiz" on GitHub referenced by Reddit users

### Statistics Deep Dives

- Statistical paradoxes: Simpson's, Berkson's, Survivorship
- Causal inference: DiD, Instrumental Variables, Matching
- A/B testing gotchas: Network effects, SUTVA violations, novelty/primacy
- Power analysis and sample size calculation

---

## 🛠️ 2025-Specific Notes

- **Google is moving toward in-person onsites** for local candidates (including Tel Aviv) to combat AI-assisted remote interviews
- **2025 emphasis**: Even more emphasis on experimentation and causal reasoning post-AI era
- **Strong fundamentals > AI-generated answers** — interviewers can tell. Structure and communication matter enormously
- **Clarifying questions are expected and valued** — don't jump to answer; spend 5 min clarifying
- **Not finishing problem is okay** if you show good reasoning and progress

---

## ✅ Quick Pre-Interview Checklist

- [ ] 8-10 STAR stories prepared and rehearsed
- [ ] SQL: Window functions, CTEs, ranking drilled
- [ ] Python: Pandas operations, statistical functions coded
- [ ] A/B testing: full lifecycle including novelty effects, user learning, sample size calc
- [ ] LLM eval: BLEU, ROUGE, BERTScore, RLHF pipeline
- [ ] Product sense: metric design framework memorized
- [ ] Statistical paradoxes: Simpson's, Berkson's, survivorship bias
- [ ] Causal inference: DiD, IV, matching, observational studies
- [ ] ML: regularization, bias-variance, class imbalance, cross-validation
- [ ] System design: personalization/recommendation framework
- [ ] Why Google (Identity/Personalization specifically) — prepared answer
- [ ] Questions to ask interviewers ready for each round type
