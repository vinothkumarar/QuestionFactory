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


def find_reasoning_duplicates(client, candidates, existing, model="gpt-5", chunk_size=40):
    """Return rejected candidate indexes, keeping earlier candidate on ties."""
    if not 1 <= chunk_size <= 100:
        raise ValueError("Invalid chunk size")
    new = [{"id": "new_" + str(i), "question": q["question_text"]} for i,q in enumerate(candidates)]
    old = [{"id": "existing_" + str(i), "question": q["question_text"]} for i,q in enumerate(existing)]
    rejected = set()
    reasons = []
    seen = {}
    for row in old + new:
        key = question_skeleton(row["question"])
        if not key:
            raise RuntimeError("Empty normalized question")
        if key in seen and row["id"].startswith("new_"):
            rejected.add(int(row["id"].split("_")[1]))
            reasons.append("Identical normalized structure: " + row["id"] + " vs " + seen[key])
        else:
            seen.setdefault(key, row["id"])
    instructions = (
        "Review mathematical/logical problem-structure equivalence. Compare NEW to EXISTING "
        "and NEW to NEW. Differences only in numbers, setting, wording, names, units or options "
        "are duplicates if givens-to-unknown relation and essential reasoning are the same. "
        "Shared concept alone is not duplication. Flag uncertain matches. "
        "Return ONLY JSON object with 'duplicates': array of objects with string "
        "'new_id', 'matches_id', 'reason'. Each pair must involve a new question."
    )
    chunks = [old[i:i+chunk_size] for i in range(0,len(old),chunk_size)] or [[]]
    # Review against all existing questions and all candidate peers; do not
    # depend on the order in which model reports equivalent pairs.
    pairs = []
    for chunk in chunks:
        corpus = chunk + new
        response = client.responses.create(
            model=model, input=instructions+"\n"+json.dumps(corpus,ensure_ascii=False)+"\nReturn only JSON.")
        raw = response.output_text.strip()
        if raw.startswith("```"):
            raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw)
        payload = json.loads(raw)
        if not isinstance(payload,dict) or not isinstance(payload.get("duplicates"),list):
            raise RuntimeError("Malformed uniqueness review")
        ids = {r["id"] for r in corpus}
        for pair in payload["duplicates"]:
            if not isinstance(pair,dict) or any(not isinstance(pair.get(k),str) or not pair[k].strip()
                for k in ("new_id","matches_id","reason")):
                raise RuntimeError("Malformed uniqueness match")
            x,y = pair["new_id"],pair["matches_id"]
            if x not in ids or y not in ids or not x.startswith("new_") or x==y:
                raise RuntimeError("Invalid uniqueness match IDs")
            pairs.append((x,y,pair["reason"]))
    # An existing match always disqualifies a new candidate. Within new
    # candidates, retain the earliest viable candidate in each duplicate pair.
    for x,y,reason in pairs:
        if y.startswith("existing_"):
            rejected.add(int(x.split("_")[1]))
            reasons.append(reason)
    for x,y,reason in pairs:
        if y.startswith("new_"):
            ix,iy = int(x.split("_")[1]),int(y.split("_")[1])
            if ix not in rejected and iy not in rejected:
                rejected.add(max(ix,iy))
                reasons.append(reason)
    return {"rejected_indices":sorted(rejected),"reasons":reasons[:30],
            "reviewed":len(new),"existing_count":len(old),"chunks_reviewed":len(chunks)}


def review_reasoning_uniqueness(client, candidates, existing, model="gpt-5", chunk_size=40):
    result = find_reasoning_duplicates(client,candidates,existing,model,chunk_size)
    if result["rejected_indices"]:
        raise RuntimeError("Reasoning-equivalent questions rejected: "+json.dumps(result))
    return {"status":"passed","new_count":len(candidates),
            "existing_count":len(existing),"chunks_reviewed":result["chunks_reviewed"]}
