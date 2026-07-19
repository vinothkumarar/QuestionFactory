"""
Question Factory OS v2.1

Batch Adapter

Bridges the AI subsystem and the manufacturing
subsystem by converting ParsedResponse objects
into QuestionBatchModel instances.

Responsibilities
----------------
• Extract normalized payloads from ParsedResponse
• Build GeneratedQuestionModel objects
• Populate QuestionBatchModel
• Preserve metadata

The adapter intentionally performs NO
validation or repair.
"""

from __future__ import annotations

import logging

from typing import Any

from Engine.factory.ai.response_parser import (
    ParsedResponse,
)
from Engine.factory.generation.generated_question_builder import (
    GeneratedQuestionBuilder,
)
from Engine.models.question_batch_model import (
    QuestionBatchModel,
)

LOGGER = logging.getLogger(__name__)


class BatchAdapter:
    """
    Converts ParsedResponse objects into
    QuestionBatchModel instances.

    This class performs only deterministic
    structural mapping.
    """

    VERSION = "2.1.0"

    COMPONENT_NAME = "Batch Adapter"

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def __init__(
        self,
    ) -> None:

        self._logger = LOGGER

        self._builder = (
            GeneratedQuestionBuilder()
        )

        self._logger.info(
            "%s initialized.",
            self.COMPONENT_NAME,
        )

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def build(
        self,
        parsed: ParsedResponse,
    ) -> QuestionBatchModel:
        """
        Convert a ParsedResponse into a
        QuestionBatchModel.
        """

        if not parsed.success:

            raise ValueError(
                "ParsedResponse was not successful."
            )

        payload = self._extract_payload(
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

    # ---------------------------------------------------------
    # Payload Extraction
    # ---------------------------------------------------------

    def _extract_payload(
        self,
        parsed: ParsedResponse,
    ) -> dict[str, Any]:
        """
        Extract the normalized JSON payload.
        """

        if parsed.raw_json is None:

            raise ValueError(
                "ParsedResponse does not "
                "contain JSON."
            )

        if not isinstance(
            parsed.raw_json,
            dict,
        ):
            raise TypeError(
                "ParsedResponse JSON "
                "must be a dictionary."
            )

        return parsed.raw_json
    # ---------------------------------------------------------
    # Batch Population
    # ---------------------------------------------------------

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
        ).strip()

        batch.unit_code = str(
            payload.get(
                "unit_code",
                "",
            )
        ).strip()

        batch.chapter_code = str(
            payload.get(
                "chapter_code",
                "",
            )
        ).strip()

        batch.subtopic_code = str(
            payload.get(
                "subtopic_code",
                "",
            )
        ).strip()

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
        ).strip()

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

    # ---------------------------------------------------------
    # Question Population
    # ---------------------------------------------------------

    def _populate_questions(
        self,
        batch: QuestionBatchModel,
        payload: dict[str, Any],
    ) -> None:
        """
        Populate all generated questions.
        """

        questions = payload.get(
            "questions",
            [],
        )

        if not isinstance(
            questions,
            list,
        ):
            raise TypeError(
                "'questions' must be a list."
            )

        for item in questions:

            if not isinstance(
                item,
                dict,
            ):
                continue

            question = self._builder.build(
                item,
            )

            batch.add_question(
                question,
            )
    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
        batch: QuestionBatchModel,
    ) -> dict[str, Any]:
        """
        Return adapter statistics.
        """

        return {
            "batch_id": batch.batch_id,
            "question_count": len(
                batch.questions,
            ),
            "status": batch.status,
            "unit_code": batch.unit_code,
            "chapter_code": batch.chapter_code,
            "subtopic_code": batch.subtopic_code,
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return adapter diagnostics.
        """

        return {
            "component": self.COMPONENT_NAME,
            "version": self.VERSION,
            "builder": self._builder.component_name,
            "supports_batch_mapping": True,
            "supports_question_mapping": True,
            "supports_metadata": True,
            "validation": "EXTERNAL",
            "repair": "EXTERNAL",
        }

    def configuration(
        self,
    ) -> dict[str, Any]:
        """
        Return adapter configuration.
        """

        return {
            "component": self.COMPONENT_NAME,
            "version": self.VERSION,
            "mapping_mode": "STRUCTURAL",
            "payload_source": "ParsedResponse.raw_json",
        }

    def health(
        self,
    ) -> dict[str, Any]:
        """
        Return runtime health.
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
            "build_batch": True,
            "build_questions": True,
            "payload_extraction": True,
            "metadata_mapping": True,
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
        Adapter version.
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
            "builder": (
                self._builder.component_name
            ),
        }

    # ---------------------------------------------------------
    # Logging Helpers
    # ---------------------------------------------------------

    def _log_build_start(
        self,
    ) -> None:
        """
        Log the start of a batch build.
        """

        self._logger.debug(
            "Building QuestionBatchModel."
        )

    def _log_build_complete(
        self,
        batch: QuestionBatchModel,
    ) -> None:
        """
        Log successful batch creation.
        """

        self._logger.debug(
            "QuestionBatchModel built successfully "
            "(batch_id=%s, questions=%d).",
            batch.batch_id,
            len(
                batch.questions,
            ),
        )

    def _log_build_failure(
        self,
        exc: Exception,
    ) -> None:
        """
        Log build failure.
        """

        self._logger.exception(
            "Failed to build QuestionBatchModel: %s",
            exc,
        )
    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.COMPONENT_NAME}"
            f"(version='{self.VERSION}')"
        )

    def __str__(
        self,
    ) -> str:
        """
        Human-readable representation.
        """

        return (
            f"{self.COMPONENT_NAME} "
            f"v{self.VERSION}"
        )

    # ---------------------------------------------------------
    # Convenience API
    # ---------------------------------------------------------

    def build_from_json(
        self,
        payload: dict[str, Any],
    ) -> QuestionBatchModel:
        """
        Build a QuestionBatchModel directly from a
        normalized JSON payload.

        Useful for testing and offline execution.
        """

        if not isinstance(
            payload,
            dict,
        ):
            raise TypeError(
                "Payload must be a dictionary."
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

    # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset the adapter state.

        Currently stateless, retained for
        lifecycle consistency.
        """

        self._logger.debug(
            "%s reset.",
            self.COMPONENT_NAME,
        )

