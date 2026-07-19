"""
Question Factory OS v2.1

Repair Engine

Coordinates execution of all registered
repair modules.

The Repair Engine is responsible for
executing every repair stage after
validation has completed.

This implementation is intentionally
stateless except for the registered
repair modules.
"""

from __future__ import annotations

import logging
from abc import ABC
from abc import abstractmethod

from Engine.factory.repair.models.batch_repair_result import (
    BatchRepairResult,
)
from Engine.factory.repair.repair_result_model import (
    RepairResultModel,
)
from Engine.models.question_batch_model import (
    QuestionBatchModel,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Repair Module Interface
# ---------------------------------------------------------


class RepairModule(ABC):
    """
    Interface implemented by every repair
    module.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human readable module name.
        """

    @property
    @abstractmethod
    def repair_code(self) -> str:
        """
        Unique repair identifier.
        """

    @abstractmethod
    def repair(
        self,
        batch: QuestionBatchModel,
    ) -> RepairResultModel:
        """
        Execute repair.
        """


# ---------------------------------------------------------
# Repair Engine
# ---------------------------------------------------------


class RepairEngine:
    """
    Coordinates execution of all repair
    modules.

    The engine itself contains no repair
    logic. Each registered RepairModule
    performs its own specialised repair.
    """

    def __init__(
        self,
    ) -> None:

        self._logger = logger

        self._modules: list[
            RepairModule
        ] = []

        self._logger.info(
            "RepairEngine initialized."
        )

    # -----------------------------------------------------
    # Module Registration
    # -----------------------------------------------------

    def register(
        self,
        module: RepairModule,
    ) -> None:
        """
        Register a repair module.
        """

        if self.contains(
            module.name,
        ):

            raise ValueError(
                f"Repair module "
                f"'{module.name}' "
                f"is already registered."
            )

        self._modules.append(
            module,
        )

        self._logger.info(
            "Registered repair module: %s",
            module.name,
        )

    def unregister(
        self,
        module_name: str,
    ) -> bool:
        """
        Remove a repair module.

        Returns
        -------
        bool
            True if removed.
        """

        for module in self._modules:

            if module.name != module_name:
                continue

            self._modules.remove(
                module,
            )

            self._logger.info(
                "Removed repair module: %s",
                module_name,
            )

            return True

        return False

    def clear(
        self,
    ) -> None:
        """
        Remove every registered module.
        """

        self._modules.clear()

        self._logger.info(
            "Repair module registry cleared."
        )

    # -----------------------------------------------------
    # Queries
    # -----------------------------------------------------

    @property
    def module_count(
        self,
    ) -> int:
        """
        Number of registered modules.
        """

        return len(
            self._modules,
        )

    @property
    def modules(
        self,
    ) -> list[RepairModule]:
        """
        Return registered modules.
        """

        return list(
            self._modules,
        )

    def module_names(
        self,
    ) -> list[str]:
        """
        Return module names.
        """

        return [
            module.name
            for module in self._modules
        ]
    # -----------------------------------------------------
    # Lookup
    # -----------------------------------------------------

    def contains(
        self,
        module_name: str,
    ) -> bool:
        """
        Return True if the specified repair
        module is registered.
        """

        return any(
            module.name == module_name
            for module in self._modules
        )

    def get(
        self,
        module_name: str,
    ) -> RepairModule | None:
        """
        Return a registered repair module.

        Parameters
        ----------
        module_name:
            Name of the repair module.

        Returns
        -------
        RepairModule | None
        """

        for module in self._modules:

            if module.name == module_name:
                return module

        return None

    # -----------------------------------------------------
    # Lifecycle Hooks
    # -----------------------------------------------------

    def before_repair(
        self,
        batch: QuestionBatchModel,
    ) -> None:
        """
        Executed immediately before the
        repair pipeline begins.

        Derived classes may override.
        """

        return

    def after_repair(
        self,
        result: BatchRepairResult,
    ) -> None:
        """
        Executed after every repair module
        has completed.

        Derived classes may override.
        """

        return

    # -----------------------------------------------------
    # Execution
    # -----------------------------------------------------

    def repair(
        self,
        batch: QuestionBatchModel,
    ) -> BatchRepairResult:
        """
        Execute every registered repair
        module sequentially.
        """

        self._logger.info(
            "Starting repair cycle."
        )

        batch_result = BatchRepairResult(
            batch=batch,
        )

        for module in self._modules:

            self._logger.info(
                "Executing repair module: %s",
                module.name,
            )

            result = module.repair(
                batch,
            )

            batch_result.add_result(
                result,
            )

        batch_result.update_statistics()

        self._logger.info(
            "Repair cycle completed."
        )

        return batch_result

    def execute(
        self,
        batch: QuestionBatchModel,
    ) -> BatchRepairResult:
        """
        Execute the complete repair
        workflow.
        """

        self.before_repair(
            batch,
        )

        result = self.repair(
            batch,
        )

        self.after_repair(
            result,
        )

        return result
    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    def summary(
        self,
        result: BatchRepairResult,
    ) -> dict[str, int | bool]:
        """
        Return a concise repair summary.
        """

        return result.summary()

    # -----------------------------------------------------
    # Diagnostics
    # -----------------------------------------------------

    def diagnostics(
        self,
        result: BatchRepairResult,
    ) -> dict[str, object]:
        """
        Return repair diagnostics.
        """

        return {
            "component": self.__class__.__name__,
            "registered_modules": self.module_names(),
            "summary": result.summary(),
            "metadata": dict(
                result.metadata,
            ),
        }

    # -----------------------------------------------------
    # Health
    # -----------------------------------------------------

    def health(
        self,
    ) -> dict[str, object]:
        """
        Return Repair Engine health.
        """

        return {
            "component": "Repair Engine",
            "version": "2.1.0",
            "status": "READY",
            "registered_modules": self.module_count,
        }

    # -----------------------------------------------------
    # Capabilities
    # -----------------------------------------------------

    def capabilities(
        self,
    ) -> dict[str, bool]:
        """
        Return supported engine capabilities.
        """

        return {
            "module_registration": True,
            "module_lookup": True,
            "repair_execution": True,
            "lifecycle_hooks": True,
            "diagnostics": True,
            "health_reporting": True,
            "summary": True,
        }

    # -----------------------------------------------------
    # Execution Information
    # -----------------------------------------------------

    def execution_information(
        self,
    ) -> dict[str, object]:
        """
        Return execution information.
        """

        return {
            "component": "Repair Engine",
            "execution_mode": "SEQUENTIAL",
            "framework_version": "2.1.0",
            "registered_modules": self.module_count,
        }
    # -----------------------------------------------------
    # Configuration
    # -----------------------------------------------------

    def validate_configuration(
        self,
    ) -> None:
        """
        Validate Repair Engine configuration.
        """

        for module in self._modules:

            if not module.name.strip():

                raise ValueError(
                    "Repair module name "
                    "cannot be empty."
                )

            if not module.repair_code.strip():

                raise ValueError(
                    "Repair module repair_code "
                    "cannot be empty."
                )

    # -----------------------------------------------------
    # Utilities
    # -----------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset the Repair Engine.
        """

        self.clear()

    @property
    def is_empty(
        self,
    ) -> bool:
        """
        Return True when no repair modules
        are registered.
        """

        return self.module_count == 0

    @property
    def has_modules(
        self,
    ) -> bool:
        """
        Return True when at least one repair
        module is registered.
        """

        return not self.is_empty

    @property
    def is_ready(
        self,
    ) -> bool:
        """
        Return True when the Repair Engine
        is ready for execution.
        """

        return self.has_modules

    # -----------------------------------------------------
    # Representation
    # -----------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return self.module_count

    def __contains__(
        self,
        module_name: str,
    ) -> bool:

        return self.contains(
            module_name,
        )

    def __iter__(
        self,
    ):

        return iter(
            self._modules,
        )

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            "("
            f"modules={self.module_count}"
            ", "
            f"ready={self.is_ready}"
            ")"
        )

    __str__ = __repr__
# ---------------------------------------------------------
# Factory Helper
# ---------------------------------------------------------


def create_repair_engine() -> RepairEngine:
    """
    Create a production-ready RepairEngine.
    """

    engine = RepairEngine()

    logger.info(
        "Production RepairEngine created."
    )

    return engine


# ---------------------------------------------------------
# Module Exports
# ---------------------------------------------------------

__all__ = [
    "RepairModule",
    "RepairEngine",
    "create_repair_engine",
]
