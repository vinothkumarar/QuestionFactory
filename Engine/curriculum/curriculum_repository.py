"""
Question Factory OS v2.3
Curriculum Repository

Read-only access to the curriculum hierarchy.
"""

from __future__ import annotations

from Engine.curriculum.curriculum_models import (
    ChapterModel,
    CurriculumModel,
    SubjectModel,
    SubtopicModel,
    UnitModel,
)


class CurriculumRepository:

    def __init__(
        self,
        curriculum: CurriculumModel,
    ) -> None:

        self._curriculum = curriculum

    # ---------------------------------------------------------
    # Root
    # ---------------------------------------------------------

    def curriculum(self) -> CurriculumModel:
        return self._curriculum

    # ---------------------------------------------------------
    # Subjects
    # ---------------------------------------------------------

    def subjects(self) -> tuple[SubjectModel, ...]:
        return self._curriculum.subjects

    def subject(
        self,
        subject_id: str,
    ) -> SubjectModel | None:

        for subject in self._curriculum.subjects:

            if subject.id == subject_id:
                return subject

        return None

    # ---------------------------------------------------------
    # Subject Lookup
    # ---------------------------------------------------------

    def subject_by_name(
        self,
        name: str,
    ) -> SubjectModel | None:

        name = name.strip().lower()

        for subject in self._curriculum.subjects:

            if subject.name.lower() == name:
                return subject

        return None

    # ---------------------------------------------------------
    # Unit Lookup
    # ---------------------------------------------------------

    def unit_by_code(
        self,
        code: str,
    ) -> UnitModel | None:

        code = code.strip().upper()

        for subject in self._curriculum.subjects:

            for unit in subject.units:

                if unit.code.upper() == code:
                    return unit

        return None

    # ---------------------------------------------------------
    # Chapter Lookup
    # ---------------------------------------------------------

    def chapter_by_code(
        self,
        code: str,
    ) -> ChapterModel | None:

        code = code.strip().upper()

        for subject in self._curriculum.subjects:

            for unit in subject.units:

                for chapter in unit.chapters:

                    if chapter.code.upper() == code:
                        return chapter

        return None

    # ---------------------------------------------------------
    # Subtopic Lookup
    # ---------------------------------------------------------

    def subtopic_by_code(
        self,
        code: str,
    ) -> SubtopicModel | None:

        code = code.strip().upper()

        for subject in self._curriculum.subjects:

            for unit in subject.units:

                for chapter in unit.chapters:

                    for subtopic in chapter.subtopics:

                        if subtopic.code.upper() == code:
                            return subtopic

        return None

    # ---------------------------------------------------------
    # Units
    # ---------------------------------------------------------

    def units(
        self,
        subject_id: str,
    ) -> tuple[UnitModel, ...]:

        subject = self.subject(subject_id)

        if subject is None:
            return ()

        return subject.units

    def unit(
        self,
        unit_id: str,
    ) -> UnitModel | None:

        for subject in self._curriculum.subjects:

            for unit in subject.units:

                if unit.id == unit_id:
                    return unit

        return None

    def enabled_subjects(
        self,
    ) -> tuple[SubjectModel, ...]:

        return tuple(
            subject
            for subject in self._curriculum.subjects
            if subject.enabled
        )

    # ---------------------------------------------------------
    # Chapters
    # ---------------------------------------------------------

    def chapters(
        self,
        unit_id: str,
    ) -> tuple[ChapterModel, ...]:

        unit = self.unit(unit_id)

        if unit is None:
            return ()

        return unit.chapters

    def chapter(
        self,
        chapter_id: str,
    ) -> ChapterModel | None:

        for subject in self._curriculum.subjects:

            for unit in subject.units:

                for chapter in unit.chapters:

                    if chapter.id == chapter_id:
                        return chapter

        return None

    # ---------------------------------------------------------
    # Subtopics
    # ---------------------------------------------------------

    def subtopics(
        self,
        chapter_id: str,
    ) -> tuple[SubtopicModel, ...]:

        chapter = self.chapter(chapter_id)

        if chapter is None:
            return ()

        return chapter.subtopics

    def subtopic(
        self,
        subtopic_id: str,
    ) -> SubtopicModel | None:

        for subject in self._curriculum.subjects:

            for unit in subject.units:

                for chapter in unit.chapters:

                    for subtopic in chapter.subtopics:

                        if subtopic.id == subtopic_id:
                            return subtopic

        return None