# Google Data Scientist Interview: Deep Research Report (2024-2025)

Source: google/research/google-ds-interview-deep-research.md

# Google Data Scientist Interview: Deep Research Report (2024-2025)

> Compiled from: IGotAnOffer, InterviewQuery, Prepfully, StrataScratch, DataLemur, BigTechInterviews, InterviewKickstart, Exponent, NickSingh.com, Emma Ding / DataInterviewPro, Glassdoor (aggregated), Blind (aggregated), edureka, projectpro, finalroundai, AceTheDataScienceInterview
>
> Last updated: March 2026

---

## 1. Interview Process Structure

### Overview
- ~3 million applicants per year; fewer than 1% receive offers
- Total timeline: **3–6 weeks** from application to offer (median ~35 days)
- Google uses a hiring committee model: your packet is reviewed by senior Googlers who did NOT interview you, ensuring consistency

### Stages

#### Stage 1: Resume + Recruiter Screen (25–30 min)
- Recruiter screens for keywords: SQL, A/B testing, experimentation, machine learning, data visualization, Python
- Introductory call covering your background, past projects, motivation
- Some roles include a short technical pre-screen questionnaire
- Tip: Prepare 1–2 project stories with measurable outcomes (metric improved, decision influenced)

#### Stage 2: Technical Phone Screen (45–60 min)
- Via Google Meet with a shared code editor (Google Doc or similar)
- Typically **1 medium-difficulty SQL question + 1 medium-difficulty Python question**
- Focus is on reasoning and communication, not speed
- May include high-level statistical discussion or interpretation questions
- Tip: Talk through assumptions, ask clarifying questions before coding

#### Stage 3: Virtual/Onsite Loop (4–5 interviews, ~45 min each, single day)
This is the core evaluation. You meet a mix of data scientists, engineers, and product partners.

| Round | Focus |
|-------|-------|
| Coding | SQL and/or Python: joins, aggregations, window functions, simulations |
| Statistics & Experimentation | Hypothesis testing, A/B test design, causal reasoning |
| Machine Learning / Applied Modeling | Model lifecycle, feature selection, evaluation metrics, trade-offs |
| Product / Business Sense | Metrics definition, diagnosing drops, success measurement |
| Behavioral ("Googleyness") | Collaboration, ambiguity, conflict resolution, leadership |

Note (2024–2025): Google has required in-person setups for some local candidates to reduce AI-assisted response risk.

#### Stage 4: Hiring Committee + Team Match + Offer
- Independent senior reviewers (who were NOT your interviewers) evaluate your packet
- Team matching follows: informal conversations with potential managers
- Formal offer: base + bonus + RSUs. Negotiation is expected and data-driven (use Levels.fyi benchmarks)

### Evaluation Criteria (4 Core Attributes)
1. **General Cognitive Ability (GCA)** — problem-solving under ambiguity
2. **Role-Related Knowledge (RRK)** — technical depth
3. **Leadership** — stepping up at different project stages ("emergent leadership")
4. **Googleyness** — collaboration, curiosity, bias toward action, alignment with mission

---

## 2. Topics Tested — Detailed Breakdown

### Question Category Distribution (based on 32 collected questions, StrataScratch)
- Coding/Algorithms: ~53% combined
- Behavioral: ~22%
- Technical (stats/ML): ~16%
- Modeling/Business Case: ~9%

### A. SQL
Heavy emphasis. Topics include:
- Window functions: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LAG()`, `LEAD()`
- Complex joins (INNER, LEFT, RIGHT, CROSS — including understanding output row counts)
- Aggregations, GROUP BY, HAVING
- Subqueries and CTEs
- Time-series queries (e.g., last transaction per day)
- Attribution logic (first-touch marketing channel)
- Ranking within groups (top-N per department/category)
- Handling NULLs, deduplication
- Query optimization for large datasets

### B. Python / Coding
- Pandas/NumPy data manipulation
- Implementing statistical functions from scratch (median, mean, percentiles)
- Drawing N samples from a distribution and plotting histogram
- Generating iid draws from distribution X using only a random number generator
- Hash tables, binary trees (invert binary tree)
- String processing (unique word counts from text)
- Simulating probability scenarios (biased coin, dice problems)

### C. Statistics & Probability
Core topics:
- p-values, Type I / Type II errors, statistical power
- Confidence intervals (construction and interpretation)
- Hypothesis testing (z-test, t-test, chi-squared, non-parametric alternatives)
- A/B testing: design, randomization checks, sample size, duration, peeking
- Bayes' theorem and conditional probability
- MLE vs. MAP
- Central Limit Theorem
- Distributions: normal, binomial, Poisson, exponential, uniform
- Expected value calculations
- Margin of error / sample size relationships
- When to use mean vs. median
- Simpson's Paradox ("If individual means rise for two groups, can pooled mean decrease?")

### D. Experimentation / Causal Inference
This is a PRIMARY focus area at Google:
- Full A/B test design: hypothesis, randomization unit, metric selection, sample size, duration, guard rails
- Randomization sanity checks (how to verify bucket assignment)
- Multiple testing / p-hacking awareness
- Non-normal data: bootstrap, Mann-Whitney, permutation tests
- Factorial / multivariate experiment design
- Causal inference beyond A/B: difference-in-difference, instrumental variables
- Interpreting inconclusive or surprising results
- Pre-experiment sanity checks (metric stability, SRM - sample ratio mismatch)
- Network effects and interference between experiment units

### E. Machine Learning
Conceptual depth expected (not deep math derivations for product DS roles):
- Supervised vs. unsupervised learning
- Bias-variance trade-off
- Regularization (L1/Lasso, L2/Ridge) vs. cross-validation — when to use each
- Feature selection, feature engineering, encoding high-cardinality categoricals
- Handling class imbalance
- Model evaluation: accuracy, precision, recall, F1, AUC-ROC, RMSE, MAE
- Overfitting prevention: regularization, dropout, early stopping
- k-means convergence proof (intuitive), k-means vs. EM/GMM
- Recommendation systems (YouTube, type-ahead search)
- Anomaly detection
- Model monitoring and lifecycle in production
- Gradient boosting, bagging vs. boosting
- Why same algorithm can produce different results on same dataset (randomness, seeds, data shuffling)

### F. Product Sense / Business Cases
- Defining success metrics for a new feature
- Diagnosing metric drops (e.g., "search volume dropped 10%, why?")
- Designing top 5 metrics for Google Docs from scratch
- Measuring time spent in Google Search per user daily
- Explaining if average searches decline but country average rises (Simpson's Paradox)
- Investigating sudden upload spikes (YouTube)
- Improving Google Maps user experience
- Detecting virus / inappropriate content on YouTube
- Should Google charge for productivity apps?
- Fermi/estimation: "How many cans of blue paint were sold in the US last year?"
- "How would you increase Gmail's user base?"

---

## 3. Specific Questions by Category (Concrete Examples)

### SQL Questions (confirmed asked)
1. Find the top 5 highest-selling items from order history
2. Calculate median for a given column using COUNT and RANK
3. Find second-highest salary in the engineering department (use DENSE_RANK / ROW_NUMBER)
4. Find top 3 salaries per department
5. Get last transaction per day from a bank transactions table
6. Determine which marketing channel brought a customer to the site for the first time (attribution)
7. Calculate join output row sizes for INNER, LEFT, RIGHT, CROSS joins
8. Find email activity rank for each user by total emails sent (descending)
9. Combine two datasets to create complete addresses for each record (JOIN on city ID)
10. Median Google Search frequency (PERCENTILE_CONT + GENERATE_SERIES)
11. Sum odd vs. even measurements per day using ROW_NUMBER + modulo
12. Most popular Google search category by month (2024 data, window functions)
13. Find users who haven't logged in during the last 30 days
14. Identify the day of the week with highest transaction volume
15. Google Ad click-through and conversion rates (join clicks and cart conversions)
16. Average cost-per-click per campaign and ad group

### Statistics / Probability Questions (confirmed asked or highly reported)
1. Given 3 coin tosses result in Heads, what is the probability the 4th is also Heads?
2. For sample size n with margin of error 3, how many samples needed for margin of error 0.3?
3. Explain assumptions of error in linear regression
4. How would you design an A/B test for a new YouTube feature?
5. If individual means rise for two groups, can pooled mean decrease? (Simpson's Paradox)
6. What's the probability each person exits a different floor in a 4-person, 4-floor scenario?
7. When do you use mean vs. median?
8. What is a p-value? What happens when the sampling distribution is altered?
9. Explain 'parametric' vs 'non-parametric' statistics
10. Two boxes: 20 pink/20 white vs. 40 pink/40 white — which gives higher probability when picking two balls?
11. Casino dice game — calculate expected payout
12. Bayesian: "If all 3 friends say it's raining in London, what's the probability it's actually raining?"
13. Simulate a biased coin toss in code
14. How would you derive a confidence interval from a series of coin tosses? **(confirmed Google question)**
15. A coin was flipped 1000 times, 550 heads — is it biased? **(confirmed Google question)**
16. X ~ Uniform(0,1), Y ~ Uniform(0,1) — what is E[min(X,Y)]? **(confirmed Google question)**
17. Two subsets with known means and standard deviations — calculate blended mean and SD for total dataset; extend to K subsets **(confirmed Google question, Hard)**
18. What is the probability that a seven-game series goes to 7 games? **(confirmed Google question)**
19. What's the probability of a Type 1 error? What happens to it when the sampling distribution is altered?
20. In a population with mean μ and variance σ², first sample shows X — would you reject the null? What's the probability another sample also rejects?

### A/B Testing / Experimentation Questions (confirmed asked)
1. How would you assess the validity of an A/B test result showing p-value = 0.04?
2. In an A/B test, how would you verify that users were assigned to test buckets randomly?
3. If you wanted to test both the color AND placement of a sign-up button, how would you design the experiment? (factorial design)
4. If your A/B test data is not normally distributed, how would you determine which variant performed better?
5. What sanity checks would you perform before launching an experiment?
6. Would a 5% click increase in one group constitute a good experiment result?
7. How do you test if a metric increased after an app change?
8. Study relationship between YouTube hours watched vs. age; address confounds like zip code

### Machine Learning Questions (confirmed asked)
1. Why use feature selection? If two predictors correlate highly, what affects logistic regression coefficients?
2. Describe Lasso vs. Ridge regression and their optimization
3. What distinguishes K-means from EM / Gaussian Mixture Models?
4. How would you design the YouTube video recommendation algorithm?
5. Design a type-ahead search recommendation algorithm
6. How would you evaluate a clustering model if labels are known?
7. How to assess if a Gaussian mixture model is appropriate for a given dataset?
8. When should you use regularization vs. cross-validation?
9. Why would the same ML algorithm generate different success rates on the same dataset?
10. How would you prove K-means converges in a finite number of steps?
11. How would you encode a categorical variable with thousands of distinct values?
12. What is AUC and what are the key evaluation metrics in ML?
13. How would you build a model to predict user engagement with Google services?
14. How would you handle imbalanced datasets in classification?
15. Derive equations for GMM (research-track roles)

### Product Sense / Business Case Questions (confirmed asked)
1. Design top 5 metrics for Google Docs (no current tracking exists)
2. Measure time spent in Google Search per user daily — explain if average searches decline but country average rises
3. You are working with the PM of Google Meet who wants new UX buttons — what advice do you give?
4. Investigate user retention patterns for a Google product
5. Detect viruses or inappropriate content on YouTube — how would you build a system?
6. Your system detects a huge uptick in new accounts in a particular region — how do you approach this?
7. Google Cloud API calls have doubled over the past month — determine the reason
8. How would you increase Gmail's user base?
9. How would you investigate opportunities to improve Google Maps user experience?
10. Fermi: How many cans of blue paint were sold in the US last year?

### Behavioral Questions (confirmed format)
1. Describe a data project you worked on and the challenges you faced
2. What are effective ways to make data accessible to non-technical people?
3. What would your current manager say about you? Strengths and weaknesses?
4. Talk about a time you had trouble communicating with stakeholders
5. Why do you want to work at Google?
6. Tell me about a time you influenced a product or business decision using data
7. Describe a time you made a decision with incomplete data
8. Tell me about a time you put someone else's interests above your own
9. Describe a time you brought disagreeing teams together
10. Share an experience when you made a data-driven decision that was wrong

---

## 4. Firsthand Reports & Candidate Experiences

### From Glassdoor/Blind aggregation (2024-2025)
- **One candidate (June 2025, Menlo Park)**: "7 rounds of interviews after phone screening, heavily based in machine learning and how quickly you can think. Evaluation based on your problem-solving ability."
- **September 2024 candidate at Menlo Park**: Technical statistics questions included: *"In a population with this mean, and that variance, first sample shows X — would you reject some null? What's the probability another sample also rejects the null?"*
- **General Blind sentiment**: "Brush up on stats and experiment design thoroughly. Have a deep understanding of linear models. The questions are scenario-based rather than direct, definitions-only style."
- **Glassdoor note**: "While interviewers were not particularly friendly, the quality of questions was good — scenario-based rather than direct questions about statistics."
- **Multiple candidates confirm**: Google has shifted toward at least one in-person round in 2024-2025 to reduce AI-assistance risk.
- **Process report**: "The phone screen includes one medium-difficulty SQL and one medium-difficulty Python. They focus on reasoning over speed — they want to see you talk through your approach."
- **On onsite rounds**: "You'll meet data scientists, engineers, and product partners. The loop is designed to evaluate technical depth, statistical reasoning, and data-driven thinking on real product problems."

### Reddit (r/developersIndia, 2025) — study list from DS candidate:
> "Here is my collated study materials for Google data scientist specifically:
> 1. Emma Ding - YouTube (@emma_ding/videos)
> 2. CME 106 Probability Cheatsheet (stanford.edu/~shervine)
> 3. SQL Interview Questions (DataLemur)
> 4. Top Data Science Interview Questions (Logicmojo)
> 5. Top 100+ Python Interview Questions (Naukri Code 360)
> 6. Most Asked Coding Questions (PrepInsta)
> 7. Google Data Scientist Interview Guide 2025 (InterviewQuery)"

### Key Pattern from Multiple Reports
- Statistics + experimentation is the most heavily weighted unique differentiator vs. other FAANG roles
- SQL is table-stakes (must be solid, but won't win the interview alone)
- Product sense + causal thinking is what separates L4 from L5 candidates
- Behavioral is ~22% but candidates who fail it are eliminated regardless of technical performance

---

## 5. Best Resources, Books, and Courses

### Books (ranked by relevance for Google DS)

| Book | Author(s) | What it covers |
|------|-----------|----------------|
| **Ace the Data Science Interview** | Nick Singh & Kevin Huo | 201 real questions from FAANG: probability, statistics, ML, SQL, Python, A/B testing, DB design. Best comprehensive solutions. |
| **Designing Machine Learning Systems** | Chip Huyen | Production ML, MLOps, model lifecycle, open-ended ML interview questions — essential for ML rounds |
| **Machine Learning Interviews Book** | Chip Huyen | Free ebook. 200+ ML questions. Author was hiring manager at NVIDIA/Netflix. |
| **Trustworthy Online Controlled Experiments** | Kohavi, Tang, Xu | The definitive book on A/B testing at scale (used internally at Google/Microsoft). Emma Ding recommends this. |
| **Cracking the Coding Interview** | McDowell | Python/algorithms for early coding screens; essential to avoid elimination |
| **Designing Data-Intensive Applications** | Kleppmann | System design for data pipelines; useful for data engineering hybrid roles |
| **120 Data Science Interview Questions** | Various | Case-study format, probability/stats focus, affordable ($19) |
| **Cracking the PM Interview** | McDowell & Bayou | Product sense + metrics + business strategy for product-sense rounds |

### Online Practice Platforms

| Platform | Best for |
|----------|---------|
| **DataLemur** (datalemur.com) | Google-specific SQL questions + stats; free tier available |
| **StrataScratch** | Data science SQL + Python questions from real FAANG interviews |
| **InterviewQuery** | Full DS interview prep: SQL, stats, ML, A/B testing, behavioral |
| **LeetCode** | Coding/algorithms (for Python round); note: SQL on LeetCode alone is insufficient |
| **NickSingh.com** | 40 real FAANG probability + stats questions with full solutions |
| **Kaggle** | Applied ML practice (especially for domain-specific applied ML rounds) |

### YouTube / Free Content

| Resource | What it covers |
|----------|---------------|
| **Emma Ding (@emma_ding)** | Google DS interview deep-dives, statistics, experimentation, product case, SQL |
| **Stanford CME 106 Probability Cheatsheet** | Compact probability reference (stanford.edu/~shervine) |
| **Andrew Ng's ML Course (Coursera)** | ML fundamentals — good for conceptual ML questions |
| **Stanford CS231n** | Deep neural networks (for research-track roles) |
| **Google AI Blog / research.google.com** | Understand Google's actual approach to ML, fairness, experimentation |

### Courses
- **Coursera / DataCamp**: Statistics and Python for Data Science
- **Interview Query's Mock Interview Program**: Hands-on with experienced mentors
- **InterviewKickstart**: Taught by FAANG hiring managers; includes webinars and coaching
- **IBM's Ultimate Data Scientist Program** (mentioned in multiple prep guides)

---

## 6. Tips from People Who Got Offers

### Process Tips
1. **Talk out loud throughout** — interviewers may drop hints if you're off track, but only if they can follow your reasoning. Silent coding is a red flag.
2. **Ask clarifying questions before writing a single line** — Google intentionally designs ambiguous problems. Seeking clarity is evaluated positively.
3. **State assumptions explicitly** — say why you're assuming something and validate with the interviewer.
4. **Start with brute force, then optimize** — find a working solution first, then iterate. Don't get paralyzed searching for elegance.
5. **Walk through a concrete example** — after writing code or designing an experiment, trace through one specific data example to validate your logic.
6. **Present multiple solutions** — show your reasoning for the chosen approach and demonstrate collaborative problem-solving.

### Technical Tips
7. **SQL: treat each query as a conversation with the data** — outline your logic in plain English before writing syntax.
8. **SQL: always address ties** — for ranking questions, explicitly compare RANK() vs DENSE_RANK() and explain your choice.
9. **SQL: mention scalability** — for window functions vs. subqueries, note that awareness of performance at Google scale impresses interviewers.
10. **Stats: structure A/B test answers clearly**: (a) define the problem, (b) state hypothesis, (c) identify key metrics, (d) explain how to interpret results accounting for bias and confounding.
11. **ML: emphasize trade-offs and real-world constraints** — interviewers want to see you understand model behavior beyond training accuracy.
12. **ML: connect explanations to impact** — show that you understand recommendation models as both technical systems and user experience engines.

### Product Sense Tips
13. **Anchor product answers in goals and metrics** — start with the user or business objective, then explain how data evaluates progress.
14. **Build a habit**: when using any Google product, ask yourself "What metric defines success here?"
15. **Pick a favorite Google product before your interview** and prepare how you'd measure its success — bring it up naturally.

### Behavioral Tips
16. **Use STAR method** (Situation, Task, Action, Result) — but end with "what I learned." Google values intellectual humility and growth mindset.
17. **Be authentic about setbacks** — Google values learning over perfection. Discussing failures thoughtfully is a positive signal.
18. **Align with Googleyness**: ambiguity tolerance, collaborative nature, user focus, bias toward action.
19. **Quantify impact** in every story — "conversion rates rose 18%", "error rate dropped 70%", "activation rates rose by 18 percentage points."

### Offer Tips
20. **Negotiate with data** — use Levels.fyi benchmarks. Express enthusiasm first, then discuss adjustments. Focus on total compensation, not just base.
21. **Team matching is not evaluative** — it's your chance to assess alignment with your interests. Ask about team priorities, ongoing projects, growth paths.
22. **Preparation timeline**: 3–6 months of dedicated prep is ideal; at minimum 6–8 weeks for candidates with strong foundations.

### What Separates L4 from L5 Candidates
- L4 (intermediate): Solid technical execution, can design basic experiments, communicates findings clearly
- L5 (senior, 5+ years): Leads cross-functional data strategy, thinks about causal inference beyond A/B, can define metrics from scratch, drives product direction — not just responds to requests

---

## 7. Salary Reference (2024-2025, from Levels.fyi)

| Level | Title | Total Comp | Base | Stock | Bonus |
|-------|-------|-----------|------|-------|-------|
| L3 | Data Scientist II | $168K | $132K | $20K | $7K |
| L4 | Data Scientist III | $264K | $180K | $66K | $24K |
| L5 | Senior Data Scientist | $372K | $204K | $120K | $36K |
| L6 | Staff Data Scientist | $444K | $240K | $156K | $49K |
| L7 | Senior Staff Data Scientist | $696K | $288K | $360K | $62K |
| L8 | Principal Data Scientist | $900K | $348K | $468K | $81K |

Bay Area median ~$360K; NYC ~$288K; Seattle ~$312K; LA ~$252K; Chicago ~$228K.

---

## 8. Key Sources

- [IGotAnOffer — Google Data Scientist Interview](https://igotanoffer.com/blogs/tech/google-data-science-interview)
- [InterviewQuery — Google DS Guide 2025](https://www.interviewquery.com/interview-guides/google-data-scientist)
- [Prepfully — Google DS Exhaustive Guide](https://prepfully.com/interview-guides/google-data-scientist)
- [StrataScratch — Google DS Interview Guide](https://www.stratascratch.com/blog/google-data-scientist-interview-guide/)
- [DataLemur — Google SQL Interview Questions](https://datalemur.com/blog/google-sql-interview-questions)
- [BigTechInterviews — Google DS Questions](https://bigtechinterviews.com/google-data-scientist-interview-questions/)
- [NickSingh.com — 40 FAANG Probability & Stats Questions](https://www.nicksingh.com/posts/40-probability-statistics-data-science-interview-questions-asked-by-fang-wall-street)
- [InterviewKickstart — Google DS Questions](https://interviewkickstart.com/blogs/interview-questions/google-data-scientist-interview-questions)
- [Exponent — Google DS Interview Guide](https://www.tryexponent.com/guides/google-data-scientist-interview-guide)
- [Emma Ding — ML Interview Guide](https://www.emmading.com/blog/the-ultimate-guide-to-acing-machine-learning-interviews-for-data-scientists-and-machine-learning-engineers)
- [AceTheDataScienceInterview — Best Books](https://www.acethedatascienceinterview.com/best-data-science-interview-books)
- [InterviewQuery — Best DS Books](https://www.interviewquery.com/p/data-science-interview-books)
- [Blind — Google DS Interview Discussion](https://www.teamblind.com/post/google-data-scientist-interview-whats-it-like-hqyaunj8)
- [Edureka — Google DS Interview Questions](https://www.edureka.co/blog/google-data-science-interview-questions/)
- [ProjectPro — Google DS Interview](https://www.projectpro.io/article/google-data-scientist-interview-/457)
- [FinalRoundAI — Google DS Prep Guide](https://www.finalroundai.com/blog/how-to-prepare-for-the-google-data-scientist-interview-a-step-by-step-guide)
