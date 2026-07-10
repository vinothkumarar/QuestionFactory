"""
Question Factory OS
Batch Execution Engine

Milestone : M6
Sprint    : S3
Release   : R1
"""

import time

from production.production_worker import ProductionWorker

from models.batch_result_model import BatchResultModel

from constants.generation_status import GenerationStatus


class BatchExecutionEngine:
    """
    Executes an entire ProductionQueue
    and returns a BatchResultModel.
    """

    def __init__(self):

        self.worker = ProductionWorker()

    def execute(
        self,
        production_queue
    ) -> BatchResultModel:

        start_time = time.time()

        worker_results = []

        successful = 0

        failed = 0

        for production_order in production_queue:

            result = self.worker.execute(
                production_order
            )

            worker_results.append(
                result
            )

            if result.status == GenerationStatus.SUCCESS:

                successful += 1

            else:

                failed += 1

        execution_time = int(

            (time.time() - start_time) * 1000

        )

        return BatchResultModel(

            total_orders=len(production_queue),

            successful=successful,

            failed=failed,

            execution_time_ms=execution_time,

            worker_results=worker_results

        )
        