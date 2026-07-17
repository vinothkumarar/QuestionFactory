"""
Question Factory OS
Production Order Model Test
"""

from Engine.models.production_order_model import ProductionOrderModel

order = ProductionOrderModel(
    order_id="ORDER_P1_CH1_ST4_S1_B3_Q201_300",
    subject="Physics",
    unit="P1",
    chapter="CH1",
    subtopic="ST4",
    set_no="S1",
    batch_no=3,
    question_start=201,
    question_count=100,
)

print("=" * 80)
print("PRODUCTION ORDER")
print("=" * 80)

print(order)
