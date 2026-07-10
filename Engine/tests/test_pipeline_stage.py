"""
Question Factory OS
Pipeline Stage Test

Version : 2.3.7.1.2
"""

from pipeline.stages.pipeline_stage import PipelineStage
from models.pipeline_context_model import PipelineContextModel
from models.production_order_model import ProductionOrderModel


class DummyStage(PipelineStage):

    name = "Dummy Stage"

    description = "Testing PipelineStage interface."

    def execute(
        self,
        context: PipelineContextModel
    ) -> PipelineContextModel:

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

    question_count=1

)

context = PipelineContextModel(
    production_order=order
)

stage = DummyStage()

result = stage.execute(context)

print("=" * 80)
print("PIPELINE STAGE")
print("=" * 80)

print("Stage Name       :", stage.name)
print("Description      :", stage.description)

print()

print(result)
