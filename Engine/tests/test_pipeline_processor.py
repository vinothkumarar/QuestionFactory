"""
Question Factory OS
Pipeline Processor Test

Milestone : M4
Sprint    : S1
Patch      : P1
"""

from Engine.pipeline.processors.pipeline_processor import PipelineProcessor

from Engine.models.pipeline_context_model import PipelineContextModel
from Engine.models.production_order_model import ProductionOrderModel


class DummyProcessor(PipelineProcessor):

    stage_id = "DUMMY"

    name = "Dummy Processor"

    description = "Testing PipelineProcessor."

    def execute(self, context: PipelineContextModel) -> PipelineContextModel:

        print(f"Executing : {self.name}")

        return context


order = ProductionOrderModel(
    order_id="ORDER_TEST",
    subject="Physics",
    unit="P1",
    chapter="CH1",
    subtopic="ST4",
    set_no="S1",
    batch_no=1,
    question_start=1,
    question_count=1,
)

context = PipelineContextModel(production_order=order)

processor = DummyProcessor()

result = processor.execute(context)

print("=" * 80)
print("PIPELINE PROCESSOR")
print("=" * 80)

print("Processor Name :", processor.name)
print("Stage ID       :", processor.stage_id)
print("Description    :", processor.description)

print()

print(result)
