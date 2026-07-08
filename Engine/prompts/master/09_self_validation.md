# PART 9 — SELF VALIDATION

## Objective

Before returning the final JSON response, perform an internal quality
review.

Do not expose your reasoning.

Only return the final validated JSON.

---

## Validation Checklist

### V01 — Question Integrity

Verify:

- The question is complete.
- The wording is unambiguous.
- The language is grammatically correct.
- The question is self-contained.

---

### V02 — Concept Validation

Verify:

- The intended concept is correctly tested.
- No unrelated concepts dominate the question.
- The learning objective is clear.

---

### V03 — Mathematical Validation

Verify:

- Formulae are correct.
- Calculations are correct.
- Units are correct.
- Dimensions are correct.
- Numerical values are internally consistent.

Never return mathematically incorrect content.

---

### V04 — Option Validation

Verify:

- Exactly four options exist.
- Exactly one option is correct.
- No duplicate options.
- No contradictory options.
- Options are mutually exclusive.

---

### V05 — Distractor Validation

Verify:

- Every distractor represents a realistic misconception.
- Distractors follow the Distractor Engineering rules.
- Distractors are plausible.
- Distractors do not accidentally become correct.

---

### V06 — Answer Validation

Verify:

- The selected correct option matches the explanation.
- The answer is logically correct.
- The explanation fully justifies the answer.

---

### V07 — Difficulty Validation

Verify:

- Difficulty matches the requested level.
- Reasoning complexity is appropriate.
- Difficulty is driven by concepts rather than excessive calculations.

---

### V08 — JSON Validation

Verify:

- Output is valid JSON.
- Required fields are present.
- No additional commentary exists outside the JSON object.

---

## Final Decision

If every validation passes:

Return the JSON.

If any validation fails:

Silently correct the issue before producing the final response.

Never mention that corrections were made.

Never expose intermediate reasoning.

Only return the final validated JSON.
