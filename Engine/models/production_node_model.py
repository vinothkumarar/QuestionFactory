"""
Question Factory OS v2.0
Production Node Model

File
----
Engine/models/production_node_model.py

Description
-----------
Defines the Manufacturing Order processed by the factory.

A Production Node represents exactly one autonomous
manufacturing task.

The Scheduler creates it.

The Manufacturing Director coordinates it.

Every downstream subsystem consumes it.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict
import uuid

# ---------------------------------------------------------
# Production Location
# ---------------------------------------------------------


@dataclass(slots=True)
class ProductionLocation:

    subject: str = ""

    unit: str = ""

    chapter: str = ""

    subtopic: str = ""

    set_number: int = 1

    batch_number: int = 1


# ---------------------------------------------------------
# Question Range
# ---------------------------------------------------------


@dataclass(slots=True)
class QuestionRange:

    question_from: int = 1

    question_to: int = 10

    expected_questions: int = 10


# ---------------------------------------------------------
# Execution Information
# ---------------------------------------------------------


@dataclass(slots=True)
class ExecutionInfo:

    priority: int = 100

    retry_count: int = 0

    max_retry: int = 3

    estimated_duration_seconds: int = 60

    execution_order: int = 0

    scheduled_at: str = ""

    started_at: str = ""

    completed_at: str = ""
    # ---------------------------------------------------------


# Quality Information
# ---------------------------------------------------------


@dataclass(slots=True)
class QualityInfo:
    """
    Manufacturing quality requirements associated with
    this production node.
    """

    require_r01: bool = True

    require_r02: bool = True

    require_r03: bool = True

    require_uniqueness_check: bool = True

    require_ambiguity_check: bool = True

    require_difficulty_validation: bool = True

    require_pyq_similarity_check: bool = True

    require_csv_validation: bool = True

    repair_before_expand: bool = True


# ---------------------------------------------------------
# Node Metadata
# ---------------------------------------------------------


@dataclass(slots=True)
class NodeMetadata:
    """
    Additional metadata describing the production order.
    """

    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    production_node: str = ""

    batch_id: str = ""

    blueprint_version: str = "2.0.0"

    factory_version: str = "2.0.0"

    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    created_by: str = "ProductionScheduler"

    tags: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------
# Production Node
# ---------------------------------------------------------


@dataclass(slots=True)
class ProductionNodeModel:
    """
    Complete manufacturing order processed by the factory.

    This object is created by the Production Scheduler and
    remains the single source of truth throughout the
    manufacturing lifecycle.
    """

    location: ProductionLocation = field(default_factory=ProductionLocation)

    question_range: QuestionRange = field(default_factory=QuestionRange)

    execution: ExecutionInfo = field(default_factory=ExecutionInfo)

    quality: QualityInfo = field(default_factory=QualityInfo)

    metadata: NodeMetadata = field(default_factory=NodeMetadata)

    status: str = "PLANNED"

    current_stage: str = "SCHEDULED"

    manufactured_questions: int = 0

    approved_questions: int = 0

    rejected_questions: int = 0

    repair_cycles: int = 0
    # ---------------------------------------------------------
    # Production Node Operations
    # ---------------------------------------------------------

    def start(self) -> None:
        """
        Mark the production node as started.
        """

        self.status = "RUNNING"
        self.current_stage = "MANUFACTURING"

        self.execution.started_at = datetime.utcnow().isoformat()

    def complete(self) -> None:
        """
        Mark the production node as completed.
        """

        self.status = "COMPLETED"
        self.current_stage = "FINISHED"

        self.execution.completed_at = datetime.utcnow().isoformat()

    def fail(self) -> None:
        """
        Mark the production node as failed.
        """

        self.status = "FAILED"

    def request_repair(self) -> None:
        """
        Request an automatic repair cycle.
        """

        self.status = "REPAIR"

        self.current_stage = "REPAIR"

        self.repair_cycles += 1

    def approve_questions(
        self,
        approved_count: int,
    ) -> None:
        """
        Record approved question count.
        """

        self.approved_questions = approved_count

    def reject_questions(
        self,
        rejected_count: int,
    ) -> None:
        """
        Record rejected question count.
        """

        self.rejected_questions = rejected_count

    def manufactured(
        self,
        question_count: int,
    ) -> None:
        """
        Record manufactured question count.
        """

        self.manufactured_questions = question_count

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    @property
    def question_count(self) -> int:
        """
        Number of questions requested for this node.
        """

        return self.question_range.question_to - self.question_range.question_from + 1

    @property
    def production_node(self) -> str:
        """
        Human-readable production node identifier.
        """

        if self.metadata.production_node:
            return self.metadata.production_node

        return (
            f"{self.location.subject}_"
            f"{self.location.unit}_"
            f"{self.location.chapter}_"
            f"{self.location.subtopic}_"
            f"S{self.location.set_number}_"
            f"B{self.location.batch_number}"
        )

    @property
    def batch_id(self) -> str:
        """
        Batch identifier.
        """

        return self.metadata.batch_id

    @property
    def is_completed(self) -> bool:
        return self.status == "COMPLETED"

    @property
    def requires_repair(self) -> bool:
        return self.status == "REPAIR"

    @property
    def is_failed(self) -> bool:
        return self.status == "FAILED"

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the production node to a serializable dictionary.
        """

        return asdict(self)

    @classmethod
    def from_dict(
        cls,
        payload: Dict[str, Any],
    ) -> "ProductionNodeModel":
        """
        Construct a ProductionNodeModel from a dictionary.
        """

        return cls(
            location=ProductionLocation(**payload.get("location", {})),
            question_range=QuestionRange(**payload.get("question_range", {})),
            execution=ExecutionInfo(**payload.get("execution", {})),
            quality=QualityInfo(**payload.get("quality", {})),
            metadata=NodeMetadata(**payload.get("metadata", {})),
            status=payload.get(
                "status",
                "PLANNED",
            ),
            current_stage=payload.get(
                "current_stage",
                "SCHEDULED",
            ),
            manufactured_questions=payload.get(
                "manufactured_questions",
                0,
            ),
            approved_questions=payload.get(
                "approved_questions",
                0,
            ),
            rejected_questions=payload.get(
                "rejected_questions",
                0,
            ),
            repair_cycles=payload.get(
                "repair_cycles",
                0,
            ),
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(self) -> Dict[str, Any]:
        """
        Return a concise summary of the production node.
        """

        return {
            "node": self.production_node,
            "status": self.status,
            "stage": self.current_stage,
            "batch": self.batch_id,
            "questions": self.question_count,
            "approved": self.approved_questions,
            "rejected": self.rejected_questions,
            "repairs": self.repair_cycles,
        }

    def __repr__(self) -> str:
        return (
            f"ProductionNodeModel("
            f"node='{self.production_node}', "
            f"status='{self.status}', "
            f"stage='{self.current_stage}')"
        )
