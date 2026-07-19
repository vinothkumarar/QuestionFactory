"""
Question Factory OS
Execution Pipeline Test
"""

from Engine.pipeline.execution_pipeline import (
    ExecutionPipeline,
    PipelineStage,
)
from Engine.models.pipeline_context_model import (
    PipelineContextModel,
)
from Engine.models.production_order_model import (
    ProductionOrderModel,
)


class DummyStage(PipelineStage):

    stage_id = "DUMMY"

    name = "Dummy Stage"

    description = "Dummy pipeline stage"

    def execute(
        self,
        context: PipelineContextModel,
    ) -> PipelineContextModel:

        context.status = "EXECUTED"

        return context


pipeline = ExecutionPipeline()

pipeline.add_stage(DummyStage())
pipeline.add_stage(DummyStage())
pipeline.add_stage(DummyStage())

context = PipelineContextModel(
    production_order=ProductionOrderModel(
        order_id="TEST-001",
        subject="Physics",
        unit="P1",
        chapter="CH1",
        subtopic="ST1",
        set_no="S1",
        batch_no=1,
        question_start=1,
        question_count=10,
    )
)

result = pipeline.run(context)

print("=" * 80)
print("EXECUTION PIPELINE")
print("=" * 80)

print(result.status)
