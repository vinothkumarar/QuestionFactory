"""
Question Factory OS v2.0

Repair Engine

Coordinates execution of all registered
repair modules.

The Repair Engine is responsible for
repairing manufacturing defects identified
during validation.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import List

from Engine.models.question_batch_model import (
    QuestionBatchModel,
)


# ---------------------------------------------------------
# Repair Interface
# ---------------------------------------------------------

class RepairModule(ABC):
    """
    Base interface for repair modules.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Module name.
        """

    @abstractmethod
    def repair(
        self,
        batch: QuestionBatchModel,
    ):
        """
        Execute repair.
        """


# ---------------------------------------------------------
# Repair Engine
# ---------------------------------------------------------

class RepairEngine:
    """
    Coordinates execution of all
    registered repair modules.
    """

    def __init__(self):

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

        self._modules: List[
            RepairModule
        ] = []

    # ---------------------------------------------------------
    # Repair
    # ---------------------------------------------------------

    def repair(
        self,
        batch: QuestionBatchModel,
    ):
        """
        Execute every registered repair module.
        """

        self.logger.info(
            "Starting repair cycle."
        )

        results = []

        for module in self._modules:

            self.logger.info(
                "Executing repair module: %s",
                module.name,
            )

            result = module.repair(
                batch
            )

            results.append(
                result
            )

        self.logger.info(
            "Repair cycle completed."
        )

        return results
    # ---------------------------------------------------------
    # Module Management
    # ---------------------------------------------------------

    def add_module(
        self,
        module: RepairModule,
    ) -> None:
        """
        Register a repair module.
        """

        self._modules.append(
            module
        )

        self.logger.info(
            "Registered repair module: %s",
            module.name,
        )

    def remove_module(
        self,
        module_name: str,
    ) -> bool:
        """
        Remove a repair module by name.

        Returns
        -------
        bool
            True if the module was removed.
        """

        for module in self._modules:

            if module.name == module_name:

                self._modules.remove(
                    module
                )

                self.logger.info(
                    "Removed repair module: %s",
                    module_name,
                )

                return True

        return False

    def get_module(
        self,
        module_name: str,
    ) -> RepairModule | None:
        """
        Return a repair module by name.
        """

        for module in self._modules:

            if module.name == module_name:

                return module

        return None

    def modules(
        self,
    ) -> List[RepairModule]:
        """
        Return a copy of all registered modules.
        """

        return list(
            self._modules
        )

    def clear(
        self,
    ) -> None:
        """
        Remove all registered repair modules.
        """

        self._modules.clear()

        self.logger.info(
            "Repair module registry cleared."
        )

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    @property
    def module_count(
        self,
    ) -> int:
        """
        Return the number of registered
        repair modules.
        """

        return len(
            self._modules
        )

    def module_names(
        self,
    ) -> List[str]:
        """
        Return the names of all registered
        repair modules.
        """

        return [
            module.name
            for module
            in self._modules
        ]

    def has_module(
        self,
        module_name: str,
    ) -> bool:
        """
        Determine whether a repair module
        is registered.
        """

        return (
            module_name
            in self.module_names()
        )
    # ---------------------------------------------------------
    # Lifecycle Hooks
    # ---------------------------------------------------------

    def before_repair(
        self,
        batch: QuestionBatchModel,
    ) -> None:
        """
        Executed immediately before the repair
        cycle begins.

        Override for telemetry, auditing or
        preprocessing.
        """

        return

    def after_repair(
        self,
        batch: QuestionBatchModel,
        results: List,
    ) -> None:
        """
        Executed immediately after the repair
        cycle completes.

        Override for reporting or metrics.
        """

        return

    # ---------------------------------------------------------
    # Convenience API
    # ---------------------------------------------------------

    def execute(
        self,
        batch: QuestionBatchModel,
    ) -> List:
        """
        Execute the complete repair workflow.
        """

        self.before_repair(
            batch
        )

        results = self.repair(
            batch
        )

        self.after_repair(
            batch,
            results,
        )

        return results

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(
        self,
        results: List,
    ) -> dict:
        """
        Return a concise repair summary.
        """

        return {
            "module_count": (
                self.module_count
            ),
            "result_count": len(
                results
            ),
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
        results: List,
    ) -> dict:
        """
        Return repair diagnostics.
        """

        return {
            "component": (
                self.__class__.__name__
            ),
            "modules": (
                self.module_names()
            ),
            "summary": self.summary(
                results
            ),
        }
    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> dict:
        """
        Return Repair Engine health information.
        """

        return {
            "component": "Repair Engine",
            "version": "2.0.0",
            "status": "READY",
            "registered_modules": (
                self.module_count
            ),
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(
        self,
    ) -> dict:
        """
        Return Repair Engine capabilities.
        """

        return {
            "module_registration": True,
            "lifecycle_hooks": True,
            "repair_execution": True,
            "diagnostics": True,
            "health_reporting": True,
            "summary": True,
        }

    # ---------------------------------------------------------
    # Execution Information
    # ---------------------------------------------------------

    def execution_information(
        self,
    ) -> dict:
        """
        Return execution information.
        """

        return {
            "component": "Repair Engine",
            "execution_mode": "SEQUENTIAL",
            "registered_modules": (
                self.module_count
            ),
        }

    # ---------------------------------------------------------
    # Configuration Validation
    # ---------------------------------------------------------

    def validate_configuration(
        self,
    ) -> None:
        """
        Validate Repair Engine configuration.
        """

        if self.module_count == 0:

            self.logger.warning(
                "No repair modules have been "
                "registered."
            )

    # ---------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset the Repair Engine.
        """

        self.clear()

    def is_empty(
        self,
    ) -> bool:
        """
        Return True if no repair modules
        are registered.
        """

        return self.module_count == 0
    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> dict:
        """
        Return Repair Engine health information.
        """

        return {
            "component": "Repair Engine",
            "version": "2.0.0",
            "status": "READY",
            "registered_modules": (
                self.module_count
            ),
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(
        self,
    ) -> dict:
        """
        Return Repair Engine capabilities.
        """

        return {
            "module_registration": True,
            "lifecycle_hooks": True,
            "repair_execution": True,
            "diagnostics": True,
            "health_reporting": True,
            "summary": True,
        }

    # ---------------------------------------------------------
    # Execution Information
    # ---------------------------------------------------------

    def execution_information(
        self,
    ) -> dict:
        """
        Return execution information.
        """

        return {
            "component": "Repair Engine",
            "execution_mode": "SEQUENTIAL",
            "registered_modules": (
                self.module_count
            ),
        }

    # ---------------------------------------------------------
    # Configuration Validation
    # ---------------------------------------------------------

    def validate_configuration(
        self,
    ) -> None:
        """
        Validate Repair Engine configuration.
        """

        if self.module_count == 0:

            self.logger.warning(
                "No repair modules have been "
                "registered."
            )

    # ---------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset the Repair Engine.
        """

        self.clear()

    def is_empty(
        self,
    ) -> bool:
        """
        Return True if no repair modules
        are registered.
        """

        return self.module_count == 0
        