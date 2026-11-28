"""Controlled Phase 8 live pilot: one Master subtopic, verified draft inserts."""
import json, os, subprocess, sys, urllib.parse, urllib.request
from pathlib import Path

STATE=Path("Engine/catalog/rounds/live_pilot_state.json")
REPORT=Path("artifacts/live_pilot_report.json")

def main():
 chapter=os.getenv("MASTER_CHAPTER_CODE","A1_CH2")
 if chapter!="A1_CH2":raise ValueError("Phase 8 pilot is restricted to A1_CH2")
 count=int(os.getenv("QUESTION_COUNT","5"))
 if count!=5:raise ValueError("Phase 8 pilot requires exactly 5 questions")
 if os.getenv("QUESTION_DIFFICULTY","S1")!="S1":raise ValueError("Pilot difficulty must be S1")
 if os.getenv("DRY_RUN","true").lower() not in ("false","0","no"):
  raise RuntimeError("Live pilot requires explicit DRY_RUN=false")
 if STATE.exists():
  old=json.loads(STATE.read_text())
  if old.get("status") in ("started","needs_review","completed"):
   raise RuntimeError("Live pilot checkpoint already exists; inspect before rerunning")
 base=os.environ["SUPABASE_URL"].rstrip("/")
 key=os.environ["SUPABASE_SERVICE_ROLE_KEY"]
 headers={"apikey":key,"Authorization":"Bearer "+key}
 def get(table,query):
  req=urllib.request.Request(base+"/rest/v1/"+table+"?"+query,headers=headers)
  with urllib.request.urlopen(req,timeout=45) as response:return json.load(response)
 ch=get("chapters","select=id&code=eq."+urllib.parse.quote(chapter,safe="")+"&limit=2")
 if len(ch)!=1:raise RuntimeError("Chapter lookup not unique")
 st=get("subtopics","select=id,code&chapter_id=eq."+str(ch[0]["id"])+"&order=code.asc&limit=1")
 if len(st)!=1:raise RuntimeError("No target subtopic")
 target=st[0]
 STATE.parent.mkdir(parents=True,exist_ok=True)
 REPORT.parent.mkdir(parents=True,exist_ok=True)
 state={"phase":8,"status":"started","chapter":chapter,"subtopic":target["code"],
        "requested":count,"accepted":0,"verified_drafts":0,"pending":count}
 def save():
  STATE.write_text(json.dumps(state,indent=2)+"\n")
  REPORT.write_text(json.dumps(state,indent=2)+"\n")
  subprocess.run(["git","add",str(STATE)],check=True)
  if subprocess.run(["git","diff","--cached","--quiet"]).returncode:
   subprocess.run(["git","-c","user.name=github-actions[bot]",
                   "-c","user.email=41898282+github-actions[bot]@users.noreply.github.com",
                   "commit","-m","Checkpoint controlled live pilot"],check=True)
   subprocess.run(["git","push","origin","HEAD:main"],check=True)
 save()
 env=dict(os.environ,MASTER_SUBTOPIC_CODE=target["code"],QUESTION_COUNT=str(count),
          QUESTION_DIFFICULTY="S1",DRY_RUN="false")
 run=subprocess.run([sys.executable,"-m","Engine.integration.master_syllabus_pilot"],
                    env=env,capture_output=True,text=True)
 print(run.stdout,flush=True)
 if run.stderr:print(run.stderr,file=sys.stderr,flush=True)
 payload=None
 for line in run.stdout.splitlines():
  try:item=json.loads(line)
  except json.JSONDecodeError:continue
  if isinstance(item,dict) and item.get("result")=="drafts_inserted":payload=item
 state["status"]="needs_review"
 if payload:
  ids=payload.get("ids",[])
  if not isinstance(ids,list) or len(ids)>count:raise RuntimeError("Invalid inserted ID list")
  state["accepted"]=len(ids)
  state["pending"]=count-len(ids)
  if ids:
   joined=",".join(str(x) for x in ids)
   rows=get("questions","select=id,question_code,subtopic_id,status,is_verified,correct_option,answer,option_a,option_b,option_c,option_d,explanation,concept_tested,question_archetype,difficulty&id=in.("+urllib.parse.quote(joined,safe=",")+")")
   def valid(row):
    opt=row.get("correct_option")
    return (row.get("subtopic_id")==target["id"] and row.get("status")=="draft"
            and row.get("is_verified") is False and opt in ("A","B","C","D")
            and row.get("answer")==row.get("option_"+opt.lower())
            and bool(row.get("explanation")) and bool(row.get("concept_tested"))
            and bool(row.get("question_archetype")) and row.get("difficulty")=="Easy")
   state["verified_drafts"]=sum(valid(r) for r in rows)
  if run.returncode==0 and state["accepted"]==count and state["verified_drafts"]==count:
   state["status"]="completed"
 save()
 print(json.dumps(state),flush=True)
 if state["status"]!="completed":raise RuntimeError("Pilot incomplete or inserted drafts failed verification; review checkpoint before retry")
if __name__=="__main__":main()
