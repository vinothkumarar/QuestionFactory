"""
Question Factory OS
Production Worker Pipeline Test

Milestone : M5
Sprint    : S3
Release   : R1
"""

from production.production_worker import ProductionWorker

from models.production_order_model import ProductionOrderModel


order = ProductionOrderModel(

    order_id="ORDER_TEST",

    subject="Physics",

    unit="P1",

    chapter="CH1",

    subtopic="ST4",

    set_no="S1",

    batch_no=6,

    question_start=501,

    question_count=100

)

worker = ProductionWorker()

result = worker.execute(order)

print("=" * 80)
print("PRODUCTION WORKER")
print("=" * 80)

print()

print("Status          :", result.status)

print("Provider        :", result.provider)

print("Execution (ms)  :", result.execution_time_ms)

print()

print("Question Code   :", result.question["question_code"])

print("Difficulty      :", result.question["difficulty"])

print("Question Type   :", result.question["question_type"])

print()

print("Question")

print("-" * 80)

print(result.question["question_text"])

print()

print("Correct Option  :", result.question["correct_option"])

print()

print("Validation")

print("-" * 80)

print(result.validation)

print()

print("Error Message   :", result.error_message)
