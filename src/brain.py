"""Question detector + rolling context window.

Maintains a rolling transcript of the conversation and detects
when an interview question is being asked. Triggers LLM calls.
"""

import re
import time
from dataclasses import dataclass, field
from typing import Callable, List, Optional


# Patterns that indicate an interview question
QUESTION_PATTERNS = [
    # Direct questions
    r"\b(how would you|how do you|how can you)\b",
    r"\b(what is|what are|what would|what's the)\b",
    r"\b(explain|describe|tell me about|walk me through)\b",
    r"\b(can you|could you|would you)\b.*\?",
    r"\b(why|when|where|which)\b.*\?",
    # Interview-specific
    r"\b(design|build|implement|approach|solve|optimize)\b",
    r"\b(difference between|compare|trade-?offs?)\b",
    r"\b(what happens|what if|suppose|imagine|consider)\b",
    r"\b(give me an example|for example|for instance)\b",
    # DS/ML-specific
    r"\b(a/?b test|experiment|hypothesis|metric|statistical)\b",
    r"\b(model|algorithm|feature|bias|variance|overfitting)\b",
    r"\b(p-?value|confidence interval|significance)\b",
]

COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in QUESTION_PATTERNS]

# Minimum confidence score to trigger (how many patterns match)
MIN_PATTERNS_TO_TRIGGER = 1


@dataclass
class TranscriptChunk:
    """A timestamped piece of transcript."""
    text: str
    timestamp: float = field(default_factory=time.time)


class Brain:
    """
    Accumulates transcript context and detects interview questions.
    When a question is detected, calls the on_question callback.
    """

    def __init__(
        self,
        on_question: Callable[[str, str], None],
        context_window_seconds: float = 90.0,
        debounce_seconds: float = 8.0,
    ):
        """
        Args:
            on_question: called with (question_text, full_context) when question detected
            context_window_seconds: how much transcript to keep (rolling)
            debounce_seconds: min time between question triggers
        """
        self.on_question = on_question
        self.context_window_seconds = context_window_seconds
        self.debounce_seconds = debounce_seconds

        self._chunks: List[TranscriptChunk] = []
        self._last_trigger_time: float = 0
        self._last_triggered_text: str = ""

    def add_text(self, text: str):
        """
        Add a new transcript chunk. Checks if it contains a question.
        """
        now = time.time()
        self._chunks.append(TranscriptChunk(text=text, timestamp=now))
        self._prune_old_chunks(now)

        # Check for question
        if self._is_question(text) and self._can_trigger(now, text):
            context = self.get_context()
            self._last_trigger_time = now
            self._last_triggered_text = text
            print(f"[Brain] Question detected: {text[:80]}...")
            self.on_question(text, context)

    def _is_question(self, text: str) -> bool:
        """Check if text contains an interview question."""
        matches = sum(1 for p in COMPILED_PATTERNS if p.search(text))
        return matches >= MIN_PATTERNS_TO_TRIGGER

    def _can_trigger(self, now: float, text: str) -> bool:
        """Debounce: avoid re-triggering on similar text."""
        if now - self._last_trigger_time < self.debounce_seconds:
            return False
        # Don't re-trigger if text is very similar to last trigger
        if self._last_triggered_text and text == self._last_triggered_text:
            return False
        return True

    def get_context(self) -> str:
        """Get the full rolling context window as a single string."""
        return " ".join(chunk.text for chunk in self._chunks)

    def _prune_old_chunks(self, now: float):
        """Remove chunks older than the context window."""
        cutoff = now - self.context_window_seconds
        self._chunks = [c for c in self._chunks if c.timestamp >= cutoff]
