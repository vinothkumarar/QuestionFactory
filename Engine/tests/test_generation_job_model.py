"""
Question Factory OS
Generation Job Model Test
"""

from models.generation_job_model import GenerationJobModel


job = GenerationJobModel(

    job_id="JOB_000001",

    subject="Physics",

    unit="P1",

    chapter="CH1",

    subtopic="ST4",

    set_no="S1",

    batch_no=3,

    question_start=201,

    question_count=100

)

print("=" * 80)
print("GENERATION JOB")
print("=" * 80)

print(job)
