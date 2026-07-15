"""
Question Factory OS
QGS Builder

Builds the complete Question Generation Specification.
"""

from pathlib import Path


class QGSBuilder:

    def __init__(self):

        self.qgs_folder = Path(__file__).parent.parent / "prompts" / "master"

        self.parts = [
            "master_prompt_v1.txt",
            "04_jee_standards.md",
            "05_blueprint_rules.md",
            "06_distractor_engineering.md",
            "07_difficulty_calibration.md",
            "08_output_contract.md",
            "09_self_validation.md",
            "10_final_assembly.md",
        ]

    def build(self) -> str:

        sections = []

        for filename in self.parts:

            file_path = self.qgs_folder / filename

            if file_path.exists():

                sections.append(file_path.read_text(encoding="utf-8"))

        return "\n\n".join(sections)
