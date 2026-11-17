from __future__ import annotations

from pathlib import Path


class BatchArchetypeCatalogGenerator:
    """Build prompts for disposition-aware batches of QPs."""

    def load_prompt(
        self,
        *,
        qps: list[dict[str, str]],
    ) -> str:
        if not qps:
            raise ValueError("QP batch cannot be empty.")

        first = qps[0]
        context_fields = (
            "subject", "unit", "chapter", "subtopic", "concept_id", "concept",
        )
        for row in qps:
            for field in context_fields:
                if row.get(field) != first.get(field):
                    raise ValueError(
                        "A batch must contain QPs from one consistent "
                        f"catalogue context; mismatch in '{field}'."
                    )

        prompt_file = (
            Path(__file__).parent
            / "prompts"
            / "archetype_catalog_prompt.txt"
        )
        prompt = prompt_file.read_text(encoding="utf-8")

        qp_context = "\n\n".join(
            f"QP ID: {row['qp_id']}\n"
            f"Question Possibility: {row['question_possibility']}"
            for row in qps
        )

        prompt += f"""

============================================================
AUTHORITATIVE BATCH CONTRACT — OVERRIDES EARLIER OUTPUT RULES
============================================================

The earlier flat-array output instructions are superseded by
this section. Return exactly one JSON object with exactly two
top-level keys: "qp_dispositions" and "archetypes".

Required shape:

{{
  "qp_dispositions": [
    {{
      "concept_id": "{first['concept_id']}",
      "qp_id": "exact supplied QP ID",
      "disposition": "ELIGIBLE | FOUNDATION_ONLY | OUT_OF_SCOPE | REQUIRES_REVIEW",
      "rationale": "Specific academic reason for this decision"
    }}
  ],
  "archetypes": []
}}

Classify EVERY supplied QP exactly once.

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
variation_dimensions. Copy all source context exactly. Set archetype_id to "".
Do not add approval or manufacturing permissions.

The "qp_dispositions" array is the coverage record. Archetype presence is
NOT the coverage record. Do not omit a QP even when it has no archetype.

Return valid JSON only. No markdown or code fences.

SOURCE CONTEXT
Subject: {first['subject']}
Unit: {first['unit']}
Chapter: {first['chapter']}
Subtopic: {first['subtopic']}
Concept ID: {first['concept_id']}
Concept: {first['concept']}

QUESTION POSSIBILITIES
{qp_context}
"""
        return prompt
