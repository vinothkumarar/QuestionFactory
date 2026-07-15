"""
Question Factory OS v2.1

Structural Repair

Repairs structural defects detected during
R01 validation.

Responsibilities
----------------
• Repair batch metadata
• Repair question structure
• Normalize structural fields
• Preserve academic correctness

This module performs only structural
repairs. It never modifies the academic
meaning of a question.
"""

from __future__ import annotations

from Engine.factory.repair.repair_base import (
    RepairBase,
)
from Engine.factory.repair.repair_result_model import (
    RepairResultModel,
)
from Engine.models.generated_question_model import (
    GeneratedQuestionModel,
)
from Engine.models.question_batch_model import (
    QuestionBatchModel,
)


class StructuralRepair(RepairBase):
    """
    Repairs structural defects within a
    generated question batch.
    """

    @property
    def name(
        self,
    ) -> str:

        return "Structural Repair"

    @property
    def repair_code(
        self,
    ) -> str:

        return "SR01"

    # -----------------------------------------------------
    # Repair
    # -----------------------------------------------------

    def repair(
        self,
        batch: QuestionBatchModel,
    ) -> RepairResultModel:
        """
        Execute structural repairs.
        """

        result = self.create_result()

        self._repair_batch(
            batch,
            result,
        )

        self._repair_questions(
            batch,
            result,
        )

        self._normalize_batch(
            batch,
            result,
        )

        self._calculate_statistics(
            batch,
            result,
        )

        return result

    # -----------------------------------------------------
    # Batch Repair
    # -----------------------------------------------------

    def _repair_batch(
        self,
        batch: QuestionBatchModel,
        result: RepairResultModel,
    ) -> None:
        """
        Repair batch-level information.
        """

        if batch.metadata is None:

            batch.metadata = {}

            result.mark_repaired(
                "Created batch metadata."
            )

        if not batch.batch_id.strip():

            batch.batch_id = "AUTO_BATCH"

            result.mark_repaired(
                "Generated batch identifier."
            )

        if (
            batch.unit_code
            and "unit" not in batch.metadata
        ):

            batch.metadata["unit"] = (
                batch.unit_code
            )

            result.mark_repaired(
                "Recovered unit metadata."
            )

        if (
            batch.chapter_code
            and "chapter"
            not in batch.metadata
        ):

            batch.metadata["chapter"] = (
                batch.chapter_code
            )

            result.mark_repaired(
                "Recovered chapter metadata."
            )

        if (
            batch.subtopic_code
            and "subtopic"
            not in batch.metadata
        ):

            batch.metadata["subtopic"] = (
                batch.subtopic_code
            )

            result.mark_repaired(
                "Recovered subtopic metadata."
            )
    # -----------------------------------------------------
    # Question Repair
    # -----------------------------------------------------

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
                index=index,
                question=question,
                result=result,
            )

    # -----------------------------------------------------
    # Individual Question Repair
    # -----------------------------------------------------

    def _repair_question(
        self,
        index: int,
        question: GeneratedQuestionModel,
        result: RepairResultModel,
    ) -> None:
        """
        Repair one generated question.
        """

        if question.metadata is None:

            question.metadata = {}

            result.mark_repaired(
                f"Question {index}: "
                "Created metadata."
            )

        #
        # Explanation
        #

        if not question.explanation.strip():

            question.explanation = (
                "Explanation will be "
                "generated during the "
                "academic repair stage."
            )

            result.mark_repaired(
                f"Question {index}: "
                "Inserted placeholder explanation."
            )

        #
        # Estimated solving time
        #

        if (
            "estimated_time_sec"
            not in question.metadata
        ):

            question.metadata[
                "estimated_time_sec"
            ] = 120

            result.mark_repaired(
                f"Question {index}: "
                "Estimated solving time assigned."
            )

        #
        # Bloom level
        #

        if (
            "bloom_level"
            not in question.metadata
        ):

            question.metadata[
                "bloom_level"
            ] = "Understand"

            result.mark_repaired(
                f"Question {index}: "
                "Bloom level assigned."
            )

        #
        # Exam level
        #

        if (
            "exam_level"
            not in question.metadata
        ):

            question.metadata[
                "exam_level"
            ] = "JEE Main"

            result.mark_repaired(
                f"Question {index}: "
                "Exam level assigned."
            )

        #
        # Source type
        #

        if (
            "source_type"
            not in question.metadata
        ):

            question.metadata[
                "source_type"
            ] = "AI_GENERATED"

            result.mark_repaired(
                f"Question {index}: "
                "Source type assigned."
            )

        self._normalize_question(
            index=index,
            question=question,
            result=result,
        )

    # -----------------------------------------------------
    # Question Normalization
    # -----------------------------------------------------

    def _normalize_question(
        self,
        index: int,
        question: GeneratedQuestionModel,
        result: RepairResultModel,
    ) -> None:
        """
        Normalize optional fields and text.
        """

        if "tags" not in question.metadata:

            question.metadata["tags"] = []

            result.mark_repaired(
                f"Question {index}: "
                "Tags initialized."
            )

        if (
            "language"
            not in question.metadata
        ):

            question.metadata[
                "language"
            ] = "English"

            result.mark_repaired(
                f"Question {index}: "
                "Language assigned."
            )

        question.question_code = (
            question.question_code
            .strip()
            .upper()
        )

        question.question_text = (
            question.question_text.strip()
        )

        question.explanation = (
            question.explanation.strip()
        )

        question.options = [
            option.strip()
            for option in question.options
        ]
    # -----------------------------------------------------
    # Batch Normalization
    # -----------------------------------------------------

    def _normalize_batch(
        self,
        batch: QuestionBatchModel,
        result: RepairResultModel,
    ) -> None:
        """
        Normalize batch information.
        """

        batch.batch_id = (
            batch.batch_id.strip()
        )

        batch.unit_code = (
            batch.unit_code.strip()
        )

        batch.chapter_code = (
            batch.chapter_code.strip()
        )

        batch.subtopic_code = (
            batch.subtopic_code.strip()
        )

        result.set_metadata(
            "normalized_questions",
            batch.question_count,
        )

        result.set_metadata(
            "normalization_completed",
            True,
        )

    # -----------------------------------------------------
    # Statistics
    # -----------------------------------------------------

    def _calculate_statistics(
        self,
        batch: QuestionBatchModel,
        result: RepairResultModel,
    ) -> None:
        """
        Calculate structural repair
        statistics.
        """

        result.set_metadata(
            "questions_processed",
            batch.question_count,
        )

        result.set_metadata(
            "repaired_questions",
            result.repaired_count,
        )

        result.set_metadata(
            "failed_repairs",
            result.failed_count,
        )

        result.set_metadata(
            "warnings",
            result.warning_count,
        )

        result.set_metadata(
            "regeneration_required",
            result.regeneration_required,
        )

    def statistics(
        self,
        result: RepairResultModel,
    ) -> dict[str, object]:
        """
        Return structural repair statistics.
        """

        return {
            "questions_processed": (
                result.get_metadata(
                    "questions_processed",
                    0,
                )
            ),
            "repaired_questions": (
                result.repaired_count
            ),
            "failed_repairs": (
                result.failed_count
            ),
            "warnings": (
                result.warning_count
            ),
            "regeneration_required": (
                result.regeneration_required
            ),
            "normalization_completed": (
                result.get_metadata(
                    "normalization_completed",
                    False,
                )
            ),
        }
    # -----------------------------------------------------
    # Diagnostics
    # -----------------------------------------------------

    def diagnostics(
        self,
        result: RepairResultModel,
    ) -> dict[str, object]:
        """
        Return structural repair diagnostics.

        Signature intentionally matches
        RepairBase.
        """

        return {
            "module": self.name,
            "repair_code": self.repair_code,
            "statistics": self.statistics(
                result,
            ),
            "repair_summary": (
                result.summary()
            ),
            "repair_metadata": (
                dict(result.metadata)
            ),
        }

    # -----------------------------------------------------
    # Repair Information
    # -----------------------------------------------------

    def repair_information(
        self,
    ) -> dict[str, object]:
        """
        Return module information.
        """

        return {
            "module": self.name,
            "repair_code": self.repair_code,
            "repair_scope": "STRUCTURAL",
            "automatic": (
                self.supports_auto_repair()
            ),
            "batch_repair": (
                self.supports_batch_repair()
            ),
            "execution": (
                self.execution_information()
            ),
        }

    # -----------------------------------------------------
    # Health
    # -----------------------------------------------------

    def health(
        self,
    ) -> dict[str, object]:
        """
        Return health information.
        """

        return {
            "component": self.name,
            "repair_code": self.repair_code,
            "status": "READY",
            "version": "2.1.0",
        }

    # -----------------------------------------------------
    # Representation
    # -----------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            "("
            f"repair_code="
            f"'{self.repair_code}'"
            ")"
        )

    __str__ = __repr__
    
