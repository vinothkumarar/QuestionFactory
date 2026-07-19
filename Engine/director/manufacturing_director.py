"""
Question Factory OS v2.1

Manufacturing Director

The Manufacturing Director is the primary entry point for the
Question Factory manufacturing system. It coordinates the complete
manufacturing workflow by initializing all required factory
components and delegating execution to the Factory Orchestrator.

Workflow
--------
Manufacturing Request
        │
        ▼
Manufacturing Director
        │
        ▼
Factory Orchestrator
        │
        ├── AI Engine
        ├── Batch Adapter
        ├── Validation Engine
        ├── Repair Engine
        └── Generation Statistics
        │
        ▼
Orchestration Result
"""

from __future__ import annotations

import logging

from Engine.factory.ai.ai_engine import AIEngine
from Engine.factory.ai.models.ai_job import AIJob
from Engine.factory.orchestrator.batch_adapter import BatchAdapter
from Engine.factory.orchestrator.factory_orchestrator import (
    FactoryOrchestrator,
)
from Engine.factory.orchestrator.orchestration_result import (
    OrchestrationResult,
)
from Engine.factory.repair.repair_engine import RepairEngine
from Engine.factory.validation.validation_engine import (
    ValidationEngine,
)


class ManufacturingDirector:
    """
    Top-level coordinator for the Question Factory.

    This class owns the lifecycle of the major factory components
    and exposes a simplified interface for executing a complete
    manufacturing cycle.
    """

    VERSION = "2.1.0"

    COMPONENT_NAME = "Manufacturing Director"

    def __init__(
        self,
        ai_engine: AIEngine,
        validation_engine: ValidationEngine,
        repair_engine: RepairEngine,
    ) -> None:
        """
        Initialize the Manufacturing Director.
        """

        self._logger = logging.getLogger(
            self.__class__.__name__,
        )

        self._ai_engine = ai_engine
        self._validation_engine = validation_engine
        self._repair_engine = repair_engine

        self._batch_adapter = BatchAdapter()

        self._factory_orchestrator = (
            FactoryOrchestrator(
                ai_engine=self._ai_engine,
                validation_engine=self._validation_engine,
                repair_engine=self._repair_engine,
                batch_adapter=self._batch_adapter,
            )
        )

        self._logger.info(
            "%s initialized.",
            self.COMPONENT_NAME,
        )
    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def manufacture(
        self,
        job: AIJob,
    ) -> OrchestrationResult:
        """
        Execute a complete manufacturing cycle.

        Parameters
        ----------
        job:
            AI generation job.

        Returns
        -------
        OrchestrationResult
            Final manufacturing result.
        """

        self._logger.info(
            "Starting manufacturing job."
        )

        try:

            result = (
                self._factory_orchestrator.orchestrate(
                    job,
                )
            )

            if result.success:

                self._logger.info(
                    "Manufacturing completed successfully."
                )

            else:

                self._logger.warning(
                    "Manufacturing completed with failures."
                )

            return result

        except Exception:

            self._logger.exception(
                "Unexpected manufacturing failure."
            )

            raise

    # ---------------------------------------------------------
    # Convenience Methods
    # ---------------------------------------------------------

    def generate(
        self,
        job: AIJob,
    ) -> OrchestrationResult:
        """
        Alias for manufacture().

        This provides a concise API while keeping
        manufacture() as the primary entry point.
        """

        return self.manufacture(
            job,
        )

    # ---------------------------------------------------------
    # Component Accessors
    # ---------------------------------------------------------

    @property
    def orchestrator(
        self,
    ) -> FactoryOrchestrator:
        """
        Return the Factory Orchestrator.
        """

        return self._factory_orchestrator

    @property
    def statistics(
        self,
    ):
        """
        Return runtime statistics.
        """

        return (
            self._factory_orchestrator.statistics
        )
    # ---------------------------------------------------------
    # Runtime Information
    # ---------------------------------------------------------

    @property
    def component_name(
        self,
    ) -> str:
        """
        Return the component name.
        """

        return self.COMPONENT_NAME

    @property
    def version(
        self,
    ) -> str:
        """
        Return the component version.
        """

        return self.VERSION

    @property
    def ai_engine(
        self,
    ) -> AIEngine:
        """
        Return the configured AI Engine.
        """

        return self._ai_engine

    @property
    def validation_engine(
        self,
    ) -> ValidationEngine:
        """
        Return the Validation Engine.
        """

        return self._validation_engine

    @property
    def repair_engine(
        self,
    ) -> RepairEngine:
        """
        Return the Repair Engine.
        """

        return self._repair_engine

    @property
    def batch_adapter(
        self,
    ) -> BatchAdapter:
        """
        Return the Batch Adapter.
        """

        return self._batch_adapter

    # ---------------------------------------------------------
    # Runtime Summary
    # ---------------------------------------------------------

    def runtime_summary(
        self,
    ) -> dict[str, object]:
        """
        Return a runtime summary of the Manufacturing Director.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "status": "READY",
            "ai_engine": (
                self._ai_engine.__class__.__name__
            ),
            "validation_engine": (
                self._validation_engine.__class__.__name__
            ),
            "repair_engine": (
                self._repair_engine.__class__.__name__
            ),
            "batch_adapter": (
                self._batch_adapter.__class__.__name__
            ),
            "orchestrator": (
                self._factory_orchestrator.__class__.__name__
            ),
        }
    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return detailed diagnostic information.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "healthy": True,
            "orchestrator": (
                self._factory_orchestrator.diagnostics()
            ),
            "statistics": (
                self.statistics.to_dict()
            ),
        }

    def health(
        self,
    ) -> dict[str, object]:
        """
        Return the health status of the Manufacturing Director.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "status": "READY",
            "ai_engine": True,
            "validation_engine": True,
            "repair_engine": True,
            "batch_adapter": True,
            "factory_orchestrator": True,
        }

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset the runtime state.
        """

        self._factory_orchestrator.reset()

        self._logger.debug(
            "%s reset completed.",
            self.COMPONENT_NAME,
        )

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown the Manufacturing Director.

        Reserved for future resource cleanup.
        """

        self._logger.info(
            "%s shutdown completed.",
            self.COMPONENT_NAME,
        )
    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.COMPONENT_NAME}"
            f"(version='{self.VERSION}')"
        )

    def __str__(
        self,
    ) -> str:
        """
        Human-readable representation.
        """

        return (
            f"{self.COMPONENT_NAME} "
            f"v{self.VERSION}"
        )

    # ---------------------------------------------------------
    # Convenience Helpers
    # ---------------------------------------------------------

    @property
    def is_ready(
        self,
    ) -> bool:
        """
        Return whether the Manufacturing Director
        is ready to accept manufacturing jobs.
        """

        return True

    def component_versions(
        self,
    ) -> dict[str, str]:
        """
        Return the versions of all managed components.
        """

        return {
            "manufacturing_director": self.VERSION,
            "factory_orchestrator": (
                self._factory_orchestrator.version
            ),
            "ai_engine": (
                self._ai_engine.execution_information()[
                    "framework_version"
                ]
            ),
            "validation_engine": (
                self._validation_engine.VERSION
            ),
            "repair_engine": (
                "2.1.0"
            ),
            "batch_adapter": (
                self._batch_adapter.version
            ),
        }