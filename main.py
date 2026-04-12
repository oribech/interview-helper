"""Orchestrator — starts all components.

Usage:
    uv run python main.py [--port 8888] [--model small]

Components started:
    1. Display server (HTTP + WebSocket on port 8888)
    2. Audio transcriber (mic → text)
    3. Brain (question detection → Claude → display)
"""

import argparse
import asyncio
import signal
import sys

from src.audio import AudioTranscriber
from src.brain import Brain
from src.display import (
    send_answer_chunk,
    send_answer_done,
    send_question,
    send_transcript,
    start_server,
)
from src.llm import ask_claude_streaming, build_prompt
from src.wiki_search import search_wiki


def main():
    parser = argparse.ArgumentParser(description="Real-Time AI Interview Helper")
    parser.add_argument("--port", type=int, default=8888, help="Server port (default: 8888)")
    parser.add_argument("--model", type=str, default="small", help="Whisper model (tiny/base/small/medium/large)")
    parser.add_argument("--language", type=str, default="en", help="Language code (default: en)")
    args = parser.parse_args()

    # --- Callbacks wired together ---

    def on_question_detected(question: str, context: str):
        """Brain detected a question → search wiki → ask Claude → stream to display."""
        # 1. Notify display
        send_question(question)

        # 2. Search wiki for relevant context
        wiki_context = search_wiki(question)

        # 3. Build prompt
        prompt = build_prompt(question, context, wiki_context or None)

        # 4. Stream Claude's answer to display
        ask_claude_streaming(
            prompt=prompt,
            on_chunk=send_answer_chunk,
            on_done=send_answer_done,
        )

    def on_transcript(text: str):
        """Final transcript chunk from audio → feed to brain."""
        brain.add_text(text)

    def on_realtime_transcript(text: str):
        """Partial transcript → update ticker on display."""
        send_transcript(text)

    # --- Initialize components ---

    brain = Brain(on_question=on_question_detected)

    audio = AudioTranscriber(
        on_text=on_transcript,
        on_realtime_text=on_realtime_transcript,
        model=args.model,
        language=args.language,
    )

    # --- Run ---

    async def run():
        # Start web server
        runner = await start_server(port=args.port)

        # Start audio in background thread
        audio.start()

        print(f"\n{'='*50}")
        print(f"  Interview Helper is LIVE")
        print(f"  Open: http://localhost:{args.port}")
        print(f"  Model: {args.model} | Language: {args.language}")
        print(f"{'='*50}\n")

        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, asyncio.CancelledError):
            pass
        finally:
            audio.stop()
            await runner.cleanup()
            print("\n[Main] Shutdown complete.")

    # Handle Ctrl+C gracefully
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\n[Main] Interrupted. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
