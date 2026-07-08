"""
Pipeline Test
"""

from core.pipeline_engine import PipelineEngine

runtime = {

    "current_project": "P1",

    "current_chapter": "CH1",

    "current_subtopic": "ST4",

    "current_set": "S1"

}

engine = PipelineEngine()

question, validation = engine.generate(
    runtime,
    1
)

print("=" * 80)
print("QUESTION CODE")
print("=" * 80)
print(question["question_code"])

print("=" * 80)
print("VALIDATION")
print("=" * 80)
print(validation)

print("=" * 80)
print("QUESTION")
print("=" * 80)

print(question["question_text"])
