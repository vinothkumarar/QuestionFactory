"""
Question Factory OS v2.1
------------------------

AI Response Parser

Responsibilities
----------------
• Parse normalized AI responses
• Extract structured content
• Parse JSON payloads
• Validate schemas
• Normalize fields
• Produce strongly typed parsed responses

The parser is completely provider-agnostic and operates only on
AIResponse objects.

Author:
Question Factory OS
"""

from __future__ import annotations

import json
import logging

from dataclasses import dataclass
from dataclasses import field

from enum import Enum

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from factory.ai.ai_client import AIResponse

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Parse Status
# ----------------------------------------------------------------------


class ParseStatus(str, Enum):
    """
    Result of parsing.
    """

    SUCCESS = "success"

    PARTIAL = "partial"

    FAILED = "failed"


# ----------------------------------------------------------------------
# Parsed Field
# ----------------------------------------------------------------------


@dataclass(slots=True)
class ParsedField:
    """
    Represents one extracted field.
    """

    name: str

    value: Any

    valid: bool = True

    message: Optional[str] = None


# ----------------------------------------------------------------------
# Parsed Response
# ----------------------------------------------------------------------


@dataclass(slots=True)
class ParsedResponse:
    """
    Result produced by ResponseParser.
    """

    success: bool

    status: ParseStatus

    fields: Dict[str, ParsedField] = field(default_factory=dict)

    raw_json: Optional[Dict[str, Any]] = None

    raw_text: Optional[str] = None

    warnings: List[str] = field(default_factory=list)

    errors: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)


# ----------------------------------------------------------------------
# Response Parser
# ----------------------------------------------------------------------


class ResponseParser:
    """
    Enterprise response parser.

    Converts provider-independent AIResponse objects into
    structured ParsedResponse objects suitable for the
    manufacturing pipeline.
    """

    def __init__(self) -> None:

        logger.info("ResponseParser initialized.")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def parse(
        self,
        response: AIResponse,
    ) -> ParsedResponse:
        """
        Parse a normalized AI response.

        This is the primary entry point used by the AIEngine.
        """

        if response is None:
            raise ValueError("response cannot be None.")

        if not response.success:
            return ParsedResponse(
                success=False,
                status=ParseStatus.FAILED,
                raw_text=response.content,
                errors=["AI response indicates unsuccessful execution."],
            )

        cleaned_text = self._preprocess(response.content)

        try:

            payload = self._extract_json(cleaned_text)

            parsed = ParsedResponse(
                success=True,
                status=ParseStatus.SUCCESS,
                raw_json=payload,
                raw_text=cleaned_text,
            )

            self._populate_fields(
                parsed,
                payload,
            )
            self._build_metadata(
                response,
                parsed,
            )

            return parsed

        except Exception as ex:

            logger.exception("Response parsing failed.")

            return ParsedResponse(
                success=False,
                status=ParseStatus.FAILED,
                raw_text=cleaned_text,
                errors=[str(ex)],
            )

    # ------------------------------------------------------------------
    # Preprocessing
    # ------------------------------------------------------------------

    def _preprocess(
        self,
        text: str,
    ) -> str:
        """
        Normalize raw AI output before parsing.
        """

        if text is None:
            return ""

        text = text.strip()

        text = self._strip_markdown_fences(text)

        return text

    # ------------------------------------------------------------------
    # JSON Extraction
    # ------------------------------------------------------------------

    def _extract_json(
        self,
        text: str,
    ) -> Dict[str, Any]:
        """
        Extract a JSON object from the response.

        Supports:

        • Pure JSON
        • ```json fenced blocks
        • Leading/trailing whitespace
        """

        if not text:
            raise ValueError("Response is empty.")

        try:
            return json.loads(text)

        except json.JSONDecodeError:
            pass

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("No JSON object found.")

        candidate = text[start : end + 1]

        return json.loads(candidate)

    # ------------------------------------------------------------------
    # Field Population
    # ------------------------------------------------------------------

    def _populate_fields(
        self,
        parsed: ParsedResponse,
        payload: Dict[str, Any],
    ) -> None:
        """
        Populate ParsedField objects from JSON.
        """

        for name, value in payload.items():

            parsed.fields[name] = ParsedField(
                name=name,
                value=value,
            )

    # ------------------------------------------------------------------
    # Markdown Helpers
    # ------------------------------------------------------------------

    def _strip_markdown_fences(
        self,
        text: str,
    ) -> str:
        """
        Remove Markdown code fences.

        Handles:

        ```json
        ...
        ```

        and

        ```
        ...
        ```
        """

        if text.startswith("```"):

            lines = text.splitlines()

            if lines:
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            text = "\n".join(lines)

        return text.strip()

    # ------------------------------------------------------------------
    # Repair Pipeline
    # ------------------------------------------------------------------

    def _repair_json(
        self,
        text: str,
    ) -> str:
        """
        Attempt lightweight repairs on malformed JSON.

        This method intentionally performs only safe,
        deterministic repairs. It never invents data.
        """

        repaired = text.strip()

        repaired = repaired.replace("\r\n", "\n")

        repaired = repaired.replace("\r", "\n")

        repaired = repaired.replace("\t", " ")

        repaired = self._remove_trailing_commas(repaired)

        repaired = self._normalize_quotes(repaired)

        return repaired

    # ------------------------------------------------------------------
    # Trailing Comma Repair
    # ------------------------------------------------------------------

    def _remove_trailing_commas(
        self,
        text: str,
    ) -> str:
        """
        Remove trailing commas before closing braces.

        Example

        {
            "a":1,
        }

        becomes

        {
            "a":1
        }
        """

        while ",}" in text:
            text = text.replace(",}", "}")

        while ",]" in text:
            text = text.replace(",]", "]")

        return text

    # ------------------------------------------------------------------
    # Quote Normalization
    # ------------------------------------------------------------------

    def _normalize_quotes(
        self,
        text: str,
    ) -> str:
        """
        Replace smart quotes with standard quotes.
        """

        replacements = {
            "“": '"',
            "”": '"',
            "‘": "'",
            "’": "'",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    # ------------------------------------------------------------------
    # Safe JSON Parsing
    # ------------------------------------------------------------------

    def _safe_json_loads(
        self,
        text: str,
    ) -> Dict[str, Any]:
        """
        Parse JSON with automatic repair.

        Repair is attempted only after the initial parse
        fails.
        """

        try:
            return json.loads(text)

        except json.JSONDecodeError:

            repaired = self._repair_json(text)

            return json.loads(repaired)

    # ------------------------------------------------------------------
    # Validation Helpers
    # ------------------------------------------------------------------

    def has_errors(
        self,
        parsed: ParsedResponse,
    ) -> bool:
        """
        Return True if parsing produced errors.
        """

        return bool(parsed.errors)

    def has_warnings(
        self,
        parsed: ParsedResponse,
    ) -> bool:
        """
        Return True if parsing produced warnings.
        """

        return bool(parsed.warnings)

    def field(
        self,
        parsed: ParsedResponse,
        name: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve a parsed field value.

        Returns the supplied default when the field does
        not exist.
        """

        item = parsed.fields.get(name)

        if item is None:
            return default

        return item.value

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    def _build_metadata(
        self,
        response: AIResponse,
        parsed: ParsedResponse,
    ) -> None:
        """
        Attach provider-independent metadata.
        """

        parsed.metadata.update(
            {
                "provider": response.provider.value,
                "model": response.model,
                "prompt_tokens": response.prompt_tokens,
                "completion_tokens": response.completion_tokens,
                "total_tokens": response.total_tokens,
            }
        )

    # ------------------------------------------------------------------
    # Schema Validation
    # ------------------------------------------------------------------

    def validate_schema(
        self,
        parsed: ParsedResponse,
        required_fields: Optional[List[str]] = None,
    ) -> bool:
        """
        Validate that all required fields exist.

        This validation is intentionally generic and does not
        understand question-specific semantics.
        """

        if required_fields is None:
            return True

        valid = True

        for field_name in required_fields:

            if field_name not in parsed.fields:

                parsed.errors.append(f"Missing required field '{field_name}'.")

                valid = False

        if not valid:
            parsed.status = ParseStatus.PARTIAL

        return valid

    # ------------------------------------------------------------------
    # Type Validation
    # ------------------------------------------------------------------

    def validate_types(
        self,
        parsed: ParsedResponse,
        expected_types: Dict[str, type],
    ) -> bool:
        """
        Validate field data types.

        Example
        -------
        {
            "difficulty": int,
            "marks": float,
            "question": str,
        }
        """

        valid = True

        for field_name, expected_type in expected_types.items():

            item = parsed.fields.get(field_name)

            if item is None:
                continue

            if not isinstance(item.value, expected_type):

                item.valid = False

                item.message = f"Expected " f"{expected_type.__name__}"

                parsed.warnings.append(f"Field '{field_name}' " f"has unexpected type.")

                valid = False

        return valid

    # ------------------------------------------------------------------
    # Normalization
    # ------------------------------------------------------------------

    def normalize_fields(
        self,
        parsed: ParsedResponse,
    ) -> None:
        """
        Normalize parsed values.

        Only generic normalization is performed.
        """

        for item in parsed.fields.values():

            if isinstance(item.value, str):

                item.value = item.value.strip()

    # ------------------------------------------------------------------
    # Field Utilities
    # ------------------------------------------------------------------

    def contains(
        self,
        parsed: ParsedResponse,
        field_name: str,
    ) -> bool:
        """
        Return True if the specified field exists.
        """

        return field_name in parsed.fields

    def fields(
        self,
        parsed: ParsedResponse,
    ) -> List[str]:
        """
        Return all parsed field names.
        """

        return sorted(parsed.fields.keys())

    def values(
        self,
        parsed: ParsedResponse,
    ) -> Dict[str, Any]:
        """
        Return a simple dictionary containing field values.
        """

        return {name: field.value for name, field in parsed.fields.items()}

    # ------------------------------------------------------------------
    # Parse Statistics
    # ------------------------------------------------------------------

    def statistics(
        self,
        parsed: ParsedResponse,
    ) -> Dict[str, Any]:
        """
        Return parsing statistics.
        """

        valid_fields = sum(1 for field in parsed.fields.values() if field.valid)

        invalid_fields = len(parsed.fields) - valid_fields

        return {
            "status": parsed.status.value,
            "success": parsed.success,
            "field_count": len(parsed.fields),
            "valid_fields": valid_fields,
            "invalid_fields": invalid_fields,
            "warnings": len(parsed.warnings),
            "errors": len(parsed.errors),
        }

    # ------------------------------------------------------------------
    # Parse Report
    # ------------------------------------------------------------------

    def report(
        self,
        parsed: ParsedResponse,
    ) -> Dict[str, Any]:
        """
        Produce a comprehensive parse report.

        This report is suitable for logging, diagnostics,
        audit trails, and future manufacturing dashboards.
        """

        return {
            "success": parsed.success,
            "status": parsed.status.value,
            "statistics": self.statistics(parsed),
            "warnings": list(parsed.warnings),
            "errors": list(parsed.errors),
            "metadata": dict(parsed.metadata),
            "fields": {
                name: {
                    "valid": field.valid,
                    "message": field.message,
                }
                for name, field in parsed.fields.items()
            },
        }

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def diagnostics(
        self,
        parsed: ParsedResponse,
    ) -> Dict[str, Any]:
        """
        Return parser diagnostics.

        Intended for runtime monitoring and troubleshooting.
        """

        return {
            "parser": self.__class__.__name__,
            "status": parsed.status.value,
            "field_count": len(parsed.fields),
            "warning_count": len(parsed.warnings),
            "error_count": len(parsed.errors),
            "metadata_keys": sorted(parsed.metadata.keys()),
        }

    # ------------------------------------------------------------------
    # Export Helpers
    # ------------------------------------------------------------------

    def to_dict(
        self,
        parsed: ParsedResponse,
    ) -> Dict[str, Any]:
        """
        Export parsed values as a plain dictionary.

        Metadata, warnings, and errors are intentionally
        excluded to provide a clean data payload.
        """

        return {name: field.value for name, field in parsed.fields.items()}

    def to_json(
        self,
        parsed: ParsedResponse,
        *,
        indent: int = 2,
    ) -> str:
        """
        Serialize parsed values as formatted JSON.
        """

        return json.dumps(
            self.to_dict(parsed),
            indent=indent,
            ensure_ascii=False,
        )

    # ------------------------------------------------------------------
    # Convenience Helpers
    # ------------------------------------------------------------------

    def is_successful(
        self,
        parsed: ParsedResponse,
    ) -> bool:
        """
        Return True if parsing completed successfully
        without errors.
        """

        return parsed.success and not parsed.errors

    def is_partial(
        self,
        parsed: ParsedResponse,
    ) -> bool:
        """
        Return True if parsing completed with recoverable
        issues.
        """

        return parsed.status == ParseStatus.PARTIAL

    def is_failed(
        self,
        parsed: ParsedResponse,
    ) -> bool:
        """
        Return True if parsing failed.
        """

        return parsed.status == ParseStatus.FAILED

    # ------------------------------------------------------------------
    # Object Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """

        return f"{self.__class__.__name__}()"

    __str__ = __repr__


# ----------------------------------------------------------------------
# Factory Helper
# ----------------------------------------------------------------------


def create_response_parser() -> ResponseParser:
    """
    Create a production-ready ResponseParser.

    Centralizing construction provides a future extension point for:

    - Configuration loading
    - Dependency injection
    - Custom validators
    - Custom repair strategies
    - Plugin registration

    The default implementation returns a standard parser.
    """

    parser = ResponseParser()

    logger.info("Production ResponseParser created.")

    return parser


# ----------------------------------------------------------------------
# Module Exports
# ----------------------------------------------------------------------

__all__ = [
    "ParseStatus",
    "ParsedField",
    "ParsedResponse",
    "ResponseParser",
    "create_response_parser",
]
