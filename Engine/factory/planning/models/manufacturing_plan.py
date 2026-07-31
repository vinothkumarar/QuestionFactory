"""
Question Factory OS v3.1
Manufacturing Plan
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ManufacturingPlan:
    subject_id: str

    unit_id: str

    chapter_id: str

    subtopic_id: str

    total_questions: int

    archetype_distribution: dict[str, int]

    difficulty_distribution: dict[str, int]

    analysis_summary: str

    manufacturing_notes: list[str]