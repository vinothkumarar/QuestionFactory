"""
Question Factory OS
Production Worker Test
"""

from repositories.factory_state_repository import FactoryStateRepository
from planning.production_planner import ProductionPlanner
from production.production_worker import ProductionWorker


repository = FactoryStateRepository()

state = repository.load()

planner = ProductionPlanner()

production_order = planner.plan(state)

worker = ProductionWorker()

result = worker.execute(
    production_order
)

print("=" * 80)
print("WORKER RESULT")
print("=" * 80)

print(result)

print()

print("=" * 80)
print("QUESTION CODE")
print("=" * 80)

print(result.question["question_code"])

print()

print("=" * 80)
print("PROMPT LENGTH")
print("=" * 80)

print(len(result.prompt))

print()

print("=" * 80)
print("PROMPT PREVIEW")
print("=" * 80)

print(result.prompt[:800])

print()

print("... PROMPT TRUNCATED ...")

print()

print("=" * 80)
print("STATUS")
print("=" * 80)

print(result.status)

print()

print("=" * 80)
print("PROVIDER")
print("=" * 80)

print(result.provider)

print()

print("=" * 80)
print("RAW RESPONSE (FIRST 1000 CHARACTERS)")
print("=" * 80)

if result.raw_response:

    print(result.raw_response[:1000])

else:

    print(result.error_message)