"""Provider-neutral contract for original-question generation.

Concrete AI providers are deployment adapters. They must return canonical
QuestionCandidate records and must never self-assert answer verification unless
an independent verification stage has actually run.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol

from .models import QuestionCandidate


@dataclass(frozen=True)
class GenerationRequest:
    subject_id: str
    unit_id: str
    chapter_id: str
    subtopic_id: str
    exam_targets: tuple[str, ...]
    concept_ids: tuple[str, ...]
    learning_outcomes: tuple[str, ...]
    excluded_reasoning_signatures: tuple[str, ...] = ()
    candidate_limit: int = 5

    def __post_init__(self) -> None:
        required = (
            self.subject_id,
            self.unit_id,
            self.chapter_id,
            self.subtopic_id,
        )
        if not all(value.strip() for value in required):
            raise ValueError("Generation request requires complete curriculum IDs")
        if self.candidate_limit < 1:
            raise ValueError("candidate_limit must be at least 1")
        if not self.exam_targets:
            raise ValueError("At least one exam target is required")
        if not self.learning_outcomes:
            raise ValueError("At least one learning outcome is required")


class QuestionGenerationProvider(Protocol):
    """Adapter contract implemented by an AI or human-assisted generator."""

    def generate(self, request: GenerationRequest) -> Iterable[QuestionCandidate]:
        """Return candidate records; quality approval is performed separately."""
        ...
