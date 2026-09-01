from __future__ import annotations

from pathlib import Path


class BatchArchetypeCatalogGenerator:
    """
    Generates Archetype Catalogs
    for a batch of Question Possibilities.
    """

    def load_prompt(
        self,
        *,
        qps: list[dict[str, str]],
    ) -> str:

        if not qps:
            raise ValueError(
                "QP batch cannot be empty."
            )

        first = qps[0]

        subject = first["subject"]
        unit = first["unit"]
        chapter = first["chapter"]
        subtopic = first["subtopic"]
        concept_id = first["concept_id"]
        concept = first["concept"]

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

IMPORTANT

The following Question Possibilities
belong to the SAME Concept.

Generate Archetypes for EVERY
Question Possibility.

Do NOT skip any Question Possibility.

Every supplied Question Possibility
must appear in the output.

Every supplied QP ID must appear
in at least one output record.

Return flat JSON records only.

Every Archetype record must
contain its originating qp_id.

Do NOT group, nest, or aggregate
Archetypes under a Question
Possibility.

IMPORTANT DISCOVERY RULES

Process each Question Possibility
independently.

Fully exhaust the Archetype space
for one Question Possibility before
moving to the next Question
Possibility.

Do NOT balance output across
Question Possibilities.

Do NOT generate an equal number
of Archetypes for all Question
Possibilities.

Different Question Possibilities may
have different Archetype counts.

Some Question Possibilities may
require significantly more
Archetypes than others.

The number of Archetypes is
determined solely by the size of the
Archetype space of that Question
Possibility.

Do NOT stop Archetype discovery
early merely because multiple
Question Possibilities were supplied.

For every Question Possibility,
discover the COMPLETE Archetype
space exactly as you would if that
Question Possibility were processed
alone in a dedicated API call.

IMPORTANT JEE FILTER

Generate ONLY JEE-worthy Archetypes.

An Archetype must represent a
distinct reasoning pathway.

Do NOT create Archetypes that differ
only by presentation format.

The following alone do NOT qualify
as distinct Archetypes:

• Table interpretation
• Graph interpretation
• Bar chart interpretation
• Line chart interpretation
• Diagram interpretation
• Data formatting variations
• Information layout variations

Such variants belong to the same
Archetype unless the underlying
reasoning pathway changes.

Prefer Archetypes requiring:

• Inference
• Deduction
• Comparison
• Ranking
• Constraint analysis
• Consistency validation
• Multi-step reasoning
• Multi-condition evaluation
• Reverse reasoning
• Exception identification

Reject Archetypes that can be solved
through direct recall alone.

Prefer fewer high-quality JEE
Archetypes over many shallow
assessment-format Archetypes.

QUESTION POSSIBILITIES
"""

        for row in qps:

            prompt += f"""

QP ID:
{row["qp_id"]}

Question Possibility:
{row["question_possibility"]}

"""

        return prompt