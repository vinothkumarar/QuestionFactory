"""
Question Factory OS v2.1

Batch Adapter

Converts AI ParsedResponse objects into
QuestionBatchModel instances.

The adapter is the bridge between the
AI subsystem and the manufacturing
subsystem.

Responsibilities
----------------
• Convert ParsedResponse to QuestionBatchModel
• Convert parsed question dictionaries to
  GeneratedQuestionModel objects
• Preserve metadata
• Perform structural mapping only

The adapter intentionally performs no
validation or repair.
"""

from __future__ import annotations

import logging
from typing import Any

from Engine.factory.ai.response_parser import ParsedResponse
from Engine.models.generated_question_model import (
    GeneratedQuestionModel,
)
from Engine.models.question_batch_model import (
    QuestionBatchModel,
)

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Batch Adapter
# ----------------------------------------------------------------------


class BatchAdapter:
    """
    Converts ParsedResponse objects into
    QuestionBatchModel instances.

    The adapter performs structural mapping
    only and contains no business rules.
    """

    def __init__(self) -> None:

        logger.info(
            "BatchAdapter initialized."
        )
    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(
        self,
        parsed: ParsedResponse,
    ) -> QuestionBatchModel:
        """
        Build a QuestionBatchModel from a
        ParsedResponse.

        Parameters
        ----------
        parsed:
            Parsed AI response.

        Returns
        -------
        QuestionBatchModel
        """

        if not parsed.success:

            raise ValueError(
                "Cannot build batch from "
                "unsuccessful ParsedResponse."
            )

        payload = self._payload(
            parsed,
        )

        batch = QuestionBatchModel()

        self._populate_batch(
            batch,
            payload,
        )

        self._populate_questions(
            batch,
            payload,
        )

        return batch
    # ------------------------------------------------------------------
    # Payload Extraction
    # ------------------------------------------------------------------

    def _payload(
        self,
        parsed: ParsedResponse,
    ) -> dict[str, Any]:
        """
        Return the parsed JSON payload.
        """

        if parsed.raw_json is None:

            raise ValueError(
                "ParsedResponse does not "
                "contain JSON."
            )

        return parsed.raw_json
    # ------------------------------------------------------------------
    # Batch Population
    # ------------------------------------------------------------------

    def _populate_batch(
        self,
        batch: QuestionBatchModel,
        payload: dict[str, Any],
    ) -> None:
        """
        Populate batch-level information.
        """

        batch.batch_id = str(
            payload.get(
                "batch_id",
                "",
            )
        )

        batch.unit_code = str(
            payload.get(
                "unit_code",
                "",
            )
        )

        batch.chapter_code = str(
            payload.get(
                "chapter_code",
                "",
            )
        )

        batch.subtopic_code = str(
            payload.get(
                "subtopic_code",
                "",
            )
        )

        batch.set_number = int(
            payload.get(
                "set_number",
                1,
            )
        )

        batch.batch_number = int(
            payload.get(
                "batch_number",
                1,
            )
        )

        batch.status = str(
            payload.get(
                "status",
                "CREATED",
            )
        )

        metadata = payload.get(
            "metadata",
            {},
        )

        if isinstance(
            metadata,
            dict,
        ):
            batch.metadata.update(
                metadata,
            )
    # ------------------------------------------------------------------
    # Question Population
    # ------------------------------------------------------------------

    def _populate_questions(
        self,
        batch: QuestionBatchModel,
        payload: dict[str, Any],
    ) -> None:
        """
        Populate all questions contained in the
        payload.
        """

        questions = payload.get(
            "questions",
            [],
        )

        if not isinstance(
            questions,
            list,
        ):
            raise ValueError(
                "'questions' must be a list."
            )

        for item in questions:

            if not isinstance(
                item,
                dict,
            ):
                continue

            batch.add_question(
                self._create_question(
                    item,
                )
            )
    # ------------------------------------------------------------------
    # Question Construction
    # ------------------------------------------------------------------

    def _create_question(
        self,
        data: dict[str, Any],
    ) -> GeneratedQuestionModel:
        """
        Create a GeneratedQuestionModel from
        a parsed dictionary.
        """

        question = GeneratedQuestionModel()

        question.question_code = str(
            data.get(
                "question_code",
                "",
            )
        )

        question.unit_code = str(
            data.get(
                "unit_code",
                "",
            )
        )

        question.chapter_code = str(
            data.get(
                "chapter_code",
                "",
            )
        )

        question.subtopic_code = str(
            data.get(
                "subtopic_code",
                "",
            )
        )

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

        question.question_text = str(
            data.get(
                "question_text",
                "",
            )
        )
        #
        # Options
        #

        options = data.get(
            "options",
            [],
        )

        if isinstance(
            options,
            list,
        ):
            question.options.extend(
                str(option)
                for option in options
            )

        question.correct_option = str(
            data.get(
                "correct_option",
                "",
            )
        )

        question.explanation = str(
            data.get(
                "explanation",
                "",
            )
        )

        #
        # Academic metadata
        #

        question.difficulty = str(
            data.get(
                "difficulty",
                "",
            )
        )

        question.archetype = str(
            data.get(
                "archetype",
                "",
            )
        )

        question.concept = str(
            data.get(
                "concept",
                "",
            )
        )

        #
        # Tags
        #

        tags = data.get(
            "tags",
            [],
        )

        if isinstance(
            tags,
            list,
        ):
            question.tags.extend(
                str(tag)
                for tag in tags
            )

        #
        # Metadata
        #

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

        return question

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def statistics(
        self,
        batch: QuestionBatchModel,
    ) -> dict[str, Any]:
        """
        Return adapter statistics for the
        supplied batch.
        """

        return {
            "question_count": (
                batch.question_count
            ),
            "complete_questions": (
                batch.complete_question_count
            ),
            "incomplete_questions": (
                batch.incomplete_question_count
            ),
        }

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def diagnostics(
        self,
        batch: QuestionBatchModel,
    ) -> dict[str, Any]:
        """
        Return adapter diagnostics.
        """

        return {
            "component": (
                self.__class__.__name__
            ),
            "batch": (
                batch.summary()
            ),
            "statistics": (
                self.statistics(batch)
            ),
        }

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    def health(
        self,
    ) -> dict[str, Any]:
        """
        Return adapter health information.
        """

        return {
            "component": (
                self.__class__.__name__
            ),
            "status": "READY",
            "version": "2.1.0",
        }
    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def validate_configuration(
        self,
    ) -> None:
        """
        Validate adapter configuration.

        The BatchAdapter is currently stateless,
        therefore there is no runtime configuration
        to validate.
        """

        return

    @property
    def is_ready(
        self,
    ) -> bool:
        """
        Return True if the adapter is ready.
        """

        return True

    # ------------------------------------------------------------------
    # Capabilities
    # ------------------------------------------------------------------

    def capabilities(
        self,
    ) -> dict[str, bool]:
        """
        Return adapter capabilities.
        """

        return {
            "batch_conversion": True,
            "question_conversion": True,
            "metadata_mapping": True,
            "diagnostics": True,
            "health_reporting": True,
        }

    def supports_batch_conversion(
        self,
    ) -> bool:
        """
        Return True if batch conversion is
        supported.
        """

        return True

    def supports_metadata(
        self,
    ) -> bool:
        """
        Return True if metadata mapping is
        supported.
        """

        return True

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summary(
        self,
    ) -> dict[str, Any]:
        """
        Return a concise adapter summary.
        """

        return {
            "component": self.__class__.__name__,
            "version": "2.1.0",
            "ready": self.is_ready,
        }

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def create(
        cls,
    ) -> "BatchAdapter":
        """
        Create a production-ready BatchAdapter.
        """

        adapter = cls()

        logger.info(
            "Production BatchAdapter created."
        )

        return adapter

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            "(ready=True)"
        )

    __str__ = __repr__


# ----------------------------------------------------------------------
# Factory Helper
# ----------------------------------------------------------------------


def create_batch_adapter() -> BatchAdapter:
    """
    Create a production-ready BatchAdapter.
    """

    return BatchAdapter.create()


# ----------------------------------------------------------------------
# Module Exports
# ----------------------------------------------------------------------

__all__ = [
    "BatchAdapter",
    "create_batch_adapter",
]
