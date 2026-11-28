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
from pathlib import Path
from Engine.integration.cire_catalog_store import upsert_chain
from Engine.integration.qp_discovery import register_possibility, record_outcome, coverage as qp_coverage
from openai import OpenAI
from Engine.models.generated_question_model import GeneratedQuestionModel
from Engine.quality.option_validator import OptionValidator
from Engine.quality.semantic_validator import SemanticValidator
from Engine.quality.difficulty_validator import DifficultyValidator
from Engine.quality.archetype_validator import ArchetypeValidator
from Engine.integration.independent_answer_review import verify_questions
from Engine.integration.reasoning_uniqueness import find_reasoning_duplicates

def main():
    base=os.environ["SUPABASE_URL"].rstrip("/")
    key=os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    code=os.environ.get("MASTER_SUBTOPIC_CODE","A1_CH1_ST1")
    count=int(os.environ.get("QUESTION_COUNT","5"))
    level=os.environ.get("QUESTION_DIFFICULTY","S1").strip().upper()
    level_to_db={"S1":"Easy","S2":"Medium","S3":"Hard","S4":"Elite"}
    if level not in level_to_db:
        raise ValueError("QUESTION_DIFFICULTY must be S1, S2, S3 or S4")
    level_guidance={"S1":"direct concept application, one clear inference",
                    "S2":"standard application, two linked reasoning steps",
                    "S3":"advanced multi-step reasoning and synthesis",
                    "S4":"non-routine expert reasoning with a genuinely demanding insight"}
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
    # Load the complete canonical-subtopic bank BEFORE generation.
    # This is the only duplicate-comparison scope, regardless of exam mappings.
    existing=[]
    for page in range(100):
        batch=api("questions?subtopic_id=eq."+st["id"]+"&select=question_text,concept_tested,question_archetype&order=id.asc&limit=1000&offset="+str(page*1000))
        existing.extend(batch)
        if len(batch)<1000:
            break
    else:
        raise RuntimeError("Duplicate scan exceeded 100000 existing questions")
    print(json.dumps({"existing_subtopic_questions":len(existing),"subtopic":code}),flush=True)
    # Dynamic CIRE coverage uses only previously accepted canonical-subtopic
    # question metadata. No extra model call or up-front catalog generation.
    from collections import Counter
    concept_counts=Counter((row.get("concept_tested") or "").strip().casefold()
                           for row in existing if (row.get("concept_tested") or "").strip())
    archetype_counts=Counter((row.get("question_archetype") or "").strip().casefold()
                             for row in existing if (row.get("question_archetype") or "").strip())
    coverage={"concepts":dict(concept_counts.most_common(50)),
              "archetypes":dict(archetype_counts.most_common(50))}
    print(json.dumps({"cire_coverage":coverage,"subtopic":code},ensure_ascii=False),flush=True)
    catalog_path=Path("Engine/catalog/cire/master")/(code+".json")
    if catalog_path.exists():
        print(json.dumps({"qp_discovery_coverage":qp_coverage(catalog_path)},ensure_ascii=False),flush=True)
    client=OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt=f"""Generate exactly {count} original {level} ({level_guidance[level]}) multiple-choice questions for the verified Master Syllabus:
Subject: {subj['subject_name']}
Unit: {unit['unit_name']}
Chapter: {ch['chapter_name']}
Subtopic: {st['subtopic_name']}
Use varied scenarios strictly relevant to the named subtopic. Do not force percentage questions unless the subtopic requires percentages. Prefer Indian educational contexts and INR (₹) for money.
Existing questions in this SAME canonical subtopic (do not reproduce their reasoning structures):
{json.dumps([row["question_text"] for row in existing], ensure_ascii=False)}
For EACH proposed question, first plan internally:
- CONCEPT: the specific knowledge relationship being tested, not merely the chapter title.
- QP (question pattern): the precise givens-to-unknown structure and solution pathway.
- ARCHETYPE: the broad reasoning presentation (e.g. reverse inference, comparison, multi-step deduction, application).
Diversify CONCEPT and QP selections across this batch. Prefer underrepresented concepts and
reasoning structures relative to the existing canonical-subtopic questions above. Do not
force an artificial concept when the syllabus scope is narrow. An archetype label alone
does not make a repeated problem unique.
Current canonical-subtopic coverage (historical labels are approximate, not formal catalog IDs):\n{json.dumps(coverage, ensure_ascii=False)}\nPrefer meaningful gaps, without inventing artificial distinctions.\nDesign NEW givens-to-unknown relationships, inference steps and solution strategies.
Do NOT merely change values, names, wording, currencies, or contexts. Reusing a concept is allowed,
but reusing the same mathematical question pattern is not. If the topic has no remaining genuinely
distinct S1 patterns, generation must fail rather than invent cosmetic variants.
Each must have exactly four distinct, plausible options, one mathematically correct option, an exact answer text matching that option, and a clear worked explanation. No duplicate questions. Do not include markdown.
Return ONLY a JSON array of objects with keys question_text, option_a, option_b, option_c, option_d, correct_option (A/B/C/D), answer, explanation, concept_tested, concept_definition, question_pattern, question_archetype, possibility_givens, possibility_unknown, possibility_reasoning_steps. For the possibility fields describe the abstract givens, target unknown and distinctive reasoning pathway independent of numerical values. Avoid cosmetic variants.\nThe question_pattern must describe the actual givens-to-unknown relationship, not a generic label.
"""
    max_attempts=int(os.environ.get("UNIQUENESS_MAX_ATTEMPTS","3"))
    if not 1<=max_attempts<=5:
        raise ValueError("UNIQUENESS_MAX_ATTEMPTS must be between 1 and 5")
    accepted_questions=[]
    metrics={"difficulty":level,"generated_candidates":0,"format_rejected":0,"duplicates_rejected":0,"answer_rejected":0,"validator_rejected":0,"attempts":0}
    feedback=""
    for attempt in range(1,max_attempts+1):
        needed=count-len(accepted_questions)
        if needed==0:
            break
        generation_prompt=prompt.replace("Generate exactly "+str(count), "Generate exactly "+str(needed))
        generation_prompt += (
            "\nAlready accepted questions in this batch; do not repeat their reasoning: "
            +json.dumps([q["question_text"] for q in accepted_questions],ensure_ascii=False)
            +feedback
        )
        response=client.responses.create(model=os.environ.get("OPENAI_MODEL","gpt-5"),input=generation_prompt)
        raw=response.output_text.strip()
        if raw.startswith("```"):
            raw=re.sub(r"^```(?:json)?\s*|\s*```$","",raw)
        candidates=json.loads(raw)
        metrics["attempts"]+=1
        if not isinstance(candidates,list) or len(candidates)!=needed:
            raise RuntimeError("Wrong question count")
        required=("question_text","option_a","option_b","option_c","option_d",
                  "correct_option","answer","explanation","concept_tested","concept_definition","question_pattern","question_archetype","possibility_givens","possibility_unknown","possibility_reasoning_steps")
        metrics["generated_candidates"]+=len(candidates)
        structurally_valid=[]
        for q in candidates:
            if any(not isinstance(q.get(k),str) or not q[k].strip() for k in required):
                continue
            options=[q["option_"+x] for x in "abcd"]
            key=q["correct_option"].strip().upper()
            if (len({x.strip().casefold() for x in options})!=4 or key not in "ABCD"
                or q["answer"].strip()!=q["option_"+key.lower()].strip()):
                continue
            structurally_valid.append(q)
        metrics["format_rejected"]+=len(candidates)-len(structurally_valid)
        print(json.dumps({"attempt":attempt,"requested":needed,
                          "format_valid":len(structurally_valid)}),flush=True)
        if structurally_valid:
            # Existing includes ONLY the canonical Master subtopic. Accepted
            # questions are treated as existing to prevent repeat selection.
            comparison_bank=existing+[{"question_text":q["question_text"]} for q in accepted_questions]
            decision=find_reasoning_duplicates(client,structurally_valid,comparison_bank,
                            model=os.environ.get("REVIEW_MODEL","gpt-5"))
            rejected=set(decision["rejected_indices"])
            metrics["duplicates_rejected"]+=len(rejected)
            feedback="\nAvoid these rejected reasoning patterns: "+json.dumps(decision["reasons"],ensure_ascii=False)
            for i,q in enumerate(structurally_valid):
                if i in rejected:
                    continue
                # Independent mathematical verification of each survivor.
                try:
                    verify_questions(client,[q],subj["subject_name"],ch["chapter_name"],
                        st["subtopic_name"],model=os.environ.get("REVIEW_MODEL","gpt-5"))
                except (RuntimeError,ValueError) as exc:
                    metrics["answer_rejected"]+=1
                    print(json.dumps({"answer_rejected":i,"reason":str(exc)[:250]}),flush=True)
                    continue
                accepted_questions.append(q)
            print(json.dumps({"attempt":attempt,"duplicates_rejected":len(rejected),
                "accepted_total":len(accepted_questions),"pending":count-len(accepted_questions)}),flush=True)
    if not accepted_questions:
        print(json.dumps({"result":"no_unique_questions","metrics":metrics,"count":0,"requested":count,
                          "pending":count,"master_subtopic":code}),flush=True)
        return
    questions=accepted_questions
    seen=set()
    records=[]
    def normalized_text(value):
        return " ".join(re.findall("[a-z0-9]+",value.casefold()))
    def near_duplicate(a,b):
        a,b=normalized_text(a),normalized_text(b)
        return bool(a and b and (a==b or SequenceMatcher(None,a,b,autojunk=False).ratio()>=0.995))
    validators=(OptionValidator(),SemanticValidator(),DifficultyValidator(),ArchetypeValidator())
    for i,q in enumerate(accepted_questions,1):
        required=("question_text","option_a","option_b","option_c","option_d","correct_option","answer","explanation","concept_tested","question_pattern","question_archetype")
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
            difficulty=level_to_db[level],archetype="Computational",
            concept=q["concept_tested"],source_type="AI",
            metadata={"question_pattern":q["question_pattern"],"question_archetype":q["question_archetype"]},
        )
        valid=True
        for validator in validators:
            report=validator.validate(model)
            if not report.passed or report.errors:
                print(json.dumps({"validator_rejected":i,"validator":validator.__class__.__name__,
                                  "errors":str(report.errors)[:300]}),flush=True)
                valid=False
                break
            if report.warnings:
                print(f"QUALITY WARNING question={i} validator={validator.__class__.__name__}: {report.warnings}",flush=True)
        if not valid:
            metrics["validator_rejected"]+=1
            continue
        records.append({"question_code":model.question_code,
            "subject_id":subj["id"],"unit_id":unit["id"],"chapter_id":ch["id"],"subtopic_id":st["id"],
            "question_text":q["question_text"],"option_a":q["option_a"],"option_b":q["option_b"],"option_c":q["option_c"],"option_d":q["option_d"],
            "correct_option":answer_key,"answer":q["answer"],"explanation":q["explanation"],
            "concept_tested":q["concept_tested"],"question_archetype":q["question_archetype"],
            "difficulty":level_to_db[level],"set_no":1,"question_type":"Single Correct","source_type":"AI",
            "status":"draft","is_verified":False})

    print(json.dumps({"unique_validated":len(records),"requested":count,
                      "pending":count-len(records),"master_subtopic":code}),flush=True)
    # Structural validation is not mathematical proof; drafts require review.
    if os.environ.get("DRY_RUN","false").lower() in ("1","true","yes"):
        print(json.dumps({"result":"validated_dry_run","metrics":metrics,"count":len(records),"requested":count,"pending":count-len(records),"master_subtopic":code,"question_codes":[q["question_code"] for q in records]}))
        return
    if not records:
        print(json.dumps({"result":"no_valid_drafts","metrics":metrics,"count":0,"requested":count,
                          "pending":count,"master_subtopic":code}),flush=True)
        return
    inserted=api("questions","POST",records)
    if len(inserted)!=len(records):
        raise RuntimeError("Unexpected insert count")
    # Catalog updates follow successful Supabase insertion, never a dry run.
    # Pair validated records with their original source questions by text.
    source_by_text={q["question_text"]:q for q in accepted_questions}
    for record in records:
        q=source_by_text[record["question_text"]]
        chain=upsert_chain(catalog_path,code,q["concept_tested"],q["concept_definition"],
                           q["question_pattern"],q["question_archetype"])
        possibility=register_possibility(catalog_path,chain["qp_id"],
                     q["possibility_givens"],q["possibility_unknown"],
                     q["possibility_reasoning_steps"],level)
        record_outcome(catalog_path,possibility["id"],question_code=record["question_code"])
    print(json.dumps({"catalog_updated":str(catalog_path),
                      "qp_discovery_coverage":qp_coverage(catalog_path)},ensure_ascii=False),flush=True)
    print(json.dumps({"result":"drafts_inserted","metrics":metrics,"count":len(inserted),"requested":count,
                      "pending":count-len(inserted),"master_subtopic":code,
                      "ids":[q["id"] for q in inserted]}))
if __name__=="__main__":
    try:
        main()
    except Exception as ex:
        print("PILOT FAILED:",type(ex).__name__,str(ex),file=sys.stderr)
        sys.exit(1)
