from __future__ import annotations

from pathlib import Path


class ArchetypeCatalogGenerator:
    """
    Generates an Archetype Catalog
    for a single Question Possibility.
    """

    def load_prompt(
        self,
        *,
        subject: str,
        unit: str,
        chapter: str,
        subtopic: str,
        concept_id: str,
        concept: str,
        qp_id: str,
        question_possibility: str,
    ) -> str:

        prompt_file = (
            Path(__file__).parent
            / "prompts"
            / "archetype_catalog_prompt.txt"
        )

        prompt = prompt_file.read_text(
            encoding="utf-8"
        )

        prompt += f"""

CONTEXT INFORMATION

Subject:
{subject}

Unit:
{unit}

Chapter:
{chapter}

Subtopic:
{subtopic}

Concept ID:
{concept_id}

Concept:
{concept}

QP ID:
{qp_id}

Question Possibility:
{question_possibility}

"""

        return prompt