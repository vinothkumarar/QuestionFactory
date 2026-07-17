"""
Question Factory OS
Batch Execution Engine

Milestone : M10
Sprint    : S2
Release   : R2
"""

import time
from copy import deepcopy

from Engine.production.production_worker import (
    ProductionWorker,
)

from Engine.models.batch_result_model import (
    BatchResultModel,
)

from Engine.constants.generation_status import (
    GenerationStatus,
)


class BatchExecutionEngine:
    """
    Manufacturing Engine

    Executes an entire Production Queue.

    Each ProductionOrder represents one production batch.

    Example

    Batch 6

    Q501-Q600

    Generates

    100 validated questions.
    """

    def __init__(self):

        self.worker = ProductionWorker()

    def execute(self, production_queue) -> BatchResultModel:

        start_time = time.time()

        worker_results = []

        successful = 0

        failed = 0

        for production_order in production_queue:

            print()

            print("=" * 70)
            print(f"Executing Batch {production_order.batch_no}")

            print(
                f"Question Range : "
                f"Q{production_order.question_start}"
                f"-Q{production_order.question_start + production_order.question_count - 1}"
            )

            print("=" * 70)

            batch_success = 0

            batch_failed = 0

            for question_no in range(
                production_order.question_start,
                production_order.question_start + production_order.question_count,
            ):

                #
                # Create an immutable copy for this question.
                #

                question_order = deepcopy(production_order)

                question_order.question_start = question_no

                result = self.worker.execute(question_order)

                worker_results.append(result)

                if result.status == GenerationStatus.SUCCESS:

                    successful += 1

                    batch_success += 1

                    print(f"✔ Q{question_no}")

                else:

                    failed += 1

                    batch_failed += 1

                    print(f"✘ Q{question_no}")

            print()

            print(f"Batch {production_order.batch_no} Completed")

            print(f"Successful : {batch_success}")

            print(f"Failed     : {batch_failed}")

        execution_time = int((time.time() - start_time) * 1000)

        return BatchResultModel(
            total_orders=len(production_queue),
            successful=successful,
            failed=failed,
            execution_time_ms=execution_time,
            worker_results=worker_results,
        )
