"""
Question Factory OS
Runtime Manager
"""

import json
from pathlib import Path
from typing import Any, cast


class RuntimeManager:
    def __init__(self) -> None:
        self.runtime_file = Path(__file__).parent.parent / "runtime.json"
        self.progress: dict[str, Any] = self.load()

    def load(self) -> dict[str, Any]:
        with open(self.runtime_file, "r", encoding="utf-8") as f:
            return cast(dict[str, Any], json.load(f))

    def save(self, runtime: dict[str, Any]) -> None:
        with open(self.runtime_file, "w", encoding="utf-8") as f:
            json.dump(runtime, f, indent=4)

        self.progress = runtime