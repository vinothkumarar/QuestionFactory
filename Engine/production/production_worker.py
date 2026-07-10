"""
Question Factory OS
Production Worker

Milestone : M5
Sprint    : S3
Release   : R1
"""

import time

from constants.generation_status import GenerationStatus

from models.pipeline_context_model import PipelineContextModel
from models.worker_result_model import WorkerResultModel

from pipeline.execution_pipeline_builder import (
    ExecutionPipelineBuilder
)


class ProductionWorker:
    """
    Thin orchestration layer.

    Responsibilities

    1. Create PipelineContext
    2. Execute Pipeline
    3. Return WorkerResult
    """

    def __init__(self):

        self.pipeline = (
            ExecutionPipelineBuilder().build()
        )

    def execute(
        self,
        production_order
    ) -> WorkerResultModel:

        start_time = time.time()

        context = PipelineContextModel(

            production_order=production_order

        )

        try:

            context = self.pipeline.run(
                context
            )

            execution_time = int(

                (time.time() - start_time) * 1000

            )

            return WorkerResultModel(

                production_order=production_order,

                question=context.question,

                prompt=context.prompt,

                raw_response=context.raw_response,

                parsed_response=context.parsed_response,

                validation=context.validation,

                provider=context.provider,

                execution_time_ms=execution_time,

                retry_count=context.retry_count,

                status=GenerationStatus.SUCCESS,

                error_message=None

            )

        except Exception as ex:

            execution_time = int(

                (time.time() - start_time) * 1000

            )

            return WorkerResultModel(

                production_order=production_order,

                question=context.question,

                prompt=context.prompt,

                raw_response=context.raw_response,

                parsed_response=context.parsed_response,

                validation=context.validation,

                provider=context.provider,

                execution_time_ms=execution_time,

                retry_count=context.retry_count,

                status=GenerationStatus.AI_FAILED,

                error_message=str(ex)

            )