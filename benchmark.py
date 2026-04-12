"""Benchmark — measure end-to-end latency of each pipeline stage.

Bypasses audio: feeds text directly into the pipeline and measures
time to receive the scratchpad update via WebSocket.

Usage:
    uv run python benchmark.py [--port 8888]
"""

import asyncio
import json
import subprocess
import time
import sys

import aiohttp

PROMPT_TEXT = "What is the probability of getting a king and a queen from a deck of cards without replacement?"

MODELS = [
    ("claude-haiku-4-5-20251001", "low"),
    ("claude-sonnet-4-6", "low"),
    ("gemini-3.1-flash-lite-preview", "medium"),
    ("gemini-3-flash-preview", "medium"),
]


def benchmark_llm_call(model: str, effort: str, prompt: str) -> dict:
    """Directly benchmark a single LLM subprocess call."""
    is_gemini = model.startswith("gemini")

    if is_gemini:
        cmd = ["gemini", "-p", prompt, "-m", model, "--sandbox=false", "-e", ""]
    else:
        cmd = ["claude", "--no-session-persistence", "-p", prompt, "--model", model]
        if effort in ("low", "high"):
            cmd += ["--effort", effort]

    t0 = time.perf_counter()
    try:
        result = subprocess.run(
            cmd,
            input=None,
            capture_output=True,
            text=True,
            timeout=60,
        )
        elapsed = time.perf_counter() - t0
        return {
            "model": model,
            "effort": effort,
            "time_s": round(elapsed, 2),
            "ok": result.returncode == 0,
            "output_len": len(result.stdout.strip()),
            "output_preview": result.stdout.strip()[:120],
            "error": result.stderr.strip()[:100] if result.returncode != 0 else None,
        }
    except subprocess.TimeoutExpired:
        elapsed = time.perf_counter() - t0
        return {"model": model, "effort": effort, "time_s": round(elapsed, 2), "ok": False, "error": "TIMEOUT"}
    except FileNotFoundError as e:
        return {"model": model, "effort": effort, "time_s": 0, "ok": False, "error": str(e)}


def benchmark_prompt_build():
    """Benchmark prompt construction."""
    from src.llm import build_scratchpad_prompt

    t0 = time.perf_counter()
    for _ in range(100):
        build_scratchpad_prompt(
            current_scratchpad="⚡ **Bayes** → P(A|B) = P(B|A)P(A)/P(B)\n• **Prior** vs **Posterior**",
            transcript=PROMPT_TEXT * 5,
        )
    elapsed = (time.perf_counter() - t0) * 1000
    return round(elapsed / 100, 3)


async def benchmark_websocket_roundtrip(port: int):
    """Connect to running server via WebSocket, measure delivery latency."""
    url = f"http://localhost:{port}/ws"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(url) as ws:
                # Send a settings change and measure round-trip
                t0 = time.perf_counter()
                await ws.send_str(json.dumps({"type": "settings", "model": "claude-sonnet-4-6", "effort": "low"}))
                # WebSocket settings don't echo back, so just measure connection health
                elapsed = (time.perf_counter() - t0) * 1000
                return {"ws_connected": True, "settings_send_ms": round(elapsed, 2)}
    except Exception as e:
        return {"ws_connected": False, "error": str(e)}


def main():
    port = 8888
    if "--port" in sys.argv:
        port = int(sys.argv[sys.argv.index("--port") + 1])

    print("=" * 60)
    print("  INTERVIEW HELPER — PIPELINE BENCHMARK")
    print("=" * 60)

    # 1. Prompt build
    print("\n--- Stage: Prompt Build (avg of 100 iterations) ---")
    prompt_ms = benchmark_prompt_build()
    print(f"  Prompt build: {prompt_ms}ms")

    # 2. WebSocket
    print("\n--- Stage: WebSocket Connection ---")
    ws_result = asyncio.run(benchmark_websocket_roundtrip(port))
    for k, v in ws_result.items():
        print(f"  {k}: {v}")

    # 3. LLM calls — the main event
    print("\n--- Stage: LLM Subprocess (one call per model) ---")
    print(f"  Prompt: \"{PROMPT_TEXT[:60]}...\"")
    print()

    from src.llm import build_scratchpad_prompt
    prompt = build_scratchpad_prompt(
        current_scratchpad="(empty)",
        transcript=PROMPT_TEXT,
    )

    results = []
    for model, effort in MODELS:
        provider = "Gemini" if model.startswith("gemini") else "Claude"
        label = f"{provider} {model}"
        if not model.startswith("gemini"):
            label += f" (effort={effort})"
        print(f"  Testing {label}...", end="", flush=True)
        r = benchmark_llm_call(model, effort, prompt)
        results.append(r)
        status = f"{r['time_s']}s" if r["ok"] else f"FAILED: {r.get('error', '?')}"
        print(f" {status}")

    # Summary table
    print("\n" + "=" * 60)
    print(f"  {'Model':<40} {'Time':>7}  {'Chars':>5}  Status")
    print("-" * 60)
    for r in results:
        label = r["model"]
        if not r["model"].startswith("gemini"):
            label += f" ({r['effort']})"
        status = "OK" if r["ok"] else f"ERR: {r.get('error', '?')[:20]}"
        chars = r.get("output_len", 0)
        print(f"  {label:<40} {r['time_s']:>6}s  {chars:>5}  {status}")

    print("=" * 60)

    # Recommendations
    print("\n--- Recommendations ---")
    ok_results = [r for r in results if r["ok"]]
    if ok_results:
        fastest = min(ok_results, key=lambda r: r["time_s"])
        slowest = max(ok_results, key=lambda r: r["time_s"])
        print(f"  Fastest: {fastest['model']} at {fastest['time_s']}s")
        print(f"  Slowest: {slowest['model']} at {slowest['time_s']}s")
        print(f"  Speedup: {slowest['time_s'] / fastest['time_s']:.1f}x")
    print()


if __name__ == "__main__":
    main()
