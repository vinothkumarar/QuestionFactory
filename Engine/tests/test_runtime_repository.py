"""
Question Factory OS
Runtime Repository Test
"""

from repositories.runtime_repository import RuntimeRepository

repo = RuntimeRepository()

runtime = repo.get_runtime()

print("=" * 80)
print("CURRENT RUNTIME")
print("=" * 80)
print(runtime)

runtime["current_batch"] += 1

repo.save_runtime(runtime)

print()
print("=" * 80)
print("UPDATED RUNTIME")
print("=" * 80)
print(repo.get_runtime())
