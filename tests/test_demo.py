"""Demo test — scratchpad mode.

Verifies: brain triggers, prompt building, display server,
and full pipeline with mocked Claude.

Usage:
    uv run python -m tests.test_demo
"""

import asyncio
import json
import time
import threading

from src.brain import Brain
from src.llm import build_scratchpad_prompt


# ============================================================================
# Test data
# ============================================================================

MOCK_TRANSCRIPT = [
    "Hi, thanks for joining us today.",
    "Let me tell you a bit about the team.",
    "How would you design an A/B test for a new search ranking algorithm?",
    "Specifically, what metrics would you track?",
    "What about guardrail metrics?",
]

MOCK_SCRATCHPAD_V1 = """⚡ **A/B test design** → define OEC first, randomization unit = user
  → sample size: n = (Zα+Zβ)²·2σ²/δ²
• **Metrics**: NDCG, CTR, time-to-success
• **Guardrails**: latency p99, revenue, crash rate
• **Duration**: min 2 weeks for weekly cycle effects"""

MOCK_SCRATCHPAD_V2 = """⚡ **Guardrail metrics** → latency p99, revenue, crash rate, abandonment
• **A/B test design** → define OEC, user-level randomization
  → sample size: n = (Zα+Zβ)²·2σ²/δ²
• **Metrics**: NDCG, CTR, time-to-success
• **SRM check** → verify sample ratio before analyzing results"""


# ============================================================================
# Tests
# ============================================================================

def test_brain_triggers():
    """Test that brain triggers on each chunk with debounce."""
    print("\n=== Test: Brain Triggers ===")

    triggered = []
    brain = Brain(
        on_update=lambda new, ctx: triggered.append(new),
        min_interval_seconds=0.1,
    )

    for text in MOCK_TRANSCRIPT:
        brain.add_text(text)
        time.sleep(0.15)

    print(f"  Triggered {len(triggered)} times")
    for t in triggered:
        print(f"    → {t[:60]}")

    assert len(triggered) >= 3, f"Expected ≥3 triggers, got {len(triggered)}"
    print("  ✅ PASSED")


def test_brain_busy_guard():
    """Test that busy mode defers work instead of dropping it."""
    print("\n=== Test: Brain Busy Guard ===")

    triggered = []
    brain = Brain(
        on_update=lambda new, ctx: triggered.append(new),
        min_interval_seconds=0.05,
    )

    brain.set_busy(True)
    for text in MOCK_TRANSCRIPT:
        brain.add_text(text)
        time.sleep(0.06)

    assert len(triggered) == 0, f"Expected 0 triggers while busy, got {len(triggered)}"
    print("  Busy guard blocked all triggers ✓")

    brain.set_busy(False)
    time.sleep(0.06)
    assert len(triggered) == 1, f"Expected deferred trigger after unbusy, got {len(triggered)}"
    print("  Pending update flushed after unbusy ✓")

    brain.add_text("Now I should trigger")
    time.sleep(0.06)
    assert len(triggered) == 2, f"Expected 2 triggers after new text, got {len(triggered)}"
    print("  Trigger resumed after unbusy ✓")
    print("  ✅ PASSED")


def test_scratchpad_prompt():
    """Test prompt building for scratchpad."""
    print("\n=== Test: Scratchpad Prompt ===")

    prompt = build_scratchpad_prompt(
        current_scratchpad=MOCK_SCRATCHPAD_V1,
        transcript="How would you design an A/B test?",
    )

    assert "current_scratchpad" in prompt
    assert "transcript" in prompt
    assert "MAX 8 bullet" in prompt
    assert MOCK_SCRATCHPAD_V1 in prompt

    print(f"  Prompt length: {len(prompt)} chars")
    print(f"  Contains scratchpad: ✓")
    print(f"  Contains glanceability rules: ✓")
    print("  ✅ PASSED")


def test_display_scratchpad():
    """Test display server sends scratchpad updates."""
    print("\n=== Test: Display Scratchpad ===")

    from src.display import start_server, broadcast, reset
    reset()

    messages = []

    async def run():
        import aiohttp
        runner = await start_server(port=8893)
        session = aiohttp.ClientSession()
        ws = await session.ws_connect("http://localhost:8893/ws")
        await asyncio.sleep(0.1)

        await broadcast({"type": "updating"})
        await broadcast({"type": "scratchpad", "text": MOCK_SCRATCHPAD_V1})
        await asyncio.sleep(0.2)

        while True:
            try:
                msg = await asyncio.wait_for(ws.receive(), timeout=0.5)
                if msg.type == aiohttp.WSMsgType.TEXT:
                    messages.append(json.loads(msg.data))
                else:
                    break
            except asyncio.TimeoutError:
                break

        await ws.close()
        await session.close()
        await runner.cleanup()

    asyncio.run(run())

    types = [m["type"] for m in messages]
    print(f"  Messages: {types}")
    assert "updating" in types
    assert "scratchpad" in types
    assert messages[-1]["text"] == MOCK_SCRATCHPAD_V1
    print("  ✅ PASSED")


def test_full_pipeline():
    """Full pipeline: transcript → brain → mock Claude → display."""
    print("\n=== Test: Full Pipeline (Mocked) ===")

    from src.display import start_server, broadcast, reset
    reset()

    results = {"updates": [], "ws_messages": []}
    scratchpad_versions = [MOCK_SCRATCHPAD_V1, MOCK_SCRATCHPAD_V2]

    async def run():
        import aiohttp
        runner = await start_server(port=8894)
        loop = asyncio.get_event_loop()

        session = aiohttp.ClientSession()
        ws = await session.ws_connect("http://localhost:8894/ws")
        await asyncio.sleep(0.1)

        call_count = [0]

        async def handle_update(new_text, context):
            results["updates"].append(new_text)
            await broadcast({"type": "updating"})

            # Mock Claude: return next scratchpad version
            idx = min(call_count[0], len(scratchpad_versions) - 1)
            pad = scratchpad_versions[idx]
            call_count[0] += 1

            await asyncio.sleep(0.1)  # simulate LLM latency
            await broadcast({"type": "scratchpad", "text": pad})
            brain.set_busy(False)

        brain = Brain(
            on_update=lambda n, c: asyncio.run_coroutine_threadsafe(
                handle_update(n, c), loop
            ),
            min_interval_seconds=0.1,
        )

        def simulate():
            for text in MOCK_TRANSCRIPT:
                brain.add_text(text)
                time.sleep(0.15)

        t = threading.Thread(target=simulate, daemon=True)
        t.start()
        t.join(timeout=5)
        await asyncio.sleep(1.0)

        while True:
            try:
                msg = await asyncio.wait_for(ws.receive(), timeout=0.5)
                if msg.type == aiohttp.WSMsgType.TEXT:
                    results["ws_messages"].append(json.loads(msg.data))
                else:
                    break
            except asyncio.TimeoutError:
                break

        await ws.close()
        await session.close()
        await runner.cleanup()

    asyncio.run(run())

    print(f"  Brain updates: {len(results['updates'])}")
    ws_types = [m["type"] for m in results["ws_messages"]]
    type_counts = {t: ws_types.count(t) for t in set(ws_types)}
    print(f"  WS message types: {type_counts}")

    assert len(results["updates"]) >= 1, "No brain updates"
    assert "scratchpad" in ws_types, "No scratchpad messages"
    assert "updating" in ws_types, "No updating messages"
    print("  ✅ PASSED")


# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Interview Helper — Scratchpad Tests")
    print("=" * 60)

    all_passed = True
    for test_fn in [
        test_brain_triggers,
        test_brain_busy_guard,
        test_scratchpad_prompt,
        test_display_scratchpad,
        test_full_pipeline,
    ]:
        try:
            test_fn()
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False

    print("\n" + "=" * 60)
    print(f"  {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    print("=" * 60)
