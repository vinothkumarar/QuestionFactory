"""
Question Factory OS
Job Factory
"""

from models.generation_job_model import GenerationJobModel
from jobs.job_id_generator import JobIdGenerator


class JobFactory:

    def __init__(self):

        self.id_generator = JobIdGenerator()

    def create(
        self,
        runtime: dict,
        question_count: int = 100
    ) -> GenerationJobModel:

        job_id = self.id_generator.generate(
            runtime,
            question_count
        )

        return GenerationJobModel(

            job_id=job_id,

            subject="Physics",

            unit=runtime["current_project"],

            chapter=runtime["current_chapter"],

            subtopic=runtime["current_subtopic"],

            set_no=runtime["current_set"],

            batch_no=runtime["current_batch"],

            question_start=runtime["next_question"],

            question_count=question_count
        )
        