"""
Question Factory OS v2.4
Curriculum Manufacturing Planner

Milestone : M14
Sprint    : S2
Release   : R1

Converts a ManufacturingRequest into a
ManufacturingQueue using the registered strategy.
"""

from __future__ import annotations

from Engine.curriculum.manufacturing_queue import (
    ManufacturingQueue,
)
from Engine.curriculum.manufacturing_request_model import (
    ManufacturingRequestModel,
)
from Engine.curriculum.planner.strategy_registry import (
    StrategyRegistry,
)


class CurriculumManufacturingPlanner:
    """
    High-level planner responsible for converting
    a ManufacturingRequest into a ManufacturingQueue.
    """

    def __init__(
        self,
        registry: StrategyRegistry | None = None,
    ) -> None:

        self._registry = registry or StrategyRegistry()

    def build(
        self,
        request: ManufacturingRequestModel,
    ) -> ManufacturingQueue:
        """
        Build a manufacturing queue from
        the supplied request.
        """

        request.validate()

        strategy = self._registry.get(
            request.scope
        )

        return strategy.build(request)