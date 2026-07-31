"""
Question Factory OS v3.0

Schema Validator

Performs structural validation of the canonical
Question Factory models.
"""

from __future__ import annotations

from Engine.models.production_node_model import ProductionNodeModel
from Engine.models.question_batch_model import QuestionBatchModel
from Engine.models.generated_question_model import GeneratedQuestionModel
from Engine.models.runtime_model import RuntimeModel
from Engine.blueprint.blueprint_model import BlueprintModel

from Engine.validation.validation_result import ValidationResult
from Engine.validation.validation_error import ValidationError


class SchemaValidator:
    """
    Structural schema validator.

    Validates canonical Question Factory models.
    """

    def validate_production_node(
        self,
        node: ProductionNodeModel,
    ) -> ValidationResult:
        """
        Validate a ProductionNodeModel.
        """

        result = ValidationResult()

        # -----------------------------------------------------
        # Location
        # -----------------------------------------------------

        if not node.location.subject.strip():
            result.add_error(
                ValidationError(
                    code="PN001",
                    field="location.subject",
                    message="Subject is required.",
                )
            )

        if not node.location.unit.strip():
            result.add_error(
                ValidationError(
                    code="PN002",
                    field="location.unit",
                    message="Unit is required.",
                )
            )

        if not node.location.chapter.strip():
            result.add_error(
                ValidationError(
                    code="PN003",
                    field="location.chapter",
                    message="Chapter is required.",
                )
            )

        if not node.location.subtopic.strip():
            result.add_error(
                ValidationError(
                    code="PN004",
                    field="location.subtopic",
                    message="Subtopic is required.",
                )
            )

        # -----------------------------------------------------
        # Question Range
        # -----------------------------------------------------

        if node.question_range.question_from <= 0:
            result.add_error(
                ValidationError(
                    code="PN005",
                    field="question_range.question_from",
                    message="Question start must be greater than zero.",
                )
            )

        if node.question_range.question_to < node.question_range.question_from:
            result.add_error(
                ValidationError(
                    code="PN006",
                    field="question_range.question_to",
                    message="Question end must be greater than or equal to question start.",
                )
            )

        if node.question_count != node.question_range.expected_questions:
            result.add_error(
                ValidationError(
                    code="PN007",
                    field="question_range.expected_questions",
                    message="Expected question count does not match question range.",
                )
            )

        # -----------------------------------------------------
        # Batch Information
        # -----------------------------------------------------

        if node.location.set_number <= 0:
            result.add_error(
                ValidationError(
                    code="PN008",
                    field="location.set_number",
                    message="Set number must be greater than zero.",
                )
            )

        if node.location.batch_number <= 0:
            result.add_error(
                ValidationError(
                    code="PN009",
                    field="location.batch_number",
                    message="Batch number must be greater than zero.",
                )
            )

        # -----------------------------------------------------
        # Metadata
        # -----------------------------------------------------

        if not node.metadata.node_id.strip():
            result.add_error(
                ValidationError(
                    code="PN010",
                    field="metadata.node_id",
                    message="Node ID is required.",
                )
            )

        return result

    def validate_batch(
        self,
        batch: QuestionBatchModel,
    ) -> ValidationResult:
        """
        Validate a QuestionBatchModel.
        """

        result = ValidationResult()

        # -----------------------------------------------------
        # Identity
        # -----------------------------------------------------

        if not batch.batch_id.strip():
            result.add_error(
                ValidationError(
                    code="B001",
                    field="batch_id",
                    message="Batch ID is required.",
                )
            )

        if not batch.unit_code.strip():
            result.add_error(
                ValidationError(
                    code="B002",
                    field="unit_code",
                    message="Unit code is required.",
                )
            )

        if not batch.chapter_code.strip():
            result.add_error(
                ValidationError(
                    code="B003",
                    field="chapter_code",
                    message="Chapter code is required.",
                )
            )

        if not batch.subtopic_code.strip():
            result.add_error(
                ValidationError(
                    code="B004",
                    field="subtopic_code",
                    message="Subtopic code is required.",
                )
            )

        # -----------------------------------------------------
        # Batch Numbers
        # -----------------------------------------------------

        if batch.set_number <= 0:
            result.add_error(
                ValidationError(
                    code="B005",
                    field="set_number",
                    message="Set number must be greater than zero.",
                )
            )

        if batch.batch_number <= 0:
            result.add_error(
                ValidationError(
                    code="B006",
                    field="batch_number",
                    message="Batch number must be greater than zero.",
                )
            )

        # -----------------------------------------------------
        # Questions
        # -----------------------------------------------------

        if batch.is_empty():
            result.add_error(
                ValidationError(
                    code="B007",
                    field="questions",
                    message="Batch contains no questions.",
                )
            )
        else:
            for index, question in enumerate(batch.questions, start=1):
                question_result = self.validate_question(question)

                for error in question_result.errors:
                    result.add_error(
                        ValidationError(
                            code=error.code,
                            field=f"questions[{index}].{error.field}",
                            message=error.message,
                            value=error.value,
                            severity=error.severity,
                        )
                    )

                for warning in question_result.warnings:
                    result.add_warning(
                        f"questions[{index}]: {warning}"
                    )

        return result

    def validate_question(
        self,
        question: GeneratedQuestionModel,
    ) -> ValidationResult:
        """
        Validate a GeneratedQuestionModel.
        """

        result = ValidationResult()

        # -----------------------------------------------------
        # Identity
        # -----------------------------------------------------

        if not question.question_code.strip():
            result.add_error(
                ValidationError(
                    code="Q001",
                    field="question_code",
                    message="Question code is required.",
                )
            )

        # -----------------------------------------------------
        # Academic Information
        # -----------------------------------------------------

        if not question.unit_code.strip():
            result.add_error(
                ValidationError(
                    code="Q002",
                    field="unit_code",
                    message="Unit code is required.",
                )
            )

        if not question.chapter_code.strip():
            result.add_error(
                ValidationError(
                    code="Q003",
                    field="chapter_code",
                    message="Chapter code is required.",
                )
            )

        if not question.subtopic_code.strip():
            result.add_error(
                ValidationError(
                    code="Q004",
                    field="subtopic_code",
                    message="Subtopic code is required.",
                )
            )

        # -----------------------------------------------------
        # Question
        # -----------------------------------------------------

        if not question.question_text.strip():
            result.add_error(
                ValidationError(
                    code="Q005",
                    field="question_text",
                    message="Question text is required.",
                )
            )

        if len(question.options) < 2:
            result.add_error(
                ValidationError(
                    code="Q006",
                    field="options",
                    message="At least two options are required.",
                )
            )

        if not question.correct_option.strip():
            result.add_error(
                ValidationError(
                    code="Q007",
                    field="correct_option",
                    message="Correct option is required.",
                )
            )

        # -----------------------------------------------------
        # Metadata
        # -----------------------------------------------------

        if not question.difficulty.strip():
            result.add_error(
                ValidationError(
                    code="Q008",
                    field="difficulty",
                    message="Difficulty is required.",
                )
            )

        if not question.archetype.strip():
            result.add_error(
                ValidationError(
                    code="Q009",
                    field="archetype",
                    message="Archetype is required.",
                )
            )

        return result

    def validate_runtime(
        self,
        runtime: RuntimeModel,
    ) -> ValidationResult:
        """
        Validate a RuntimeModel.
        """

        result = ValidationResult()

        # -----------------------------------------------------
        # Factory
        # -----------------------------------------------------

        if not runtime.factory.version.strip():
            result.add_error(
                ValidationError(
                    code="R001",
                    field="factory.version",
                    message="Factory version is required.",
                )
            )

        if not runtime.factory.status.strip():
            result.add_error(
                ValidationError(
                    code="R002",
                    field="factory.status",
                    message="Factory status is required.",
                )
            )

        # -----------------------------------------------------
        # Production
        # -----------------------------------------------------

        if not runtime.production.subject.strip():
            result.add_error(
                ValidationError(
                    code="R003",
                    field="production.subject",
                    message="Subject is required.",
                )
            )

        if not runtime.production.unit.strip():
            result.add_error(
                ValidationError(
                    code="R004",
                    field="production.unit",
                    message="Unit is required.",
                )
            )

        if runtime.production.question_from <= 0:
            result.add_error(
                ValidationError(
                    code="R005",
                    field="production.question_from",
                    message="Question start must be greater than zero.",
                )
            )

        if runtime.production.question_to < runtime.production.question_from:
            result.add_error(
                ValidationError(
                    code="R006",
                    field="production.question_to",
                    message="Question end must be greater than or equal to question start.",
                )
            )

        return result

    def validate_blueprint(
        self,
        blueprint: BlueprintModel,
    ) -> ValidationResult:
        """
        Validate a BlueprintModel.
        """

        result = ValidationResult()

        # -----------------------------------------------------
        # Factory Information
        # -----------------------------------------------------

        if not blueprint.factory.name.strip():
            result.add_error(
                ValidationError(
                    code="BP001",
                    field="factory.name",
                    message="Factory name is required.",
                )
            )

        if not blueprint.factory.version.strip():
            result.add_error(
                ValidationError(
                    code="BP002",
                    field="factory.version",
                    message="Factory version is required.",
                )
            )

        # -----------------------------------------------------
        # Version Control
        # -----------------------------------------------------

        if not blueprint.version.blueprint_version.strip():
            result.add_error(
                ValidationError(
                    code="BP003",
                    field="version.blueprint_version",
                    message="Blueprint version is required.",
                )
            )

        if blueprint.version.schema_version <= 0:
            result.add_error(
                ValidationError(
                    code="BP004",
                    field="version.schema_version",
                    message="Schema version must be greater than zero.",
                )
            )

        # -----------------------------------------------------
        # Metadata
        # -----------------------------------------------------

        if blueprint.metadata.document_count < 0:
            result.add_error(
                ValidationError(
                    code="BP005",
                    field="metadata.document_count",
                    message="Document count cannot be negative.",
                )
            )

        return result