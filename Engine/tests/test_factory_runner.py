"""
Question Factory OS
Factory Runner Test

Milestone : M9
Sprint    : S4
Release   : R1
"""

from factory.factory_runner import FactoryRunner


def main():

    print("=" * 80)
    print("FACTORY RUNNER TEST")
    print("=" * 80)

    print()

    runner = FactoryRunner()

    total_generated = runner.run()

    print()

    print("=" * 80)
    print("TEST RESULT")
    print("=" * 80)

    print()

    print(
        "Questions Generated :",
        total_generated
    )

    print()

    print("Factory Runner Test PASSED")


if __name__ == "__main__":

    main()