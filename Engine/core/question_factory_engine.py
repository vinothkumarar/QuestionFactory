"""
Question Factory Engine

Central orchestrator for the Question Factory.

Responsibilities:
- Load runtime state
- Ensure required resources exist
- Coordinate future modules
"""

from core.runtime_manager import RuntimeManager
from core.resource_manager import ensure_questionbank_path


class QuestionFactoryEngine:

    def __init__(self):

        self.runtime = RuntimeManager()

    def execute(self):

        progress = self.runtime.progress

        folder = ensure_questionbank_path(
            progress["current_project"],
            progress["current_chapter"],
            progress["current_subtopic"]
        )

        print()
        print("=" * 50)
        print("QUESTION FACTORY ENGINE")
        print("=" * 50)

        print(f"Current Node : {progress['current_node']}")
        print(f"QuestionBank : {folder}")

        print()
        print("Engine executed successfully.")
