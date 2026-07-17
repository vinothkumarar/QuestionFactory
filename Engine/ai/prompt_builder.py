"""
Question Factory OS
Prompt Builder

Builds the final AI prompt.
"""

from pathlib import Path

from Engine.core.contract_manager import ContractManager
from Engine.core.qgs_builder import QGSBuilder


class PromptBuilder:
    def __init__(self) -> None:
        self.qgs_builder = QGSBuilder()
        self.contract_manager = ContractManager()

        self.template_path = (
            Path(__file__).parent.parent
            / "prompts"
            / "templates"
            / "jee_mcq_v1.txt"
        )

    def build(self, question: dict) -> str:
        qgs = str(self.qgs_builder.build())

        contract = str(self.contract_manager.required_json_contract())

        template = self.template_path.read_text(encoding="utf-8")

        rendered_template = template.format(
            subject_name=question["subject_name"],
            unit_name=question["unit_name"],
            chapter_name=question["chapter_name"],
            subtopic_name=question["subtopic_name"],
        )

        return qgs + "\n\n" + contract + "\n\n" + rendered_template
        