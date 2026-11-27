"""Deterministic, versionable CIRE catalog store for one canonical subtopic.

A store file can be committed to GitHub after human/workflow review.
No OpenAI calls and no Supabase writes occur here.
"""
import json
import re
from pathlib import Path

def normalize(value):
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))

def upsert_chain(path, subtopic, concept, definition, pattern, archetype):
    if not re.fullmatch(r"[A-Za-z0-9_]+", subtopic):
        raise ValueError("Invalid subtopic")
    values=(concept,definition,pattern,archetype)
    if not all(isinstance(v,str) and v.strip() for v in values):
        raise ValueError("All CIRE fields must be nonempty")
    path=Path(path)
    data=json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"subtopic":subtopic,"concepts":[]}
    if data["subtopic"]!=subtopic:
        raise ValueError("Catalog subtopic mismatch")
    concepts=data["concepts"]
    c=next((x for x in concepts if normalize(x["name"])==normalize(concept)),None)
    if c is None:
        c={"id":f"{subtopic}_C{len(concepts)+1:03d}","name":concept,"definition":definition,"patterns":[]}
        concepts.append(c)
    patterns=c["patterns"]
    q=next((x for x in patterns if normalize(x["description"])==normalize(pattern)),None)
    if q is None:
        q={"id":f"{c['id']}_QP{len(patterns)+1:03d}","description":pattern,"archetypes":[]}
        patterns.append(q)
    archetypes=q["archetypes"]
    a=next((x for x in archetypes if normalize(x["name"])==normalize(archetype)),None)
    if a is None:
        a={"id":f"{q['id']}_A{len(archetypes)+1:03d}","name":archetype}
        archetypes.append(a)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return {"concept_id":c["id"],"qp_id":q["id"],"archetype_id":a["id"]}

def test_round_trip():
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as directory:
        path=Path(directory)/"A1_CH1_ST1.json"
        args=(path,"A1_CH1_ST1","Successive percentage changes",
              "Combining sequential percentage changes",
              "Recover original value from final value after two changes",
              "Reverse calculation")
        first=upsert_chain(*args)
        second=upsert_chain(*args)
        assert first==second
        data=json.loads(path.read_text(encoding="utf-8"))
        assert len(data["concepts"])==1
        assert len(data["concepts"][0]["patterns"])==1
        assert len(data["concepts"][0]["patterns"][0]["archetypes"])==1
        third=upsert_chain(path,"A1_CH1_ST1","Successive percentage changes",
              "Combining sequential percentage changes",
              "Determine net percentage change from two sequential changes",
              "Forward calculation")
        assert third["concept_id"]==first["concept_id"]
        assert third["qp_id"]!=first["qp_id"]
        print(json.dumps({"result":"cire_round_trip_passed","reused":second,
                          "new_pattern":third,"concept_count":1,"qp_count":2}))
if __name__=="__main__":
    test_round_trip()
