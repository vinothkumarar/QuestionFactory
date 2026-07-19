"""
Question Factory OS v2.2

Validator Interface
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from Engine.export.models.csv_row import CSVRow
from Engine.export.models.export_summary import ExportSummary


class Validator(ABC):
    """
    Validates CSV rows before export.
    """

    @abstractmethod
    def validate_row(
        self,
        row: CSVRow,
    ) -> list[str]:
        """
        Validate a single row.

        Returns
        -------
        list[str]
            Validation errors.
        """
        raise NotImplementedError

    @abstractmethod
    def validate(
        self,
        rows: list[CSVRow],
    ) -> ExportSummary:
        """
        Validate the complete export.
        """
        raise NotImplementedError