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

    status: str = "PLANNED"
