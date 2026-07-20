"""
Question Factory OS
AUTORUN Engine

Entry point for the Question Factory Engine.
"""

from Engine.config import FACTORY_NAME, FACTORY_VERSION
from Engine.factory.factory_runner import (
    FactoryRunner,
)


def print_header():
    print("=" * 50)
    print(f"{FACTORY_NAME} v{FACTORY_VERSION}")
    print("=" * 50)
    print()


def main():

    print_header()

    runner = FactoryRunner()

    raise SystemExit(
        runner.run()
    )


if __name__ == "__main__":
    main()
