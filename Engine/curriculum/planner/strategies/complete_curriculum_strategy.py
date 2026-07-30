"""
Question Factory OS v2.4
Complete Curriculum Strategy

Expands an entire curriculum by delegating
each subject to SubjectStrategy.
"""

from __future__ import annotations

from copy import deepcopy

from Engine.curriculum.manufacturing_queue import ManufacturingQueue
from Engine.curriculum.manufacturing_request_model import ManufacturingRequestModel
from Engine.curriculum.planner.base_strategy import BaseManufacturingStrategy
from Engine.curriculum.planner.strategies.subject_strategy import SubjectStrategy
from Engine.curriculum.repositories.curriculum_repository import CurriculumRepository


class CompleteCurriculumStrategy(BaseManufacturingStrategy):
    """
    Expands the complete curriculum by delegating
    each subject to SubjectStrategy.
    """

    def __init__(
        self,
        repository: CurriculumRepository,
    ) -> None:
        self._repository = repository
        self._subject_strategy = SubjectStrategy(repository)

    def build(
        self,
        request: ManufacturingRequestModel,
    ) -> ManufacturingQueue:

        queue = ManufacturingQueue()

        subjects = self._repository.get_subjects()

        for subject in subjects:

            subject_request = deepcopy(request)
            subject_request.subject = subject

            subject_queue = self._subject_strategy.build(
                subject_request,
            )

            while subject_queue.has_next:

                queue.enqueue(
                    subject_queue.dequeue(),
                )

        return queue