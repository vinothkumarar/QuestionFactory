# P1 Blueprint Authority and Rule Crosswalk Audit

**Audit date:** 2026-11-17  
**Status:** BLOCKED FOR FINAL FREEZE — authoritative frozen v1.5 artifact not recovered  
**Repository branch:** `feature/dual-question-engine-v1`  
**Baseline commit:** `4fe34c92e77c511aabbe1b18f4663714ab74c701`

## 1. Authority finding

The recovered project decisions establish the intended hierarchy:

1. Explicit user-approved decisions and frozen architecture.
2. Latest complete, versioned and approved blueprint.
3. Current generation prompt/runtime specification.
4. Repository implementation (evidence of what is executable, not authority to redefine the blueprint).
5. Historical notes, temporary files and generated artifacts.

The user previously approved the direction to embed the entire frozen Blueprint v1.5. However, the complete signed-off v1.5 document and complete text of its rule families were not found in the inspected repository or recovered Library materials. Historical references to v1.2–v1.5 do not establish the full contents or final version. A previous approval to use v1.5 is not a substitute for the missing authoritative text.

**Decision:** Do not reconstruct or declare a v1.5 freeze from fragments. Retain the current prompt and legacy rule files as separate provisional sources. Do not merge duplicate identifiers.

## 2. Rule namespace collision register

| Namespace/source | Identifier | Recovered definition/scope | Implementation evidence | Test evidence | Status |
|---|---|---|---|---|---|
| Frozen Blueprint v1.5 (approved direction; full artifact missing) | R01–R20 | Full approved definitions not recovered | No authoritative source-to-code map | No authoritative rule test map | BLOCKED |
| Frozen Blueprint v1.5 historical notes | AR-01 | Dynamic Count Rule mentioned in recovered assistant-side history; full text/provenance not recovered | QA001 Question Count exists as metadata; no proven AR-01 link | No direct test | UNVERIFIED |
| Frozen Blueprint v1.5 historical notes | SC-01 | Schema Freeze Rule mentioned; full approved definition not recovered | Versioned schema files exist, but no explicit SC-01 traceability | No direct test | UNVERIFIED |
| `Engine/prompts/master/05_blueprint_rules.md` | R01 | Concept First | No direct R01 code implementation; code R01 means Structural Validator | No dedicated test | CONFLICT |
| Same | R02 | Single Learning Objective | No direct R02 code implementation; code R02 means Academic Validator | No dedicated test | CONFLICT |
| Same | R03 | Mathematical Verification (formulae, calculations, units, dimensions, logic) | Code R03 is Blueprint Validator; no independent mathematical verification path is demonstrated | No dedicated test | CRITICAL GAP |
| Same | R04–R12 | Unique Answer; Explanation Quality; Difficulty Alignment; Language Quality; Examination Authenticity; Originality; Educational Value; Internal Consistency; Production Readiness | Some partial structural/academic/blueprint checks exist, but no explicit complete mapping to these IDs | No dedicated per-rule tests | PROVISIONAL |
| `Blueprint/01_RULES.md` | R01–R12 | Continuity; Difficulty Progression; Strict Verification; Quality; Stable IDs; Internal Rebuild; Coverage Expansion; Archetype Activation; Diversity; Pattern Repetition; Formula Diversity; Saturation Monitoring | RB-01 exists in `Blueprint/04_REBUILD.md`; remaining mappings are not demonstrated as a complete executable rule registry | No dedicated tests for the complete rule set | LEGACY / CONFLICT |
| `Engine/prompts/master/06_distractor_engineering.md` | DE-01 | DR01–DR10: Arithmetic, Sign, Reciprocal, Formula Misapplication, Unit Conversion, Dimensional, Conceptual, Boundary Condition, Approximation and Logical errors | R03's current distractor check only flags distractors shorter than two characters; no semantic misconception classification | No direct tests | PROVISIONAL / PARTIAL |
| Same | DE-02 | Plausibility, educational meaning, closeness where appropriate, non-revealing and non-absurd distractors | No complete executable check demonstrated | No direct tests | PROVISIONAL / PARTIAL |
| Historical v1.3 note | DR01–DR07 | Different registry: arithmetic, sign, reciprocal, identity misuse, quadrant, principal-value and periodicity mistakes | Not aligned to current DR01–DR10; preserve as separate historical taxonomy | No direct tests | HISTORICAL CONFLICT |
| `Blueprint/02_ARCHETYPES.md` | AR17–AR20 | Case Splitting, Optimization, Functional Relation, Mixed Concept | These are archetype patterns, not validation rules. R03's archetype/attribute checks are not proven to execute fully | No direct tests | CONFIRMED NAMESPACE SEPARATION |
| Historical QGS / Library | S1–S5 | S1 Foundation, S2 Easy+, S3 Medium, S4 Hard, S5 Elite | Current R03 accepted values are Easy, Easy+, Medium, Hard, Elite; Foundation is not accepted as written | No dedicated tests | VERIFIED GAP |

## 3. Runtime implementation crosswalk — observed code behaviour

The current feature branch registers `R01Validator`, `R02Validator` and `R03Validator` in `Engine/bootstrap/service_container.py` through `ModuleValidatorAdapter` and `ValidationEngine`.

### Code R01 — Structural Validator

File: `Engine/factory/validation/r01_validator.py`

Observed checks:
- Batch exists and is non-empty.
- Batch/unit/chapter/subtopic codes are checked for empty values (some are warnings).
- Question code and question text are required.
- At least four options are required; the current check does not enforce exactly four.
- Correct option must be A/B/C/D.
- Explanation absence is a warning.
- Duplicate question codes are errors.

It is not the prompt's R01 Concept First rule.

### Code R02 — Academic Validator

File: `Engine/factory/validation/r02_validator.py`

Observed checks:
- Options are non-empty and duplicate normalized options are rejected.
- Correct option label is valid and refers to an existing, non-empty option.
- Missing explanations and explanations shorter than 20 characters are warnings.
- Basic question/option integrity checks are performed.

It does not independently solve the question or establish that the selected answer is mathematically/scientifically correct. It is not the prompt's R02 Single Learning Objective rule.

### Code R03 — Blueprint Validator

File: `Engine/factory/validation/r03_validator.py`

Observed checks:
- Batch metadata presence and unit/chapter/subtopic consistency.
- Difficulty labels and batch progression.
- Concept presence and estimated solving time.
- Limited distractor length check.
- Bloom-level presence.

Important limitations:
- The current code R03 is not the prompt's R03 Mathematical Verification rule.
- The `validate()` method invokes `_validate_blueprint`, `_validate_difficulty`, `_validate_concepts`, `_validate_quality` and score calculation.
- `_validate_quality` invokes distractor-length, Bloom-progression and difficulty-progression checks.
- `_validate_blueprint_attributes` and `_validate_jee_quality` exist as helper methods but are not called by the observed `validate()` path.
- No independent symbolic/numeric mathematical verification is demonstrated by this validator.

### QA001–QA014 registry and QualityPipeline

Files:
- `Engine/factory/quality/rule_registry.py`
- `Engine/factory/quality/quality_pipeline.py`
- `Engine/factory/quality/models/validation_rule.py`

The registry defines QA001–QA014 metadata (question count, text, option count, unique options, correct answer, explanation, difficulty, archetype, Bloom level, blueprint compliance, duplicate question, CSV compatibility, metadata and internal consistency). The QualityPipeline executes supplied validators sequentially.

Repository search found the QA001–QA014 constants only in the registry/model context and found no runtime references wiring `ALL_RULES` or `QualityPipeline` into the active service-container validation path. These definitions must not be described as executed validation merely because the registry exists.

## 4. Test evidence

- Repository tree contains many pipeline/catalogue tests.
- No dedicated `test_r01_validator.py`, `test_r02_validator.py`, `test_r03_validator.py`, or rule-by-rule QA001–QA014 test files were found.
- `Engine/tests/test_validation_processor.py` is a pipeline script that constructs and executes processors; it is not a focused R01/R02/R03 rule test suite.
- `Engine/tests/test_csv_validator.py` concerns CSV validation, not academic rule semantics.
- No current test run was performed as part of this read-only source audit.

## 5. Recovered historical details — not authoritative

The recovered historical discussion mentions:
- Blueprint versions v1.2, v1.3, v1.4 and v1.5.
- v1.3 distractor additions and a DR01–DR07 taxonomy that differs from the current repository's DR01–DR10.
- R01–R20, DE and AR rule families.
- AR-01 Dynamic Count Rule and SC-01 Schema Freeze Rule.
- QC-01 stable question-code pattern and QC-02 difficulty mapping in an assistant-side historical output.

These details are discovery leads only. Where complete user-approved source text, version provenance or exact definitions are missing, they are not promoted into the canonical crosswalk.

## 6. P1 disposition and required resolution

1. Keep the prompt R01–R12, legacy Blueprint R01–R12, code R01–R03 and QA001–QA014 in separate namespaces.
2. Keep DR01–DR10 and historical DR01–DR07 separate until the signed-off blueprint resolves them.
3. Keep AR17–AR20 archetypes separate from AR rule identifiers.
4. Do not claim R03 Mathematical Verification is implemented by code R03.
5. Do not treat QA001–QA014 registry metadata as active runtime validators.
6. Do not declare S1–S5 fully implemented while the current validator rejects “Foundation”.
7. Recover the complete approved Blueprint v1.5 source, then build a rule-by-rule crosswalk with definition, scope, implementation path, test ID, test evidence, severity, repair behaviour and release gate.
8. If the original approved source cannot be recovered, the project owner must explicitly authorize a new reconstructed baseline and version; it must not be labelled the historical v1.5.

**P1 status:** Rule authority not resolved. Final blueprint freeze is prohibited. This is a genuine blocking dependency for final P1 acceptance and for selecting a pilot that depends on the disputed rules.
