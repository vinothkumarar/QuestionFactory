"""
Question Factory OS
Question Code Generator
"""


class QuestionCodeGenerator:

    def generate(
        self,
        project: str,
        chapter: str,
        subtopic: str,
        set_no: str,
        question_number: int,
    ) -> str:

        return (
            f"{project}_"
            f"{chapter}_"
            f"{subtopic}_"
            f"{set_no}_"
            f"Q{question_number:03}"
        )
