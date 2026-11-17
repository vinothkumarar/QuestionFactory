# P1 Question-to-Taxonomy Second-Pass Review

**Review date:** 2026-11-17  
**Branch:** `feature/dual-question-engine-v1`  
**Purpose:** Independently re-check the four question-level PYQ samples against their internal taxonomy paths, official syllabus wording and parent/child enablement snapshot.  
**Status:** SAMPLE REVIEW ONLY — not a substitute for independent academic sign-off across the 1,026-row taxonomy.

## 1. Results

| Sample | Internal subtopic | Question concept | Main 2027 | Advanced baseline | Effective enabled snapshot | Disposition |
|---|---|---|---|---|---|---|
| JEE Main 2026, 2 Apr Shift 1, Physics Q26 | `P1_CH1_ST4` Dimensional Analysis | Dimensions of electric-field energy density | Explicit: dimensional analysis and applications | Explicit: units, dimensions and dimensional analysis | TRUE | Strong candidate for continued pilot validation |
| JEE Main 2026, 2 Apr Shift 1, Physics Q27 | `P1_CH1_ST6` Errors and Measurements | Error propagation in Young's modulus measurement | Explicit: errors in measurements | Explicit: methods of measurement and error analysis | TRUE | Strong candidate for continued pilot validation |
| JEE Advanced 2026, Paper 1, Mathematics Q3 | `U2_CH8_ST2` Matrix Operations | Invertibility under elementary row transformations | Explicit Main Unit 3 matrices and determinants | Explicit Advanced algebra/matrices | FALSE | Valid academic mapping sample, but not active under current parent flags |
| JEE Advanced 2026, Paper 2, Physics Q1 | `P12_CH1_ST2` Drift Velocity | Drift velocity from conductivity, current and carrier density | Explicit Main Unit 12 current electricity | Explicit Advanced electricity and magnetism | FALSE | Valid academic mapping sample, but not active under current parent flags |

## 2. Stable identity and enablement evidence

- `P1_CH1_ST4`: UUID `eca3ac93-a40f-471e-9f9b-91c90aa71557`; unit, chapter and subtopic flags are TRUE.
- `P1_CH1_ST6`: UUID `03590ba5-480d-46bb-8b4f-334aab7eab74`; unit, chapter and subtopic flags are TRUE.
- `U2_CH8_ST2`: UUID `d390847f-0165-4f9b-a015-daa7ce6b63ea`; U2 unit and U2_CH8 chapter flags are FALSE while the subtopic flag is TRUE. The effective parent-chain flag is therefore FALSE.
- `P12_CH1_ST2`: UUID `fb59903b-3ff9-4754-b31c-88c62dd173ae`; P12 unit and P12_CH1 chapter flags are FALSE while the subtopic flag is TRUE. The effective parent-chain flag is therefore FALSE.

No flag or stable ID was changed. A subtopic-level TRUE flag cannot override a disabled parent unit or chapter.

## 3. Scope-boundary checks

### Dimensional Analysis — P1_CH1_ST4
The sampled question tests dimensions of an energy density and a dimensional-exponent expression. This is within the explicit dimensional-analysis wording of both official syllabus baselines. The sample does not justify broadening the subtopic to unrelated measurement-error topics or all dimensional algebra variants without separate syllabus evidence.

### Errors and Measurements — P1_CH1_ST6
The sampled question requires propagation of measurement uncertainties in a physical measurement. This is directly within Main's errors-in-measurements wording and Advanced's measurement/error-analysis scope. The Main syllabus also has a separate Experimental Skills unit; this mapping does not establish coverage of every listed experiment, apparatus, observation or practical procedure.

### Matrix Operations — U2_CH8_ST2
The sampled question tests invertibility, an elementary matrix property, and aligns to the official matrices/algebra scope. This sample does not independently approve every matrix subtopic, determinant identity or advanced manipulation in U2_CH8. Parent flags currently exclude it from the effective-enabled snapshot.

### Drift Velocity — P12_CH1_ST2
The sampled question combines circuit resistance/current with carrier density and drift velocity. Drift velocity is in the official current-electricity/electricity-and-magnetism scope. The sample does not approve every subtopic in P12_CH1 or permit bypassing disabled P12/P12_CH1 parent flags.

## 4. PYQ answer verification cross-reference

All four samples have question-level source URLs, final-key URLs, paper/key page references and independent calculations in `P1_PYQ_EVIDENCE_REGISTER.csv`:
- Main Physics Q26: official NTA question ID 69112126; key option ID 69112187; answer B / 1.
- Main Physics Q27: official NTA question ID 69112127; key option ID 69112191; answer B / 1.65.
- Advanced Paper 1 Mathematics Q3: official final key Q3:B; determinant check confirms B.
- Advanced Paper 2 Physics Q1: official final key Q1:C; independent drift-velocity calculation gives approximately 0.2083 mm/s, matching C.

Local source PDF bytes and SHA-256 hashes remain pending for all four samples. This review therefore validates the question-level mapping logic using the inspected official source content, but does not certify local-file provenance or hash integrity.

## 5. Review limitations and actions

1. This is an internal second-pass review, not an independent human subject-matter-expert approval.
2. The full 1,026-row mapping register remains `PENDING_INDEPENDENT_REVIEW`; no global review status is changed.
3. Only two Main questions from one shift and one question from each Advanced paper are represented. This is not a frequency, trend or representativeness sample.
4. Keep P1_CH1_ST4 and P1_CH1_ST6 as the leading candidate paths for further P1 gate work; do not authorize production generation.
5. Preserve the disabled parent-chain state of U2_CH8_ST2 and P12_CH1_ST2; no enablement changes are made.
6. Continue source-byte acquisition/hash work, broader PYQ sampling, taxonomy review and blueprint-authority resolution.

**Conclusion:** The two Physics P1 candidates have the clearest combination of explicit official syllabus scope, matched Main PYQ evidence and currently effective parent-chain enablement. The two Advanced samples strengthen source/mapping validation but their internal parent chains are disabled. P1 remains in progress and no production pilot is authorized.
