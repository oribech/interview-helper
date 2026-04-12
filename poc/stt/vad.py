#!/usr/bin/env python3
from __future__ import annotations

import re

QUESTION_RE = re.compile(
    r'\b(how|what|why|when|which|tell me about|walk me through|design|write|compute|estimate|explain|compare)\b',
    re.IGNORECASE,
)


def is_likely_question(text: str) -> bool:
    text = text.strip()
    if not text:
        return False
    return text.endswith('?') or bool(QUESTION_RE.search(text))
