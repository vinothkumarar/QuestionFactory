"""
Question Factory OS
Production Queue Test
"""

from repositories.factory_state_repository import FactoryStateRepository
from planning.production_planner import ProductionPlanner
from planning.production_queue import ProductionQueue


repository = FactoryStateRepository()

state = repository.load()

planner = ProductionPlanner()

queue = ProductionQueue()

production_order = planner.plan(state)

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
