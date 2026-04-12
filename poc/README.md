# Interview scratchpad PoC

## What this implements
- A local Claude Code channel server that hosts a live web scratchpad UI.
- A retrieval pipeline over `/Users/oribecher/Projects/interview-helper/google/`.
- A replay harness that generates spoken turns with macOS `say`, transcribes them with `whisper.cpp`, and feeds them into the channel.
- A room-audio capture helper for live PoC testing on a separate sidecar machine.

## One-time setup
```bash
cd /Users/oribecher/Projects/interview-helper
python3 poc/retrieval/build_wiki.py
python3 poc/retrieval/build_index.py
brew install whisper-cpp
mkdir -p poc/stt/models
curl -L https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin -o poc/stt/models/ggml-tiny.en.bin
cd poc/channel && bun install
claude mcp add-json -s local interview_sidecar '{"command":"bun","args":["run","/Users/oribecher/Projects/interview-helper/poc/channel/src/channel.ts"],"cwd":"/Users/oribecher/Projects/interview-helper/poc/channel","env":{"INTERVIEW_PROJECT_ROOT":"/Users/oribecher/Projects/interview-helper","INTERVIEW_CHANNEL_PORT":"8788","INTERVIEW_TRACE_DIR":"/Users/oribecher/Projects/interview-helper/poc/runs"}}'
```

## Start the Claude-side session
```bash
cd /Users/oribecher/Projects/interview-helper
expect /Users/oribecher/Projects/interview-helper/poc/run_claude_sidecar.expect
```

This auto-confirms the local development-channel warning and seeds Claude with the scratchpad behavior prompt.

## Run the replay PoC
```bash
python3 /Users/oribecher/Projects/interview-helper/poc/stt/replay.py --delay 20
```

Open [http://127.0.0.1:8788](http://127.0.0.1:8788).

## Live room-audio helper
For a real mic on the sidecar computer:
```bash
python3 /Users/oribecher/Projects/interview-helper/poc/stt/capture.py --out-dir /tmp/interview-capture
```

This currently records rolling WAV segments. Pair it with `transcribe.py` + `event_bridge.py` in a supervising loop for live use.
