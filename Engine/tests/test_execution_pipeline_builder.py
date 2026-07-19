"""
Question Factory OS
Execution Pipeline Builder Test
"""

from Engine.pipeline.execution_pipeline_builder import (
    ExecutionPipelineBuilder,
)

builder = ExecutionPipelineBuilder()

pipeline = builder.build()

print("=" * 80)
print("EXECUTION PIPELINE BUILDER")
print("=" * 80)

print()

print("Total Stages :", pipeline.size())

print()

print("Registered Stages")

print("-" * 80)

for index, stage in enumerate(
    pipeline.stages(),
    start=1,
):
    print(f"{index}. {stage.name}")