"""
Question Factory OS v2.0

Response Parser

Responsible for converting raw AI responses into
structured question objects.

The parser performs response parsing only.
Question validation and repair are handled by
downstream manufacturing stages.
"""

from __future__ import annotations

import json
import logging
from typing import Dict, List


class ResponseParser:
    """
    Parses AI responses into structured questions.
    """

    def __init__(self):

        self.logger = logging.getLogger(self.__class__.__name__)

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def parse(
        self,
        response: str,
    ) -> List[Dict]:
        """
        Parse an AI response.

        Parameters
        ----------
        response
            Raw response returned by the AI provider.

        Returns
        -------
        List[Dict]
            Parsed question objects.
        """

        self.logger.info("Parsing AI response.")

        cleaned_response = self._clean_response(response)

        questions = self._parse_json(cleaned_response)

        self.logger.info(
            "Parsed %d question(s).",
            len(questions),
        )

        return questions
        # ---------------------------------------------------------

    # Response Cleaning
    # ---------------------------------------------------------

    def _clean_response(
        self,
        response: str,
    ) -> str:
        """
        Clean the raw AI response.

        Removes common markdown wrappers and
        leading/trailing whitespace.
        """

        cleaned = response.strip()

        #
        # Remove fenced markdown blocks if present.
        #

        if cleaned.startswith("```json"):

            cleaned = cleaned[len("```json") :]

        elif cleaned.startswith("```"):

            cleaned = cleaned[len("```") :]

        if cleaned.endswith("```"):

            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        self.logger.info("AI response cleaned.")

        return cleaned

    # ---------------------------------------------------------
    # JSON Parsing
    # ---------------------------------------------------------

    def _parse_json(
        self,
        response: str,
    ) -> List[Dict]:
        """
        Parse the cleaned response as JSON.

        Returns
        -------
        List[Dict]
            Parsed question collection.
        """

        try:

            parsed = json.loads(response)

        except json.JSONDecodeError as ex:

            raise ValueError("Invalid JSON returned by AI.") from ex

        if isinstance(
            parsed,
            dict,
        ):

            #
            # Allow both:
            #
            # {
            #     "questions": [...]
            # }
            #
            # and
            #
            # {
            #     ...
            # }
            #

            if "questions" in parsed:

                parsed = parsed["questions"]

            else:

                parsed = [parsed]

        if not isinstance(
            parsed,
            list,
        ):

            raise ValueError("Expected a JSON array of questions.")

        self.logger.info("JSON successfully parsed.")

        return parsed

    # ---------------------------------------------------------
    # Basic Validation
    # ---------------------------------------------------------

    def validate_questions(
        self,
        questions: List[Dict],
    ) -> None:
        """
        Perform basic structural validation.

        This verifies only response structure.
        Question quality validation is performed
        by downstream validators.
        """

        if not questions:

            raise ValueError("No questions were parsed.")

        for index, question in enumerate(
            questions,
            start=1,
        ):

            if not isinstance(
                question,
                dict,
            ):

                raise ValueError("Question " f"{index} " "is not a JSON object.")

        self.logger.info("Basic response validation completed.")
        # ---------------------------------------------------------

    # Lifecycle Hooks
    # ---------------------------------------------------------

    def before_parse(
        self,
        response: str,
    ) -> None:
        """
        Executed immediately before parsing begins.

        Override in derived implementations for
        telemetry, auditing or preprocessing.
        """

        return

    def after_parse(
        self,
        response: str,
        questions: List[Dict],
    ) -> None:
        """
        Executed immediately after parsing completes.

        Override for reporting, metrics or custom
        integrations.
        """

        return

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
        response: str,
        questions: List[Dict],
    ) -> Dict:
        """
        Return parsing statistics.
        """

        return {
            "response_characters": len(response),
            "response_lines": len(response.splitlines()),
            "parsed_questions": len(questions),
        }

    def summary(
        self,
        response: str,
        questions: List[Dict],
    ) -> Dict:
        """
        Return a concise parsing summary.
        """

        stats = self.statistics(
            response,
            questions,
        )

        return {
            "parsed_questions": (stats["parsed_questions"]),
            "response_lines": (stats["response_lines"]),
        }

    def diagnostics(
        self,
        response: str,
        questions: List[Dict],
    ) -> Dict:
        """
        Return detailed parser diagnostics.
        """

        return {
            "component": self.__class__.__name__,
            "summary": self.summary(
                response,
                questions,
            ),
            "statistics": self.statistics(
                response,
                questions,
            ),
        }

    # ---------------------------------------------------------
    # Convenience API
    # ---------------------------------------------------------

    def execute(
        self,
        response: str,
    ) -> List[Dict]:
        """
        Convenience wrapper that performs the
        complete parsing workflow.
        """

        self.before_parse(response)

        questions = self.parse(response)

        self.validate_questions(questions)

        self.after_parse(
            response,
            questions,
        )

        return questions
        # ---------------------------------------------------------

    # Component Information
    # ---------------------------------------------------------

    @property
    def version(self) -> str:
        """
        Response Parser version.
        """

        return "2.0.0"

    @property
    def component_name(self) -> str:
        """
        Component name.
        """

        return "Response Parser"

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(self) -> Dict:
        """
        Return parser health information.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "supported_format": "JSON",
            "status": "READY",
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(self) -> Dict:
        """
        Describe parser capabilities.
        """

        return {
            "markdown_cleanup": True,
            "json_parsing": True,
            "basic_validation": True,
            "provider_independent": True,
            "diagnostics": True,
            "statistics": True,
            "lifecycle_hooks": True,
        }

    # ---------------------------------------------------------
    # Supported Formats
    # ---------------------------------------------------------

    def supported_formats(
        self,
    ) -> List[str]:
        """
        Return supported response formats.
        """

        return [
            "JSON",
        ]

    def is_supported_format(
        self,
        response_format: str,
    ) -> bool:
        """
        Determine whether a response format is supported.
        """

        return response_format.upper() in self.supported_formats()

    # ---------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------

    def create_empty_result(
        self,
    ) -> List[Dict]:
        """
        Return an empty parsing result.

        Useful for testing and fallback scenarios.
        """

        return []

    def normalize_response(
        self,
        response: str,
    ) -> str:
        """
        Normalize a response prior to parsing.

        Currently delegates to the internal response
        cleaning routine.
        """

        return self._clean_response(response)
        # ---------------------------------------------------------

    # Parser Information
    # ---------------------------------------------------------

    def parser_information(self) -> Dict:
        """
        Return parser information.
        """

        return {
            "name": self.component_name,
            "version": self.version,
            "supported_formats": (self.supported_formats()),
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return "ResponseParser(" f"version='{self.version}')"

    def __str__(self) -> str:
        return f"{self.component_name} " f"[v{self.version}]"
