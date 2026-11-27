"""QP discovery intelligence for the canonical CIRE catalog.

A possibility is a distinct givens-to-unknown reasoning pathway, not a change
of numbers, names or wording. Exact normalized matching is only a first-pass
guard; semantic equivalence must be reviewed by the generator/reviewer.
"""
import json
import re
from pathlib import Path

LEVELS = ("S1", "S2", "S3", "S4")


def _norm(value):
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def register_possibility(path, qp_id, givens, unknown, reasoning_steps, difficulty):
    """Register a concrete possibility beneath an existing QP; never invent a quota."""
    if difficulty not in LEVELS:
        raise ValueError("Difficulty must be S1, S2, S3 or S4")
    if not all(isinstance(v, str) and v.strip() for v in (givens, unknown, reasoning_steps)):
        raise ValueError("Possibility fields must be nonempty")
    data = _read(path)
    qp = next((p for c in data["concepts"] for p in c["patterns"] if p["id"] == qp_id), None)
    if qp is None:
        raise ValueError("Unknown QP ID")
    possibilities = qp.setdefault("possibilities", [])
    signature = tuple(_norm(v) for v in (givens, unknown, reasoning_steps))
    found = next((p for p in possibilities if tuple(_norm(p[k]) for k in ("givens", "unknown", "reasoning_steps")) == signature), None)
    if found is not None:
        if found["difficulty"] != difficulty:
            raise ValueError("Existing possibility has different difficulty; review classification")
        return {"id": found["id"], "created": False}
    used = {p["id"] for p in possibilities}
    index = 1
    while f"{qp_id}_P{index:03d}" in used:
        index += 1
    item = {"id": f"{qp_id}_P{index:03d}", "givens": givens.strip(),
            "unknown": unknown.strip(), "reasoning_steps": reasoning_steps.strip(),
            "difficulty": difficulty, "question_codes": [], "rejections": 0,
            "status": "discovered"}
    possibilities.append(item)
    _write(path, data)
    return {"id": item["id"], "created": True}


def record_outcome(path, possibility_id, question_code=None, rejected=False):
    """Update coverage only after an accepted question is inserted into the canonical bank."""
    if bool(question_code) == bool(rejected):
        raise ValueError("Provide an inserted question_code OR rejected=True")
    data = _read(path)
    p = next((p for c in data["concepts"] for q in c["patterns"]
              for p in q.get("possibilities", []) if p["id"] == possibility_id), None)
    if p is None:
        raise ValueError("Unknown possibility")
    if rejected:
        p["rejections"] += 1
    elif question_code not in p["question_codes"]:
        p["question_codes"].append(question_code)
    p["status"] = "generated" if p["question_codes"] else "discovered"
    _write(path, data)
    return {"id": p["id"], "accepted": len(p["question_codes"]), "rejections": p["rejections"]}


def coverage(path):
    data = _read(path)
    rows = []
    for c in data["concepts"]:
        for q in c["patterns"]:
            possibilities = q.get("possibilities", [])
            rows.append({"concept_id": c["id"], "qp_id": q["id"],
                         "discovered": len(possibilities),
                         "generated": sum(bool(p["question_codes"]) for p in possibilities),
                         "questions": sum(len(p["question_codes"]) for p in possibilities),
                         "by_difficulty": {level: sum(p["difficulty"] == level for p in possibilities)
                                           for level in LEVELS}})
    return {"subtopic": data["subtopic"], "qps": rows}


def test_discovery():
    from tempfile import TemporaryDirectory
    from Engine.integration.cire_catalog_store import upsert_chain
    with TemporaryDirectory() as directory:
        path = Path(directory) / "A1_CH1_ST1.json"
        chain = upsert_chain(path, "A1_CH1_ST1", "Percentage change",
                             "Sequential proportional transformations",
                             "Reverse original value from final value", "Reverse inference")
        args = (path, chain["qp_id"], "Final value and two rates",
                "Original value", "Undo the multipliers in reverse order", "S2")
        first = register_possibility(*args)
        assert first["created"]
        assert register_possibility(*args) == {"id": first["id"], "created": False}
        assert coverage(path)["qps"][0]["discovered"] == 1
        record_outcome(path, first["id"], rejected=True)
        record_outcome(path, first["id"], question_code="TEST_Q001")
        record_outcome(path, first["id"], question_code="TEST_Q001")
        row = coverage(path)["qps"][0]
        assert row["questions"] == 1 and row["generated"] == 1
        assert row["by_difficulty"]["S2"] == 1
        print(json.dumps({"result": "qp_discovery_test_passed", "coverage": row}))


if __name__ == "__main__":
    test_discovery()
