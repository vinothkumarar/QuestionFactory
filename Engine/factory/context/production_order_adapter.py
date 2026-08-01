"""
Question Factory OS v3.0

Production Order Adapter

Temporary adapter used during the v2.5 → v3.0 migration.

Converts a ManufacturingContext into the existing
ProductionOrderModel so the current FactoryRunner
can remain unchanged.
"""

from __future__ import annotations

from Engine.factory.context.manufacturing_context import (
    ManufacturingContext,
)

from Engine.models.production_order_model import (
    ProductionOrderModel,
)


class ProductionOrderAdapter:
    """
    Converts ManufacturingContext into
    ProductionOrderModel.
    """

    def build(
        self,
        context: ManufacturingContext,
    ) -> ProductionOrderModel:

        return ProductionOrderModel(
            order_id=context.order_id,
            subject=context.subject_code,
            unit=context.unit_code,
            chapter=context.chapter_code,
            subtopic=context.subtopic_code,
            set_no=context.set_no,
            batch_no=context.batch_no,
            question_start=context.question_start,
            question_count=context.question_count,
            status=context.status,
        )


__all__ = [
    "ProductionOrderAdapter",
]