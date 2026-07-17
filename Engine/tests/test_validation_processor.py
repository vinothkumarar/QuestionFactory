"""
Question Factory OS
Validation Processor Test

Milestone : M4
Sprint    : S6
Release   : R1
"""

from Engine.models.pipeline_context_model import PipelineContextModel
from Engine.models.production_order_model import ProductionOrderModel

from Engine.pipeline.processors.build_processor import BuildProcessor
from Engine.pipeline.processors.prompt_processor import PromptProcessor
from Engine.pipeline.processors.ai_processor import AIProcessor
from Engine.pipeline.processors.parse_processor import ParseProcessor
from Engine.pipeline.processors.merge_processor import MergeProcessor
from Engine.pipeline.processors.validation_processor import ValidationProcessor

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

context = AIProcessor().execute(context)

context = ParseProcessor().execute(context)

context = MergeProcessor().execute(context)

context = ValidationProcessor().execute(context)

print("=" * 80)
print("VALIDATION PROCESSOR")
print("=" * 80)

print()

print("Question Code :", context.question["question_code"])

print("Validation")

print("-" * 80)

print(context.validation)

print()

print("Question Status :", context.question["status"])
