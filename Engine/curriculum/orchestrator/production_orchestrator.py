"""
Question Factory OS v2.5
Production Orchestrator

Bridges the Curriculum Manufacturing layer
and the Question Factory production engine.
"""

from __future__ import annotations

from Engine.curriculum.integration.curriculum_production_planner import (
    CurriculumProductionPlanner,
)

from Engine.curriculum.manufacturing_work_item_model import (
    ManufacturingWorkItemModel,
)

from Engine.curriculum.runtime.factory_runtime_service import (
    FactoryRuntimeService,
)

from Engine.factory.factory_runner import (
    FactoryRunner,
)


class ProductionOrchestrator:
    """
    Bridges Curriculum Manufacturing and the
    Question Factory production engine.

    Responsibilities
    ----------------
    1. Prepare runtime.
    2. Convert WorkItem -> ProductionOrder.
    3. Execute FactoryRunner using the supplied
       ProductionOrder.
    """

    VERSION = "2.5.0"

    def __init__(
        self,
        runtime_service: FactoryRuntimeService,
        factory_runner: FactoryRunner,
        planner: CurriculumProductionPlanner,
    ) -> None:

        self._runtime_service = runtime_service
        self._factory_runner = factory_runner
        self._planner = planner

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(
        self,
        work_item: ManufacturingWorkItemModel,
    ) -> int:
        """
        Execute one curriculum manufacturing work item.
        """

        #
        # Prepare runtime
        #

        self._runtime_service.prepare(
            work_item,
        )

        #
        # Convert to ProductionOrder
        #

        production_order = self._planner.plan(
            work_item,
        )

        #
        # Execute production
        #

        return self._factory_runner.run_production_order(
            production_order,
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def component_name(
        self,
    ) -> str:

        return self.__class__.__name__

    @property
    def version(
        self,
    ) -> str:

        return self.VERSION

    def health(
        self,
    ) -> dict[str, object]:

        return {
            "component": self.component_name,
            "version": self.version,
            "status": "READY",
        }

    def diagnostics(
        self,
    ) -> dict[str, object]:

        return {
            "component": self.component_name,
            "version": self.version,
            "runtime_service": (
                self._runtime_service.__class__.__name__
            ),
            "factory_runner": (
                self._factory_runner.__class__.__name__
            ),
            "planner": (
                self._planner.__class__.__name__
            ),
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.component_name}"
            f"(version='{self.version}')"
        )

    def __str__(
        self,
    ) -> str:

        return (
            f"{self.component_name} "
            f"[v{self.version}]"
        )


__all__ = [
    "ProductionOrchestrator",
]