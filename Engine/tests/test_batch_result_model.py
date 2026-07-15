"""
Question Factory OS
Batch Result Model Test

Milestone : M6
Sprint    : S2
Release   : R1
"""

from models.batch_result_model import BatchResultModel

result = BatchResultModel(
    total_orders=100, successful=98, failed=2, execution_time_ms=125000
)

print("=" * 80)
print("BATCH RESULT MODEL")
print("=" * 80)

print()

print("Total Orders    :", result.total_orders)

print("Successful      :", result.successful)

print("Failed          :", result.failed)

print("Execution (ms)  :", result.execution_time_ms)

print("Success Rate    :", result.success_rate, "%")
