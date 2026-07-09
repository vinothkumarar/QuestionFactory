"""
Question Factory OS
Job Queue Test
"""

from repositories.runtime_repository import RuntimeRepository
from planning.production_planner import ProductionPlanner
from planning.production_queue import ProductionQueue


runtime = RuntimeRepository().get_runtime()

planner = ProductionPlanner()

queue = ProductionQueue()

production_order = planner.create(runtime)

queue.add(production_order)

print("=" * 80)
print("QUEUE SIZE")
print("=" * 80)

print(queue.size())

print()

print("=" * 80)
print("NEXT PRODUCTION ORDER")
print("=" * 80)

print(queue.get())

print()

print("=" * 80)
print("QUEUE SIZE")
print("=" * 80)

print(queue.size())