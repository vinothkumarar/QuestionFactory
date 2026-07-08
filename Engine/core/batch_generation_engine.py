"""
Question Factory OS
Batch Generation Engine
"""

from core.pipeline_engine import PipelineEngine


class BatchGenerationEngine:

    def __init__(self):

        self.pipeline = PipelineEngine()

    def generate(self, job):

        results = []

        for question_number in range(
            job.start_question,
            job.start_question + job.count
        ):

            question, validation = self.pipeline.generate(
                job.runtime,
                question_number
            )

            results.append({

                "question_number": question_number,

                "question": question,

                "validation": validation

            })

        return results
        