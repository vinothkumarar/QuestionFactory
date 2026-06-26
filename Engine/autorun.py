"""
Question Factory OS
AUTORUN Engine

Phase 6.1

Reads the current runtime state and displays it.
"""

from core.logger import get_logger
from core.state_manager import load_progress
from config import FACTORY_NAME, FACTORY_VERSION
from core.runtime_manager import RuntimeManager


def print_header():
    print("=" * 50)
    print(f"{FACTORY_NAME} v{FACTORY_VERSION}")
    print("=" * 50)
    print()


def main():

    logger = get_logger()

    logger.info("AUTORUN Started")

    print_header()

    runtime = RuntimeManager()
    progress = runtime.progress

    
    from core.resource_manager import ensure_questionbank_path
    folder = ensure_questionbank_path(
    progress["current_project"],
    progress["current_chapter"],
    progress["current_subtopic"]
)

print()
print("QuestionBank Path")
print(folder)

    print("Current Runtime State")
    print("-" * 50)

    print(f"Project      : {progress.get('current_project')}")
    print(f"Chapter      : {progress.get('current_chapter')}")
    print(f"Subtopic     : {progress.get('current_subtopic')}")
    print(f"Set          : {progress.get('current_set')}")
    print(f"Batch        : {progress.get('current_batch')}")
    print(f"Question From: Q{progress.get('question_start'):03}")
    print(f"Question To  : Q{progress.get('question_end'):03}")
    print(f"Current Node : {progress.get('current_node')}")
    print(f"Status       : {progress.get('status')}")

    print()
    print("AUTORUN State Engine loaded successfully.")

    logger.info("AUTORUN Completed Successfully")


if __name__ == "__main__":
    main()
