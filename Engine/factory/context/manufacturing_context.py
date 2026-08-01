"""
Question Factory OS v3.0

Manufacturing Context

Single runtime object passed through the entire
manufacturing pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ManufacturingContext:
    """
    Canonical runtime manufacturing context.
    """

    #
    # Request
    #

    request_id: str

    scope: str

    #
    # Curriculum
    #

    subject_code: str
    subject_name: str

    unit_code: str
    unit_name: str

    chapter_code: str
    chapter_name: str

    subtopic_code: str
    subtopic_name: str

    #
    # Production
    #

    set_no: str

    batch_no: int

    question_start: int

    question_count: int

    #
    # Runtime
    #

    order_id: str

    status: str = "PLANNED"

    retries: int = 0

    #
    # AI
    #

    academic_analysis: dict[str, Any] = field(
        default_factory=dict,
    )

    #
    # Output
    #

    generated_questions: list[Any] = field(
        default_factory=list,
    )

    diagnostics: list[str] = field(
        default_factory=list,
    )


__all__ = [
    "ManufacturingContext",
]