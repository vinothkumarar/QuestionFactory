"""
Question Factory OS v2.0

Blueprint Validator

File
----
Engine/blueprint/blueprint_validator.py

Description
-----------
Validates compiled BlueprintModel instances before they are
used by the factory.

The validator performs structural and semantic validation
but never mutates the blueprint.

Pipeline

BlueprintModel
      │
      ▼
BlueprintValidator
      │
      ▼
Validated Blueprint
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import List

from Engine.blueprint.blueprint_model import (
    BlueprintModel,
)

# ---------------------------------------------------------
# Validation Result
# ---------------------------------------------------------


@dataclass(slots=True)
class ValidationResult:
    """
    Result returned by BlueprintValidator.
    """

    valid: bool = True

    errors: List[str] = field(default_factory=list)

    warnings: List[str] = field(default_factory=list)

    validated_sections: int = 0


# ---------------------------------------------------------
# Blueprint Validator
# ---------------------------------------------------------


class BlueprintValidator:
    """
    Validates BlueprintModel instances.
    """

    def __init__(self) -> None:

        self.logger = logging.getLogger(self.__class__.__name__)

    # -----------------------------------------------------
    # Public API
    # -----------------------------------------------------

    def validate(
        self,
        blueprint: BlueprintModel,
    ) -> ValidationResult:
        """
        Validate a compiled blueprint.

        Returns
        -------
        ValidationResult
        """

        result = ValidationResult()

        self._validate_structure(
            blueprint,
            result,
        )

        self._validate_versions(
            blueprint,
            result,
        )

        self._validate_runtime(
            blueprint,
            result,
        )

        self._validate_automation(
            blueprint,
            result,
        )

        self._validate_folders(
            blueprint,
            result,
        )

        self._validate_upload(
            blueprint,
            result,
        )

        result.valid = len(result.errors) == 0

        self.logger.info(
            "Blueprint validation completed " "(valid=%s).",
            result.valid,
        )

        return result
        # -----------------------------------------------------

    # Structure Validation
    # -----------------------------------------------------

    def _validate_structure(
        self,
        blueprint: BlueprintModel,
        result: ValidationResult,
    ) -> None:
        """
        Validate that all required blueprint domains exist.
        """

        required_sections = [
            ("factory", blueprint.factory),
            ("rules", blueprint.rules),
            ("archetypes", blueprint.archetypes),
            ("saturation", blueprint.saturation),
            ("schema", blueprint.schema),
            ("runtime", blueprint.runtime),
            ("folders", blueprint.folders),
            ("upload", blueprint.upload),
            ("version", blueprint.version),
            ("automation", blueprint.automation),
            ("metadata", blueprint.metadata),
        ]

        for section_name, section in required_sections:

            if section is None:

                result.errors.append(f"Missing blueprint section: " f"{section_name}")

            else:

                result.validated_sections += 1

        if blueprint.metadata.document_count <= 0:
            result.warnings.append(
                "Blueprint contains no recorded " "source documents."
            )

    # -----------------------------------------------------
    # Version Validation
    # -----------------------------------------------------

    def _validate_versions(
        self,
        blueprint: BlueprintModel,
        result: ValidationResult,
    ) -> None:
        """
        Validate blueprint version information.
        """

        version = blueprint.version

        if not version.blueprint_version:

            result.errors.append("Blueprint version is missing.")

        if version.schema_version <= 0:

            result.errors.append("Invalid schema version.")

        if not version.minimum_factory_version:

            result.warnings.append("Minimum factory version " "not specified.")

        if not version.frozen:

            result.warnings.append("Blueprint is not marked as frozen.")

    # -----------------------------------------------------
    # Runtime Validation
    # -----------------------------------------------------

    def _validate_runtime(
        self,
        blueprint: BlueprintModel,
        result: ValidationResult,
    ) -> None:
        """
        Validate runtime configuration.
        """

        runtime = blueprint.runtime

        if runtime.max_repair_cycles < 1:

            result.errors.append("Maximum repair cycles " "must be at least 1.")

        if runtime.checkpoint_interval < 1:

            result.errors.append("Checkpoint interval " "must be greater than zero.")

        if runtime.enable_recovery and not runtime.auto_checkpoint:

            result.warnings.append(
                "Recovery is enabled without " "automatic checkpoints."
            )

        if runtime.repair_before_expand and runtime.max_repair_cycles == 1:

            result.warnings.append(
                "Repair-before-expand is enabled " "with only one repair attempt."
            )
            # -----------------------------------------------------

    # Automation Validation
    # -----------------------------------------------------

    def _validate_automation(
        self,
        blueprint: BlueprintModel,
        result: ValidationResult,
    ) -> None:
        """
        Validate autonomous factory configuration.
        """

        automation = blueprint.automation

        if automation.auto_repair and not automation.auto_quality_check:

            result.warnings.append(
                "Automatic repair is enabled "
                "while automatic quality checks "
                "are disabled."
            )

        if automation.auto_schedule and not automation.autonomous_mode:

            result.warnings.append(
                "Automatic scheduling is enabled " "while autonomous mode is disabled."
            )

        if automation.auto_package and not automation.auto_runtime_update:

            result.warnings.append(
                "Automatic packaging is enabled " "without automatic runtime updates."
            )

    # -----------------------------------------------------
    # Folder Validation
    # -----------------------------------------------------

    def _validate_folders(
        self,
        blueprint: BlueprintModel,
        result: ValidationResult,
    ) -> None:
        """
        Validate folder configuration.
        """

        folders = blueprint.folders

        required = {
            "engine": folders.engine,
            "blueprint": folders.blueprint,
            "question_bank": folders.question_bank,
            "upload": folders.upload,
            "logs": folders.logs,
            "metadata": folders.metadata,
            "progress": folders.progress,
        }

        for name, value in required.items():

            if not value:

                result.errors.append(f"Folder mapping missing: {name}")

    # -----------------------------------------------------
    # Upload Validation
    # -----------------------------------------------------

    def _validate_upload(
        self,
        blueprint: BlueprintModel,
        result: ValidationResult,
    ) -> None:
        """
        Validate export configuration.
        """

        upload = blueprint.upload

        supported_formats = {
            "CSV",
        }

        if upload.export_format not in supported_formats:

            result.errors.append(
                "Unsupported export format: " f"{upload.export_format}"
            )

        if not upload.output_directory:

            result.errors.append("Upload output directory " "is not configured.")

        if upload.compress_output and upload.export_format != "CSV":

            result.warnings.append(
                "Compression is enabled for an " "unrecognized export format."
            )

        if upload.include_manifest and not upload.include_metadata:

            result.warnings.append(
                "Manifest generation is enabled " "without metadata inclusion."
            )
            # -----------------------------------------------------

    # Validation Summary
    # -----------------------------------------------------

    def summary(
        self,
        result: ValidationResult,
    ) -> dict:
        """
        Return a concise validation summary.
        """

        return {
            "valid": result.valid,
            "validated_sections": (result.validated_sections),
            "error_count": len(result.errors),
            "warning_count": len(result.warnings),
        }

    def diagnostics(
        self,
        result: ValidationResult,
    ) -> dict:
        """
        Return detailed validation diagnostics.
        """

        return {
            "summary": self.summary(result),
            "errors": result.errors,
            "warnings": result.warnings,
        }

    # -----------------------------------------------------
    # Convenience APIs
    # -----------------------------------------------------

    def has_errors(
        self,
        result: ValidationResult,
    ) -> bool:
        """
        Determine whether validation produced errors.
        """

        return len(result.errors) > 0

    def has_warnings(
        self,
        result: ValidationResult,
    ) -> bool:
        """
        Determine whether validation produced warnings.
        """

        return len(result.warnings) > 0

    def raise_on_failure(
        self,
        result: ValidationResult,
    ) -> None:
        """
        Raise an exception when validation fails.
        """

        if result.valid:
            return

        message = "\n".join(result.errors)

        raise ValueError(f"Blueprint validation failed:\n{message}")

    # -----------------------------------------------------
    # Lifecycle Hooks
    # -----------------------------------------------------

    def before_validation(
        self,
        blueprint: BlueprintModel,
    ) -> None:
        """
        Hook executed immediately before validation.

        Override in derived implementations to perform
        custom preprocessing or telemetry.
        """

        return

    def after_validation(
        self,
        blueprint: BlueprintModel,
        result: ValidationResult,
    ) -> None:
        """
        Hook executed after validation completes.

        Override for metrics collection or custom reporting.
        """

        return

    # -----------------------------------------------------
    # Health
    # -----------------------------------------------------

    @property
    def version(self) -> str:
        """
        Validator version.
        """

        return "2.0.0"

    def health(self) -> dict:
        """
        Return validator health information.
        """

        return {
            "component": self.__class__.__name__,
            "version": self.version,
            "status": "READY",
        }
        # -----------------------------------------------------

    # Validator Information
    # -----------------------------------------------------

    @property
    def component_name(self) -> str:
        """
        Validator component name.
        """

        return "Blueprint Validator"

    def supported_domains(self) -> List[str]:
        """
        Return the validation domains supported by
        this validator.
        """

        return [
            "structure",
            "version",
            "runtime",
            "automation",
            "folders",
            "upload",
        ]

    def capabilities(self) -> dict:
        """
        Describe validator capabilities.
        """

        return {
            "structural_validation": True,
            "version_validation": True,
            "runtime_validation": True,
            "automation_validation": True,
            "folder_validation": True,
            "upload_validation": True,
            "diagnostics": True,
            "health_reporting": True,
        }

    # -----------------------------------------------------
    # Utility Methods
    # -----------------------------------------------------

    def reset_result(self) -> ValidationResult:
        """
        Create a fresh validation result.

        Useful for repeated validation runs.
        """

        return ValidationResult()

    # -----------------------------------------------------
    # Representation
    # -----------------------------------------------------

    def __repr__(self) -> str:
        return "BlueprintValidator(" f"version='{self.version}')"

    def __str__(self) -> str:
        return f"{self.component_name} " f"[v{self.version}]"
