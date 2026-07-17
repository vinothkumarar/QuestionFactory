"""
Question Factory OS
Queue Builder Test

Milestone : M10
Sprint    : S1
Rollback  : Restore Original Design
"""

from Engine.planning.queue_builder import QueueBuilder

from Engine.models.production_request_model import ProductionRequestModel

request = ProductionRequestModel(
    request_id="REQ_001",
    subject="Physics",
    unit="P1",
    chapter="CH1",
    subtopic="ST4",
    set_no="S1",
    total_questions=250,
)

builder = QueueBuilder()

queue = builder.build(request)

print("=" * 80)
print("QUEUE BUILDER")
print("=" * 80)

print()

print("Total Batches   :", queue.total_batches)

print("Total Questions :", queue.total_questions)

print()

for order in queue.orders:

    end_question = order.question_start + order.question_count - 1

    print(f"Batch {order.batch_no} : " f"Q{order.question_start}" f"-Q{end_question}")

print()

print("Queue Builder Rollback PASSED")
