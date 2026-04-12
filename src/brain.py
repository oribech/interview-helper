"""Brain — transcript accumulator + LLM trigger.

Accumulates transcript chunks into a rolling context window.
Triggers an update callback on every finalized transcript chunk,
with debounce to skip if an LLM call is already in-flight.
"""

import time
import threading
from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class TranscriptChunk:
    """A timestamped piece of transcript."""
    text: str
    timestamp: float = field(default_factory=time.time)


class Brain:
    """
    Accumulates transcript and triggers scratchpad updates.
    Skips triggering if an update is already in-flight.
    """

    def __init__(
        self,
        on_update: Callable[[str, str], None],
        context_window_seconds: float = 90.0,
        min_interval_seconds: float = 3.0,
    ):
        """
        Args:
            on_update: called with (new_text, full_context) for each meaningful chunk
            context_window_seconds: how much transcript to keep (rolling)
            min_interval_seconds: minimum time between triggers
        """
        self.on_update = on_update
        self.context_window_seconds = context_window_seconds
        self.min_interval_seconds = min_interval_seconds

        self._chunks: List[TranscriptChunk] = []
        self._last_trigger_time: float = 0
        self._busy = False  # True when an LLM call is in-flight
        self._lock = threading.Lock()

    def add_text(self, text: str):
        """Add a finalized transcript chunk. Triggers update if not busy."""
        if not text or not text.strip():
            return

        now = time.time()
        self._chunks.append(TranscriptChunk(text=text.strip(), timestamp=now))
        self._prune_old_chunks(now)

        # Skip if too soon or LLM is busy
        if now - self._last_trigger_time < self.min_interval_seconds:
            return
        if self._busy:
            print("[Brain] Skipping — LLM still processing")
            return

        context = self.get_context()
        self._last_trigger_time = now
        print(f"[Brain] Triggering update: {text[:60]}...")
        self.on_update(text.strip(), context)

    def set_busy(self, busy: bool):
        """Set/clear the busy flag (called by orchestrator)."""
        with self._lock:
            self._busy = busy

    def get_context(self) -> str:
        """Get the full rolling context window as a single string."""
        return " ".join(chunk.text for chunk in self._chunks)

    def _prune_old_chunks(self, now: float):
        """Remove chunks older than the context window."""
        cutoff = now - self.context_window_seconds
        self._chunks = [c for c in self._chunks if c.timestamp >= cutoff]
