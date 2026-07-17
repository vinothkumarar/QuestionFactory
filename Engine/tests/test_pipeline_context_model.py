"""
Question Factory OS
Pipeline Context Model Test
"""

from Engine.models.pipeline_context_model import PipelineContextModel
from Engine.models.production_order_model import ProductionOrderModel

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

print("=" * 80)
print("PIPELINE CONTEXT")
print("=" * 80)

print(context)
