"""
Question Factory OS v2.5

Curriculum Service Container

Composition root for the Curriculum Manufacturing
subsystem.
"""
from __future__ import annotations

from pathlib import Path

from Engine.curriculum.curriculum_registry import (
    CurriculumRegistry,
)


import logging
from functools import cached_property

from Engine.bootstrap.service_container import ServiceContainer

from Engine.factory.factory_runner import FactoryRunner

from Engine.curriculum.integration.curriculum_production_planner import (
    CurriculumProductionPlanner,
)

from Engine.curriculum.runtime.factory_runtime_service import (
    FactoryRuntimeService,
)

from Engine.curriculum.orchestrator.production_orchestrator import (
    ProductionOrchestrator,
)

from Engine.curriculum.execution.manufacturing_work_item_executor import (
    ManufacturingWorkItemExecutor,
)

from Engine.curriculum.runner.curriculum_manufacturing_runner import (
    CurriculumManufacturingRunner,
)
from Engine.curriculum.planner.curriculum_manufacturing_planner import (
    CurriculumManufacturingPlanner,
)

LOGGER = logging.getLogger(__name__)


class CurriculumServiceContainer:
    """
    Composition root for Curriculum Manufacturing.

    Reuses the existing Question Factory
    ServiceContainer while constructing the
    curriculum execution pipeline.
    """

    VERSION = "2.5.0"

    def __init__(
        self,
        factory_container: ServiceContainer | None = None,
    ) -> None:

        self._logger = LOGGER

        self._factory_container = (
            factory_container
            if factory_container is not None
            else ServiceContainer()
        )

    # ---------------------------------------------------------
    # Shared Services
    # ---------------------------------------------------------

    @property
    def factory_container(
        self,
    ) -> ServiceContainer:

        return self._factory_container

    @cached_property
    def runtime_service(
        self,
    ) -> FactoryRuntimeService:

        self._logger.info(
            "Creating FactoryRuntimeService."
        )

        return FactoryRuntimeService()

    @cached_property
    def curriculum_registry(
        self,
    ) -> CurriculumRegistry:

        self._logger.info(
            "Creating CurriculumRegistry."
        )

        return CurriculumRegistry(
            Path("Engine/curriculum")
        )

    @cached_property
    def production_planner(
        self,
    ) -> CurriculumProductionPlanner:

        self._logger.info(
            "Creating CurriculumProductionPlanner."
        )

        return CurriculumProductionPlanner()
            

    @cached_property
    def factory_runner(
        self,
    ) -> FactoryRunner:
        """
        Shared FactoryRunner.
        """

        self._logger.info(
            "Creating FactoryRunner."
        )

        return FactoryRunner()

    @cached_property
    def manufacturing_runner(
        self,
    ) -> CurriculumManufacturingRunner:

        self._logger.info(
            "Creating CurriculumManufacturingRunner."
        )

        return CurriculumManufacturingRunner(
            planner=self.manufacturing_planner,
            executor=self.work_item_executor,
        )
            
    @cached_property
    def production_orchestrator(
        self,
    ) -> ProductionOrchestrator:
        """
        Shared ProductionOrchestrator.
        """

        self._logger.info(
            "Creating ProductionOrchestrator."
        )

        return ProductionOrchestrator(
            runtime_service=self.runtime_service,
            factory_runner=self.factory_runner,
            planner=self.production_planner,
        )

    @cached_property
    def work_item_executor(
        self,
    ) -> ManufacturingWorkItemExecutor:
        """
        Shared ManufacturingWorkItemExecutor.
        """

        self._logger.info(
            "Creating ManufacturingWorkItemExecutor."
        )

        return ManufacturingWorkItemExecutor(
            orchestrator=self.production_orchestrator,
        )

    

    @cached_property
    def manufacturing_planner(
        self,
    ) -> CurriculumManufacturingPlanner:

        self._logger.info(
            "Creating CurriculumManufacturingPlanner."
        )

        return CurriculumManufacturingPlanner()
    # ---------------------------------------------------------
    # Health & Diagnostics
    # ---------------------------------------------------------

    def health(
        self,
    ) -> dict[str, bool]:
        """
        Return the health of the curriculum container.
        """

        return {
            "factory_container": (
                self._factory_container is not None
            ),
            "runtime_service": (
                "runtime_service" in self.__dict__
            ),
            "manufacturing_planner": (
                "manufacturing_planner" in self.__dict__
            ),

            "production_planner": (
                "production_planner" in self.__dict__
            ),
            "factory_runner": (
                "factory_runner" in self.__dict__
            ),
            "production_orchestrator": (
                "production_orchestrator"
                in self.__dict__
            ),
            "work_item_executor": (
                "work_item_executor"
                in self.__dict__
            ),
            "manufacturing_runner": (
                "manufacturing_runner"
                in self.__dict__
            ),
        }

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return diagnostics for the curriculum container.
        """

        return {
            "component": self.__class__.__name__,
            "version": self.VERSION,
            "health": self.health(),
        }

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset container state.
        """

        self._logger.info(
            "CurriculumServiceContainer reset."
        )

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown container.
        """

        self._logger.info(
            "CurriculumServiceContainer shutdown."
        )

    # ---------------------------------------------------------
    # Representation
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
    "CurriculumServiceContainer",
]