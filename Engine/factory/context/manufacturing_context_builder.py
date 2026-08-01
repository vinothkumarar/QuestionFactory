"""
Question Factory OS v3.0

Manufacturing Context Builder

Builds the canonical ManufacturingContext from a
ManufacturingWorkItemModel.
"""

from __future__ import annotations

from Engine.curriculum.manufacturing_work_item_model import (
    ManufacturingWorkItemModel,
)

from Engine.factory.context.manufacturing_context import (
    ManufacturingContext,
)


class ManufacturingContextBuilder:
    """
    Builds the canonical ManufacturingContext.
    """

    def build(
        self,
        work_item: ManufacturingWorkItemModel,
    ) -> ManufacturingContext:

        question_start = work_item.question_start

        order_id = (
            f"ORDER_"
            f"{work_item.subject}_"
            f"{work_item.unit}_"
            f"{work_item.chapter}_"
            f"{work_item.subtopic}_"
            f"{work_item.set_no}_"
            f"B{work_item.batch_no}_"
            f"Q{question_start}_"
            f"{work_item.question_end}"
        )

        return ManufacturingContext(
            request_id=work_item.request_id,
            scope="CURRICULUM",

            subject_code=work_item.subject,
            subject_name="",

            unit_code=work_item.unit,
            unit_name="",

            chapter_code=work_item.chapter,
            chapter_name="",

            subtopic_code=work_item.subtopic,
            subtopic_name="",

            set_no=work_item.set_no,

            batch_no=work_item.batch_no,

            question_start=work_item.question_start,

            question_count=work_item.questions_per_batch,

            order_id=order_id,
        )


__all__ = [
    "ManufacturingContextBuilder",
]