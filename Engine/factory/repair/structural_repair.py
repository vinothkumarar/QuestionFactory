"""
Question Factory OS v2.0

Structural Repair

Repairs structural defects identified by the
R01 Structural Validator.
"""

from __future__ import annotations

from Engine.factory.repair.repair_base import (
    RepairBase,
)

from Engine.factory.repair.repair_result_model import (
    RepairResultModel,
)

from Engine.models.question_batch_model import (
    QuestionBatchModel,
)


class StructuralRepair(RepairBase):
    """
    Structural repair module.
    """

    @property
    def name(self) -> str:

        return "Structural Repair"

    @property
    def repair_code(self) -> str:

        return "SR01"

    # ---------------------------------------------------------
    # Repair
    # ---------------------------------------------------------

    def repair(
        self,
        batch: QuestionBatchModel,
    ) -> RepairResultModel:
        """
        Execute structural repairs.
        """

        result = self.create_result()

        self._repair_batch_metadata(
            batch,
            result,
        )

        self._repair_questions(
            batch,
            result,
        )

        return result

    # ---------------------------------------------------------
    # Batch Repair
    # ---------------------------------------------------------

    def _repair_batch_metadata(
        self,
        batch: QuestionBatchModel,
        result: RepairResultModel,
    ) -> None:
        """
        Repair batch-level metadata.
        """

        #
        # Ensure metadata exists
        #

        if batch.metadata is None:

            batch.metadata = {}

            result.mark_repaired("Created batch metadata.")

        #
        # Unit
        #

        if "unit" not in batch.metadata and batch.unit_code:

            batch.metadata["unit"] = batch.unit_code

            result.mark_repaired("Recovered unit metadata.")

        #
        # Chapter
        #

        if "chapter" not in batch.metadata and batch.chapter_code:

            batch.metadata["chapter"] = batch.chapter_code

            result.mark_repaired("Recovered chapter metadata.")

        #
        # Subtopic
        #

        if "subtopic" not in batch.metadata and batch.subtopic_code:

            batch.metadata["subtopic"] = batch.subtopic_code

            result.mark_repaired("Recovered subtopic metadata.")

        #
        # Batch ID
        #

        if not batch.batch_id.strip():

            batch.batch_id = "AUTO_BATCH"

            result.mark_repaired("Generated batch ID.")

    # ---------------------------------------------------------
    # Question Repair
    # ---------------------------------------------------------

    def _repair_questions(
        self,
        batch: QuestionBatchModel,
        result: RepairResultModel,
    ) -> None:
        """
        Repair every question in the batch.
        """

        for index, question in enumerate(
            batch.questions,
            start=1,
        ):

            self._repair_question(
                index,
                question,
                result,
            )

    # ---------------------------------------------------------
    # Individual Question Repair
    # ---------------------------------------------------------

    def _repair_question(
        self,
        index: int,
        question,
        result: RepairResultModel,
    ) -> None:
        """
        Repair one generated question.
        """

        #
        # Ensure metadata exists
        #

        if question.metadata is None:

            question.metadata = {}

            result.mark_repaired(f"Question {index}: " "Created metadata.")

        #
        # Explanation
        #

        if not question.explanation.strip():

            question.explanation = (
                "Explanation will be " "generated during the " "academic repair stage."
            )

            result.mark_repaired(
                f"Question {index}: " "Inserted placeholder " "explanation."
            )

        #
        # Estimated solving time
        #

        if "estimated_time_sec" not in question.metadata:

            question.metadata["estimated_time_sec"] = 120

            result.mark_repaired(
                f"Question {index}: " "Estimated solving time " "assigned."
            )

        #
        # Bloom level
        #

        if "bloom_level" not in question.metadata:

            question.metadata["bloom_level"] = "Understand"

            result.mark_repaired(f"Question {index}: " "Bloom level assigned.")

        #
        # Exam level
        #

        if "exam_level" not in question.metadata:

            question.metadata["exam_level"] = "JEE Main"

            result.mark_repaired(f"Question {index}: " "Exam level assigned.")

        #
        # Source type
        #

        if "source_type" not in question.metadata:

            question.metadata["source_type"] = "AI_GENERATED"

            result.mark_repaired(f"Question {index}: " "Source type assigned.")

    # ---------------------------------------------------------
    # Metadata Normalization
    # ---------------------------------------------------------

    def _normalize_question(
        self,
        index: int,
        question,
        result: RepairResultModel,
    ) -> None:
        """
        Normalize question metadata and
        optional fields.
        """

        #
        # Tags
        #

        if "tags" not in question.metadata:

            question.metadata["tags"] = []

            result.mark_repaired(f"Question {index}: " "Tags initialized.")

        #
        # Language
        #

        if "language" not in question.metadata:

            question.metadata["language"] = "English"

            result.mark_repaired(f"Question {index}: " "Language assigned.")

        #
        # Question code
        #

        if question.question_code:

            question.question_code = question.question_code.strip().upper()

        #
        # Trim text fields
        #

        question.question_text = question.question_text.strip()

        question.explanation = question.explanation.strip()

        question.options = [option.strip() for option in question.options]

    # ---------------------------------------------------------
    # Batch Normalization
    # ---------------------------------------------------------

    def _normalize_batch(
        self,
        batch: QuestionBatchModel,
        result: RepairResultModel,
    ) -> None:
        """
        Normalize batch information.
        """

        batch.batch_id = batch.batch_id.strip()

        batch.unit_code = batch.unit_code.strip()

        batch.chapter_code = batch.chapter_code.strip()

        batch.subtopic_code = batch.subtopic_code.strip()

        result.set_metadata(
            "normalized_questions",
            batch.question_count,
        )

        result.set_metadata(
            "normalization_completed",
            True,
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
        batch: QuestionBatchModel,
        result: RepairResultModel,
    ) -> dict:
        """
        Return structural repair statistics.
        """

        return {
            "questions_processed": (batch.question_count),
            "repairs_applied": (result.repaired_count),
            "failed_repairs": (result.failed_count),
            "warnings": (result.warning_count),
            "regeneration_required": (result.regeneration_required),
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
        batch: QuestionBatchModel,
        result: RepairResultModel,
    ) -> dict:
        """
        Return complete structural repair
        diagnostics.
        """

        return {
            "module": self.name,
            "repair_code": self.repair_code,
            "statistics": self.statistics(
                batch,
                result,
            ),
            "repair_summary": (result.summary()),
            "repair_metadata": (dict(result.metadata)),
        }

    # ---------------------------------------------------------
    # Repair Information
    # ---------------------------------------------------------

    def repair_information(
        self,
    ) -> dict:
        """
        Return structural repair information.
        """

        return {
            "module": self.name,
            "repair_code": self.repair_code,
            "repair_scope": ("STRUCTURAL"),
            "automatic": (self.supports_auto_repair()),
            "batch_repair": (self.supports_batch_repair()),
            "execution": (self.execution_information()),
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return "StructuralRepair(" f"repair_code='{self.repair_code}')"

    def __str__(
        self,
    ) -> str:

        return f"{self.repair_code} - " "Structural Repair"
