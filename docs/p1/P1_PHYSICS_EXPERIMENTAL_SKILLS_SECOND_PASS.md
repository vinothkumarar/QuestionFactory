# P1 Physics Experimental Skills — Second-Pass Coverage Review

**Review date:** 2026-11-17  
**Status:** INTERNAL SECOND-PASS REVIEW — dedicated practical taxonomy not established  
**Scope:** 18 experiments/activities in official JEE Main 2027 Physics Unit 20, compared against all 233 existing Physics subtopic names.

## 1. Official requirement

The NTA JEE Main 2027 Physics syllabus lists 18 experiments/activities under Unit 20 Experimental Skills (official PDF page 5, lines 140–152; https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/10/20261024683680768.pdf).

The requirement includes apparatus use, observations, measurement procedures, experimental graphs/curves and practical methods. A theory subtopic with the same scientific concept is not automatically equivalent to the experiment.

## 2. Experiment-to-taxonomy crosswalk

| # | Official Main experiment/activity | Existing candidate taxonomy path | Coverage finding |
|---:|---|---|---|
| 1 | Vernier calipers: internal/external diameter and vessel depth | P1_CH1_ST1 Physical Quantities; P1_CH1_ST6 Errors and Measurements | Measurement foundations only; no explicit Vernier procedure, least-count workflow or observation treatment identified |
| 2 | Screw gauge: thickness/diameter of thin sheet or wire | P1_CH1_ST1; P1_CH1_ST6 | Measurement foundations only; no explicit screw-gauge procedure or zero-error workflow identified |
| 3 | Simple pendulum: energy dissipation graph against time | P10_CH1_ST8 Simple Pendulum | Theory concept exists; no explicit amplitude-squared/time experimental graph or observation workflow identified. Main theory mapping was incorrectly marked no-direct and is corrected provisionally in the mapping register |
| 4 | Metre scale: mass by principle of moments | P5_CH1 Centre of Mass / P5_CH2 Rotational Motion | Both internal P5 chapters are empty; no subtopic row exists for this experiment's moments procedure |
| 5 | Young's modulus of a metallic wire | P7_CH1_ST3 Young's Modulus | Theory concept exists; wire-loading/extension measurement and experiment procedure are not separately represented |
| 6 | Surface tension by capillary rise and detergent effect | P7_CH3_ST1 Surface Energy; P7_CH3_ST2 Capillarity | Theory concepts exist; capillary-rise procedure and detergent comparison are not separately represented |
| 7 | Viscosity by terminal velocity of a sphere | P7_CH2_ST8 Viscosity; P7_CH2_ST9 Stokes Law | Theory concepts exist; terminal-velocity measurement procedure is not separately represented |
| 8 | Speed of sound in air using a resonance tube | P10_CH1_ST10 Resonance; P10_CH2_ST8 Organ Pipes | Related theory exists; resonance-tube procedure and observation method are not separately represented |
| 9 | Specific heat capacity by method of mixtures | P8_CH2_ST1 Specific Heat | Theory concept exists; calorimetry/method-of-mixtures procedure is not separately represented |
| 10 | Resistivity of wire using a metre bridge | P12_CH1_ST5 Resistivity; P12_CH1_ST13 Meter Bridge | Theory/instrument concept exists; experiment procedure and observation calculation are not separately represented |
| 11 | Resistance of wire using Ohm's law | P12_CH1_ST4 Ohm Law | Theory relation exists; experimental setup, readings and V-I graph are not separately represented |
| 12 | Galvanometer resistance/figure of merit by half-deflection | P13_CH1_ST12 Moving Coil Galvanometer | Instrument theory exists; half-deflection method and figure-of-merit procedure are not separately represented |
| 13 | Focal length of mirrors/lens by parallax | P18_CH1_ST2 Spherical Mirrors; P18_CH3_ST1 Thin Lens Formula | Optical theory exists; parallax method and experiment-specific observation tables are not separately represented |
| 14 | Angle of deviation vs incidence for triangular prism | P18_CH4_ST1 Deviation; P18_CH4_ST2 Minimum Deviation | Theory concepts exist; experiment graph/measurement procedure is not separately represented |
| 15 | Refractive index of glass slab using travelling microscope | P18_CH2_ST2 Refractive Index | Theory concept exists; travelling-microscope procedure is not separately represented |
| 16 | p-n junction diode characteristic curves | P23_CH2_ST1 PN Junction; ST2 Forward Bias; ST3 Reverse Bias | Device theory exists; experimental I-V characteristic measurement is not separately represented |
| 17 | Zener diode characteristic curve and breakdown voltage | P23_CH2_ST5 Zener Diode | Device theory exists; breakdown-curve measurement procedure is not separately represented |
| 18 | Identification of diode, LED, resistor and capacitor | P23_CH2_ST5 Zener Diode; P23_CH2_ST6 LED; P11 capacitor concepts | Component concepts exist in parts; no dedicated component-identification practical activity is represented |

## 3. Mapping correction discovered

The existing row `P10_CH1_ST8 — Simple Pendulum` was marked `NO_DIRECT_EXPLICIT_SCOPE` for Main 2027 with a note that Main did not explicitly list resonance for this SHM subtopic.

That disposition missed the direct wording in Main Physics Unit 10: the syllabus explicitly includes the simple pendulum and derivation of its time-period expression (PDF page 3, lines 90–95). Main Unit 20 separately includes the simple-pendulum energy-dissipation experiment (PDF page 5, lines 143–145).

The mapping register is corrected to:
- Main candidate: Physics Unit 10 — Oscillations and Waves (simple pendulum theory), plus Unit 20 — Experimental Skills (simple-pendulum activity).
- Main mapping status: `MAPPED_PROVISIONAL`.
- Academic review status remains `PENDING_INDEPENDENT_REVIEW`.
- Existing stable UUID/code and all enablement flags remain unchanged.

This correction is limited to the explicit simple-pendulum scope; it does not approve the other 17 practical activities or the entire P10 chapter.

## 4. Overall coverage finding

- The existing taxonomy contains theory subtopics related to many of the 18 experiments.
- The register does not contain a dedicated Experimental Skills unit or an explicit practical-method hierarchy that captures all required apparatus, procedures, observations, graphs and activity outcomes.
- The metre-scale/moments experiment is additionally blocked by the two empty P5 chapters.
- A theory-to-experiment crosswalk is useful for traceability but is not a substitute for practical taxonomy coverage.
- The official Advanced 2026 syllabus is only a provisional Advanced 2027 baseline and does not establish an equivalent Main-style 18-item Experimental Skills list.

## 5. Required follow-up

1. Preserve all existing taxonomy IDs and flags.
2. Decide, through a controlled taxonomy change after P1, whether to create a dedicated Physics Experimental Skills hierarchy or attach experiment/activity entities to existing theory subtopics with explicit many-to-many links.
3. For each activity, define apparatus, variables, procedure, observations, graph/calculation, error sources and expected inference before treating it as covered.
4. Resolve the empty P5 chapter gap before mapping the metre-scale moments experiment to a usable subtopic.
5. Keep Main and Advanced scope distinct and revalidate when the official Advanced 2027 syllabus is published.

**Conclusion:** Main Unit 20 is not covered by the current Physics taxonomy merely because related theory subtopics exist. Coverage is partial and structurally incomplete. One definite Main simple-pendulum mapping error was found and corrected provisionally; all other mapping rows remain pending independent academic review.
