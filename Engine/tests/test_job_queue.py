"""
Question Factory OS
Job Queue Test
"""

from scheduler.job_queue import JobQueue
from jobs.job_factory import JobFactory
from repositories.runtime_repository import RuntimeRepository


runtime = RuntimeRepository().get_runtime()

factory = JobFactory()

queue = JobQueue()

job = factory.create(runtime)

queue.add(job)

print("=" * 80)
print("QUEUE SIZE")
print("=" * 80)

print(queue.size())

print()

print("=" * 80)
print("NEXT JOB")
print("=" * 80)

print(queue.get())

print()

print("=" * 80)
print("QUEUE SIZE")
print("=" * 80)

print(queue.size())
