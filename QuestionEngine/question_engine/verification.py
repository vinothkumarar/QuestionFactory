"""Independent answer-verification contract for generated questions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .models import QuestionCandidate


@dataclass(frozen=True)
class AnswerVerificationResult:
    question_id: str
    verified: bool
    method: str
    evidence: str
    reason: str = ""


class QuestionAnswerVerifier(Protocol):
    """A verifier independent of the question-generation provider."""

    def verify(self, question: QuestionCandidate) -> AnswerVerificationResult:
        """Check the answer and reasoning; return traceable evidence."""
        ...
