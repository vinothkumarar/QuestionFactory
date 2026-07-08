"""
Question Factory OS
Prompt Builder

Loads prompt templates and renders them.
"""

from pathlib import Path


class PromptBuilder:

    def __init__(self):

        self.template_path = (
            Path(__file__).parent.parent
            / "prompts"
            / "jee_mcq_v1.txt"
        )

    def build(self, question: dict) -> str:

        template = self.template_path.read_text(
            encoding="utf-8"
        )

        return template.format(
            subject_name=question["subject_name"],
            unit_name=question["unit_name"],
            chapter_name=question["chapter_name"],
            subtopic_name=question["subtopic_name"]
        )
        