"""
Question Factory OS v2.4
Manufacturing Work Item Model

Milestone : M14
Sprint    : S1
Release   : R1

Represents one executable manufacturing task.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ManufacturingWorkItemModel:
    """
    One executable manufacturing unit.

    One Work Item
        ↓
    One FactoryRunner execution
        ↓
    One CSV output
    """

    request_id: str

    work_item_id: str

    subject: str

    unit: str

    chapter: str

    subtopic: str

    set_no: str

    batch_no: int

    questions_per_batch: int

    question_start: int

    question_end: int

    qp_id: str = ""

    question_possibility: str = ""

    status: str = "PENDING"

    retries: int = 0

    def mark_running(self) -> None:

        self.status = "RUNNING"

    def mark_completed(self) -> None:

        self.status = "COMPLETED"

    def mark_failed(self) -> None:

        self.status = "FAILED"

    @property
    def batch_id(self) -> str:

        return (
            f"{self.subject}_"
            f"{self.unit}_"
            f"{self.chapter}_"
            f"{self.subtopic}_"
            f"{self.set_no}_"
            f"B{self.batch_no}"
        )

    @property
    def question_range(self) -> str:

        return (
            f"Q{self.question_start:03d}_"
            f"Q{self.question_end:03d}"
        )


__all__ = [
    "ManufacturingWorkItemModel",
]