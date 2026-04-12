# Product Sense Q&A -- Flashcard Style

Source: Ace the Data Science Interview, Ch 10 (Q10.1-10.18) + Ch 11 (Case Studies 11.1-11.8)

---

## Chapter 10: Product Questions

---

### Q10.1 -- Facebook vs Twitter Social Graphs

**Q:** How do the social graphs of Facebook and Twitter differ? What metrics to measure the difference?

- Facebook = friendships (mutual, two-way). Twitter = followership (one-way, you follow celebrities)
- Twitter has a few "hub" accounts with huge followings; Facebook's connections are more evenly spread
- Measure: compare the **degree distribution** (number of connections per user) on each platform
- Twitter distribution will be right-skewed (a few accounts with millions of followers)
- Metrics: average degree, skewness, kurtosis of the degree distribution; box plots of node degrees

---

### Q10.2 -- Uber Surge Pricing Metrics

**Q:** Why does surge pricing exist? What metrics to track if it's working?

- Surge pricing fixes supply/demand imbalance -- too many riders, not enough drivers
- Goal: get more drivers on the road (higher pay) and reduce demand (higher prices)
- **Core metrics:** surge duration, surge multiplier, number of riders/drivers in surge area
- **Counter metrics:** rides taken, rides cancelled, total revenue, driver profit, average wait time
- **Guardrail:** Net Promoter Score (NPS) -- surge pricing annoys people, track customer satisfaction
- Also consider PR risk (those $800 New Year's Uber stories)

---

### Q10.3 -- Airbnb A/B Testing Challenges

**Q:** What makes A/B testing on Airbnb hard?

- **Complex user flow:** search -> message host -> book -> stay -> review. Long process, lots of noise
- **Multiple people & devices:** families plan trips together, use different devices. Hard to track one user
- **Long time horizon:** a "successful stay" takes weeks/months to measure, not minutes
- **Mitigations:** focus on non-intermediary metrics (search-to-booking rate), use ML to find short-term proxies for long-term success
- Mention your own A/B testing war stories for bonus points

---

### Q10.4 -- Google Paying Firefox to Be Default Search

**Q:** Mozilla wants 2x the price for Google to remain Firefox's default search engine. How to estimate the upper bound Google should pay?

- Google's motivation: not just ad revenue -- losing Firefox default could boost competitors like Bing or DuckDuckGo
- **Network effects:** more Google users = better search quality = more users (flywheel)
- Losing Firefox default also hurts Google Maps, Shopping, and other downstream products
- **Pricing approaches:** (1) look at what Google pays Apple for Safari default (~$10B/yr) and scale by Firefox market share, (2) estimate ad revenue from Firefox users and calculate worst-case loss, (3) estimate total revenue (not just search ads) from Firefox users
- Key insight: Google's willingness to pay goes beyond direct search revenue

---

### Q10.5 -- LinkedIn Feed Engagement Metrics

**Q:** What metrics to track LinkedIn Feed engagement? How to improve them?

- **Why the Feed matters:** it keeps users coming back even when not job hunting; drives ad revenue
- **Engagement metrics:** DAU, WAU, MAU, L7/L28 (days active per week/month), session time, posts seen, likes, comments, shares
- Weight different actions: a comment is more valuable than a view
- Also track ad engagement (impressions, clicks) separately
- **Improvement ideas:** personalize the feed ranking, encourage posting, add new content types (video, stories), build ML models to predict what users want to see

---

### Q10.6 -- Lyft A/B Test for New Rider App UI

**Q:** How to A/B test a new rider app feature? How to split users and ensure balanced groups?

- **Metric:** number of rides taken
- Use **stratified random sampling** (balance on demographics, location, etc.) for fair groups
- **Network effects problem:** in one city, if treatment riders book more, drivers shift to them, hurting control riders. Results are exaggerated
- **Solution:** use **geo-based assignment** -- test in comparable cities/markets, not within one city
- **Caveat:** two markets may not stay comparable forever; check baseline metrics are stable

---

### Q10.7 -- Amazon Seller Revenue Distribution Shape

**Q:** What would the distribution of average revenue per seller on Amazon look like?

- **Right-skewed** (long tail to the right)
- Follows the Pareto principle: 80% of revenue from 20% of sellers
- Many small sellers making little, a few power sellers making enormous amounts
- Think: 80/20 rule applies to almost all business revenue distributions

---

### Q10.8 -- Facebook Bad Content Removal

**Q:** What posts should Facebook take down? How to identify them? What are the trade-offs?

- **Remove:** explicit content, hate speech, misinformation, content from bad actors, regulated goods, scams
- **Detection features:** content (keywords, images), entity (is poster a known bad actor?), context (which group was it posted in?)
- **Trade-off: false positives vs false negatives**
  - False positive (removing a good post) = angry users, censorship accusations
  - False negative (missing a bad post) = harmful content spreads, PR disaster
- Use different sensitivity thresholds for different content types
- For sensitive accounts (politicians, news), add human review to avoid controversy

---

### Q10.9 -- Amazon Author Profiles and Book Sales

**Q:** Books with more complete author profiles sell more. A team scrapes Wikipedia/Goodreads to auto-fill profiles. Sales don't change. Why?

- **Correlation is not causation!**
- Books with better profiles probably had a more reputable publisher who filled it out
- Those publishers also have better book covers, marketing, distribution
- The profile itself isn't driving sales -- it's a proxy for publisher quality
- Auto-filling profiles doesn't replicate the underlying cause

---

### Q10.10 -- Snapchat DAU 5% Drop

**Q:** Snapchat daily active users dropped 5% week-over-week. Diagnose it.

- **Scope:** clarify -- is it daily log-ins? Is 5% a lot for this metric? Any seasonality?
- **Hypothesize:** logging issues? Push notification bug? Product change (snap streaks)? External event (disaster, outage)?
- **Validate:** check with SRE team (logging ok?). Check push notification volume. Check snaps sent, stories posted. Segment by market, OS, language
- **Classify:** found the drop is 7% for iOS, only 1% for Android. Drill into iOS by app version and carrier. Discover a bug in the latest iOS release is logging users out and they can't get back in
- **Root cause:** bug in latest iOS app update

---

### Q10.11 -- Pinterest New Search Algorithm Metrics

**Q:** New search ranking algorithm on Pinterest. How to measure its impact?

- Clarify: was it a backend-only change or UI change too? Any latency impact?
- **Why search matters:** Pinterest is a visual discovery engine; good search = engaged users = ad revenue
- **Direct metrics:** time spent searching, searches per session (but more searches could mean frustration!)
- **Downstream metrics (better):** pin saves after search, clicks on search results, purchases from shoppable pins
- Use **precision@10** or **nDCG** for relevance quality of search results
- Revenue from purchases of buyable pins found via search

---

### Q10.12 -- Netflix Sci-Fi Low Watch Time

**Q:** Sci-fi category has less total watch time than others. Is it a demand problem or supply problem?

- Don't just look at total watch time -- look at **watch time per show**
- If watch time per show is high but there are few shows, it's a **supply problem** (Netflix should make/buy more sci-fi)
- If watch time per show is also low, it's a **demand problem** (people don't want sci-fi)
- Also check: completion rates, user ratings, browse-to-play conversion rate
- Segment by country/language -- maybe sci-fi is popular in some markets
- Look outside Netflix: survey data, Nielsen, competitor offerings
- Consider: maybe the discovery/recommendation algorithm doesn't surface sci-fi well

---

### Q10.13 -- Apple Store Customer Segmentation

**Q:** How to use customer segmentation to boost Apple retail store sales?

- **Why segment?** Treating all customers the same misses opportunities. Different groups have different needs
- **Segment by:** tech savviness, product type bought (iPhone vs MacBook vs Genius Bar)
- **Example insight:** iPhone buyers are 5x more likely to buy AirPods than MacBook buyers. Place AirPods next to iPhones!
- **Techniques:** K-means clustering, cross-reference with online Apple.com purchases
- **Caveat:** can't segment non-Apple customers (no data). Complement with market research

---

### Q10.14 -- Facebook iOS vs Android Instagram Usage Gap

**Q:** 70% of Facebook iOS users also use Instagram, but only 50% of Android users do. Why?

- Check demographics: iOS users may be younger, more urban, higher income
- Check Facebook ecosystem: iOS users may spend more time on Facebook overall (top-of-funnel effect)
- Check the app itself: Instagram app may be smaller/faster on iOS, better optimized
- Check app store ratings, bug reports, scroll latency on both platforms
- Maybe Instagram has under-invested in Android app optimization
- Talk to UX researchers and product leads for both platforms

---

### Q10.15 -- Capital One Quicksilver Card Stickiness

**Q:** How to assess the stickiness of a credit card?

- **Stickiness** = how often and how long people keep using the card
- **DAU/MAU ratio:** what % of monthly users also use it daily? Higher = stickier
- **Month-over-month retention:** by sign-up cohort, what % are still active after X months?
- **Transaction volume churn:** compare total spend this month vs last month for the same users
- Watch for "silent churn" -- people who stop using the card but don't cancel
- Track whether users use the card for a specific purpose (travel vs dining) -- that tells you about switching behavior

---

### Q10.16 -- YouTube Premium Pricing in New Countries

**Q:** How to determine pricing for YouTube Premium in a new country?

- Ask first: "What's the goal of pricing?" (market share grab vs profit from day one)
- **Three pricing approaches:**
  - **Cost-plus:** add up costs (localization, bandwidth, licensing, lost ad revenue) + margin
  - **Value-based:** surveys/focus groups to find what users would pay; look at similar markets
  - **Competitor-based:** price relative to Netflix, Spotify, Hulu, Apple Music in that country
- Best answer: blend all three. Also A/B test different price points or offer tiered pricing

---

### Q10.17 -- Twitter Emoji Reactions

**Q:** Should Twitter add Facebook-style emoji reactions (love, haha, sad, angry) to tweets?

- **Clarify hypothesis:** goal is to increase engagement by making it easier to react (vs writing a reply)
- **Business case:** more engagement = more time on platform = more ads seen = more revenue
- **Data support:** analyze existing tweets/replies for sentiment keywords ("lol", "haha", "so sad") to estimate demand
- **Counter-arguments:** increases complexity, reduces reply-based engagement, risks "Facebook-ification" of the brand
- **Recommendation:** if data shows demand and business case is strong, A/B test it. Pre-align with stakeholders on the trade-off (reactions up, replies down)

---

### Q10.18 -- Slack User Engagement Metrics

**Q:** How to measure Slack engagement? How to detect early signs of decline?

- **Core metrics:** DAU, WAU, MAU + the ratios DAU/WAU and DAU/MAU (higher ratio = stickier)
- **Messages sent** per day/week/month (the core action)
- **Auxiliary:** orgs created, membership applications, channels joined
- **Leading indicators of decline:** watch for users dropping from DAU to WAU to MAU-only. Track DAU/WAU trend over time -- if it's shrinking, trouble is coming
- Segment by cohort -- overall DAU might look fine while specific cohorts are churning

---

## Chapter 11: Case Study Questions

---

### Q11.1 -- Citadel: Predict Retail Store Revenue from Foot Traffic

**Q:** Use GPS-based foot traffic data (10M phones) to predict a retail chain's quarterly in-store revenue.

- **Clarify:** revenue for entire chain or per store? Quarterly granularity (for stock trading decisions)
- **Approach:** aggregate daily foot traffic to quarterly level, normalize for panel size (foot traffic / panel size x population)
- Use simple linear regression: revenue ~ normalized foot traffic
- **Only 12 quarters of data?** Use simpler models (linear regression), add regularization, report confidence intervals. Include data from similar retailers (Target, Costco)
- **True visits** = (sample foot traffic for store / sample panel size) x U.S. population
- **Sampling bias:** not everyone has a smartphone, location apps, or location permissions turned on. Compare panel demographics to census data
- **Limitations:** foot traffic != purchases; third-party data provider may change their attribution algorithm

---

### Q11.2 -- Amazon: Show Recommendation System

**Q:** Design a system to recommend shows on Amazon Prime Video.

- **Main approach:** collaborative filtering -- recommend shows watched by similar users
- **Data:** user-show rating matrix (rows = users, columns = shows, values = 1-5 ratings)
- **Similarity:** cosine similarity between user rows (normalize first to handle rating bias)
- **Cold-start problem for new shows:** use content-based features (genre, actors, language)
- **Cold-start for new users:** show popular/trending content until you have enough data
- **A/B test the model:** even if watch time goes up (p=0.04), also check precision (% of recs actually watched), recall, and counter metrics (avg rating of recommended vs user-selected shows)
- **Deployment considerations:** how often to retrain? Should Amazon originals get a boost? Batch vs real-time?

---

### Q11.3 -- Airbnb: Predict New Listing Revenue

**Q:** Predict yearly revenue for a new Airbnb property listing. What features to use?

- **Clarify purpose:** showing potential hosts expected earnings, or deciding what markets to expand in?
- **Features:** bedrooms, bathrooms, sq footage, kitchen, nightly rate, occupancy limit, min nights, zip code, distance to attractions, nearby listing prices and occupancy rates
- **Model:** start with linear regression (Occam's Razor). Consider XGBoost if non-linear
- **Missing data (10% missing square footage):** don't just drop or average -- build a model to predict sq footage from bedrooms + bathrooms. Or use third-party parcel data
- **Too many features?** Use feature selection (RFE, VIF) then PCA for dimensionality reduction
- **Sparse features?** Use random forests or embedding layers instead of plain linear regression

---

### Q11.4 -- Walmart: Optimal Product Pricing Algorithm

**Q:** Build a pricing algorithm for all Walmart products.

- **Scale:** ~5,000 stores x 100,000 items = 500 million price decisions
- **Frequency trade-off:** update prices too often = confuses customers (Walmart's brand is "everyday low prices"). Update twice: initial price + clearance price
- **Approach:** build demand curves using linear regression (demand ~ price). Find optimal price point that maximizes profit = (price - cost) x quantity sold
- **Price elasticity:** negative coefficient = elastic good (demand drops fast with price increase, e.g., beer). Small negative = inelastic (e.g., prescription drugs)
- **Extra data for a "black box" model:** item cost, shelf placement, competitor prices, inventory/expiry, historical sell-through rates
- **A/B test it:** pick two similar product categories (toothpaste vs toilet paper), use algorithm for one, status quo for the other. Measure revenue, profit, sell-through rate over a few months

---

### Q11.5 -- Accenture: Hotel Brand Sentiment Analysis

**Q:** Help a hotel chain analyze what people say about them on social media. How and why?

- **Why:** social listening catches feedback that formal surveys miss. A viral tweet or Reddit post can do real damage
- **Preprocessing:** fix encoding, strip HTML, remove stopwords, stem/lemmatize, then vectorize
- **Vectorization:** Bag-of-words, n-grams, or TF-IDF
- **Sentiment model:** logistic regression, SVM, random forest, or fine-tuned NLP model (spaCy, Hugging Face). Evaluate with precision/recall
- **Topic classification:** use k-means clustering or LDA (Latent Dirichlet Allocation) to group reviews by topic (check-in, room quality, food)
- **Actionable output:** route negative reviews to the right department. Proactively reach out to unhappy customers. Alert properties in real-time about negative spikes

---

### Q11.6 -- Facebook: People You May Know (PYMK)

**Q:** Build Facebook's friend recommendation feature.

- **Two approaches:** (1) contact-book import at sign-up, (2) leverage the social graph (friends of friends)
- **Features for ranking potential friends:** mutual friend count, profile similarities (school, employer, hometown), in-app activity (same events, tagged in photos together), ecosystem signals (connected on Instagram, Messenger), off-app signals (email, phone, GPS)
- **Ranking models:** logistic regression or naive Bayes to predict friendship probability. Or unsupervised: K-means/PCA to find similar users with maximum friend overlap
- **Cold-start for new users:** hard -- no friends yet, no activity data. Boost new users in existing users' PYMK. Use gamification (progress bar: "Add 5 more friends!")
- **Why new users matter:** Facebook's value = social graph. Without friends, the feed is empty, user churns. Helping new users make friends fast is strategically critical

---

### Q11.7 -- Stripe: Loan Approval Model

**Q:** Evaluate a loan approval model for small businesses. What metrics? What trade-offs?

- **It's binary classification:** will the loan be repaid or defaulted?
- **Metrics:** precision, recall, precision-recall curve (NOT accuracy -- it's imbalanced, most loans don't default)
- **False positives vs false negatives are NOT equal cost:**
  - False negative (loan denied but would have been repaid) = lost 10% interest income
  - False positive (loan approved but defaults) = lost 100% of principal
  - So FN:FP cost ratio is roughly 1:10. Optimize the threshold accordingly
- **Improve the model:** use reject inference (learn from rejected applications too), add anomaly detection
- **Features:** applicant demographics, bank balance, credit score, liens; plus loan-level features (amount, purpose, collateral)
- **A/B test:** difficult because loans take months to resolve. Use offline model comparison (paired t-test) instead. If p=0.06, run longer -- don't ship on borderline significance

---

### Q11.8 -- Instagram: Content Recommendations for Explore

**Q:** How to build Instagram Explore recommendations?

- **Account-level approach:** find accounts a user would like (not individual posts) using collaborative filtering
- **Candidate retrieval:** build "ig2vec" embeddings (like word2vec but for IG accounts based on user interaction sequences). Or use a user-account interaction matrix and factorize it
- **Ranking:** KNN on embeddings to find similar accounts, then train a neural network to predict actions (like, comment, share, save, hide, report) as multi-class probabilities. Weight them by business value into a final recommendation score
- **Deployment:** must be real-time (not batch). Store features in fast-access storage (Cassandra, not HDFS)
- **Rollout:** use "flighting" deployment (A/B test the new model vs old)
- **Monitor over time:** track model drift with KL divergence on feature distributions. Retrain periodically
- **Watch out:** a model that's too good at predicting preferences can feel creepy and actually decrease engagement
