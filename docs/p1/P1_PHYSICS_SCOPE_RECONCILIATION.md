# P1 Physics Scope Reconciliation — Detailed Initial Findings

**Audit date:** 2026-11-17  
**Status:** PROVISIONAL SUBTOPIC REVIEW — not final academic approval

## Official authorities

- JEE Main 2027 Physics syllabus: https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/10/20261024683680768.pdf
  - Unit 1 Units and Measurements: PDF page 2, lines 56–58.
  - Unit 7 Properties of Solids and Liquids: pages 2–3, lines 77–82.
  - Unit 8 Thermodynamics: page 3, lines 83–86.
  - Unit 12 Current Electricity: page 4, lines 109–112.
  - Unit 13 Magnetic Effects of Current and Magnetism: page 4, lines 112–122.
  - Unit 14 Electromagnetic Induction and Alternating Currents: page 4, lines 122–123.
  - Unit 16 Optics: pages 4–5, lines 125–133.
  - Unit 18 Atoms and Nuclei: page 5, lines 135–138.
  - Unit 19 Electronic Devices: page 5, lines 138–140.
  - Unit 20 Experimental Skills: pages 5–6, lines 140–153.
- JEE Advanced 2026 Physics syllabus (provisional Advanced 2027 baseline): https://jeeadv.ac.in/documents/jee-advanced-2026-syllabus.pdf
  - General units, dimensions, measurement and error analysis: lines 190–192.
  - Mechanics: lines 193–207.
  - Thermal Physics: lines 208–209.
  - Electricity and Magnetism: lines 210–222.
  - EM waves and Optics: lines 223–232.
  - Modern Physics: lines 234–237.

## High-impact taxonomy findings

### 1. Empty Physics chapters

Internal P4 Work, Energy and Power has three empty chapters; P5 System of Particles and Rotational Motion has two empty chapters. All five are disabled and have zero subtopic rows. They map to major official Main and Advanced syllabus areas. See `P1_EMPTY_CHAPTER_AND_COVERAGE_GAP_AUDIT.md`.

No production question can be assigned to an absent subtopic. Preserve the chapter UUIDs; do not generate placeholder subtopics.

### 2. Cross-unit mappings that differ from internal parents

| Internal stable path | Internal parent | Official Main mapping | Advanced 2026 mapping | Disposition |
|---|---|---|---|---|
| P2_CH2_ST1 Vector Algebra | P2 Kinematics | Unit 12 Vector Algebra | Vectors | Explicit cross-unit mapping; do not rely on P2 parent alone |
| P8_CH1_ST1–ST3 Thermal Expansion | P8 Thermodynamics | Unit 7 Properties of Solids and Liquids | Thermal Physics | Direct subtopic mapping to Main U7 |
| P8_CH2_ST1–ST3 Calorimetry / heat | P8 Thermodynamics | Unit 7 Properties of Solids and Liquids | Thermal Physics | Direct subtopic mapping to Main U7 |
| P8_CH3 Thermodynamics | P8 Thermodynamics | Unit 8 Thermodynamics | Thermal Physics | Direct mapping to Main U8 |

This confirms that a single internal unit can contain subtopics mapped to more than one official unit.

### 3. Combined official units

- Main Unit 13 combines internal P13 Moving Charges and Magnetism with P14 Magnetism and Matter.
- Main Unit 14 combines internal P15 Electromagnetic Induction with P16 Alternating Current.
- Main Unit 16 combines internal P18 Ray Optics with P19 Wave Optics.
- Main Unit 18 combines internal P21 Atoms with P22 Nuclei.

Preserve all internal identities; use many-to-one official mappings.

## Main vs Advanced scope differences and exclusions

| Internal topic | Main 2027 | Advanced 2026 | Initial finding |
|---|---|---|---|
| P12_CH1_ST14 Potentiometer | Not explicitly listed in Unit 12 | Not explicitly listed in reviewed Electricity and Magnetism scope | No direct mapping |
| P13_CH1_ST4 Cyclotron | Not named; force on moving charge is listed | Not named; force on moving charge is listed | Partial application only; academic review required |
| P14_CH1_ST3 Earth Magnetism | Not explicit | Not explicit | No direct mapping |
| P14_CH1_ST4 Magnetic Elements | Not explicit | Not explicit | No direct mapping |
| P14_CH1_ST6 Magnetic Hysteresis | Not explicit | Not explicit | No direct mapping |
| P15_CH1_ST5 Eddy Currents | Explicit in Main Unit 14 | Not explicitly named | Main-only mapping |
| P16_CH1_ST8 Resonance | Explicit in Main Unit 14 | LCR series circuits listed, resonance not named | Main direct; Advanced partial |
| P16_CH1_ST9 Quality Factor | Not explicit | Not explicit | No direct mapping |
| P16_CH1_ST10 Power Factor | Power in AC circuits and wattless current listed | AC/LCR circuits listed | Partial derived scope |
| P16_CH1_ST11 Transformers | Explicit in Main Unit 14 | Not explicitly named | Main-only mapping |
| P18_CH2_ST6 Optical Fibres | Not explicit | Not explicit | No direct mapping |
| P19_CH3_ST3 Malus Law | Polarization/Brewster/Polaroids listed; Malus not named | Polarization/Brewster/Polaroids listed; Malus not named | No direct explicit mapping |
| P21_CH1_ST1 Thomson Model | Not explicit | Not explicit | No direct mapping |
| P22_CH1_ST10–ST12 Decay Law, Half-Life, Mean Life | Radiations listed; decay law/half-life/mean life not named | Explicitly listed in Modern Physics | Advanced-only mapping |
| P23 Semiconductor Electronics | Explicit Main Unit 19 | No corresponding Electronic Devices unit in Advanced 2026 syllabus | Main-only mapping |

Other P18/P19/P21/P22/P23 subtopics are mapped in the CSV where their official wording is direct or partial; the full 233-row Physics review remains incomplete.

## Experimental Skills — separate coverage gate

Main Unit 20 lists 18 experiments/activities, including Vernier calipers, screw gauge, simple pendulum, metre scale, Young's modulus, surface tension, viscosity, sound resonance tube, specific heat, metre bridge, Ohm's law, galvanometer, optical focal length, prism deviation, refractive index and diode characteristics.

Advanced 2026 General scope lists a separate set of measurement/error-analysis experiments.

Internal P1_CH1_ST6 Errors and Measurements maps the error-analysis concept but does not represent all practical procedures, apparatus, observations and experiment-specific calculations. No dedicated internal Experimental Skills unit/chapter is evident. This is a real taxonomy coverage gap, not something to infer from P1.

## Candidate pilot evidence

Physics P1_CH1_ST4 Dimensional Analysis and P1_CH1_ST6 Errors and Measurements have explicit Main 2027 wording and Advanced 2026 comparison wording, plus matched 2026 Main question/key references. See:
- `P1_CANDIDATE_PILOT_SEQUENCE.md`
- `P1_PYQ_EVIDENCE_REGISTER.csv`

These are candidates only. Their source authenticity and question-key linkage are high confidence; local PDF bytes/hashes and cross-year representativeness remain pending.

## Required follow-up

- Complete all 233 Physics subtopic mappings, including exact Main/Advanced applicability and confidence.
- Map every P4/P5 chapter gap before enabling.
- Build a separate Experimental Skills hierarchy or explicitly map every experiment to stable existing taxonomy IDs after academic review.
- Verify all P8 cross-unit assignments and P2 vector cross-unit assignment.
- Confirm the no-direct/partial topics against a second academic reviewer.
- Preserve all IDs and source enable flags; do not make bulk enablement changes during P1.
