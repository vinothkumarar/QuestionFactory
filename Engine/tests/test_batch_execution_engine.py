"""
Question Factory OS
Batch Execution Engine Test

Milestone : M6
Sprint    : S1
Release   : R1
"""

from batch.batch_execution_engine import BatchExecutionEngine

from models.production_order_model import ProductionOrderModel


queue = [

    ProductionOrderModel(

        order_id="ORDER_001",

        subject="Physics",

        unit="P1",

        chapter="CH1",

        subtopic="ST4",

        set_no="S1",

        batch_no=6,

        question_start=501,

        question_count=1

    ),

    ProductionOrderModel(

        order_id="ORDER_002",

        subject="Physics",

        unit="P1",

        chapter="CH1",

        subtopic="ST4",

        set_no="S1",

        batch_no=6,

        question_start=502,

        question_count=1

    )

]

engine = BatchExecutionEngine()

results = engine.execute(
    queue
)

print("=" * 80)
print("BATCH EXECUTION ENGINE")
print("=" * 80)

print()

print("Orders Executed :", len(results))

print()

for index, result in enumerate(results, start=1):

    print("-" * 80)

    print("Result :", index)

    print("Status :", result.status)

    print("Question Code :", result.question["question_code"])

    print("Difficulty :", result.question["difficulty"])

    print("Validation :", result.validation["passed"])
    