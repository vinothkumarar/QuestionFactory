"""ExamHub master-driven five-question pilot.

Uses the live canonical Supabase Master Syllabus and OpenAI to generate a
small S1 draft batch. Does not modify the legacy Question Factory engine.
"""
import json
from difflib import SequenceMatcher
import os
import re
import sys
import urllib.parse
import urllib.request
import urllib.error
import uuid
from openai import OpenAI
from Engine.models.generated_question_model import GeneratedQuestionModel
from Engine.quality.option_validator import OptionValidator
from Engine.quality.semantic_validator import SemanticValidator
from Engine.quality.difficulty_validator import DifficultyValidator
from Engine.quality.archetype_validator import ArchetypeValidator
from Engine.integration.independent_answer_review import verify_questions

def main():
    base=os.environ["SUPABASE_URL"].rstrip("/")
    key=os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    code=os.environ.get("MASTER_SUBTOPIC_CODE","A1_CH1_ST1")
    count=int(os.environ.get("QUESTION_COUNT","5"))
    if not 1<=count<=20 or not re.fullmatch(r"[A-Za-z0-9_]+",code):
        raise ValueError("Invalid pilot inputs")
    # Validate legacy JWT role without exposing the secret.
    if key.count(".")==2:
        import base64
        part=key.split(".")[1]
        claims=json.loads(base64.urlsafe_b64decode(part+"="*(-len(part)%4)))
        if claims.get("role")!="service_role":
            raise RuntimeError("GitHub SUPABASE_SERVICE_ROLE_KEY is not a service_role key; replace the secret, do not weaken RLS.")
    headers={"apikey":key,"Authorization":"Bearer "+key,"Content-Type":"application/json"}
    def api(path,method="GET",payload=None):
        req=urllib.request.Request(base+"/rest/v1/"+path,headers={**headers,**({"Prefer":"return=representation"} if method=="POST" else {})},data=None if payload is None else json.dumps(payload).encode(),method=method)
        try:
            with urllib.request.urlopen(req,timeout=45) as resp:
                return json.loads(resp.read() or b"[]")
        except urllib.error.HTTPError as exc:
            detail=exc.read().decode("utf-8",errors="replace")[:1200]
            raise RuntimeError(f"Supabase REST {method} {path.split('?')[0]} HTTP {exc.code}: {detail}") from exc
    def get_one(table, column, value, select):
        rows=api(table+"?"+column+"=eq."+urllib.parse.quote(str(value),safe="")+"&select="+select)
        if not isinstance(rows,list) or len(rows)!=1:
            raise RuntimeError("Master lookup failed for "+table+" ("+column+")")
        return rows[0]
    # Explicit FK traversal avoids fragile nested REST embedding.
    st=get_one("subtopics","code",code,"id,code,subtopic_name,chapter_id")
    ch=get_one("chapters","id",st["chapter_id"],"id,code,chapter_name,unit_id")
    unit=get_one("units","id",ch["unit_id"],"id,code,unit_name,subject_id")
    try:
        subj=get_one("subjects","id",unit["subject_id"],"id,subject_name")
    except RuntimeError as exc:
        raise RuntimeError("Subject inaccessible: verify GitHub SUPABASE_SERVICE_ROLE_KEY uses the real service_role/secret key for the SUPABASE_URL project. Do not change RLS.") from exc
    if not all([st["subtopic_name"],ch["chapter_name"],unit["unit_name"],subj["subject_name"]]):
        raise RuntimeError("Master syllabus names incomplete")
    print("MASTER VERIFIED:",subj["subject_name"],unit["code"],ch["code"],st["code"],flush=True)
    client=OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt=f"""Generate exactly {count} original easy (S1 foundation) multiple-choice questions for the verified Master Syllabus:
Subject: {subj['subject_name']}
Unit: {unit['unit_name']}
Chapter: {ch['chapter_name']}
Subtopic: {st['subtopic_name']}
Use varied scenarios strictly relevant to the named subtopic. Do not force percentage questions unless the subtopic requires percentages. Prefer Indian educational contexts and INR (₹) for money.
Each must have exactly four distinct, plausible options, one mathematically correct option, an exact answer text matching that option, and a clear worked explanation. No duplicate questions. Do not include markdown.
Return ONLY a JSON array of objects with keys question_text, option_a, option_b, option_c, option_d, correct_option (A/B/C/D), answer, explanation, concept_tested, question_archetype.
"""
    response=client.responses.create(model=os.environ.get("OPENAI_MODEL","gpt-5"),input=prompt)
    raw=response.output_text.strip()
    if raw.startswith("```"):
        raw=re.sub(r"^\`\`\`(?:json)?\s*|\s*\`\`\`$","",raw)
    questions=json.loads(raw)
    if not isinstance(questions,list) or len(questions)!=count:
        raise RuntimeError("Wrong question count")
    seen=set(); records=[]
    def normalized_text(value):
        return re.sub(r"[^\\w]+", " ", value.casefold()).strip()
    def near_duplicate(a, b):
        a, b = normalized_text(a), normalized_text(b)
        if not a or not b:
            return False
        if a == b:
            return True
        # Similar phrasing alone is insufficient: different numerical inputs
        # can represent distinct practice questions in the same archetype.
        numbers_a = re.findall(r"\\d+(?:\\.\\d+)?", a)
        numbers_b = re.findall(r"\\d+(?:\\.\\d+)?", b)
        if numbers_a != numbers_b:
            return False
        return SequenceMatcher(None, a, b, autojunk=False).ratio() >= 0.98
    validators=(OptionValidator(), SemanticValidator(), DifficultyValidator(), ArchetypeValidator())
    for i,q in enumerate(questions,1):
        required=("question_text","option_a","option_b","option_c","option_d","correct_option","answer","explanation","concept_tested","question_archetype")
        if any(not isinstance(q.get(f),str) or not q[f].strip() for f in required):
            raise RuntimeError(f"Question {i}: missing required fields")
        options=[q["option_"+x] for x in "abcd"]
        if len(set(x.strip().casefold() for x in options))!=4:
            raise RuntimeError(f"Question {i}: duplicate options")
        answer_key=q["correct_option"].strip().upper()
        if answer_key not in "ABCD" or q["answer"].strip()!=q["option_"+answer_key.lower()].strip():
            raise RuntimeError(f"Question {i}: answer mismatch")
        normalized=q["question_text"].strip().casefold()
        if normalized in seen or any(near_duplicate(q["question_text"], previous["question_text"]) for previous in records):
            raise RuntimeError(f"Question {i}: duplicate or near-duplicate within batch")
        seen.add(normalized)
        # Adapt the Supabase payload to the existing Question Factory OS model.
        # Archetype Validator expects a canonical family, while the generated
        # question_archetype is a more specific descriptive subtype.
        model=GeneratedQuestionModel(
            question_code=code+"_Q"+uuid.uuid4().hex[:16].upper(),
            unit_code=unit["code"],chapter_code=ch["code"],subtopic_code=st["code"],
            set_number=1,question_text=q["question_text"],options=options,
            correct_option=answer_key,explanation=q["explanation"],
            difficulty="Easy",archetype="Computational",
            concept=q["concept_tested"],source_type="AI",
            metadata={"question_archetype":q["question_archetype"]},
        )
        for validator in validators:
            report=validator.validate(model)
            if not report.passed or report.errors:
                raise RuntimeError(f"Question {i} failed {validator.__class__.__name__}: {report.errors}")
            if report.warnings:
                print(f"QUALITY WARNING question={i} validator={validator.__class__.__name__}: {report.warnings}",flush=True)
        records.append({"question_code":model.question_code,
            "subject_id":subj["id"],"unit_id":unit["id"],"chapter_id":ch["id"],"subtopic_id":st["id"],
            "question_text":q["question_text"],"option_a":q["option_a"],"option_b":q["option_b"],"option_c":q["option_c"],"option_d":q["option_d"],
            "correct_option":answer_key,"answer":q["answer"],"explanation":q["explanation"],
            "concept_tested":q["concept_tested"],"question_archetype":q["question_archetype"],
            "difficulty":"Easy","set_no":1,"question_type":"Single Correct","source_type":"AI",
            "status":"draft","is_verified":False})
    # Fail closed if an identical question already exists in this subtopic.
    existing=[]
    for page in range(100):
        batch=api("questions?subtopic_id=eq."+st["id"]+"&select=question_text&order=id.asc&limit=1000&offset="+str(page*1000))
        existing.extend(batch)
        if len(batch)<1000:
            break
    else:
        raise RuntimeError("Duplicate scan exceeded 100000 existing questions; refusing incomplete scan")
    for candidate in records:
        if any(near_duplicate(candidate["question_text"], prior["question_text"]) for prior in existing):
            raise RuntimeError("A duplicate or near-duplicate question already exists in Supabase")
    # An independent model reviews answers before even a dry-run can pass.
    # This is additional evidence, not a mathematical proof or publication approval.
    review=verify_questions(
        client,questions,subj["subject_name"],ch["chapter_name"],
        st["subtopic_name"],model=os.environ.get("REVIEW_MODEL","gpt-5"),
    )
    print(json.dumps({"independent_review":"passed","count":len(review)}),flush=True)
    # Structural validation is not mathematical proof; drafts require review.
    if os.environ.get("DRY_RUN","false").lower() in ("1","true","yes"):
        print(json.dumps({"result":"validated_dry_run","count":len(records),"master_subtopic":code,"question_codes":[q["question_code"] for q in records]}))
        return
    inserted=api("questions","POST",records)
    if len(inserted)!=count:
        raise RuntimeError("Unexpected insert count")
    print(json.dumps({"result":"drafts_inserted","count":len(inserted),"master_subtopic":code,"ids":[q["id"] for q in inserted]}))
if __name__=="__main__":
    try:
        main()
    except Exception as ex:
        print("PILOT FAILED:",type(ex).__name__,str(ex),file=sys.stderr)
        sys.exit(1)
