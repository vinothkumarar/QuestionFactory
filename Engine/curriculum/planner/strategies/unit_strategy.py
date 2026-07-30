"""
Question Factory OS v2.4
Unit Strategy

Expands a unit request into
chapter/subtopic work items.
"""

from __future__ import annotations

from Engine.curriculum.manufacturing_queue import ManufacturingQueue
from Engine.curriculum.manufacturing_request_model import ManufacturingRequestModel
from Engine.curriculum.manufacturing_work_item_model import ManufacturingWorkItemModel
from Engine.curriculum.planner.base_strategy import BaseManufacturingStrategy
from Engine.curriculum.repositories.curriculum_repository import CurriculumRepository


class UnitStrategy(BaseManufacturingStrategy):
    """
    Expands a unit into chapter/subtopic work items.
    """

    def __init__(
        self,
        repository: CurriculumRepository,
    ) -> None:
        self._repository = repository

    def build(
        self,
        request: ManufacturingRequestModel,
    ) -> ManufacturingQueue:

        queue = ManufacturingQueue()

        chapters = self._repository.get_chapters(
            request.subject,
            request.unit,
        )

        for chapter in chapters:

            subtopics = self._repository.get_subtopics(
                request.subject,
                request.unit,
                chapter,
            )

            for subtopic in subtopics:

                for batch_no in range(
                    request.start_batch,
                    request.end_batch + 1,
                ):

                    work_item = ManufacturingWorkItemModel(
                        request_id=request.request_id,
                        work_item_id=(
                            f"{request.request_id}_{chapter}_{subtopic}_B{batch_no}"
                        ),
                        subject=request.subject,
                        unit=request.unit,
                        chapter=chapter,
                        subtopic=subtopic,
                        set_no=request.start_set,
                        batch_no=batch_no,
                        questions_per_batch=request.questions_per_batch,
                        question_start=0,
                        question_end=0,
                    )

                    queue.enqueue(work_item)

        return queue