"""Simple index-based wiki search.

Searches the pre-compiled wiki for relevant pages matching a query.
Uses the index.md file for navigation — no embedding DB needed.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple


WIKI_DIR = Path(__file__).parent.parent / "wiki"
INDEX_FILE = WIKI_DIR / "index.md"
TOPICS_DIR = WIKI_DIR / "topics"


def load_index() -> List[Tuple[str, str, str]]:
    """
    Parse wiki/index.md and return list of (title, filename, summary).
    Expected index format per line:
        - [Title](topics/filename.md) — summary text
    """
    if not INDEX_FILE.exists():
        return []

    entries = []
    pattern = re.compile(r"-\s*\[(.+?)\]\((.+?)\)\s*[—-]\s*(.+)")

    for line in INDEX_FILE.read_text().splitlines():
        m = pattern.match(line.strip())
        if m:
            title, filepath, summary = m.group(1), m.group(2), m.group(3)
            entries.append((title, filepath, summary.strip()))

    return entries


def search_wiki(query: str, max_results: int = 3) -> str:
    """
    Search wiki for pages relevant to the query.
    Returns concatenated content of matching pages.

    Simple keyword matching against titles and summaries.
    """
    entries = load_index()
    if not entries:
        return ""

    query_lower = query.lower()
    query_words = set(re.findall(r'\w+', query_lower))

    # Score each entry by keyword overlap
    scored = []
    for title, filepath, summary in entries:
        entry_text = f"{title} {summary}".lower()
        entry_words = set(re.findall(r'\w+', entry_text))
        overlap = len(query_words & entry_words)
        if overlap > 0:
            scored.append((overlap, title, filepath))

    # Sort by score descending, take top results
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:max_results]

    if not top:
        return ""

    # Read and concatenate matching pages
    parts = []
    for score, title, filepath in top:
        full_path = WIKI_DIR / filepath
        if full_path.exists():
            content = full_path.read_text()
            parts.append(f"## {title}\n{content}")

    return "\n\n---\n\n".join(parts)
