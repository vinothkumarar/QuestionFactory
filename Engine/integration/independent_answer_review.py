"""Independent AI review gate for generated multiple-choice questions.

This is a second model assessment, not formal mathematical proof.
Fail closed on malformed, uncertain or inconsistent reviews.
"""
import json
import re


def verify_questions(client, questions, subject, chapter, subtopic, model="gpt-5"):
    if not questions:
        raise ValueError("Cannot review an empty question batch")
    payload = [
        {key: q[key] for key in (
            "question_text", "option_a", "option_b", "option_c", "option_d",
            "correct_option", "answer", "explanation"
        )} for q in questions
    ]
    prompt = (
        "You are an independent academic QA reviewer. Solve EACH question from "
        "first principles, independently of its provided answer and explanation. "
        "Check arithmetic/algebra, interpretation, option uniqueness, answer-key "
        "correctness, and whether the explanation supports the answer. "
        "Do not assume the supplied key is correct. If ambiguous, unanswerable, "
        "or uncertain, mark fail. Academic context: "
        + json.dumps({"subject": subject, "chapter": chapter, "subtopic": subtopic})
        + "\nQuestions: " + json.dumps(payload, ensure_ascii=False)
        + "\nReturn ONLY a JSON array with exactly one item per input question, "
        "in order. Each item must contain verdict ('pass' or 'fail'), "
        "computed_answer (string), and reason (string). "
        "Pass only when independently computed answer agrees with the keyed "
        "option AND the explanation is mathematically consistent."
    )
    response = client.responses.create(model=model, input=prompt)
    raw = response.output_text.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^\x60{3}(?:json)?\s*|\s*\x60{3}$", "", raw)
    results = json.loads(raw)
    if not isinstance(results, list) or len(results) != len(questions):
        raise RuntimeError("Independent review returned invalid number of verdicts")
    for i, item in enumerate(results, 1):
        if not isinstance(item, dict) or item.get("verdict") not in ("pass", "fail"):
            raise RuntimeError(f"Independent review verdict {i} is invalid")
        if not isinstance(item.get("computed_answer"), str) or not item["computed_answer"].strip():
            raise RuntimeError(f"Independent review answer {i} is missing")
        if not isinstance(item.get("reason"), str) or not item["reason"].strip():
            raise RuntimeError(f"Independent review reasoning {i} is missing")
        if item["verdict"] != "pass":
            raise RuntimeError(f"Independent review rejected question {i}: {item['reason']}")
    return results
