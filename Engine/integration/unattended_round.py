"""Unattended validation-only round controller; bounded, checkpointed on GitHub."""
import json, os, re, subprocess, sys
from pathlib import Path
P=Path("Engine/catalog/rounds/unattended_state.json")
def main():
 chapter=os.getenv("MASTER_CHAPTER_CODE","A1_CH1")
 difficulty=os.getenv("QUESTION_DIFFICULTY","S1")
 round_no=int(os.getenv("GENERATION_ROUND","1"))
 offset=int(os.getenv("SUBTOPIC_OFFSET","0"))
 limit=int(os.getenv("SUBTOPIC_LIMIT","1"))
 count=int(os.getenv("QUESTION_COUNT","1"))
 batches=int(os.getenv("MAX_BATCHES","2"))
 resume=os.getenv("RESUME","false").lower()=="true"
 if not re.fullmatch("[A-Za-z0-9_]{1,40}",chapter) or difficulty not in ("S1","S2","S3","S4") or not (1<=round_no<=1000 and 0<=offset<=10000 and 1<=limit<=20 and 1<=count<=20 and 1<=batches<=20):
  raise ValueError("Invalid generation settings")
 cfg=dict(chapter=chapter,difficulty=difficulty,round_number=round_no,limit=limit,count=count,dry_run=True)
 P.parent.mkdir(parents=True,exist_ok=True)
 if resume:
  if not P.exists(): raise RuntimeError("No resume checkpoint")
  state=json.loads(P.read_text())
  if state["config"]!=cfg or state["status"]!="paused" or state.get("incomplete_subtopics"): raise RuntimeError("Unsafe resume checkpoint")
  offset=state["next_offset"]
 else:
  state=dict(config=cfg,next_offset=offset,completed_batches=0,incomplete_subtopics=[],status="running",history=[])
 def save():
  P.write_text(json.dumps(state,indent=2)+"\n")
  subprocess.run(["git","add",str(P)],check=True)
  if subprocess.run(["git","diff","--cached","--quiet"]).returncode:
   subprocess.run(["git","-c","user.name=github-actions[bot]","-c","user.email=41898282+github-actions[bot]@users.noreply.github.com","commit","-m","Checkpoint unattended round"],check=True)
   subprocess.run(["git","push","origin","HEAD:main"],check=True)
 save()
 for _ in range(batches):
  env=dict(os.environ,MASTER_CHAPTER_CODE=chapter,QUESTION_DIFFICULTY=difficulty,GENERATION_ROUND=str(round_no),SUBTOPIC_OFFSET=str(offset),SUBTOPIC_LIMIT=str(limit),QUESTION_COUNT=str(count),DRY_RUN="true")
  result=subprocess.run([sys.executable,"-m","Engine.integration.master_syllabus_bulk"],env=env)
  report_path=Path("artifacts/question_factory_run_summary.json")
  if not report_path.exists(): state["status"]="failed";save();raise RuntimeError("Missing batch report")
  report=json.loads(report_path.read_text())
  state["history"].append(dict(offset=offset,next_offset=report.get("next_offset"),pending=report.get("pending")))
  state["incomplete_subtopics"]=report.get("incomplete_subtopics",[])
  if result.returncode or state["incomplete_subtopics"] or report.get("pending") or report.get("failed_subtopics"):
   state["status"]="needs_review";save();raise RuntimeError("Batch requires review")
  nxt=report.get("next_offset")
  if not isinstance(nxt,int) or nxt<=offset: state["status"]="failed";save();raise RuntimeError("Non-advancing checkpoint")
  offset=nxt
  state["next_offset"]=offset
  state["completed_batches"]+=1
  save()
 state["status"]="paused";save()
 print(json.dumps(dict(status="paused",next_offset=offset,completed_batches=state["completed_batches"])))
if __name__=="__main__":main()
