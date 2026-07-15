"""
Question Factory OS
CSV Validation Result Model

Milestone : M7
Sprint    : S3
Release   : R1
"""

from dataclasses import dataclass
from dataclasses import field


@dataclass
class CSVValidationResultModel:

    total_rows: int = 0

    passed: bool = True

    total_errors: int = 0

    errors: list[str] = field(default_factory=list)
