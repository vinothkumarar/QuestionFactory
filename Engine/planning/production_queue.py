"""
Question Factory OS
Production Queue
"""

from __future__ import annotations

from collections import deque
from typing import Deque, cast

from Engine.models.production_order_model import (
    ProductionOrderModel,
)


class ProductionQueue:
    """
    FIFO queue used by the production pipeline.
    """

    def __init__(self) -> None:

        self.queue: Deque[ProductionOrderModel] = deque()

    def add(
        self,
        production_order: ProductionOrderModel,
    ) -> None:

        self.queue.append(production_order)

    def get(
        self,
    ) -> ProductionOrderModel | None:

        if not self.queue:

            return None

        return cast(
            ProductionOrderModel,
            self.queue.popleft(),
        )

    def size(
        self,
    ) -> int:

        return len(self.queue)

    def is_empty(
        self,
    ) -> bool:

        return len(self.queue) == 0