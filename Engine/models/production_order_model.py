"""
Question Factory OS
Production Order Model
"""

from dataclasses import dataclass


@dataclass
class ProductionOrderModel:

    order_id: str

    subject: str

    unit: str

    chapter: str

    subtopic: str

    set_no: str

    batch_no: int

    question_start: int

    question_count: int

    concept_id: str = ""

    concept: str = ""

    qp_id: str = ""

    question_possibility: str = ""

    archetype_id: str = ""

    archetype: str = ""

    variation_capacity: str = ""

    variation_dimensions: list[str] | None = None

    subject_name: str = ""

    unit_name: str = ""

    chapter_name: str = ""

    subtopic_name: str = ""

    subject_description: str = ""

    unit_description: str = ""

    chapter_description: str = ""

    subtopic_description: str = ""

    status: str = "PLANNED"
