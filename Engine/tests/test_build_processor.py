"""
Question Factory OS
Build Processor Test

Milestone : M4
Sprint    : S1
Release   : R1
"""

from Engine.models.pipeline_context_model import PipelineContextModel
from Engine.models.production_order_model import ProductionOrderModel

from Engine.pipeline.processors.build_processor import BuildProcessor

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

processor = BuildProcessor()

context = processor.execute(context)

print("=" * 80)
print("BUILD PROCESSOR")
print("=" * 80)

print("Processor    :", processor.name)
print("Stage ID     :", processor.stage_id)
print()

print("Question Code:", context.question["question_code"])
print("Subject      :", context.question["subject_name"])
print("Chapter      :", context.question["chapter_name"])
print("Subtopic     :", context.question["subtopic_name"])
print("Batch        :", context.question["batch_no"])
print("Marks        :", context.question["marks"])
print("Language     :", context.question["language"])
