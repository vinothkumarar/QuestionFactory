"""
Question Factory OS v2.1

Manufacturing Director

Central orchestration layer responsible for executing one
complete manufacturing cycle.

Pipeline
--------
Runtime
    ↓
Blueprint
    ↓
Production Scheduler
    ↓
Question Generator
    ↓
R01 Validation
    ↓
R02 Validation
    ↓
R03 Validation
    ↓
Repair (if required)
    ↓
Production Report
    ↓
Runtime Update
"""

from __future__ import annotations

import logging

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from Engine.blueprint.blueprint_loader import BlueprintLoader
from Engine.director.production_scheduler import ProductionScheduler
from Engine.director.runtime_controller import RuntimeController

from Engine.factory.generation.question_generator import (
    QuestionGenerator,
)

from Engine.factory.repair.repair_engine import (
    RepairEngine,
)

from Engine.factory.validation.r01_validator import (
    R01Validator,
)

from Engine.factory.validation.r02_validator import (
    R02Validator,
)

from Engine.factory.validation.r03_validator import (
    R03Validator,
)

from Engine.reporting.production_report import (
    ProductionReport,
)

from Engine.models.generated_question_model import (
    GeneratedQuestionModel,
)

from Engine.models.question_batch_model import (
    QuestionBatchModel,
)


class FactoryState(Enum):
    """
    Manufacturing lifecycle state.
    """

    IDLE = "IDLE"
    INITIALIZING = "INITIALIZING"
    LOADING_RUNTIME = "LOADING_RUNTIME"
    LOADING_BLUEPRINT = "LOADING_BLUEPRINT"
    SCHEDULING = "SCHEDULING"
    GENERATING = "GENERATING"
    VALIDATING = "VALIDATING"
    REPAIRING = "REPAIRING"
    REPORTING = "REPORTING"
    UPDATING_RUNTIME = "UPDATING_RUNTIME"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass(slots=True)
class ManufacturingContext:
    """
    Shared execution context for one manufacturing cycle.
    """

    runtime: Any | None = None

    blueprint: Any | None = None

    production_node: Any | None = None

    question_batch: Any | None = None

    validation_results: list[Any] = field(
        default_factory=list,
    )

    repair_results: list[Any] = field(
        default_factory=list,
    )

    report: Any | None = None

    started_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


class ManufacturingDirector:
    """
    Factory OS v2.1 Manufacturing Director.

    This class contains no business logic.

    It coordinates every subsystem required to
    manufacture one validated question batch.
    """

    def __init__(self) -> None:

        self._logger = logging.getLogger(
            self.__class__.__name__,
        )

        self._state = FactoryState.IDLE

        #
        # Core Services
        #

        self.runtime_controller = RuntimeController()

        self.blueprint_loader = BlueprintLoader()

        self.scheduler = ProductionScheduler()

        self.question_generator = QuestionGenerator()

        #
        # Validation
        #

        self.r01_validator = R01Validator()

        self.r02_validator = R02Validator()

        self.r03_validator = R03Validator()

        #
        # Repair
        #

        self.repair_engine = RepairEngine()

        #
        # Reporting
        #

        self.production_report = ProductionReport()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def run(self) -> ManufacturingContext:
        """
        Execute one complete manufacturing cycle.
        """

        context = ManufacturingContext()

        try:

            self.initialize()

            self._load_runtime(
                context,
            )

            self._load_blueprint(
                context,
            )

            self._schedule(
                context,
            )

            self._generate(
                context,
            )

            self._validate(
                context,
            )

            self._repair(
                context,
            )

            self._report(
                context,
            )

            self._update_runtime(
                context,
            )

            self._state = FactoryState.COMPLETED

            return context

        except Exception:

            self._state = FactoryState.FAILED

            self._logger.exception(
                "Manufacturing cycle failed."
            )

            raise

    def initialize(self) -> None:
        """
        Prepare the Manufacturing Director
        for execution.
        """

        self._state = FactoryState.INITIALIZING

        self._logger.info(
            "Manufacturing Director initialized."
        )
    # ---------------------------------------------------------
    # Runtime
    # ---------------------------------------------------------

    def _load_runtime(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Load the current manufacturing runtime.
        """

        self._state = FactoryState.LOADING_RUNTIME

        runtime = self.runtime_controller.load()

        context.runtime = runtime

        self._logger.info(
            "Runtime loaded successfully."
        )

    # ---------------------------------------------------------
    # Blueprint
    # ---------------------------------------------------------

    def _load_blueprint(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Load the frozen production blueprint.
        """

        self._state = FactoryState.LOADING_BLUEPRINT

        if context.runtime is None:

            raise RuntimeError(
                "Runtime must be loaded before loading the blueprint."
            )

        #
        # Verified API:
        # BlueprintLoader.load()
        #

        blueprint = self.blueprint_loader.load()

        context.blueprint = blueprint

        self._logger.info(
            "Blueprint loaded successfully."
        )

    # ---------------------------------------------------------
    # Scheduling
    # ---------------------------------------------------------

    def _schedule(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Ask the Production Scheduler for the
        next manufacturing node.
        """

        self._state = FactoryState.SCHEDULING

        if context.runtime is None:

            raise RuntimeError(
                "Runtime unavailable."
            )

        if context.blueprint is None:

            raise RuntimeError(
                "Blueprint unavailable."
            )

        #
        # Verified API:
        #
        # get_next_node(
        #     runtime,
        #     blueprint,
        # )
        #

        production_node = (
            self.scheduler.get_next_node(
                runtime=context.runtime,
                blueprint=context.blueprint,
            )
        )

        context.production_node = (
            production_node
        )

        self._logger.info(
            "Production node selected."
        )

        self._logger.debug(
            "Production node: %s",
            production_node,
        )
 
    # ---------------------------------------------------------
    # Generation
    # ---------------------------------------------------------

    def _generate(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Generate one manufacturing batch.
        """

        self._state = FactoryState.GENERATING

        if context.runtime is None:
            raise RuntimeError(
                "Runtime unavailable."
            )

        if context.blueprint is None:
            raise RuntimeError(
                "Blueprint unavailable."
            )

        if context.production_node is None:
            raise RuntimeError(
                "Production node unavailable."
            )

        #
        # Verified API:
        #
        # generate(
        #     node,
        #     blueprint,
        #     runtime,
        # )
        #

        generated = self.question_generator.generate(
            node=context.production_node,
            blueprint=context.blueprint,
            runtime=context.runtime,
        )

        batch = QuestionBatchModel()

        for item in generated:

            question = GeneratedQuestionModel.from_dict(
                item,
            )

            batch.add_question(
                question,
            )

        context.question_batch = batch

        self._logger.info(
            "Generated %d question(s).",
            batch.question_count,
        )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def _validate(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Execute the complete validation pipeline.
        """

        self._state = FactoryState.VALIDATING

        batch = context.question_batch

        if batch is None:

            raise RuntimeError(
                "Question batch unavailable."
            )

        if batch.is_empty():

            raise RuntimeError(
                "Generated batch is empty."
            )

        validators = (
            self.r01_validator,
            self.r02_validator,
            self.r03_validator,
        )

        results: list[Any] = []

        for validator in validators:

            result = validator.validate(
                batch,
            )

            results.append(
                result,
            )

            self._logger.info(
                "%s completed.",
                validator.rule_code,
            )

            if not result.is_successful():

                break

        context.validation_results = results
    # ---------------------------------------------------------
    # Repair
    # ---------------------------------------------------------

    def _repair(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Execute structural repair when validation
        identifies repairable issues.
        """

        self._state = FactoryState.REPAIRING

        batch = context.question_batch

        if batch is None:
            raise RuntimeError(
                "Question batch unavailable."
            )

        validation_results = context.validation_results

        #
        # If every validator passed,
        # repair is unnecessary.
        #

        if validation_results and all(
            result.is_successful()
            for result in validation_results
        ):

            self._logger.info(
                "Repair skipped. Batch passed validation."
            )

            context.repair_results = []

            return

        self._logger.info(
            "Repair pipeline started."
        )

        repair_results = self.repair_engine.execute(
            batch,
        )

        context.repair_results = repair_results

        self._logger.info(
            "Repair completed (%d repair result(s)).",
            len(repair_results),
        )

    # ---------------------------------------------------------
    # Reporting
    # ---------------------------------------------------------

    def _report(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Produce the manufacturing report.
        """

        self._state = FactoryState.REPORTING

        batch = context.question_batch

        if batch is None:
            raise RuntimeError(
                "Question batch unavailable."
            )

        validation_result = (
            context.validation_results[-1]
            if context.validation_results
            else None
        )

        #
        # Current ProductionReport API:
        #
        # print_report(
        #     request,
        #     batch_result,
        #     validation_result,
        #     csv_file,
        # )
        #

        self.production_report.print_report(
            request=context.production_node,
            batch_result=batch,
            validation_result=validation_result,
            csv_file=None,
        )

        context.report = {
            "generated": True,
        }

        self._logger.info(
            "Production report generated."
        )

    # ---------------------------------------------------------
    # Runtime Update
    # ---------------------------------------------------------

    def _update_runtime(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Persist runtime progression after a
        successful manufacturing cycle.
        """

        self._state = FactoryState.UPDATING_RUNTIME

        if context.runtime is None:
            raise RuntimeError(
                "Runtime unavailable."
            )

        if context.production_node is None:
            raise RuntimeError(
                "Production node unavailable."
            )

        next_runtime = (
            self.runtime_controller.build_next_runtime(
                current_runtime=context.runtime,
                production_node=context.production_node,
                package_result=context.question_batch,
            )
        )

        self.runtime_controller.save(
            next_runtime,
        )

        context.runtime = next_runtime

        self._logger.info(
            "Runtime updated successfully."
        )
    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def state(self) -> FactoryState:
        """
        Return the current manufacturing state.
        """

        return self._state

    @property
    def component_name(self) -> str:
        """
        Component name.
        """

        return "Manufacturing Director"

    @property
    def version(self) -> str:
        """
        Component version.
        """

        return "2.1.0"

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(self) -> dict[str, Any]:
        """
        Return runtime diagnostics.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "state": self._state.value,
            "services": {
                "runtime_controller": (
                    self.runtime_controller.__class__.__name__
                ),
                "blueprint_loader": (
                    self.blueprint_loader.__class__.__name__
                ),
                "scheduler": (
                    self.scheduler.__class__.__name__
                ),
                "question_generator": (
                    self.question_generator.__class__.__name__
                ),
                "r01_validator": (
                    self.r01_validator.__class__.__name__
                ),
                "r02_validator": (
                    self.r02_validator.__class__.__name__
                ),
                "r03_validator": (
                    self.r03_validator.__class__.__name__
                ),
                "repair_engine": (
                    self.repair_engine.__class__.__name__
                ),
                "production_report": (
                    self.production_report.__class__.__name__
                ),
            },
        }

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(self) -> dict[str, Any]:
        """
        Return component health.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "status": (
                "READY"
                if self._state != FactoryState.FAILED
                else "FAILED"
            ),
            "state": self._state.value,
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(self) -> dict[str, bool]:
        """
        Return supported capabilities.
        """

        return {
            "runtime_management": True,
            "blueprint_loading": True,
            "production_scheduling": True,
            "question_generation": True,
            "validation_pipeline": True,
            "automatic_repair": True,
            "production_reporting": True,
            "runtime_progression": True,
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "ManufacturingDirector("
            f"state='{self._state.value}')"
        )

    def __str__(self) -> str:

        return (
            f"{self.component_name} "
            f"v{self.version} "
            f"[{self._state.value}]"
        )


__all__ = [
    "FactoryState",
    "ManufacturingContext",
    "ManufacturingDirector",
]
