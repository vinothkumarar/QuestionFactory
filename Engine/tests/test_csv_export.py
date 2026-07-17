"""
Question Factory OS
CSV Export Test
"""

from Engine.core.batch_generation_engine import BatchGenerationEngine
from Engine.core.export_engine import ExportEngine
from Engine.jobs.generation_job import GenerationJob

runtime = {
    "current_project": "P1",
    "current_chapter": "CH1",
    "current_subtopic": "ST4",
    "current_set": "S1",
    "current_batch": 1,
}


job = GenerationJob(runtime=runtime, start_question=1, count=3)


print("=" * 80)
print("GENERATING QUESTIONS")
print("=" * 80)

batch_engine = BatchGenerationEngine()

report = batch_engine.generate(job)

print()

print("=" * 80)
print("BATCH REPORT")
print("=" * 80)

print(report.summary())

print()

export_engine = ExportEngine()

output_file = export_engine.export_csv(report, runtime)

print()

print("=" * 80)
print("SMART EXPORT COMPLETE")
print("=" * 80)

print(output_file)
