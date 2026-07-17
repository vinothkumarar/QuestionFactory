"""
Question Factory OS
Metadata Enricher

Milestone : M11
Sprint    : Hardening
Release   : R1
"""

from typing import Any

from Engine.metadata.metadata_loader import MetadataLoader


class MetadataEnricher:
    def __init__(self) -> None:
        self.metadata_loader = MetadataLoader()

    def apply(
        self,
        question: dict[str, Any],
        runtime: dict[str, Any],
    ) -> dict[str, Any]:
        metadata_key = (
            f"{runtime['current_project']}_"
            f"{runtime['current_chapter']}_"
            f"{runtime['current_subtopic']}"
        )

        metadata = self.metadata_loader.get_metadata(metadata_key)

        if metadata is None:
            raise RuntimeError(f"Metadata not found for {metadata_key}")

        #
        # Apply metadata from repository
        #

        question.update(metadata)

        #
        # Runtime controlled values
        #

        question["subject_name"] = runtime.get(
            "current_subject",
            question.get("subject_name"),
        )

        question["unit_name"] = runtime.get(
            "current_unit",
            question.get("unit_name"),
        )

        question["chapter_name"] = runtime.get(
            "current_chapter",
            question.get("chapter_name"),
        )

        question["subtopic_name"] = runtime.get(
            "current_subtopic",
            question.get("subtopic_name"),
        )

        question["language"] = "English"
        question["marks"] = 4
        question["negative_marks"] = -1
        question["status"] = "Draft"
        question["version"] = "1.0"

        return question
        