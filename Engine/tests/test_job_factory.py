"""
Question Factory OS
Job Factory Test
"""

from repositories.runtime_repository import RuntimeRepository
from jobs.job_factory import JobFactory


runtime = RuntimeRepository().get_runtime()

factory = JobFactory()

job = factory.create(runtime)

print("=" * 80)
print("GENERATION JOB CREATED")
print("=" * 80)

print(job)
