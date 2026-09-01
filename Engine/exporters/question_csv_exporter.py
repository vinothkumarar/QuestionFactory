"""
Question Factory OS v2.2

Question CSV Exporter

Exports a QuestionBatchModel into the canonical
Question Factory CSV format.
"""

from __future__ import annotations

import csv
from pathlib import Path

from Engine.models.production_order_model import (
    ProductionOrderModel,
)

from Engine.models.question_batch_model import (
    QuestionBatchModel,
)

from Engine.schema.question_schema import (
    EXPORT_COLUMNS,
)


class QuestionCSVExporter:
    """
    Export QuestionBatchModel instances to CSV.
    """

    VERSION = "2.2.0"

    def export(
        self,
        batch: QuestionBatchModel,
        production_order: ProductionOrderModel,
    ) -> str:
        """
        Export one production batch.

        Returns
        -------
        str
            Generated CSV file path.
        """

        if not batch.has_questions:
            raise ValueError(
                "Question batch contains no questions."
            )

        output_folder = self._build_output_folder(
            production_order,
        )

        output_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_file = (
            output_folder
            / self._build_filename(
                production_order,
            )
        )

        self._write_rows(
            output_file=output_file,
            batch=batch,
        )

        return str(output_file)

    # ---------------------------------------------------------
    # Folder Helpers
    # ---------------------------------------------------------

    def _build_output_folder(
        self,
        production_order: ProductionOrderModel,
    ) -> Path:
        """
        Build production output folder.
        """

        return (
            Path("output")
            / production_order.unit
            / production_order.chapter
            / production_order.subtopic
        )

    # ---------------------------------------------------------
    # File Helpers
    # ---------------------------------------------------------

    def _build_filename(
        self,
        production_order: ProductionOrderModel,
    ) -> str:
        """
        Build the canonical production CSV filename.

        One CSV represents one subtopic/set.
        """

        return (
            f"{production_order.unit}_"
            f"{production_order.chapter}_"
            f"{production_order.subtopic}_"
            f"{production_order.set_no}.csv"
        )

    # ---------------------------------------------------------
    # CSV Writing
    # ---------------------------------------------------------

    def _write_rows(
        self,
        *,
        output_file: Path,
        batch: QuestionBatchModel,
    ) -> None:
        """
        Write QuestionBatchModel contents to CSV.
        """

        file_exists = output_file.exists()

        with output_file.open(
            mode="a",
            newline="",
            encoding="utf-8",
        ) as csv_file:

            writer = csv.DictWriter(
                csv_file,
                fieldnames=EXPORT_COLUMNS,
                extrasaction="ignore",
            )

            if not file_exists:
                writer.writeheader()

            for question in batch.questions:

                export_data = question.to_export_dict()

                export_row = {
                    column: export_data.get(column, "")
                    for column in EXPORT_COLUMNS
                }

                writer.writerow(
                    export_row,
                )
    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def component_name(
        self,
    ) -> str:
        """
        Component name.
        """

        return self.__class__.__name__

    @property
    def version(
        self,
    ) -> str:
        """
        Exporter version.
        """

        return self.VERSION

    def health(
        self,
    ) -> dict[str, object]:
        """
        Exporter health.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "status": "READY",
        }

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Exporter diagnostics.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "export_columns": len(EXPORT_COLUMNS),
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.component_name}"
            f"(version='{self.version}')"
        )

    def __str__(
        self,
    ) -> str:

        return (
            f"{self.component_name} "
            f"[v{self.version}]"
        )


__all__ = [
    "QuestionCSVExporter",
]
