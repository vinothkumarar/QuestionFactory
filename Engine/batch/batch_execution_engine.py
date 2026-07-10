"""
Question Factory OS
Batch Execution Engine

Milestone : M6
Sprint    : S1
Release   : R1
"""

from production.production_worker import ProductionWorker


class BatchExecutionEngine:
    """
    Executes an entire ProductionQueue.

    Version 1 responsibilities

    - Iterate production orders
    - Execute ProductionWorker
    - Collect WorkerResultModel objects
    """

    def __init__(self):

        self.worker = ProductionWorker()

    def execute(
        self,
        production_queue
    ) -> list:

        results = []

        for production_order in production_queue:

            result = self.worker.execute(
                production_order
            )

            results.append(
                result
            )

        return results
        