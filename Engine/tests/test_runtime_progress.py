"""
Question Factory OS
Runtime Progress Test
"""

from core.runtime_manager import RuntimeManager
from core.batch_progress_manager import BatchProgressManager


runtime_manager = RuntimeManager()

runtime = runtime_manager.load()

print("=" * 80)
print("CURRENT RUNTIME")
print("=" * 80)
print(runtime)

progress = BatchProgressManager()

updated_runtime = progress.next_batch(runtime)

print()

print("=" * 80)
print("UPDATED RUNTIME")
print("=" * 80)
print(updated_runtime)

runtime_manager.save(updated_runtime)

print()

print("=" * 80)
print("RUNTIME SAVED")
print("=" * 80)
