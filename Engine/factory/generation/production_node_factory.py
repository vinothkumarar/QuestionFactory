"""
Question Factory OS v2.2

Production Node Factory

Converts a ProductionOrderModel produced by the planning
subsystem into a ProductionNodeModel consumed by the
manufacturing subsystem.
"""

from __future__ import annotations

from Engine.models.production_node_model import (
    ProductionNodeModel,
)
from Engine.models.production_order_model import (
    ProductionOrderModel,
)


class ProductionNodeFactory:
    """
    Builds ProductionNodeModel instances from
    ProductionOrderModel instances.

    This class acts as the bridge between the
    Planning subsystem and the Manufacturing subsystem.
    """

    VERSION = "2.2.0"

    def build(
        self,
        order: ProductionOrderModel,
    ) -> ProductionNodeModel:
        """
        Convert a ProductionOrderModel into a
        ProductionNodeModel.
        """

        node = ProductionNodeModel()

        # -------------------------------------------------
        # Production Location
        # -------------------------------------------------

        node.location.subject = order.subject
        node.location.unit = order.unit
        node.location.chapter = order.chapter
        node.location.subtopic = order.subtopic

        if isinstance(order.set_no, str):
            node.location.set_number = int(
                order.set_no.replace("S", "")
            )
        else:
            node.location.set_number = int(order.set_no)

        node.location.batch_number = order.batch_no

        # -------------------------------------------------
        # Question Range
        # -------------------------------------------------

        node.question_range.question_from = (
            order.question_start
        )

        node.question_range.question_to = (
            order.question_start
            + order.question_count
            - 1
        )

        node.question_range.expected_questions = (
            order.question_count
        )

        # -------------------------------------------------
        # Metadata
        # -------------------------------------------------

        node.metadata.batch_id = order.order_id

        node.metadata.production_node = (
            f"{order.subject}_"
            f"{order.unit}_"
            f"{order.chapter}_"
            f"{order.subtopic}_"
            f"S{node.location.set_number}_"
            f"B{order.batch_no}"
        )

        node.status = order.status

        return node


__all__ = [
    "ProductionNodeFactory",
]
