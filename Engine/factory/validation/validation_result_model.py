"""
Question Factory OS v2.0

Validation Result Model

Represents the outcome of a validator execution.

Returned by every validation rule (R01, R02, R03, ...).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(slots=True)
class ValidationResultModel:
    """
    Represents one validator execution result.
    """

    # ---------------------------------------------------------
    # Validator Information
    # ---------------------------------------------------------

    validator_name: str = ""

    rule_code: str = ""

    # ---------------------------------------------------------
    # Result
    # ---------------------------------------------------------

    success: bool = False

    # ---------------------------------------------------------
    # Findings
    # ---------------------------------------------------------

    errors: List[str] = field(default_factory=list)

    warnings: List[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    metadata: Dict = field(default_factory=dict)
    # ---------------------------------------------------------
    # Result Management
    # ---------------------------------------------------------

    def add_error(
        self,
        message: str,
    ) -> None:
        """
        Add a validation error.
        """

        self.errors.append(message)

        self.success = False

    def add_warning(
        self,
        message: str,
    ) -> None:
        """
        Add a validation warning.
        """

        self.warnings.append(message)

    def clear_errors(
        self,
    ) -> None:
        """
        Remove all validation errors.
        """

        self.errors.clear()

    def clear_warnings(
        self,
    ) -> None:
        """
        Remove all validation warnings.
        """

        self.warnings.clear()

    def mark_success(
        self,
    ) -> None:
        """
        Mark validation as successful.
        """

        self.success = True

    def mark_failure(
        self,
    ) -> None:
        """
        Mark validation as failed.
        """

        self.success = False

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(
        self,
    ) -> Dict:
        """
        Convert the result to a dictionary.
        """

        return {
            "validator_name": self.validator_name,
            "rule_code": self.rule_code,
            "success": self.success,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(
        cls,
        data: Dict,
    ) -> "ValidationResultModel":
        """
        Create a result from a dictionary.
        """

        return cls(
            validator_name=data.get(
                "validator_name",
                "",
            ),
            rule_code=data.get(
                "rule_code",
                "",
            ),
            success=data.get(
                "success",
                False,
            ),
            errors=list(
                data.get(
                    "errors",
                    [],
                )
            ),
            warnings=list(
                data.get(
                    "warnings",
                    [],
                )
            ),
            metadata=dict(
                data.get(
                    "metadata",
                    {},
                )
            ),
        )
        # ---------------------------------------------------------

    # Copy Support
    # ---------------------------------------------------------

    def copy(
        self,
    ) -> "ValidationResultModel":
        """
        Create a deep copy of the validation result.
        """

        return ValidationResultModel.from_dict(self.to_dict())

    # ---------------------------------------------------------
    # State Inspection
    # ---------------------------------------------------------

    def has_errors(
        self,
    ) -> bool:
        """
        Determine whether validation errors exist.
        """

        return len(self.errors) > 0

    def has_warnings(
        self,
    ) -> bool:
        """
        Determine whether validation warnings exist.
        """

        return len(self.warnings) > 0

    def is_successful(
        self,
    ) -> bool:
        """
        Determine whether validation succeeded.
        """

        return self.success and not self.has_errors()

    def is_failed(
        self,
    ) -> bool:
        """
        Determine whether validation failed.
        """

        return not self.is_successful()

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
    ) -> Dict:
        """
        Return validation statistics.
        """

        return {
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "metadata_count": len(self.metadata),
        }

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def error_count(
        self,
    ) -> int:
        """
        Number of validation errors.
        """

        return len(self.errors)

    @property
    def warning_count(
        self,
    ) -> int:
        """
        Number of validation warnings.
        """

        return len(self.warnings)

    @property
    def has_metadata(
        self,
    ) -> bool:
        """
        Determine whether metadata exists.
        """

        return len(self.metadata) > 0

    # ---------------------------------------------------------
    # Metadata Helpers
    # ---------------------------------------------------------

    def set_metadata(
        self,
        key: str,
        value,
    ) -> None:
        """
        Store a metadata value.
        """

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default=None,
    ):
        """
        Retrieve a metadata value.
        """

        return self.metadata.get(
            key,
            default,
        )
        # ---------------------------------------------------------

    # Summary
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> Dict:
        """
        Return a concise validation summary.
        """

        return {
            "validator_name": self.validator_name,
            "rule_code": self.rule_code,
            "success": self.is_successful(),
            "error_count": self.error_count,
            "warning_count": self.warning_count,
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
    ) -> Dict:
        """
        Return detailed validation diagnostics.
        """

        return {
            "summary": self.summary(),
            "statistics": self.statistics(),
            "metadata": dict(self.metadata),
        }

    # ---------------------------------------------------------
    # Component Information
    # ---------------------------------------------------------

    @property
    def version(
        self,
    ) -> str:
        """
        Model version.
        """

        return "2.0.0"

    @property
    def component_name(
        self,
    ) -> str:
        """
        Component name.
        """

        return "Validation Result Model"

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> Dict:
        """
        Return model health information.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "validator": self.validator_name,
            "status": ("PASSED" if self.is_successful() else "FAILED"),
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(
        self,
    ) -> Dict:
        """
        Describe model capabilities.
        """

        return {
            "serialization": True,
            "copy_support": True,
            "error_tracking": True,
            "warning_tracking": True,
            "metadata": True,
            "statistics": True,
            "summary": True,
            "diagnostics": True,
            "state_inspection": True,
        }

    # ---------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------

    def clear_metadata(
        self,
    ) -> None:
        """
        Remove all metadata entries.
        """

        self.metadata.clear()

    def reset(
        self,
    ) -> None:
        """
        Reset the validation result.
        """

        self.success = False

        self.errors.clear()

        self.warnings.clear()

        self.metadata.clear()
        # ---------------------------------------------------------

    # Information
    # ---------------------------------------------------------

    def validation_information(
        self,
    ) -> Dict:
        """
        Return validation result information.
        """

        return {
            "validator_name": self.validator_name,
            "rule_code": self.rule_code,
            "success": self.is_successful(),
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "version": self.version,
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            "ValidationResultModel("
            f"validator='{self.validator_name}', "
            f"success={self.is_successful()}, "
            f"errors={self.error_count}, "
            f"warnings={self.warning_count})"
        )

    def __str__(
        self,
    ) -> str:

        status = "PASSED" if self.is_successful() else "FAILED"

        return (
            f"{self.rule_code} | "
            f"{status} | "
            f"Errors={self.error_count} | "
            f"Warnings={self.warning_count}"
        )
