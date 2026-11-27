"""Subtopic-scoped reasoning uniqueness screening.

The caller supplies ONLY questions from the canonical Master subtopic.
Every candidate is checked against its batch and the complete supplied bank.
"""
import json
import re


def question_skeleton(value):
    """Normalize wording and replace numerical values without losing Unicode."""
    value = re.sub(r"\d+(?:[.,]\d+)*", "#", value.casefold())
    return " ".join(re.findall(r"[^\W_]+|#", value, flags=re.UNICODE))


def review_reasoning_uniqueness(client, candidates, existing, model="gpt-5", chunk_size=40):
    if not candidates:
        raise RuntimeError("No questions for reasoning review")
    if not 1 <= chunk_size <= 100:
        raise ValueError("Invalid review chunk size")
    new = [{"id": "new_" + str(i), "question": q["question_text"]}
           for i, q in enumerate(candidates)]
    old = [{"id": "existing_" + str(i), "question": q["question_text"]}
           for i, q in enumerate(existing)]
    all_rows = old + new
    seen = {}
    for row in all_rows:
        key = question_skeleton(row["question"])
        if not key:
            raise RuntimeError("Empty normalized question")
        if key in seen and (row["id"].startswith("new_") or seen[key].startswith("new_")):
            raise RuntimeError("Repeated question structure: " + seen[key] + " and " + row["id"])
        seen[key] = row["id"]

    instructions = (
        "You are a strict mathematical and logical problem-structure duplicate reviewer. "
        "Compare every NEW question to all EXISTING questions in this request, and to other NEW questions. "
        "Changes of numerical values, names, wording, setting, units, or answer choices alone "
        "do NOT make a question unique. If givens-to-unknown relationships, essential reasoning "
        "and solution algorithm are equivalent, mark duplicate. Shared concept alone is NOT a duplicate. "
        "Flag uncertain pairs for review. Return ONLY JSON object with key 'duplicates', an array "
        "of objects with string keys 'new_id', 'matches_id', and 'reason'. "
        "Every pair must include a new question."
    )
    # Check every existing question, not just the first 300. Each call includes
    # the full new batch, so within-batch comparisons are also reviewed.
    chunks = [old[i:i + chunk_size] for i in range(0, len(old), chunk_size)] or [[]]
    for index, chunk in enumerate(chunks, 1):
        corpus = chunk + new
        response = client.responses.create(
            model=model,
            input=instructions + "\n" + json.dumps(corpus, ensure_ascii=False)
                  + "\nReturn only JSON; no markdown.",
        )
        raw = response.output_text.strip()
        if raw.startswith("```"):
            raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw)
        payload = json.loads(raw)
        if not isinstance(payload, dict) or not isinstance(payload.get("duplicates"), list):
            raise RuntimeError("Malformed reasoning review response in chunk " + str(index))
        ids = {row["id"] for row in corpus}
        for pair in payload["duplicates"]:
            if not isinstance(pair, dict) or any(not isinstance(pair.get(k), str) or not pair[k].strip()
                for k in ("new_id", "matches_id", "reason")):
                raise RuntimeError("Malformed reasoning duplicate pair")
            if pair["new_id"] not in ids or pair["matches_id"] not in ids or not pair["new_id"].startswith("new_"):
                raise RuntimeError("Invalid reasoning duplicate IDs")
        if payload["duplicates"]:
            raise RuntimeError("Reasoning-equivalent questions rejected in chunk " + str(index)
                               + ": " + json.dumps(payload["duplicates"][:8], ensure_ascii=False))
    return {"status": "passed", "new_count": len(new),
            "existing_count": len(old), "chunks_reviewed": len(chunks)}
