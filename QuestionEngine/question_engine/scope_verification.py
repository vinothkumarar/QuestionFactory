"""Independent curriculum-scope verification contract."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .models import QuestionCandidate


@dataclass(frozen=True)
class ScopeVerificationResult:
    question_id: str
    verified: bool
    method: str
    evidence: str
    reason: str = ""


class QuestionScopeVerifier(Protocol):
    """Check each question against the authoritative curriculum hierarchy."""

    def verify(self, question: QuestionCandidate) -> ScopeVerificationResult:
        ...
