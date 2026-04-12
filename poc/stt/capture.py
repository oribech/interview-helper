#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description='Capture room audio from the default macOS input using ffmpeg segment files.')
    parser.add_argument('--out-dir', type=Path, default=Path('/tmp/interview-capture'))
    parser.add_argument('--segment-seconds', type=int, default=4)
    parser.add_argument('--device', default=':0')
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    output_pattern = str(args.out_dir / 'segment-%04d.wav')
    cmd = [
        'ffmpeg', '-hide_banner', '-loglevel', 'info',
        '-f', 'avfoundation', '-i', args.device,
        '-ac', '1', '-ar', '16000',
        '-f', 'segment', '-segment_time', str(args.segment_seconds), '-reset_timestamps', '1',
        output_pattern,
    ]
    print('Running:', ' '.join(cmd))
    print('Note: this is a simple capture helper. Pair it with transcribe.py + event_bridge.py in a supervising loop.')
    subprocess.run(cmd, check=False)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
