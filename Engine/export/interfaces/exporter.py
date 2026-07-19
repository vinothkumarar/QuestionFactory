"""
Question Factory OS v2.2

Exporter Interface
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path

from Engine.export.models.export_options import ExportOptions
from Engine.export.models.export_result import ExportResult
from Engine.models.batch_result_model import BatchResultModel
from Engine.models.worker_result_model import WorkerResultModel


class Exporter(ABC):
    """
    Contract for CSV export engines.
    """

    @abstractmethod
    def export_worker(
        self,
        worker_result: WorkerResultModel,
        output_file: Path,
        options: ExportOptions | None = None,
    ) -> ExportResult:
        """
        Export a single WorkerResultModel.
        """
        raise NotImplementedError

    @abstractmethod
    def export_batch(
        self,
        batch_result: BatchResultModel,
        output_file: Path,
        options: ExportOptions | None = None,
    ) -> ExportResult:
        """
        Export an entire BatchResultModel.
        """
        raise NotImplementedError