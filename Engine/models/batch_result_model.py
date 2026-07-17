"""
Question Factory OS
Batch Result Model

Milestone : M6
Sprint    : S2
Release   : R1
"""

from dataclasses import dataclass
from dataclasses import field

from .worker_result_model import WorkerResultModel


@dataclass
class BatchResultModel:
    """
    Represents the outcome of an entire
    batch execution.
    """

    total_orders: int = 0
    successful: int = 0
    failed: int = 0

    execution_time_ms: int = 0

    worker_results: list[WorkerResultModel] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        if self.total_orders == 0:
            return 0.0

        return round((self.successful / self.total_orders) * 100, 2)
        