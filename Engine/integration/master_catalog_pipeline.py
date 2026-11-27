"""Master Syllabus catalog pipeline: Concept -> QP -> Archetype.

Standalone dry-run prototype. No Supabase writes or question publication.
Reuses the existing catalog prompt generators.
"""
import json
import os
import re
import urllib.parse
import urllib.request
from openai import OpenAI
from Engine.catalog.concept_catalog.concept_catalog_generator import ConceptCatalogGenerator
from Engine.catalog.qp_catalog.qp_catalog_generator import QPCatalogGenerator
from Engine.catalog.archetype_catalog.archetype_catalog_generator import ArchetypeCatalogGenerator


def main():
    code = os.environ.get("MASTER_SUBTOPIC_CODE", "A1_CH1_ST1")
    if not re.fullmatch("[A-Za-z0-9_]+", code):
        raise ValueError("Invalid canonical subtopic code")
    base = os.environ["SUPABASE_URL"].rstrip("/")
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    def one(table, column, value, select):
        url = base + "/rest/v1/" + table + "?" + column + "=eq." + urllib.parse.quote(str(value), safe="") + "&select=" + select
        req = urllib.request.Request(url, headers={"apikey": key, "Authorization": "Bearer " + key})
        with urllib.request.urlopen(req, timeout=45) as resp:
            rows = json.load(resp)
        if len(rows) != 1:
            raise RuntimeError("Canonical master lookup failed: " + table)
        return rows[0]
    st = one("subtopics", "code", code, "id,subtopic_name,chapter_id")
    ch = one("chapters", "id", st["chapter_id"], "chapter_name,unit_id")
    unit = one("units", "id", ch["unit_id"], "unit_name,subject_id")
    subj = one("subjects", "id", unit["subject_id"], "subject_name")
    context = dict(subject=subj["subject_name"], unit=unit["unit_name"],
                   chapter=ch["chapter_name"], subtopic=st["subtopic_name"])
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.environ.get("OPENAI_MODEL", "gpt-5")
    def generate(prompt, parser):
        response = client.responses.create(model=model, input=prompt + "\nReturn ONLY a JSON array. No markdown.")
        raw = response.output_text.strip()
        if raw.startswith("```"):
            raw = re.sub("^\\x60{3}(?:json)?\\s*|\\s*\\x60{3}$", "", raw)
        rows = parser.parse_response(raw)
        if not rows or not all(isinstance(x, dict) for x in rows):
            raise RuntimeError("Empty or invalid catalog")
        return rows
    concept_gen = ConceptCatalogGenerator()
    qp_gen = QPCatalogGenerator()
    archetype_gen = ArchetypeCatalogGenerator()
    concepts = generate(concept_gen.load_prompt(**context), concept_gen)
    max_concepts = int(os.environ.get("CATALOG_CONCEPT_LIMIT", "1"))
    if not 1 <= max_concepts <= 5:
        raise ValueError("CATALOG_CONCEPT_LIMIT must be 1..5")
    output = []
    for concept in concepts[:max_concepts]:
        concept_id = concept.get("concept_id")
        concept_text = concept.get("concept")
        if not isinstance(concept_id, str) or not isinstance(concept_text, str) or not concept_id.strip() or not concept_text.strip():
            raise RuntimeError("Concept missing canonical catalog fields")
        qps = generate(qp_gen.load_prompt(**context, concept_id=concept_id, concept=concept_text), qp_gen)
        qp = qps[0]
        qp_id = qp.get("qp_id")
        possibility = qp.get("question_possibility")
        if not isinstance(qp_id, str) or not isinstance(possibility, str) or not qp_id.strip() or not possibility.strip():
            raise RuntimeError("QP missing expected fields")
        archetypes = generate(archetype_gen.load_prompt(**context, concept_id=concept_id, concept=concept_text,
                                  qp_id=qp_id, question_possibility=possibility), archetype_gen)
        output.append({"concept": concept, "qp": qp, "archetype_count": len(archetypes),
                       "archetype_sample": archetypes[0]})
    print(json.dumps({"result": "catalog_dry_run", "master_subtopic": code,
                      "concepts_generated": len(concepts), "chains_checked": output}, ensure_ascii=False))


if __name__ == "__main__":
    main()
