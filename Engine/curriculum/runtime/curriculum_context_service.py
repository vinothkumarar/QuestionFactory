"""
Question Factory OS v3.0

Curriculum Context Service

Resolves curriculum names from production codes.
"""

from __future__ import annotations

from pathlib import Path

from Engine.curriculum.curriculum_registry import (
    CurriculumRegistry,
)

from Engine.models.production_order_model import (
    ProductionOrderModel,
)


class CurriculumContextService:
    """
    Resolves curriculum names from codes.
    """

    def __init__(self) -> None:

        self._registry = CurriculumRegistry(
            Path("Engine/curriculum"),
        )

    def enrich(
        self,
        order: ProductionOrderModel,
    ) -> dict[str, str]:

        subject = self._registry.subject_by_code(
            order.subject,
        )

        unit = self._registry.unit_by_code(
            order.subject,
            order.unit,
        )

        chapter = self._registry.chapter_by_code(
            order.unit,
            order.chapter,
        )

        subtopic = self._registry.subtopic_by_code(
            chapter.id,
            order.subtopic,
        )

        return {
            "subject_name": subject.name,
            "unit_name": unit.name,
            "chapter_name": chapter.name,
            "subtopic_name": subtopic.name,
        }


__all__ = [
    "CurriculumContextService",
]