"""Claude CLI subprocess wrapper.

Sends prompts to Claude via the `claude` CLI command and returns responses.
Supports both blocking and streaming modes.
"""

import subprocess
import threading
from typing import Callable, Optional


SYSTEM_PROMPT = """You are a real-time interview answer assistant for a Data Science interview at Google.
You hear the conversation transcript and must answer the detected question.

Rules:
- Be concise: bullet points, key formulas, numbers
- Max 150 words
- Start with the direct answer, then supporting detail
- Include specific examples when relevant
- Use markdown formatting for readability
- If wiki context is provided, reference it

Format:
**Answer:** [1-2 sentence direct answer]

**Key Points:**
- point 1
- point 2
- point 3

**Example:** [brief concrete example if applicable]"""


def build_prompt(
    question: str,
    context: str,
    wiki_context: Optional[str] = None,
) -> str:
    """Build the full prompt for Claude."""

    parts = [SYSTEM_PROMPT, ""]

    if wiki_context:
        parts.append(f"<wiki_context>\n{wiki_context}\n</wiki_context>\n")

    parts.append(f"<transcript>\n{context}\n</transcript>\n")
    parts.append(f"<question>\n{question}\n</question>")

    return "\n".join(parts)


def ask_claude_blocking(prompt: str, timeout: int = 30) -> str:
    """
    Send prompt to Claude CLI and return the full response.
    Blocking call — waits for completion.
    """
    try:
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        if result.returncode != 0:
            return f"[Claude error: {result.stderr.strip()}]"

        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        return "[Claude timeout — question may be too complex]"
    except FileNotFoundError:
        return "[Claude CLI not found — install with: npm install -g @anthropic-ai/claude-cli]"
    except Exception as e:
        return f"[Claude error: {e}]"


def ask_claude_streaming(
    prompt: str,
    on_chunk: Callable[[str], None],
    on_done: Optional[Callable[[], None]] = None,
    timeout: int = 30,
):
    """
    Send prompt to Claude CLI and stream the response chunk by chunk.
    Runs in a background thread.

    Args:
        prompt: full prompt text
        on_chunk: called with each text chunk as it arrives
        on_done: called when streaming is complete
        timeout: max seconds to wait
    """

    def _stream():
        try:
            proc = subprocess.Popen(
                ["claude", "-p", prompt],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            buffer = ""
            for char in iter(lambda: proc.stdout.read(1), ""):
                buffer += char
                # Flush on word boundaries or newlines
                if char in (" ", "\n", "\t") or len(buffer) > 20:
                    on_chunk(buffer)
                    buffer = ""

            # Flush remaining
            if buffer:
                on_chunk(buffer)

            proc.wait(timeout=timeout)

            if proc.returncode != 0:
                stderr = proc.stderr.read()
                on_chunk(f"\n[Claude error: {stderr.strip()}]")

        except Exception as e:
            on_chunk(f"\n[Error: {e}]")
        finally:
            if on_done:
                on_done()

    thread = threading.Thread(target=_stream, daemon=True)
    thread.start()
    return thread
