"""
Question Factory OS
Factory State Model

Represents the current state of the production factory.
"""

from dataclasses import dataclass


@dataclass
class FactoryStateModel:

    project: str

    chapter: str

    subtopic: str

    set_no: str

    current_batch: int

    questions_per_batch: int = 100

    status: str = "READY"
