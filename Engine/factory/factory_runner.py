"""
Question Factory OS
Factory Runner

Milestone : M8
Sprint    : S2
Release   : R1
"""

from models.production_order_model import ProductionOrderModel

from batch.batch_execution_engine import BatchExecutionEngine

from exporters.question_csv_exporter import (
    QuestionCSVExporter
)

from validators.csv_validator import CSVValidator

from config.factory_config import (
    OUTPUT_FILE,
    PRODUCTION_ORDERS
)


class FactoryRunner:

    def __init__(self):

        self.batch_engine = BatchExecutionEngine()

        self.exporter = QuestionCSVExporter()

        self.validator = CSVValidator()

    def run(self):

        print("=" * 60)
        print("QUESTION FACTORY OS")
        print("=" * 60)

        #
        # Build Production Queue
        #

        queue = []

        for order in PRODUCTION_ORDERS:

            queue.append(

                ProductionOrderModel(**order)

            )

        print()

        print("Production Orders :", len(queue))

        #
        # Execute Batch
        #

        batch = self.batch_engine.execute(
            queue
        )

        print("Questions Generated :", batch.successful)

        #
        # Export CSV
        #

        csv_file = self.exporter.export(

            batch,

            OUTPUT_FILE

        )

        print("CSV Exported :", csv_file)

        #
        # Validate CSV
        #

        validation = self.validator.validate(
            csv_file
        )

        print("CSV Validation :", validation.passed)

        print()

        if validation.passed:

            print("READY FOR IMPORT")

        else:

            print("CSV VALIDATION FAILED")

        return batch
        