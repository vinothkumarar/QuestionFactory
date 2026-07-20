"""
Question Factory OS v2.0

Generated Question Model

Represents a single manufactured question.

This model is the canonical in-memory representation
used throughout the manufacturing pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(slots=True)
class GeneratedQuestionModel:
    """
    Represents one generated question.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    question_code: str = ""

    # ---------------------------------------------------------
    # Academic Information
    # ---------------------------------------------------------

    unit_code: str = ""

    chapter_code: str = ""

    subtopic_code: str = ""

    set_number: int = 1

    batch_number: int = 1

    # ---------------------------------------------------------
    # Question
    # ---------------------------------------------------------

    question_text: str = ""

    options: List[str] = field(default_factory=list)

    correct_option: str = ""

    explanation: str = ""

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    difficulty: str = ""

    archetype: str = ""

    concept: str = ""

    tags: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)
    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> Dict:
        """
        Convert the model into a dictionary.
        """

        return {
            "question_code": self.question_code,
            "unit_code": self.unit_code,
            "chapter_code": self.chapter_code,
            "subtopic_code": self.subtopic_code,
            "set_number": self.set_number,
            "batch_number": self.batch_number,
            "question_text": self.question_text,
            "options": list(self.options),
            "correct_option": self.correct_option,
            "explanation": self.explanation,
            "difficulty": self.difficulty,
            "archetype": self.archetype,
            "concept": self.concept,
            "tags": list(self.tags),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(
        cls,
        data: Dict,
    ) -> "GeneratedQuestionModel":
        """
        Create a model from a dictionary.
        """

        return cls(
            question_code=data.get(
                "question_code",
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
            question_text=data.get(
                "question_text",
                "",
            ),
            options=list(
                data.get(
                    "options",
                    [],
                )
            ),
            correct_option=data.get(
                "correct_option",
                "",
            ),
            explanation=data.get(
                "explanation",
                "",
            ),
            difficulty=data.get(
                "difficulty",
                "",
            ),
            archetype=data.get(
                "archetype",
                "",
            ),
            concept=data.get(
                "concept",
                "",
            ),
            tags=list(
                data.get(
                    "tags",
                    [],
                )
            ),
            metadata=dict(
                data.get(
                    "metadata",
                    {},
                )
            ),
        )

    # ---------------------------------------------------------
    # Copy Support
    # ---------------------------------------------------------

    def copy(
        self,
    ) -> "GeneratedQuestionModel":
        """
        Create a deep copy of this model.
        """

        return GeneratedQuestionModel.from_dict(self.to_dict())

    def to_export_dict(self) -> Dict:
        """
        Convert the question into the canonical CSV
        export schema used by Question Factory.
        """

        options = list(self.options)

        while len(options) < 4:
            options.append("")

        metadata = dict(self.metadata)

        return {
            # -------------------------------------------------
            # Foreign Keys
            # -------------------------------------------------
            "subject_id": metadata.get("subject_id", ""),
            "chapter_id": self.chapter_code,
            "unit_id": self.unit_code,
            "subtopic_id": self.subtopic_code,

            # -------------------------------------------------
            # AI Generated Content
            # -------------------------------------------------
            "difficulty": self.difficulty,
            "question_type": metadata.get(
                "question_type",
                "MCQ",
            ),
            "question_text": self.question_text,

            "option_a": options[0],
            "option_b": options[1],
            "option_c": options[2],
            "option_d": options[3],

            "answer": self.correct_option,
            "explanation": self.explanation,
            "more_explanation": metadata.get(
                "more_explanation",
                "",
            ),

            "correct_option": self.correct_option,

            "difficulty_score": metadata.get(
                "difficulty_score",
                "",
            ),

            "answer_type": metadata.get(
                "answer_type",
                "single",
            ),

            "concept_tested": self.concept,
            "question_archetype": self.archetype,

            "exam_level": metadata.get(
                "exam_level",
                "",
            ),

            "source_type": metadata.get(
                "source_type",
                "AI",
            ),

            "tags": ",".join(self.tags),

            "estimated_time_sec": metadata.get(
                "estimated_time_sec",
                "",
            ),

            "marks": metadata.get(
                "marks",
                "",
            ),

            "negative_marks": metadata.get(
                "negative_marks",
                "",
            ),

            "bloom_level": metadata.get(
                "bloom_level",
                "",
            ),

            "chapter_weightage": metadata.get(
                "chapter_weightage",
                "",
            ),

            "exam_relevance": metadata.get(
                "exam_relevance",
                "",
            ),

            "pyq_inspired": metadata.get(
                "pyq_inspired",
                "",
            ),

            "pyq_exam": metadata.get(
                "pyq_exam",
                "",
            ),

            "pyq_year": metadata.get(
                "pyq_year",
                "",
            ),

            "pyq_topic": metadata.get(
                "pyq_topic",
                "",
            ),

            "status": metadata.get(
                "status",
                "ACTIVE",
            ),

            "version": metadata.get(
                "version",
                "1.0",
            ),

            "is_verified": metadata.get(
                "is_verified",
                False,
            ),

            "reviewed_by": metadata.get(
                "reviewed_by",
                "",
            ),

            "review_date": metadata.get(
                "review_date",
                "",
            ),

            "image_required": metadata.get(
                "image_required",
                False,
            ),

            "has_diagram": metadata.get(
                "has_diagram",
                False,
            ),

            "latex_required": metadata.get(
                "latex_required",
                False,
            ),

            "language": metadata.get(
                "language",
                "English",
            ),

            "question_image_url": metadata.get(
                "question_image_url",
                "",
            ),

            "solution_image_url": metadata.get(
                "solution_image_url",
                "",
            ),

            # -------------------------------------------------
            # Factory Metadata
            # -------------------------------------------------
            "question_code": self.question_code,

            "subject_name": metadata.get(
                "subject_name",
                "",
            ),

            "unit_name": metadata.get(
                "unit_name",
                "",
            ),

            "chapter_name": metadata.get(
                "chapter_name",
                "",
            ),

            "subtopic_name": metadata.get(
                "subtopic_name",
                "",
            ),

            "set_no": self.set_number,
        }

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

    # State Inspection
    # ---------------------------------------------------------

    def is_complete(self) -> bool:
        """
        Determine whether the question contains the
        minimum required information.

        This is a structural check only. It does not
        perform academic validation.
        """

        return (
            bool(self.question_text.strip())
            and len(self.options) >= 2
            and bool(self.correct_option.strip())
        )

    def is_empty(self) -> bool:
        """
        Determine whether the question contains
        any meaningful content.
        """

        return (
            not self.question_text.strip()
            and len(self.options) == 0
            and not self.correct_option.strip()
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(self) -> Dict:
        """
        Return basic statistics for the question.
        """

        return {
            "option_count": len(self.options),
            "tag_count": len(self.tags),
            "question_length": len(self.question_text),
            "explanation_length": len(self.explanation),
        }

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def option_count(self) -> int:
        """
        Number of answer options.
        """

        return len(self.options)

    @property
    def tag_count(self) -> int:
        """
        Number of tags.
        """

        return len(self.tags)

    @property
    def has_explanation(self) -> bool:
        """
        Determine whether an explanation exists.
        """

        return bool(self.explanation.strip())

    @property
    def has_metadata(self) -> bool:
        """
        Determine whether metadata has been attached.
        """

        return len(self.metadata) > 0

    @property
    def has_tags(self) -> bool:
        """
        Determine whether tags have been assigned.
        """

        return len(self.tags) > 0
        # ---------------------------------------------------------

    # Summary
    # ---------------------------------------------------------

    def summary(self) -> Dict:
        """
        Return a concise summary of the question.
        """

        return {
            "question_code": self.question_code,
            "unit_code": self.unit_code,
            "chapter_code": self.chapter_code,
            "subtopic_code": self.subtopic_code,
            "difficulty": self.difficulty,
            "option_count": self.option_count,
            "complete": self.is_complete(),
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(self) -> Dict:
        """
        Return detailed diagnostics for the question.
        """

        return {
            "summary": self.summary(),
            "statistics": self.statistics(),
            "metadata": dict(self.metadata),
            "tags": list(self.tags),
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

        return "Generated Question Model"

    def health(self) -> Dict:
        """
        Return model health information.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "complete": self.is_complete(),
            "status": ("READY" if self.is_complete() else "INCOMPLETE"),
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(self) -> Dict:
        """
        Describe model capabilities.
        """

        return {
            "serialization": True,
            "copy_support": True,
            "metadata": True,
            "tags": True,
            "statistics": True,
            "diagnostics": True,
            "summary": True,
            "state_inspection": True,
        }

    # ---------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------

    def clear_metadata(self) -> None:
        """
        Remove all metadata entries.
        """

        self.metadata.clear()

    def clear_tags(self) -> None:
        """
        Remove all assigned tags.
        """

        self.tags.clear()
        # ---------------------------------------------------------

    # Utility Methods
    # ---------------------------------------------------------

    def reset(self) -> None:
        """
        Reset the model to its default state.
        """

        self.question_code = ""

        self.unit_code = ""
        self.chapter_code = ""
        self.subtopic_code = ""

        self.set_number = 1
        self.batch_number = 1

        self.question_text = ""

        self.options.clear()

        self.correct_option = ""

        self.explanation = ""

        self.difficulty = ""

        self.archetype = ""

        self.concept = ""

        self.tags.clear()

        self.metadata.clear()

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "GeneratedQuestionModel("
            f"question_code='{self.question_code}', "
            f"difficulty='{self.difficulty}')"
        )

    def __str__(self) -> str:

        return (
            f"{self.question_code} | "
            f"{self.unit_code}/{self.chapter_code}/"
            f"{self.subtopic_code}"
        )
