# P1 Unit-Level Taxonomy Reconciliation — Working Draft

**Audit date:** 2026-11-17  
**Status:** PROVISIONAL — chapter/subtopic mapping and review gates remain open  
**Internal source:** `Engine/curriculum/{mathematics,physics,chemistry}/units.csv`, `chapters.csv`, `subtopics.csv`  
**Primary exam scope:** JEE Main 2027 official syllabus  
**Advanced comparison scope:** JEE Advanced 2026 official syllabus, provisional only until 2027 syllabus is published

## Authority and interpretation

- JEE Main 2027 syllabus PDF: https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/10/20261024683680768.pdf
- NTA official documents listing: https://jeemain.nta.nic.in/documents/
- JEE Advanced 2027 syllabus status page: https://jeeadv.ac.in/syllabus.html (currently “Coming soon”)
- JEE Advanced 2026 provisional comparison baseline: https://jeeadv.ac.in/documents/jee-advanced-2026-syllabus.pdf

Main and Advanced mappings are separate. “No direct mapping” means the current official syllabus does not explicitly establish the internal scope as a standalone topic; it does not mean that a concept is mathematically invalid. Do not enable such scope for an exam without exact topic-level evidence.

## Inventory totals

| Subject | Internal units | Internal chapters | Internal subtopics | Official Main 2027 units |
|---|---:|---:|---:|---:|
| Mathematics | 15 | 95 | 533 | 14 |
| Physics | 23 | 42 | 233 | 20 |
| Chemistry | 29 | 48 | 260 | 20 |
| **Total** | **67** | **185** | **1,026** | **54** |

## Mathematics — unit-level crosswalk

Official JEE Main 2027 units: (M1) Sets, Relations and Functions; (M2) Complex Numbers and Quadratic Equations; (M3) Matrices and Determinants; (M4) Permutations and Combinations; (M5) Binomial Theorem and its Simple Applications; (M6) Sequence and Series; (M7) Limit, Continuity and Differentiability; (M8) Integral Calculus; (M9) Differential Equations; (M10) Coordinate Geometry; (M11) Three-Dimensional Geometry; (M12) Vector Algebra; (M13) Statistics and Probability; (M14) Trigonometry.

| Internal unit | Internal title | Main 2027 alignment | Advanced 2026 comparison | Initial disposition |
|---|---|---|---|---|
| U1 | Number System | No explicit standalone Main unit | No explicit standalone Number System heading; sets/functions contain number-set language | No direct mapping; review each subtopic |
| U2 | Algebra | Split across M2–M6 and M3; chapters also contain Sets/Relations, Functions and Probability | Algebra; matrices; probability/statistics; functions | Mixed container; chapter/subtopic split required |
| U3 | Coordinate Geometry | M10 | Analytical Geometry (2D) | Direct at unit level; topic check required |
| U4 | Geometry | Partial: triangle centres and coordinate-geometry elements within M10 | Analytical Geometry includes triangle centres, circles, conics and loci | Split scope; do not approve all chapters as a single mapping |
| U5 | Mensuration | No explicit standalone Main unit | No explicit standalone Mensuration heading | No direct mapping pending exact topic evidence |
| U6 | Statistics | M13 | Probability and Statistics | Direct/partial; exact statistical measures to be checked |
| U7 | Probability | M13 | Probability and Statistics | Direct |
| U8 | Trigonometry | M14 | Trigonometry | Direct |
| U9 | Functions | M1 and M7 | Sets, Relations and Functions; Differential Calculus | Direct but overlaps U2 and U15; deduplication review required |
| U10 | Limits, Continuity and Differentiability | M7 | Differential Calculus | Direct |
| U11 | Integral Calculus | M8 | Integral Calculus | Direct |
| U12 | Differential Equations | M9 | Integral Calculus | Direct |
| U13 | Vectors and 3D Geometry | M11 and M12 | Three-dimensional Analytical Geometry; vector concepts in the syllabus | Split into 3D and Vector subtopic mappings |
| U14 | Mathematical Reasoning | No explicit Main 2027 unit | No explicit standalone Mathematical Reasoning unit | No direct mapping pending evidence |
| U15 | Sets and Relations | M1 | Sets, Relations and Functions | Direct but overlaps U2_CH1 and U9 chapters; identity-preserving consolidation study required |

### Mathematics duplication and boundary flags

- Sets/relations appear under U2_CH1, U9_CH1 and U15 chapters. These are not assumed to be three distinct academic scopes.
- Functions appear under U2_CH2, U9 and U15 chapters. Exact concept/subtopic deduplication is required.
- U1 contains greatest-integer, fractional-part, logarithms, surds/indices and modular/remainder material. Some may align to official function/algebra wording, but a unit-level label is insufficient to approve them.
- U4 geometry contains both coordinate-relevant triangle-centre content and broader geometry/transformations. Only explicitly supported subtopics can map.
- U5 Mensuration and U14 Mathematical Reasoning have no explicit standalone Main 2027 headings in the official list.

No existing U/CH/ST code or UUID is changed by this draft.

## Physics — unit-level crosswalk

Official JEE Main 2027 units: (P1) Units and Measurements; (P2) Kinematics; (P3) Laws of Motion; (P4) Work, Energy and Power; (P5) Rotational Motion; (P6) Gravitation; (P7) Properties of Solids and Liquids; (P8) Thermodynamics; (P9) Kinetic Theory of Gases; (P10) Oscillations and Waves; (P11) Electrostatics; (P12) Current Electricity; (P13) Magnetic Effects of Current and Magnetism; (P14) Electromagnetic Induction and Alternating Currents; (P15) Electromagnetic Waves; (P16) Optics; (P17) Dual Nature of Matter and Radiation; (P18) Atoms and Nuclei; (P19) Electronic Devices; (P20) Experimental Skills.

| Internal unit | Internal title | Main 2027 alignment | Advanced 2026 comparison | Initial disposition |
|---|---|---|---|---|
| P1 | Units and Measurements | P1 | General Physics foundations | Direct |
| P2 | Kinematics | P2 | Kinematics | Direct |
| P3 | Laws of Motion | P3 | Laws of Motion | Direct |
| P4 | Work, Energy and Power | P4 | Work, Energy and Power | Direct |
| P5 | System of Particles and Rotational Motion | P5 | Rotational Dynamics | Direct |
| P6 | Gravitation | P6 | Gravitation | Direct |
| P7 | Mechanical Properties of Solids and Fluids | P7 | Mechanical properties/fluids where included | Direct/partial |
| P8 | Thermodynamics | P8 | Thermal Physics | Direct |
| P9 | Kinetic Theory of Gases | P9 | Kinetic Theory | Direct |
| P10 | Oscillations and Waves | P10 | Oscillations and Waves | Direct |
| P11 | Electrostatics | P11 | Electrostatics | Direct |
| P12 | Current Electricity | P12 | Current Electricity | Direct |
| P13 | Moving Charges and Magnetism | P13 | Magnetic effects | Direct/partial |
| P14 | Magnetism and Matter | P13 | Magnetism and Matter | Direct/partial |
| P15 | Electromagnetic Induction | P14 | Electromagnetic Induction | Direct/partial |
| P16 | Alternating Current | P14 | Alternating Current | Direct/partial |
| P17 | Electromagnetic Waves | P15 | Electromagnetic Waves | Direct |
| P18 | Ray Optics and Optical Instruments | P16 | Optics | Direct/partial |
| P19 | Wave Optics | P16 | Optics | Direct/partial |
| P20 | Dual Nature of Matter and Radiation | P17 | Modern Physics | Direct |
| P21 | Atoms | P18 | Atomic Physics | Direct/partial |
| P22 | Nuclei | P18 | Nuclear Physics | Direct/partial |
| P23 | Semiconductor Electronics | P19 | Electronic/modern physics scope requires exact chapter check | Direct/partial |
| **No internal unit** | **Experimental Skills** | **P20** | No equivalent standalone unit established by this mapping | **Coverage gap identified** |

### Physics gap and consolidation flags

- Official Main P13 combines internal P13 and P14.
- Official Main P14 combines internal P15 and P16.
- Official Main P16 combines internal P18 and P19.
- Official Main P18 combines internal P21 and P22.
- Official Main P20 Experimental Skills has no clearly identified dedicated internal unit in the current P1–P23 unit list. Check whether any existing P1 subtopics cover experimental procedures; do not assume dimensional analysis or errors alone satisfy the full practical/experimental skills scope.
- Consolidation of internal units is not proposed in this phase. Preserve IDs and record a many-to-one official mapping.

## Chemistry — unit-level crosswalk

Official JEE Main 2027 units: (C1) Some Basic Concepts in Chemistry; (C2) Atomic Structure; (C3) Chemical Bonding and Molecular Structure; (C4) Chemical Thermodynamics; (C5) Solutions; (C6) Equilibrium; (C7) Redox Reactions and Electrochemistry; (C8) Chemical Kinetics; (C9) Classification of Elements and Periodicity in Properties; (C10) p-Block Elements; (C11) d- and f-Block Elements; (C12) Coordination Compounds; (C13) Purification and Characterisation of Organic Compounds; (C14) Some Basic Principles of Organic Chemistry; (C15) Hydrocarbons; (C16) Organic Compounds Containing Halogens; (C17) Organic Compounds Containing Oxygen; (C18) Organic Compounds Containing Nitrogen; (C19) Biomolecules; (C20) Principles Related to Practical Chemistry.

| Internal unit | Internal title | Main 2027 alignment | Advanced 2026 comparison | Initial disposition |
|---|---|---|---|---|
| C1 | Mole Concept | C1 | General Topics / Mole Concept | Direct |
| C2 | Atomic Structure | C2 | Atomic Structure | Direct |
| C3 | Chemical Bonding and Molecular Structure | C3 | Chemical Bonding | Direct |
| C4 | States of Matter | No explicit standalone Main unit | States of Matter: Gases and Liquids | Advanced-only baseline candidate |
| C5 | Thermodynamics | C4 | Chemical Thermodynamics | Direct |
| C6 | Chemical Equilibrium | C6 | Chemical Equilibrium | Direct/partial |
| C7 | Ionic Equilibrium | C6 | Ionic Equilibrium | Direct/partial |
| C8 | Redox Reactions | C7 | Redox/Electrochemistry | Direct/partial |
| C9 | Solutions | C5 | Solutions | Direct |
| C10 | Electrochemistry | C7 | Electrochemistry | Direct/partial |
| C11 | Chemical Kinetics | C8 | Chemical Kinetics | Direct |
| C12 | Surface Chemistry | No explicit standalone Main unit | Surface Chemistry | Advanced-only baseline candidate |
| C13 | Classification of Elements and Periodicity | C9 | Classification and Periodicity | Direct |
| C14 | Hydrogen | No explicit standalone Main unit | Hydrogen | Advanced-only baseline candidate |
| C15 | s-Block Elements | No explicit standalone Main unit | s-Block Elements | Advanced-only baseline candidate |
| C16 | p-Block Elements | C10 | p-Block Elements | Direct |
| C17 | d-Block Elements | C11 | d-Block Elements | Direct/partial |
| C18 | f-Block Elements | C11 | f-Block Elements | Direct/partial |
| C19 | Coordination Compounds | C12 | Coordination Compounds | Direct |
| C20 | Metallurgy | No explicit standalone Main unit | Isolation of Metals | Advanced-only baseline candidate |
| C21 | General Organic Chemistry | C14 | Basic Principles of Organic Chemistry | Direct/partial |
| C22 | Hydrocarbons | C15 | Alkanes, Alkenes and Alkynes; Benzene | Direct |
| C23 | Haloalkanes and Haloarenes | C16 | Alkyl Halides; Haloarenes | Direct |
| C24 | Alcohols, Phenols and Ethers | C17 | Alcohols, Phenols and Ethers | Direct |
| C25 | Aldehydes, Ketones and Carboxylic Acids | C17 | Aldehydes, Ketones and Carboxylic Acids | Direct |
| C26 | Amines | C18 | Amines | Direct |
| C27 | Biomolecules | C19 | Biomolecules | Direct |
| C28 | Polymers | No explicit standalone Main unit | Polymers | Advanced-only baseline candidate |
| C29 | Chemistry in Everyday Life | No explicit standalone Main unit | Chemistry in Everyday Life | Advanced-only baseline candidate |
| **No clear dedicated internal unit** | **Purification and Characterisation of Organic Compounds** | **C13** | Basic/practical organic chemistry contains related elements | **Coverage gap requires subtopic audit** |
| **No clear dedicated internal unit** | **Principles Related to Practical Chemistry** | **C20** | Practical Organic Chemistry / qualitative analysis | **Coverage gap requires subtopic audit** |

### Chemistry gap and boundary flags

- Main C6 combines internal C6 and C7.
- Main C7 combines internal C8 and C10.
- Main C11 combines internal C17 and C18.
- Main C13 and C20 require explicit purification, characterization, practical exercises and qualitative analysis coverage. A second-pass scan of all 260 Chemistry subtopics found one cross-unit chromatography entry (`C20_CH1_ST9`) mapped to Main C13, but no demonstrated coverage of the other major purification/characterisation methods. No directly named practical-chemistry subtopics were found for titrimetric exercises, salt analysis, functional-group detection or preparations. See `P1_CHEMISTRY_COVERAGE_GAP_SECOND_PASS.md`; do not treat the existence of chromatography as full Unit 13 coverage.
- Internal C4, C12, C14, C15, C20, C28 and C29 have corresponding or related headings in the Advanced 2026 syllabus but no explicit standalone unit in Main 2027. Their Main applicability must not be inferred.
- Main 2027 is the current Main source; Advanced 2026 remains provisional for Advanced 2027.

## Cross-subject structural controls

1. Official units may map to several internal units (many-to-one) or one internal unit may span multiple official units (one-to-many).
2. Mapping is applied at the narrowest verified subtopic, not solely by matching unit/chapter titles.
3. Each mapping row must include exam, syllabus version, official wording, internal stable code, mapping status, evidence source, confidence, reviewer and review date.
4. A shared internal subtopic can have different Main and Advanced applicability.
5. Unmapped/uncertain scope is blocked for that exam target; it is not silently treated as eligible.
6. Duplicate internal concepts and chapter overlap are audited separately from official syllabus coverage.
7. Preserve all UUIDs, codes, catalogues and historical records. Any future merge/split requires a lineage map and explicit migration plan.

## Outstanding work before approval

- Inspect all 185 chapter names and 1,026 subtopic names against the official text.
- Identify all duplicate or overlapping subtopics, especially Mathematics U2/U9/U15 and cross-unit duplicates.
- Confirm Experimental Skills coverage in Physics.
- Confirm Chemistry purification/characterisation and practical chemistry coverage.
- Separate Main 2027, Advanced 2026 provisional and Advanced 2027 pending status in the mapping registry.
- Add official source fingerprints when local PDF bytes are acquired.
- Obtain independent academic review for borderline mappings.
- Do not mark any mapping APPROVED based on this unit-level draft alone.
