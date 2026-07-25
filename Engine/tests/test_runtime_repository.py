"""
Question Factory OS
Runtime Repository Test
"""

from Engine.repositories.runtime_repository import RuntimeRepository

repo = RuntimeRepository()

runtime = repo.get_runtime()

print("=" * 80)
print("CURRENT RUNTIME")
print("=" * 80)
print(runtime)

runtime.production.batch_id = "TEST_BATCH_2"

repo.save_runtime(runtime)

print()
print("=" * 80)
print("UPDATED RUNTIME")
print("=" * 80)
print(repo.get_runtime())
