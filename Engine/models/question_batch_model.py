"""
Question Factory OS v2.0

Question Batch Model

Represents one manufactured batch.

A batch is the unit exchanged between
Generation, Validation, Repair,
Packaging and Reporting.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from Engine.models.generated_question_model import (
    GeneratedQuestionModel,
)


@dataclass(slots=True)
class QuestionBatchModel:
    """
    Represents one manufacturing batch.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    batch_id: str = ""

    unit_code: str = ""

    chapter_code: str = ""

    subtopic_code: str = ""

    set_number: int = 1

    batch_number: int = 1

    # ---------------------------------------------------------
    # Questions
    # ---------------------------------------------------------

    questions: List[
        GeneratedQuestionModel
    ] = field(
        default_factory=list
    )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    metadata: Dict = field(
        default_factory=dict
    )

    status: str = "CREATED"
        # ---------------------------------------------------------
    # Question Management
    # ---------------------------------------------------------

    def add_question(
        self,
        question: GeneratedQuestionModel,
    ) -> None:
        """
        Add a question to the batch.
        """

        self.questions.append(
            question
        )

    def remove_question(
        self,
        question_code: str,
    ) -> bool:
        """
        Remove a question by its code.

        Returns
        -------
        bool
            True if the question was removed.
        """

        for question in self.questions:

            if (
                question.question_code
                == question_code
            ):

                self.questions.remove(
                    question
                )

                return True

        return False

    def get_question(
        self,
        question_code: str,
    ) -> GeneratedQuestionModel | None:
        """
        Return a question by its code.
        """

        for question in self.questions:

            if (
                question.question_code
                == question_code
            ):

                return question

        return None

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> Dict:
        """
        Convert the batch into a dictionary.
        """

        return {
            "batch_id": self.batch_id,
            "unit_code": self.unit_code,
            "chapter_code": self.chapter_code,
            "subtopic_code": self.subtopic_code,
            "set_number": self.set_number,
            "batch_number": self.batch_number,
            "status": self.status,
            "questions": [
                question.to_dict()
                for question in self.questions
            ],
            "metadata": dict(
                self.metadata
            ),
        }

    @classmethod
    def from_dict(
        cls,
        data: Dict,
    ) -> "QuestionBatchModel":
        """
        Create a batch from a dictionary.
        """

        batch = cls(
            batch_id=data.get(
                "batch_id",
                "",
            ),
            unit_code=data.get(
                "unit_code",
                "",
            ),
            chapter_code=data.get(
                "chapter_code",
                "",
            ),
            subtopic_code=data.get(
                "subtopic_code",
                "",
            ),
            set_number=data.get(
                "set_number",
                1,
            ),
            batch_number=data.get(
                "batch_number",
                1,
            ),
            status=data.get(
                "status",
                "CREATED",
            ),
            metadata=dict(
                data.get(
                    "metadata",
                    {},
                )
            ),
        )

        batch.questions = [

            GeneratedQuestionModel.from_dict(
                item
            )

            for item in data.get(
                "questions",
                [],
            )

        ]

        return batch

    # ---------------------------------------------------------
    # Copy Support
    # ---------------------------------------------------------

    def copy(
        self,
    ) -> "QuestionBatchModel":
        """
        Create a deep copy of the batch.
        """

        return QuestionBatchModel.from_dict(
            self.to_dict()
        )
            # ---------------------------------------------------------
    # State Inspection
    # ---------------------------------------------------------

    def is_empty(self) -> bool:
        """
        Determine whether the batch contains
        any questions.
        """

        return len(self.questions) == 0

    def is_complete(self) -> bool:
        """
        Determine whether every question in the
        batch is structurally complete.

        This is a structural check only.
        """

        if self.is_empty():
            return False

        return all(
            question.is_complete()
            for question in self.questions
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(self) -> Dict:
        """
        Return batch statistics.
        """

        complete_questions = sum(
            1
            for question in self.questions
            if question.is_complete()
        )

        return {
            "question_count": len(
                self.questions
            ),
            "complete_questions": (
                complete_questions
            ),
            "incomplete_questions": (
                len(self.questions)
                - complete_questions
            ),
        }

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def question_count(self) -> int:
        """
        Number of questions in the batch.
        """

        return len(self.questions)

    @property
    def has_questions(self) -> bool:
        """
        Determine whether the batch contains
        questions.
        """

        return self.question_count > 0

    @property
    def complete_question_count(self) -> int:
        """
        Number of structurally complete questions.
        """

        return sum(
            1
            for question in self.questions
            if question.is_complete()
        )

    @property
    def incomplete_question_count(self) -> int:
        """
        Number of structurally incomplete questions.
        """

        return (
            self.question_count
            - self.complete_question_count
        )

    # ---------------------------------------------------------
    # Metadata Helpers
    # ---------------------------------------------------------

    def set_metadata(
        self,
        key: str,
        value,
    ) -> None:
        """
        Store a metadata value.
        """

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default=None,
    ):
        """
        Retrieve a metadata value.
        """

        return self.metadata.get(
            key,
            default,
        )
            # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(self) -> Dict:
        """
        Return a concise summary of the batch.
        """

        return {
            "batch_id": self.batch_id,
            "unit_code": self.unit_code,
            "chapter_code": self.chapter_code,
            "subtopic_code": self.subtopic_code,
            "set_number": self.set_number,
            "batch_number": self.batch_number,
            "status": self.status,
            "question_count": self.question_count,
            "complete": self.is_complete(),
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(self) -> Dict:
        """
        Return detailed batch diagnostics.
        """

        return {
            "summary": self.summary(),
            "statistics": self.statistics(),
            "metadata": dict(self.metadata),
        }

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    @property
    def version(self) -> str:
        """
        Model version.
        """

        return "2.0.0"

    @property
    def component_name(self) -> str:
        """
        Component name.
        """

        return "Question Batch Model"

    def health(self) -> Dict:
        """
        Return batch health information.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "status": (
                "READY"
                if self.is_complete()
                else "INCOMPLETE"
            ),
            "question_count": self.question_count,
            "complete_questions": (
                self.complete_question_count
            ),
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(self) -> Dict:
        """
        Describe batch model capabilities.
        """

        return {
            "question_management": True,
            "serialization": True,
            "copy_support": True,
            "statistics": True,
            "diagnostics": True,
            "summary": True,
            "metadata": True,
            "state_inspection": True,
        }

    # ---------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------

    def clear_questions(self) -> None:
        """
        Remove all questions from the batch.
        """

        self.questions.clear()

    def clear_metadata(self) -> None:
        """
        Remove all metadata entries.
        """

        self.metadata.clear()

    def set_status(
        self,
        status: str,
    ) -> None:
        """
        Update the batch status.
        """

        self.status = status
            # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------

    def reset(self) -> None:
        """
        Reset the batch to its default state.
        """

        self.batch_id = ""

        self.unit_code = ""
        self.chapter_code = ""
        self.subtopic_code = ""

        self.set_number = 1
        self.batch_number = 1

        self.questions.clear()

        self.metadata.clear()

        self.status = "CREATED"

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "QuestionBatchModel("
            f"batch_id='{self.batch_id}', "
            f"questions={self.question_count}, "
            f"status='{self.status}')"
        )

    def __str__(self) -> str:

        return (
            f"{self.batch_id} | "
            f"{self.question_count} question(s)"
        )
        