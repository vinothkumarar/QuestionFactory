"""
Question Factory OS v2.0
Autonomous Manufacturing

File:
    Engine/director/manufacturing_director.py

Description
-----------
The Manufacturing Director is the single orchestration authority for
Question Factory OS.

It coordinates the complete manufacturing lifecycle but never performs
business logic itself.

Responsibilities
----------------
* Load runtime state
* Initialize factory services
* Execute manufacturing cycle
* Coordinate scheduler
* Coordinate manufacturing engine
* Coordinate QA
* Coordinate repair
* Coordinate packaging
* Update runtime
* Write production logs

This module intentionally delegates all domain logic to specialized
components.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

# Director
from Engine.director.runtime_controller import RuntimeController
from Engine.director.production_scheduler import ProductionScheduler

# Blueprint
from Engine.blueprint.blueprint_loader import BlueprintLoader

# Manufacturing
from Engine.manufacturing.manufacturing_engine import ManufacturingEngine

# QA
from Engine.qa.quality_lab import QualityLab

# Repair
from Engine.repair.repair_engine import RepairEngine

# Packaging
from Engine.packaging.packaging_engine import PackagingEngine

# Logging
from Engine.logging.production_logger import ProductionLogger


class FactoryState(Enum):
    """Factory execution states."""

    IDLE = "IDLE"
    INITIALIZING = "INITIALIZING"
    LOADING_BLUEPRINT = "LOADING_BLUEPRINT"
    PLANNING = "PLANNING"
    MANUFACTURING = "MANUFACTURING"
    VERIFYING = "VERIFYING"
    REPAIRING = "REPAIRING"
    PACKAGING = "PACKAGING"
    UPDATING_RUNTIME = "UPDATING_RUNTIME"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass(slots=True)
class ManufacturingContext:
    """
    Shared context passed through the manufacturing lifecycle.
    """

    runtime: Dict[str, Any] = field(default_factory=dict)

    blueprint: Optional[Any] = None

    production_node: Optional[Any] = None

    manufactured_batch: Optional[Any] = None

    qa_report: Optional[Any] = None

    repair_report: Optional[Any] = None

    package_result: Optional[Any] = None

    started_at: datetime = field(default_factory=datetime.utcnow)

    metadata: Dict[str, Any] = field(default_factory=dict)


class ManufacturingDirector:
    """
    Central orchestration engine.

    The director contains NO question generation logic.

    It only coordinates specialized factory departments.
    """

    def __init__(self) -> None:

        self.logger = logging.getLogger(self.__class__.__name__)

        self.state = FactoryState.IDLE

        self.runtime_controller = RuntimeController()

        self.scheduler = ProductionScheduler()

        self.blueprint_loader = BlueprintLoader()

        self.manufacturing_engine = ManufacturingEngine()

        self.quality_lab = QualityLab()

        self.repair_engine = RepairEngine()

        self.packaging_engine = PackagingEngine()

        self.production_logger = ProductionLogger()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def start_factory(self) -> None:
        """
        Factory bootstrap.

        Initializes every subsystem required to begin production.
        """

        self.logger.info("Initializing Manufacturing Director")

        self.state = FactoryState.INITIALIZING

        self.production_logger.factory_started()

        self.logger.info("Factory initialized successfully")

    def execute(self) -> None:
        """
        Execute one autonomous manufacturing cycle.

        A single cycle produces one approved batch.
        """

        context = ManufacturingContext()

        try:

            self._load_runtime(context)

            self._load_blueprint(context)

            self._plan_production(context)

            self._manufacture(context)

            self._quality_verification(context)

            self._repair_if_required(context)

            self._package(context)

            self._update_runtime(context)

            self._finalize(context)

        except Exception as ex:

            self.state = FactoryState.FAILED

            self.production_logger.factory_failed(str(ex))

            self.logger.exception(ex)

            raise
            # ---------------------------------------------------------

    # Private Lifecycle
    # ---------------------------------------------------------

    def _load_runtime(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Load the persisted runtime state.

        The runtime is the factory's single source of truth for
        determining the current manufacturing position.
        """

        self.logger.info("Loading runtime state")

        self.state = FactoryState.INITIALIZING

        runtime_state = self.runtime_controller.load()

        context.runtime = runtime_state

        self.production_logger.runtime_loaded(runtime_state)

    def _load_blueprint(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Load the frozen blueprint.

        The blueprint defines manufacturing rules, quality
        constraints, schema requirements, and production policies.
        """

        self.logger.info("Loading frozen blueprint")

        self.state = FactoryState.LOADING_BLUEPRINT

        blueprint = self.blueprint_loader.load()

        context.blueprint = blueprint

        self.production_logger.blueprint_loaded()

    def _plan_production(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Ask the scheduler to determine the next production node.

        The scheduler decides:
            - Unit
            - Chapter
            - Subtopic
            - Set
            - Batch
            - Question Range

        The Manufacturing Director never makes these decisions.
        """

        self.logger.info("Planning next manufacturing node")

        self.state = FactoryState.PLANNING

        node = self.scheduler.get_next_node(
            runtime=context.runtime,
            blueprint=context.blueprint,
        )

        context.production_node = node

        self.production_logger.production_planned(node)

    def _manufacture(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Produce one candidate batch.

        The manufacturing engine performs the complete generation
        process and returns an unapproved batch.
        """

        self.logger.info("Starting manufacturing")

        self.state = FactoryState.MANUFACTURING

        batch = self.manufacturing_engine.manufacture(
            node=context.production_node,
            blueprint=context.blueprint,
        )

        context.manufactured_batch = batch

        self.production_logger.batch_manufactured(batch)

    def _quality_verification(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Execute Quality Assurance.

        The Quality Lab performs all verification including:

            • R01
            • R02
            • R03
            • Mathematical validation
            • Ambiguity detection
            • Distractor validation
            • Difficulty validation
            • Coverage validation
            • CSV schema validation
        """

        self.logger.info("Running quality verification")

        self.state = FactoryState.VERIFYING

        qa_report = self.quality_lab.verify(
            batch=context.manufactured_batch,
            blueprint=context.blueprint,
        )

        context.qa_report = qa_report

        self.production_logger.quality_completed(qa_report)

    def _repair_if_required(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Execute automatic repair when QA identifies defects.

        Repair-before-expand is a core manufacturing principle.
        """

        if context.qa_report.is_success:
            return

        self.logger.info("Repair cycle required")

        self.state = FactoryState.REPAIRING

        repair_report = self.repair_engine.repair(
            batch=context.manufactured_batch,
            qa_report=context.qa_report,
            blueprint=context.blueprint,
        )

        context.repair_report = repair_report

        self.production_logger.repair_completed(repair_report)

        if not repair_report.is_success:

            raise RuntimeError(
                "Automatic repair failed. " "Manufacturing cycle aborted."
            )

        self.logger.info("Re-running QA after repair")

        qa_report = self.quality_lab.verify(
            batch=context.manufactured_batch,
            blueprint=context.blueprint,
        )

        context.qa_report = qa_report

        if not qa_report.is_success:

            raise RuntimeError(
                "Batch failed quality verification " "after repair cycle."
            )

    def _package(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Package the approved manufacturing output.

        The Packaging Engine is responsible for creating all
        production deliverables (CSV, JSON, manifests, reports,
        upload bundles, etc.).
        """

        self.logger.info("Packaging approved batch")

        self.state = FactoryState.PACKAGING

        package_result = self.packaging_engine.package(
            batch=context.manufactured_batch,
            qa_report=context.qa_report,
            production_node=context.production_node,
            runtime=context.runtime,
        )

        context.package_result = package_result

        self.production_logger.packaging_completed(package_result)

    def _update_runtime(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Persist the next runtime position.

        Runtime is only updated after successful packaging to
        guarantee recoverable manufacturing.
        """

        self.logger.info("Updating runtime")

        self.state = FactoryState.UPDATING_RUNTIME

        next_runtime = self.runtime_controller.build_next_runtime(
            current_runtime=context.runtime,
            production_node=context.production_node,
            package_result=context.package_result,
        )

        self.runtime_controller.save(next_runtime)

        context.runtime = next_runtime

        self.production_logger.runtime_updated(next_runtime)

    def _finalize(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Finalize a successful manufacturing cycle.
        """

        self.state = FactoryState.COMPLETED

        completed_at = datetime.utcnow()

        duration = (completed_at - context.started_at).total_seconds()

        summary = {
            "state": self.state.value,
            "duration_seconds": duration,
            "completed_at": completed_at.isoformat(),
            "production_node": context.production_node,
        }

        self.production_logger.factory_completed(summary)

        self.logger.info(
            "Manufacturing cycle completed successfully " "(%.2f seconds)",
            duration,
        )

    # ---------------------------------------------------------
    # State Helpers
    # ---------------------------------------------------------

    @property
    def current_state(self) -> FactoryState:
        """
        Return the current factory execution state.
        """

        return self.state

    @property
    def is_running(self) -> bool:
        """
        True while the factory is actively processing a cycle.
        """

        return self.state not in (
            FactoryState.IDLE,
            FactoryState.COMPLETED,
            FactoryState.FAILED,
        )

    @property
    def has_failed(self) -> bool:
        """
        Indicates whether the previous manufacturing cycle failed.
        """

        return self.state == FactoryState.FAILED

    @property
    def is_completed(self) -> bool:
        """
        Indicates whether the current manufacturing cycle
        completed successfully.
        """

        return self.state == FactoryState.COMPLETED

    # ---------------------------------------------------------
    # Convenience Operations
    # ---------------------------------------------------------

    def run(self) -> None:
        """
        Execute one complete manufacturing cycle.

        This is the primary entry point for the autonomous
        manufacturing system.
        """

        self.start_factory()

        self.execute()

    def shutdown(self) -> None:
        """
        Gracefully stop the Manufacturing Director.
        """

        self.logger.info("Stopping Manufacturing Director")

        self.state = FactoryState.IDLE

        self.production_logger.factory_stopped()

        self.logger.info("Manufacturing Director stopped")
        # ---------------------------------------------------------

    # Health & Diagnostics
    # ---------------------------------------------------------

    def health(self) -> Dict[str, Any]:
        """
        Return the current health status of the Manufacturing Director.

        This method is intended for dashboards, monitoring, CLI tools,
        and future REST endpoints.
        """

        return {
            "component": self.__class__.__name__,
            "state": self.state.value,
            "running": self.is_running,
            "completed": self.is_completed,
            "failed": self.has_failed,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def validate_dependencies(self) -> None:
        """
        Validate that all required factory services are available.

        This check runs before production begins to detect missing
        components early.
        """

        required_services = {
            "RuntimeController": self.runtime_controller,
            "ProductionScheduler": self.scheduler,
            "BlueprintLoader": self.blueprint_loader,
            "ManufacturingEngine": self.manufacturing_engine,
            "QualityLab": self.quality_lab,
            "RepairEngine": self.repair_engine,
            "PackagingEngine": self.packaging_engine,
            "ProductionLogger": self.production_logger,
        }

        missing = [
            name for name, service in required_services.items() if service is None
        ]

        if missing:
            raise RuntimeError(
                "Manufacturing Director initialization failed. "
                f"Missing services: {', '.join(missing)}"
            )

        self.logger.info(
            "Dependency validation successful (%d services)",
            len(required_services),
        )

    # ---------------------------------------------------------
    # Extension Hooks
    # ---------------------------------------------------------

    def before_cycle(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Hook executed immediately before a manufacturing cycle starts.

        Override in derived implementations if additional behavior is
        required.
        """

        return

    def after_cycle(
        self,
        context: ManufacturingContext,
    ) -> None:
        """
        Hook executed after a successful manufacturing cycle.

        Override in derived implementations if additional behavior is
        required.
        """

        return

    def on_failure(
        self,
        exception: Exception,
        context: Optional[ManufacturingContext] = None,
    ) -> None:
        """
        Hook executed when a manufacturing cycle fails.

        Override for custom notification, alerting, telemetry,
        or recovery logic.
        """

        self.logger.error(
            "Manufacturing cycle failed: %s",
            exception,
        )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    @property
    def version(self) -> str:
        """
        Manufacturing Director version.
        """

        return "2.0.0"

    @property
    def component_name(self) -> str:
        """
        Component identifier.
        """

        return "Manufacturing Director"

    @property
    def architecture(self) -> str:
        """
        Architecture identifier.
        """

        return "Question Factory OS v2.0"

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"{self.component_name}("
            f"version={self.version}, "
            f"state={self.state.value})"
        )

    def __str__(self) -> str:
        return f"{self.component_name} " f"[{self.state.value}]"
