#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path('/Users/oribecher/Projects/interview-helper')
DB = ROOT / 'poc' / 'retrieval' / 'index.db'


def excerpt(text: str, limit: int = 240) -> str:
    text = ' '.join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + '…'


def fts_query(text: str) -> str:
    tokens = re.findall(r"[A-Za-z0-9_]+", text.lower())
    if not tokens:
        return '""'
    return ' OR '.join(dict.fromkeys(tokens))


def query_db(query: str, top_k: int, db_path: Path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    match_query = fts_query(query)
    rows = conn.execute(
        "SELECT snippet_id, source_path, title, body, topic, bm25(snippets) AS score FROM snippets WHERE snippets MATCH ? ORDER BY score LIMIT ?",
        (match_query, top_k),
    ).fetchall()
    conn.close()
    return [
        {
            'snippet_id': row['snippet_id'],
            'source_path': row['source_path'],
            'title': row['title'],
            'topic': row['topic'],
            'score': row['score'],
            'snippet': excerpt(row['body']),
        }
        for row in rows
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', required=True)
    parser.add_argument('--top-k', type=int, default=4)
    parser.add_argument('--db', type=Path, default=DB)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    results = query_db(args.query, args.top_k, args.db)
    payload = {'query': args.query, 'results': results}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False))
    else:
        for item in results:
            print(f"[{item['score']:.2f}] {item['title']} :: {item['snippet']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
