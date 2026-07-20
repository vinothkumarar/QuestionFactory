"""
Question Factory OS v2.2

Factory Runner

Production entry point for the autonomous
manufacturing pipeline.

Pipeline
--------
ServiceContainer
        ↓
Production Planner
        ↓
Question Generator
        ↓
Factory Orchestrator
        ↓
Question CSV Exporter
        ↓
Runtime Persistence
        ↓
Factory State Advancement
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

from Engine.planning.production_planner import (
    ProductionPlanner,
)

from Engine.repositories.factory_state_repository import (
    FactoryStateRepository,
)

from Engine.repositories.runtime_repository import (
    RuntimeRepository,
)


class FactoryRunner:
    """
    Executes one complete autonomous
    manufacturing cycle.
    """

    VERSION = "2.2.0"

    def __init__(
        self,
    ) -> None:

        self._logger = logging.getLogger(
            self.__class__.__name__
        )

        #
        # Dependency Container
        #

        self.container = ServiceContainer()

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
            ProductionPlanner()
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
    # Manufacturing
    # ---------------------------------------------------------

    def run(
        self,
    ) -> int:
        """
        Execute one complete manufacturing cycle.
        """

        self._logger.info(
            "Starting manufacturing cycle."
        )

        print("=" * 60)
        print("QUESTION FACTORY OS v2.2")
        print("=" * 60)
        print()

        try:

            #
            # Load factory state
            #

            factory_state = (
                self.factory_state_repository.load()
            )

            self._logger.info(
                "Factory state loaded."
            )

            #
            # Plan next production order
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

            if not orchestration_result.success:

                message = (
                    orchestration_result.message
                    or "Manufacturing failed."
                )

                self._logger.error(
                    message,
                )

                if orchestration_result.errors:

                    for error in (
                        orchestration_result.errors
                    ):

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

            batch = orchestration_result.batch

            if batch is None:
                raise RuntimeError(
                    "Question batch is None."
                )

            #
            # Export CSV
            #

            csv_path = (
                self.question_csv_exporter.export(
                    batch=batch,
                    production_order=production_order,
                )
            )

            self._logger.info(
                "CSV export completed."
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
            # Advance factory state
            #

            self.factory_state_manager.advance_batch(
                factory_state,
            )

            #
            # Persist updated factory state
            #

            self.factory_state_repository.save(
                factory_state,
            )

            self._logger.info(
                "Factory state advanced."
            )

            #
            # Success output
            #

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

            return 0

        except Exception:

            self._logger.exception(
                "Manufacturing failed."
            )

            raise

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
        Factory OS version.
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
