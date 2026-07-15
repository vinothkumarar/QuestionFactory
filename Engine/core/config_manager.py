"""
Question Factory OS
Configuration Manager
"""

import json
from pathlib import Path


class ConfigManager:

    def __init__(self):

        self.config_path = (
            Path(__file__).parent.parent / "config" / "engine_config.json"
        )

    def load(self):

        with open(self.config_path, encoding="utf-8") as file:

            return json.load(file)
