"""
Question Factory OS v3.0

Validation Context

Shared immutable context passed to every
quality validator.
"""

from __future__ import annotations

from dataclasses import dataclass

from Engine.blueprint.blueprint_model import (
    BlueprintModel,
)

from Engine.models.production_node_model import (
    ProductionNodeModel,
)

from Engine.models.question_batch_model import (
    QuestionBatchModel,
)


@dataclass(frozen=True, slots=True)
class ValidationContext:
    """
    Shared context supplied to every validator.

    This avoids repeatedly passing the same
    arguments throughout the validation pipeline.
    """

    batch: QuestionBatchModel

    blueprint: BlueprintModel

    production_node: ProductionNodeModel


__all__ = [
    "ValidationContext",
]