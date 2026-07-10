"""
Question Factory OS
Parse Processor Test

Milestone : M4
Sprint    : S4
Release   : R1
"""

from models.pipeline_context_model import PipelineContextModel
from models.production_order_model import ProductionOrderModel

from pipeline.processors.build_processor import BuildProcessor
from pipeline.processors.prompt_processor import PromptProcessor
from pipeline.processors.ai_processor import AIProcessor
from pipeline.processors.parse_processor import ParseProcessor


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

context = ParseProcessor().execute(context)

print("=" * 80)
print("PARSE PROCESSOR")
print("=" * 80)

print("Question Code :", context.question["question_code"])

print()

print("Parsed Keys")
print("-" * 80)

for key in sorted(context.parsed_response.keys()):
    print(key)

print()

print("Question Text")
print("-" * 80)

print(context.parsed_response["question_text"])

print()

print("Correct Option :", context.parsed_response["correct_option"])
