"""
Question Factory OS v2.1

Generated Question Builder

Builds a GeneratedQuestionModel from a normalized
AI question dictionary.

Responsibilities
----------------
• Deterministic field mapping
• Structural normalization
• Metadata preservation
• No validation
• No repair
"""

from __future__ import annotations

import logging

from typing import Any

from Engine.models.generated_question_model import (
    GeneratedQuestionModel,
)

LOGGER = logging.getLogger(__name__)


class GeneratedQuestionBuilder:
    """
    Converts a normalized question dictionary into
    a GeneratedQuestionModel.

    This component performs only structural mapping.
    Validation and repair belong to their respective
    subsystems.
    """

    VERSION = "2.1.0"

    COMPONENT_NAME = "Generated Question Builder"

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def __init__(
        self,
    ) -> None:

        self._logger = LOGGER

        self._logger.info(
            "%s initialized.",
            self.COMPONENT_NAME,
        )

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def build(
        self,
        data: dict[str, Any],
    ) -> GeneratedQuestionModel:
        """
        Build a GeneratedQuestionModel from a
        normalized dictionary.
        """

        if data is None:
            raise ValueError(
                "Question data cannot be None."
            )

        if not isinstance(
            data,
            dict,
        ):
            raise TypeError(
                "Question data must be a dictionary."
            )

        question = GeneratedQuestionModel()

        self._populate_identity(
            question,
            data,
        )

        self._populate_question(
            question,
            data,
        )

        self._populate_options(
            question,
            data,
        )

        self._populate_answer(
            question,
            data,
        )

        self._populate_explanation(
            question,
            data,
        )

        self._populate_metadata(
            question,
            data,
        )

        return question

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    def _populate_identity(
        self,
        question: GeneratedQuestionModel,
        data: dict[str, Any],
    ) -> None:

        question.question_code = str(
            data.get(
                "question_code",
                "",
            )
        ).strip()

        question.unit_code = str(
            data.get(
                "unit_code",
                "",
            )
        ).strip()

        question.chapter_code = str(
            data.get(
                "chapter_code",
                "",
            )
        ).strip()

        question.subtopic_code = str(
            data.get(
                "subtopic_code",
                "",
            )
        ).strip()

        question.set_number = int(
            data.get(
                "set_number",
                1,
            )
        )

        question.batch_number = int(
            data.get(
                "batch_number",
                1,
            )
        )
    # ---------------------------------------------------------
    # Question
    # ---------------------------------------------------------

    def _populate_question(
        self,
        question: GeneratedQuestionModel,
        data: dict[str, Any],
    ) -> None:
        """
        Populate question content.
        """

        question.question_text = str(
            data.get(
                "question_text",
                "",
            )
        ).strip()

    # ---------------------------------------------------------
    # Options
    # ---------------------------------------------------------

    def _populate_options(
        self,
        question: GeneratedQuestionModel,
        data: dict[str, Any],
    ) -> None:
        """
        Populate MCQ options.

        Supports:

        {
            "options": [...]
        }

        and

        {
            "option_a": "...",
            "option_b": "...",
            "option_c": "...",
            "option_d": "..."
        }
        """

        options = data.get(
            "options",
        )

        #
        # Preferred format
        #

        if isinstance(
            options,
            list,
        ):

            question.options = [
                str(item).strip()
                for item in options
            ]

            return

        #
        # Legacy format
        #

        question.options = [
            str(
                data.get(
                    "option_a",
                    "",
                )
            ).strip(),
            str(
                data.get(
                    "option_b",
                    "",
                )
            ).strip(),
            str(
                data.get(
                    "option_c",
                    "",
                )
            ).strip(),
            str(
                data.get(
                    "option_d",
                    "",
                )
            ).strip(),
        ]
    # ---------------------------------------------------------
    # Answer
    # ---------------------------------------------------------

    def _populate_answer(
        self,
        question: GeneratedQuestionModel,
        data: dict[str, Any],
    ) -> None:
        """
        Populate the correct option text.

        Supports:

        • correct_option
        • correct_answer
        • answer
        """

        answer = data.get(
            "correct_option",
        )

        if answer is None:

            answer = data.get(
                "correct_answer",
            )

        if answer is None:

            answer = data.get(
                "answer",
                "",
            )

        #
        # Integer index support
        #

        if isinstance(
            answer,
            int,
        ):

            if (
                0 <= answer
                < len(question.options)
            ):

                question.correct_option = (
                    question.options[
                        answer
                    ]
                )

                return

            question.correct_option = ""

            return

        answer = str(
            answer,
        ).strip()

        #
        # Letter support
        #

        option_index = {
            "A": 0,
            "B": 1,
            "C": 2,
            "D": 3,
        }

        upper = answer.upper()

        if upper in option_index:

            index = option_index[
                upper
            ]

            if (
                index
                < len(question.options)
            ):

                question.correct_option = (
                    question.options[
                        index
                    ]
                )

                return

        #
        # Already supplied as option text
        #

        question.correct_option = answer

    # ---------------------------------------------------------
    # Explanation
    # ---------------------------------------------------------

    def _populate_explanation(
        self,
        question: GeneratedQuestionModel,
        data: dict[str, Any],
    ) -> None:
        """
        Populate explanation.
        """

        question.explanation = str(
            data.get(
                "explanation",
                data.get(
                    "solution",
                    "",
                ),
            )
        ).strip()
    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def _populate_metadata(
        self,
        question: GeneratedQuestionModel,
        data: dict[str, Any],
    ) -> None:
        """
        Populate academic metadata.
        """

        question.difficulty = str(
            data.get(
                "difficulty",
                "",
            )
        ).strip()

        question.archetype = str(
            data.get(
                "archetype",
                "",
            )
        ).strip()

        question.concept = str(
            data.get(
                "concept",
                "",
            )
        ).strip()

        tags = data.get(
            "tags",
            [],
        )

        if isinstance(
            tags,
            list,
        ):
            question.tags.extend(
                str(tag).strip()
                for tag in tags
                if str(tag).strip()
            )

        metadata = data.get(
            "metadata",
            {},
        )

        if isinstance(
            metadata,
            dict,
        ):
            question.metadata.update(
                metadata,
            )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return builder diagnostics.
        """

        return {
            "component": self.COMPONENT_NAME,
            "version": self.VERSION,
            "supports_option_list": True,
            "supports_legacy_options": True,
            "supports_metadata": True,
            "supports_tags": True,
            "mapping_mode": "STRUCTURAL",
        }

    def configuration(
        self,
    ) -> dict[str, Any]:
        """
        Return current builder configuration.
        """

        return {
            "component": self.COMPONENT_NAME,
            "version": self.VERSION,
            "validation": "EXTERNAL",
            "repair": "EXTERNAL",
        }

    def health(
        self,
    ) -> dict[str, Any]:
        """
        Return health information.
        """

        return {
            "component": self.COMPONENT_NAME,
            "version": self.VERSION,
            "status": "READY",
        }
    def capabilities(
        self,
    ) -> dict[str, bool]:
        """
        Return supported capabilities.
        """

        return {
            "build_question": True,
            "identity_mapping": True,
            "question_mapping": True,
            "option_mapping": True,
            "answer_mapping": True,
            "metadata_mapping": True,
            "tag_mapping": True,
            "legacy_option_support": True,
            "structural_mapping_only": True,
        }

    # ---------------------------------------------------------
    # Component Information
    # ---------------------------------------------------------

    @property
    def version(
        self,
    ) -> str:
        """
        Builder version.
        """

        return self.VERSION

    @property
    def component_name(
        self,
    ) -> str:
        """
        Human-readable component name.
        """

        return self.COMPONENT_NAME

    # ---------------------------------------------------------
    # Runtime Summary
    # ---------------------------------------------------------

    def runtime_summary(
        self,
    ) -> dict[str, Any]:
        """
        Return a concise runtime summary.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "status": "READY",
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.COMPONENT_NAME}"
            f"(version='{self.VERSION}')"
        )

    def __str__(
        self,
    ) -> str:

        return (
            f"{self.COMPONENT_NAME} "
            f"v{self.VERSION}"
        )

