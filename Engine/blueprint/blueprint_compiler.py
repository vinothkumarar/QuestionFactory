"""
Question Factory OS v2.0

Blueprint Compiler

File
----
Engine/blueprint/blueprint_compiler.py

Description
-----------
Compiles parsed blueprint documents into a strongly typed
BlueprintModel.

The compiler understands blueprint semantics but does not
perform final business validation. Validation belongs to the
BlueprintValidator.

Pipeline

Parsed Documents
        │
        ▼
BlueprintCompiler
        │
        ▼
BlueprintModel
"""

from __future__ import annotations

import logging
from typing import Dict

from Engine.blueprint.blueprint_model import (
    BlueprintModel,
)

from Engine.blueprint.blueprint_parser import (
    BlueprintParser,
    ParsedDocument,
)


class BlueprintCompiler:
    """
    Compiles parsed blueprint documents into a BlueprintModel.
    """

    def __init__(self) -> None:

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

        self.parser = BlueprintParser()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def compile(
        self,
        markdown_documents: Dict[str, str],
    ) -> BlueprintModel:
        """
        Compile the complete blueprint.

        Parameters
        ----------
        markdown_documents
            Dictionary mapping filename to markdown content.

        Returns
        -------
        BlueprintModel
        """

        self.logger.info(
            "Starting blueprint compilation."
        )

        parsed_documents = self.parser.parse(
            markdown_documents
        )

        blueprint = BlueprintModel()

        self._compile_factory_information(
            blueprint,
            parsed_documents,
        )

        self._compile_rules(
            blueprint,
            parsed_documents,
        )

        self._compile_archetypes(
            blueprint,
            parsed_documents,
        )

        self._compile_runtime(
            blueprint,
            parsed_documents,
        )

        self._compile_schema(
            blueprint,
            parsed_documents,
        )

        self._compile_folder_structure(
            blueprint,
            parsed_documents,
        )

        self._compile_upload(
            blueprint,
            parsed_documents,
        )

        self._compile_version(
            blueprint,
            parsed_documents,
        )

        self._compile_metadata(
            blueprint,
            parsed_documents,
        )

        self.logger.info(
            "Blueprint compilation completed."
        )

        return blueprint
            # ---------------------------------------------------------
    # Factory Information
    # ---------------------------------------------------------

    def _compile_factory_information(
        self,
        blueprint: BlueprintModel,
        documents: Dict[str, ParsedDocument],
    ) -> None:
        """
        Compile factory-level information.

        At this stage most values come from defaults defined in
        BlueprintModel. Future versions may extract additional
        metadata directly from the blueprint documents.
        """

        blueprint.factory.description = (
            "Autonomous Manufacturing Operating System "
            "for Question Factory."
        )

        self.logger.info(
            "Factory information compiled."
        )

    # ---------------------------------------------------------
    # Rules
    # ---------------------------------------------------------

    def _compile_rules(
        self,
        blueprint: BlueprintModel,
        documents: Dict[str, ParsedDocument],
    ) -> None:
        """
        Compile manufacturing rules.

        Source document:
            01_RULES.md
        """

        document = documents.get("01_RULES.md")

        if document is None:

            self.logger.warning(
                "Rules document not found."
            )

            return

        rules = blueprint.rules.rules

        for section in document.sections:

            bullet_items = (
                self.parser.extract_bullet_lists(
                    section
                )
            )

            numbered_items = (
                self.parser.extract_numbered_lists(
                    section
                )
            )

            collected_items = (
                bullet_items + numbered_items
            )

            if collected_items:

                rules[section.title] = (
                    "\n".join(collected_items)
                )

            else:

                rules[section.title] = (
                    "\n".join(section.content)
                    .strip()
                )

        self.logger.info(
            "Compiled %d rule section(s).",
            len(rules),
        )

    # ---------------------------------------------------------
    # Archetypes
    # ---------------------------------------------------------

    def _compile_archetypes(
        self,
        blueprint: BlueprintModel,
        documents: Dict[str, ParsedDocument],
    ) -> None:
        """
        Compile question archetypes.

        Source document:
            02_ARCHETYPES.md
        """

        document = documents.get(
            "02_ARCHETYPES.md"
        )

        if document is None:

            self.logger.warning(
                "Archetypes document not found."
            )

            return

        archetypes = (
            blueprint.archetypes.archetypes
        )

        for section in document.sections:

            archetypes[section.title] = {
                "content": (
                    "\n".join(section.content)
                    .strip()
                ),
                "bullet_items": (
                    self.parser.extract_bullet_lists(
                        section
                    )
                ),
                "tables": (
                    self.parser.extract_tables(
                        section
                    )
                ),
            }

        self.logger.info(
            "Compiled %d archetype section(s).",
            len(archetypes),
        )
            # ---------------------------------------------------------
    # Runtime
    # ---------------------------------------------------------

    def _compile_runtime(
        self,
        blueprint: BlueprintModel,
        documents: Dict[str, ParsedDocument],
    ) -> None:
        """
        Compile runtime behaviour.

        Source document:
            13_RUNTIME_BEHAVIOR.md
        """

        document = documents.get(
            "13_RUNTIME_BEHAVIOR.md"
        )

        if document is None:

            self.logger.warning(
                "Runtime behaviour document not found."
            )

            return

        runtime = blueprint.runtime

        for section in document.sections:

            text = "\n".join(
                section.content
            ).lower()

            title = section.title.lower()

            #
            # The compiler currently performs lightweight
            # semantic interpretation.
            #
            # Future versions should replace these heuristics
            # with dedicated runtime rule definitions.
            #

            if (
                "repair" in title
                or "repair before expand" in text
            ):
                runtime.repair_before_expand = True

            if (
                "checkpoint" in title
                or "checkpoint" in text
            ):
                runtime.auto_checkpoint = True

            if (
                "recovery" in title
                or "recovery" in text
            ):
                runtime.enable_recovery = True

            if (
                "logging" in title
                or "logging" in text
            ):
                runtime.enable_logging = True

            if (
                "packaging" in title
                or "package" in text
            ):
                runtime.enable_packaging = True

        self.logger.info(
            "Runtime behaviour compiled."
        )

    # ---------------------------------------------------------
    # Schema
    # ---------------------------------------------------------

    def _compile_schema(
        self,
        blueprint: BlueprintModel,
        documents: Dict[str, ParsedDocument],
    ) -> None:
        """
        Compile schema information.

        Source document:
            05_SCHEMA.md
        """

        document = documents.get(
            "05_SCHEMA.md"
        )

        if document is None:

            self.logger.warning(
                "Schema document not found."
            )

            return

        schema = blueprint.schema

        for section in document.sections:

            schema.validation_rules[
                section.title
            ] = "\n".join(
                section.content
            ).strip()

            tables = self.parser.extract_tables(
                section
            )

            if tables:

                schema.csv_schema[
                    section.title
                ] = tables

        self.logger.info(
            "Schema compiled."
        )

    # ---------------------------------------------------------
    # Folder Structure
    # ---------------------------------------------------------

    def _compile_folder_structure(
        self,
        blueprint: BlueprintModel,
        documents: Dict[str, ParsedDocument],
    ) -> None:
        """
        Compile expected folder structure.

        Source document:
            07_FOLDER_STRUCTURE.md
        """

        document = documents.get(
            "07_FOLDER_STRUCTURE.md"
        )

        if document is None:

            self.logger.warning(
                "Folder structure document not found."
            )

            return

        folders = blueprint.folders

        #
        # Preserve the document for diagnostics.
        #

        blueprint.metadata.custom_properties[
            "folder_structure_document"
        ] = "\n".join(

            line

            for section in document.sections

            for line in section.content

        ).strip()

        #
        # Folder defaults are already supplied by the
        # BlueprintModel.
        #
        # Future compiler versions may dynamically build
        # FolderStructure from the markdown itself.
        #

        self.logger.info(
            "Folder structure compiled."
        )
            # ---------------------------------------------------------
    # Upload
    # ---------------------------------------------------------

    def _compile_upload(
        self,
        blueprint: BlueprintModel,
        documents: Dict[str, ParsedDocument],
    ) -> None:
        """
        Compile upload and export configuration.

        Source document:
            08_UPLOAD_REPAIR.md
        """

        document = documents.get(
            "08_UPLOAD_REPAIR.md"
        )

        if document is None:

            self.logger.warning(
                "Upload document not found."
            )

            return

        upload = blueprint.upload

        for section in document.sections:

            text = "\n".join(
                section.content
            ).lower()

            if "csv" in text:
                upload.export_format = "CSV"

            if "metadata" in text:
                upload.include_metadata = True

            if "manifest" in text:
                upload.include_manifest = True

            if "validate" in text:
                upload.validate_before_export = True

            if "compress" in text:
                upload.compress_output = True

            if "archive" in text:
                upload.archive_completed_batches = True

        self.logger.info(
            "Upload configuration compiled."
        )

    # ---------------------------------------------------------
    # Version
    # ---------------------------------------------------------

    def _compile_version(
        self,
        blueprint: BlueprintModel,
        documents: Dict[str, ParsedDocument],
    ) -> None:
        """
        Compile blueprint version information.

        Source document:
            10_VERSION_CONTROL.md
        """

        document = documents.get(
            "10_VERSION_CONTROL.md"
        )

        if document is None:

            self.logger.warning(
                "Version document not found."
            )

            return

        version = blueprint.version

        version.release_notes = "\n\n".join(
            "\n".join(section.content).strip()
            for section in document.sections
            if section.content
        )

        version.release_date = (
            blueprint.metadata.compiled_at
        )

        self.logger.info(
            "Version information compiled."
        )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def _compile_metadata(
        self,
        blueprint: BlueprintModel,
        documents: Dict[str, ParsedDocument],
    ) -> None:
        """
        Compile blueprint metadata.
        """

        metadata = blueprint.metadata

        metadata.source_documents = sorted(
            documents.keys()
        )

        metadata.document_count = len(
            documents
        )

        metadata.custom_properties[
            "compiled_sections"
        ] = sum(
            len(document.sections)
            for document in documents.values()
        )

        metadata.custom_properties[
            "compiler"
        ] = self.__class__.__name__

        metadata.custom_properties[
            "parser_version"
        ] = self.parser.version

        self.logger.info(
            "Blueprint metadata compiled."
        )
            # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
        blueprint: BlueprintModel,
    ) -> Dict[str, object]:
        """
        Return a concise compilation summary.
        """

        return {
            "factory": blueprint.factory.name,
            "factory_version": blueprint.factory.version,
            "blueprint_version": (
                blueprint.version.blueprint_version
            ),
            "schema_version": (
                blueprint.version.schema_version
            ),
            "documents": (
                blueprint.metadata.document_count
            ),
            "compiled_sections": (
                blueprint.metadata.custom_properties.get(
                    "compiled_sections",
                    0,
                )
            ),
        }

    def diagnostics(
        self,
        blueprint: BlueprintModel,
    ) -> Dict[str, object]:
        """
        Return detailed compiler diagnostics.
        """

        return {
            "component": self.__class__.__name__,
            "summary": self.summary(
                blueprint
            ),
            "metadata": blueprint.metadata.custom_properties,
            "runtime": {
                "auto_checkpoint": (
                    blueprint.runtime.auto_checkpoint
                ),
                "enable_recovery": (
                    blueprint.runtime.enable_recovery
                ),
                "repair_before_expand": (
                    blueprint.runtime.repair_before_expand
                ),
            },
            "automation": {
                "autonomous_mode": (
                    blueprint.automation.autonomous_mode
                ),
                "auto_schedule": (
                    blueprint.automation.auto_schedule
                ),
                "auto_repair": (
                    blueprint.automation.auto_repair
                ),
                "auto_package": (
                    blueprint.automation.auto_package
                ),
            },
        }

    # ---------------------------------------------------------
    # Lifecycle Hooks
    # ---------------------------------------------------------

    def before_compile(
        self,
        documents: Dict[str, ParsedDocument],
    ) -> None:
        """
        Hook executed immediately before compilation.

        Override in derived implementations for metrics,
        telemetry or preprocessing.
        """

        return

    def after_compile(
        self,
        blueprint: BlueprintModel,
    ) -> None:
        """
        Hook executed after compilation completes.

        Override for custom post-processing.
        """

        return

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    @property
    def version(self) -> str:
        """
        Compiler version.
        """

        return "2.0.0"

    def health(self) -> Dict[str, object]:
        """
        Return compiler health information.
        """

        return {
            "component": self.__class__.__name__,
            "version": self.version,
            "status": "READY",
            "parser": self.parser.component_name,
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            "BlueprintCompiler("
            f"version='{self.version}')"
        )

    def __str__(self) -> str:
        return (
            f"BlueprintCompiler "
            f"[v{self.version}]"
        )
        