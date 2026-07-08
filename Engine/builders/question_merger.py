"""
Question Factory OS
Question Merger
"""


class QuestionMerger:

    def merge(
        self,
        question: dict,
        ai_data: dict
    ) -> dict:

        merged = question.copy()

        merged.update(ai_data)

        return merged
        