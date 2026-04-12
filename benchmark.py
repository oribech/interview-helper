"""Benchmark — measure end-to-end latency of each pipeline stage.

Usage:
    uv run python benchmark.py
"""

import time
import sys

from src.llm import build_scratchpad_prompt, _claude_proc, _call_gemini

PROMPT_TEXT = "What is the probability of getting a king and a queen from a deck of cards without replacement?"

MODELS = [
    ("claude-sonnet-4-6", "low"),
    ("claude-sonnet-4-6", "low"),      # 2nd call — should be fast (warm)
    ("claude-sonnet-4-6", "low"),      # 3rd call
    ("claude-haiku-4-5-20251001", "low"),  # model switch — restarts process
    ("claude-haiku-4-5-20251001", "low"),  # 2nd call — warm again
    ("gemini-3.1-flash-lite-preview", "medium"),
    ("gemini-3-flash-preview", "medium"),
]


def main():
    prompt = build_scratchpad_prompt("(empty)", PROMPT_TEXT)

    print("=" * 65)
    print("  PIPELINE BENCHMARK — Persistent Claude vs One-Shot Gemini")
    print("=" * 65)
    print(f"  Prompt: \"{PROMPT_TEXT[:55]}...\"")
    print(f"  Prompt length: {len(prompt)} chars")
    print()

    results = []
    for model, effort in MODELS:
        is_gemini = model.startswith("gemini")
        provider = "Gemini" if is_gemini else "Claude"
        label = f"{provider} {model}"
        if not is_gemini:
            label += f" (effort={effort})"

        print(f"  {label}...", end="", flush=True)
        t0 = time.perf_counter()
        try:
            if is_gemini:
                output = _call_gemini(prompt, model, timeout=60)
            else:
                output = _claude_proc.send(prompt, model, effort, timeout=60)
            elapsed = time.perf_counter() - t0
            results.append({"label": label, "time_s": round(elapsed, 2), "ok": True, "chars": len(output)})
            print(f" {elapsed:.2f}s ({len(output)} chars)")
        except Exception as e:
            elapsed = time.perf_counter() - t0
            results.append({"label": label, "time_s": round(elapsed, 2), "ok": False, "error": str(e)[:40]})
            print(f" FAILED ({elapsed:.2f}s): {e}")

    # Cleanup
    _claude_proc.kill()

    # Summary
    print()
    print("=" * 65)
    print(f"  {'Model':<45} {'Time':>7}  Status")
    print("-" * 65)
    for r in results:
        status = f"OK ({r['chars']} chars)" if r["ok"] else f"ERR: {r.get('error', '?')}"
        print(f"  {r['label']:<45} {r['time_s']:>6}s  {status}")
    print("=" * 65)

    ok_results = [r for r in results if r["ok"]]
    if ok_results:
        fastest = min(ok_results, key=lambda r: r["time_s"])
        slowest = max(ok_results, key=lambda r: r["time_s"])
        print(f"\n  Fastest: {fastest['label']} at {fastest['time_s']}s")
        print(f"  Slowest: {slowest['label']} at {slowest['time_s']}s")
    print()


if __name__ == "__main__":
    main()
