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


## 7. Additional prior-conversation recovery — 2026-11-17

The following fragments were recovered from prior conversation context after the initial repository/Library search. They improve the historical reconstruction, but they are **not a substitute for the missing canonical v1.5 file** and must not be treated as a final source-of-truth artifact.

### 7.1 Recovered part structure

The historical v1.5 structure is remembered as 18 parts: Philosophy; Lifecycle; SC-01 Database-first; Stable IDs; R01–R12; AR-01 Dynamic Count/Saturation; BS-01 Batch Size; DE-01/DE-02; AR-02 Archetype Registry; DI-01; META-01; CM-01; PYQ engines; v1.4 engines; RL-01; EDF-01; Subject Design Pipeline; Hard Stop. Exact original headings and body text are still missing.

### 7.2 R01–R12 recovered quality-rule names

| Rule | Recovered name | Recovered core intent |
|---|---|---|
| R01 | Concept First | Test conceptual understanding; concept must be identifiable |
| R02 | Single Learning Objective | One primary learning objective per question unless integration is intentional |
| R03 | Mathematical Verification | Verify formulae, calculations, units, dimensions and logic |
| R04 | Unique Answer | Exactly one correct answer unless the item type permits otherwise |
| R05 | Explanation Quality | Complete educational explanation of the governing concept |
| R06 | Difficulty Alignment | Difficulty comes from conceptual depth, not calculation length |
| R07 | Language Quality | Clear, precise and professional exam language |
| R08 | Examination Authenticity | Official exam style without answer-revealing patterns |
| R09 | Originality | Original questions inspired by trends, not copied questions |
| R10 | Educational Value | Explanation should teach |
| R11 | Internal Consistency | Question, options, answer and explanation agree |
| R12 | Production Readiness | Production inclusion gate must pass |

These match the names/intent in `Engine/prompts/master/05_blueprint_rules.md`. No reliable R13–R20 quality-rule definitions were recovered; do not infer them from the AR01–AR20 archetypes.

### 7.3 AR-01, BS-01 and saturation intent

- **AR-01:** Dynamic Count Rule. Batch size is a container; set completion depends on saturation, not a fixed question count. Inputs include concept/archetype coverage, formula diversity, solution diversity, Bloom coverage, PYQ patterns and repetition. Outputs: `CONTINUE` or `SATURATED`.
- Global principles recovered: coverage over count; quality over speed; set saturation over batch saturation.
- **BS-01:** default batch size is 10; it does not define set completion.
- Exact saturation thresholds, weights, formula and minimum coverage percentages remain unknown.

### 7.4 AR-02 archetype names recovered

| ID | Name | ID | Name |
|---|---|---|---|
| AR01 | Direct | AR11 | Integer Answer |
| AR02 | Reverse | AR12 | Counting |
| AR03 | Parameterized | AR13 | Graphical |
| AR04 | Composite | AR14 | Advanced Manipulation |
| AR05 | Transformation | AR15 | PYQ Style |
| AR06 | Hidden Identity | AR16 | Symmetry |
| AR07 | Variable Substitution | AR17 | Case Splitting |
| AR08 | Multi-Step Chain | AR18 | Optimization |
| AR09 | Statement | AR19 | Functional Equation |
| AR10 | Assertion–Reason | AR20 | Mixed Concept |

Names are recovered; complete definitions, selection criteria, per-set quotas, examples and activation/saturation thresholds are not. The v1.5 AR19 name is Functional Equation; repository `Blueprint/02_ARCHETYPES.md` says Functional Relation.

### 7.5 DE-01/DE-02 and DR01–DR12 recovered

- **DE-01:** every distractor must represent a plausible, identifiable student misconception; random distractors are prohibited.
- **DE-02:** distractors must be plausible, distinct, internally consistent, clearly incorrect after correct reasoning and not accidentally become correct; diversify misconception categories.

| ID | Recovered v1.5 distractor category |
|---|---|
| DR01 | Arithmetic Error |
| DR02 | Sign Error |
| DR03 | Reciprocal Confusion |
| DR04 | Identity Misuse |
| DR05 | Quadrant Mistake |
| DR06 | Principal Value Error |
| DR07 | Periodicity Mistake |
| DR08 | Half-Angle Confusion |
| DR09 | Formula Substitution Error |
| DR10 | Unit Mismatch |
| DR11 | Root Selection Mistake |
| DR12 | Parameter Misinterpretation |

Full definitions, examples, weighting and allowed category distributions are not recovered. This is a third registry distinct from both the repository's DR01–DR10 prompt taxonomy and the historical v1.3 DR01–DR07 taxonomy.

### 7.6 DI-01 and historical execution defaults

Recovered intended set progression:
- S1 Foundation
- S2 Easy+
- S3 Medium
- S4 Hard
- S5 Elite

Additional historical difficulty score bands were recorded as Easy 10–20, Easy+ 21–35, Medium 36–55, Medium+ 56–75 and Advanced 76–100. The mapping of these five score bands to S1–S5 is unresolved; Medium+/Advanced must not be silently renamed Hard/Elite.

Historical question-type distributions recovered:
- S1: 80/10/10
- S2: 70/15/15
- S3: 60/20/20
- S4: 50/25/25
- S5 adds Integer Answer, Multi-step and PYQ-style forms.

Single Correct / Statement / Assertion–Reason are associated with the S1 split. The exact category allocation for S2–S4 is not recovered.

Other historical defaults (not active production settings until verified): +4/-1 marks; estimated-time bands Easy 45–90s, Easy+ 60–120s, Medium 90–150s, Medium+ 120–210s, Advanced 180–300s; exam relevance mix 70% Main / 20% Advanced / 10% BITSAT; status DRAFT; version v1.0; `is_verified=false`.

### 7.7 Remaining recovered rules

| Rule | Recovered detail | Still unknown |
|---|---|---|
| META-01 | `mistake_pattern`, `common_error`, `difficulty_tag`, `prerequisite_concept`, `jee_frequency`, `revision_priority` | Required/optional status and value dictionaries |
| CM-01 | Unit → Chapter → Subtopic → Concept → Formula → Common Error → Archetype → Question IDs → Difficulty | Cardinality and linking constraints |
| PYQ-01 | Source/exam/year/paper/shift/question provenance; separate paper, key and solution sources | Full source hierarchy and recency rules |
| PYQ-02 | Similarity distance 0 Original, 1 Inspired, 2 PYQ-like, 3 Near Duplicate (reject) | Algorithm and score thresholds |
| SV-01 | Nulls, option completeness, answer consistency, allowed values, escaping, CSV integrity and length limits | Complete canonical schema/value table |
| QE-01 | Five dimensions /10 each: concept clarity, difficulty accuracy, distractor quality, novelty, JEE relevance; minimum 40/50 | Rubric and veto conditions |
| RL-01 | DRAFT → UNDER_VERIFICATION → RELEASED | Complete state machine and rollback rules |
| FD-01 | Formula diversity | Formula families and thresholds |
| SD-01 | Solution-method diversity | Method taxonomy and thresholds |
| CE-01 | Coverage expansion | Coverage metric and quotas |
| CT-01 | Continuity and stable-ID preservation | Full transition/recovery rules |
| EDF-01 | Defaults include DRAFT, v1.0, `is_verified=false` | Full defaults and override hierarchy |
| Hard Stop | Stop if schema, continuity, coverage, archetype, formula/solution diversity, PYQ similarity, distractor, answer, explanation or quality gates fail | Exact aggregation and override policy |

### 7.8 Updated P1 decision

The prior conversation recovery is sufficient to identify the intended v1.5 direction and to prove several repository conflicts. It is **not sufficient to reconstruct the complete frozen blueprint without guessing**. The full original artifact remains the authority blocker. If it cannot be recovered, the safe route is an explicitly versioned recovery candidate, not a file falsely labelled as the original v1.5.



## 8. Exam-format evidence affecting EDF-01 — 2026-11-17

The official JEE Advanced 2026 Paper 1 and its final-key PDF were opened directly. The paper demonstrates that marking defaults are section-specific, not one global `+4/-1` rule:

| Paper 1 section | Question format | Official marking observed |
|---|---|---|
| Section 1 | Single-correct MCQ | +3 correct, 0 unanswered, −1 otherwise |
| Section 2 | Multiple-correct MCQ | +4 full; partial +1/+2/+3 under stated selection conditions; 0 unanswered; −1 otherwise |
| Section 3 | Numerical value | +4 correct; 0 otherwise; no negative mark stated |
| Section 4 | Matching-list MCQ | +4 correct; 0 unanswered; −1 otherwise |

Official evidence: `https://jeeadv.ac.in/documents/p1_english.pdf` and `https://jeeadv.ac.in/documents/p1_solutions_final.pdf`.

**P1 implication:** EDF-01 cannot safely apply a universal +4/−1 default to every JEE Advanced question. It must be keyed to exam, year, paper and section/question format. The recovered historical +4/−1 value remains a default fragment only, not a complete scoring policy. Main 2026 and future exam patterns must also be represented separately.

## 8. Second recovery pass — 2026-11-17

A second targeted recovery pass was performed after the initial audit:

- ChatGPT Library semantic search was repeated with the exact title phrase `MASTER CONSOLIDATED FROZEN BLUEPRINT v1.5`, the 18-part structure, and the v1.5 identifiers (AR-01, SC-01, DI-01). The returned relevant records were the consolidated blueprint/QPC notes, decision register, reconciliation addendum and MECP plan; none was the complete signed-off v1.5 artifact.
- GitHub repository code search was run for the exact title, `Blueprint v1.5`, `AR-01 Dynamic Count SC-01 Schema Freeze` and the recovered DR12 label. No matching files were returned from the repository's default-branch code-search index.
- The Library materials corroborate fragments and the authority hierarchy, but expressly state that the precise final approved version and complete rule text must be checked against the canonical source. They do not authorize promoting the recovered fragments to a new freeze.

**Recovery disposition:** The canonical v1.5 artifact remains NOT RECOVERED after the second pass. This is a real P1 blocker, not a missing-document assumption. Preserve the provisional crosswalk and current rule namespaces; do not silently reconstruct or freeze a candidate. If the original file is later supplied or located, compare it line-by-line before changing the authority status.
