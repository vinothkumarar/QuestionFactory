"""
Question Factory OS
Factory State Manager Test

Milestone : M10
Sprint    : S1
Release   : R2
"""

from core.factory_state_manager import FactoryStateManager

from repositories.factory_state_repository import (
    FactoryStateRepository
)


manager = FactoryStateManager()

repository = FactoryStateRepository()

state = repository.load()

print("=" * 80)
print("FACTORY STATE MANAGER V2")
print("=" * 80)

print()

print("Initial State")
print("-" * 80)

print(state)

print()

print("Question Range")
print("-" * 80)

print(
    "Start :",
    manager.get_question_start(state)
)

print(
    "End   :",
    manager.get_question_end(state)
)

print()

print("Set RUNNING")
print("-" * 80)

state = manager.set_running(state)

repository.update(state)

print(repository.load())

print()

print("Complete Batch")
print("-" * 80)

state = manager.complete_batch(state)

repository.update(state)

print(repository.load())

print()

print("Question Range After Batch Completion")
print("-" * 80)

print(
    "Start :",
    manager.get_question_start(state)
)

print(
    "End   :",
    manager.get_question_end(state)
)

print()

print("Set COMPLETED")
print("-" * 80)

state = manager.set_completed(state)

repository.update(state)

print(repository.load())

print()

print("Factory State Manager V2 PASSED")
