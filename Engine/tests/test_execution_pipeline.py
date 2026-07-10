"""
Question Factory OS
Execution Pipeline Test

Milestone : M5
Sprint    : S2
Release   : R1
"""

from models.pipeline_context_model import PipelineContextModel
from models.production_order_model import ProductionOrderModel

from pipeline.execution_pipeline_builder import ExecutionPipelineBuilder


order = ProductionOrderModel(

    order_id="ORDER_TEST",

    subject="Physics",

    unit="P1",

    chapter="CH1",

    subtopic="ST4",

    set_no="S1",

    batch_no=6,

    question_start=501,

    question_count=100

)

context = PipelineContextModel(

    production_order=order

)

pipeline = ExecutionPipelineBuilder().build()

context = pipeline.run(context)

print("=" * 80)
print("EXECUTION PIPELINE")
print("=" * 80)

print()

print("Question Code :", context.question["question_code"])

print("Difficulty    :", context.question["difficulty"])

print("Question Type :", context.question["question_type"])

print()

print("Question")

print("-" * 80)

print(context.question["question_text"])

print()

print("Correct Option :", context.question["correct_option"])

print()

print("Validation")

print("-" * 80)

print(context.validation)

print()

print("Provider       :", context.provider)

print("Execution(ms)  :", context.execution_time_ms)


