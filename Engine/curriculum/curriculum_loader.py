"""
Question Factory OS v2.3
Curriculum Loader

Builds an immutable CurriculumModel from raw curriculum records.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from Engine.curriculum.curriculum_models import (
    ChapterModel,
    CurriculumModel,
    SubjectModel,
    SubtopicModel,
    UnitModel,
)


class CurriculumLoader:
    """
    Builds the complete curriculum hierarchy.

    Input:
        - subjects
        - units
        - chapters
        - subtopics

    Output:
        CurriculumModel
    """

    def load(
        self,
        *,
        subjects: list[dict[str, Any]],
        units: list[dict[str, Any]],
        chapters: list[dict[str, Any]],
        subtopics: list[dict[str, Any]],
    ) -> CurriculumModel:

        subtopics_by_chapter = self._build_subtopics(subtopics)

        chapters_by_unit = self._build_chapters(
            chapters,
            subtopics_by_chapter,
        )

        units_by_subject = self._build_units(
            units,
            chapters_by_unit,
        )

        curriculum_subjects = self._build_subjects(
            subjects,
            units_by_subject,
        )

        return CurriculumModel(
            subjects=tuple(curriculum_subjects)
        )

    # ------------------------------------------------------------------

    def _build_subtopics(
        self,
        rows: list[dict[str, Any]],
    ) -> dict[str, list[SubtopicModel]]:

        result: dict[str, list[SubtopicModel]] = defaultdict(list)

        ordered = sorted(
            rows,
            key=lambda r: (
                r.get("display_order", 0),
                r.get("code", ""),
            ),
        )

        for row in ordered:

            model = SubtopicModel(
                id=str(row["id"]),
                chapter_id=str(row["chapter_id"]),
                code=row["code"],
                name=row["subtopic_name"],
                display_order=row.get("display_order", 0),
                enabled=row.get("is_test_enabled", True),
            )

            result[model.chapter_id].append(model)

        return dict(result)

    # ------------------------------------------------------------------

    def _build_chapters(
        self,
        rows: list[dict[str, Any]],
        subtopics: dict[str, list[SubtopicModel]],
    ) -> dict[str, list[ChapterModel]]:

        result: dict[str, list[ChapterModel]] = defaultdict(list)

        ordered = sorted(
            rows,
            key=lambda r: (
                r.get("display_order", 0),
                r.get("code", ""),
            ),
        )

        for row in ordered:

            model = ChapterModel(
                id=str(row["id"]),
                unit_id=str(row["unit_id"]),
                code=row["code"],
                name=row["chapter_name"],
                display_order=row.get("display_order", 0),
                enabled=row.get("is_test_enabled", True),
                subtopics=tuple(
                    subtopics.get(str(row["id"]), [])
                ),
            )

            result[model.unit_id].append(model)

        return dict(result)

    # ------------------------------------------------------------------

    def _build_units(
        self,
        rows: list[dict[str, Any]],
        chapters: dict[str, list[ChapterModel]],
    ) -> dict[str, list[UnitModel]]:

        result: dict[str, list[UnitModel]] = defaultdict(list)

        ordered = sorted(
            rows,
            key=lambda r: (
                r.get("display_order", 0),
                r.get("code", ""),
            ),
        )

        for row in ordered:

            model = UnitModel(
                id=str(row["id"]),
                subject_id=str(row["subject_id"]),
                code=row["code"],
                name=row["unit_name"],
                display_order=row.get("display_order", 0),
                enabled=row.get("is_test_enabled", True),
                chapters=tuple(
                    chapters.get(str(row["id"]), [])
                ),
            )

            result[model.subject_id].append(model)

        return dict(result)

    # ------------------------------------------------------------------

    def _build_subjects(
        self,
        rows: list[dict[str, Any]],
        units: dict[str, list[UnitModel]],
    ) -> list[SubjectModel]:

        ordered = sorted(
            rows,
            key=lambda r: r.get("subject_name", ""),
        )

        subjects: list[SubjectModel] = []

        for row in ordered:

            subjects.append(
                SubjectModel(
                    id=str(row["id"]),
                    name=row["subject_name"],
                    enabled=row.get("is_test_enabled", True),
                    units=tuple(
                        units.get(str(row["id"]), [])
                    ),
                )
            )

        return subjects