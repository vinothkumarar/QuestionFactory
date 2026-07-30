"""
Question Factory OS v2.4
Manufacturing Request Model

Milestone : M14
Sprint    : S1
Release   : R1

Defines a curriculum manufacturing request.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import uuid

from Engine.curriculum.manufacturing_scope import (
    ManufacturingScope,
)



@dataclass(slots=True)
class ManufacturingRequestModel:
    """
    High-level manufacturing request.

    This model describes WHAT should be manufactured.
    """

    scope: ManufacturingScope
    subject: str

    request_id: str = field(
        default_factory=lambda: (
            f"REQ_{uuid.uuid4().hex[:12].upper()}"
        )
    )

   
    unit: str = ""

    chapter: str = ""

    subtopic: str = ""

    start_set: str = "S1"

    end_set: str = "S5"

    start_batch: int = 1

    end_batch: int = 1

    questions_per_batch: int = 20

    auto_commit: bool = True

    stop_on_failure: bool = True

    def validate(self) -> None:
        """
        Validate request consistency.
        """

        if self.start_batch < 1:
            raise ValueError(
                "start_batch must be >= 1"
            )

        if self.end_batch < self.start_batch:
            raise ValueError(
                "end_batch cannot be smaller than start_batch"
            )

        if self.questions_per_batch < 1:
            raise ValueError(
                "questions_per_batch must be >= 1"
            )


__all__ = [
    "ManufacturingRequestModel",
]