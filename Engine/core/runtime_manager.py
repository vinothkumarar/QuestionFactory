"""
Question Factory OS
Runtime Manager
"""

import json
from pathlib import Path


class RuntimeManager:

    def __init__(self):

        self.runtime_file = (
            Path(__file__).parent.parent
            / "runtime.json"
        )

    def load(self):

        with open(
            self.runtime_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def save(
        self,
        runtime: dict
    ):

        with open(
            self.runtime_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                runtime,
                f,
                indent=4
            )
            