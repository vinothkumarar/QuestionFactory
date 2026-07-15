"""
Question Factory OS
Factory State Repository Test
"""

from repositories.factory_state_repository import FactoryStateRepository

repository = FactoryStateRepository()

state = repository.load()

print("=" * 80)
print("FACTORY STATE")
print("=" * 80)

print(state)

print()

print("=" * 80)
print("UPDATING BATCH")
print("=" * 80)

state.current_batch += 1

repository.save(state)

print(repository.load())
