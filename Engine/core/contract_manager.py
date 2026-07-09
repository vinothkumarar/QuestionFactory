"""
Question Factory OS
Contract Manager
"""

import json
from pathlib import Path


class ContractManager:

    def __init__(self):

        self.contract_path = (
            Path(__file__).parent.parent
            / "schema"
            / "question_contract_v1.json"
        )

    def load(self):

        with open(
            self.contract_path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def educational_fields(self):

        contract = self.load()

        return contract["sections"]["educational"]["fields"]

    def required_json_contract(self):

        fields = self.educational_fields()

        lines = []

        lines.append("Return ONE JSON object.")
        lines.append("")
        lines.append("The JSON MUST contain ALL of the following fields.")
        lines.append("")
        lines.append("Fields:")

        for field in fields:

            lines.append(f"- {field}")

        lines.append("")
        lines.append("Do not omit any field.")
        lines.append("Use null if a field is not applicable.")
        lines.append("Do not return markdown.")
        lines.append("Do not return explanations outside JSON.")

        return "\n".join(lines)
        