"""Claude CLI subprocess wrapper — scratchpad mode.

Sends the current scratchpad + transcript to Claude.
Claude returns the full updated scratchpad.
"""

import subprocess
import threading
from typing import Callable, Optional


SCRATCHPAD_PROMPT = """You maintain a real-time interview scratchpad for a Data Science candidate.
You receive: the current scratchpad content and new conversation transcript.
Return ONLY the updated scratchpad — nothing else.

RULES:
- MAX 8 bullet points visible at a time
- Each bullet: ≤15 words, keyword-dense, glanceable
- Use → for sub-points (indent with 2 spaces)
- **Bold** key terms, formulas, numbers
- Remove stale bullets no longer relevant to the current topic
- If a new topic appears, replace old topic bullets
- If you hear a question, add concise answer hints
- Use ⚡ prefix for the most urgent/current point
- NO headers, NO paragraphs, NO explanations
- Format for GLANCING at a screen, not reading

EXAMPLE OUTPUT:
⚡ **A/B test design** → define OEC first, then randomization unit
  → sample size: n = (Zα+Zβ)²·2σ²/δ²
• **Guardrails**: latency p99, revenue, crash rate
• **Duration**: min 2 weeks for weekly cycle effects
• **Interference** → cluster randomization for network effects
• **Multiple testing** → Bonferroni or BH correction"""


def build_scratchpad_prompt(
    current_scratchpad: str,
    transcript: str,
    wiki_context: Optional[str] = None,
) -> str:
    """Build prompt for scratchpad update."""
    parts = [SCRATCHPAD_PROMPT, ""]

    if wiki_context:
        parts.append(f"<wiki_context>\n{wiki_context}\n</wiki_context>\n")

    parts.append(f"<current_scratchpad>\n{current_scratchpad or '(empty)'}\n</current_scratchpad>\n")
    parts.append(f"<transcript>\n{transcript}\n</transcript>")

    return "\n".join(parts)


def update_scratchpad(
    prompt: str,
    on_result: Callable[[str], None],
    on_error: Optional[Callable[[str], None]] = None,
    timeout: int = 20,
) -> threading.Thread:
    """
    Call Claude CLI to get the updated scratchpad.
    Runs in a background thread. Calls on_result with the full new scratchpad.
    """

    def _run():
        try:
            result = subprocess.run(
                ["claude", "-p", prompt],
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            if result.returncode != 0:
                err = result.stderr.strip()
                if on_error:
                    on_error(f"Claude error: {err}")
                return

            output = result.stdout.strip()
            if output:
                on_result(output)

        except subprocess.TimeoutExpired:
            if on_error:
                on_error("Claude timeout")
        except FileNotFoundError:
            if on_error:
                on_error("Claude CLI not found")
        except Exception as e:
            if on_error:
                on_error(str(e))

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    return thread
