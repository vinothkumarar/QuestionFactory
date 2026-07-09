"""
Question Factory OS
CSV Export Test
"""

from pathlib import Path

from jobs.generation_job import GenerationJob
from core.batch_generation_engine import BatchGenerationEngine
from core.export_engine import ExportEngine


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

print("=" * 80)
print("GENERATING QUESTIONS")
print("=" * 80)

batch_engine = BatchGenerationEngine()

report = batch_engine.generate(job)

print(report.summary())

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

output_file = output_dir / "questions.csv"

export_engine = ExportEngine()

export_engine.export_csv(
    report,
    str(output_file)
)

print()
print("=" * 80)
print("EXPORT COMPLETE")
print("=" * 80)
print(output_file.resolve())
