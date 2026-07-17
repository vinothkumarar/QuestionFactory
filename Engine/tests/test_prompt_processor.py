"""
Question Factory OS
Prompt Processor Test

Milestone : M4
Sprint    : S2
Release   : R1
"""

from Engine.models.pipeline_context_model import PipelineContextModel
from Engine.models.production_order_model import ProductionOrderModel

from Engine.pipeline.processors.build_processor import BuildProcessor
from Engine.pipeline.processors.prompt_processor import PromptProcessor

order = ProductionOrderModel(
    order_id="ORDER_TEST",
    subject="Physics",
    unit="P1",
    chapter="CH1",
    subtopic="ST4",
    set_no="S1",
    batch_no=6,
    question_start=501,
    question_count=100,
)

context = PipelineContextModel(production_order=order)

context = BuildProcessor().execute(context)

context = PromptProcessor().execute(context)

print("=" * 80)
print("PROMPT PROCESSOR")
print("=" * 80)

print("Question Code :", context.question["question_code"])

print()

print("Prompt Preview")
print("-" * 80)

print(context.prompt[:500])

print()

print("Prompt Length :", len(context.prompt))
