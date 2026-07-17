"""
Question Factory OS
Production Worker

Milestone : M13
Sprint    : S1
Release   : R2

Automatic Retry & Self-Healing Engine
"""

import time

from Engine.constants.generation_status import (
    GenerationStatus,
)

from Engine.models.pipeline_context_model import (
    PipelineContextModel,
)

from Engine.models.worker_result_model import (
    WorkerResultModel,
)

from Engine.pipeline.execution_pipeline_builder import (
    ExecutionPipelineBuilder,
)

from Engine.config.factory_config import (
    MAX_RETRY_COUNT,
    RETRY_DELAY_SECONDS,
)


class ProductionWorker:
    """
    Executes one Production Order.

    Features

    • Automatic Retry
    • Self Healing
    • Retry Statistics
    • Stable Return Model
    """

    def __init__(self):

        self.pipeline = ExecutionPipelineBuilder().build()

    def execute(self, production_order) -> WorkerResultModel:

        last_result = None

        for attempt in range(1, MAX_RETRY_COUNT + 1):

            start_time = time.time()

            context = PipelineContextModel(production_order=production_order)

            try:

                context = self.pipeline.run(context)

                execution_time = int((time.time() - start_time) * 1000)

                return WorkerResultModel(
                    production_order=production_order,
                    question=context.question,
                    prompt=context.prompt,
                    raw_response=context.raw_response,
                    parsed_response=context.parsed_response,
                    validation=context.validation,
                    provider=context.provider,
                    execution_time_ms=execution_time,
                    retry_count=attempt - 1,
                    status=GenerationStatus.SUCCESS,
                    error_message=None,
                )

            except Exception as ex:

                execution_time = int((time.time() - start_time) * 1000)

                last_result = WorkerResultModel(
                    production_order=production_order,
                    question=context.question,
                    prompt=context.prompt,
                    raw_response=context.raw_response,
                    parsed_response=context.parsed_response,
                    validation=context.validation,
                    provider=context.provider,
                    execution_time_ms=execution_time,
                    retry_count=attempt,
                    status=GenerationStatus.AI_FAILED,
                    error_message=str(ex),
                )

                print()

                print(
                    f"[Retry {attempt}/{MAX_RETRY_COUNT}] "
                    f"Q{production_order.question_start}"
                )

                print(f"Reason : {ex}")

                if attempt < MAX_RETRY_COUNT:

                    time.sleep(RETRY_DELAY_SECONDS)

        print()

        print(f"FAILED AFTER {MAX_RETRY_COUNT} ATTEMPTS")

        
        if last_result is None:
            raise RuntimeError(
                "Production worker completed without producing a result."
            )

        return last_result
