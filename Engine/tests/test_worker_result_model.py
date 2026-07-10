"""
Question Factory OS
Worker Result Model Test
"""

from models.production_order_model import ProductionOrderModel
from models.worker_result_model import WorkerResultModel


order = ProductionOrderModel(

    order_id="ORDER_P1_CH1_ST4_S1_B6_Q501_600",

    subject="Physics",

    unit="P1",

    chapter="CH1",

    subtopic="ST4",

    set_no="S1",

    batch_no=6,

    question_start=501,

    question_count=100

)


result = WorkerResultModel(

    production_order=order,

    provider="OpenAIProvider"

)


print("=" * 80)
print("WORKER RESULT")
print("=" * 80)

print(result)
