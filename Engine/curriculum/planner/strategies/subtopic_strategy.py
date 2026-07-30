"""
Question Factory OS v2.4
SUBTOPIC Manufacturing Strategy

Milestone : M16
Sprint    : S1
Release   : R1
"""

from __future__ import annotations

import uuid

from Engine.curriculum.manufacturing_queue import (
    ManufacturingQueue,
)
from Engine.curriculum.manufacturing_request_model import (
    ManufacturingRequestModel,
)
from Engine.curriculum.manufacturing_work_item_model import (
    ManufacturingWorkItemModel,
)
from Engine.curriculum.planner.base_strategy import (
    BaseManufacturingStrategy,
)


class SubtopicStrategy(BaseManufacturingStrategy):
    """
    Expands a SUBTOPIC request into one
    ManufacturingWorkItem per batch.
    """

    def build(
        self,
        request: ManufacturingRequestModel,
    ) -> ManufacturingQueue:

        request.validate()

        queue = ManufacturingQueue()

        for batch_no in range(
            request.start_batch,
            request.end_batch + 1,
        ):

            work_item = ManufacturingWorkItemModel(
                request_id=request.request_id,
                work_item_id=(
                    f"WI_{uuid.uuid4().hex[:8].upper()}"
                ),
                subject=request.subject,
                unit=request.unit,
                chapter=request.chapter,
                subtopic=request.subtopic,
                set_no=request.start_set,
                batch_no=batch_no,
                questions_per_batch=request.questions_per_batch,
                question_start=0,
                question_end=0,
            )

            queue.enqueue(
                work_item
            )

        return queue