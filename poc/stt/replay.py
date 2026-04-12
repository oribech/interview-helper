#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

from event_bridge import post_event
from transcribe import transcribe_audio
from vad import is_likely_question

ROOT = Path('/Users/oribecher/Projects/interview-helper')
RUNS = ROOT / 'poc' / 'runs'
SCENARIO = ROOT / 'poc' / 'scenarios' / 'basic-ab-test' / 'scenario.json'
VOICE = 'Samantha'


def generate_turn_audio(text: str, out_wav: Path) -> None:
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    aiff_path = out_wav.with_suffix('.aiff')
    subprocess.run(['say', '-v', VOICE, '-o', str(aiff_path), text], check=True)
    subprocess.run(['ffmpeg', '-y', '-i', str(aiff_path), '-ar', '16000', '-ac', '1', str(out_wav)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    aiff_path.unlink(missing_ok=True)


def fetch_json(url: str):
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode('utf-8'))


def post_json(url: str, payload: dict):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))


def emit_partial_updates(server: str, chat_id: str, speaker: str, text: str) -> None:
    words = text.split()
    if len(words) < 6:
        return
    cut_points = sorted({max(3, len(words) // 2), max(4, int(len(words) * 0.8))})
    for cut in cut_points:
        partial_text = ' '.join(words[:cut]).strip()
        post_event(server, {
            'type': 'transcript.partial',
            'chat_id': chat_id,
            'speaker_guess': speaker,
            'text': partial_text,
            'source': 'replay',
            'ts': datetime.now().isoformat(),
        })
        if speaker == 'interviewer':
            post_event(server, {
                'type': 'question.update',
                'chat_id': chat_id,
                'speaker_guess': speaker,
                'text': partial_text,
                'source': 'replay',
                'ts': datetime.now().isoformat(),
            })
        time.sleep(0.6)


def reset_chat(server: str, chat_id: str) -> None:
    post_json(server.rstrip('/') + '/reset', {'chat_id': chat_id})


def wait_for_version(server: str, min_version: int, timeout_s: float) -> dict:
    deadline = time.time() + timeout_s
    last_state = fetch_json(server.rstrip('/') + '/state')
    while time.time() < deadline:
        last_state = fetch_json(server.rstrip('/') + '/state')
        if int(last_state.get('version', 0)) >= min_version and last_state.get('last_event_type') == 'reply':
            return last_state
        time.sleep(0.5)
    return last_state


def main() -> int:
    parser = argparse.ArgumentParser(description='Replay a spoken interview scenario into the local scratchpad channel.')
    parser.add_argument('--scenario', type=Path, default=SCENARIO)
    parser.add_argument('--server', default='http://127.0.0.1:8788')
    parser.add_argument('--delay', type=float, default=20.0)
    parser.add_argument('--no-reset', action='store_true')
    args = parser.parse_args()

    scenario = json.loads(args.scenario.read_text(encoding='utf-8'))
    chat_id = scenario.get('chat_id', 'interview-1')
    run_dir = RUNS / f"replay-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / 'scenario.json').write_text(json.dumps(scenario, indent=2), encoding='utf-8')
    if not args.no_reset:
        reset_chat(args.server, chat_id)
    latest_state = fetch_json(args.server.rstrip('/') + '/state')

    for idx, turn in enumerate(scenario['turns'], start=1):
        wav_path = run_dir / f'turn-{idx:02d}-{turn["speaker"]}.wav'
        generate_turn_audio(turn['text'], wav_path)
        transcript = transcribe_audio(wav_path)
        emit_partial_updates(
            server=args.server,
            chat_id=chat_id,
            speaker=turn['speaker'],
            text=turn['text'],
        )
        post_event(args.server, {
            'type': 'transcript.final',
            'chat_id': chat_id,
            'speaker_guess': turn['speaker'],
            'text': transcript,
            'source': 'replay',
            'ts': datetime.now().isoformat(),
        })
        if turn['speaker'] == 'interviewer' and is_likely_question(transcript):
            previous_version = int(latest_state.get('version', 0))
            post_event(args.server, {
                'type': 'question.pause',
                'chat_id': chat_id,
                'speaker_guess': turn['speaker'],
                'text': transcript,
                'source': 'replay',
                'ts': datetime.now().isoformat(),
            })
            target_version = previous_version + 1
            latest_state = wait_for_version(args.server, target_version, args.delay)
        else:
            time.sleep(1.0)
            latest_state = fetch_json(args.server.rstrip('/') + '/state')
        state = latest_state
        (run_dir / f'state-after-turn-{idx:02d}.json').write_text(json.dumps(state, indent=2), encoding='utf-8')
        print(f'Turn {idx}: {turn["speaker"]}\n  source : {turn["text"]}\n  heard  : {transcript}\n  status : {state["status"]}\n  answer : {state["short_answer"]}\n')
    print(f'Replay artifacts written to {run_dir}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
