"""
Question Factory OS v2.0

Academic Repair

Repairs educational issues identified by
the R02 Academic Validator.

This module performs safe rule-based repairs
followed by optional AI-assisted enhancement.
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


class AcademicRepair(RepairBase):
    """
    Academic repair module.

    Responsible for repairing educational
    quality while preserving correctness.
    """

    @property
    def name(self) -> str:

        return "Academic Repair"

    @property
    def repair_code(self) -> str:

        return "AR01"

    # ---------------------------------------------------------
    # Repair
    # ---------------------------------------------------------

    def repair(
        self,
        batch: QuestionBatchModel,
    ) -> RepairResultModel:
        """
        Execute academic repair.
        """

        result = self.create_result()

        self._repair_metadata(
            batch,
            result,
        )

        self._repair_questions(
            batch,
            result,
        )

        self._ai_enhancement(
            batch,
            result,
        )

        return result

    # ---------------------------------------------------------
    # Metadata Repair
    # ---------------------------------------------------------

    def _repair_metadata(
        self,
        batch: QuestionBatchModel,
        result: RepairResultModel,
    ) -> None:
        """
        Repair academic metadata.
        """

        if batch.metadata is None:

            batch.metadata = {}

            result.mark_repaired("Created academic metadata.")

        if "academic_review" not in batch.metadata:

            batch.metadata["academic_review"] = "PENDING"

            result.mark_repaired("Academic review status assigned.")

        if "quality_level" not in batch.metadata:

            batch.metadata["quality_level"] = "STANDARD"

            result.mark_repaired("Quality level assigned.")

        if "review_required" not in batch.metadata:

            batch.metadata["review_required"] = False

            result.mark_repaired("Review flag initialized.")

    # ---------------------------------------------------------
    # Question Repair
    # ---------------------------------------------------------

    def _repair_questions(
        self,
        batch: QuestionBatchModel,
        result: RepairResultModel,
    ) -> None:
        """
        Repair academic information for every
        question.
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
        Repair academic fields for a single
        question.
        """

        if question.metadata is None:

            question.metadata = {}

            result.mark_repaired(f"Question {index}: " "Academic metadata created.")

        #
        # Concept
        #

        if not question.concept.strip():

            question.concept = "GENERAL_CONCEPT"

            result.mark_repaired(f"Question {index}: " "Concept assigned.")

        #
        # Archetype
        #

        if not question.archetype.strip():

            question.archetype = "STANDARD_MCQ"

            result.mark_repaired(f"Question {index}: " "Archetype assigned.")

        #
        # Educational objective
        #

        if "learning_objective" not in question.metadata:

            question.metadata["learning_objective"] = "Understand the core " "concept."

            result.mark_repaired(f"Question {index}: " "Learning objective assigned.")

        #
        # Explanation quality
        #

        if len(question.explanation.strip()) < 30:

            result.add_warning(
                f"Question {index}: " "Explanation may require " "AI enhancement."
            )

    # ---------------------------------------------------------
    # AI Enhancement
    # ---------------------------------------------------------

    def _ai_enhancement(
        self,
        batch: QuestionBatchModel,
        result: RepairResultModel,
    ) -> None:
        """
        Perform AI-assisted academic enhancement.

        This stage identifies questions that
        would benefit from AI improvement while
        ensuring correctness is never modified
        automatically.
        """

        for index, question in enumerate(
            batch.questions,
            start=1,
        ):

            self._evaluate_question(
                index,
                question,
                result,
            )

    # ---------------------------------------------------------
    # Question Evaluation
    # ---------------------------------------------------------

    def _evaluate_question(
        self,
        index: int,
        question,
        result: RepairResultModel,
    ) -> None:
        """
        Evaluate one question for academic
        enhancement.
        """

        #
        # Explanation Quality
        #

        if len(question.explanation.strip()) < 100:

            result.add_warning(
                f"Question {index}: " "Explanation recommended " "for AI enhancement."
            )

        #
        # Distractor Quality
        #

        duplicate_options = len(set(question.options)) != len(question.options)

        if duplicate_options:

            result.add_warning(
                f"Question {index}: " "Duplicate distractors " "detected."
            )

        #
        # Question Length
        #

        if len(question.question_text.strip()) < 40:

            result.add_warning(
                f"Question {index}: " "Question wording may be " "too brief."
            )

        #
        # Ambiguity Indicators
        #

        ambiguity_terms = {
            "may",
            "might",
            "possibly",
            "approximately",
        }

        lower_text = question.question_text.lower()

        if any(word in lower_text for word in ambiguity_terms):

            result.add_warning(f"Question {index}: " "Potential ambiguity " "detected.")

        #
        # Unsafe Repairs
        #

        if question.correct_option.strip() == "":

            result.mark_regeneration_required(
                f"Question {index}: " "Correct answer missing."
            )

    # ---------------------------------------------------------
    # Academic Quality Metrics
    # ---------------------------------------------------------

    def _calculate_quality_metrics(
        self,
        batch: QuestionBatchModel,
        result: RepairResultModel,
    ) -> None:
        """
        Calculate academic quality metrics.
        """

        question_count = max(
            batch.question_count,
            1,
        )

        ai_recommended = 0

        regeneration_required = 0

        for item in result.warnings:

            if "AI enhancement" in item:

                ai_recommended += 1

        if result.regeneration_required:

            regeneration_required = 1

        quality_score = max(
            0,
            100 - (result.warning_count * 2) - (result.failed_count * 10),
        )

        result.set_metadata(
            "academic_quality_score",
            quality_score,
        )

        result.set_metadata(
            "questions_processed",
            question_count,
        )

        result.set_metadata(
            "ai_recommendations",
            ai_recommended,
        )

        result.set_metadata(
            "regeneration_requests",
            regeneration_required,
        )

    # ---------------------------------------------------------
    # Enhancement Summary
    # ---------------------------------------------------------

    def _build_enhancement_summary(
        self,
        result: RepairResultModel,
    ) -> None:
        """
        Build AI enhancement summary.
        """

        summary = {
            "academic_quality_score": result.get_metadata(
                "academic_quality_score",
                0,
            ),
            "ai_recommendations": result.get_metadata(
                "ai_recommendations",
                0,
            ),
            "regeneration_requests": result.get_metadata(
                "regeneration_requests",
                0,
            ),
            "warnings": result.warning_count,
            "failed_repairs": result.failed_count,
        }

        result.set_metadata(
            "enhancement_summary",
            summary,
        )

    # ---------------------------------------------------------
    # Academic Diagnostics
    # ---------------------------------------------------------

    def _build_diagnostics(
        self,
        result: RepairResultModel,
    ) -> None:
        """
        Build academic repair diagnostics.
        """

        diagnostics = {
            "repair_status": (
                "REGENERATION_REQUIRED" if result.regeneration_required else "COMPLETED"
            ),
            "quality_score": result.get_metadata(
                "academic_quality_score",
                0,
            ),
            "ai_required": (result.get_metadata("ai_recommendations", 0) > 0),
            "warnings": result.warning_count,
            "repaired": result.repaired_count,
        }

        result.set_metadata(
            "academic_diagnostics",
            diagnostics,
        )

    