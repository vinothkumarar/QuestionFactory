"""
Question Factory OS v2.2

Mapper Interface
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from Engine.export.models.csv_row import CSVRow
from Engine.models.batch_result_model import BatchResultModel
from Engine.models.worker_result_model import WorkerResultModel


class Mapper(ABC):
    """
    Maps production results into CSV rows.
    """

    @abstractmethod
    def map_worker(
        self,
        worker_result: WorkerResultModel,
    ) -> CSVRow:
        """
        Convert a WorkerResult into a CSV row.
        """
        raise NotImplementedError

    @abstractmethod
    def map_batch(
        self,
        batch_result: BatchResultModel,
    ) -> list[CSVRow]:
        """
        Convert an entire BatchResult into CSV rows.
        """
        raise NotImplementedError