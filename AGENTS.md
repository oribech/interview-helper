# Interview Helper — Real-Time AI Interview Assistant

Listens to mic audio, transcribes in real-time, and maintains a **scratchpad** that an LLM (Claude or Gemini) continuously updates with concise answer hints.

## Quick Start

```bash
# Install deps
uv venv && uv pip install -r requirements.txt

# Run
uv run python main.py
# Open: http://localhost:8888
```

## Structure

```
main.py              # Orchestrator — audio → brain → LLM → display
src/
  audio.py           # Mic capture via RealtimeSTT + faster-whisper
  brain.py           # Transcript accumulator + debounced LLM trigger
  llm.py             # LLM subprocess wrapper (Claude CLI + Gemini CLI)
  display.py         # HTTP/WebSocket server + scratchpad overlay HTML
tests/
  test_demo.py       # Demo tests with mocked LLM
google/              # Study materials (read-only source)
```

## How It Works

1. **Audio** → RealtimeSTT transcribes mic in real-time
2. **Brain** → accumulates transcript, triggers LLM every ~3s (skips if busy)
3. **LLM** → receives current scratchpad + transcript → returns updated scratchpad
4. **Display** → WebSocket pushes full scratchpad to browser (replaces in-place)

## UI Controls

The browser overlay includes dropdowns for:
- **Model** — Claude (Sonnet 4.6, Opus 4.6, Haiku 4.5) or Gemini (3 Flash, 3.1 Pro)
- **Effort** — Low / Medium / High (Claude only; hidden for Gemini)

Settings are sent to the server via WebSocket and take effect on the next LLM call.

## Scratchpad Rules

- MAX 8 bullet points
- Each bullet ≤15 words, keyword-dense
- ⚡ prefix for most urgent point
- **Bold** key terms, numbers; formulas in LaTeX (`$...$`)
- Stale bullets removed when topic changes

## Changelog

After every code modification, append an entry to `CHANGELOG.md` using concise [Conventional Commits](https://www.conventionalcommits.org/) format:

```
## YYYY-MM-DD
- fix(scope): short description
- feat(scope): short description
- test(scope): short description
- refactor(scope): short description
```

One line per change. Group by date. Scope = affected module (brain, llm, display, tests, etc.).

## Conventions

- Python: `uv run python <file>`
- LLM CLI: `claude -p <prompt> --model <model>` or `gemini -m <model>` (stdin) via subprocess
- Display: aiohttp WebSocket on port 8888, KaTeX for LaTeX rendering
- Tests: `uv run python -m tests.test_demo`
