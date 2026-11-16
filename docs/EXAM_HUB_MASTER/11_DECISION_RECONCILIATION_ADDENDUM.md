# Decision Reconciliation Addendum

## Authority hierarchy
1. Explicit user-approved project decisions and frozen architecture.
2. Latest versioned approved blueprint/catalog specification.
3. Current generation prompt and runtime specification.
4. Repository implementation (evidence of current behavior, not authority to silently redefine design).
5. Historical logs and generated artifacts.

AMA v1.0 remains the intended high-level architecture. Current repository conformance is partial.

## Reconciled positions

### R01–R12
Engine/prompts/master/05_blueprint_rules.md is the current working generation-quality rule text: Concept First through Production Readiness. Blueprint/01_RULES.md is a different legacy runtime/continuity rule set. Do not combine or reuse the same IDs across both. A versioned Blueprint v1.5 file was not located; the prompt file is a provisional working source, not proof of the complete v1.5 freeze.

### Distractor taxonomy
Engine/prompts/master/06_distractor_engineering.md is the repository's current working source: DE-01 DR01–DR10 and DE-02 quality rules. Keep the historical DR01–DR07 registry as history; do not merge the taxonomies.

### Archetypes
AR17–AR20 in Blueprint/02_ARCHETYPES.md are archetype patterns, not validation rules.

### Difficulty
Preserve S1 Foundation, S2 Easy+, S3 Medium, S4 Hard, S5 Elite. The current R03 validator accepts Easy, Easy+, Medium, Hard and Elite. The older Medium+ text should not silently replace the agreed set mapping.

### Curriculum
Supabase remains master data source; repo CSVs are snapshots. The default CLI registry's in-memory Physics sample is an implementation gap, not a new data-source decision.

### U1 assets
Preserve legacy U1 QPC and chapter-level QP/archetype data. Map concepts, QPs and archetypes to new subtopic-scoped identifiers without recycling stable IDs.

### Repair and coverage
Required behavior remains automatic validation, repair-before-expand, validation restart at R01, bounded iterative rebuild and export only after quality and coverage gates pass. Current implementation does not yet demonstrate this full behavior.

### CSV
The target remains a simplified CSV retaining subject_id and excluding unnecessary empty fields. Current 29-column exporter is legacy; reconcile against Supabase import contract before changing it.

### Branch baseline
Use main at 2a253dc as the audit baseline. Keep recovery-test separate until its code divergence and raw-response logging are reviewed.

## Priority order
P0: canonical blueprint/rule namespace; wire full curriculum into CLI; fix full-scope archetype lookup; migrate U1 legacy assets.  
P1: complete validation registry; bounded repair/rebuild; 100% coverage gate; simplified CSV contract.  
P2: reconcile Mathematics U1–U15 curriculum; review recovery-test; run clean-checkout verification.

## Preservation rules
Do not delete legacy U1 data. Preserve stable question/concept/QP/archetype IDs. Do not rewrite completed modules merely to align version labels. Keep internal audits/repairs automatic and bounded. Do not export unvalidated or incomplete batches. This addendum does not authorize source-code changes.