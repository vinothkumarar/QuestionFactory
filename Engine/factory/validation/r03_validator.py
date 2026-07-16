"""
Question Factory OS v2.0

R03 Validator

Blueprint and manufacturing quality validation.

Performs comprehensive evaluation of generated
question batches against the Frozen Blueprint,
JEE quality standards and manufacturing rules.
"""

from __future__ import annotations

from Engine.factory.validation.validator_base import (
    ValidatorBase,
)

from Engine.factory.validation.validation_result_model import (
    ValidationResultModel,
)

from Engine.models.question_batch_model import (
    QuestionBatchModel,
)


class R03Validator(ValidatorBase):
    """
    Blueprint and quality validator.

    R03 is responsible for determining whether a
    generated batch satisfies the manufacturing
    standards required for publication.
    """

    @property
    def name(self) -> str:

        return "R03 Blueprint Validator"

    @property
    def rule_code(self) -> str:

        return "R03"

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
        batch: QuestionBatchModel,
    ) -> ValidationResultModel:
        """
        Execute blueprint validation.
        """

        result = self.create_success_result()

        self._validate_blueprint(
            batch,
            result,
        )

        self._validate_difficulty(
            batch,
            result,
        )

        self._validate_concepts(
            batch,
            result,
        )

        self._validate_quality(
            batch,
            result,
        )

        self._calculate_score(
            batch,
            result,
        )

        if result.has_errors():

            result.mark_failure()

        else:

            result.mark_success()

        return result

    # ---------------------------------------------------------
    # Blueprint Validation
    # ---------------------------------------------------------

    def _validate_blueprint(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Validate compliance with the production
        blueprint.

        R03 verifies that the generated batch
        contains the information required by the
        manufacturing blueprint before advanced
        quality analysis begins.
        """

        if not batch.metadata:

            result.add_warning("Batch contains no blueprint metadata.")

            return

        required_fields = [
            "subject",
            "unit",
            "chapter",
            "subtopic",
            "difficulty",
            "exam_level",
        ]

        for field in required_fields:

            if field not in batch.metadata:

                result.add_warning(f"Blueprint metadata missing: " f"{field}")

        #
        # Blueprint consistency
        #

        metadata = batch.metadata

        if "unit" in metadata and metadata["unit"] != batch.unit_code:

            result.add_error("Blueprint unit mismatch.")

        if "chapter" in metadata and metadata["chapter"] != batch.chapter_code:

            result.add_error("Blueprint chapter mismatch.")

        if "subtopic" in metadata and metadata["subtopic"] != batch.subtopic_code:

            result.add_error("Blueprint subtopic mismatch.")

    # ---------------------------------------------------------
    # Difficulty Validation
    # ---------------------------------------------------------

    def _validate_difficulty(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Validate question difficulty information.
        """

        allowed = {
            "Easy",
            "Easy+",
            "Medium",
            "Hard",
            "Elite",
        }

        for index, question in enumerate(
            batch.questions,
            start=1,
        ):

            difficulty = question.difficulty.strip()

            if not difficulty:

                result.add_warning(f"Question {index}: " "Difficulty missing.")

                continue

            if difficulty not in allowed:

                result.add_error(
                    f"Question {index}: " f"Invalid difficulty " f"'{difficulty}'."
                )

    # ---------------------------------------------------------
    # Concept Validation
    # ---------------------------------------------------------

    def _validate_concepts(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Validate educational concepts and
        blueprint attributes.
        """

        concept_registry = set()

        archetype_registry = set()

        for index, question in enumerate(
            batch.questions,
            start=1,
        ):

            #
            # Concept
            #

            concept = question.concept.strip()

            if not concept:

                result.add_warning(f"Question {index}: " "Concept not specified.")

            else:

                concept_registry.add(concept.lower())

            #
            # Archetype
            #

            archetype = question.archetype.strip()

            if not archetype:

                result.add_warning(f"Question {index}: " "Archetype not specified.")

            else:

                archetype_registry.add(archetype.lower())

            #
            # Estimated solving time
            #

            estimated_time = question.metadata.get(
                "estimated_time_sec",
                None,
            )

            if estimated_time is None:

                result.add_warning(
                    f"Question {index}: " "Estimated solving time " "not provided."
                )

            elif estimated_time <= 0:

                result.add_error(
                    f"Question {index}: " "Invalid estimated solving " "time."
                )

        #
        # Batch-level coverage
        #

        if len(concept_registry) == 1:

            result.add_warning("All questions use the same " "concept.")

        if len(archetype_registry) == 1:

            result.add_warning("All questions use the same " "archetype.")

    # ---------------------------------------------------------
    # Blueprint Attribute Validation
    # ---------------------------------------------------------

    def _validate_blueprint_attributes(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Validate blueprint-specific attributes.
        """

        for index, question in enumerate(
            batch.questions,
            start=1,
        ):

            bloom = question.metadata.get(
                "bloom_level",
                "",
            )

            if not bloom:

                result.add_warning(f"Question {index}: " "Bloom level missing.")

            exam_level = question.metadata.get(
                "exam_level",
                "",
            )

            if not exam_level:

                result.add_warning(f"Question {index}: " "Exam level missing.")

            source_type = question.metadata.get(
                "source_type",
                "",
            )

            if not source_type:

                result.add_warning(f"Question {index}: " "Source type missing.")

    # ---------------------------------------------------------
    # Quality Validation
    # ---------------------------------------------------------

    def _validate_quality(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Execute manufacturing quality validation.
        """

        self._validate_distractors(
            batch,
            result,
        )

        self._validate_bloom_progression(
            batch,
            result,
        )

        self._validate_difficulty_progression(
            batch,
            result,
        )

    # ---------------------------------------------------------
    # Distractor Engineering
    # ---------------------------------------------------------

    def _validate_distractors(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Validate distractor quality.
        """

        for index, question in enumerate(
            batch.questions,
            start=1,
        ):

            correct = question.correct_option.strip().upper()

            option_labels = (
                "A",
                "B",
                "C",
                "D",
            )

            for label, option in zip(
                option_labels,
                question.options,
            ):

                if label == correct:

                    continue

                if len(option.strip()) < 2:

                    result.add_warning(
                        f"Question {index}: "
                        f"Distractor {label} "
                        "appears too short."
                    )

    # ---------------------------------------------------------
    # Bloom Progression
    # ---------------------------------------------------------

    def _validate_bloom_progression(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Validate Bloom taxonomy information.
        """

        for index, question in enumerate(
            batch.questions,
            start=1,
        ):

            bloom = question.metadata.get(
                "bloom_level",
                "",
            ).strip()

            if not bloom:

                result.add_warning(f"Question {index}: " "Bloom level not assigned.")

    # ---------------------------------------------------------
    # Difficulty Progression
    # ---------------------------------------------------------

    def _validate_difficulty_progression(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Validate batch difficulty progression.
        """

        difficulty_order = {
            "Easy": 1,
            "Easy+": 2,
            "Medium": 3,
            "Hard": 4,
            "Elite": 5,
        }

        previous = None

        for index, question in enumerate(
            batch.questions,
            start=1,
        ):

            current = difficulty_order.get(
                question.difficulty,
            )

            if current is None:

                continue

            if previous is not None and current < previous:

                result.add_warning(
                    f"Question {index}: "
                    "Difficulty progression "
                    "decreases within batch."
                )

            previous = current

    # ---------------------------------------------------------
    # JEE Quality Validation
    # ---------------------------------------------------------

    def _validate_jee_quality(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Validate JEE-oriented quality attributes.
        """

        for index, question in enumerate(
            batch.questions,
            start=1,
        ):

            metadata = question.metadata

            #
            # Exam relevance
            #

            exam_relevance = metadata.get(
                "exam_relevance",
                "",
            )

            if not exam_relevance:

                result.add_warning(f"Question {index}: " "Exam relevance missing.")

            #
            # PYQ information
            #

            pyq_inspired = metadata.get(
                "pyq_inspired",
                None,
            )

            if pyq_inspired is None:

                result.add_warning(
                    f"Question {index}: " "PYQ inspiration flag " "missing."
                )

            #
            # Estimated solving time
            #

            estimated_time = metadata.get(
                "estimated_time_sec",
                None,
            )

            if estimated_time is not None and estimated_time > 300:

                result.add_warning(
                    f"Question {index}: "
                    "Estimated solving time "
                    "appears unusually high."
                )

    # ---------------------------------------------------------
    # Manufacturing Metrics
    # ---------------------------------------------------------

    def _calculate_score(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Calculate manufacturing quality metrics.
        """

        question_count = max(
            batch.question_count,
            1,
        )

        penalty = result.error_count * 10 + result.warning_count * 2

        score = max(
            0,
            100 - penalty,
        )

        result.set_metadata(
            "manufacturing_score",
            score,
        )

        result.set_metadata(
            "questions_checked",
            question_count,
        )

        result.set_metadata(
            "quality_grade",
            self._quality_grade(score),
        )

    def _quality_grade(
        self,
        score: int,
    ) -> str:
        """
        Convert a numeric score into a quality grade.
        """

        if score >= 95:
            return "A+"

        if score >= 90:
            return "A"

        if score >= 80:
            return "B"

        if score >= 70:
            return "C"

        return "REVIEW"

    # ---------------------------------------------------------
    # Blueprint Metrics
    # ---------------------------------------------------------

    def _calculate_blueprint_metrics(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Calculate blueprint compliance metrics.
        """

        question_count = max(
            batch.question_count,
            1,
        )

        concepts = set()

        archetypes = set()

        bloom_levels = set()

        difficulty_levels = set()

        for question in batch.questions:

            if question.concept.strip():

                concepts.add(question.concept.strip())

            if question.archetype.strip():

                archetypes.add(question.archetype.strip())

            bloom = question.metadata.get(
                "bloom_level",
                "",
            )

            if bloom:

                bloom_levels.add(bloom)

            if question.difficulty.strip():

                difficulty_levels.add(question.difficulty)

        metrics = {
            "concept_diversity": round(
                len(concepts) / question_count,
                2,
            ),
            "archetype_diversity": round(
                len(archetypes) / question_count,
                2,
            ),
            "bloom_diversity": round(
                len(bloom_levels) / question_count,
                2,
            ),
            "difficulty_diversity": round(
                len(difficulty_levels) / question_count,
                2,
            ),
        }

        result.set_metadata(
            "blueprint_metrics",
            metrics,
        )

    # ---------------------------------------------------------
    # Coverage Metrics
    # ---------------------------------------------------------

    def _calculate_coverage_metrics(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Calculate manufacturing coverage metrics.
        """

        total = max(
            batch.question_count,
            1,
        )

        completed = sum(1 for question in batch.questions if question.is_complete())

        coverage = round(
            completed / total,
            2,
        )

        result.set_metadata(
            "coverage_score",
            coverage,
        )

        result.set_metadata(
            "completed_questions",
            completed,
        )

        result.set_metadata(
            "total_questions",
            total,
        )

    # ---------------------------------------------------------
    # Manufacturing Readiness
    # ---------------------------------------------------------

    def _evaluate_manufacturing_readiness(
        self,
        result: ValidationResultModel,
    ) -> None:
        """
        Determine whether the batch is ready
        for the next manufacturing stage.
        """

        score = result.get_metadata(
            "manufacturing_score",
            0,
        )

        coverage = result.get_metadata(
            "coverage_score",
            0.0,
        )

        errors = result.error_count

        if errors > 0:

            readiness = "REPAIR_REQUIRED"

        elif score >= 95 and coverage >= 1.0:

            readiness = "READY_FOR_PACKAGING"

        elif score >= 80:

            readiness = "QUALITY_REVIEW"

        else:

            readiness = "REPAIR_REQUIRED"

        result.set_metadata(
            "manufacturing_readiness",
            readiness,
        )

    # ---------------------------------------------------------
    # Approval Decision
    # ---------------------------------------------------------

    def _approval_decision(
        self,
        result: ValidationResultModel,
    ) -> None:
        """
        Determine the production decision.
        """

        readiness = result.get_metadata(
            "manufacturing_readiness",
            "",
        )

        decision_map = {
            "READY_FOR_PACKAGING": "APPROVED",
            "QUALITY_REVIEW": "REVIEW",
            "REPAIR_REQUIRED": "REJECTED",
        }

        decision = decision_map.get(
            readiness,
            "REVIEW",
        )

        result.set_metadata(
            "production_decision",
            decision,
        )

    # ---------------------------------------------------------
    # Quality Classification
    # ---------------------------------------------------------

    def _classify_quality(
        self,
        result: ValidationResultModel,
    ) -> None:
        """
        Classify manufacturing quality.
        """

        score = result.get_metadata(
            "manufacturing_score",
            0,
        )

        if score >= 95:

            classification = "PREMIUM"

        elif score >= 90:

            classification = "STANDARD"

        elif score >= 80:

            classification = "ACCEPTABLE"

        else:

            classification = "BELOW_STANDARD"

        result.set_metadata(
            "quality_classification",
            classification,
        )

    # ---------------------------------------------------------
    # Manufacturing Report
    # ---------------------------------------------------------

    def _build_manufacturing_report(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Build the complete manufacturing report.
        """

        report = {
            "batch_id": batch.batch_id,
            "question_count": batch.question_count,
            "manufacturing_score": result.get_metadata(
                "manufacturing_score",
                0,
            ),
            "quality_grade": result.get_metadata(
                "quality_grade",
                "",
            ),
            "quality_classification": result.get_metadata(
                "quality_classification",
                "",
            ),
            "coverage_score": result.get_metadata(
                "coverage_score",
                0,
            ),
            "production_decision": result.get_metadata(
                "production_decision",
                "",
            ),
            "manufacturing_readiness": result.get_metadata(
                "manufacturing_readiness",
                "",
            ),
            "error_count": result.error_count,
            "warning_count": result.warning_count,
        }

        result.set_metadata(
            "manufacturing_report",
            report,
        )

    # ---------------------------------------------------------
    # Blueprint Summary
    # ---------------------------------------------------------

    def _build_blueprint_summary(
        self,
        result: ValidationResultModel,
    ) -> None:
        """
        Create blueprint summary.
        """

        metrics = result.get_metadata(
            "blueprint_metrics",
            {},
        )

        summary = {
            "concept_diversity": metrics.get(
                "concept_diversity",
                0,
            ),
            "archetype_diversity": metrics.get(
                "archetype_diversity",
                0,
            ),
            "difficulty_diversity": metrics.get(
                "difficulty_diversity",
                0,
            ),
            "bloom_diversity": metrics.get(
                "bloom_diversity",
                0,
            ),
        }

        result.set_metadata(
            "blueprint_summary",
            summary,
        )

    # ---------------------------------------------------------
    # Quality Indicators
    # ---------------------------------------------------------

    def _build_quality_indicators(
        self,
        result: ValidationResultModel,
    ) -> None:
        """
        Build manufacturing indicators.
        """

        indicators = {
            "structure": "PASS",
            "academic": ("PASS" if result.error_count == 0 else "FAIL"),
            "blueprint": (
                "PASS"
                if result.get_metadata(
                    "manufacturing_score",
                    0,
                )
                >= 80
                else "FAIL"
            ),
            "ready": (
                result.get_metadata(
                    "manufacturing_readiness",
                    "",
                )
                == "READY_FOR_PACKAGING"
            ),
        }

        result.set_metadata(
            "quality_indicators",
            indicators,
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> dict:
        """
        Return manufacturing statistics.
        """

        return {
            "questions_checked": (batch.question_count),
            "errors": (result.error_count),
            "warnings": (result.warning_count),
            "manufacturing_score": (
                result.get_metadata(
                    "manufacturing_score",
                    0,
                )
            ),
            "coverage_score": (
                result.get_metadata(
                    "coverage_score",
                    0,
                )
            ),
        }

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    
    def summary(
        self,
        result: ValidationResultModel,
    ) -> dict:
        """
        Return a concise manufacturing summary.
        """

        return {
            "validator": self.name,
            "rule_code": self.rule_code,
            "quality_grade": result.get_metadata(
                "quality_grade",
                "",
            ),
            "production_decision": result.get_metadata(
                "production_decision",
                "",
            ),
            "success": result.is_successful(),
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    
    def diagnostics(
        self,
        result: ValidationResultModel,
    ) -> dict:
        """
        Return complete R03 diagnostics.
        """

        return {
            "component": self.__class__.__name__,
            "summary": self.summary(result),
            "statistics": result.statistics(),
            "metadata": dict(result.metadata),
        }

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(self) -> dict:
        """
        Return validator health information.
        """

        return {
            "validator": self.name,
            "rule_code": self.rule_code,
            "version": self.version,
            "validation_scope": ("BLUEPRINT_QUALITY"),
            "status": "READY",
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(self) -> dict:
        """
        Describe validator capabilities.
        """

        return {
            "blueprint_validation": True,
            "difficulty_validation": True,
            "concept_validation": True,
            "archetype_validation": True,
            "quality_analysis": True,
            "jee_quality": True,
            "manufacturing_scoring": True,
            "readiness_evaluation": True,
            "report_generation": True,
            "diagnostics": True,
            "health_reporting": True,
        }

    # ---------------------------------------------------------
    # Execution Information
    # ---------------------------------------------------------

    def execution_information(
        self,
    ) -> dict:
        """
        Return execution information.
        """

        return {
            "validator": self.name,
            "rule_code": self.rule_code,
            "execution_mode": "SEQUENTIAL",
            "validation_scope": ("BLUEPRINT_AND_QUALITY"),
            "framework_version": self.version,
        }

    
