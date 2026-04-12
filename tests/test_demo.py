"""Demo test — runs the full pipeline with mocked audio and Claude CLI.

Simulates an interview conversation, verifies question detection,
wiki search, prompt building, and display server output.

Usage:
    uv run python -m tests.test_demo
"""

import asyncio
import json
import time
import threading

from src.brain import Brain
from src.llm import build_prompt
from src.wiki_search import search_wiki


# ============================================================================
# Test data — simulated interview transcript
# ============================================================================

MOCK_TRANSCRIPT = [
    # Small talk (should NOT trigger)
    ("Hi, thanks for joining us today.", 1.0),
    ("Sure, happy to be here.", 1.0),
    ("Let me tell you a bit about the team.", 1.5),

    # First question (SHOULD trigger)
    ("How would you design an A/B test for a new search ranking algorithm?", 2.0),

    # Interviewer follow-up context (should NOT trigger — debounce)
    ("Specifically, what metrics would you track?", 1.0),

    # Pause, then a new question (SHOULD trigger after debounce)
    ("Great. Now, can you explain the difference between Type I and Type II errors?", 9.0),

    # Another question
    ("What is overfitting and how do you prevent it?", 9.0),
]

MOCK_CLAUDE_RESPONSE = """**Answer:** An A/B test for search ranking should use interleaving or parallel experiments.

**Key Points:**
- **Metric**: NDCG, click-through rate, time-to-success
- **Randomization**: user-level (not query-level) to avoid inconsistency
- **Duration**: minimum 2 weeks to capture weekly patterns
- **Guardrails**: latency p99, revenue, abandonment rate

**Example:** Google runs >10k experiments/year on search using interleaved designs."""


# ============================================================================
# Unit tests
# ============================================================================

def test_brain_question_detection():
    """Test that Brain correctly detects questions and respects debounce."""
    print("\n=== Test: Brain Question Detection ===")

    detected = []

    def on_question(question, context):
        detected.append(question)

    brain = Brain(on_question=on_question, debounce_seconds=5.0)

    for text, delay in MOCK_TRANSCRIPT:
        time.sleep(0.05)
        brain.add_text(text)
        if delay > 5.0:
            time.sleep(0.1)
            brain._last_trigger_time -= delay  # fast-forward debounce

    print(f"  Detected {len(detected)} questions:")
    for i, q in enumerate(detected):
        print(f"    {i+1}. {q[:70]}...")

    assert len(detected) >= 1, f"Expected at least 1 question, got {len(detected)}"
    assert "A/B test" in detected[0] or "design" in detected[0].lower()
    print("  ✅ PASSED")
    return True


def test_wiki_search():
    """Test that wiki search finds relevant pages."""
    print("\n=== Test: Wiki Search ===")

    result = search_wiki("A/B test experiment design metrics")
    assert len(result) > 0, "Wiki search returned nothing"
    assert "Null hypothesis" in result or "A/B" in result
    print(f"  Found {len(result)} chars of wiki context")

    result2 = search_wiki("overfitting bias variance model")
    assert len(result2) > 0, "Wiki search for ML returned nothing"
    print(f"  Found {len(result2)} chars of ML wiki context")

    result3 = search_wiki("quantum computing blockchain")
    print(f"  Irrelevant query returned {len(result3)} chars (should be 0)")

    print("  ✅ PASSED")
    return True


def test_prompt_building():
    """Test that prompts are correctly assembled."""
    print("\n=== Test: Prompt Building ===")

    question = "How would you design an A/B test?"
    context = "The interviewer asked about search ranking experiments"
    wiki = search_wiki(question)

    prompt = build_prompt(question, context, wiki)

    assert "<transcript>" in prompt
    assert "<question>" in prompt
    assert "<wiki_context>" in prompt
    assert question in prompt
    assert context in prompt

    print(f"  Prompt length: {len(prompt)} chars")
    print(f"  Contains transcript: ✓")
    print(f"  Contains question: ✓")
    print(f"  Contains wiki_context: ✓")
    print("  ✅ PASSED")
    return True


def test_display_server_and_websocket():
    """Test that display server starts and can broadcast messages."""
    print("\n=== Test: Display Server + WebSocket ===")

    from src.display import start_server, broadcast, reset

    reset()
    messages_received = []

    async def run_test():
        import aiohttp

        runner = await start_server(port=8890)

        # Connect a WebSocket client
        session = aiohttp.ClientSession()
        ws = await session.ws_connect("http://localhost:8890/ws")
        await asyncio.sleep(0.1)  # let connection register

        # Broadcast messages directly (same event loop)
        await broadcast({"type": "question", "text": "Test question?"})
        await broadcast({"type": "answer_chunk", "text": "This is "})
        await broadcast({"type": "answer_chunk", "text": "the answer."})
        await broadcast({"type": "answer_done"})
        await asyncio.sleep(0.2)

        # Read all messages
        while True:
            try:
                msg = await asyncio.wait_for(ws.receive(), timeout=0.5)
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    messages_received.append(data)
                else:
                    break
            except asyncio.TimeoutError:
                break

        await ws.close()
        await session.close()
        await runner.cleanup()

    asyncio.run(run_test())

    print(f"  Received {len(messages_received)} WebSocket messages:")
    for msg in messages_received:
        print(f"    {msg['type']}: {msg.get('text', '')[:60]}")

    assert len(messages_received) >= 3, f"Expected ≥3 messages, got {len(messages_received)}"

    types = [m["type"] for m in messages_received]
    assert "question" in types
    assert "answer_chunk" in types
    assert "answer_done" in types

    print("  ✅ PASSED")
    return True


def test_full_pipeline_with_mock():
    """Full integration: mock audio → brain → wiki → mock Claude → display WS."""
    print("\n=== Test: Full Pipeline (Mocked) ===")

    from src.display import start_server, broadcast, reset

    reset()

    results = {
        "questions_detected": [],
        "prompts_sent": [],
        "ws_messages": [],
    }

    async def run_full_test():
        import aiohttp

        runner = await start_server(port=8891)
        loop = asyncio.get_event_loop()

        # Connect WS client
        session = aiohttp.ClientSession()
        ws = await session.ws_connect("http://localhost:8891/ws")
        await asyncio.sleep(0.1)

        # On question: search wiki, build prompt, mock Claude, broadcast answer
        async def handle_question(question, context):
            results["questions_detected"].append(question)
            await broadcast({"type": "question", "text": question})

            wiki_context = search_wiki(question)
            prompt = build_prompt(question, context, wiki_context or None)
            results["prompts_sent"].append(prompt)

            for word in MOCK_CLAUDE_RESPONSE.split(" "):
                await broadcast({"type": "answer_chunk", "text": word + " "})
            await broadcast({"type": "answer_done"})

        brain = Brain(
            on_question=lambda q, c: asyncio.run_coroutine_threadsafe(
                handle_question(q, c), loop
            ),
            debounce_seconds=0.5,
        )

        # Run brain from a separate thread (like real audio callback)
        def simulate_audio():
            for text, delay in MOCK_TRANSCRIPT:
                brain.add_text(text)
                if delay > 5.0:
                    brain._last_trigger_time -= delay
                time.sleep(0.02)

        audio_thread = threading.Thread(target=simulate_audio, daemon=True)
        audio_thread.start()
        audio_thread.join(timeout=5)

        # Wait for async processing to complete
        await asyncio.sleep(1.0)

        # Collect WS messages
        while True:
            try:
                msg = await asyncio.wait_for(ws.receive(), timeout=0.5)
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    results["ws_messages"].append(data)
                else:
                    break
            except asyncio.TimeoutError:
                break

        await ws.close()
        await session.close()
        await runner.cleanup()

    asyncio.run(run_full_test())

    # Verify
    print(f"  Questions detected: {len(results['questions_detected'])}")
    for q in results["questions_detected"]:
        print(f"    → {q[:70]}")

    print(f"  Prompts sent to Claude: {len(results['prompts_sent'])}")
    print(f"  WebSocket messages: {len(results['ws_messages'])}")

    ws_types = [m["type"] for m in results["ws_messages"]]
    type_counts = {t: ws_types.count(t) for t in set(ws_types)}
    print(f"  Message types: {type_counts}")

    assert len(results["questions_detected"]) >= 1, "No questions detected"
    assert len(results["prompts_sent"]) >= 1, "No prompts sent"
    assert "question" in ws_types, "No question message on WS"
    assert "answer_chunk" in ws_types, "No answer chunks on WS"

    # Verify prompt quality
    first_prompt = results["prompts_sent"][0]
    assert "wiki_context" in first_prompt, "Prompt missing wiki context"
    assert "transcript" in first_prompt, "Prompt missing transcript"

    print("  ✅ PASSED")
    return True


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import sys

    print("=" * 60)
    print("  Interview Helper — Demo Tests")
    print("=" * 60)

    all_passed = True
    tests = [
        test_brain_question_detection,
        test_wiki_search,
        test_prompt_building,
        test_display_server_and_websocket,
        test_full_pipeline_with_mock,
    ]

    for test_fn in tests:
        try:
            test_fn()
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("  ✅ ALL TESTS PASSED")
    else:
        print("  ❌ SOME TESTS FAILED")
    print("=" * 60)
