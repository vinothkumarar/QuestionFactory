"""
Batch Generation Test
"""

from jobs.generation_job import GenerationJob
from core.batch_generation_engine import BatchGenerationEngine

runtime = {

    "current_project": "P1",

    "current_chapter": "CH1",

    "current_subtopic": "ST4",

    "current_set": "S1"

}

job = GenerationJob(

    runtime=runtime,

    start_question=1,

    count=3

)

engine = BatchGenerationEngine()

results = engine.generate(job)

print("=" * 80)
print("BATCH SUMMARY")
print("=" * 80)

for result in results:

    q = result["question"]

    v = result["validation"]

    print(
        q["question_code"],
        "PASS" if v["passed"] else "FAIL"
    )
    