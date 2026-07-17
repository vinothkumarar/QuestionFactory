"""
Question Factory OS
Merge Processor Test

Milestone : M4
Sprint    : S5
Release   : R1
"""

from Engine.models.pipeline_context_model import PipelineContextModel
from Engine.models.production_order_model import ProductionOrderModel

from Engine.pipeline.processors.build_processor import BuildProcessor
from Engine.pipeline.processors.prompt_processor import PromptProcessor
from Engine.pipeline.processors.ai_processor import AIProcessor
from Engine.pipeline.processors.parse_processor import ParseProcessor
from Engine.pipeline.processors.merge_processor import MergeProcessor

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

print("=" * 80)
print("MERGE PROCESSOR")
print("=" * 80)

print("Question Code :", context.question["question_code"])

print("Difficulty    :", context.question["difficulty"])

print("Question Type :", context.question["question_type"])

print()

print("Question")

print("-" * 80)

print(context.question["question_text"])

print()

print("Options")

print("-" * 80)

print("A.", context.question["option_a"])

print("B.", context.question["option_b"])

print("C.", context.question["option_c"])

print("D.", context.question["option_d"])

print()

print("Correct Option :", context.question["correct_option"])

print("Marks          :", context.question["marks"])

print("Batch          :", context.question["batch_no"])

print("Language       :", context.question["language"])
