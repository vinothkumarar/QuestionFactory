"""
Question Factory OS v2.5

Curriculum Production Planner

Converts a ManufacturingWorkItemModel into a
ProductionOrderModel.
"""

from __future__ import annotations

from Engine.curriculum.manufacturing_work_item_model import (
    ManufacturingWorkItemModel,
)

from Engine.models.production_order_model import (
    ProductionOrderModel,
)


class CurriculumProductionPlanner:
    """
    Builds a ProductionOrderModel from a
    ManufacturingWorkItemModel.
    """

    def plan(
        self,
        work_item: ManufacturingWorkItemModel,
    ) -> ProductionOrderModel:
        """
        Convert one curriculum work item into one
        production order.
        """

        question_start = work_item.question_start

        question_end = work_item.question_end

        order_id = (
            f"ORDER_"
            f"{work_item.subject}_"
            f"{work_item.unit}_"
            f"{work_item.chapter}_"
            f"{work_item.subtopic}_"
            f"{work_item.set_no}_"
            f"B{work_item.batch_no}_"
            f"Q{question_start}_{question_end}"
        )

        return ProductionOrderModel(
            order_id=order_id,
            subject=work_item.subject,
            unit=work_item.unit,
            chapter=work_item.chapter,
            subtopic=work_item.subtopic,
            set_no=work_item.set_no,
            batch_no=work_item.batch_no,
            question_start=question_start,
            question_count=work_item.questions_per_batch,
            status="PLANNED",
        )


__all__ = [
    "CurriculumProductionPlanner",
]