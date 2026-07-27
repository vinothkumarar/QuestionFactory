"""
Question Factory OS v2.3

Validation Context

Provides all information required by validators.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ValidationContext:
    """
    Shared validation context.

    Every validator receives the same context object.
    """

    question: dict[str, Any]

    blueprint: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    runtime: Any | None = None

    ai_job: Any | None = None

    production_node: Any | None = None

    configuration: dict[str, Any] = field(default_factory=dict)