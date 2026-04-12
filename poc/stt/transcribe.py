#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path('/Users/oribecher/Projects/interview-helper')
MODEL = ROOT / 'poc' / 'stt' / 'models' / 'ggml-tiny.en.bin'


def transcribe_audio(audio_path: Path, model_path: Path = MODEL) -> str:
    cli = shutil.which('whisper-cli')
    if not cli:
        raise RuntimeError('whisper-cli not found in PATH')
    if not model_path.exists():
        raise RuntimeError(f'Model not found: {model_path}')
    with tempfile.TemporaryDirectory() as tmpdir:
        prefix = Path(tmpdir) / 'out'
        cmd = [
            cli,
            '-m', str(model_path),
            '-f', str(audio_path),
            '-l', 'en',
            '-nt',
            '-np',
            '-of', str(prefix),
            '-otxt',
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out_file = prefix.with_suffix('.txt')
        return out_file.read_text(encoding='utf-8', errors='ignore').strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('audio', type=Path)
    parser.add_argument('--model', type=Path, default=MODEL)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    text = transcribe_audio(args.audio, args.model)
    if args.json:
        print(json.dumps({'audio': str(args.audio), 'text': text}, ensure_ascii=False))
    else:
        print(text)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
