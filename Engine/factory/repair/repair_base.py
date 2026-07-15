"""
Question Factory OS v2.0

Repair Base

Provides the common implementation shared by
all repair modules.

Concrete repair modules should inherit from
this class and implement only repair logic.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from Engine.factory.repair.repair_result_model import (
    RepairResultModel,
)

from Engine.models.question_batch_model import (
    QuestionBatchModel,
)


class RepairBase(ABC):
    """
    Base class for all repair modules.
    """

    def __init__(self):

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Repair module name.
        """

    @property
    @abstractmethod
    def repair_code(self) -> str:
        """
        Repair module identifier.
        """

    # ---------------------------------------------------------
    # Repair
    # ---------------------------------------------------------

    @abstractmethod
    def repair(
        self,
        batch: QuestionBatchModel,
    ) -> RepairResultModel:
        """
        Execute repair.
        """
    # ---------------------------------------------------------
    # Lifecycle Hooks
    # ---------------------------------------------------------

    def before_repair(
        self,
        batch: QuestionBatchModel,
    ) -> None:
        """
        Executed immediately before repair.

        Override in derived repair modules when
        preprocessing is required.
        """

        return

    def after_repair(
        self,
        batch: QuestionBatchModel,
        result: RepairResultModel,
    ) -> None:
        """
        Executed immediately after repair.

        Override for reporting, telemetry or
        post-processing.
        """

        return

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(
        self,
        batch: QuestionBatchModel,
    ) -> RepairResultModel:
        """
        Execute the complete repair workflow.
        """

        self.logger.info(
            "Executing repair module: %s",
            self.name,
        )

        self.before_repair(
            batch
        )

        result = self.repair(
            batch
        )

        self.after_repair(
            batch,
            result,
        )

        self.logger.info(
            "Repair module '%s' completed.",
            self.name,
        )

        return result

    # ---------------------------------------------------------
    # Result Helpers
    # ---------------------------------------------------------

    def create_result(
        self,
    ) -> RepairResultModel:
        """
        Create an empty repair result.
        """

        return RepairResultModel(
            module_name=self.name,
        )

    def create_regeneration_result(
        self,
        reason: str,
    ) -> RepairResultModel:
        """
        Create a repair result that requires
        regeneration.
        """

        result = RepairResultModel(
            module_name=self.name,
        )

        result.mark_regeneration_required(
            reason
        )

        return result
    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(
        self,
        result: RepairResultModel,
    ) -> dict:
        """
        Return a concise repair summary.
        """

        return {
            "module": self.name,
            "repair_code": self.repair_code,
            "repaired": (
                result.repaired
            ),
            "repaired_items": (
                result.repaired_count
            ),
            "failed_repairs": (
                result.failed_count
            ),
            "warnings": (
                result.warning_count
            ),
            "regeneration_required": (
                result.regeneration_required
            ),
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
        result: RepairResultModel,
    ) -> dict:
        """
        Return repair diagnostics.
        """

        return {
            "component": (
                self.__class__.__name__
            ),
            "summary": (
                self.summary(
                    result
                )
            ),
            "statistics": (
                result.statistics()
            ),
            "metadata": (
                dict(
                    result.metadata
                )
            ),
        }

    # ---------------------------------------------------------
    # Component Information
    # ---------------------------------------------------------

    @property
    def version(
        self,
    ) -> str:
        """
        Repair framework version.
        """

        return "2.0.0"

    @property
    def component_name(
        self,
    ) -> str:
        """
        Component name.
        """

        return "Repair Base"

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> dict:
        """
        Return repair module health.
        """

        return {
            "component": (
                self.component_name
            ),
            "module": self.name,
            "repair_code": (
                self.repair_code
            ),
            "version": (
                self.version
            ),
            "status": "READY",
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(
        self,
    ) -> dict:
        """
        Describe repair capabilities.
        """

        return {
            "execution_pipeline": True,
            "lifecycle_hooks": True,
            "repair_tracking": True,
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
        Return repair execution information.
        """

        return {
            "module": self.name,
            "repair_code": self.repair_code,
            "execution_mode": "SEQUENTIAL",
            "framework_version": self.version,
        }

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def validate_configuration(
        self,
    ) -> None:
        """
        Validate repair module configuration.

        Raises
        ------
        ValueError
            If required properties are invalid.
        """

        if not self.name.strip():

            raise ValueError(
                "Repair module name cannot "
                "be empty."
            )

        if not self.repair_code.strip():

            raise ValueError(
                "Repair code cannot be empty."
            )

    # ---------------------------------------------------------
    # Metadata Helpers
    # ---------------------------------------------------------

    def create_metadata(
        self,
    ) -> dict:
        """
        Create default repair metadata.
        """

        return {
            "module": self.name,
            "repair_code": self.repair_code,
            "framework_version": self.version,
        }

    def reset_result(
        self,
        result: RepairResultModel,
    ) -> None:
        """
        Reset an existing repair result.
        """

        result.reset()

        result.module_name = self.name

    # ---------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------

    def supports_batch_repair(
        self,
    ) -> bool:
        """
        Indicates whether this repair module
        operates on an entire batch.

        Override in derived modules when the
        repair operates on individual questions.
        """

        return True

    def supports_auto_repair(
        self,
    ) -> bool:
        """
        Indicates whether this repair module
        can perform automatic repairs without
        regeneration.

        Override when AI-assisted or manual
        repair is required.
        """

        return True
    # ---------------------------------------------------------
    # Execution Information
    # ---------------------------------------------------------

    def execution_information(
        self,
    ) -> dict:
        """
        Return repair execution information.
        """

        return {
            "module": self.name,
            "repair_code": self.repair_code,
            "execution_mode": "SEQUENTIAL",
            "framework_version": self.version,
        }

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def validate_configuration(
        self,
    ) -> None:
        """
        Validate repair module configuration.

        Raises
        ------
        ValueError
            If required properties are invalid.
        """

        if not self.name.strip():

            raise ValueError(
                "Repair module name cannot "
                "be empty."
            )

        if not self.repair_code.strip():

            raise ValueError(
                "Repair code cannot be empty."
            )

    # ---------------------------------------------------------
    # Metadata Helpers
    # ---------------------------------------------------------

    def create_metadata(
        self,
    ) -> dict:
        """
        Create default repair metadata.
        """

        return {
            "module": self.name,
            "repair_code": self.repair_code,
            "framework_version": self.version,
        }

    def reset_result(
        self,
        result: RepairResultModel,
    ) -> None:
        """
        Reset an existing repair result.
        """

        result.reset()

        result.module_name = self.name

    # ---------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------

    def supports_batch_repair(
        self,
    ) -> bool:
        """
        Indicates whether this repair module
        operates on an entire batch.

        Override in derived modules when the
        repair operates on individual questions.
        """

        return True

    def supports_auto_repair(
        self,
    ) -> bool:
        """
        Indicates whether this repair module
        can perform automatic repairs without
        regeneration.

        Override when AI-assisted or manual
        repair is required.
        """

        return True
        
