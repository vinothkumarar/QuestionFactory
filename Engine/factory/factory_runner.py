"""
Question Factory OS v2.5

Factory Runner

Unified production entry point for both:

1. Autonomous Manufacturing
2. Curriculum Manufacturing

Autonomous Flow
---------------
FactoryStateRepository
        ↓
ProductionPlanner
        ↓
ProductionOrderModel
        ↓
_execute_production_order()
        ↓
Advance Factory State

Curriculum Flow
---------------
ProductionOrderModel
        ↓
run_production_order()
        ↓
_execute_production_order()
"""

from __future__ import annotations

import logging

from Engine.bootstrap.service_container import (
    ServiceContainer,
)

from Engine.blueprint.blueprint_loader import (
    BlueprintLoader,
)

from Engine.exporters.question_csv_exporter import (
    QuestionCSVExporter,
)

from Engine.factory.orchestrator.orchestration_result import (
    OrchestrationResult,
)

from Engine.factory.generation.production_node_factory import (
    ProductionNodeFactory,
)

from Engine.models.production_order_model import (
    ProductionOrderModel,
)

from Engine.models.question_batch_model import (
    QuestionBatchModel,
)

from Engine.factory.planning.subtopic_analyzer import (
    SubtopicAnalyzer,
)

from Engine.planning.production_planner import (
    ProductionPlanner as AutonomousProductionPlanner,
)

from Engine.repositories.factory_state_repository import (
    FactoryStateRepository,
)

from Engine.repositories.runtime_repository import (
    RuntimeRepository,
)

from Engine.factory.planning.planning_director import (
    PlanningDirector,
)

from Engine.factory.planning.academic_analyzer import (
    AcademicAnalyzer,
)

from Engine.factory.planning.subtopic_analyzer import (
    SubtopicAnalyzer,
)

from Engine.factory.planning.batch_planner import (
    BatchPlanner,
)

from Engine.factory.planning.production_planner import (
    ProductionPlanner as ManufacturingProductionPlanner,
)

class FactoryRunner:
    """
    Executes Question Factory production.

    Supports both:

    • Autonomous production
    • Curriculum production

    All manufacturing logic is centralized in
    _execute_production_order().
    """

    VERSION = "2.5.0"

    def __init__(self) -> None:

        self._logger = logging.getLogger(
            self.__class__.__name__
        )

        

        #
        # Dependency Container
        #

        self.container = ServiceContainer()

        self.academic_analyzer = (
            AcademicAnalyzer(
                self.container.ai_engine,
            )
        )

        self.subtopic_analyzer = (
            SubtopicAnalyzer(
                self.academic_analyzer,
            )
        )

        #
        # Repositories
        #

        self.factory_state_repository = (
            FactoryStateRepository()
        )

        self.runtime_repository = (
            RuntimeRepository()
        )

        #
        # Core Services
        #

        self.blueprint_loader = (
            BlueprintLoader()
        )

        self.production_planner = (
            AutonomousProductionPlanner()
        )

        self.manufacturing_production_planner = (
            ManufacturingProductionPlanner()
        )
        self.batch_planner = (
            BatchPlanner()
        )

        self.planning_director = (
            PlanningDirector(
                academic_analyzer=self.academic_analyzer,
                production_planner=self.manufacturing_production_planner,
                batch_planner=self.batch_planner,
            )
        )

        

        self.factory_state_manager = (
            self.production_planner.state_manager
        )

        self.production_node_factory = (
            ProductionNodeFactory()
        )

        self.question_generator = (
            self.container.question_generator
        )

        self.question_csv_exporter = (
            QuestionCSVExporter()
        )

        self._logger.info(
            "FactoryRunner initialized."
        )
    # ---------------------------------------------------------
    # Autonomous Manufacturing
    # ---------------------------------------------------------

    def run(
        self,
    ) -> int:
        """
        Execute one complete autonomous
        manufacturing cycle.

        This entry point preserves the original
        FactoryRunner behaviour.

        Returns
        -------
        int
            Number of questions generated.
        """

        self._logger.info(
            "Starting autonomous manufacturing cycle."
        )

        print("=" * 60)
        print("QUESTION FACTORY OS v2.5")
        print("=" * 60)
        print()

        try:

            #
            # Load current factory state
            #

            factory_state = (
                self.factory_state_repository.load()
            )

            self._logger.info(
                "Factory state loaded."
            )

            #
            # Build next production order
            #

            production_order = (
                self.production_planner.plan(
                    factory_state,
                )
            )

            self._logger.info(
                "Production order created."
            )

            #
            # Execute the shared production pipeline
            #

            question_count = (
                self._execute_production_order(
                    production_order,
                )
            )

            #
            # Advance autonomous state
            #

            self.factory_state_manager.advance_batch(
                factory_state,
            )

            self.factory_state_repository.save(
                factory_state,
            )

            self._logger.info(
                "Factory state advanced."
            )

            return question_count

        except Exception:

            self._logger.exception(
                "Autonomous manufacturing failed."
            )

            raise

    # ---------------------------------------------------------
    # Curriculum Manufacturing
    # ---------------------------------------------------------

    def run_production_order(
        self,
        production_order: ProductionOrderModel,
    ) -> int:
        """
        Execute a supplied ProductionOrderModel.

        Unlike run(), this method does NOT:

        - Load FactoryState
        - Advance FactoryState
        - Persist FactoryState

        It simply executes the supplied
        production order.

        Returns
        -------
        int
            Number of questions generated.
        """

        self._logger.info(
            "Starting curriculum manufacturing."
        )

        return self._execute_production_order(
            production_order,
        )

    # ---------------------------------------------------------
    # Shared Production Engine
    # ---------------------------------------------------------

    def _execute_production_order(
        self,
        production_order: ProductionOrderModel,
    ) -> int:
        """
        Execute one production order.

        This method contains the common
        manufacturing pipeline shared by both

        • Autonomous Runner
        • Curriculum Runner
        """

        self._logger.info(
            "Executing production order %s",
            production_order.order_id,
        )

           #
        # Analyze production order
        #

        planning_result = (
            self.planning_director.plan(
                production_order,
            )
        )

        manufacturing_plan = (
            planning_result.manufacturing_plan
        )

        self._logger.info(
            "Manufacturing plan created."
        )
        #
        # Build production node
        #

        production_node = (
            self.production_node_factory.build(
                production_order,
            )
        )

        self._logger.info(
            "Production node created."
        )

        #
        # Load blueprint
        #

        blueprint = (
            self.blueprint_loader.load()
        )

        self._logger.info(
            "Blueprint loaded."
        )

        #
        # Load runtime
        #

        runtime = (
            self.runtime_repository.get_runtime()
        )

        self._logger.info(
            "Runtime loaded."
        )
        #
        # Generate questions
        #

        orchestration_result: OrchestrationResult = (
            self.question_generator.generate(
                node=production_node,
                blueprint=blueprint,
                runtime=runtime,
            )
        )

        self._logger.info(
            "Question generation completed."
        )

        #
        # Validate orchestration result
        #

        self._validate_orchestration_result(
            orchestration_result,
        )

        batch = orchestration_result.batch

        if batch is None:
            raise RuntimeError(
                "Question batch is None."
            )

        #
        # Export CSV
        #

        csv_path = (
            self._export_batch(
                batch=batch,
                production_order=production_order,
            )
        )

        #
        # Persist runtime
        #

        self.runtime_repository.save_runtime(
            runtime,
        )

        self._logger.info(
            "Runtime saved."
        )

        #
        # Success output
        #

        self._print_success(
            batch=batch,
            csv_path=csv_path,
        )

        return len(batch.questions)

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def _validate_orchestration_result(
        self,
        orchestration_result: OrchestrationResult,
    ) -> None:
        """
        Validate QuestionGenerator output.
        """

        if not orchestration_result.success:

            message = (
                orchestration_result.message
                or "Manufacturing failed."
            )

            self._logger.error(
                message,
            )

            if orchestration_result.errors:

                for error in orchestration_result.errors:

                    self._logger.error(
                        error,
                    )

            raise RuntimeError(
                message,
            )

        if not orchestration_result.has_batch:

            raise RuntimeError(
                "Question generator completed "
                "without returning a batch."
            )

    # ---------------------------------------------------------
    # CSV Export
    # ---------------------------------------------------------

    def _export_batch(
        self,
        *,
        batch: QuestionBatchModel,
        production_order: ProductionOrderModel,
    ) -> str:
        """
        Export a manufactured batch to CSV.
        """

        csv_path = (
            self.question_csv_exporter.export(
                batch=batch,
                production_order=production_order,
            )
        )

        self._logger.info(
            "CSV export completed."
        )

        return csv_path
    # ---------------------------------------------------------
    # Console Output
    # ---------------------------------------------------------

    def _print_success(
        self,
        *,
        batch: QuestionBatchModel,
        csv_path: str,
    ) -> None:
        """
        Print manufacturing success summary.
        """

        print("=" * 60)
        print("MANUFACTURING COMPLETED")
        print("=" * 60)
        print()

        print(
            "CSV Export : SUCCESS"
        )

        print(
            "Questions  :",
            len(batch.questions),
        )

        print(
            "Output File:",
            csv_path,
        )

        print()

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return FactoryRunner diagnostics.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "repositories": {
                "factory_state": (
                    self.factory_state_repository.__class__.__name__
                ),
                "runtime": (
                    self.runtime_repository.__class__.__name__
                ),
            },
            "services": {
                "planner": (
                    self.production_planner.__class__.__name__
                ),
                "node_factory": (
                    self.production_node_factory.__class__.__name__
                ),
                "blueprint_loader": (
                    self.blueprint_loader.__class__.__name__
                ),
                "question_generator": (
                    self.question_generator.configuration()
                ),
                "csv_exporter": (
                    self.question_csv_exporter.diagnostics()
                ),
            },
            "container": (
                self.container.diagnostics()
            ),
        }

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> dict[str, object]:
        """
        Return FactoryRunner health.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "status": "READY",
            "question_generator": (
                self.question_generator.health()
            ),
            "csv_exporter": (
                self.question_csv_exporter.health()
            ),
            "container": (
                self.container.health()
            ),
        }
    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset the FactoryRunner.
        """

        self._logger.info(
            "FactoryRunner reset requested."
        )

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown the FactoryRunner.
        """

        self._logger.info(
            "FactoryRunner shutdown."
        )

    # ---------------------------------------------------------
    # Component Information
    # ---------------------------------------------------------

    @property
    def component_name(
        self,
    ) -> str:
        """
        Component name.
        """

        return self.__class__.__name__

    @property
    def version(
        self,
    ) -> str:
        """
        FactoryRunner version.
        """

        return self.VERSION

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        """
        Debug representation.
        """

        return (
            f"{self.component_name}"
            f"(version='{self.version}')"
        )

    def __str__(
        self,
    ) -> str:
        """
        Human readable representation.
        """

        return (
            f"{self.component_name} "
            f"[v{self.version}]"
        )


__all__ = [
    "FactoryRunner",
]