"""Orchestrator — starts all components (scratchpad mode).

Usage:
    uv run python main.py [--port 8888] [--model small]

Flow:
    Audio → Brain (accumulate, debounce) → Claude (update scratchpad) → Display
"""

import argparse
import asyncio
import sys
import time

from src.audio import AudioTranscriber
from src.brain import Brain
from src.display import (
    get_settings,
    send_error,
    send_scratchpad,
    send_transcript,
    send_updating,
    set_on_settings_change,
    set_on_stt_change,
    start_server,
)
from src.llm import build_scratchpad_prompt, update_scratchpad, warmup_claude



# Server-side scratchpad state
_current_scratchpad: str = ""


def main():
    parser = argparse.ArgumentParser(description="Real-Time AI Interview Helper")
    parser.add_argument("--port", type=int, default=8888, help="Server port")
    parser.add_argument("--model", type=str, default="small", help="Whisper model size")
    parser.add_argument("--language", type=str, default="en", help="Language code")
    args = parser.parse_args()

    # --- Callbacks ---

    def on_brain_update(new_text: str, full_context: str):
        """Brain has new transcript → ask Claude to update scratchpad."""
        global _current_scratchpad

        t_start = time.perf_counter()
        brain.set_busy(True)
        send_updating()

        # Build prompt
        t_prompt = time.perf_counter()
        prompt = build_scratchpad_prompt(
            current_scratchpad=_current_scratchpad,
            transcript=full_context,
        )
        print(f"[Timing] Prompt build: {(time.perf_counter() - t_prompt)*1000:.0f}ms  (prompt length: {len(prompt)} chars)")

        def on_result(new_pad: str):
            global _current_scratchpad
            t_total = (time.perf_counter() - t_start) * 1000
            _current_scratchpad = new_pad
            send_scratchpad(new_pad)
            brain.set_busy(False)
            print(f"[Timing] Total brain→result: {t_total:.0f}ms")
            print(f"[Main] Scratchpad updated ({len(new_pad)} chars)")

        def on_llm_error(err: str):
            t_total = (time.perf_counter() - t_start) * 1000
            send_error(err)
            brain.set_busy(False)
            print(f"[Timing] Total brain→error: {t_total:.0f}ms")
            print(f"[Main] LLM error: {err}")

        settings = get_settings()
        print(f"[Timing] Settings: model={settings['model']}, effort={settings['effort']}")
        update_scratchpad(
            prompt=prompt,
            on_result=on_result,
            on_error=on_llm_error,
            model=settings["model"],
            effort=settings["effort"],
        )

    def on_transcript(text: str):
        """Final transcript chunk from audio → feed to brain."""
        brain.add_text(text)

    def on_realtime_transcript(text: str):
        """Partial transcript → update ticker on display."""
        send_transcript(text)

    def on_settings_change(settings: dict):
        """Warm the selected Claude model in the background."""
        warmup_claude(settings["model"], settings["effort"])

    # --- Components ---

    brain = Brain(
        on_update=on_brain_update,
        min_interval_seconds=1.5,
    )

    audio = AudioTranscriber(
        on_text=on_transcript,
        on_realtime_text=on_realtime_transcript,
        model=args.model,
        language=args.language,
    )

    # --- Run ---

    async def run():
        runner = await start_server(port=args.port)
        set_on_settings_change(on_settings_change)
        set_on_stt_change(lambda model: audio.change_model(model))
        warmup_claude(get_settings()["model"], get_settings()["effort"])
        audio.start()

        print(f"\n{'='*50}")
        print(f"  Interview Helper — SCRATCHPAD MODE")
        print(f"  Open: http://localhost:{args.port}")
        print(f"  Model: {args.model} | Language: {args.language}")
        print(f"{'='*50}\n")

        try:
            while True:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, asyncio.CancelledError):
            pass
        finally:
            audio.stop()
            await runner.cleanup()
            print("\n[Main] Shutdown complete.")

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\n[Main] Interrupted. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
