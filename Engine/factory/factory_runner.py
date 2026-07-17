"""
Question Factory OS
Factory Runner

Milestone : M12
Sprint    : S5
Release   : R1
"""
from typing import Any, cast

from Engine.planning.queue_builder import QueueBuilder
from Engine.batch.batch_execution_engine import BatchExecutionEngine
from Engine.exporters.question_csv_exporter import QuestionCSVExporter
from Engine.validators.csv_validator import CSVValidator
from Engine.reporting.production_report import ProductionReport
from Engine.models.production_request_model import ProductionRequestModel
from Engine.repositories.factory_state_repository import FactoryStateRepository
from Engine.runtime.factory_state_manager import FactoryStateManager
from Engine.config.factory_config import (
    OUTPUT_FILE,
    PRODUCTION_ORDERS,
)


class FactoryRunner:

    def __init__(self):

        self.queue_builder = QueueBuilder()

        self.batch_engine = BatchExecutionEngine()

        self.exporter = QuestionCSVExporter()

        self.validator = CSVValidator()

        self.production_report = ProductionReport()

        self.state_repository = FactoryStateRepository()

        self.state_manager = FactoryStateManager()

    def run(self):

        print("=" * 60)
        print("QUESTION FACTORY OS")
        print("=" * 60)

        total_questions_generated = 0

        state = self.state_repository.load()

        state = self.state_manager.set_running(state)

        self.state_repository.update(state)

        
        for raw_order in PRODUCTION_ORDERS:

            order = cast(dict[str, Any], raw_order)

            request = ProductionRequestModel(
                request_id=str(order["order_id"]),
                subject=str(order["subject"]),
                unit=str(order["unit"]),
                chapter=str(order["chapter"]),
                subtopic=str(order["subtopic"]),
                set_no=str(order["set_no"]),
                total_questions=int(order["question_count"]),
            )    

            queue = self.queue_builder.build(request)

            print()

            print(f"Production Request : {request.request_id}")

            print(f"Total Batches      : {queue.total_batches}")

            print(f"Total Questions    : {queue.total_questions}")

            print()

            batch_result = self.batch_engine.execute(queue.orders)

            total_questions_generated += batch_result.successful

            csv_file = self.exporter.export(batch_result, queue.orders[0])

            print("CSV Exported       :", csv_file)

            validation = self.validator.validate(csv_file)

            print("CSV Validation     :", validation.passed)

            #
            # Production Report
            #

            self.production_report.print_report(
                request, batch_result, validation, csv_file
            )

            #
            # Runtime Commit
            #

            if validation.passed:

                for _ in range(queue.total_batches):

                    state = self.state_manager.complete_batch(state)

                self.state_repository.update(state)

        print()

        print("=" * 60)
        print("FACTORY RUN COMPLETED")
        print("=" * 60)

        print()

        print("Questions Generated :", total_questions_generated)

        print("CSV File            :", OUTPUT_FILE)

        print()

        print("Current Batch       :", state.current_batch)

        print("Factory Status      :", state.status)

        print()

        print("READY FOR IMPORT")

        return total_questions_generated
