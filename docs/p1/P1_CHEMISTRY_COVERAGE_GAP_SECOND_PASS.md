# P1 Chemistry Coverage-Gap Second Pass

**Review date:** 2026-11-17  
**Status:** INTERNAL SECOND-PASS INVENTORY REVIEW — academic approval pending  
**Scope:** All 260 existing Chemistry subtopic rows in `P1_TAXONOMY_MAPPING_REGISTER.csv`  
**Official baseline:** JEE Main 2027; JEE Advanced 2026 is provisional for Advanced 2027.

## 1. Purpose and method

A second-pass scan was performed across all 260 Chemistry subtopic names, their parent unit/chapter labels and the Main/Advanced mapping dispositions. The scan specifically searched for the JEE Main 2027 Purification and Characterisation and Practical Chemistry topic families, and for the explicit Biomolecules vitamins requirement.

This is a taxonomy-name and parent-path review. It does not establish complete academic coverage where a subtopic label is broad or an internal catalogue might contain relevant content outside the curriculum register.

## 2. Confirmed partial coverage — chromatography is present but misfiled

One directly relevant subtopic exists:

| Field | Value |
|---|---|
| Internal unit/chapter/subtopic | `C20_CH1_ST9 — Chromatographic Methods` |
| Subtopic UUID | `3bd3b3eb-e250-4e91-8efe-ca8827a2657a` |
| Internal parent | C20 Metallurgy → C20_CH1 Extraction of Metals |
| Main 2027 mapping | Unit 13 — Purification and Characterisation of Organic Compounds |
| Advanced 2026 mapping | No direct explicit mapping recorded |
| Mapping basis/status | CROSS_UNIT_OR_SUBJECT / Main MAPPED_PROVISIONAL; Advanced NO_DIRECT_EXPLICIT_SCOPE |
| Parent flags | C20 unit FALSE; C20_CH1 chapter FALSE; subtopic TRUE; effective parent-chain FALSE |

The Main syllabus explicitly includes chromatography under Unit 13 (NTA 2027 syllabus PDF, page 8, lines 206–207). The internal subtopic is therefore a real cross-unit mapping, not a reason to treat the whole Main Unit 13 as covered.

## 3. Main Unit 13 — Purification and Characterisation

The 260-row subtopic-name scan found no other directly named entries for:
- Crystallisation / recrystallisation
- Sublimation
- Distillation and its variants
- Solvent extraction
- Purification of organic compounds
- Qualitative elemental analysis
- Quantitative organic analysis
- Empirical/molecular formula calculations specifically under organic characterisation

**Disposition:** Partial coverage only. Chromatography is represented by one existing subtopic but is nested under the internal Metallurgy unit and is effectively disabled by its parent flags. The remaining Unit 13 topics are not demonstrated by the current Chemistry taxonomy snapshot.

Do not create duplicate chromatography IDs or move the existing UUID during P1. Record the cross-unit relationship and defer any parent migration/lineage decision to a controlled taxonomy change.

## 4. Main Unit 20 — Principles Related to Practical Chemistry

The subtopic-name scan found no directly named entries for:
- Titrimetric exercises / volumetric analysis
- Qualitative salt analysis and systematic cation/anion identification
- Detection of functional groups in organic compounds
- Preparation of specified inorganic/organic compounds
- Practical experiments and observation-based procedures

Some existing concepts (e.g. redox reactions, acid-base equilibrium, organic reaction chemistry) are prerequisite theory, not proof that practical exercises, analytical procedures or salt-analysis workflows are represented.

**Disposition:** No demonstrated direct taxonomy coverage in the 260-row snapshot. Keep this as an explicit gap pending a content-level review of any external practical-chemistry catalogues or source materials. Do not infer coverage from adjacent theory chapters.

## 5. Main Unit 19 — Biomolecules / Vitamins

Internal `C27_CH3 — Vitamins` has zero subtopic rows and is one of the six empty chapters in the P1 audit. Main 2027 Biomolecules explicitly includes vitamins, their classification and functions. Therefore:
- The chapter identity exists and is currently disabled.
- No subtopic identity or content currently exists beneath it in the inspected snapshot.
- This is a genuine Main-scope coverage gap unless relevant content is located in another stable taxonomy path.
- Preserve the chapter UUID; do not create placeholder subtopics or enable the empty chapter during P1.

## 6. Evidence and limitations

- Source inventory: 260 Chemistry rows in `P1_TAXONOMY_MAPPING_REGISTER.csv`.
- Exact cross-unit record: `C20_CH1_ST9`, with official Main Unit 13 mapping and evidence recorded in the mapping register.
- Empty chapter record: `C27_CH3 Vitamins`, documented in `P1_EMPTY_CHAPTER_AND_COVERAGE_GAP_AUDIT.md`.
- Official Main source: https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/10/20261024683680768.pdf
- Official Advanced comparison: https://jeeadv.ac.in/documents/jee-advanced-2026-syllabus.pdf (provisional baseline only).

The name scan cannot rule out coverage hidden inside broadly named subtopics or in separate question catalogues. Such coverage must be demonstrated by inspecting the actual content and its stable-ID lineage before any gap is closed.

## 7. Required follow-up

1. Review the actual content/catalogue behind `C20_CH1_ST9` to confirm it covers the intended chromatography scope and no more.
2. Search external/prior Chemistry catalogues for purification, characterisation and practical-chemistry material before creating new taxonomy IDs.
3. If no approved material exists, prepare a proposed new taxonomy hierarchy with official syllabus wording, stable-ID/lineage plan and review evidence; do not add it in this phase.
4. Resolve the Main/Advanced applicability of each proposed topic separately.
5. Preserve all current IDs and flags; no taxonomy or enablement changes are made by this report.

**Conclusion:** Chemistry Main Unit 13 has one misfiled, cross-unit chromatography subtopic but remains substantially uncovered. Main Unit 20 Practical Chemistry has no demonstrated direct coverage in the current taxonomy snapshot. Main Biomolecules vitamins has an empty chapter. These gaps are explicit and bounded; P1 remains in progress.
