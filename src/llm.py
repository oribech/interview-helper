"""LLM subprocess wrapper — scratchpad mode.

Sends the current scratchpad + transcript to an LLM (Claude or Gemini CLI).
Returns the full updated scratchpad.
"""

import subprocess
import threading
import time
from typing import Callable, Optional


SCRATCHPAD_PROMPT = """You maintain a real-time interview scratchpad for a Data Science candidate.
You receive: the current scratchpad content and new conversation transcript.
Return ONLY the updated scratchpad — nothing else.

RULES:
- MAX 8 bullet points visible at a time
- Each bullet: ≤15 words, keyword-dense, glanceable
- Use → for sub-points (indent with 2 spaces)
- **Bold** key terms and numbers
- Write ALL formulas in LaTeX using $...$ delimiters (e.g. $n = \\frac{(Z_\\alpha + Z_\\beta)^2 \\cdot 2\\sigma^2}{\\delta^2}$)
- Remove stale bullets no longer relevant to the current topic
- If a new topic appears, replace old topic bullets
- If you hear a question, add concise answer hints
- Use ⚡ prefix for the most urgent/current point
- NO headers, NO paragraphs, NO explanations
- Format for GLANCING at a screen, not reading

EXAMPLE OUTPUT:
⚡ **A/B test design** → define OEC first, then randomization unit
  → sample size: $n = \\frac{(Z_\\alpha + Z_\\beta)^2 \\cdot 2\\sigma^2}{\\delta^2}$
• **Guardrails**: latency p99, revenue, crash rate
• **Duration**: min 2 weeks for weekly cycle effects
• **Interference** → cluster randomization for network effects
• **Multiple testing** → Bonferroni or BH correction"""


def build_scratchpad_prompt(
    current_scratchpad: str,
    transcript: str,
) -> str:
    """Build prompt for scratchpad update."""
    parts = [
        SCRATCHPAD_PROMPT,
        "",
        f"<current_scratchpad>\n{current_scratchpad or '(empty)'}\n</current_scratchpad>\n",
        f"<transcript>\n{transcript}\n</transcript>",
    ]

    return "\n".join(parts)


def update_scratchpad(
    prompt: str,
    on_result: Callable[[str], None],
    on_error: Optional[Callable[[str], None]] = None,
    timeout: int = 20,
    model: str = "claude-sonnet-4-6",
    effort: str = "medium",
) -> threading.Thread:
    """
    Call Claude CLI to get the updated scratchpad.
    Runs in a background thread. Calls on_result with the full new scratchpad.
    """

    is_gemini = model.startswith("gemini")

    def _run():
        try:
            if is_gemini:
                cmd = ["gemini", "-m", model]
            else:
                cmd = ["claude", "-p", prompt, "--model", model]
                if effort in ("low", "high"):
                    cmd += ["--effort", effort]

            provider = "Gemini" if is_gemini else "Claude"
            print(f"[Timing] LLM subprocess starting: {provider} model={model} (prompt {len(prompt)} chars)")
            t0 = time.perf_counter()
            result = subprocess.run(
                cmd,
                input=prompt if is_gemini else None,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            elapsed = (time.perf_counter() - t0) * 1000
            print(f"[Timing] LLM subprocess finished: {elapsed:.0f}ms (returncode={result.returncode})")

            if result.returncode != 0:
                err = result.stderr.strip()
                if on_error:
                    on_error(f"{provider} error: {err}")
                return

            output = result.stdout.strip()
            if output:
                on_result(output)

        except subprocess.TimeoutExpired:
            if on_error:
                on_error(f"{provider} timeout")
        except FileNotFoundError:
            if on_error:
                on_error(f"{provider} CLI not found — install with: {'brew install gemini-cli' if is_gemini else 'npm install -g @anthropic-ai/claude-code'}")
        except Exception as e:
            if on_error:
                on_error(str(e))

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    return thread
