"""
Question Factory OS
Execution Pipeline Builder Test

Milestone : M5
Sprint    : S1
Release   : R1
"""

from pipeline.execution_pipeline_builder import ExecutionPipelineBuilder

builder = ExecutionPipelineBuilder()

pipeline = builder.build()

print("=" * 80)
print("EXECUTION PIPELINE BUILDER")
print("=" * 80)

print()

print("Total Processors :", pipeline.size())

print()

print("Registered Processors")

print("-" * 80)

for index, processor in enumerate(pipeline.processors, start=1):

    print(f"{index}. {processor.name}")
