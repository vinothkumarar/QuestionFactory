"""Controlled chapter-level Question Factory runner using existing pilot validation.

Runs one subtopic per child process. Defaults to dry-run; publication never occurs.
"""
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request


def main():
    chapter = os.environ.get("MASTER_CHAPTER_CODE", "").strip()
    if not re.fullmatch(r"[A-Za-z0-9_]+", chapter):
        raise ValueError("MASTER_CHAPTER_CODE must be a valid canonical chapter code")
    limit = int(os.environ.get("SUBTOPIC_LIMIT", "5"))
    offset = int(os.environ.get("SUBTOPIC_OFFSET", "0"))
    count = int(os.environ.get("QUESTION_COUNT", "5"))
    if not 1 <= limit <= 20 or not 1 <= count <= 20 or not 0 <= offset <= 10000:
        raise ValueError("Limits must be between 1 and 20")
    base = os.environ["SUPABASE_URL"].rstrip("/")
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    headers = {"apikey": key, "Authorization": "Bearer " + key}
    def get(path):
        request = urllib.request.Request(base + "/rest/v1/" + path, headers=headers)
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.load(response)
    chapters = get("chapters?code=eq." + urllib.parse.quote(chapter, safe="") + "&select=id,code")
    if len(chapters) != 1:
        raise RuntimeError("Chapter not uniquely found in Master Syllabus")
    subtopics = get("subtopics?chapter_id=eq." + chapters[0]["id"] +
                    "&select=id,code,subtopic_name&order=code.asc&limit=" + str(limit) + "&offset=" + str(offset))
    if not subtopics:
        raise RuntimeError("No Master Syllabus subtopics found")
    expected = os.environ.get("EXPECTED_FIRST_SUBTOPIC", "").strip()
    if expected and subtopics[0]["code"] != expected:
        raise RuntimeError(f"Wrong target: expected first subtopic {expected}, got {subtopics[0]['code']}. Nothing generated.")
    dry_run = os.environ.get("DRY_RUN", "true").lower() not in ("false", "0", "no")
    print(json.dumps({"chapter": chapter, "subtopics": [s["code"] for s in subtopics],
                      "per_subtopic": count, "offset": offset, "expected_first": expected, "dry_run": dry_run}), flush=True)
    results = []
    for st in subtopics:
        env = os.environ.copy()
        env["MASTER_SUBTOPIC_CODE"] = st["code"]
        env["QUESTION_COUNT"] = str(count)
        env["DRY_RUN"] = "true" if dry_run else "false"
        print("START SUBTOPIC:", st["code"], flush=True)
        result = subprocess.run([sys.executable, "-m", "Engine.integration.master_syllabus_pilot"],
                                env=env, check=False)
        results.append({"subtopic": st["code"], "passed": result.returncode == 0})
        if result.returncode:
            print("SUBTOPIC FAILED: continuing to next independent subtopic", file=sys.stderr, flush=True)
    print("BULK SUMMARY:", json.dumps(results), flush=True)
    if any(not r["passed"] for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
