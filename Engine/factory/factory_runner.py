"""
Question Factory OS
Factory Runner

Milestone : M9
Sprint    : S4
Release   : R1
"""

from planning.queue_builder import QueueBuilder

from batch.batch_execution_engine import BatchExecutionEngine

from exporters.question_csv_exporter import (
    QuestionCSVExporter
)

from validators.csv_validator import CSVValidator

from models.production_request_model import (
    ProductionRequestModel
)

from config.factory_config import (
    OUTPUT_FILE,
    PRODUCTION_ORDERS
)


class FactoryRunner:

    def __init__(self):

        self.queue_builder = QueueBuilder()

        self.batch_engine = BatchExecutionEngine()

        self.exporter = QuestionCSVExporter()

        self.validator = CSVValidator()

    def run(self):

        print("=" * 60)
        print("QUESTION FACTORY OS")
        print("=" * 60)

        total_questions_generated = 0

        for order in PRODUCTION_ORDERS:

            request = ProductionRequestModel(

                request_id=order["order_id"],

                subject=order["subject"],

                unit=order["unit"],

                chapter=order["chapter"],

                subtopic=order["subtopic"],

                set_no=order["set_no"],

                total_questions=order["question_count"]

            )

            queue = self.queue_builder.build(
                request
            )

            print()

            print(
                f"Production Request : {request.request_id}"
            )

            print(
                f"Total Batches      : {queue.total_batches}"
            )

            print(
                f"Total Questions    : {queue.total_questions}"
            )

            print()

            batch_result = self.batch_engine.execute(
                queue.orders
            )

            total_questions_generated += (
                batch_result.successful
            )

            csv_file = self.exporter.export(

                batch_result,

                OUTPUT_FILE

            )

            print(
                "CSV Exported       :",
                csv_file
            )

            validation = self.validator.validate(
                csv_file
            )

            print(
                "CSV Validation     :",
                validation.passed
            )

        print()

        print("=" * 60)
        print("FACTORY RUN COMPLETED")
        print("=" * 60)

        print()

        print(
            "Questions Generated :",
            total_questions_generated
        )

        print(
            "CSV File            :",
            OUTPUT_FILE
        )

        print()

        print("READY FOR IMPORT")

        return total_questions_generated
        