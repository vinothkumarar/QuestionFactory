"""
Question Factory OS
Prompt Builder

Builds the final AI prompt.
"""

from pathlib import Path

from core.qgs_builder import QGSBuilder


class PromptBuilder:

    def __init__(self):

        self.qgs_builder = QGSBuilder()

        self.template_path = (
            Path(__file__).parent.parent
            / "prompts"
            / "templates"
            / "jee_mcq_v1.txt"
        )

    def build(self, question: dict) -> str:

        qgs = self.qgs_builder.build()

        template = self.template_path.read_text(
            encoding="utf-8"
        )

        rendered_template = template.format(

            subject_name=question["subject_name"],

            unit_name=question["unit_name"],

            chapter_name=question["chapter_name"],

            subtopic_name=question["subtopic_name"]

        )

        return (

            qgs

            + "\n\n"

            + rendered_template

        )
                