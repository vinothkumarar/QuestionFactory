"""
Question Factory OS
Batch Execution Engine V2 Test

Milestone : M6
Sprint    : S3
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
        question_count=1,
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
        question_count=1,
    ),
]

engine = BatchExecutionEngine()

batch = engine.execute(queue)

print("=" * 80)
print("BATCH EXECUTION ENGINE V2")
print("=" * 80)

print()

print("Total Orders   :", batch.total_orders)

print("Successful     :", batch.successful)

print("Failed         :", batch.failed)

print("Success Rate   :", batch.success_rate, "%")

print("Execution (ms) :", batch.execution_time_ms)

print()

print("Worker Results")

print("-" * 80)

for index, result in enumerate(batch.worker_results, start=1):

    print(f"{index}. {result.question['question_code']}  [{result.status}]")
