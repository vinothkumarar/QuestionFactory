"""
Question Factory OS v2.2

Export Result
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from Engine.export.models.export_summary import ExportSummary


@dataclass(slots=True)
class ExportResult:
    """
    Final result returned by the CSV Export Engine.
    """

    output_file: Path

    summary: ExportSummary

    statistics: dict[str, object]

    def succeeded(self) -> bool:
        """
        True if export completed successfully.
        """
        return self.summary.success