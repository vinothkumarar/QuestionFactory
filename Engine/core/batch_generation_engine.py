"""
Question Factory OS
Batch Generation Engine
"""

from Engine.core.pipeline_engine import PipelineEngine
from Engine.models.batch_report import BatchReport


class BatchGenerationEngine:
    def __init__(self) -> None:
        self.pipeline = PipelineEngine()

    def generate(self, job):
        report = BatchReport()

        for question_number in range(
            job.start_question,
            job.start_question + job.count,
        ):
            question, validation = self.pipeline.generate(
                job.runtime,
                question_number,
            )

            report.add_result(question, validation)

        return report
        