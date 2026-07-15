"""
Question Factory OS

Application Entry Point

Milestone : M10
Sprint    : S1
Release   : R3
"""

from factory.factory_runner import FactoryRunner


def main():

    print("=" * 80)
    print("QUESTION FACTORY OS")
    print("PHASE 3 - QUESTION MANUFACTURING")
    print("M10-S1-R3")
    print("=" * 80)

    print()

    runner = FactoryRunner()

    total_generated = runner.run()

    print()

    print("=" * 80)
    print("PRODUCTION SUMMARY")
    print("=" * 80)

    print()

    print("Questions Generated :", total_generated)

    print()

    print("Production Completed Successfully.")

    print()


if __name__ == "__main__":

    main()
