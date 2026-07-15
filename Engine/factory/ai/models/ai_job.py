"""
Question Factory OS v2.1

Factory AI Job

Represents one AI manufacturing job.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class AIJob:
    """
    Represents one AI execution request.
    """

    job_type: str

    system_prompt: str

    user_prompt: str

    response_schema: str

    temperature: float = 0.2

    max_tokens: int = 4096

    metadata: Dict[str, Any] = field(default_factory=dict)
    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store metadata associated with this
        AI job.
        """

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve metadata.
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
        Determine whether metadata exists.
        """

        return key in self.metadata

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def set_temperature(
        self,
        value: float,
    ) -> None:
        """
        Update model temperature.
        """

        self.temperature = value

    def set_max_tokens(
        self,
        value: int,
    ) -> None:
        """
        Update token limit.
        """

        self.max_tokens = value

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
    ) -> None:
        """
        Validate the AI job configuration.

        Raises
        ------
        ValueError
            If configuration is invalid.
        """

        if not self.job_type.strip():

            raise ValueError("Job type cannot be empty.")

        if not self.system_prompt.strip():

            raise ValueError("System prompt cannot be empty.")

        if not self.user_prompt.strip():

            raise ValueError("User prompt cannot be empty.")

        if self.temperature < 0:

            raise ValueError("Temperature cannot be negative.")

        if self.max_tokens <= 0:

            raise ValueError("Maximum tokens must be greater " "than zero.")

    # ---------------------------------------------------------
    # Execution Information
    # ---------------------------------------------------------

    def execution_information(
        self,
    ) -> Dict[str, Any]:
        """
        Return execution information for
        this AI job.
        """

        return {
            "job_type": self.job_type,
            "response_schema": (self.response_schema),
            "temperature": (self.temperature),
            "max_tokens": (self.max_tokens),
        }

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, Any]:
        """
        Return AI job statistics.
        """

        return {
            "metadata_entries": (len(self.metadata)),
            "system_prompt_length": (len(self.system_prompt)),
            "user_prompt_length": (len(self.user_prompt)),
            "total_prompt_length": (len(self.system_prompt) + len(self.user_prompt)),
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
    ) -> Dict[str, Any]:
        """
        Return complete diagnostics for
        this AI job.
        """

        return {
            "execution": (self.execution_information()),
            "statistics": (self.statistics()),
            "metadata": (dict(self.metadata)),
        }

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> Dict[str, Any]:
        """
        Return AI job health information.
        """

        return {
            "component": "AI Job",
            "status": "READY",
            "job_type": (self.job_type),
            "configuration_valid": (True),
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(
        self,
    ) -> Dict[str, bool]:
        """
        Describe AI job capabilities.
        """

        return {
            "metadata": True,
            "validation": True,
            "diagnostics": True,
            "execution_information": True,
            "statistics": True,
            "health_reporting": True,
        }

    # ---------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------

    def reset_metadata(
        self,
    ) -> None:
        """
        Remove all metadata entries.
        """

        self.metadata.clear()

    def clone(
        self,
    ) -> "AIJob":
        """
        Create a shallow copy of this AI job.

        Metadata is copied so the cloned job
        can be modified independently.
        """

        return AIJob(
            job_type=self.job_type,
            system_prompt=self.system_prompt,
            user_prompt=self.user_prompt,
            response_schema=self.response_schema,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            metadata=dict(self.metadata),
        )

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(
        self,
    ) -> Dict[str, Any]:
        """
        Convert the AI job into a dictionary.
        """

        return {
            "job_type": self.job_type,
            "system_prompt": (self.system_prompt),
            "user_prompt": (self.user_prompt),
            "response_schema": (self.response_schema),
            "temperature": (self.temperature),
            "max_tokens": (self.max_tokens),
            "metadata": (dict(self.metadata)),
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
            job_type=data["job_type"],
            system_prompt=data["system_prompt"],
            user_prompt=data["user_prompt"],
            response_schema=data["response_schema"],
            temperature=data.get(
                "temperature",
                0.2,
            ),
            max_tokens=data.get(
                "max_tokens",
                4096,
            ),
            metadata=dict(
                data.get(
                    "metadata",
                    {},
                )
            ),
        )

    # ---------------------------------------------------------
    # Convenience Methods
    # ---------------------------------------------------------

    @property
    def prompt(
        self,
    ) -> str:
        """
        Return the complete prompt.

        This is intended for AI clients that
        expect a single prompt string.
        """

        return self.system_prompt + "\n\n" + self.user_prompt

    @property
    def prompt_length(
        self,
    ) -> int:
        """
        Return the combined prompt length.
        """

        return len(self.prompt)

    # ---------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------

    def reset_metadata(
        self,
    ) -> None:
        """
        Remove all metadata entries.
        """

        self.metadata.clear()

    def clone(
        self,
    ) -> "AIJob":
        """
        Create a shallow copy of this AI job.

        Metadata is copied so the cloned job
        can be modified independently.
        """

        return AIJob(
            job_type=self.job_type,
            system_prompt=self.system_prompt,
            user_prompt=self.user_prompt,
            response_schema=self.response_schema,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            metadata=dict(self.metadata),
        )

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(
        self,
    ) -> Dict[str, Any]:
        """
        Convert the AI job into a dictionary.
        """

        return {
            "job_type": self.job_type,
            "system_prompt": (self.system_prompt),
            "user_prompt": (self.user_prompt),
            "response_schema": (self.response_schema),
            "temperature": (self.temperature),
            "max_tokens": (self.max_tokens),
            "metadata": (dict(self.metadata)),
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
            job_type=data["job_type"],
            system_prompt=data["system_prompt"],
            user_prompt=data["user_prompt"],
            response_schema=data["response_schema"],
            temperature=data.get(
                "temperature",
                0.2,
            ),
            max_tokens=data.get(
                "max_tokens",
                4096,
            ),
            metadata=dict(
                data.get(
                    "metadata",
                    {},
                )
            ),
        )

    # ---------------------------------------------------------
    # Convenience Methods
    # ---------------------------------------------------------

    @property
    def prompt(
        self,
    ) -> str:
        """
        Return the complete prompt.

        This is intended for AI clients that
        expect a single prompt string.
        """

        return self.system_prompt + "\n\n" + self.user_prompt

    @property
    def prompt_length(
        self,
    ) -> int:
        """
        Return the combined prompt length.
        """

        return len(self.prompt)
