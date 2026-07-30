"""
Question Factory OS v2.5

Manufacturing Work Item Executor
"""

from __future__ import annotations

import logging

from Engine.curriculum.manufacturing_work_item_model import (
    ManufacturingWorkItemModel,
)

from Engine.curriculum.orchestrator.production_orchestrator import (
    ProductionOrchestrator,
)


class ManufacturingWorkItemExecutor:
    """
    Executes a single ManufacturingWorkItemModel.

    Responsibilities
    ----------------
    1. Manage work item lifecycle.
    2. Delegate execution to the ProductionOrchestrator.
    3. Update work item status.
    """

    VERSION = "2.5.0"

    def __init__(
        self,
        orchestrator: ProductionOrchestrator,
    ) -> None:

        self._logger = logging.getLogger(
            self.__class__.__name__
        )

        self._orchestrator = orchestrator

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(
        self,
        work_item: ManufacturingWorkItemModel,
    ) -> int:
        """
        Execute one manufacturing work item.

        Returns
        -------
        int
            Number of questions generated.
        """

        self._logger.info(
            "Starting work item %s",
            work_item.work_item_id,
        )

        work_item.mark_running()

        try:

            generated = (
                self._orchestrator.execute(
                    work_item,
                )
            )

            work_item.mark_completed()

            self._logger.info(
                "Completed work item %s (%d questions)",
                work_item.work_item_id,
                generated,
            )

            return generated

        except Exception:

            work_item.mark_failed()

            self._logger.exception(
                "Work item %s failed.",
                work_item.work_item_id,
            )

            raise

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
            "orchestrator": (
                self._orchestrator.__class__.__name__
            ),
        }

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def reset(
        self,
    ) -> None:

        self._logger.info(
            "Executor reset requested."
        )

    def shutdown(
        self,
    ) -> None:

        self._logger.info(
            "Executor shutdown."
        )

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
    "ManufacturingWorkItemExecutor",
]