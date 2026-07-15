"""
Question Factory OS v2.0

Blueprint Loader

Responsible for loading and compiling the
factory blueprint.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List, Optional

from Engine.blueprint.blueprint_model import BlueprintModel
from Engine.blueprint.blueprint_compiler import BlueprintCompiler


class BlueprintLoader:
    """
    Loads the complete factory blueprint.

    The loader performs:

        Discovery

        Validation

        Compilation

        Caching

    Every subsystem receives the same
    immutable BlueprintModel.
    """

    DEFAULT_BLUEPRINT_DIRECTORY = Path("Blueprint")

    def __init__(
        self,
        blueprint_directory: Optional[Path] = None,
    ):

        self.logger = logging.getLogger(self.__class__.__name__)

        self.blueprint_directory = (
            blueprint_directory or self.DEFAULT_BLUEPRINT_DIRECTORY
        )

        self.compiler = BlueprintCompiler()

        self._cache: Optional[BlueprintModel] = None

    # -----------------------------------------------------

    def load(self) -> BlueprintModel:
        """
        Load the factory blueprint.

        Uses cache when available.
        """

        if self._cache is not None:

            self.logger.info("Using cached blueprint.")

            return self._cache

        markdown_files = self._discover()

        markdown_content = self._read_files(markdown_files)

        blueprint = self.compiler.compile(markdown_content)

        self.validate(blueprint)

        self._cache = blueprint

        self.logger.info("Blueprint successfully loaded.")

        return blueprint
        # -----------------------------------------------------

    # Blueprint Discovery
    # -----------------------------------------------------

    def _discover(self) -> List[Path]:
        """
        Discover all blueprint markdown files.

        Files are ordered lexicographically so that the blueprint
        is compiled in a deterministic sequence.
        """

        if not self.blueprint_directory.exists():
            raise FileNotFoundError(
                f"Blueprint directory not found: " f"{self.blueprint_directory}"
            )

        files = sorted(self.blueprint_directory.glob("*.md"))

        if not files:
            raise FileNotFoundError("No blueprint markdown files found.")

        self._verify_required_files(files)

        self.logger.info(
            "Discovered %d blueprint file(s).",
            len(files),
        )

        return files

    def _verify_required_files(
        self,
        files: List[Path],
    ) -> None:
        """
        Verify that all mandatory blueprint documents
        are present.

        Additional blueprint documents are allowed, but the
        required core set must always exist.
        """

        required_files = [
            "01_RULES.md",
            "02_ARCHETYPES.md",
            "03_SATURATION.md",
            "04_REBUILD.md",
            "05_SCHEMA.md",
            "06_PROGRESS.md",
            "07_FOLDER_STRUCTURE.md",
            "08_UPLOAD_REPAIR.md",
            "09_MASTER_AUTORUN.md",
            "10_VERSION_CONTROL.md",
            "11_GENERATION_ENGINE.md",
            "12_FOLDER_AUTOMATION.md",
            "13_RUNTIME_BEHAVIOR.md",
        ]

        discovered = {file.name for file in files}

        missing = [
            filename for filename in required_files if filename not in discovered
        ]

        if missing:
            raise RuntimeError(
                "Blueprint is incomplete. Missing file(s): " f"{', '.join(missing)}"
            )

        self.logger.info("Blueprint integrity verification passed.")

    # -----------------------------------------------------
    # Blueprint Reading
    # -----------------------------------------------------

    def _read_files(
        self,
        files: List[Path],
    ) -> Dict[str, str]:
        """
        Read all blueprint markdown files.

        Returns
        -------
        Dict[str, str]
            Mapping of filename to markdown content.
        """

        documents: Dict[str, str] = {}

        for file in files:

            self.logger.info(
                "Loading blueprint: %s",
                file.name,
            )

            with file.open(
                "r",
                encoding="utf-8",
            ) as fp:

                documents[file.name] = fp.read()

        self.logger.info(
            "Loaded %d blueprint document(s).",
            len(documents),
        )

        return documents
        # -----------------------------------------------------

    # Validation
    # -----------------------------------------------------

    def validate(
        self,
        blueprint: BlueprintModel,
    ) -> None:
        """
        Validate the compiled blueprint.

        The BlueprintCompiler is responsible for semantic
        validation during compilation. This method performs
        loader-level validation to ensure a usable blueprint
        instance has been produced.
        """

        if blueprint is None:
            raise ValueError("Blueprint compilation returned None.")

        if not isinstance(
            blueprint,
            BlueprintModel,
        ):
            raise TypeError("Invalid blueprint type returned by compiler.")

        self.logger.info("Blueprint validation successful.")

    # -----------------------------------------------------
    # Cache Management
    # -----------------------------------------------------

    def is_cached(self) -> bool:
        """
        Determine whether a compiled blueprint is currently
        cached.
        """

        return self._cache is not None

    def get_cached(self) -> Optional[BlueprintModel]:
        """
        Return the cached blueprint.

        Returns None when no blueprint has been loaded.
        """

        return self._cache

    def clear_cache(self) -> None:
        """
        Remove the cached blueprint.

        The next call to load() will perform a complete
        discovery and compilation cycle.
        """

        self.logger.info("Clearing blueprint cache.")

        self._cache = None

    def reload(self) -> BlueprintModel:
        """
        Force a complete reload of the blueprint.
        """

        self.clear_cache()

        self.logger.info("Reloading blueprint.")

        return self.load()

    # -----------------------------------------------------
    # Diagnostics
    # -----------------------------------------------------

    def blueprint_directory_exists(self) -> bool:
        """
        Determine whether the blueprint directory exists.
        """

        return self.blueprint_directory.exists()

    def discovered_file_count(self) -> int:
        """
        Return the number of blueprint markdown files
        currently available.
        """

        if not self.blueprint_directory_exists():
            return 0

        return len(list(self.blueprint_directory.glob("*.md")))

    def health(self) -> dict:
        """
        Return Blueprint Loader health information.
        """

        return {
            "component": self.__class__.__name__,
            "blueprint_directory": str(self.blueprint_directory),
            "directory_exists": (self.blueprint_directory_exists()),
            "cached": self.is_cached(),
            "discovered_files": (self.discovered_file_count()),
        }
        # -----------------------------------------------------

    # Blueprint Metadata
    # -----------------------------------------------------

    @property
    def version(self) -> str:
        """
        Blueprint Loader version.
        """

        return "2.0.0"

    @property
    def component_name(self) -> str:
        """
        Component identifier.
        """

        return "Blueprint Loader"

    @property
    def blueprint_path(self) -> Path:
        """
        Return the configured blueprint directory.
        """

        return self.blueprint_directory

    # -----------------------------------------------------
    # Information Helpers
    # -----------------------------------------------------

    def list_documents(self) -> List[str]:
        """
        Return the discovered blueprint document names.
        """

        if not self.blueprint_directory.exists():
            return []

        return sorted(file.name for file in self.blueprint_directory.glob("*.md"))

    def blueprint_exists(
        self,
        filename: str,
    ) -> bool:
        """
        Determine whether a specific blueprint document exists.
        """

        return (self.blueprint_directory / filename).exists()

    def document_path(
        self,
        filename: str,
    ) -> Path:
        """
        Return the absolute path to a blueprint document.
        """

        return self.blueprint_directory / filename

    # -----------------------------------------------------
    # Extension Hooks
    # -----------------------------------------------------

    def before_load(self) -> None:
        """
        Hook executed before blueprint loading begins.

        Override in derived implementations to perform
        custom initialization or telemetry.
        """

        return

    def after_load(
        self,
        blueprint: BlueprintModel,
    ) -> None:
        """
        Hook executed after a blueprint has been loaded
        and validated.

        Override for custom post-processing.
        """

        return

    def on_validation_complete(
        self,
        blueprint: BlueprintModel,
    ) -> None:
        """
        Hook executed after validation succeeds.

        Intended for future integrations such as plugin
        registration, metrics collection or diagnostics.
        """

        return

    # -----------------------------------------------------
    # Factory Integration
    # -----------------------------------------------------

    def initialize(self) -> None:
        """
        Initialize the Blueprint Loader.

        This method prepares the loader for long-running
        factory execution.
        """

        self.logger.info("Initializing Blueprint Loader.")

        self.before_load()

    def shutdown(self) -> None:
        """
        Shutdown the Blueprint Loader.

        Clears cached state and releases resources.
        """

        self.logger.info("Shutting down Blueprint Loader.")

        self.clear_cache()

        self.logger.info("Blueprint Loader shutdown complete.")
        # -----------------------------------------------------

    # Summary
    # -----------------------------------------------------

    def summary(self) -> Dict[str, object]:
        """
        Return a concise summary of the Blueprint Loader.

        Suitable for CLI output, dashboards and diagnostics.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "directory": str(self.blueprint_directory),
            "directory_exists": self.blueprint_directory_exists(),
            "cached": self.is_cached(),
            "document_count": self.discovered_file_count(),
            "documents": self.list_documents(),
        }

    # -----------------------------------------------------
    # Blueprint Information
    # -----------------------------------------------------

    def blueprint_loaded(self) -> bool:
        """
        Indicates whether a compiled blueprint is currently
        available.
        """

        return self._cache is not None

    def invalidate(self) -> None:
        """
        Invalidate the cached blueprint.

        The next call to load() will perform a complete
        reload and recompilation.
        """

        self.logger.info("Blueprint cache invalidated.")

        self.clear_cache()

    # -----------------------------------------------------
    # Diagnostics
    # -----------------------------------------------------

    def diagnostics(self) -> Dict[str, object]:
        """
        Return detailed diagnostic information.
        """

        return {
            "loader_version": self.version,
            "component": self.component_name,
            "blueprint_directory": str(self.blueprint_directory),
            "cached": self.blueprint_loaded(),
            "documents": self.list_documents(),
            "health": self.health(),
        }

    # -----------------------------------------------------
    # Representation
    # -----------------------------------------------------

    def __repr__(self) -> str:
        return (
            "BlueprintLoader("
            f"directory='{self.blueprint_directory}', "
            f"cached={self.is_cached()})"
        )

    def __str__(self) -> str:
        return f"{self.component_name} " f"[v{self.version}]"
