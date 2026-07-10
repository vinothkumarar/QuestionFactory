"""
Question Factory OS
Question CSV Exporter Test

Milestone : M7
Sprint    : S2
Release   : R1
"""

from batch.batch_execution_engine import BatchExecutionEngine

from exporters.question_csv_exporter import QuestionCSVExporter

from models.production_order_model import ProductionOrderModel


queue = [

    ProductionOrderModel(

        order_id="ORDER_001",

        subject="Physics",

        unit="P1",

        chapter="CH1",

        subtopic="ST4",

        set_no="S1",

        batch_no=6,

        question_start=501,

        question_count=1

    ),

    ProductionOrderModel(

        order_id="ORDER_002",

        subject="Physics",

        unit="P1",

        chapter="CH1",

        subtopic="ST4",

        set_no="S1",

        batch_no=6,

        question_start=502,

        question_count=1

    )

]

engine = BatchExecutionEngine()

batch = engine.execute(queue)

exporter = QuestionCSVExporter()

csv_file = exporter.export(

    batch,

    "output/questions.csv"

)

print("=" * 80)
print("QUESTION CSV EXPORTER")
print("=" * 80)

print()

print("Questions Exported :", batch.total_orders)

print("CSV File           :", csv_file)

print("Success Rate       :", batch.success_rate, "%")
