"""
Question Factory OS
Worker Result Model
"""

from dataclasses import dataclass
from typing import Optional
from Engine.constants.generation_status import (
    GenerationStatus,
)


@dataclass
class WorkerResultModel:

    production_order: object

    question: Optional[dict] = None

    prompt: Optional[str] = None

    raw_response: Optional[str] = None

    parsed_response: Optional[dict] = None

    validation: Optional[dict] = None

    provider: str | None = None

    execution_time_ms: int = 0

    retry_count: int = 0

    status: str = GenerationStatus.SUCCESS

    error_message: Optional[str] = None
