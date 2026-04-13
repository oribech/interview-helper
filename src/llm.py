"""LLM subprocess wrapper — scratchpad mode.

Sends the current scratchpad + transcript to an LLM (Claude or Gemini CLI).
Claude uses a persistent process (stream-json) to avoid respawning overhead.
Gemini uses one-shot subprocess with optimized flags.
"""

import json
import re
import subprocess
import threading
import time
import uuid
from typing import Callable, Optional


SCRATCHPAD_PROMPT = """You maintain a real-time interview scratchpad for a Data Science candidate.
You receive: the current scratchpad content and new conversation transcript.
Return ONLY the updated scratchpad. No intro, no explanation, no code fences.

OPTIMIZE FOR REAL-TIME GLANCEABILITY:
- First line must be the exact phrase they can say next: `⚡ Say: **...**`
- Then write 3-6 compact bullets, each with a short label like:
  `• Step 1: ...`, `• Metric: ...`, `• Why: ...`, `• Pitfall: ...`
- Keep top-level bullets to ONE short line whenever possible
- Use indented `  →` lines only for a formula or one critical caveat
- Prefer fewer bullets over crowded bullets

CONTENT RULES:
- MAX 8 bullet points total
- Clear plain English, instantly understandable under stress
- Explain the answer, not just keywords
- **Bold** the key answer, term, number, or metric
- Write formulas in LaTeX using $...$ delimiters
- Remove stale bullets when the topic changes

EXAMPLE OUTPUT:
⚡ Say: **"K-means alternates between assigning points and recomputing centroids."**
• Step 1: **Initialize** with $k$ starting centroids
• Step 2: **Assign** each point to the nearest centroid
• Step 3: **Update** each centroid to the mean of its cluster
• Stop: when assignments stabilize or centroid movement is tiny
• Pitfall: empty clusters need reinitialization
  → Distance is usually Euclidean: $d(x, c) = \\sqrt{\\sum_i (x_i - c_i)^2}$"""


def build_scratchpad_prompt(
    current_scratchpad: str,
    transcript: str,
    wiki_context: str = "",
) -> str:
    """Build prompt for scratchpad update."""
    parts = [
        SCRATCHPAD_PROMPT,
        "",
        f"<current_scratchpad>\n{current_scratchpad or '(empty)'}\n</current_scratchpad>\n",
    ]

    if wiki_context.strip():
        parts.append(f"<wiki_context>\n{wiki_context}\n</wiki_context>\n")

    parts.append(f"<transcript>\n{transcript}\n</transcript>")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Persistent Claude CLI process
# ---------------------------------------------------------------------------

class ClaudeProcess:
    """Keeps a single Claude CLI process alive using stream-json I/O."""

    def __init__(self):
        self._proc: Optional[subprocess.Popen] = None
        self._lock = threading.Lock()
        self._model: Optional[str] = None
        self._effort: Optional[str] = None
        self._primed = False

    def _start(self, model: str, effort: str):
        """Spawn the persistent Claude process."""
        t0 = time.perf_counter()
        cmd = [
            "claude",
            "--input-format", "stream-json",
            "--output-format", "stream-json",
            "--verbose",
            "-p", "",
            "--model", model,
            "--session-id", str(uuid.uuid4()),
        ]
        if effort in ("low", "high"):
            cmd += ["--effort", effort]

        print(f"[Claude] Starting persistent process: model={model} effort={effort}")
        self._proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )
        self._model = model
        self._effort = effort
        self._primed = False
        print(f"[Claude] Persistent process ready in {(time.perf_counter() - t0)*1000:.0f}ms")

    def ensure_started(self, model: str, effort: str):
        """Ensure a matching Claude process is warm."""
        with self._lock:
            if self._needs_restart(model, effort):
                self.kill()
                self._start(model, effort)

    def _read_response(self, timeout: float = 30.0) -> Optional[str]:
        """Read stdout lines until a result event, return result text."""
        import select

        deadline = time.monotonic() + timeout
        text_parts = []

        while time.monotonic() < deadline:
            if self._proc is None or self._proc.poll() is not None:
                return None

            # Use select to avoid blocking forever on readline
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            ready, _, _ = select.select([self._proc.stdout], [], [], min(remaining, 1.0))
            if not ready:
                continue

            line = self._proc.stdout.readline()
            if not line:
                continue
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            etype = event.get("type")

            # Skip system/hook events
            if etype == "system":
                continue

            if etype == "assistant":
                msg = event.get("message", {})
                for block in msg.get("content", []):
                    if block.get("type") == "text":
                        text_parts.append(block["text"])

            elif etype == "result":
                result_text = event.get("result", "")
                if result_text:
                    return result_text
                return "".join(text_parts) if text_parts else None

        return None

    def _is_alive(self) -> bool:
        return self._proc is not None and self._proc.poll() is None

    def _needs_restart(self, model: str, effort: str) -> bool:
        if not self._is_alive():
            return True
        if self._model != model or self._effort != effort:
            return True
        return False

    def kill(self):
        """Kill the persistent process."""
        if self._proc:
            try:
                self._proc.stdin.close()
                self._proc.kill()
                self._proc.wait(timeout=3)
            except Exception:
                pass
            self._proc = None
            self._model = None
            self._effort = None
            self._primed = False

    def send(self, prompt: str, model: str, effort: str, timeout: float = 30.0) -> str:
        """Send a prompt and return the response. Thread-safe."""
        with self._lock:
            if self._needs_restart(model, effort):
                self.kill()
                self._start(model, effort)

            # Send user message
            msg = json.dumps({
                "type": "user",
                "message": {"role": "user", "content": prompt},
            })
            try:
                self._proc.stdin.write(msg + "\n")
                self._proc.stdin.flush()
            except (BrokenPipeError, OSError):
                # Process died, restart and retry once
                self.kill()
                self._start(model, effort)
                self._proc.stdin.write(msg + "\n")
                self._proc.stdin.flush()

            result = self._read_response(timeout=timeout)
            if result is None:
                # Process may have died
                self.kill()
                raise RuntimeError("No response from Claude process")
            self._primed = True
            return result

    def prime(self, model: str, effort: str, timeout: float = 30.0):
        """Warm the session with a tiny hidden request so the first real answer is faster."""
        with self._lock:
            if self._needs_restart(model, effort):
                self.kill()
                self._start(model, effort)
            if self._primed:
                return

            msg = json.dumps({
                "type": "user",
                "message": {"role": "user", "content": "Reply with exactly OK."},
            })
            try:
                self._proc.stdin.write(msg + "\n")
                self._proc.stdin.flush()
            except (BrokenPipeError, OSError):
                self.kill()
                self._start(model, effort)
                self._proc.stdin.write(msg + "\n")
                self._proc.stdin.flush()

            result = self._read_response(timeout=timeout)
            if result is None:
                self.kill()
                raise RuntimeError("Claude warmup request failed")
            self._primed = True


# Global persistent Claude process
_claude_proc = ClaudeProcess()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def update_scratchpad(
    prompt: str,
    on_result: Callable[[str], None],
    on_error: Optional[Callable[[str], None]] = None,
    timeout: int = 30,
    model: str = "claude-sonnet-4-6",
    effort: str = "medium",
) -> threading.Thread:
    """
    Send prompt to LLM and call on_result with the response.
    Claude: persistent process (fast). Gemini: one-shot subprocess.
    """

    is_gemini = model.startswith("gemini")

    def _run():
        provider = "Gemini" if is_gemini else "Claude"
        print(f"[Timing] LLM starting: {provider} model={model} (prompt {len(prompt)} chars)")
        t0 = time.perf_counter()

        try:
            if is_gemini:
                output = _call_gemini(prompt, model, timeout)
            else:
                output = _claude_proc.send(prompt, model, effort, timeout=timeout)

            output = normalize_scratchpad(output)

            elapsed = (time.perf_counter() - t0) * 1000
            print(f"[Timing] LLM finished: {elapsed:.0f}ms")

            if output:
                on_result(output)

        except Exception as e:
            elapsed = (time.perf_counter() - t0) * 1000
            print(f"[Timing] LLM error after {elapsed:.0f}ms: {e}")
            if on_error:
                on_error(f"{provider}: {e}")

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    return thread


def warmup_claude(
    model: str = "claude-sonnet-4-6",
    effort: str = "medium",
) -> Optional[threading.Thread]:
    """Pre-start the Claude CLI so the first real answer is not a cold start."""
    if model.startswith("gemini"):
        return None

    def _run():
        t0 = time.perf_counter()
        try:
            _claude_proc.prime(model, effort)
            print(f"[Timing] Claude warmup ready: {(time.perf_counter() - t0)*1000:.0f}ms")
        except Exception as e:
            print(f"[Claude] Warmup failed: {e}")

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    return thread


def _call_gemini(prompt: str, model: str, timeout: int) -> str:
    """One-shot Gemini CLI call with optimized flags."""
    cmd = ["gemini", "-p", prompt, "-m", model, "--sandbox=false", "-e", ""]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"exit code {result.returncode}")
    output = result.stdout.strip()
    if not output:
        raise RuntimeError("Empty response")
    return output


def normalize_scratchpad(text: str) -> str:
    """Clean common model formatting issues so the UI can render predictably."""
    cleaned = _strip_code_fences((text or "").strip())
    if not cleaned:
        return ""

    normalized_lines = []
    for raw_line in cleaned.splitlines():
        if not raw_line.strip():
            continue

        is_subpoint = raw_line.startswith(("  ", "\t"))
        content = raw_line.strip()
        content = re.sub(r"^\d+[.)]\s*", "", content)

        if is_subpoint:
            content = content.lstrip("•-* ").strip()
            if not content.startswith("→"):
                content = f"→ {content}"
            normalized_lines.append(f"  {content}")
            continue

        content = content.lstrip("># ").strip()
        if content.startswith(("•", "-", "*")):
            content = content[1:].strip()
            content = f"• {content}" if content else ""
        elif not content.startswith("⚡"):
            content = f"• {content}"

        if content:
            normalized_lines.append(content)

    if normalized_lines and not any(line.startswith("⚡") for line in normalized_lines if not line.startswith("  ")):
        normalized_lines[0] = normalized_lines[0].replace("• ", "⚡ ", 1)

    return "\n".join(normalized_lines)


def _strip_code_fences(text: str) -> str:
    """Remove wrapping markdown fences if the CLI returns them."""
    if not text.startswith("```"):
        return text

    lines = text.splitlines()
    if len(lines) >= 3 and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1]).strip()
    return text
