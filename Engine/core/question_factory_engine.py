"""
Question Factory Engine

Central orchestrator for the Question Factory.

Responsibilities:
- Load runtime state
- Ensure required resources exist
- Coordinate future modules
"""

from core.runtime_manager import RuntimeManager
from core.resource_manager import ResourceManager


class QuestionFactoryEngine:

    def __init__(self):
        self.resource_manager = ResourceManager()
        self.runtime = RuntimeManager()
        self.folder = None

    def execute(self):

        progress = self.runtime.progress

        self.folder = self.resource_manager.ensure_questionbank_path(
            progress["current_project"],
            progress["current_chapter"],
            progress["current_subtopic"]
        )

        print()
        print("=" * 50)
        print("QUESTION FACTORY ENGINE")
        print("=" * 50)

        print(f"Current Node : {progress['current_node']}")
        print(f"QuestionBank : {self.folder}")

        print()
        print("Engine executed successfully.")