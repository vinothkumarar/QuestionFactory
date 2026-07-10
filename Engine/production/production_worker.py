"""
Question Factory OS
Production Worker
"""

import time

from builders.question_builder import QuestionBuilder
from builders.question_merger import QuestionMerger

from ai.prompt_builder import PromptBuilder
from ai.provider_factory import ProviderFactory
from ai.response_parser import ResponseParser

from core.validation_engine import ValidationEngine

from constants.generation_status import GenerationStatus
from models.worker_result_model import WorkerResultModel


class ProductionWorker:

    def __init__(self):

        self.question_builder = QuestionBuilder()

        self.question_merger = QuestionMerger()

        self.prompt_builder = PromptBuilder()

        self.provider = ProviderFactory().create()

        self.parser = ResponseParser()

        self.validator = ValidationEngine()

    def execute(
        self,
        production_order
    ) -> WorkerResultModel:

        start_time = time.time()

        try:

            # --------------------------------------------------
            # Build Question Skeleton
            # --------------------------------------------------

            skeleton = self._build_question(
                production_order
            )

            # --------------------------------------------------
            # Build Prompt
            # --------------------------------------------------

            prompt = self._build_prompt(
                skeleton
            )

            # --------------------------------------------------
            # Generate AI Response
            # --------------------------------------------------

            raw_response = self._generate_response(
                prompt
            )

            # --------------------------------------------------
            # Parse AI Response
            # --------------------------------------------------

            parsed_response = self._parse_response(
                raw_response
            )

            execution_time = int(
                (time.time() - start_time) * 1000
            )

            return self._create_result(

                production_order=production_order,

                question=skeleton,

                prompt=prompt,

                raw_response=raw_response,

                parsed_response=parsed_response,

                validation=None,

                execution_time=execution_time,

                status=GenerationStatus.SUCCESS

            )

        except Exception as ex:

            execution_time = int(
                (time.time() - start_time) * 1000
            )

            return self._create_result(

                production_order=production_order,

                question=None,

                prompt=None,

                raw_response=None,

                parsed_response=None,

                validation=None,

                execution_time=execution_time,

                status=GenerationStatus.AI_FAILED,

                error_message=str(ex)

            )

    # ----------------------------------------------------------
    # Private Methods
    # ----------------------------------------------------------

    def _build_question(
        self,
        production_order
    ) -> dict:

        runtime = {

            "current_project": production_order.unit,

            "current_chapter": production_order.chapter,

            "current_subtopic": production_order.subtopic,

            "current_set": production_order.set_no,

            "current_batch": production_order.batch_no

        }

        return self.question_builder.build(

            runtime,

            production_order.question_start

        )

    def _build_prompt(
        self,
        question: dict
    ) -> str:

        return self.prompt_builder.build(
            question
        )

    def _generate_response(
        self,
        prompt: str
    ) -> str:

        return self.provider.generate(
            prompt
        )

    def _parse_response(
        self,
        response: str
    ) -> dict:

        return self.parser.parse(
            response
        )

    def _merge_question(
        self,
        skeleton: dict,
        ai_question: dict
    ) -> dict:

        return self.question_merger.merge(

            skeleton,

            ai_question

        )

    def _validate_question(
        self,
        question: dict
    ):

        return self.validator.validate(
            question
        )

    def _create_result(
        self,
        production_order,
        question,
        prompt,
        raw_response,
        parsed_response,
        validation,
        execution_time,
        status,
        error_message=None
    ) -> WorkerResultModel:

        return WorkerResultModel(

            production_order=production_order,

            question=question,

            prompt=prompt,

            raw_response=raw_response,

            parsed_response=parsed_response,

            validation=validation,

            provider=type(self.provider).__name__,

            execution_time_ms=execution_time,

            retry_count=0,

            status=status,

            error_message=error_message

        )