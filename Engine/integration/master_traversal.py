"""Master syllabus traversal, validation-only, resumable across chapters."""
import json, os, re, subprocess, sys, urllib.parse, urllib.request
from pathlib import Path

STATE=Path("Engine/catalog/rounds/master_traversal_state.json")
REPORT=Path("artifacts/master_traversal_summary.json")

def main():
 subject=os.getenv("MASTER_SUBJECT_CODE","ALL").strip()
 level=os.getenv("QUESTION_DIFFICULTY","S1").strip()
 round_no=int(os.getenv("GENERATION_ROUND","1"))
 limit=int(os.getenv("SUBTOPIC_LIMIT","1"))
 count=int(os.getenv("QUESTION_COUNT","1"))
 max_batches=int(os.getenv("MAX_BATCHES","2"))
 resume=os.getenv("RESUME","false").lower()=="true"
 if not re.fullmatch(r"[A-Za-z0-9_]{1,40}",subject) or level not in ("S1","S2","S3","S4"):
  raise ValueError("Invalid subject or difficulty")
 if not (1<=round_no<=1000 and 1<=limit<=20 and 1<=count<=20 and 1<=max_batches<=20):
  raise ValueError("Invalid batch bounds")
 config=dict(subject=subject,difficulty=level,round_number=round_no,subtopics_per_batch=limit,questions_per_subtopic=count,dry_run=True)
 base=os.environ["SUPABASE_URL"].rstrip("/")
 key=os.environ["SUPABASE_SERVICE_ROLE_KEY"]
 headers={"apikey":key,"Authorization":"Bearer "+key}
 def get(table,query):
  req=urllib.request.Request(base+"/rest/v1/"+table+"?"+query,headers=headers)
  with urllib.request.urlopen(req,timeout=45) as resp:return json.load(resp)
 # Explicit traversal avoids assuming PostgREST relationship names.
 subjects=get("subjects","select=id,subject_name&order=subject_name.asc&limit=1000")
 # The canonical subjects table has no code column; A1/B1 are unit-code families.
 subject_aliases={"A1":"Aptitude","B1":"Biology","C1":"Chemistry","P1":"Physics","M1":"Maths"}
 if subject!="ALL":
  wanted=subject_aliases.get(subject,subject)
  subjects=[s for s in subjects if s["subject_name"].casefold()==wanted.casefold()]
 if not subjects:raise RuntimeError("No matching Master subject")
 chapters=[]
 chapter_sizes={}
 for s in subjects:
  units=get("units","select=id,code&subject_id=eq."+urllib.parse.quote(str(s["id"]),safe="")+"&order=code.asc&limit=1000")
  for u in units:
   rows=get("chapters","select=id,code&unit_id=eq."+urllib.parse.quote(str(u["id"]),safe="")+"&order=code.asc&limit=1000")
   for ch in rows:
    # Count subtopics to report coverage and advance at exact chapter boundaries.
    chapter_id=urllib.parse.quote(str(ch["id"]),safe="")
    subtopics=[]
    page=0
    while True:
     batch=get("subtopics","select=id&chapter_id=eq."+chapter_id+"&order=code.asc&limit=1000&offset="+str(page))
     subtopics.extend(batch)
     if len(batch)<1000:break
     page+=1000
    if subtopics:
     if ch["code"] in chapter_sizes:raise RuntimeError("Duplicate Master chapter code")
     chapters.append(ch["code"])
     chapter_sizes[ch["code"]]=len(subtopics)
 if not chapters:raise RuntimeError("No Master chapters with subtopics")
 total_subtopics=sum(chapter_sizes.values())
 STATE.parent.mkdir(parents=True,exist_ok=True)
 REPORT.parent.mkdir(parents=True,exist_ok=True)
 if resume:
  if not STATE.exists():raise RuntimeError("No saved traversal checkpoint")
  state=json.loads(STATE.read_text())
  if state.get("config")!=config or state.get("status")!="paused" or state.get("incomplete_subtopics"):
   raise RuntimeError("Resume blocked: settings mismatch or unresolved work")
  if state.get("chapters")!=chapters:raise RuntimeError("Master chapter list changed; review before resume")
 else:
  state=dict(config=config,chapters=chapters,chapter_index=0,subtopic_offset=0,completed_batches=0,
             status="running",incomplete_subtopics=[],history=[])
 def save():
  completed=sum(chapter_sizes[ch] for ch in chapters[:state["chapter_index"]])+state["subtopic_offset"]
  state["coverage"]={"total_chapters":len(chapters),"total_subtopics":total_subtopics,
                     "completed_chapters":state["chapter_index"],"validated_subtopics":completed,
                     "remaining_subtopics":total_subtopics-completed,
                     "percent":round(100*completed/total_subtopics,2)}
  STATE.write_text(json.dumps(state,indent=2)+"\n",encoding="utf-8")
  REPORT.write_text(json.dumps(state,indent=2)+"\n",encoding="utf-8")
  subprocess.run(["git","add",str(STATE)],check=True)
  if subprocess.run(["git","diff","--cached","--quiet"]).returncode:
   subprocess.run(["git","-c","user.name=github-actions[bot]",
                   "-c","user.email=41898282+github-actions[bot]@users.noreply.github.com",
                   "commit","-m","Checkpoint Master traversal validation"],check=True)
   subprocess.run(["git","push","origin","HEAD:main"],check=True)
 save()
 for _ in range(max_batches):
  if state["chapter_index"]>=len(chapters):
   state["status"]="completed";save();break
  chapter=chapters[state["chapter_index"]]
  offset=state["subtopic_offset"]
  # Check chapter remainder before dispatch; avoids treating end-of-chapter as failure.
  ids=get("chapters","select=id&code=eq."+urllib.parse.quote(chapter,safe="")+"&limit=2")
  if len(ids)!=1:raise RuntimeError("Ambiguous chapter code")
  remaining=get("subtopics","select=id&chapter_id=eq."+urllib.parse.quote(str(ids[0]["id"]),safe="")+
                "&order=code.asc&offset="+str(offset)+"&limit="+str(limit))
  if not remaining:
   if offset!=chapter_sizes[chapter]:raise RuntimeError("Unexpected empty subtopic page")
   state["chapter_index"]+=1
   state["subtopic_offset"]=0
   save()
   continue
  env=dict(os.environ,MASTER_CHAPTER_CODE=chapter,QUESTION_DIFFICULTY=level,GENERATION_ROUND=str(round_no),
           SUBTOPIC_OFFSET=str(offset),SUBTOPIC_LIMIT=str(limit),QUESTION_COUNT=str(count),DRY_RUN="true")
  report_file=Path("artifacts/question_factory_run_summary.json")
  report_file.unlink(missing_ok=True)
  run=subprocess.run([sys.executable,"-m","Engine.integration.master_syllabus_bulk"],env=env)
  if not report_file.exists():
   state["status"]="needs_review";save();raise RuntimeError("Batch report missing")
  report=json.loads(report_file.read_text())
  state["incomplete_subtopics"]=report.get("incomplete_subtopics",[])
  state["history"].append(dict(chapter=chapter,offset=offset,next_offset=report.get("next_offset"),
                               requested=report.get("requested"),accepted=report.get("validated_or_inserted"),
                               pending=report.get("pending"),failed_subtopics=report.get("failed_subtopics")))
  if run.returncode or state["incomplete_subtopics"] or report.get("pending") or report.get("failed_subtopics"):
   state["status"]="needs_review";save();raise RuntimeError("Incomplete batch; manual review required")
  nxt=report.get("next_offset")
  if not isinstance(nxt,int) or nxt<=offset or nxt-offset!=len(remaining):
   state["status"]="needs_review";save();raise RuntimeError("Invalid checkpoint advancement")
  state["subtopic_offset"]=nxt
  state["completed_batches"]+=1
  if nxt>=chapter_sizes[chapter]:
   state["chapter_index"]+=1
   state["subtopic_offset"]=0
  save()
 if state["status"]=="running":state["status"]="paused"
 if state["chapter_index"]>=len(chapters):state["status"]="completed"
 save()
 print(json.dumps(dict(status=state["status"],chapter_index=state["chapter_index"],
                       subtopic_offset=state["subtopic_offset"],completed_batches=state["completed_batches"],
                       total_chapters=len(chapters))))
if __name__=="__main__":main()
