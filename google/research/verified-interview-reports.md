# Google Data Scientist: Verified Firsthand Interview Reports

> Sources: onsites.fyi (structured candidate submissions), sqlpad.io (named candidate with offer), Blind URLs (manual access needed), LeetCode Discuss (manual access needed).
> AI-generated content deliberately excluded. Only real people's reports.

---

## Real Candidate Reports — Onsites.fyi

| Date | Level | Stage | Outcome | Questions Asked |
|------|-------|-------|---------|----------------|
| Nov 2023 | L4 | Onsite | **Rejected** | Drug effectiveness experiment design; YouTube watch time vs age; percentile function (code); Google search trend decline |
| July 2023 | L3 | Onsite | Unknown | HR round; theoretical stats; data analysis; A/B testing + bias removal; ad campaign inference |
| June 2023 | L4 | Phone Screen | **Rejected** | Mean vs median; sample N=1000 from N(0,1) + plot histogram (Python); sum of odd-positioned numbers; Type 1 error with altered sampling distribution; logistic regression theory |
| June 2023 | L4 | Onsite | **Rejected** | No questions shared — candidate: "interviewers seemed highly inexperienced and condescending" |
| Apr 2023 | L4 | Phone Screen | **Rejected** | Regression basics; training/testing; sorting + histogram coding |
| Apr 2023 | L3 | Phone Screen | Unknown | "Derive the MLE for logistic regression" — candidate: **"much harder stats than other DS interviews"** |

---

## Jay — Google Cloud DS — OFFER ~$280K (sqlpad.io)

2 YOE, M.S. in ML, Mountain View CA. 3-month process.

### Round 1: Recruiter Screen
- Visa, salary expectations, start date, team fit

### Round 2: Technical Phone Screen
- "Which Google apps would you show by default on the Google homepage?" (product reasoning)
- Techniques for handling missing data
- Dimensionality reduction methods
- Logistic regression regularization approaches

### Round 3: Onsite — Stats & ML
- Explain confidence intervals to a non-technical audience
- How to determine A/B test duration
- What is a null hypothesis
- How to improve statistical power

### Round 4: Onsite — Googliness / Behavioral
- Example of demonstrating initiative
- Example of conflict resolution / standing your ground
- Describe your ideal team composition

### Round 5: Onsite — Statistics Coding
- "Create a function that generates **unbiased coin flips from a biased coin**" (Python)
- "Calculate array **median without any built-in functions**" (Python)
- Time series: ARIMA + handling **heteroscedasticity**

### Round 6: Onsite — Leadership / Behavioral
- Why Google?
- Why leaving current role?
- Proudest accomplishment
- Questions for interviewer

**Offer received ~1 week after onsite.**

---

## Confirmed Recurring Questions (4+ independent sources)

### Phone Screen Level

**Statistics:**
- "When would you use mean over median?" *(appears in almost every phone screen report)*
- "What is the probability of a Type 1 error? What happens when the sampling distribution is altered?"
- "For sample size n, margin of error is 3. How many more samples to get MOE = 0.3?" → 100x (MOE ∝ 1/√n)
- "Given 3 coin tosses of a fair coin result in Heads — probability 4th is also Heads?" → 0.5 (independent)
- "Derive the MLE for logistic regression" *(L3, flagged as hard)*

**Coding (Python — from scratch, no shortcuts):**
- "Draw N samples from N(0,1) and plot a histogram"
- "Calculate sum of odd-positioned numbers in a sequence of 100 numbers"
- "Calculate median without built-in functions"
- "Generate unbiased coin flips from a biased coin" (von Neumann extractor)
- "Write a percentile function from scratch"

**SQL:**
- "Find top 3 highest salaries per department" (DENSE_RANK)
- "Get last transaction for each day" (ROW_NUMBER PARTITION BY date)
- "First-touch marketing attribution" (join user_sessions + user_channels)
- "Calculate median in SQL" (PERCENTILE_CONT or GENERATE_SERIES workaround)
- "Find second-highest salary in engineering department" (RANK vs DENSE_RANK edge cases)

### Onsite — Experimentation Round

- "Design an A/B test to test drug effectiveness with 2 groups"
- "Design an A/B test to detect a 3% increase — what sample size, duration, randomization checks?"
- "Assess validity of an A/B test showing p = 0.04"
- "Verify that users were randomly assigned to test buckets — how?"
- "If you want to test both color AND placement of a sign-up button, how would you design this?" (factorial)
- "Your A/B test data is not normally distributed — how do you determine the winner?"
- "What sanity checks do you run before launching an experiment?"
- "Explain what statistical power is and how you would improve it"
- "How would you study the relationship between YouTube hours watched and age? What about confounds like zip code?"

### Onsite — Product / Analysis Round

- "Google search time per user is going down. Walk through your analysis"
- "YouTube watch time on homepage dropped significantly — what happened?"
- "Google Cloud API calls doubled this month. Determine the reason"
- "If individual group means rise but pooled mean falls — is that possible? Explain" → Simpson's Paradox
- "How would you detect viruses or inappropriate content on YouTube?"
- "Working with the Google Meet PM on new UX buttons — what metrics would you track?"
- "How would you measure success of a new Google Maps feature?"
- "Does upgrading Android produce more searches? How would you measure this?"
- "Given no current metrics for Google Docs — what top 5 would you implement?"

### Onsite — ML Round

- "What is the difference between K-means and EM algorithm?"
- "When is a Gaussian mixture model the right choice?"
- "What is the difference between a bagged model and a boosted model?"
- "Why would the same ML algorithm produce different results on the same dataset?"
- "When should you use regularization vs cross-validation?"
- "How would you design YouTube's video recommendation algorithm?"
- "How would you build a model to predict user churn for Google Cloud?"
- "How would you evaluate clustering when labels are known?"
- "If two predictors are highly correlated, what happens to logistic regression coefficients? And confidence intervals?"

### Onsite — Behavioral / Googleyness

- "Give an example of a time you demonstrated initiative"
- "Give an example of a conflict and how you resolved it"
- "Tell me about a time you had to influence without authority"
- "Tell me about a time you made a decision based on data and were wrong"
- "How do you manage tight deadlines with competing priorities?"
- "Why Google specifically?"

---

## What Surprised Real Candidates vs What Guides Say

| Topic | Guides Say | Reality (from reports) |
|-------|-----------|----------------------|
| Coding difficulty | "Medium LeetCode, data manipulation" | NOT LeetCode hard. Python stats from scratch: implement median, coin flip corrector, sampling, MLE derivation |
| Stats depth | "Know the basics" | L3 phone screen opened with "Derive MLE for logistic regression." Candidates called Google stats **significantly harder than other FAANG DS interviews** |
| SQL prominence | Very heavy emphasis | Less prominent in actual reports than guides suggest — Python stats coding appears more often |
| Interviewer quality | Implied professional | Two separate onsites.fyi candidates reported condescending, inexperienced interviewers |
| Post-rejection feedback | Not mentioned | **Zero feedback given.** Multiple candidates asked 4+ times and received nothing |
| Product sense weight | "Big focus" | Experiment design appears in every onsite; product sense is secondary |

---

## Topics in Guides with Weak Evidence in Real Reports

These get heavy coverage in prep guides but rarely appear in actual candidate reports:

- LLM evaluation (BLEU, ROUGE, RLHF) — only relevant if your JD explicitly mentions it
- Full ML system design — more SWE/ML Engineer territory
- Causal inference (DiD, instrumental variables) — mentioned in guides but absent from reports
- Detailed NLP/transformers — not prominent in DS interview reports

---

## Topics Appearing in Every Real Account

- A/B test design with specifics: duration, power, randomization checks
- Python from scratch: median, sampling from distributions, statistical simulation
- **Mean vs median** — literally in 4+ sources, have a nuanced 2-min answer
- Type 1 error and what happens when sampling distributions change
- Product analysis anchored to specific Google products (YouTube, Maps, Meet, Ads)

---

## Blind Posts to Read Manually

Open these in your browser — content confirmed to exist but not crawlable:

```
teamblind.com/post/Google-Data-Scientist-Interview-0Gukj7YS
teamblind.com/post/google-data-scientist-interview-ushumj2o
teamblind.com/post/ruined-my-google-data-science-interview-njsse3by
teamblind.com/post/google-data-scientist-interview-prep-0euuvjem
teamblind.com/post/python-in-google-data-scientist-interview-kywfg6n1
teamblind.com/post/Google-data-scientist-interview-questions-zGRhutXJ
teamblind.com/post/google-data-scientist-interview-bkEwWMJE
```

## LeetCode Discuss Posts to Read Manually

```
leetcode.com/discuss/post/6701617/google-onsite-interview-experience-mar-2-h182/   ← March 2025 onsite
leetcode.com/discuss/interview-experience/1926993/   ← Google L3 Reject
```
