"""
Question Factory OS
Job ID Generator
"""


class JobIdGenerator:

    def generate(
        self,
        runtime: dict,
        question_count: int
    ) -> str:

        start = runtime["next_question"]

        end = start + question_count - 1

        return (

            f"JOB_"

            f"{runtime['current_project']}_"

            f"{runtime['current_chapter']}_"

            f"{runtime['current_subtopic']}_"

            f"{runtime['current_set']}_"

            f"B{runtime['current_batch']}_"

            f"Q{start}_{end}"

        )
        