"""
Question Factory OS
Job Factory Test
"""

from repositories.runtime_repository import RuntimeRepository
from planning.production_planner import ProductionPlanner


runtime = RuntimeRepository().get_runtime()

planner = ProductionPlanner()

order = planner.create(runtime)

print("=" * 80)
print("GENERATION JOB CREATED")
print("=" * 80)

print(order)
