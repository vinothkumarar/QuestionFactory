"""
Question Factory OS
Pipeline Context Model

Version : 2.3.7.1
"""

from dataclasses import dataclass

from Engine.models.production_order_model import (
    ProductionOrderModel,
)


@dataclass
class PipelineContextModel:

    # -------------------------------------------------
    # Planning
    # -------------------------------------------------

    production_order: ProductionOrderModel

    # -------------------------------------------------
    # Question Objects
    # -------------------------------------------------

    question: dict | None = None

    prompt: str | None = None

    raw_response: str | None = None

    parsed_response: dict | None = None

    validation: dict | None = None

    # -------------------------------------------------
    # Runtime
    # -------------------------------------------------

    provider: str | None = None

    execution_time_ms: int = 0

    retry_count: int = 0

    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    status: str | None = None

    error_message: str | None = None
