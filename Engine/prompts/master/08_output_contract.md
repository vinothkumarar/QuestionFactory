# PART 8 — OUTPUT CONTRACT

## Objective

The AI shall return output that can be consumed directly by
Question Factory OS.

Return STRICT JSON only.

Do not return:

- Markdown
- Code fences
- Bullet lists
- Explanatory text
- Additional commentary

The response must contain exactly one JSON object.

---

## JSON Rules

The JSON must be:

- Valid
- UTF-8 compatible
- Properly escaped
- Parseable using Python json.loads()

---

## Required Fields

The following fields are mandatory.

{
    "question_text": "",
    "option_a": "",
    "option_b": "",
    "option_c": "",
    "option_d": "",
    "correct_option": "",
    "answer": "",
    "explanation": "",

    "difficulty": "",
    "difficulty_score": 0,

    "question_type": "MCQ",
    "answer_type": "Single Correct",

    "concept_tested": "",
    "question_archetype": "",

    "estimated_time_sec": 0,

    "bloom_level": "",

    "exam_level": "JEE Main + Advanced",

    "source_type": "AI Generated",

    "tags": []
}

---

## Field Rules

question_text

- Clear.
- Grammatically correct.
- Self-contained.

options

- Four options.
- Mutually exclusive.
- Similar style and length where appropriate.

correct_option

Allowed values:

A
B
C
D

answer

A concise justification of the correct option.

explanation

A detailed educational explanation.

difficulty

Allowed values:

- Foundation
- Easy+
- Medium
- Hard
- Elite

difficulty_score

Allowed values:

1
2
3
4
5

estimated_time_sec

Positive integer.

tags

Return an array of keywords.

Example:

[
    "measurement",
    "error analysis",
    "significant figures"
]

---

## Forbidden Output

Never return:

- Invalid JSON
- Missing fields
- Duplicate options
- Empty explanations
- Multiple correct answers
