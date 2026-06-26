"""
Question Factory OS
AUTORUN Engine

Entry point for the Question Factory Engine.
"""

from config import FACTORY_NAME, FACTORY_VERSION
from core.question_factory_engine import QuestionFactoryEngine


def print_header():
    print("=" * 50)
    print(f"{FACTORY_NAME} v{FACTORY_VERSION}")
    print("=" * 50)
    print()


def main():

    print_header()

    engine = QuestionFactoryEngine()

    engine.execute()


if __name__ == "__main__":
    main()
