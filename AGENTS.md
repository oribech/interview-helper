# Interview Helper — Real-Time AI Interview Assistant

Listens to interview audio via mic, detects questions, sends to Claude, displays answers on a browser overlay.

## Quick Start

```bash
# Install deps
uv pip install -r requirements.txt

# Start the helper
uv run python main.py

# Open overlay
open http://localhost:8888
```

## Structure

```
main.py              # Orchestrator — starts all components
src/
  audio.py           # Mic capture + RealtimeSTT transcription
  brain.py           # Question detector + rolling context window
  llm.py             # Claude CLI subprocess wrapper
  display.py         # HTTP/WebSocket server + overlay HTML
  wiki_search.py     # Simple index-based wiki search
wiki/                # Pre-compiled knowledge base (Karpathy pattern)
  index.md           # Page catalog
  topics/            # Topic pages compiled from study materials
google/              # Existing study materials (read-only source)
```

## Conventions

- Python: run with `uv run python <file>`
- Claude CLI: called via subprocess (no SDK)
- Wiki: pre-compiled markdown, searched via index — no embedding DB
- Display: aiohttp WebSocket server on port 8888
- Audio: RealtimeSTT with faster-whisper (local, no API keys)
