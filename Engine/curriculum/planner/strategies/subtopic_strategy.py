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

from Engine.qpc.qpc_loader import QPCLoader

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

        qpc_loader = QPCLoader()

        question_possibilities = qpc_loader.load(
            chapter_code=request.chapter,
            subtopic_code=request.subtopic,
        )

        for set_no in range(
            int(request.start_set[1:]),
            int(request.end_set[1:]) + 1,
        ):

            for qp in question_possibilities:

                work_item = ManufacturingWorkItemModel(
                    request_id=request.request_id,
                    work_item_id=(
                        f"WI_{uuid.uuid4().hex[:8].upper()}"
                    ),
                    subject=request.subject,
                    unit=request.unit,
                    chapter=request.chapter,
                    subtopic=request.subtopic,
                    set_no=f"S{set_no}",
                    batch_no=1,
                    questions_per_batch=request.questions_per_batch,
                    question_start=1,
                    question_end=request.questions_per_batch,

                    qp_id=qp["qp_id"],
                    question_possibility=qp["question_possibility"],
                )

                queue.enqueue(work_item)

        return queue