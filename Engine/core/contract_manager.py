"""
Question Factory OS
Contract Manager

Milestone : M11
Sprint    : P6
Release   : R1
"""

import json
from pathlib import Path


class ContractManager:

    def __init__(self):

        self.contract_path = (
            Path(__file__).parent.parent / "schema" / "question_contract_v1.json"
        )

    def load(self):

        with open(self.contract_path, "r", encoding="utf-8") as f:

            return json.load(f)

    def educational_fields(self):

        contract = self.load()

        return contract["sections"]["educational"]["fields"]

    def required_json_contract(self):

        fields = self.educational_fields()

        lines = []

        lines.append("=" * 75)
        lines.append("JSON OUTPUT CONTRACT")
        lines.append("=" * 75)
        lines.append("")
        lines.append("Return EXACTLY ONE valid JSON object.")
        lines.append("")
        lines.append("The JSON object MUST contain ALL fields listed below.")
        lines.append("")
        lines.append("Do NOT omit any field.")
        lines.append("Do NOT invent additional fields.")
        lines.append("Do NOT rename fields.")
        lines.append("Use the exact spelling shown below.")
        lines.append("")
        lines.append("If a value is not applicable, use null.")
        lines.append("")
        lines.append("FIELD LIST")
        lines.append("")

        for field in fields:

            lines.append(f'"{field}"')

        lines.append("")
        lines.append("=" * 75)
        lines.append("JSON RULES")
        lines.append("=" * 75)
        lines.append("")
        lines.append("Return ONLY JSON.")
        lines.append("Do NOT use markdown.")
        lines.append("Do NOT use code fences.")
        lines.append("Do NOT explain the answer.")
        lines.append("Do NOT add comments.")
        lines.append("Do NOT wrap inside an array.")
        lines.append("Do NOT wrap inside another object.")
        lines.append("")
        lines.append("=" * 75)
        lines.append("QUALITY CHECK")
        lines.append("=" * 75)
        lines.append("")
        lines.append("Before returning JSON verify internally:")
        lines.append("")
        lines.append("✓ Valid JSON syntax")
        lines.append("✓ Every mandatory field exists")
        lines.append("✓ Exactly four options")
        lines.append("✓ One correct option")
        lines.append("✓ Answer matches correct_option")
        lines.append("✓ Explanation matches answer")
        lines.append("✓ Difficulty matches requested set")
        lines.append("✓ No duplicate options")
        lines.append("✓ No empty educational fields")
        lines.append("")
        lines.append("Return ONLY the final validated JSON object.")

        return "\n".join(lines)
