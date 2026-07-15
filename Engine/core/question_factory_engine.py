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
from core.csv_writer import CSVWriter


class QuestionFactoryEngine:

    def __init__(self):
        self.resource_manager = ResourceManager()
        self.runtime = RuntimeManager()
        self.csv_writer = CSVWriter()
        self.folder = None

    def execute(self):

        progress = self.runtime.progress

        self.folder = self.resource_manager.ensure_questionbank_path(
            progress["current_project"],
            progress["current_chapter"],
            progress["current_subtopic"],
        )

        filename = (
            f"{progress['current_project']}_"
            f"{progress['current_chapter']}_"
            f"{progress['current_subtopic']}_"
            f"{progress['current_set']}_"
            f"{progress['current_batch']}.csv"
        )

        csv_file = self.csv_writer.create_batch_file(self.folder, filename)

        print()
        print("=" * 50)
        print("QUESTION FACTORY ENGINE")
        print("=" * 50)

        print(f"Current Node : {progress['current_node']}")
        print(f"QuestionBank : {self.folder}")
        print(f"CSV File     : {csv_file}")

        print()
        print("Engine executed successfully.")
