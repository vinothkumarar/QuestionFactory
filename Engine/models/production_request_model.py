"""
Question Factory OS
Production Request Model

Milestone : M9
Sprint    : S1
Release   : R1
"""

from dataclasses import dataclass


@dataclass
class ProductionRequestModel:
    """
    Represents a production request submitted
    by the factory operator.

    A Queue Builder will convert this request
    into one or more ProductionOrderModel objects.
    """

    request_id: str

    subject: str

    unit: str

    chapter: str

    subtopic: str

    set_no: str

    total_questions: int

    batch_size: int = 100

    language: str = "English"

    difficulty_profile: str = "Blueprint"

    output_file: str = "output/questions.csv"

    blueprint_version: str = "v3.1"
