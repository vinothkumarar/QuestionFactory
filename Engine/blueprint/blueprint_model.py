"""
Question Factory OS v2.0

Blueprint Model

File
----
Engine/blueprint/blueprint_model.py

Description
-----------
Strongly typed representation of the compiled factory blueprint.

The BlueprintModel represents the complete manufacturing
knowledge base for Question Factory OS.

Once compiled it should be treated as immutable.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List


# ---------------------------------------------------------
# Factory Information
# ---------------------------------------------------------

@dataclass(slots=True)
class FactoryInfo:

    name: str = "Question Factory OS"

    version: str = "2.0.0"

    blueprint_version: str = "2.0.0"

    author: str = ""

    description: str = ""

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )


# ---------------------------------------------------------
# Rules
# ---------------------------------------------------------

@dataclass(slots=True)
class RuleBook:

    rules: Dict[str, str] = field(
        default_factory=dict
    )

    rebuild_rules: Dict[str, str] = field(
        default_factory=dict
    )

    generation_rules: Dict[str, str] = field(
        default_factory=dict
    )

    runtime_rules: Dict[str, str] = field(
        default_factory=dict
    )


# ---------------------------------------------------------
# Archetypes
# ---------------------------------------------------------

@dataclass(slots=True)
class ArchetypeBook:

    archetypes: Dict[str, Any] = field(
        default_factory=dict
    )
    # ---------------------------------------------------------
# Saturation
# ---------------------------------------------------------

@dataclass(slots=True)
class SaturationBook:
    """
    Stores saturation policies and tracking rules.

    These define when a subtopic, set, or chapter is considered
    complete and when manufacturing should advance.
    """

    policies: Dict[str, Any] = field(
        default_factory=dict
    )

    thresholds: Dict[str, Any] = field(
        default_factory=dict
    )

    progression_rules: Dict[str, Any] = field(
        default_factory=dict
    )


# ---------------------------------------------------------
# Schema
# ---------------------------------------------------------

@dataclass(slots=True)
class SchemaBook:
    """
    Defines the canonical schema used throughout the factory.
    """

    question_schema: Dict[str, Any] = field(
        default_factory=dict
    )

    csv_schema: Dict[str, Any] = field(
        default_factory=dict
    )

    metadata_schema: Dict[str, Any] = field(
        default_factory=dict
    )

    validation_rules: Dict[str, Any] = field(
        default_factory=dict
    )


# ---------------------------------------------------------
# Runtime Behavior
# ---------------------------------------------------------

@dataclass(slots=True)
class RuntimeBehavior:
    """
    Runtime execution behavior defined by the blueprint.
    """

    auto_continue: bool = True

    repair_before_expand: bool = True

    auto_checkpoint: bool = True

    enable_recovery: bool = True

    enable_logging: bool = True

    enable_packaging: bool = True

    checkpoint_interval: int = 1

    max_repair_cycles: int = 3


# ---------------------------------------------------------
# Folder Structure
# ---------------------------------------------------------

@dataclass(slots=True)
class FolderStructure:
    """
    Canonical folder layout expected by the factory.
    """

    root: str = "QuestionFactory"

    engine: str = "Engine"

    blueprint: str = "Blueprint"

    question_bank: str = "QuestionBank"

    upload: str = "Upload"

    logs: str = "Logs"

    metadata: str = "Metadata"

    progress: str = "Progress"

    batch_manifest: str = "BatchManifest"


# ---------------------------------------------------------
# Upload Rules
# ---------------------------------------------------------

@dataclass(slots=True)
class UploadRules:
    """
    Upload packaging and export configuration.
    """

    export_format: str = "CSV"

    validate_before_export: bool = True

    include_manifest: bool = True

    include_metadata: bool = True

    compress_output: bool = False

    output_directory: str = "Upload"

    archive_completed_batches: bool = True
    # ---------------------------------------------------------
# Version Control
# ---------------------------------------------------------

@dataclass(slots=True)
class VersionControl:
    """
    Blueprint versioning and compatibility information.

    This section allows future blueprint schema evolution
    while maintaining backward compatibility.
    """

    blueprint_version: str = "2.0.0"

    schema_version: int = 1

    minimum_factory_version: str = "2.0.0"

    compatible_factory_versions: List[str] = field(
        default_factory=lambda: ["2.0.0"]
    )

    frozen: bool = True

    release_date: str = ""

    release_notes: str = ""


# ---------------------------------------------------------
# Automation
# ---------------------------------------------------------

@dataclass(slots=True)
class AutomationSettings:
    """
    Autonomous manufacturing behavior configured by
    the blueprint.
    """

    autonomous_mode: bool = True

    auto_schedule: bool = True

    auto_quality_check: bool = True

    auto_repair: bool = True

    auto_package: bool = True

    auto_runtime_update: bool = True

    auto_logging: bool = True

    continue_after_success: bool = True

    stop_on_fatal_error: bool = True


# ---------------------------------------------------------
# Blueprint Metadata
# ---------------------------------------------------------

@dataclass(slots=True)
class BlueprintMetadata:
    """
    Metadata describing the compiled blueprint.
    """

    source_documents: List[str] = field(
        default_factory=list
    )

    compiled_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    compiler_version: str = "2.0.0"

    checksum: str = ""

    document_count: int = 0

    custom_properties: Dict[str, Any] = field(
        default_factory=dict
    )


# ---------------------------------------------------------
# Blueprint Model
# ---------------------------------------------------------

@dataclass(slots=True)
class BlueprintModel:
    """
    Root blueprint model.

    Represents the complete compiled factory knowledge base.

    Every subsystem receives the same BlueprintModel
    instance during execution.
    """

    factory: FactoryInfo = field(
        default_factory=FactoryInfo
    )

    rules: RuleBook = field(
        default_factory=RuleBook
    )

    archetypes: ArchetypeBook = field(
        default_factory=ArchetypeBook
    )

    saturation: SaturationBook = field(
        default_factory=SaturationBook
    )

    schema: SchemaBook = field(
        default_factory=SchemaBook
    )

    runtime: RuntimeBehavior = field(
        default_factory=RuntimeBehavior
    )

    folders: FolderStructure = field(
        default_factory=FolderStructure
    )

    upload: UploadRules = field(
        default_factory=UploadRules
    )

    version: VersionControl = field(
        default_factory=VersionControl
    )

    automation: AutomationSettings = field(
        default_factory=AutomationSettings
    )

    metadata: BlueprintMetadata = field(
        default_factory=BlueprintMetadata
    )
    # ---------------------------------------------------------
# Blueprint Operations
# ---------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the blueprint into a serializable dictionary.
        """

        return asdict(self)

    @classmethod
    def from_dict(
        cls,
        payload: Dict[str, Any],
    ) -> "BlueprintModel":
        """
        Reconstruct a BlueprintModel from a dictionary.

        Missing sections are initialized with defaults to
        support forward-compatible blueprint evolution.
        """

        return cls(
            factory=FactoryInfo(
                **payload.get("factory", {})
            ),
            rules=RuleBook(
                **payload.get("rules", {})
            ),
            archetypes=ArchetypeBook(
                **payload.get("archetypes", {})
            ),
            saturation=SaturationBook(
                **payload.get("saturation", {})
            ),
            schema=SchemaBook(
                **payload.get("schema", {})
            ),
            runtime=RuntimeBehavior(
                **payload.get("runtime", {})
            ),
            folders=FolderStructure(
                **payload.get("folders", {})
            ),
            upload=UploadRules(
                **payload.get("upload", {})
            ),
            version=VersionControl(
                **payload.get("version", {})
            ),
            automation=AutomationSettings(
                **payload.get("automation", {})
            ),
            metadata=BlueprintMetadata(
                **payload.get("metadata", {})
            ),
        )

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def is_frozen(self) -> bool:
        """
        Indicates whether the blueprint is frozen for
        production use.
        """

        return self.version.frozen

    @property
    def blueprint_version(self) -> str:
        """
        Return the blueprint version.
        """

        return self.version.blueprint_version

    @property
    def schema_version(self) -> int:
        """
        Return the blueprint schema version.
        """

        return self.version.schema_version

    @property
    def document_count(self) -> int:
        """
        Number of source documents compiled.
        """

        return self.metadata.document_count

    @property
    def source_documents(self) -> List[str]:
        """
        Source markdown documents used to build
        this blueprint.
        """

        return self.metadata.source_documents

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(self) -> Dict[str, Any]:
        """
        Return a concise blueprint summary.
        """

        return {
            "factory": self.factory.name,
            "factory_version": self.factory.version,
            "blueprint_version": self.blueprint_version,
            "schema_version": self.schema_version,
            "frozen": self.is_frozen,
            "documents": self.document_count,
            "compiled_at": self.metadata.compiled_at,
        }

    def diagnostics(self) -> Dict[str, Any]:
        """
        Return detailed blueprint diagnostics.
        """

        return {
            "summary": self.summary(),
            "automation": {
                "autonomous_mode": self.automation.autonomous_mode,
                "auto_schedule": self.automation.auto_schedule,
                "auto_quality_check": self.automation.auto_quality_check,
                "auto_repair": self.automation.auto_repair,
                "auto_package": self.automation.auto_package,
                "auto_runtime_update": self.automation.auto_runtime_update,
            },
            "runtime": {
                "repair_before_expand": (
                    self.runtime.repair_before_expand
                ),
                "auto_checkpoint": (
                    self.runtime.auto_checkpoint
                ),
                "enable_recovery": (
                    self.runtime.enable_recovery
                ),
            },
            "folders": {
                "engine": self.folders.engine,
                "blueprint": self.folders.blueprint,
                "question_bank": self.folders.question_bank,
                "upload": self.folders.upload,
            },
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            "BlueprintModel("
            f"version='{self.blueprint_version}', "
            f"schema={self.schema_version}, "
            f"documents={self.document_count})"
        )

    def __str__(self) -> str:
        return (
            f"{self.factory.name} "
            f"Blueprint v{self.blueprint_version}"
        )
        