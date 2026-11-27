"""Publish a reviewed Question Factory CSV batch to Exam-Hub as DRAFT records.

Required environment: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY.
Usage: python -m Engine.integration.publish_examhub --csv PATH --subtopic A1_CH1_ST1 --set S1 --limit 5
This intentionally does not auto-approve questions or expose service credentials.
"""
from __future__ import annotations
import argparse
import csv
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import json
from pathlib import Path

FIELDS = ("question_text", "option_a", "option_b", "option_c", "option_d", "correct_option", "answer", "explanation")
DIFFICULTY = {"S1": "Easy", "S2": "Easy+", "S3": "Medium", "S4": "Hard", "S5": "Elite"}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, type=Path)
    parser.add_argument("--subtopic", required=True)
    parser.add_argument("--set", required=True, choices=list(DIFFICULTY))
    parser.add_argument("--limit", required=True, type=int)
    args = parser.parse_args()
    if not 1 <= args.limit <= 20:
        parser.error("Pilot limit must be between 1 and 20")
    base = os.environ.get("SUPABASE_URL", "").rstrip("/")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not base.startswith("https://") or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY secrets required")
    headers = {"apikey": key, "Authorization": "Bearer " + key, "Content-Type": "application/json"}
    def request(path: str, method: str = "GET", payload=None):
        data = None if payload is None else json.dumps(payload).encode()
        h = dict(headers)
        if method == "POST":
            h["Prefer"] = "return=representation"
        req = urllib.request.Request(base + "/rest/v1/" + path, data=data, headers=h, method=method)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read() or b"[]")
    code = urllib.parse.quote(args.subtopic, safe="")
    subtopics = request("subtopics?code=eq." + code + "&select=id,chapter_id,chapters(id,unit_id,units(id,subject_id))")
    if len(subtopics) != 1:
        raise RuntimeError("Master subtopic not found or ambiguous: " + args.subtopic)
    st = subtopics[0]
    ch = st["chapters"]
    unit = ch["units"]
    with args.csv.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    # A mixed-set CSV is rejected rather than silently relabeling its difficulty.
    if len(rows) != args.limit:
        raise RuntimeError(f"Expected exactly {args.limit} CSV rows; found {len(rows)}")
    staged = []
    seen = set()
    for i, row in enumerate(rows, 1):
        missing = [f for f in FIELDS if not str(row.get(f) or "").strip()]
        if missing:
            raise RuntimeError(f"Row {i}: missing {missing}")
        correct = row["correct_option"].strip().upper()
        if correct not in ("A", "B", "C", "D"):
            raise RuntimeError(f"Row {i}: invalid correct_option")
        if row["answer"].strip() != row["option_" + correct.lower()].strip():
            raise RuntimeError(f"Row {i}: answer does not match selected option")
        if row.get("subtopic_id", "").strip() not in ("", args.subtopic, str(st["id"])):
            raise RuntimeError(f"Row {i}: different master subtopic")
        if row.get("difficulty", "").strip() != DIFFICULTY[args.set]:
            raise RuntimeError(f"Row {i}: unexpected difficulty")
        if row.get("set_no", "").strip() not in ("", args.set, args.set[1:]):
            raise RuntimeError(f"Row {i}: unexpected set")
        qcode = (row.get("question_code") or "").strip()
        if not qcode or qcode in seen:
            raise RuntimeError(f"Row {i}: missing or duplicate question_code")
        seen.add(qcode)
        staged.append({
            "question_code": qcode, "subject_id": unit["subject_id"],
            "unit_id": unit["id"], "chapter_id": ch["id"], "subtopic_id": st["id"],
            "question_text": row["question_text"], "option_a": row["option_a"],
            "option_b": row["option_b"], "option_c": row["option_c"], "option_d": row["option_d"],
            "correct_option": correct, "answer": row["answer"], "explanation": row["explanation"],
            "difficulty": DIFFICULTY[args.set], "set_no": args.set,
            "question_type": "Single Correct", "source_type": "AI",
            "status": "DRAFT", "is_verified": False,
        })
    existing = request("questions?question_code=in.(" + ",".join(urllib.parse.quote(x, safe="") for x in seen) + ")&select=question_code")
    if existing:
        raise RuntimeError("Question codes already exist; no rows inserted")
    inserted = request("questions", method="POST", payload=staged)
    if len(inserted) != len(staged):
        raise RuntimeError("Unexpected inserted row count")
    print(json.dumps({"inserted": len(inserted), "subtopic": args.subtopic, "status": "DRAFT", "ids": [x["id"] for x in inserted]}))
    return 0

if __name__ == "__main__":
    sys.exit(main())
