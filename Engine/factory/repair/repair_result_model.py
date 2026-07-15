"""
Question Factory OS v2.0

Repair Result Model

Represents the outcome of one repair module.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class RepairResultModel:
    """
    Result produced by a repair module.
    """

    module_name: str

    repaired: bool = False

    regeneration_required: bool = False

    repaired_items: List[str] = field(
        default_factory=list
    )

    failed_repairs: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    metadata: Dict = field(
        default_factory=dict
    )
    # ---------------------------------------------------------
    # Repair Status
    # ---------------------------------------------------------

    def mark_repaired(
        self,
        item: str,
    ) -> None:
        """
        Record a successful repair.
        """

        self.repaired = True

        self.repaired_items.append(
            item
        )

    def mark_failed(
        self,
        item: str,
    ) -> None:
        """
        Record a repair that could not be
        completed.
        """

        self.failed_repairs.append(
            item
        )

    def mark_regeneration_required(
        self,
        reason: str,
    ) -> None:
        """
        Mark this repair result as requiring
        question regeneration.
        """

        self.regeneration_required = True

        self.failed_repairs.append(
            reason
        )

    # ---------------------------------------------------------
    # Warnings
    # ---------------------------------------------------------

    def add_warning(
        self,
        warning: str,
    ) -> None:
        """
        Add a repair warning.
        """

        self.warnings.append(
            warning
        )

    @property
    def warning_count(
        self,
    ) -> int:
        """
        Number of repair warnings.
        """

        return len(
            self.warnings
        )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def set_metadata(
        self,
        key: str,
        value,
    ) -> None:
        """
        Store metadata.
        """

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default=None,
    ):
        """
        Retrieve metadata.
        """

        return self.metadata.get(
            key,
            default,
        )
    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    @property
    def repaired_count(
        self,
    ) -> int:
        """
        Number of successfully repaired items.
        """

        return len(
            self.repaired_items
        )

    @property
    def failed_count(
        self,
    ) -> int:
        """
        Number of failed repair attempts.
        """

        return len(
            self.failed_repairs
        )

    def statistics(
        self,
    ) -> Dict:
        """
        Return repair statistics.
        """

        return {
            "module": self.module_name,
            "repaired": self.repaired_count,
            "failed": self.failed_count,
            "warnings": self.warning_count,
            "regeneration_required": (
                self.regeneration_required
            ),
        }

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> Dict:
        """
        Return a concise repair summary.
        """

        return {
            "module": self.module_name,
            "success": self.repaired,
            "repaired_items": (
                self.repaired_count
            ),
            "failed_items": (
                self.failed_count
            ),
            "warnings": (
                self.warning_count
            ),
            "regeneration_required": (
                self.regeneration_required
            ),
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
    ) -> Dict:
        """
        Return complete repair diagnostics.
        """

        return {
            "summary": self.summary(),
            "statistics": self.statistics(),
            "repaired_items": (
                list(self.repaired_items)
            ),
            "failed_repairs": (
                list(self.failed_repairs)
            ),
            "warnings": (
                list(self.warnings)
            ),
            "metadata": (
                dict(self.metadata)
            ),
        }
    # ---------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset the repair result.
        """

        self.repaired = False

        self.regeneration_required = False

        self.repaired_items.clear()

        self.failed_repairs.clear()

        self.warnings.clear()

        self.metadata.clear()

    def has_repairs(
        self,
    ) -> bool:
        """
        Return True if any repair
        was successfully completed.
        """

        return self.repaired_count > 0

    def has_failures(
        self,
    ) -> bool:
        """
        Return True if any repair
        operation failed.
        """

        return self.failed_count > 0

    def has_warnings(
        self,
    ) -> bool:
        """
        Return True if warnings exist.
        """

        return self.warning_count > 0

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> Dict:
        """
        Return repair result health.
        """

        return {
            "module": self.module_name,
            "status": (
                "REGENERATION_REQUIRED"
                if self.regeneration_required
                else "READY"
            ),
            "repaired_items": (
                self.repaired_count
            ),
            "failed_repairs": (
                self.failed_count
            ),
            "warnings": (
                self.warning_count
            ),
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(
        self,
    ) -> Dict:
        """
        Describe supported features.
        """

        return {
            "repair_tracking": True,
            "failure_tracking": True,
            "warning_tracking": True,
            "metadata": True,
            "statistics": True,
            "diagnostics": True,
            "health_reporting": True,
        }

    # ---------------------------------------------------------
    # Execution Information
    # ---------------------------------------------------------

    def execution_information(
        self,
    ) -> Dict:
        """
        Return execution metadata.
        """

        return {
            "module": self.module_name,
            "repair_status": (
                "REGENERATION_REQUIRED"
                if self.regeneration_required
                else "COMPLETED"
            ),
            "successful_repairs": (
                self.repaired_count
            ),
            "failed_repairs": (
                self.failed_count
            ),
        }
    # ---------------------------------------------------------
    # Repair Information
    # ---------------------------------------------------------

    def repair_information(
        self,
    ) -> Dict:
        """
        Return repair information.
        """

        return {
            "module": self.module_name,
            "repaired": self.repaired,
            "regeneration_required": (
                self.regeneration_required
            ),
            "statistics": (
                self.statistics()
            ),
            "execution": (
                self.execution_information()
            ),
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            "RepairResultModel("
            f"module='{self.module_name}', "
            f"repaired={self.repaired}, "
            "regeneration_required="
            f"{self.regeneration_required})"
        )

    def __str__(
        self,
    ) -> str:

        if self.regeneration_required:

            status = "REGENERATION_REQUIRED"

        elif self.repaired:

            status = "REPAIRED"

        else:

            status = "NO_CHANGES"

        return (
            f"{self.module_name} - "
            f"{status}"
        )
        