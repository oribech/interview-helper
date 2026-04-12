#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path('/Users/oribecher/Projects/interview-helper')
SOURCE = ROOT / 'google'
OUT = ROOT / 'poc' / 'retrieval' / 'wiki'


def clean_text(text: str) -> str:
    text = text.replace('\r', '')
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith('#'):
            return line.lstrip('#').strip()
    return fallback


def convert_file(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding='utf-8', errors='ignore')
    text = clean_text(text)
    title = first_heading(text, path.stem.replace('-', ' '))
    body = f'# {title}\n\nSource: {path.relative_to(ROOT)}\n\n{text}\n'
    return title, body


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--out', type=Path, default=OUT)
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(args.source.rglob('*')):
        if not path.is_file() or path.suffix.lower() not in {'.md', '.txt'}:
            continue
        rel = path.relative_to(args.source)
        out_path = args.out / rel.with_suffix('.md')
        out_path.parent.mkdir(parents=True, exist_ok=True)
        _, body = convert_file(path)
        out_path.write_text(body, encoding='utf-8')
        count += 1
    print(f'Wrote {count} wiki files to {args.out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
