"""
Question Factory OS
Rule Manager
"""

import json
from pathlib import Path


class RuleManager:

    def __init__(self):

        self.rules_folder = Path(__file__).parent.parent / "rules"

    def load(self, filename):

        file_path = self.rules_folder / filename

        with open(file_path, "r", encoding="utf-8") as f:

            return json.load(f)

    def difficulty(self, set_no):

        rules = self.load("difficulty_rules.json")

        return rules["difficulty_by_set"].get(set_no)
