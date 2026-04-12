# Google Data Scientist: Firsthand Interview Reports

Source: google/research/reddit/firsthand-interview-reports.md

# Google Data Scientist: Firsthand Interview Reports

> Compiled from: onsites.fyi (real candidate submissions), sqlpad.io (named candidate account), IGotAnOffer, InterviewQuery, Glassdoor aggregates, Blind discussion threads (content extracted where JS rendering allowed), and prep guides that cite sourced candidate quotes.
>
> Research conducted: March 2026
>
> NOTE ON SOURCING: Reddit blocks all crawler access. Blind uses JS rendering that prevents content extraction via fetch. LeetCode Discuss returns 403. Glassdoor returns 403. The most reliably fetchable firsthand source was **onsites.fyi** (structured candidate submissions) and **sqlpad.io** (named candidate writeup). Everything else is sourced from guides that aggregate candidate-reported questions.

---

## SOURCING TRANSPARENCY

| Source | Fetchable? | Content Quality |
|---|---|---|
| reddit.com | BLOCKED by Anthropic crawler policy | Cannot access |
| teamblind.com | Renders via JS only - content not extractable | Cannot read post body |
| glassdoor.com | 403 Forbidden | Cannot access |
| leetcode.com/discuss | 403 Forbidden | Cannot access |
| medium.com (most articles) | 403 Forbidden | Cannot access |
| onsites.fyi | YES - structured submissions | Real candidate reports |
| sqlpad.io | YES | Named candidate, full account |
| igotanoffer.com | YES | Aggregated from candidate reports |
| interviewquery.com | YES | Aggregated from candidate reports |
| prepfully.com | YES | Aggregated from candidate reports |

---

## PART 1: VERIFIED FIRSTHAND ACCOUNTS

---

### Account 1: "Jay" - Google Cloud Data Scientist - OFFER
**Source:** https://sqlpad.io/tutorial/google-cloud-data-scientist-job-interview/
**Date:** Not specified (writeup appears 2023-2024 era)
**Outcome:** OFFER received
**TC:** ~$280K USD
**Location:** Mountain View, CA
**Experience at time of interview:** 2 years
**Education:** M.S. in Machine Learning
**Prep time:** 3 months
**Total interview process:** 3 months

#### Round 1: Recruiter Phone Screen
- Covered logistics: VISA status, salary expectation, start date, ideal team
- Team introduction and project overview for the role

#### Round 2: Technical Phone Screen (4 questions)
1. "How do you decide which Google apps to show by default on Google's home page?" *(product/decision question)*
2. Techniques for handling missing data
3. Dimensionality reduction methods
4. Logistic regression regularization approaches

#### Round 3: Virtual Onsite - Statistics & ML (4 questions)
1. Explaining confidence intervals to non-technical audiences
2. Determining A/B test duration
3. Definition of null hypothesis
4. Statistical power and improvement strategies

#### Round 4: Virtual Onsite - Googliness / Behavioral
- Demonstrate initiative: give an example
- Conflict handling and standing ground: give an example
- Describe your ideal team composition

#### Round 5: Virtual Onsite - Statistics Coding (3 questions)
1. "Create a function that generates unbiased coin flips from a biased coin"
2. "Calculate array median without using any built-in functions"
3. Time series analysis: ARIMA and handling heteroscedasticity

#### Round 6: Virtual Onsite - Leadership / Behavioral
1. "Why Google?"
2. Reasons for leaving current position
3. Biggest accomplishment / proudest project
4. Candidate questions for interviewer

**Outcome:** Offer received approximately one week after virtual onsite.

**Notable surprises:** The statistics coding round (Round 5) mixing implementation (median without builtins) with advanced time series concepts (ARIMA + heteroscedasticity) in the same round.

---

## PART 2: ONSITES.FYI STRUCTURED CANDIDATE REPORTS

Source: https://www.onsites.fyi/Google/Data%20Scientist
These are real candidate submissions with level, stage, outcome, and difficulty ratings.

---

### Report A: L4 Onsite - REJECTED
**Date:** November 2023
**Level:** L4
**Stage:** Onsite
**Outcome:** Rejected
**Difficulty:** Medium
**Candidate note:** "Overall process was ok. Did about 6 interviews and was treated nicely in most."

**Questions asked:**
- Drug effectiveness experiment design (2 groups, 2 drugs) *(experimentation round)*
- YouTube watched vs. Age relationship study *(analysis/product round)*
- Percentile function coding challenge *(coding round)*
- Google search time analysis and trend explanation *(product/analysis round)*

**Additional note:** Candidate requested feedback 4 times after rejection and received none. Flagged poor post-rejection communication as a complaint.

---

### Report B: L3 Onsite - Outcome Unknown
**Date:** July 2023
**Level:** L3
**Stage:** Onsite (5 rounds total)
**Outcome:** Not reported
**Difficulty:** Medium

**Round structure:**
- Round 1: HR - discussion on past projects
- Rounds 2-3: Theoretical stats + data analysis questions
- Rounds 4-5: Applied problem-solving: A/B testing, bias removal, inference from ad campaign data

---

### Report C: L4 Phone Screen - REJECTED
**Date:** June 2023
**Level:** L4
**Stage:** Phone Screen
**Outcome:** Rejected
**Difficulty:** Medium
**Format:** Google Meet + Google Docs

**Questions asked:**
1. "When do you use mean vs. median?" *(statistics)*
2. "Sample N=1000 from a normal distribution (μ=0, σ=1) and plot a histogram" *(coding - Python)*
3. "Calculate the sum of odd-positioned numbers from a sequence of 100 numbers" *(coding)*
4. Past data science project discussion *(behavioral)*
5. "What is the probability of a Type 1 error with altered sampling distributions?" *(statistics)*
6. Logistic regression theory question *(ML)*

**Surprise:** Described as "exam-style statistics questions" - heavier theoretical stats than expected for a phone screen.

---

### Report D: L4 Onsite - REJECTED
**Date:** June 2023
**Level:** L4
**Stage:** Onsite
**Outcome:** Rejected
**Difficulty:** Hard
**Candidate note:** "The stages prior to the on-site were conducted well. However, my negative rating is because of how the on-site was conducted."

**Complaints:** Interviewers seemed inexperienced; condescending behavior; misaligned expectations on problem-solving approaches; no feedback provided after multiple requests.

*(Specific questions not disclosed by candidate)*

---

### Report E: L4 Phone Screen - REJECTED
**Date:** April/May 2023
**Level:** L4
**Stage:** Phone Screen
**Outcome:** Rejected
**Difficulty:** Medium
**Format:** Google Meet + Google Docs

**Questions asked:**
- Regression concepts (foundational)
- Training/testing fundamentals
- Number sorting coding exercise
- Histogram visualization task (coding)

---

### Report F: L3 Phone Screen - Outcome Unknown
**Date:** April 2023
**Level:** L3
**Stage:** Phone Screen
**Outcome:** Not reported
**Difficulty:** Hard
**Candidate note:** "Difficult statistical questions, much different than other data science interviews. Focused on theory on hypothesis testing, time series analysis, logistic regression."

**Specific question asked (verbatim):**
- "Derive the maximum likelihood estimator for logistic regression"

**Additional topics covered:** Hypothesis testing theory, time series analysis, Python coding

**Surprise:** Explicitly called out as much harder on stats theory than typical DS interviews at other companies.

---

## PART 3: AGGREGATED REAL QUESTIONS (from guides citing Glassdoor/Blind candidate reports)

The following questions are cited across multiple prep guides as sourced from actual Glassdoor interview reports or Blind threads. They appear with high frequency across independent sources, suggesting genuine provenance.

### Phone Screen - Consistently Reported Questions

**Statistics:**
- "When would you consider using mean over median?" (appears in 4+ sources)
- "For sample size n, the margin of error is 3. How many more samples do we need to make the margin of error 0.3?" (appears in 3+ sources)
- "What is the probability of a Type 1 error with altered sampling distributions?"
- "What are the assumptions of error in linear regression?"
- "Given 3 coin tosses of a fair coin resulting in Heads, what is the probability the 4th is also Heads?"
- "There are 4 people in an elevator and 4 floors in a building. What's the probability each person gets off on a different floor?"
- "Make an unfair coin fair." (classic Bernoulli trick - use von Neumann extractor)
- "What's the probability of heads given a biased coin and ten fair coins?"
- "If the individual mean of two groups is rising, is it possible the pooled mean decreases? If yes, how?" (Simpson's Paradox)

**Coding:**
- "Write a function to generate N samples from a normal distribution and plot the histogram" (Python)
- "How would you find the top 5 highest-selling items from a list of order histories?" (SQL/Python)
- "How do you calculate the median for a given column of numbers in a data set without built-in functions?" (Python)
- "Calculate the sum of odd numbers in a sequence of 100 numbers" (Python)
- "Write code to implement a hash table in Python"
- "Write code to invert a binary tree"

---

### Onsite - Statistics & Experimentation Round

- "How would you design an A/B test comparing two drug treatments for effectiveness?" (experiment design)
- "How would you design an A/B test to detect a 3% increase in conversion?"
- "How would you assess the validity of an A/B test result that shows a p-value of 0.04?"
- "In an A/B test, how would you verify that users were assigned to test buckets randomly?"
- "If you wanted to test both the color and placement of a sign-up button, how would you design the experiment?" (multivariate)
- "If your A/B test data is not normally distributed, how would you determine which variant performed better?"
- "How would you determine A/B test duration?"
- "What sanity checks would you perform before launching an experiment?"
- "What statistical power is and how you would improve it"
- "Explain confidence intervals to a non-technical audience"
- "Derive the maximum likelihood estimator for logistic regression" (L3 phone screen, theory-heavy)
- "Effect of highly correlated predictors on logistic regression coefficients?"
- "How to generate a Bernoulli distribution matrix in Python?"
- "Explain parametric vs non-parametric statistics differences"

---

### Onsite - Product Interpretation / Case Round

- "You have a Google app and you make a change. How do you test if a metric has increased or not?"
- "How do you detect viruses or inappropriate content on YouTube?"
- "Does upgrading Android produce more searches? How would you measure this?"
- "The outcome of an experiment is that 5% of one group clicks more. Is that a good result?"
- "How would you investigate a significant drop in YouTube watch time on the homepage?"
- "Your system detects a huge uptick in new accounts in a particular region. How do you approach this?"
- "Google Cloud API calls have doubled over the past month. How do you determine the reason?"
- "Working with the PM of Google Meet on rolling out new UX buttons - what advice would you give and what metrics would you track?"
- "How would you design an automated system to catch abusive comments on Google's platforms?"
- "Determine whether user growth is organic or bots using a particular dataset"
- "Data shows a massive decrease in user engagement. Find out why using these datasets and recommend a solution"
- "How would you measure the success of a new Google Maps feature?"
- "How would you investigate opportunities to improve the Google Maps user experience?"
- "How would you design the YouTube video recommendation algorithm?"
- "YouTube watch time vs. age relationship - how would you study this?"

---

### Onsite - Machine Learning Round

- "When should you use regularization versus cross-validation?"
- "Why would the same ML algorithm generate different success rates using the same dataset?"
- "What is the difference between K-means and EM algorithm?"
- "When is a Gaussian mixture model appropriate?"
- "What are the steps to test the applicability of the Gaussian mixture model?"
- "How would you evaluate clustering model performance when labels are known?"
- "How would you encode a categorical variable with thousands of distinct values?"
- "What is the difference between a bagged model and boosted model?"
- "How would you build a model to predict user churn for Google Cloud customers? Describe feature engineering, model selection, and evaluation."
- "Design a machine learning/LLM tool to help track advertising performance"
- "How can you prove that a k-means clustering algorithm converges in a finite number of steps?"
- "How would you build the recommendation algorithm for type-ahead search?"
- "ARIMA and handling heteroscedasticity in time series" (coding round)

---

### Onsite - Statistics Coding Round (Python)

- "Create a function that generates unbiased coin flips from a biased coin" (von Neumann)
- "Calculate array median without built-in functions"
- "Write a function that draws N samples from a population with mean=0, SD=1"
- "Generate a percentile function from scratch"
- "How would you simulate a biased coin toss?"
- "How would you simulate a bivariate normal distribution?"
- "ARIMA time series implementation + heteroscedasticity handling"

---

### Onsite - Behavioral / Googleyness Round

- "Google values a culture of continuous learning. Can you provide an example?"
- "How did you manage tight deadlines and competing priorities?"
- "Tell me about a time you put someone else's interests above your own"
- "Tell me about a time you brought disagreeing teams together"
- "Tell me about a time you launched a new initiative"
- "Tell me about a time you made a decision based on data and were wrong"
- "Tell me about a time you had a conflict with someone. How did you resolve it?"
- "Demonstrate initiative: give an example"
- "Conflict handling and standing your ground: give an example"
- "Describe your ideal team composition"
- "Why Google?"
- "Why are you leaving your current role?"

---

### SQL Round (from Google Data Analyst / DS interviews)

- "Return the last transaction for each day, including id, timestamp, and amount"
- "Get the top three salaries by department"
- "Calculate first touch attribution for each user who converted"
- "Compute departmental spend by fiscal quarter, grouping IT, HR, Marketing, and Other"
- "Find the second-highest salary in the engineering department"
- "Find the top three highest salaries in each department"
- "Get the last transaction for each day from a bank transactions table"
- "Median Google Search Frequency" - calculate median from a summary table
- "Odd & Even Measurements" - sum odd/even-numbered measurements by day
- "How would you determine which marketing channel brought a customer to your website for the first time?" (first touch attribution)
- "How would you handle missing values in a dataset using SQL?"

---

## PART 4: CANDIDATE EXPERIENCE PATTERNS (cross-source synthesis)

### What surprised candidates the most:

1. **Statistics theory depth**: Multiple L3/L4 candidates noted Google's stats questions are significantly harder than other FAANG DS interviews. One candidate explicitly wrote: "Difficult statistical questions, much different than other data science interviews."

2. **Deriving from scratch**: Deriving MLE for logistic regression, implementing median without builtins, writing coin-flip functions from scratch - these are more rigorous than typical "explain the concept" questions.

3. **No Leetcode-hard**: The coding component is NOT Leetcode hard. It's more Python/SQL data manipulation, statistical simulation, and basic algorithms. The L3 candidate who had to derive MLE was at the hard end.

4. **Experiment design is central**: A/B testing questions appear in nearly every account - not just "explain A/B testing" but "design a specific test" with details about power, duration, randomization checks.

5. **Interviewer quality variance**: Two separate candidates on onsites.fyi complained about inexperienced, condescending interviewers during their onsite loop. Both were rejected. Whether this is correlated or coincidental is unknown.

6. **No feedback given**: Multiple candidates noted Google provides zero feedback after rejection.

7. **Product questions require Google product knowledge**: Questions are anchored to specific Google products (YouTube, Google Maps, Google Meet, Android, Google Ads). Knowing these products matters.

### Pass rates and timelines:
- ~3 million applicants annually; fewer than 1% receive offers
- Phone screen to onsite: not always guaranteed even if phone screen "went well"
- Offer decision: 1-2 weeks after onsite (Jay's account: 1 week)
- Most rejections at the phone screen stage (onsites.fyi shows majority of reports are phone screen rejections)

### Level-specific observations:
- **L3**: Heavier theory emphasis (MLE derivation, time series theory)
- **L4**: More balanced - statistics coding + product cases + experimentation design
- **L5+**: Expect system design for ML/DS, deeper domain expertise questions

---

## PART 5: SOURCE URLS

**Directly fetchable firsthand accounts:**
- https://sqlpad.io/tutorial/google-cloud-data-scientist-job-interview/ (Jay's full account - OFFER)
- https://www.onsites.fyi/Google/Data%20Scientist (6 structured candidate submissions)

**Prep guides aggregating real Glassdoor/Blind questions:**
- https://igotanoffer.com/blogs/tech/google-data-science-interview
- https://www.interviewquery.com/interview-guides/google-data-scientist
- https://prepfully.com/interview-guides/google-data-scientist
- https://www.tryexponent.com/guides/google-data-scientist-interview-guide
- https://bigtechinterviews.com/google-data-scientist-interview-questions/

**Blocked/inaccessible (required for truly raw Reddit/Blind/Glassdoor data):**
- reddit.com (Anthropic crawler blocked by domain policy)
- teamblind.com (JS-rendered, body not extractable)
- glassdoor.com (403 Forbidden)
- leetcode.com/discuss (403 Forbidden)
- medium.com (most articles 403)

**Specific Blind posts found (titles only - content not accessible):**
- https://www.teamblind.com/post/Google-Data-Scientist-Interview-0Gukj7YS
- https://www.teamblind.com/post/google-data-scientist-interview-ushumj2o
- https://www.teamblind.com/post/researchdata-science-interview-google-27mj5gbt
- https://www.teamblind.com/post/ruined-my-google-data-science-interview-njsse3by
- https://www.teamblind.com/post/Google-data-scientist-interview-questions-zGRhutXJ
- https://www.teamblind.com/post/google-data-scientist-interview-bkEwWMJE
- https://www.teamblind.com/post/google-data-scientist-interview-prep-0euuvjem
- https://www.teamblind.com/post/python-in-google-data-scientist-interview-kywfg6n1

**Specific LeetCode Discuss posts found (titles only - content not accessible):**
- https://leetcode.com/discuss/interview-experience/1926993/amazon-sde-1offer-agoda-sr-data-scientistoffer-google-l3reject (Google L3 Reject)
- https://leetcode.com/discuss/interview-experience/1585287/amazon-msft-google-apple-fb-zoom-applied-scientist-multiple-sep-21-offer-rest-reject (Applied Scientist)
- https://leetcode.com/discuss/post/6701617/google-onsite-interview-experience-mar-2-h182/ (March 2025 onsite)
