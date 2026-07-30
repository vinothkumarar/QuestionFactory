"""
Question Factory OS v2.4
Curriculum Repository

Milestone : M17
Sprint    : S1
Release   : R1

Defines the abstraction for accessing
curriculum information.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class CurriculumRepository(ABC):
    """
    Abstract curriculum repository.

    Provides curriculum navigation for
    higher-level manufacturing strategies.
    """

    @abstractmethod
    def get_units(
        self,
        subject: str,
    ) -> list[str]:
        """
        Return all units for a subject.
        """
        raise NotImplementedError

    @abstractmethod
    def get_chapters(
        self,
        subject: str,
        unit: str,
    ) -> list[str]:
        """
        Return all chapters for a unit.
        """
        raise NotImplementedError

    @abstractmethod
    def get_subtopics(
        self,
        subject: str,
        unit: str,
        chapter: str,
    ) -> list[str]:
        """
        Return all subtopics for a chapter.
        """
        raise NotImplementedError

    @abstractmethod
    def get_sets(
        self,
        subject: str,
        unit: str,
        chapter: str,
        subtopic: str,
    ) -> list[str]:
        """
        Return available sets for a subtopic.
        """
        raise NotImplementedError

    @abstractmethod
    def get_batches(
        self,
        subject: str,
        unit: str,
        chapter: str,
        subtopic: str,
        set_no: str,
    ) -> list[int]:
        """
        Return available batch numbers.
        """
        raise NotImplementedError

    @abstractmethod
    def get_subjects(self) -> list[str]:
        """
        Return all available subjects.
        """
        raise NotImplementedError