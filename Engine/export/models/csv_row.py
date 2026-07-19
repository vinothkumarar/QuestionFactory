"""
Question Factory OS v2.2

CSV Row Model

Represents a single row that will be exported to the Supabase
questions table.

This model intentionally stores data as a dictionary so that
the SchemaMapper remains the single source of truth for the
database schema.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class CSVRow:
    """
    Represents a single CSV row.

    The keys must exactly match the Supabase questions
    table column names.
    """

    values: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """
        Return a shallow copy suitable for csv.DictWriter.
        """
        return dict(self.values)

    def __getitem__(self, key: str) -> Any:
        return self.values[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.values[key] = value

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        return self.values.get(key, default)

    @property
    def columns(self) -> list[str]:
        """
        Return ordered column names.
        """
        return list(self.values.keys())