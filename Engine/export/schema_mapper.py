"""
Question Factory OS v2.2

Schema Mapper

Converts production results into canonical CSV rows matching the
Supabase questions table schema.
"""

from __future__ import annotations

from typing import Any

from Engine.export.constants import SUPABASE_COLUMNS
from Engine.export.interfaces.mapper import Mapper
from Engine.export.models.csv_row import CSVRow
from Engine.models.batch_result_model import BatchResultModel
from Engine.models.worker_result_model import WorkerResultModel


class SchemaMapper(Mapper):
    """
    Maps production results into CSV rows.

    Responsibilities
    ----------------
    - Convert WorkerResult -> CSVRow
    - Convert BatchResult -> list[CSVRow]
    - Preserve canonical column ordering
    - Never perform validation
    - Never write CSV files
    """

    def __init__(self) -> None:
        self._columns: tuple[str, ...] = SUPABASE_COLUMNS

    @property
    def columns(self) -> tuple[str, ...]:
        """
        Canonical CSV column ordering.
        """
        return self._columns

    def map_worker(
        self,
        worker_result: WorkerResultModel,
    ) -> CSVRow:
        """
        Convert a WorkerResult into a CSVRow.
        """

        values = self._extract_worker_fields(worker_result)

        row = self._build_csv_row(values)

        return row

    def map_batch(
        self,
        batch_result: BatchResultModel,
    ) -> list[CSVRow]:
        """
        Convert an entire batch into CSV rows.
        """

        rows: list[CSVRow] = []

        for worker in self._iterate_workers(batch_result):
            rows.append(self.map_worker(worker))

        return rows

    #####################################################################
    # Extraction
    #####################################################################


    #####################################################################
    # CSV Construction
    #####################################################################


    #####################################################################
    # Batch Helpers
    #####################################################################

    

    #####################################################################
    # Normalization Helpers
    #####################################################################

    
    #####################################################################
    # Extraction
    #####################################################################

    def _extract_worker_fields(
        self,
        worker_result: WorkerResultModel,
    ) -> dict[str, Any]:
        """
        Extract exportable values from a WorkerResultModel.

        The AI pipeline stores the final validated question inside
        WorkerResultModel.question.

        This method extracts that payload while also preserving useful
        execution metadata for downstream export.
        """

        question = worker_result.question or {}

        values: dict[str, Any] = {}

        #
        # Copy all generated question fields.
        #
        # The SchemaMapper intentionally avoids hard-coding every
        # question attribute here. Whatever the validated pipeline
        # produced becomes available for CSV mapping.
        #
        values.update(question)

        #
        # Production metadata
        #
        values["_production_order"] = worker_result.production_order

        values["_provider"] = worker_result.provider

        values["_execution_time_ms"] = worker_result.execution_time_ms

        values["_retry_count"] = worker_result.retry_count

        values["_status"] = worker_result.status

        values["_error_message"] = worker_result.error_message

        #
        # Prompt / AI metadata
        #
        values["_prompt"] = worker_result.prompt

        values["_raw_response"] = worker_result.raw_response

        values["_parsed_response"] = worker_result.parsed_response

        values["_validation"] = worker_result.validation

        return values

    #####################################################################
    # Internal Helpers
    #####################################################################

    def _get(
        self,
        values: dict[str, Any],
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Safe dictionary lookup.
        """

        return values.get(key, default)

    def _get_str(
        self,
        values: dict[str, Any],
        key: str,
    ) -> str:
        """
        Return a normalized string value.
        """

        value = values.get(key)

        if value is None:
            return ""

        return str(value)

    def _get_bool(
        self,
        values: dict[str, Any],
        key: str,
    ) -> bool:
        """
        Return a boolean value.
        """

        return bool(values.get(key, False))

    def _get_int(
        self,
        values: dict[str, Any],
        key: str,
        default: int = 0,
    ) -> int:
        """
        Return an integer value.
        """

        value = values.get(key)

        if value is None:
            return default

        try:
            return int(value)
        except (TypeError, ValueError):
            return default
    #####################################################################
    # CSV Construction
    #####################################################################

    def _build_csv_row(
        self,
        values: dict[str, Any],
    ) -> CSVRow:
        """
        Build a CSVRow using the canonical Supabase schema.

        Every exported row contains every column defined in
        SUPABASE_COLUMNS.

        Missing values are populated using _default_value().
        """

        row = CSVRow()

        for column in self._columns:

            row[column] = self._map_column(
                column,
                values,
            )

        return row

    #####################################################################
    # Column Mapping
    #####################################################################

    def _map_column(
        self,
        column: str,
        values: dict[str, Any],
    ) -> Any:
        """
        Map a single CSV column.

        Unknown columns receive the configured default value.
        """

        #
        # Question identifiers
        #

        if column == "question_id":
            return self._get_str(values, "question_id")

        if column == "subject_code":
            return self._get_str(values, "subject_code")

        if column == "unit_code":
            return self._get_str(values, "unit_code")

        if column == "chapter_code":
            return self._get_str(values, "chapter_code")

        if column == "subtopic_code":
            return self._get_str(values, "subtopic_code")

        if column == "set_code":
            return self._get_str(values, "set_code")

        if column == "batch_code":
            return self._get_str(values, "batch_code")

        if column == "question_number":
            return self._get_int(values, "question_number")

        #
        # Question
        #

        if column == "question_type":
            return self._get_str(values, "question_type")

        if column == "difficulty":
            return self._get_str(values, "difficulty")

        if column == "question_text":
            return self._get_str(values, "question_text")

        #
        # Options
        #

        if column == "option_a":
            return self._get_str(values, "option_a")

        if column == "option_b":
            return self._get_str(values, "option_b")

        if column == "option_c":
            return self._get_str(values, "option_c")

        if column == "option_d":
            return self._get_str(values, "option_d")

        #
        # Answer
        #

        if column == "correct_answer":
            return self._get_str(values, "correct_answer")

        if column == "explanation":
            return self._get_str(values, "explanation")

        #
        # Metadata
        #

        if column == "pyq_inspired":
            return self._get_bool(values, "pyq_inspired")

        if column == "pyq_year":
            return self._get(values, "pyq_year")

        if column == "marks":
            return self._get_int(values, "marks")

        if column == "negative_marks":
            return self._get(values, "negative_marks")

        if column == "time_seconds":
            return self._get_int(values, "time_seconds")

        if column == "status":
            return self._get_str(values, "status")

        if column == "created_by":
            return self._get_str(values, "created_by")

        if column == "created_at":
            return self._get(values, "created_at")

        #
        # Unknown column
        #

        return self._default_value(column)
    #####################################################################
    # Batch Helpers
    #####################################################################

    def _iterate_workers(
        self,
        batch_result: BatchResultModel,
    ) -> list[WorkerResultModel]:
        """
        Return all worker results contained in the batch.

        The SchemaMapper does not decide whether a worker is valid.
        It simply returns the workers produced by the execution
        pipeline.
        """

        return batch_result.worker_results

    #####################################################################
    # Batch Mapping Helpers
    #####################################################################

    def batch_size(
        self,
        batch_result: BatchResultModel,
    ) -> int:
        """
        Return the total number of worker results.
        """

        return len(batch_result.worker_results)

    def successful_workers(
        self,
        batch_result: BatchResultModel,
    ) -> list[WorkerResultModel]:
        """
        Return workers that successfully generated a question.
        """

        return [
            worker
            for worker in batch_result.worker_results
            if worker.question is not None
        ]

    def failed_workers(
        self,
        batch_result: BatchResultModel,
    ) -> list[WorkerResultModel]:
        """
        Return workers that failed generation.
        """

        return [
            worker
            for worker in batch_result.worker_results
            if worker.question is None
        ]

    def map_batch_to_rows(
        self,
        batch_result: BatchResultModel,
    ) -> list[CSVRow]:
        """
        Convenience helper that converts every successful worker
        into a CSV row.
        """

        rows: list[CSVRow] = []

        for worker in self.successful_workers(batch_result):
            rows.append(
                self.map_worker(worker)
            )

        return rows

    def map_batch_to_dicts(
        self,
        batch_result: BatchResultModel,
    ) -> list[dict[str, Any]]:
        """
        Convert the successful workers into dictionaries.

        Useful for diagnostics and unit tests.
        """

        dictionaries: list[dict[str, Any]] = []

        for worker in self.successful_workers(batch_result):

            dictionaries.append(
                self._extract_worker_fields(worker)
            )

        return dictionaries
    #####################################################################
    # Normalization Helpers
    #####################################################################

    def _normalize_value(
        self,
        value: Any,
    ) -> Any:
        """
        Normalize a value before writing it to the CSV row.

        This method intentionally performs only lightweight
        normalization. It does not validate business rules.
        """

        if value is None:
            return ""

        #
        # Preserve primitive CSV-friendly types.
        #
        if isinstance(value, (str, int, float, bool)):
            return value

        #
        # Convert collections into a readable string.
        #
        if isinstance(value, (list, tuple, set)):
            return ", ".join(
                str(item)
                for item in value
            )

        #
        # Dictionaries are represented as strings.
        #
        if isinstance(value, dict):
            return str(value)

        return str(value)

    def _default_value(
        self,
        column: str,
    ) -> Any:
        """
        Return the default value for a missing column.
        """

        numeric_defaults = {
            "question_number",
            "marks",
            "negative_marks",
            "time_seconds",
        }

        boolean_defaults = {
            "pyq_inspired",
        }

        if column in numeric_defaults:
            return 0

        if column in boolean_defaults:
            return False

        return ""

    #####################################################################
    # Utility Helpers
    #####################################################################

    def has_column(
        self,
        column: str,
    ) -> bool:
        """
        Return True if the column exists in the canonical schema.
        """

        return column in self._columns

    def column_count(self) -> int:
        """
        Return the number of exported columns.
        """

        return len(self._columns)

    def empty_row(self) -> CSVRow:
        """
        Create an empty CSV row populated with default values.
        """

        row = CSVRow()

        for column in self._columns:
            row[column] = self._default_value(column)

        return row

    def schema(self) -> tuple[str, ...]:
        """
        Return the canonical CSV schema.
        """

        return self._columns

    def normalize_values(
        self,
        values: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Normalize an extracted value dictionary.

        Unknown keys are preserved to allow future schema
        extensions without changing the extraction logic.
        """

        normalized: dict[str, Any] = {}

        for key, value in values.items():
            normalized[key] = self._normalize_value(value)

        return normalized
