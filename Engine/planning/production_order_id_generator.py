"""
Question Factory OS
Production Order ID Generator
"""


class ProductionOrderIdGenerator:

    def generate(
        self,
        runtime: dict,
        question_count: int
    ) -> str:

        start = runtime["next_question"]

        end = start + question_count - 1

        return (

            f"ORDER_"

            f"{runtime['current_project']}_"

            f"{runtime['current_chapter']}_"

            f"{runtime['current_subtopic']}_"

            f"{runtime['current_set']}_"

            f"B{runtime['current_batch']}_"

            f"Q{start}_{end}"

        )
        