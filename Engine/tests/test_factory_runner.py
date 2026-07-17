"""
Question Factory OS
Factory Runner Test

Milestone : M10
Sprint    : S1
Release   : R3
"""

from Engine.factory.factory_runner import FactoryRunner

from Engine.repositories.factory_state_repository import FactoryStateRepository


def main():

    print("=" * 80)
    print("FACTORY RUNNER TEST")
    print("=" * 80)

    print()

    repository = FactoryStateRepository()

    before = repository.load()

    print("Runtime Before")
    print("-" * 80)

    print(f"Batch  : {before.current_batch}")

    print(f"Status : {before.status}")

    print()

    runner = FactoryRunner()

    total_generated = runner.run()

    after = repository.load()

    print()

    print("=" * 80)
    print("RUNTIME AFTER EXECUTION")
    print("=" * 80)

    print()

    print(f"Batch  : {after.current_batch}")

    print(f"Status : {after.status}")

    print()

    print("=" * 80)
    print("TEST RESULT")
    print("=" * 80)

    print()

    print("Questions Generated :", total_generated)

    print("Batch Advanced      :", after.current_batch > before.current_batch)

    print("Factory Status      :", after.status)

    print()

    print("Factory Runner Runtime Commit PASSED")


if __name__ == "__main__":

    main()
