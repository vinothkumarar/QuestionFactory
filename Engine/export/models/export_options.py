"""
Question Factory OS v2.2

Export Options
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ExportOptions:
    """
    Configuration used during CSV export.
    """

    output_path: Path

    overwrite: bool = False

    include_header: bool = True

    validate_before_write: bool = True

    include_statistics: bool = True

    encoding: str = "utf-8"

    newline: str = ""