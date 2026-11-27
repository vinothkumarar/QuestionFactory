"""Fail-closed reasoning-level duplicate review for generated MCQs.

A model's judgement is a screening aid, not a proof of uniqueness.
"""
import json
import re


def review_reasoning_uniqueness(client, candidates, existing, model="gpt-5"):
    """Reject equivalent reasoning patterns in batch or the existing bank.

    Existing rows must include question_text; a bounded review avoids silent
    partial coverage. Fail closed if review cannot be completed.
    """
    if len(existing) > 300:
        raise RuntimeError("Reasoning review bank exceeds 300 questions; chunked review required")
    if not candidates:
        raise RuntimeError("No questions for reasoning review")
    corpus = [{"id": "existing_" + str(i), "question": q["question_text"]}
              for i, q in enumerate(existing)]
    corpus += [{"id": "new_" + str(i), "question": q["question_text"]}
               for i, q in enumerate(candidates)]
    # Deterministic first-pass catches cosmetic number changes.
    def skeleton(s):
        s = re.sub(r"\\d+(?:[.,]\\d+)*", "#", s.casefold())
        return " ".join(re.findall(r"[^\\W_]+|#", s, flags=re.UNICODE))
    seen = {}
    for row in corpus:
        key = skeleton(row["question"])
        if key in seen and (row["id"].startswith("new_") or seen[key].startswith("new_")):
            raise RuntimeError("Repeated question skeleton: " + seen[key] + " and " + row["id"])
        seen[key] = row["id"]
    instructions = (
        "You are a strict mathematical problem-structure duplicate reviewer. "
        "Compare every NEW question against every other NEW question and every EXISTING question. "
        "Treat changes of names, wording, scenario, numerical constants, units or answer choices "
        "as the SAME problem if the essential givens-to-unknown relationship, reasoning steps, "
        "and solution algorithm are unchanged. Shared concept alone does NOT make questions duplicates. "
        "Return JSON object with key 'duplicates', an array of objects containing 'new_id', "
        "'matches_id', and 'reason'. Every pair must include at least one new question. "
        "If uncertain whether two questions are meaningfully distinct, flag the pair."
    )
    response = client.responses.create(model=model, input=instructions + "\n" + json.dumps(corpus, ensure_ascii=False)
                                     + "\nReturn ONLY valid JSON, no markdown.")
    raw = response.output_text.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^\\x60{3}(?:json)?\\s*|\\s*\\x60{3}$", "", raw)
    payload = json.loads(raw)
    if not isinstance(payload, dict) or not isinstance(payload.get("duplicates"), list):
        raise RuntimeError("Invalid reasoning uniqueness review output")
    valid_ids = {row["id"] for row in corpus}
    for pair in payload["duplicates"]:
        if not isinstance(pair, dict) or any(not isinstance(pair.get(k), str) for k in ("new_id", "matches_id", "reason")):
            raise RuntimeError("Malformed reasoning duplicate pair")
        if pair["new_id"] not in valid_ids or pair["matches_id"] not in valid_ids or not pair["new_id"].startswith("new_"):
            raise RuntimeError("Invalid reasoning duplicate IDs")
    if payload["duplicates"]:
        raise RuntimeError("Reasoning-equivalent questions rejected: " + json.dumps(payload["duplicates"][:8], ensure_ascii=False))
    return {"status": "passed", "new_count": len(candidates), "existing_count": len(existing)}
