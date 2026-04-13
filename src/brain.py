"""Brain — transcript accumulator + LLM trigger.

Accumulates transcript chunks into a rolling context window.
Triggers an update callback on every finalized transcript chunk,
with debounce to skip if an LLM call is already in-flight.
"""

import threading
import time
from dataclasses import dataclass, field
from typing import Callable, List, Optional


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
        self._unsent: List[str] = []  # chunks not yet sent to LLM
        self._last_trigger_time: float = 0
        self._busy = False  # True when an LLM call is in-flight
        self._pending = False
        self._timer: Optional[threading.Timer] = None
        self._lock = threading.Lock()

    def add_text(self, text: str):
        """Add a finalized transcript chunk and schedule a fresh update."""
        cleaned = (text or "").strip()
        if not cleaned:
            return

        with self._lock:
            now = time.time()
            self._chunks.append(TranscriptChunk(text=cleaned, timestamp=now))
            self._unsent.append(cleaned)
            self._prune_old_chunks(now)
            self._pending = True

        self._schedule_or_trigger()

    def set_busy(self, busy: bool):
        """Set/clear the busy flag (called by orchestrator)."""
        with self._lock:
            self._busy = busy
        if not busy:
            self._schedule_or_trigger()

    def get_context(self) -> str:
        """Get the full rolling context window as a single string."""
        with self._lock:
            return " ".join(chunk.text for chunk in self._chunks)

    def _schedule_or_trigger(self):
        """Trigger immediately if possible, otherwise schedule the earliest retry."""
        payload = None
        delay = None

        with self._lock:
            if not self._pending or not self._chunks:
                return
            if self._busy:
                return

            now = time.time()
            remaining = self.min_interval_seconds - (now - self._last_trigger_time)

            if remaining > 0:
                if self._timer is None or not self._timer.is_alive():
                    delay = remaining
            else:
                self._cancel_timer_locked()
                self._pending = False
                self._last_trigger_time = now
                delta_text = " ".join(self._unsent)
                self._unsent.clear()
                context = " ".join(chunk.text for chunk in self._chunks)
                payload = (delta_text, context, len(self._chunks))

        if delay is not None:
            self._start_timer(delay)

        if payload is not None:
            delta_text, context, chunk_count = payload
            print(f"[Brain] Triggering update (delta): {delta_text[:60]}...")
            print(
                f"[Timing] Brain dispatch: delta={len(delta_text)} chars | "
                f"total context={len(context)} chars | chunks={chunk_count}"
            )
            self.on_update(delta_text, context)

    def _start_timer(self, delay: float):
        timer = threading.Timer(delay, self._timer_fired)
        timer.daemon = True
        with self._lock:
            if self._timer is not None and self._timer.is_alive():
                return
            self._timer = timer
            self._timer.start()

    def _timer_fired(self):
        with self._lock:
            self._timer = None
        self._schedule_or_trigger()

    def _cancel_timer_locked(self):
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None

    def _prune_old_chunks(self, now: float):
        """Remove chunks older than the context window."""
        cutoff = now - self.context_window_seconds
        self._chunks = [c for c in self._chunks if c.timestamp >= cutoff]
