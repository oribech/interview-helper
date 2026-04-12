New chat
⇧⌘O
Search
⌘K
Customize
Chats
Projects
Artifacts
Code
Starred
food-tracker
AB testing interview prep
ADHD stimulant effects: designing an n-back training experiment
Dual n-back for ADHD engineering: transfer problem and working memory
Mental macro unit approximation hack
Getting shredded abs: 8-16 week fat loss plan
Analyzing weight and nutrition data for calorie balance
Trading strategies to earn $200 monthly consistently
Greeks in finance and quantitative trading strategies
Recents
Hide
Understanding population sampling methods
Understanding population sampling methods
Daily food intake log
עוגת בסקוויטים עם גבינת קוטג׳
עוגת גבינה עם מלטיטול
How compound interest works
Daily food and calorie tracking
Personal coaching request
Coach me
Coaching request
Personal coaching request
Personal coaching request
Personal coaching request
תכנון תזונה יומי
Daily macro tracking reminder
Claude legal plugins overview
הודעה על חופשת מחלה וגמילה מתרופה
Custom website with WordPress editing access
חיפוש פרטי קשר של עו"ד נהורא לוי
חיפוש רשומה מאתמול
תכנון מאקרו יומי
Daily food log
Wine 400ml daily measurement
Male sexual expression terminology
Male lust in one word
Male pride in one word
Attitude determines altitude
Risk management formulas and best practices
Trending AI tools and news
Missile trajectory angles to Tzur Hadassah
All chats
AC
A certified MD and psychiatrist with a deep need for concrete analytucal details
Max plan
AB testing interview prep

PDF

ab_concrete_2day.html

HTML

ab-testing.md

17 lines

MD

I'm hard full blown adhd data scientist
i have google ds interview in 2 days
i need to learn this subject: ab testing
I'm attaching learning materials and interivew questions
your job is to ask me questions from the interivew questions, i will answer and we discusse each answer enabling me to answer better more accurately using knowledge from the md and your knowledge.
Make sure to respond very very clearly very very shortly
Mar 15
Calibrated concise A/B testing interview prep strategy
Calibrated concise A/B testing interview prep strategy

Got it. Let's go.

Q026 (most common — asked 3x):

Walk me through how you'd design an A/B test.

ok we have few components

hypothesis
the main goal metric, the OEC, guardrails
randomization units
Population
size and duration

the problem here is that i knew to tell these 5 but I cannot think alone about some example

Mar 15
Validated framework comprehension and devised practical example approach
Validated framework comprehension and devised practical example approach

Solid structure. Let's make it stick with a real example.

Scenario: YouTube is testing a new "Skip Ad" button design.

Walk me through your 5 points for this. Don't overthink it — just go.

ok but bewofre we continue put here plan to cover what we need + metric to test if I'm ready?

then i will answer your questions

Mar 15
Recognized need for structured plan and readiness assessment
Recognized need for structured plan and readiness assessment

Plan:

Design an A/B test (Q026) — structure + example
Small effect handling (Q027) — 3% increase scenario
Metrics & KPIs (Q030) — what to measure
Bias removal (Q032) — selection bias, SRM
Stats concepts — p-value, power, Type I/II, sample size
Edge cases — novelty effects, network interference, multi-variant

Readiness metric:

After each question I'll score you 1-3:

3 = could say this in an interview confidently
2 = right direction, needs sharpening
1 = gap, needs work

Target: average ≥ 2.5 across all questions before your interview.

Ready? Back to YouTube Skip Ad — walk me through your 5 points.

wait. YouTube is testing a new "Skip Ad" button design.
why they do it? what is the purpose? is this part of the question?

1.

Mar 15
Recognized importance of clarifying test objectives first
Recognized importance of clarifying test objectives first

Yes! Great instinct. In an interview, always clarify the goal first.

"Why are we changing the button?" → e.g., to increase ad completion rate? reduce frustration? improve CTR?

This directly determines your hypothesis and OEC.

For our example: goal = increase user satisfaction while keeping ad revenue stable.

Now go — your 5 points.

ok. so

hypothesis: increase user satisfaction 
OEC: more consecutive page views for a user with the button, guardrails: CTR, make sure it doesnt decrease due to the button
randomization unit: users
population: users who viewed page with video
size and duration: not sure. I guess week or 2 and the size? 500? depends on the size of the assumed effect? what is the minimal delta we are looking for what  is the current satisfaction, how do you measure it? what is the expected increase?

BTW: be hontest, dont try to appease me, strive to simualte an actual google ds interivew, give me tips

Mar 15
Scrutinized experimental design flaws and formulated constructive feedback
Scrutinized experimental design flaws and formulated constructive feedback

Score: 2/3

Issues:

Hypothesis — too vague. Not testable. Should be:

"New skip button design increases sessions-per-user without decreasing ad CTR"

OEC — "consecutive page views" is unclear. Say: sessions-per-user or watch-time-per-user

Guardrails — good instinct, but also add: ad revenue per user

Population — too broad. Should be: users who were served an ad (triggered analysis — only people who could be affected)

Size — 500 is laughably small for Google. The right answer:

"Use power analysis: n ≈ 16σ²/δ² where δ is the minimum detectable effect I care about"

You don't know exact number but you know the formula and inputs.

Duration — good, but say why: capture day-of-week effects, avoid novelty effects

Interview tip: Google interviewers want to hear you think out loud with structure, not just list components. Say "because" after every choice.

Try re-answering the hypothesis + OEC + population in 3 clean sentences.

few points:
1. re-answering will not help me here, generate new business example and I will answer it
2. is there tip for HOW to answers or THINK outloud? how to show it
3. show me the derivation of the power formula
4. duration: week is ok to detect novelty effects?

Mar 15
Organized four distinct requests requiring varied approaches
Organized four distinct requests requiring varied approaches

1. New example coming after we cover 2-4.

2. How to think out loud: Always say: "I'm choosing X because Y, and the tradeoff is Z"

"I'm using sessions-per-user as OEC because it captures engagement, though it might miss ad revenue impact, so I'll add that as guardrail"

3. Power formula derivation:

You want P(reject H0 | true delta = δ) = 80%

Reject when |T| > 1.96, where T = δ / (σ√(2/n))

So: δ / (σ√(2/n)) = 0.84 (80th percentile of normal)

Solve for n:

n ≈ 16σ²/δ² (per variant)

The 16 = 2 × (1.96 + 0.84)²

4. Duration — NO, one week is NOT enough for novelty effects.

One week captures day-of-week effects. ✅

For novelty effects you need 2-4 weeks — users initially click new button out of curiosity, behavior stabilizes later.

Rule: plot your metric daily — if it's still changing at week 1, run longer.

New example ready?

the power formula. it is not clear. not clear at all. search the web. show me the probabilistic derivation. also hard to read the formula style you put (see image)

use some md file artifact. not here in the chat body

dont write anything here just create md file

Mar 15
4 / 4
Deliberated optimal format for rendering mathematical derivations clearly
Deliberated optimal format for rendering mathematical derivations clearly
Claude's response was interrupted
Retry

much shorter and clearer

Mar 15
Architected concise HTML visualization for formula derivation
Architected concise HTML visualization for formula derivation

Ready for the new example when you are.

Power derivation
Code · HTML 
Download

lets very concise create md cheatsheet and put there

the components  for  the ab test (hypothesis oec ...) 
the power formula
Mar 15
Architected concise markdown cheatsheet covering A/B test components and power formula
Architected concise markdown cheatsheet covering A/B test components and power formula

Ready for the next question?

Ab cheatsheet
Document · MD 
Download

much much more conscise and desne. no explanations. it is formula cheat sheet god damn it.

Mar 15
Recognized user's demand for formula-only cheat sheet format
Recognized user's demand for formula-only cheat sheet format

Next question?

Ab cheatsheet
Document · MD 
Download

ok. lets proceed to the new example

Mar 15
Prepared fresh A/B testing scenario for practice
Prepared fresh A/B testing scenario for practice

Google Search is testing adding an AI-generated summary box at the top of search results.

Walk me through your 5 components.

hypothesis: increase user session because it will have less friction but the trade off can be less ad clicks as the user will not get into the site so we need guard rails for ad revenue/ad views

oec: adding an AI-generated summary box at the top of search results. will increase user session without harming ad revenue/views

Rand. unit: use_id
population: users who viewed the search results page
duration: ≥ 1 week (day-of-week) + 2–4 weeks if novelty effects
size: n = 16sigma2/delta2 where delta is the expected change and sigma is the sd of the user sessions

now since the user sessions might not be normally distributed we maybe want different formula for exmple for poisson? keeping in mind that T is less fragile to non normaility

Show more
Mar 16
Evaluated experimental design and statistical methodology rigor
Evaluated experimental design and statistical methodology rigor

Score: 2.5/3

Good: Nailed the tradeoff instinct (less friction → fewer ad clicks). Guardrails are correct.

Issues:

Population too broad — should be users who searched and were served the summary box, not all search results viewers
OEC vague — "user session" → say sessions-per-user or queries-per-user (more precise for search)
Normality point — good instinct but incomplete. Correct answer:

CLT saves you at Google scale (millions of users). T-test is fine. Normality assumption is on the mean, not the raw metric. Only worry if extreme skew → then cap outliers (e.g. cap sessions-per-user at 99th percentile).

Poisson is for counts with small n — irrelevant at Google scale.

One gap I want to test you on:

Why is "users who viewed search results" a bad population choice — what's the specific term for the correct approach?

about Population too broad: but this is the treatment group the popoulation is the treatement or both control+treatment?

Mar 16

Both. Population = the pool from which you draw both Control and Treatment.

The issue: users who viewed search results but didn't get an ad cannot be affected by ad revenue guardrail. Including them adds noise.

The correct term is triggered analysis — only include users who were actually eligible to see the summary box (i.e. made a search query that triggered the feature).

Now answer my previous question: what's wrong with "all search results viewers" in one sentence?

i dont understand really.
1. the point about the ad, this is the exact problem we have less ad views because the user is not bothering in entering sites and viewing the ads
2. so the population should be these that searched something in google and we want to see whether they have less ad vies
3. i didnt understand the triggered analysis 
4. you asked for population which should include both those that saw the box and those that didnt (control group)

Mar 16

You're right, I was wrong on the ad point. Let me clarify cleanly.

Population = everyone eligible for the experiment (both Control + Treatment).

For this test: users who made a search query ✅

That's it. You had it right.

Triggered analysis — only relevant when the feature doesn't fire for everyone. Example: summary box only appears for queries with >5 words. Then users with short queries can't be affected → exclude them → less noise → more power.

Not critical here if box shows for all queries.

Your answer was actually 2.5-3/3. I overcomplicated it. Sorry.

Next: Q027 — hardest one.

You run the test. You see a 3% increase in sessions-per-user. p-value = 0.12. What do you do?

First of all do we have practical significance? is 3% good. I guess yes how does it implicate on business kpis?
since p=0.12 and effect size is big enough i would say come up with more power as there is maybe a noise in the sample
Mar 16

Score: 3/3

Exactly right. That's case 5 from the book — practically significant, not statistically significant → run again with more power.

How to say it in interview:

"3% is likely practically significant for Google scale. p=0.12 means we can't rule out noise. I'd increase sample size or run longer — not change the hypothesis."

One add-on they might push back with:

"We can't wait. Should we launch or not?"

What do you say?

you can do ramping. 
is this the correct answer?

BTW. 2 days almost past, what is the plan until covering the full subject?

Mar 16
3 / 3

Ramping — partially correct. Ramping is for risk mitigation during rollout, not for resolving statistical uncertainty.

Better answer:

"Without statistical significance I'd not launch. The cost of a wrong decision at Google scale is too high. I'd push for more data."

But if forced: > "Launch to small % (ramping), monitor guardrails in real-time, treat it as extended experiment."

Plan — you have ~1 day left:

Priority	Topic	Status
✅	Design components	Done
✅	Power formula	Done
✅	p-value / practical significance	Done
🔲	Bias & SRM (Q032)	Next
🔲	Type I/II + multiple testing	After
🔲	Novelty/primacy effects	After
🔲	Network interference	After
🔲	2 drug experiment (Q029)	After
🔲	Mock full question end-to-end	Last

Suggest: 3 more topics today, mock tomorrow morning.

Ready for bias & SRM?

ok.lets go

Mar 16
Acknowledged user's readiness to commence
Acknowledged user's readiness to commence

You run your Google summary box experiment. Results look great — sessions-per-user up 8%, p < 0.001.

But Control group has 52,000 users and Treatment has 48,000 users. You configured 50/50.

What's wrong and what do you do?

quick clarification: in the beginning you had 50k-50k?

Mar 16

Yes, you configured 50/50 so you expected ~50k in each. You got 52k vs 48k.

What's wrong and what do you do?

not familiar with SRM, can you give me some learning sections written very clearly

i remember we has unbalanced design with weights when I studied analysis of variance. 
or maybe it is kind of attrition?
obviously we are talking about some sort of bias? where the bias is coming from? maybe it is not that bad. the randomization shouldnt be correlated to the users left or came so I woud say we dont have a probelm except from learning power diminshed
Mar 16
Prepared concise SRM explanation for learner
Prepared concise SRM explanation for learner

Good instincts. Now read this, then I'll quiz you.

SRM = Sample Ratio Mismatch

You configured 50/50 but got 52k/48k. That gap is statistically significant → something in the system is wrong.

Why it's serious: The 8% lift is untrustworthy. Full stop. Don't launch.

Common causes:

Cause	Example
Bot filtering	bots filtered differently per variant
Redirect bug	Treatment users redirect → some drop off
Logging bug	Treatment events logged twice
Cache difference	unequal LRU cache hits per variant

Your ANOVA/attrition intuition: yes, it's like attrition — users "leaving" the experiment non-randomly. The randomization was fine at assignment, but something downstream caused differential dropout → the groups are no longer comparable.

What to do:

Do NOT trust results
Investigate cause (check logs, redirects, bots)
Fix and rerun

How to detect: chi-square test on group sizes vs expected ratio.

Now: your experiment has no SRM. But 3 unrelated metrics are significant at p<0.05. Should you be worried?

actually not sure

Mar 16

Multiple testing problem.

If you test 100 metrics, ~5 will be significant by chance alone (5% × 100 = 5 false positives).

Fix — tiered significance:

Metric tier	Threshold
Primary (OEC)	p < 0.05
Secondary (guardrails)	p < 0.01
Everything else	p < 0.001

So 3 random metrics significant at p<0.05 → likely false positives, don't worry unless they're in tier 1 or 2.

Add this to cheatsheet?

yes and go on to next question

Mar 16
Resolved to update materials and advance forward
Resolved to update materials and advance forward

Q029 — You have 2 groups, testing 2 drugs. How do you design the experiment?

Ab cheatsheet
Document · MD 
Download

next question + where are we on the map in terms of progress

Mar 16
Gauged progress status and prepared subsequent inquiry
Gauged progress status and prepared subsequent inquiry

Progress:

	Topic	Status
✅	Design components	Done
✅	Power formula	Done
✅	p-value / practical significance	Done
✅	SRM	Done
✅	Multiple testing	Done
🔲	2 drug experiment (Q029)	Now
🔲	Novelty/primacy effects	Next
🔲	Network interference	After
🔲	Bias / selection bias (Q032)	After
🔲	Mock end-to-end	Tomorrow

Q029:

You have 2 drugs, 2 groups of patients. How do you design the experiment to test effectiveness of both?

my answer

if we had 1 drug we would use control and treatement. 
now since we have 2 drugs we would need to adminster and swap after a week or so. so say y,x the groups and y_week1_week2 are the notation for weeks where 0 is first med and 1 second

y1-x1

Im not sure how to continue now

not as part of the interview 
1. add the different desgin models (different arms, cross overs with pros cons to cheatsheeet as i forgot about them do ti n token efficient manner)
2. please add to the cheat sheet the road map and the checked topic and everytime we check a topic update it in the cheatsheet

Show more
Mar 16
1 / 2
Formulated feedback and orchestrated cheatsheet updates comprehensively
Formulated feedback and orchestrated cheatsheet updates comprehensively

Good instinct — you're describing a crossover design. Let me give quick feedback then update.

Your answer: correct direction. Crossover = each group gets both drugs in sequence. Eliminates between-subject variance.

Missing: you also need a washout period between drugs to avoid carryover effects.

Full answer:

2 drugs + control → 3-arm parallel design (simplest)
Or crossover → A→B vs B→A with washout period in between
Ran a command, created a file, read a file
Ran a command, created a file, read a file

Next: novelty/primacy effects — quick concept then a question. Ready?

Ab cheatsheet
Document · MD 
Download

next question

Mar 16
Identified request for subsequent question on cognitive biases
Identified request for subsequent question on cognitive biases

You launch a new YouTube homepage redesign. After 3 days, engagement is up 15%. Your manager wants to ship it immediately.

What do you tell him?

could be novelty effect lets wait

Mar 16

Correct. How long and how do you confirm it's stabilized?

~2 weks

Mar 16

Correct on timing. But how do you confirm the novelty effect is gone — what do you actually look at?

check if there is spike or a diminishing increase overtime 
use new users without baseline
Mar 16

Score: 3/3

Exactly right.

Plot metric daily — if lift is decreasing over time → novelty effect, wait for stabilization
New users — no prior exposure, no novelty bias → clean signal

Primacy effect is the opposite — users resist change initially, metric looks bad but improves over time. Same fix: wait and plot daily.

Add to cheatsheet + next topic?

ok

Mar 16
Orchestrated resource updates and pivoted toward network analysis
Orchestrated resource updates and pivoted toward network analysis

Network interference:

You're testing a new LinkedIn feature that shows more posts from your connections. You run A/B test. Why might your results be wrong?

Ab cheatsheet
Document · MD 
Download

did you check the cheatsheet?
also are we doing one question per topic. here it was sufficient. but what about other topics.

Mar 16
Thinking about clarifying reference materials and question-per-topic consistency across topics
Thinking about clarifying reference materials and question-per-topic consistency across topics

Fixed. ✅

On your question: yes, one question per topic is enough if you nail it. If you struggle I add more. You've been strong — we'll do 1 each for the remaining 3 topics (network interference, bias, mock), then you're done.

Now answer: why might the LinkedIn A/B test results be wrong?

btw just to clarify. which metric would you like to test here?

Mar 16

Good instinct to clarify — that's exactly what Google wants to see.

For this question the metric doesn't matter — I want to test if you know why the experimental setup itself is broken regardless of metric.

Hint: think about what happens to Control users when their Treatment friends see more posts.

network effect. 

people from a group have correlation with b group

Mar 16

Exactly. Full answer for interview:

"Treatment users see more posts → engage more → generate more content → Control users also see this content → Control is contaminated. The groups aren't independent. We're underestimating the true effect."

This violates SUTVA — Stable Unit Treatment Value Assumption (units must not interfere).

Fix: randomize by cluster (friend groups) not by user.

Ready for bias/selection bias — last topic before mock?

3 / 3

yes

Mar 16

You're analyzing results of your Google summary box experiment. You notice that users who opted in to try the new feature have 20% higher engagement than Control.

What's wrong?

selection bias you selected people that have tendency to engage more with our features

Mar 16

Score: 3/3. Exactly.

Full interview answer:

"Self-selection bias — users who opt in are inherently more engaged. The 20% lift is not caused by the feature, it's a pre-existing difference. You can't establish causality. This is why we randomize — to eliminate selection bias by design."

Key point: this is why observational studies are weaker than RCTs. Randomization is the only way to ensure groups are comparable.

Update roadmap
Update roadmap

All topics done. Mock end-to-end tomorrow?

do it now. if you spot things I'm weak it. mark it on the side so we can focus on them and train me. be honest. help me answer in the right manner

Mar 16
Orchestrated mock interview simulation with feedback tracking
Orchestrated mock interview simulation with feedback tracking

I'm your Google interviewer. No hints, no coaching mid-answer. Answer as if it's real.

Question:

YouTube is considering adding a "Chapters" feature to long videos — clickable timestamps that let users jump to sections.

Design an A/B test to decide whether to launch it.

<thinking-outloud>
what should be our metric of interest. 
overall google wants to profit as company
youtube profits from ads and premium
more sessions, more ads
the more convenient the more users enrolling to premium
so lets say we want to maximize user sessions
maybe i should collect list of metrics so it will be easier for me to retrieve  during interview.

what should be our guardrails? not sure here. maybe users will be able to skip ads the video authors are putting but what damage can it do? there is not other youtube but maybe it will harm somehow

why dont i know to answer this what will happen in the real interview?

i should add because to each component, what because i can add to hypothesis/oec/guardrails

about duration: week will give us the day of week effect, is there primacy or novelty here. I guess so, lets make it 2 weeks
</thinking-outloud>

hypothesis: adding chapters will increase sessions per user without harming ad click per user
oec: sessions per user 
guardrails: ad click per users (users will see less video time and will have less ads)
factorization unit: user id keeps sutva without user bad ux
population: users who viewed long videos in the last 14 days (because we don't want users with dead account)
size: 16*sigma2/delta2. need to figure out our requirements here from management
duration: 2 weeks because of day of week/primacy/novelty effects

Show more
Mar 16
Evaluated experimental design, identified gaps in metrics and guardrails
Evaluated experimental design, identified gaps in metrics and guardrails

Overall: 2.5/3 — solid, hirable answer. Here's the honest breakdown:

✅ Strong:

Hypothesis clean and testable
SUTVA mention → impressive
Power formula + duration reasoning correct
Guardrail instinct good

⚠️ Weaknesses to fix:

Issue	What you said	Better
OEC	sessions-per-user	watch-time-per-user — more direct for YouTube chapters
Population	"last 14 days"	users who watched a video >10min — triggered analysis, only users who could benefit from chapters
Guardrails incomplete	ad clicks only	add ad revenue-per-user + video completion rate
Missing	nothing said	practical significance boundary — "we care if δ > X%"

Biggest gap: population definition. "Last 14 days" is arbitrary and doesn't use triggered analysis logic.

Things to drill before tomorrow:

 Always define population as "users who could be affected by the feature"
 For YouTube → default OEC = watch-time-per-user
 Always state practical significance boundary explicitly

Want to redo population + OEC in one sentence?

answer very very very clearly and shortly cause i didn udnerstand: what is the Missing "practical significance boundary — "we care if δ > X%"
add to cheatsheet list of metrics for different google products
what should I improve in my outloud thinking?
Mar 16

1. Practical significance boundary:

Before running, decide: "what's the minimum effect that matters to us businesswise?"

Example: "We only care if watch-time increases by ≥1%. Smaller than that — not worth the engineering cost."

You never stated this. In interview say it explicitly.

2 & 3 — doing now:

Ran a command, read a file
Ran a command, read a file

3. Your think-out-loud — what to fix:

✅ Good: questioning the metric, thinking about tradeoffs
❌ Missing: never stated practical significance boundary
❌ Too vague on population — "last 14 days" has no causal logic
❌ Guardrails: only one, think harder about what the feature could break

Rule: for every component ask yourself "what could go wrong here?"

Ab cheatsheet
Document · MD 
Download

how exactly should I state it. i dont know it

Mar 16

You don't know the exact number — that's fine. You ask:

"What's the minimum lift that justifies the engineering cost of this feature?"

Then in interview say:

"I'd work with the team to define practical significance — for YouTube at scale I'd guess ≥1% lift in watch-time is our bar. I'd use that as δ in the power analysis."

Formula connection:

You just defined δ
Plug into n ≈ 16σ²/δ²
Done

You never need to know the exact number. You just need to show you know it's required.

does this mock interivew represents the entire ab -testing material for my google interview?

Mar 16

Mostly yes, but 3 gaps remain:

Covered ✅

Full design (all components)
Power + sample size
p-value, CI, Type I/II
Practical vs statistical significance
SRM
Multiple testing
Experiment designs (multi-arm, crossover)
Novelty/primacy effects
Network interference / SUTVA
Selection bias
Triggered analysis

Not covered ⚠️

Topic	Likelihood in Google interview
CUPED / variance reduction	Medium — PhD level
Long-term holdout design	Low
Bayesian A/B testing	Low

Verdict: for a DS (non-research) role you're covered. If it's a research/PhD-level role, CUPED could come up.

Want a quick CUPED explainer?

i want to cover them
more important in the mock interivew you did now most topics didnt show. I worry I'm not ready yet
Mar 16
Reconciled coverage gaps and fortified mock interview comprehensiveness
Reconciled coverage gaps and fortified mock interview comprehensiveness

On the mock: you're right. One question can't cover everything. We need a multi-question mock like the real interview.

Plan:

Quick CUPED + long-term holdout + Bayesian explainers (15 min)
Full mock — 4-5 questions hitting all topics
I flag every weakness

Which first?

Q: What do you want to do first?
A: Jump straight to full mock, learn gaps as they appear

Mar 16
Architected comprehensive mock interview spanning discussed topics
Architected comprehensive mock interview spanning discussed topics

Full mock. I'm your Google interviewer. No hints.

Q1:

Google Maps is testing a new feature that suggests real-time parking spots near your destination.

Design an A/B test.

wait lets add to the md cheat sheet Components
also gotchas component. handling edge cases (product sense)

Mar 16
Recognized user's intent to expand cheatsheet before proceeding
Recognized user's intent to expand cheatsheet before proceeding

Done. Now — Google Maps parking feature. Design the A/B test.

Ab cheatsheet
Document · MD 
Download

ok but we make sure we test all componenets int his mock right? do you want to create tasklist/plan to make sure?

Mar 16

Yes. Here's the plan:

Q	Topic tested
Q1 — Maps parking	Full design (all components)
Q2 — Ambiguous metric	Practical significance + launch decision
Q3 — Buggy results	SRM + trust
Q4 — Social feature	SUTVA + network interference
Q5 — Surprising result	Multiple testing + novelty
Q6 — Two treatments	Multi-arm + power

After each I score you and flag weaknesses. At the end — overall verdict.

Q1: Google Maps parking feature. Go.

wait does this include CUPED, bayesian ab test and holdout?
also make sure you flag weaknesses so we can iterate until perfect score

Mar 16
Reconciled testing methodologies and flagged improvement areas
Reconciled testing methodologies and flagged improvement areas

Good catch. Updated plan:

Q	Topic tested
Q1 — Maps parking	Full design (all components)
Q2 — Ambiguous metric	Practical significance + launch decision
Q3 — Buggy results	SRM + trust
Q4 — Social feature	SUTVA + network interference
Q5 — Surprising result	Multiple testing + novelty
Q6 — Two treatments	Multi-arm + power
Q7 — Variance too high	CUPED
Q8 — Long running test	Holdout design
Q9 — Prior beliefs	Bayesian A/B

For each question: you answer → I score → we iterate until 3/3 → next question.

Q1: Google Maps parking feature. Go.

can you shrink it to have same topic coverage in less questions? questions that truely simulate ds interview

Mar 16
Restructured interview questions for denser topic coverage
Restructured interview questions for denser topic coverage
Q	Topics covered
Q1 — Maps parking	Full design + triggered analysis + practical significance
Q2 — Social feature + weird results	SUTVA + SRM + multiple testing + launch decision
Q3 — Two drugs + high variance	Multi-arm + crossover + CUPED + power
Q4 — YouTube redesign	Novelty + primacy + holdout + Bayesian

4 questions, full coverage, each multi-layered like real Google interviews.

Q1: Go.

<thinking>
the questions Google Maps is testing a new feature that suggests real-time parking spots near your destination.

about guardrails. what can affect the user? it can add latency? make ux more complex but to measure it here? not sure

<thinking>

Clarify the Goal & Hypothesis goal: improve user experience and value by helping users find parking spots and save time

hypothesis: increase session per users, route completions
guardrails:  not sure
oec:   session per users
populations: all maps users
duration: 2 weeks novelty primacy day of week effects

gotachs: not sure

Show more
Mar 16
Identified critical gaps in experimental design and metrics
Identified critical gaps in experimental design and metrics

Score: 1.5/3 — several gaps. Let's fix one by one.

❌ Gap 1 — OEC wrong Sessions-per-user doesn't capture if parking feature helped. Better:

route completions per user or navigation sessions per user

Fix it in one sentence.

2 / 2

you give me the answer what does it helped me to tell you repeat you

Mar 16

You're right.

Hint only: think about what the user's goal is when they open Maps for a trip. What's the one action that means "this worked"?

i dont understand. you want me to answer the "route complete answer as it is written in front of my eyes?

Mar 16

Fair point. Let me just flag all gaps, then you redo the full answer from scratch without looking.

Gaps:

OEC — sessions-per-user doesn't measure parking success
Population — too broad, not triggered
Guardrails — you said "not sure" — think: latency, session length, crash rate
Practical significance — never stated
Gotchas — missed: not all users drive/need parking

Close this chat window, redo the full answer from memory. Then paste it here.

show me the correct answer and ask me another one in the same style and i will answer, if not answering 3/3 you will ask me another and we do it until I master the what q1 covers

now go ahead and show me what I answered vs what is right in easy nice to read way

5:02 PM
2 / 2
Architected visual comparison widget for answer feedback
Architected visual comparison widget for answer feedback

Now — same topics, new scenario:

Google Drive is testing a feature that auto-suggests file names when you create a new document.

Design the A/B test.




Sonnet 4.6
Extended
Claude is AI and can make mistakes. Please double-check responses.
Share
Content

PDF

ab_concrete_2day.html

HTML

ab-testing.md

17 lines

MD