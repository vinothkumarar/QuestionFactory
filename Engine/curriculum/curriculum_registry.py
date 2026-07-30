"""
Question Factory OS v2.2
========================

Curriculum Registry

Provides high-performance access to the complete curriculum.

Responsibilities
----------------
- Own the curriculum graph
- Build lookup indexes
- Provide O(1) access
- Resolve complete curriculum paths

The registry NEVER reads CSV files.
Loading is delegated to CurriculumLoader.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from Engine.curriculum.loader import CurriculumData
from Engine.curriculum.loader import CurriculumLoader

from Engine.curriculum.models import (
    SubjectModel,
    UnitModel,
    ChapterModel,
    SubtopicModel,
)


# ============================================================
# Curriculum Path
# ============================================================


@dataclass(frozen=True, slots=True)
class CurriculumPath:
    """
    Complete curriculum hierarchy.
    """

    subject: SubjectModel
    unit: UnitModel
    chapter: ChapterModel
    subtopic: SubtopicModel


# ============================================================
# Registry
# ============================================================


class CurriculumRegistry:

    def __init__(self, curriculum_root: Path):

        loader = CurriculumLoader(curriculum_root)

        self._data: CurriculumData = loader.load()

        loader.validate()

        # ----------------------------------------------------
        # UUID Indexes
        # ----------------------------------------------------

        self._subjects_by_uuid: dict[str, SubjectModel] = {}

        self._units_by_uuid: dict[str, UnitModel] = {}

        self._chapters_by_uuid: dict[str, ChapterModel] = {}

        self._subtopics_by_uuid: dict[str, SubtopicModel] = {}

        # ----------------------------------------------------
        # Code Indexes
        # ----------------------------------------------------

        self._subjects_by_code: dict[str, SubjectModel] = {}

        self._units_by_key: dict[
            tuple[str, str],
            UnitModel,
        ] = {}

        self._chapters_by_key: dict[
            tuple[str, str],
            ChapterModel,
        ] = {}

        self._subtopics_by_key: dict[
            tuple[str, str],
            SubtopicModel,
        ] = {}

        # ----------------------------------------------------
        # Parent → Children
        # ----------------------------------------------------

        self._units_by_subject: dict[
            str,
            list[UnitModel],
        ] = {}

        self._chapters_by_unit: dict[
            str,
            list[ChapterModel],
        ] = {}

        self._subtopics_by_chapter: dict[
            str,
            list[SubtopicModel],
        ] = {}

        # ----------------------------------------------------
        # Child → Parent
        # ----------------------------------------------------

        self._subject_of_unit: dict[
            str,
            SubjectModel,
        ] = {}

        self._unit_of_chapter: dict[
            str,
            UnitModel,
        ] = {}

        self._chapter_of_subtopic: dict[
            str,
            ChapterModel,
        ] = {}

        self._build_indexes()
    # ---------------------------------------------------------
    # Index Builder
    # ---------------------------------------------------------

    def _build_indexes(self) -> None:

        # -----------------------------------------------------
        # Subjects
        # -----------------------------------------------------

        for subject in self._data.subjects:

            self._subjects_by_uuid[subject.id] = subject
            self._subjects_by_code[subject.code] = subject

            self._units_by_subject.setdefault(
                subject.id,
                [],
            )

        # -----------------------------------------------------
        # Units
        # -----------------------------------------------------

        for unit in self._data.units:

            self._units_by_uuid[unit.id] = unit

            if unit.subject_id not in self._subjects_by_uuid:
                raise ValueError(
                    f"Unknown Subject UUID "
                    f"'{unit.subject_id}' "
                    f"referenced by "
                    f"Unit '{unit.code}'."
                )

            subject = self._subjects_by_uuid[unit.subject_id]

            self._units_by_key[
                (
                    subject.code,
                    unit.code,
                )
            ] = unit

            self._units_by_subject.setdefault(
                subject.id,
                [],
            ).append(unit)

            self._subject_of_unit[
                unit.id
            ] = subject

            self._chapters_by_unit.setdefault(
                unit.id,
                [],
            )

        # -----------------------------------------------------
        # Chapters
        # -----------------------------------------------------

        for chapter in self._data.chapters:

            self._chapters_by_uuid[
                chapter.id
            ] = chapter

            if chapter.unit_id not in self._units_by_uuid:
                raise ValueError(
                    f"Unknown Unit UUID "
                    f"'{chapter.unit_id}' "
                    f"referenced by "
                    f"Chapter '{chapter.code}'."
                )

            unit = self._units_by_uuid[chapter.unit_id]

            subject = self._subject_of_unit[
                unit.id
            ]

            self._chapters_by_key[
                (
                    unit.code,
                    chapter.code,
                )
            ] = chapter

            self._chapters_by_unit.setdefault(
                unit.id,
                [],
            ).append(chapter)

            self._unit_of_chapter[
                chapter.id
            ] = unit

            self._subtopics_by_chapter.setdefault(
                chapter.id,
                [],
            )

        # -----------------------------------------------------
        # Subtopics
        # -----------------------------------------------------

        for subtopic in self._data.subtopics:

            self._subtopics_by_uuid[
                subtopic.id
            ] = subtopic

            if subtopic.chapter_id not in self._chapters_by_uuid:
                raise ValueError(
                    f"Unknown Chapter UUID "
                    f"'{subtopic.chapter_id}' "
                    f"referenced by "
                    f"Subtopic '{subtopic.code}'."
                )

            chapter = self._chapters_by_uuid[subtopic.chapter_id]

            self._subtopics_by_key[
                (
                    chapter.id,
                    subtopic.code,
                )
            ] = subtopic

            self._subtopics_by_chapter.setdefault(
                chapter.id,
                [],
            ).append(subtopic)

            self._chapter_of_subtopic[
                subtopic.id
            ] = chapter
    # ---------------------------------------------------------
    # UUID Lookups
    # ---------------------------------------------------------

    def subject(self, subject_uuid: str) -> SubjectModel:
        return self._subjects_by_uuid[subject_uuid]

    def unit(self, unit_uuid: str) -> UnitModel:
        return self._units_by_uuid[unit_uuid]

    def chapter(self, chapter_uuid: str) -> ChapterModel:
        return self._chapters_by_uuid[chapter_uuid]

    def subtopic(self, subtopic_uuid: str) -> SubtopicModel:
        return self._subtopics_by_uuid[subtopic_uuid]

    # ---------------------------------------------------------
    # Business Code Lookups
    # ---------------------------------------------------------

    def subject_by_code(
        self,
        subject_code: str,
    ) -> SubjectModel:
        return self._subjects_by_code[subject_code]

    def unit_by_code(
        self,
        subject_code: str,
        unit_code: str,
    ) -> UnitModel:
        return self._units_by_key[
            (
                subject_code,
                unit_code,
            )
        ]

    def chapter_by_code(
        self,
        unit_code: str,
        chapter_code: str,
    ) -> ChapterModel:
        return self._chapters_by_key[
            (
                unit_code,
                chapter_code,
            )
        ]

    def subtopic_by_code(
        self,
        chapter_uuid: str,
        subtopic_code: str,
    ) -> SubtopicModel:
        return self._subtopics_by_key[
            (
                chapter_uuid,
                subtopic_code,
            )
        ]

    # ---------------------------------------------------------
    # Parent Navigation
    # ---------------------------------------------------------

    def subject_of_unit(
        self,
        unit_uuid: str,
    ) -> SubjectModel:
        return self._subject_of_unit[unit_uuid]

    def unit_of_chapter(
        self,
        chapter_uuid: str,
    ) -> UnitModel:
        return self._unit_of_chapter[chapter_uuid]

    def chapter_of_subtopic(
        self,
        subtopic_uuid: str,
    ) -> ChapterModel:
        return self._chapter_of_subtopic[subtopic_uuid]

    # ---------------------------------------------------------
    # Child Navigation
    # ---------------------------------------------------------

    def units(
        self,
        subject_uuid: str,
    ) -> list[UnitModel]:
        return self._units_by_subject.get(
            subject_uuid,
            [],
        )

    def chapters(
        self,
        unit_uuid: str,
    ) -> list[ChapterModel]:
        return self._chapters_by_unit.get(
            unit_uuid,
            [],
        )

    def subtopics(
        self,
        chapter_uuid: str,
    ) -> list[SubtopicModel]:
        return self._subtopics_by_chapter.get(
            chapter_uuid,
            [],
        )

    # ---------------------------------------------------------
    # Resolve
    # ---------------------------------------------------------

    def resolve(
        self,
        subtopic_uuid: str,
    ) -> CurriculumPath:

        subtopic = self.subtopic(
            subtopic_uuid
        )

        chapter = self.chapter_of_subtopic(
            subtopic_uuid
        )

        unit = self.unit_of_chapter(
            chapter.id
        )

        subject = self.subject_of_unit(
            unit.id
        )

        return CurriculumPath(
            subject=subject,
            unit=unit,
            chapter=chapter,
            subtopic=subtopic,
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def subject_count(self) -> int:
        return len(self._subjects_by_uuid)

    @property
    def unit_count(self) -> int:
        return len(self._units_by_uuid)

    @property
    def chapter_count(self) -> int:
        return len(self._chapters_by_uuid)

    @property
    def subtopic_count(self) -> int:
        return len(self._subtopics_by_uuid)

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "CurriculumRegistry("
            f"subjects={self.subject_count}, "
            f"units={self.unit_count}, "
            f"chapters={self.chapter_count}, "
            f"subtopics={self.subtopic_count}"
            ")"
        )
      