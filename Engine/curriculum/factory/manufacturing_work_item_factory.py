"""
Question Factory OS v2.4
Manufacturing Work Item Factory

Milestone : M16
Sprint    : S2
Release   : R1
"""

from __future__ import annotations

import uuid

from Engine.curriculum.manufacturing_request_model import (
    ManufacturingRequestModel,
)
from Engine.curriculum.manufacturing_work_item_model import (
    ManufacturingWorkItemModel,
)


class ManufacturingWorkItemFactory:
    """
    Factory responsible for creating
    ManufacturingWorkItemModel instances.
    """

    def create(
        self,
        request: ManufacturingRequestModel,
        batch_no: int,
    ) -> ManufacturingWorkItemModel:

        return ManufacturingWorkItemModel(
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