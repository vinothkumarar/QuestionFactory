"""
Question Factory OS
Batch Progress Manager
"""


class BatchProgressManager:

    def next_batch(
        self,
        runtime: dict,
        questions_per_batch: int = 100
    ) -> dict:

        runtime = runtime.copy()

        runtime["current_batch"] += 1

        runtime["next_question"] += questions_per_batch

        return runtime
        