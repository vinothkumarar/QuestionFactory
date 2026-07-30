"""
Question Factory OS v2.4
ONE_BATCH Manufacturing Strategy

Milestone : M14
Sprint    : S2
Release   : R1
"""

from __future__ import annotations

import uuid

from Engine.curriculum.manufacturing_queue import ManufacturingQueue
from Engine.curriculum.manufacturing_request_model import (
    ManufacturingRequestModel,
)
from Engine.curriculum.manufacturing_work_item_model import (
    ManufacturingWorkItemModel,
)
from Engine.curriculum.planner.base_strategy import (
    BaseManufacturingStrategy,
)


class OneBatchStrategy(BaseManufacturingStrategy):
    """
    Creates exactly one ManufacturingWorkItem
    from a ONE_BATCH manufacturing request.
    """

    def build(
        self,
        request: ManufacturingRequestModel,
    ) -> ManufacturingQueue:

        request.validate()

        queue = ManufacturingQueue()

        question_start = (
            (request.start_batch - 1)
            * request.questions_per_batch
        ) + 1

        question_end = (
            question_start
            + request.questions_per_batch
            - 1
        )

        work_item = ManufacturingWorkItemModel(
            request_id=request.request_id,
            work_item_id=f"WI_{uuid.uuid4().hex[:8].upper()}",
            subject=request.subject,
            unit=request.unit,
            chapter=request.chapter,
            subtopic=request.subtopic,
            set_no=request.start_set,
            batch_no=request.start_batch,
            questions_per_batch=request.questions_per_batch,
            question_start=question_start,
            question_end=question_end,
        )

        queue.enqueue(work_item)

        return queue