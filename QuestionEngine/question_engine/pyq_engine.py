"""PYQ intake and verification status. This module never invents missing source content."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .models import QuestionCandidate, QuestionOrigin
from .quality import QuestionQualityGate


@dataclass(frozen=True)
class PYQIntakeResult:
    verified_for_practice: bool
    pending_reasons: tuple[str, ...]


class PYQPracticeEngine:
    """Accept historical questions only with traceable, verified source evidence."""

    def __init__(self, quality_gate: QuestionQualityGate | None = None):
        self.quality_gate = quality_gate or QuestionQualityGate()
        self._verified: List[QuestionCandidate] = []
        self._pending: List[QuestionCandidate] = []

    def ingest(self, question: QuestionCandidate) -> PYQIntakeResult:
        if question.origin != QuestionOrigin.PYQ:
            return PYQIntakeResult(False, ("PYQ engine accepts exact PYQ records only",))

        decision = self.quality_gate.evaluate(question)
        if decision.approved:
            self._verified.append(question)
            return PYQIntakeResult(True, ())

        self._pending.append(question)
        return PYQIntakeResult(False, decision.reasons)

    @property
    def verified_questions(self) -> tuple[QuestionCandidate, ...]:
        return tuple(self._verified)

    @property
    def pending_questions(self) -> tuple[QuestionCandidate, ...]:
        return tuple(self._pending)
