"""
Question Factory OS
Production Planner Test
"""

from Engine.repositories.factory_state_repository import FactoryStateRepository

from Engine.planning.production_planner import ProductionPlanner

repository = FactoryStateRepository()

state = repository.load()

planner = ProductionPlanner()

production_order = planner.plan(state)

print("=" * 80)
print("PRODUCTION ORDER")
print("=" * 80)

print(production_order)
