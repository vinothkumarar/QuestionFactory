"""
Question Factory OS v2.2

CSV Export Engine

Facade for the CSV Export subsystem.
"""

from __future__ import annotations

import time
from pathlib import Path

from Engine.export.csv_writer import CSVWriter
from Engine.export.export_statistics import ExportStatistics
from Engine.export.export_validator import ExportValidator
from Engine.export.interfaces.exporter import Exporter
from Engine.export.models.export_options import ExportOptions
from Engine.export.models.export_result import ExportResult
from Engine.export.models.export_summary import ExportSummary
from Engine.export.schema_mapper import SchemaMapper
from Engine.models.batch_result_model import BatchResultModel
from Engine.models.worker_result_model import WorkerResultModel


class CSVExportEngine(Exporter):
    """
    CSV Export Engine.

    Orchestrates the complete export pipeline.

    WorkerResultModel
            │
            ▼
       SchemaMapper
            │
            ▼
      ExportValidator
            │
            ▼
         CSVWriter
            │
            ▼
     ExportStatistics
            │
            ▼
       ExportResult
    """

    def __init__(self) -> None:

        self._mapper = SchemaMapper()

        self._validator = ExportValidator()

        self._writer = CSVWriter()

        self._statistics = ExportStatistics()

    ####################################################################
    # Public API
    ####################################################################

    def export_worker(
        self,
        worker_result: WorkerResultModel,
        output_file: Path,
        options: ExportOptions | None = None,
    ) -> ExportResult:

        row = self._mapper.map_worker(worker_result)

        return self._export_rows(
            [row],
            output_file,
            options,
        )

    def export_batch(
        self,
        batch_result: BatchResultModel,
        output_file: Path,
        options: ExportOptions | None = None,
    ) -> ExportResult:

        rows = self._mapper.map_batch(batch_result)

        return self._export_rows(
            rows,
            output_file,
            options,
        )

    ####################################################################
    # Internal
    ####################################################################

    def _export_rows(
        self,
        rows,
        output_file: Path,
        options: ExportOptions | None,
    ) -> ExportResult:

        start = time.perf_counter()

        if options is None:

            options = ExportOptions(
                output_path=output_file,
            )

        else:

            options.output_path = output_file

        #
        # Validation
        #
        if options.validate_before_write:

            summary = self._validator.validate(rows)

        else:

            summary = ExportSummary()

            summary.total_rows = len(rows)
            summary.successful_rows = len(rows)

        #
        # Abort on validation errors
        #
        if not summary.success:

            summary.duration_seconds = (
                time.perf_counter() - start
            )

            return ExportResult(
                output_file=output_file,
                summary=summary,
                statistics={},
            )

        #
        # Write CSV
        #
        self._writer.write(
            rows,
            options,
        )

        #
        # Statistics
        #
        statistics = {}

        if options.include_statistics:

            statistics = self._statistics.generate(rows)

        summary.duration_seconds = (
            time.perf_counter() - start
        )

        return ExportResult(
            output_file=output_file,
            summary=summary,
            statistics=statistics,
        )