"""
Question Factory OS v2.0
Runtime Model

File:
    Engine/models/runtime_model.py

Description
-----------
Defines the strongly typed runtime model used throughout
Question Factory OS.

The runtime model is the single source of truth describing
the current manufacturing position, factory status,
production statistics and recovery information.

Every subsystem should consume this model instead of raw
dictionaries.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict

# ---------------------------------------------------------
# Factory
# ---------------------------------------------------------


@dataclass(slots=True)
class FactoryStateModel:
    """
    Overall factory execution state.
    """

    version: str = "2.0.0"

    status: str = "IDLE"

    started_at: str = ""

    completed_at: str = ""

    last_updated: str = ""

    current_cycle_id: str = ""


# ---------------------------------------------------------
# Production
# ---------------------------------------------------------


@dataclass(slots=True)
class ProductionStateModel:
    """
    Current manufacturing location.
    """

    subject: str = ""

    unit: str = ""

    chapter: str = ""

    subtopic: str = ""

    set_number: int = 1

    batch_number: int = 1

    question_from: int = 1

    question_to: int = 10

    next_question_number: int = 1

    production_node: str = ""

    batch_id: str = ""
    # ---------------------------------------------------------


# Statistics
# ---------------------------------------------------------


@dataclass(slots=True)
class StatisticsModel:
    """
    Manufacturing statistics accumulated over the lifetime
    of the factory.
    """

    total_questions: int = 0

    total_batches: int = 0

    successful_batches: int = 0

    failed_batches: int = 0

    repaired_batches: int = 0

    total_repair_cycles: int = 0

    total_runtime_seconds: float = 0.0

    average_batch_time_seconds: float = 0.0

    last_batch_duration_seconds: float = 0.0


# ---------------------------------------------------------
# History
# ---------------------------------------------------------


@dataclass(slots=True)
class HistoryModel:
    """
    Stores the most recent production history.

    This information is primarily used for reporting,
    dashboards and operator diagnostics.
    """

    last_subject: str = ""

    last_unit: str = ""

    last_chapter: str = ""

    last_subtopic: str = ""

    last_set_number: int = 0

    last_batch_number: int = 0

    last_batch_id: str = ""

    last_production_node: str = ""

    last_completed_at: str = ""

    last_status: str = ""


# ---------------------------------------------------------
# Recovery
# ---------------------------------------------------------


@dataclass(slots=True)
class RecoveryModel:
    """
    Recovery information used to resume manufacturing
    after an interruption.

    This enables autonomous recovery without requiring
    manual intervention.
    """

    checkpoint_id: str = ""

    checkpoint_time: str = ""

    last_successful_stage: str = ""

    resume_from_stage: str = ""

    recovery_required: bool = False

    interrupted: bool = False

    interruption_reason: str = ""

    retry_count: int = 0


# ---------------------------------------------------------
# Runtime Root
# ---------------------------------------------------------


@dataclass(slots=True)
class RuntimeModel:
    """
    Root runtime model shared across the factory.
    """

    factory: FactoryStateModel = field(default_factory=FactoryStateModel)

    production: ProductionStateModel = field(default_factory=ProductionStateModel)

    statistics: StatisticsModel = field(default_factory=StatisticsModel)

    history: HistoryModel = field(default_factory=HistoryModel)

    recovery: RecoveryModel = field(default_factory=RecoveryModel)

    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    # ---------------------------------------------------------
    # Runtime Operations
    # ---------------------------------------------------------

    def touch(self) -> None:
        """
        Update the runtime modification timestamp.
        """

        self.updated_at = datetime.utcnow().isoformat()

        self.factory.last_updated = self.updated_at

    def start_cycle(self, cycle_id: str) -> None:
        """
        Mark the beginning of a manufacturing cycle.
        """

        now = datetime.utcnow().isoformat()

        self.factory.status = "RUNNING"
        self.factory.current_cycle_id = cycle_id
        self.factory.started_at = now
        self.factory.last_updated = now

        self.touch()

    def complete_cycle(self) -> None:
        """
        Mark the current manufacturing cycle as completed.
        """

        now = datetime.utcnow().isoformat()

        self.factory.status = "COMPLETED"
        self.factory.completed_at = now
        self.factory.last_updated = now

        self.statistics.successful_batches += 1

        self.touch()

    def mark_failed(self, reason: str = "") -> None:
        """
        Mark the current manufacturing cycle as failed.
        """

        now = datetime.utcnow().isoformat()

        self.factory.status = "FAILED"
        self.factory.completed_at = now
        self.factory.last_updated = now

        self.statistics.failed_batches += 1

        self.recovery.recovery_required = True
        self.recovery.interrupted = True
        self.recovery.interruption_reason = reason

        self.touch()

    def create_checkpoint(self, stage: str) -> None:
        """
        Save a recovery checkpoint for the current manufacturing stage.
        """

        now = datetime.utcnow().isoformat()

        self.recovery.last_successful_stage = stage
        self.recovery.resume_from_stage = stage
        self.recovery.checkpoint_time = now

        self.touch()

    def reset_cycle(self) -> None:
        """
        Reset transient cycle state while preserving production progress.
        """

        self.factory.status = "IDLE"
        self.factory.current_cycle_id = ""

        self.recovery.recovery_required = False
        self.recovery.interrupted = False
        self.recovery.interruption_reason = ""
        self.recovery.resume_from_stage = ""

        self.touch()

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the runtime model into a serializable dictionary.
        """

        return asdict(self)

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "RuntimeModel":
        """
        Construct a RuntimeModel from a dictionary.

        Missing sections are initialized with defaults to support
        forward-compatible schema evolution.
        """

        return cls(
            factory=FactoryStateModel(**data.get("factory", {})),
            production=ProductionStateModel(**data.get("production", {})),
            statistics=StatisticsModel(**data.get("statistics", {})),
            history=HistoryModel(**data.get("history", {})),
            recovery=RecoveryModel(**data.get("recovery", {})),
            created_at=data.get(
                "created_at",
                datetime.utcnow().isoformat(),
            ),
            updated_at=data.get(
                "updated_at",
                datetime.utcnow().isoformat(),
            ),
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def current_node(self) -> str:
        """
        Return the current production node identifier.
        """

        return self.production.production_node

    @property
    def current_batch(self) -> str:
        """
        Return the active batch identifier.
        """

        return self.production.batch_id

    @property
    def is_recovery_required(self) -> bool:
        """
        Indicates whether the factory should resume from
        a recovery checkpoint.
        """

        return self.recovery.recovery_required

    @property
    def is_running(self) -> bool:
        """
        Indicates whether a manufacturing cycle is active.
        """

        return self.factory.status == "RUNNING"

    def __repr__(self) -> str:
        return (
            f"RuntimeModel("
            f"status={self.factory.status}, "
            f"node='{self.production.production_node}', "
            f"batch='{self.production.batch_id}')"
        )
