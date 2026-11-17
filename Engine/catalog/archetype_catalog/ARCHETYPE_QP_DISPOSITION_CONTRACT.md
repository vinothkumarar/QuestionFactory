# Archetype Catalogue: QP Disposition Contract

Status: Implemented and CI-validated on 2026-11-17
Scope: Archetype catalogue generation pipeline
Branch: feature/dual-question-engine-v1

## Problem

The current pipeline equates QP coverage with archetype existence:

- The batch prompt says every supplied QP must produce at least one archetype.
- The runner rejects a batch if any supplied QP ID is absent from returned archetype records.
- The runner marks a QP complete by finding at least one archetype record for its (concept_id, qp_id) pair.

This is academically unsafe. A QP may be foundational, outside the active exam scope, invalid, or require review. Such a QP must remain traceable without fabricating an archetype.

## Decision

Separate QP disposition from archetype records. The AI response contract becomes a JSON object with exactly two top-level arrays:

```json
{
  "qp_dispositions": [
    {
      "concept_id": "C001",
      "qp_id": "QP001",
      "disposition": "ELIGIBLE",
      "rationale": "A distinct examination-relevant assessment mechanism exists."
    }
  ],
  "archetypes": []
}
```

Allowed dispositions:

- `ELIGIBLE`: one or more archetypes must be returned for this QP.
- `FOUNDATION_ONLY`: no JEE archetype is justified; retain as prerequisite/foundation material.
- `OUT_OF_SCOPE`: the QP does not belong in the active manufacturing scope.
- `REQUIRES_REVIEW`: evidence or source quality is insufficient for a final decision.

## Invariants

1. Every input QP must have exactly one disposition, identified by the composite key `(concept_id, qp_id)`.
2. Every archetype must reference an input QP with disposition `ELIGIBLE`.
3. Every `ELIGIBLE` QP must have at least one archetype.
4. Every non-eligible disposition must have zero archetypes.
5. An empty archetype array is valid when all QPs are non-eligible.
6. Archetype IDs remain blank in AI output and are assigned by the factory only.
7. Duplicate, missing, or unknown QP keys are hard validation failures.
8. Completion/resume state is based on a persisted disposition for every source QP, not on whether an archetype happens to exist.
9. Existing flat-list catalogues remain readable as legacy data during migration; they must not be silently reinterpreted as fully dispositioned.
10. CSV export contains archetype rows only. QP dispositions are persisted in the JSON catalogue and exported to a dedicated disposition CSV so zero-archetype QPs remain auditable.

## Migration sequence

1. Introduce typed response parsing and validation for the two-array contract.
2. Update the batch prompt to request dispositions first and archetypes only for eligible QPs.
3. Update the runner's resume/completion logic to persist and validate dispositions.
4. Update JSON/CSV persistence: archetype CSV remains archetype-only; add a disposition CSV.
5. Add regression tests for all four dispositions, empty archetype output, missing/duplicate QPs, ineligible-QP archetypes, eligible-QP-without-archetype, and legacy catalogue handling.
6. Keep all manufacturing gates false until the separate academic approval process explicitly enables them.

## Explicit non-goals

- Do not generate questions as part of this migration.
- Do not alter existing QP source catalogues or stable IDs.
- Do not auto-approve archetypes.
- Do not change syllabus/curriculum mappings in this engineering task.

## Acceptance criteria

The pipeline can process a batch in which every QP is classified `FOUNDATION_ONLY` and correctly persist/complete it with zero archetypes. It must also reject any attempt to attach an archetype to a non-eligible QP or omit a QP disposition.


## Implementation record

Implemented in the archetype catalogue subsystem:
- `qp_disposition_contract.py`: strict QP disposition and archetype/source alignment validator.
- `archetype_catalog_ai_client.py`: parses the two-array response and validates archetype metadata.
- `batch_archetype_catalog_generator.py`: emits the authoritative disposition-aware prompt contract.
- `run_all_archetype_catalogs.py`: disposition-based resume, persistence, completion and factory ID assignment.
- `archetype_catalog_csv_exporter.py`: separate archetype and QP-disposition CSV exports.
- Regression tests cover eligible/non-eligible handling, missing/duplicate/unknown QPs, copied metadata integrity and empty archetype output.
- GitHub Actions workflow: `.github/workflows/archetype-catalog-quality.yml`.

CI result for commit `9647bae37ad9d74040fcb4341d35475e156e0bec`:
- Python compile: passed.
- Contract tests: 12 passed.
- Workflow: https://github.com/vinothkumarar/QuestionFactory/actions/runs/44018238267

Production generation has not been run. Existing legacy flat-list catalogues remain preserved and require an explicit migration before resume.
