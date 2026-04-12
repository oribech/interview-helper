#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sqlite3
from pathlib import Path

ROOT = Path('/Users/oribecher/Projects/interview-helper')
WIKI = ROOT / 'poc' / 'retrieval' / 'wiki'
DB = ROOT / 'poc' / 'retrieval' / 'index.db'


def chunk_text(text: str, target: int = 1200) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    chunks: list[str] = []
    current: list[str] = []
    size = 0
    for para in paragraphs:
        if current and size + len(para) > target:
            chunks.append('\n\n'.join(current))
            current = []
            size = 0
        current.append(para)
        size += len(para)
    if current:
        chunks.append('\n\n'.join(current))
    return chunks or [text[:target]]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--wiki', type=Path, default=WIKI)
    parser.add_argument('--db', type=Path, default=DB)
    args = parser.parse_args()

    args.db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(args.db)
    conn.execute('DROP TABLE IF EXISTS snippets')
    conn.execute("CREATE VIRTUAL TABLE snippets USING fts5(snippet_id UNINDEXED, source_path UNINDEXED, title, body, topic, tokenize='porter unicode61 remove_diacritics 2')")

    count = 0
    for path in sorted(args.wiki.rglob('*.md')):
        text = path.read_text(encoding='utf-8', errors='ignore').strip()
        if not text:
            continue
        title = text.splitlines()[0].lstrip('#').strip() if text.startswith('#') else path.stem
        topic = path.parts[-2] if len(path.parts) > 1 else 'general'
        for idx, chunk in enumerate(chunk_text(text)):
            snippet_id = f'{path.relative_to(args.wiki)}#{idx + 1}'
            conn.execute(
                'INSERT INTO snippets (snippet_id, source_path, title, body, topic) VALUES (?, ?, ?, ?, ?)',
                (snippet_id, str(path.relative_to(ROOT)), title, chunk, topic),
            )
            count += 1
    conn.commit()
    conn.close()
    print(f'Indexed {count} snippets into {args.db}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
