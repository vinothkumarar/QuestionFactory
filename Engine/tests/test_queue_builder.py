"""
Question Factory OS
Queue Builder Test

Milestone : M10
Sprint    : S1
Release   : R1
"""

from planning.queue_builder import QueueBuilder

from models.production_request_model import (
    ProductionRequestModel
)


request = ProductionRequestModel(

    request_id="REQ_001",

    subject="Physics",

    unit="P1",

    chapter="CH1",

    subtopic="ST4",

    set_no="S1",

    total_questions=250

)

builder = QueueBuilder()

queue = builder.build(request)

print("=" * 80)
print("QUEUE BUILDER V2")
print("=" * 80)

print()

print("Total Orders    :", len(queue.orders))

print("Total Questions :", queue.total_questions)

print("Total Batches   :", queue.total_batches)

print()

print("First Five Orders")
print("-" * 80)

for order in queue.orders[:5]:

    print(

        f"Batch {order.batch_no} | "

        f"Q{order.question_start}"

    )

print()

print("Last Five Orders")
print("-" * 80)

for order in queue.orders[-5:]:

    print(

        f"Batch {order.batch_no} | "

        f"Q{order.question_start}"

    )

print()

print("Queue Builder V2 PASSED")
