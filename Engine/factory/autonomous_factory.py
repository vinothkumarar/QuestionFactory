"""
Question Factory OS
Autonomous Factory

Milestone : M13
Sprint    : S2
Release   : R3

Runs an entire Production Plan automatically.
"""


from Engine.factory.factory_runner import FactoryRunner

from Engine.scheduler.production_scheduler import ProductionScheduler

from Engine.repositories.factory_state_repository import (
    FactoryStateRepository,
)

from Engine.models.production_plan_model import (
    ProductionPlanModel,
)


class AutonomousFactory:
    """
    Autonomous Manufacturing Controller

    Responsibilities

    • Build production schedule
    • Execute every batch
    • Maintain runtime
    • Print production summary
    """

    def __init__(self):

        self.scheduler = ProductionScheduler()

        self.runner = FactoryRunner()

        self.state_repository = FactoryStateRepository()

    def execute(self, plan: ProductionPlanModel):

        print("=" * 80)
        print("QUESTION FACTORY OS")
        print("AUTONOMOUS FACTORY")
        print("=" * 80)

        print()

        print("Loading Production Plan...")

        requests = self.scheduler.build_schedule(plan)

        print(f"Total Batches    : {len(requests)}")

        print(f"Questions/Batch  : " f"{plan.questions_per_batch}")

        print()

        total_questions = 0

        completed_batches = 0

        failed_batches = 0

        for request in requests:

            print()

            print("=" * 80)
            print(f"Starting Request {request.request_id}")
            print("=" * 80)

            #
            # Execute Factory
            #

            generated = self.runner.run()

            total_questions += generated

            if generated == request.total_questions:

                completed_batches += 1

            else:

                failed_batches += 1

                print()

                print(f"Request {request.request_id} failed.")

                if plan.stop_on_failure:

                    print()

                    print("Stopping Production...")

                    break

        print()

        print("=" * 80)
        print("AUTONOMOUS FACTORY SUMMARY")
        print("=" * 80)

        print()

        print(f"Completed Batches : " f"{completed_batches}")

        print(f"Failed Batches    : " f"{failed_batches}")

        print(f"Questions Created : " f"{total_questions}")

        print()

        state = self.state_repository.load()

        print(f"Current Batch     : " f"{state.current_batch}")

        print(f"Factory Status    : " f"{state.status}")

        print()

        print("AUTONOMOUS RUN COMPLETED")

        return total_questions
