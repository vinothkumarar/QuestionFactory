"""
Question Factory OS
Question Merger
"""


class QuestionMerger:

    def merge(self, skeleton: dict, ai_question: dict) -> dict:

        question = skeleton.copy()

        # Only AI-generated educational fields
        allowed_fields = [
            "difficulty",
            "difficulty_score",
            "question_type",
            "answer_type",
            "question_text",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct_option",
            "answer",
            "explanation",
            "more_explanation",
            "concept_tested",
            "question_archetype",
            "estimated_time_sec",
            "bloom_level",
            "exam_level",
            "chapter_weightage",
            "exam_relevance",
            "source_type",
            "tags",
            "pyq_inspired",
            "pyq_exam",
            "pyq_year",
            "pyq_topic",
            "image_required",
            "has_diagram",
            "latex_required",
        ]

        for field in allowed_fields:

            if field in ai_question:

                question[field] = ai_question[field]

        return question
