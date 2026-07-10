"""
Question Factory OS
AI Processor Test

Milestone : M4
Sprint    : S3
Release   : R1
"""

from models.pipeline_context_model import PipelineContextModel
from models.production_order_model import ProductionOrderModel

from pipeline.processors.build_processor import BuildProcessor
from pipeline.processors.prompt_processor import PromptProcessor
from pipeline.processors.ai_processor import AIProcessor


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

context = BuildProcessor().execute(context)

context = PromptProcessor().execute(context)

context = AIProcessor().execute(context)

print("=" * 80)
print("AI PROCESSOR")
print("=" * 80)

print("Provider      :", context.provider)

print("Execution(ms) :", context.execution_time_ms)

print()

print("Response Preview")
print("-" * 80)

print(context.raw_response[:500])

print()

print("Response Length :", len(context.raw_response))
