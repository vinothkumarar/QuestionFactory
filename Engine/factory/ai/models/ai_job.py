"""
Question Factory OS v2.1
------------------------

AI Job Model

Represents a single AI execution request travelling through
the Question Factory AI subsystem.

Responsibilities
----------------
• Carry prompt information
• Carry AI execution configuration
• Carry manufacturing context
• Carry runtime metadata
• Support validation and serialization

This model is provider-agnostic and immutable in structure,
while allowing controlled mutation of execution metadata.

Author:
Question Factory OS
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from typing import Any
from typing import Dict
from typing import Optional


# ----------------------------------------------------------------------
# AI Job
# ----------------------------------------------------------------------


@dataclass(slots=True)
class AIJob:
    """
    Represents a single AI execution request.

    This object is exchanged between the Manufacturing Layer
    and the AI Layer.
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    job_id: str = ""

    request_id: str = ""

    project: str = ""

    job_type: str = ""

    # ------------------------------------------------------------------
    # Prompt Information
    # ------------------------------------------------------------------

    system_prompt: str = ""

    user_prompt: str = ""

    response_schema: str = ""

    # ------------------------------------------------------------------
    # AI Configuration
    # ------------------------------------------------------------------

    temperature: float = 0.2

    max_tokens: int = 4096

    # ------------------------------------------------------------------
    # Manufacturing Context
    # ------------------------------------------------------------------

    subject: str = ""

    chapter: str = ""

    subtopic: str = ""

    difficulty: str = ""

    batch: str = ""

    question_count: int = 1

    blueprint: str = ""

    # ------------------------------------------------------------------
    # Runtime Metadata
    # ------------------------------------------------------------------

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # ------------------------------------------------------------------
    # Metadata Management
    # ------------------------------------------------------------------

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store runtime metadata.
        """

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve runtime metadata.
        """

        return self.metadata.get(
            key,
            default,
        )

    def has_metadata(
        self,
        key: str,
    ) -> bool:
        """
        Return True if a metadata key exists.
        """

        return key in self.metadata

    def reset_metadata(
        self,
    ) -> None:
        """
        Remove every metadata entry.
        """

        self.metadata.clear()
    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def set_temperature(
        self,
        value: float,
    ) -> None:
        """
        Update the model temperature.
        """

        self.temperature = value

    def set_max_tokens(
        self,
        value: int,
    ) -> None:
        """
        Update the maximum token limit.
        """

        self.max_tokens = value

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(
        self,
    ) -> None:
        """
        Validate the AI job configuration.

        Raises
        ------
        ValueError
            If the job configuration is invalid.
        """

        if not self.job_type.strip():
            raise ValueError(
                "Job type cannot be empty."
            )

        if not self.system_prompt.strip():
            raise ValueError(
                "System prompt cannot be empty."
            )

        if not self.user_prompt.strip():
            raise ValueError(
                "User prompt cannot be empty."
            )

        if self.temperature < 0.0:
            raise ValueError(
                "Temperature cannot be negative."
            )

        if self.temperature > 2.0:
            raise ValueError(
                "Temperature cannot exceed 2.0."
            )

        if self.max_tokens <= 0:
            raise ValueError(
                "Maximum tokens must be greater than zero."
            )

        if self.question_count <= 0:
            raise ValueError(
                "Question count must be greater than zero."
            )

    @property
    def is_valid(
        self,
    ) -> bool:
        """
        Return True if the job configuration is valid.
        """

        try:
            self.validate()
            return True
        except ValueError:
            return False

    # ------------------------------------------------------------------
    # Execution Information
    # ------------------------------------------------------------------

    def execution_information(
        self,
    ) -> Dict[str, Any]:
        """
        Return execution information for this job.
        """

        return {
            "job_id": self.job_id,
            "request_id": self.request_id,
            "project": self.project,
            "job_type": self.job_type,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "response_schema": self.response_schema,
        }

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, Any]:
        """
        Return AI job statistics.
        """

        return {
            "metadata_entries": len(self.metadata),
            "system_prompt_length": len(
                self.system_prompt
            ),
            "user_prompt_length": len(
                self.user_prompt
            ),
            "total_prompt_length": (
                len(self.system_prompt)
                + len(self.user_prompt)
            ),
            "question_count": self.question_count,
        }

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def diagnostics(
        self,
    ) -> Dict[str, Any]:
        """
        Return complete diagnostics.
        """

        return {
            "execution": self.execution_information(),
            "statistics": self.statistics(),
            "metadata": dict(self.metadata),
            "valid": self.is_valid,
        }
    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    def health(
        self,
    ) -> Dict[str, Any]:
        """
        Return AI job health information.
        """

        return {
            "component": "AIJob",
            "status": "READY" if self.is_valid else "INVALID",
            "job_id": self.job_id,
            "job_type": self.job_type,
            "configuration_valid": self.is_valid,
        }

    # ------------------------------------------------------------------
    # Capabilities
    # ------------------------------------------------------------------

    def capabilities(
        self,
    ) -> Dict[str, bool]:
        """
        Return the capabilities supported by this model.
        """

        return {
            "metadata": True,
            "validation": True,
            "serialization": True,
            "cloning": True,
            "diagnostics": True,
            "manufacturing_context": True,
        }

    # ------------------------------------------------------------------
    # Copy
    # ------------------------------------------------------------------

    def clone(
        self,
    ) -> "AIJob":
        """
        Create a shallow copy of the AI job.

        Runtime metadata is copied so the cloned
        instance can be modified independently.
        """

        return AIJob(
            job_id=self.job_id,
            request_id=self.request_id,
            project=self.project,
            job_type=self.job_type,
            system_prompt=self.system_prompt,
            user_prompt=self.user_prompt,
            response_schema=self.response_schema,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            subject=self.subject,
            chapter=self.chapter,
            subtopic=self.subtopic,
            difficulty=self.difficulty,
            batch=self.batch,
            question_count=self.question_count,
            blueprint=self.blueprint,
            metadata=dict(self.metadata),
        )

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(
        self,
    ) -> Dict[str, Any]:
        """
        Convert this AI job into a serializable dictionary.
        """

        return {
            "job_id": self.job_id,
            "request_id": self.request_id,
            "project": self.project,
            "job_type": self.job_type,
            "system_prompt": self.system_prompt,
            "user_prompt": self.user_prompt,
            "response_schema": self.response_schema,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "subject": self.subject,
            "chapter": self.chapter,
            "subtopic": self.subtopic,
            "difficulty": self.difficulty,
            "batch": self.batch,
            "question_count": self.question_count,
            "blueprint": self.blueprint,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "AIJob":
        """
        Construct an AIJob from a dictionary.
        """

        return cls(
            job_id=data.get(
                "job_id",
                "",
            ),
            request_id=data.get(
                "request_id",
                "",
            ),
            project=data.get(
                "project",
                "",
            ),
            job_type=data.get(
                "job_type",
                "",
            ),
            system_prompt=data.get(
                "system_prompt",
                "",
            ),
            user_prompt=data.get(
                "user_prompt",
                "",
            ),
            response_schema=data.get(
                "response_schema",
                "",
            ),
            temperature=data.get(
                "temperature",
                0.2,
            ),
            max_tokens=data.get(
                "max_tokens",
                4096,
            ),
            subject=data.get(
                "subject",
                "",
            ),
            chapter=data.get(
                "chapter",
                "",
            ),
            subtopic=data.get(
                "subtopic",
                "",
            ),
            difficulty=data.get(
                "difficulty",
                "",
            ),
            batch=data.get(
                "batch",
                "",
            ),
            question_count=data.get(
                "question_count",
                1,
            ),
            blueprint=data.get(
                "blueprint",
                "",
            ),
            metadata=dict(
                data.get(
                    "metadata",
                    {},
                )
            ),
        )
    # ------------------------------------------------------------------
    # Convenience Properties
    # ------------------------------------------------------------------

    @property
    def prompt(
        self,
    ) -> str:
        """
        Return the complete prompt.

        Intended for AI providers that expect a single
        prompt string.
        """

        if not self.system_prompt:
            return self.user_prompt

        return (
            f"{self.system_prompt}\n\n"
            f"{self.user_prompt}"
        )

    @property
    def prompt_length(
        self,
    ) -> int:
        """
        Return the combined prompt length.
        """

        return len(self.prompt)

    @property
    def has_system_prompt(
        self,
    ) -> bool:
        """
        Return True if a system prompt exists.
        """

        return bool(self.system_prompt.strip())

    

    # ------------------------------------------------------------------
    # Manufacturing Context
    # ------------------------------------------------------------------

    def manufacturing_context(
        self,
    ) -> Dict[str, Any]:
        """
        Return the manufacturing context associated
        with this AI job.
        """

        return {
            "project": self.project,
            "subject": self.subject,
            "chapter": self.chapter,
            "subtopic": self.subtopic,
            "difficulty": self.difficulty,
            "batch": self.batch,
            "question_count": self.question_count,
            "blueprint": self.blueprint,
        }

    def has_manufacturing_context(
        self,
    ) -> bool:
        """
        Return True if any manufacturing context
        has been supplied.
        """

        return any(
            (
                self.project,
                self.subject,
                self.chapter,
                self.subtopic,
                self.batch,
                self.blueprint,
            )
        )

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summary(
        self,
    ) -> Dict[str, Any]:
        """
        Return a concise summary suitable for logging.
        """

        return {
            "job_id": self.job_id,
            "request_id": self.request_id,
            "job_type": self.job_type,
            "project": self.project,
            "subject": self.subject,
            "chapter": self.chapter,
            "subtopic": self.subtopic,
            "difficulty": self.difficulty,
            "question_count": self.question_count,
            "prompt_length": self.prompt_length,
        }

    # ------------------------------------------------------------------
    # Runtime Utilities
    # ------------------------------------------------------------------

    def clear_prompts(
        self,
    ) -> None:
        """
        Remove prompt content while preserving the
        remainder of the job definition.
        """

        self.system_prompt = ""
        self.user_prompt = ""

    def update_prompts(
        self,
        *,
        system_prompt: Optional[str] = None,
        user_prompt: Optional[str] = None,
    ) -> None:
        """
        Update one or both prompts.
        """

        if system_prompt is not None:
            self.system_prompt = system_prompt

        if user_prompt is not None:
            self.user_prompt = user_prompt
# ----------------------------------------------------------------------
# Factory Helper
# ----------------------------------------------------------------------

def create_ai_job(
    *,
    job_type: str,
    system_prompt: str,
    user_prompt: str,
    response_schema: str,
    temperature: float = 0.2,
    max_tokens: int = 4096,
    job_id: str = "",
    request_id: str = "",
    project: str = "",
    subject: str = "",
    chapter: str = "",
    subtopic: str = "",
    difficulty: str = "",
    batch: str = "",
    question_count: int = 1,
    blueprint: str = "",
    metadata: Optional[Dict[str, Any]] = None,
) -> AIJob:
    """
    Factory helper for creating an AIJob.

    This helper provides a stable construction point for the
    AI subsystem and avoids mutable default arguments.
    """

    return AIJob(
        job_id=job_id,
        request_id=request_id,
        project=project,
        job_type=job_type,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_schema=response_schema,
        temperature=temperature,
        max_tokens=max_tokens,
        subject=subject,
        chapter=chapter,
        subtopic=subtopic,
        difficulty=difficulty,
        batch=batch,
        question_count=question_count,
        blueprint=blueprint,
        metadata=dict(metadata or {}),
    )


# ----------------------------------------------------------------------
# Module Exports
# ----------------------------------------------------------------------

__all__ = [
    "AIJob",
    "create_ai_job",
]
