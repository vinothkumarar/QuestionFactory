# P1 Empty-Chapter and Official-Syllabus Coverage-Gap Audit

**Audit date:** 2026-11-17  
**Status:** INITIAL GAP REGISTER — academic mapping and remediation plan pending

## 1. Empty chapter inventory

The current curriculum CSV snapshot contains six chapters with zero subtopic rows:

| Subject | Unit | Chapter code | Chapter title | Chapter UUID | Parent unit UUID | Enabled |
|---|---|---|---|---|---|---|
| Physics | P4 — Work, Energy and Power | P4_CH1 | Work | `c0258188-e7af-42ac-baf2-c765eee56d56` | `d4a46504-20af-4749-ac12-3da7ad5591cf` | FALSE |
| Physics | P4 — Work, Energy and Power | P4_CH2 | Energy | `f73f5b27-e3de-454e-908c-bac77a4ef5b6` | `d4a46504-20af-4749-ac12-3da7ad5591cf` | FALSE |
| Physics | P4 — Work, Energy and Power | P4_CH3 | Power | `ddcc722b-260d-4dfc-b91e-22d18e255797` | `d4a46504-20af-4749-ac12-3da7ad5591cf` | FALSE |
| Physics | P5 — System of Particles and Rotational Motion | P5_CH1 | Centre of Mass | `f67144b0-5dc4-48f1-b445-8c2fc3d44166` | `92f2418b-e911-4195-bd34-c71c346587a3` | FALSE |
| Physics | P5 — System of Particles and Rotational Motion | P5_CH2 | Rotational Motion | `04f8f8c9-0a63-45e6-8150-2b8f4f0e23ce` | `92f2418b-e911-4195-bd34-c71c346587a3` | FALSE |
| Chemistry | C27 — Biomolecules | C27_CH3 | Vitamins | `77e106e0-67a7-4239-93dd-eb221f8d5b5c` | `8bceb272-bdf9-446c-abcd-c00f0bf91464` | FALSE |

- Mathematics: 0 empty chapters.
- Physics: 5 empty chapters.
- Chemistry: 1 empty chapter.
- All six empty chapters are currently disabled.
- No subtopic UUIDs exist beneath these chapters in the inspected CSV snapshot.
- Existing chapter UUIDs and codes must be preserved; do not create generic placeholder subtopics merely to satisfy counts.

## 2. Official JEE Main 2027 coverage gaps

### Physics

1. **Official Unit 4 — Work, Energy and Power** and **Unit 5 — Rotational Motion** are major official syllabus units, but internal P4 and P5 currently have five empty chapters and no subtopic rows. Their taxonomy coverage is not manufacturing-ready.
2. **Official Unit 20 — Experimental Skills** has no clearly dedicated internal unit/chapter. P1_CH1_ST6 Errors and Measurements covers only part of the experimental measurement/error scope; it does not represent the full official list of 18 experiments/activities.
3. **Internal P2_CH2_ST1 Vector Algebra** sits under Kinematics, while official Main lists Vector Algebra as a separate Unit 12. It may be used within kinematics, but its official mapping must include Unit 12 as well; do not assume parent unit P2 determines exam scope.
4. **Internal P8_CH1 Thermal Expansion and P8_CH2 Calorimetry** are under the internal Thermodynamics unit, but official Main places thermal expansion, calorimetry and heat transfer within Unit 7 Properties of Solids and Liquids. P8_CH3 Thermodynamics maps to official Unit 8. This is a cross-unit mapping boundary.
5. Several subtopics require exact scope checks: P12 potentiometer; P13 cyclotron; P14 earth magnetism, magnetic elements and hysteresis; P18 optical fibres and resolving power; P19 Malus law; P21 Thomson model; P22 radioactive decay/half-life/mean life. Some are absent or less explicit in Main 2027 and may be Advanced-only, partial or out of scope.

### Chemistry

1. **Official Main Unit 19 — Biomolecules** includes vitamins (classification and functions), but internal C27_CH3 Vitamins has no subtopics.
2. **Official Main Unit 13 — Purification and Characterisation of Organic Compounds** includes crystallisation, sublimation, distillation, extraction, chromatography, qualitative/quantitative analysis and formula calculations. No dedicated internal unit/chapter is evident from the unit list; check all existing subtopics before deciding whether content is covered elsewhere.
3. **Official Main Unit 20 — Principles Related to Practical Chemistry** includes functional-group detection, preparations, titrimetric exercises, qualitative salt analysis and practical experiments. No dedicated internal unit/chapter is evident from the unit list; coverage must be demonstrated at subtopic level, not inferred from Metallurgy or General Organic Chemistry.

## 2A. Chemistry coverage second-pass finding — 2026-11-17

A scan of all 260 Chemistry subtopic names found one relevant existing Main Unit 13 topic: `C20_CH1_ST9 — Chromatographic Methods` (UUID `3bd3b3eb-e250-4e91-8efe-ca8827a2657a`). It is currently nested under C20 Metallurgy, but the mapping register correctly records a cross-unit mapping to Main 2027 Unit 13 Purification and Characterisation (NTA syllabus PDF page 8, lines 206–207). Its parent unit/chapter are disabled, so its effective parent-chain flag is FALSE.

No other direct taxonomy labels were found for crystallisation, sublimation, distillation, extraction, qualitative/quantitative organic analysis or formula determination. This makes Main Unit 13 **partially represented**, not wholly absent and not complete.

No directly named practical-chemistry entries were found for titrimetric exercises, salt analysis, functional-group detection, preparations or practical procedures. Adjacent theory subtopics are not accepted as proof of practical coverage.

See `P1_CHEMISTRY_COVERAGE_GAP_SECOND_PASS.md` for the complete second-pass method, evidence and bounded conclusions. No IDs, parent paths or enable flags were changed.

## 3. JEE Advanced 2026 comparison

- P4/P5 topics are within the Advanced Physics mechanics scope, but empty chapters prevent subtopic-level mapping and PYQ traceability.
- The Advanced Physics syllabus includes detailed mechanics, rotational dynamics, rolling motion and energy/momentum; the missing internal P4/P5 taxonomy is a direct Advanced coverage risk.
- Advanced 2026 Chemistry includes several topics not explicit in Main 2027 (e.g. States of Matter, Surface Chemistry, Hydrogen, s-Block, Isolation of Metals, Polymers, Chemistry in Everyday Life). These must remain separately scoped; the Main gaps above do not imply Advanced gaps.

## 4. Required handling

- Preserve all six chapter IDs and existing disabled flags.
- Record missing subtopic coverage as an explicit gap; do not invent subtopics or enable empty chapters.
- Before adding subtopics, inspect approved syllabus scope, existing question catalogues, PYQ evidence and stable-ID conventions.
- Any new subtopic creation must use a deliberate taxonomy change with a lineage/migration record and user-approved or formally delegated academic review.
- Keep Main and Advanced applicability separate. Some internal subtopics may be Main-only, Advanced-only or shared with different depth.
- Do not start production question generation for P4/P5 or C27_CH3 until the taxonomy is populated, mapped and reviewed.
