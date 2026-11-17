from __future__ import annotations

from pathlib import Path


class BatchArchetypeCatalogGenerator:
    """Build disposition-aware prompts for batches that may span concepts."""

    def load_prompt(
        self,
        *,
        qps: list[dict[str, str]],
    ) -> str:
        if not qps:
            raise ValueError("QP batch cannot be empty.")

        prompt_file = (
            Path(__file__).parent
            / "prompts"
            / "archetype_catalog_prompt.txt"
        )
        prompt = prompt_file.read_text(encoding="utf-8")

        context_fields = (
            "subject", "unit", "chapter", "subtopic",
            "concept_id", "concept", "qp_id", "question_possibility",
        )
        blocks: list[str] = []
        for index, row in enumerate(qps, start=1):
            missing = [
                field for field in context_fields
                if not isinstance(row.get(field), str) or not row[field].strip()
            ]
            if missing:
                raise ValueError(
                    f"QP row #{index} is missing required source fields: "
                    + ", ".join(missing)
                )
            blocks.append(
                "\n".join(
                    f"{field}: {row[field]}" for field in context_fields
                )
            )

        prompt += """

============================================================
AUTHORITATIVE BATCH CONTRACT — OVERRIDES EARLIER OUTPUT RULES
============================================================

The earlier flat-array output instructions are superseded by
this section. Return exactly one JSON object with exactly two
top-level keys: "qp_dispositions" and "archetypes".

Required shape:

{
  "qp_dispositions": [
    {
      "concept_id": "exact source concept_id",
      "qp_id": "exact supplied QP ID",
      "disposition": "ELIGIBLE | FOUNDATION_ONLY | OUT_OF_SCOPE | REQUIRES_REVIEW",
      "rationale": "Specific academic reason for this decision"
    }
  ],
  "archetypes": []
}

Classify EVERY supplied QP exactly once, using the composite identity
(concept_id, qp_id). QP IDs may repeat under different concepts.

Disposition meanings:
- ELIGIBLE: one or more genuinely distinct, in-scope JEE archetypes exist.
- FOUNDATION_ONLY: useful prerequisite/foundation learning, but no standalone
  JEE archetype is justified for this QP.
- OUT_OF_SCOPE: this QP does not belong in the active manufacturing scope.
- REQUIRES_REVIEW: source or academic evidence is insufficient for a decision.

Only ELIGIBLE QPs may have archetype records. Every ELIGIBLE QP must have
at least one archetype. All other dispositions must have zero archetypes.
An empty "archetypes" array is valid when no QP is ELIGIBLE.
Do not fabricate a shallow archetype to satisfy coverage.

Each archetype record must retain the complete established archetype fields:
subject, unit, chapter, subtopic, concept_id, concept, qp_id,
question_possibility, archetype_id, archetype, assessment_mechanism,
reasoning_path, exam_fit, difficulty_potential, variation_capacity,
variation_dimensions. Copy all source context exactly from the matching
QP record below. Never copy context from another QP in the same batch.
Set archetype_id to "". Do not add approval or manufacturing permissions.

The "qp_dispositions" array is the coverage record. Archetype presence is
NOT the coverage record. Do not omit a QP even when it has no archetype.

Return valid JSON only. No markdown or code fences.

SOURCE QUESTION POSSIBILITIES
Each numbered block is an independent source record. Concepts may differ.

"""
        for index, block in enumerate(blocks, start=1):
            prompt += f"\n--- SOURCE QP {index} ---\n{block}\n"

        return prompt
