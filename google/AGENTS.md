# AGENTS.md

Google Data Scientist interview prep. Deadline: 2026-03-31.

## Structure

```
position/       Job description + cover letter
books/          Reference PDFs + markdown extracts (canonical copies — no duplicates elsewhere)
research/       External intel: Reddit, Glassdoor, recruiter materials, deep research
  reddit/       Reddit/blog sources
  provided-materials/  Recruiter-provided prep info
questions/      Glassdoor question bank split by topic (README.md has index)
study/          Study notes, cheatsheets, practice code, notebooks — by topic
  ab-testing/   A/B testing (sprint plan, notes, ab_lab/ code, quiz, notebook)
  stats-probability/  Stats & probability (cheatsheet, patterns, mock results, PCA notebook)
  ml-llm-eval/  ML + LLM evaluation (cheatsheet, transformer notes, BLEU, eval metrics)
  times.csv     Study time tracker data
  time_tracker.* Time tracker UI + script
```

## Key Files

- `PLAN.md` — master study plan (5 topics, hour allocations)
- `questions/README.md` — index mapping Q001-Q118 to topic files
- `books/ace-ds-interivew.md` — single canonical copy (do NOT duplicate into study/ folders)
- `questions/ml-llm-eval.md` — single canonical copy (do NOT duplicate)
- `study/ab-testing/ab-testing-2-day-sprint.md` — structured 2-day A/B testing study plan
- `study/ab-testing/ab_subset_quiz.py` — runnable quiz: `uv run python study/ab-testing/ab_subset_quiz.py`

## Conventions

- Internal links use absolute paths (`/Users/oribecher/Projects/private/job_interview/positions/google/...`)
- Python: run with `uv run python <file>`
- No file duplication — books/ and questions/ hold canonical copies, study/ folders reference them
- `research/` = external sources; `study/` = personal notes and practice
