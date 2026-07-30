"""
Question Factory OS v2.4
In-Memory Curriculum Repository

Milestone : M17
Sprint    : S2
Release   : R1
"""

from __future__ import annotations

from Engine.curriculum.repositories.curriculum_repository import (
    CurriculumRepository,
)


class InMemoryCurriculumRepository(
    CurriculumRepository,
):
    """
    Temporary in-memory curriculum repository.

    This implementation exists solely to validate
    curriculum-aware manufacturing without requiring
    a database.
    """

    def __init__(self) -> None:

        #
        # Temporary sample curriculum.
        #
        # Replace this later with Supabase.
        #

        self._curriculum = {

            "Physics": {

                "P1": {

                    "CH1": [

                        "ST1",

                        "ST2",

                        "ST3",

                        "ST4",

                    ]

                }

            }

        }

    def get_units(
        self,
        subject: str,
    ) -> list[str]:

        return list(
            self._curriculum.get(
                subject,
                {},
            ).keys()
        )

    def get_chapters(
        self,
        subject: str,
        unit: str,
    ) -> list[str]:

        return list(

            self._curriculum.get(
                subject,
                {},
            ).get(
                unit,
                {},
            ).keys()

        )

    def get_subjects(self) -> list[str]:
        return list(self._curriculum.keys())

    def get_subtopics(
        self,
        subject: str,
        unit: str,
        chapter: str,
    ) -> list[str]:

        return list(

            self._curriculum.get(
                subject,
                {},
            ).get(
                unit,
                {},
            ).get(
                chapter,
                [],
            )

        )

    def get_sets(
        self,
        subject: str,
        unit: str,
        chapter: str,
        subtopic: str,
    ) -> list[str]:

        #
        # Current factory standard.
        #

        return [

            "S1",

            "S2",

            "S3",

            "S4",

            "S5",

        ]

    def get_batches(
        self,
        subject: str,
        unit: str,
        chapter: str,
        subtopic: str,
        set_no: str,
    ) -> list[int]:

        #
        # Temporary implementation.
        #

        return list(range(1, 6))