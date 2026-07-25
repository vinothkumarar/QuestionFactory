"""
Question Factory OS v2.2

Question CSV Exporter Test
"""

from pathlib import Path

from Engine.exporters.question_csv_exporter import QuestionCSVExporter
from Engine.models.generated_question_model import GeneratedQuestionModel
from Engine.models.production_order_model import ProductionOrderModel
from Engine.models.question_batch_model import QuestionBatchModel

question = GeneratedQuestionModel(
    question_code="P1_CH1_ST4_S1_B1_Q001",
    unit_code="P1",
    chapter_code="CH1",
    subtopic_code="ST4",
    set_number=1,
    batch_number=1,
    question_text="What is the SI unit of force?",
    options=[
        "Newton",
        "Joule",
        "Pascal",
        "Watt",
    ],
    correct_option="A",
    explanation="Force is measured in Newtons.",
    difficulty="Easy",
    archetype="Concept",
    concept="SI Units",
    metadata={
        "subject_id": "Physics",
        "question_type": "MCQ",
    },
)

batch = QuestionBatchModel(
    batch_id="P1_CH1_ST4_S1_B1",
    unit_code="P1",
    chapter_code="CH1",
    subtopic_code="ST4",
    set_number=1,
    batch_number=1,
)

batch.add_question(question)

production_order = ProductionOrderModel(
    order_id="ORDER_001",
    subject="Physics",
    unit="P1",
    chapter="CH1",
    subtopic="ST4",
    set_no="S1",
    batch_no=1,
    question_start=1,
    question_count=1,
)

exporter = QuestionCSVExporter()

csv_file = exporter.export(
    batch=batch,
    production_order=production_order,
)

print("=" * 80)
print("QUESTION CSV EXPORTER")
print("=" * 80)
print(f"CSV File: {csv_file}")

assert Path(csv_file).exists()